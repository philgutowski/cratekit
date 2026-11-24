# Mutation table: u334-replay-before-8

Measured by `scripts/mutate.py` on 2026-11-24 04:10 UTC, branch `HEAD` at `89c9e120`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 322.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:10 UTC for commit `89c9e120f5d4`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 57, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u220.A14_multiset_agrees` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 1 | killed |
| `u220.A17_settle_once` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 4 | killed |
| `u220.A1_front_target` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 12 | killed |
| `u220.A23_pause_index` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 1 | killed |
| `u226.M10_settle_lag_known_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 5 | killed |
| `u226.M11_settle_kept_ignored` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 1 | killed |
| `u226.M13_removal_window_wrong` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 2 | killed |
| `u226.M15_wait_uncounted` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 2 | killed |
| `u226.M17_removal_positions_unsettled` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 54 | 3 | killed |
| `u226.M18_waited_unformatted` | `src/cratekit/modules/outbound/tidal_account.py` | maintainer | 9 file(s) | 23216 | 0 (promoted) | zero |
| `u226.M7_reading_takes_window` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 5 | killed |
| `u226.M8_unpaged_first` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 3 | killed |
| `u226.M9_positions_no_lag_refusal` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 5 | killed |
| `u231.M4_resend_with_the_stale_tag` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 6 | killed |
| `u231.M5_positions_not_advanced` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 38 | killed |
| `u231.M6_settle_lag_taken` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 4 | killed |
| `u255.C4_held_before_read_and_playlist_keeps_the_hold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 24 | 2 | killed |
| `u255.C8_no_open_before_and_retry_opens_raw` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 3 | killed |
| `u255.M10_failed_attempt_keeps_the_hold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 5 | killed |
| `u255.M11_retry_opens_raw` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 2 | killed |
| `u255.M12_add_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 7 | killed |
| `u255.M13_add_retried_twice` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 3 | killed |
| `u255.M1_playlist_keeps_the_hold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 2 | killed |
| `u255.M2_membership_reads_the_held_object` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 3 | killed |
| `u255.M3_membership_holds_nothing` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 6 | killed |
| `u255.M5_membership_reuses_the_hold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 2 | killed |
| `u255.M6_held_never_stores` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 3 | killed |
| `u255.M7_held_always_opens` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 9 | killed |
| `u255.M9_every_attempt_opens` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 11 | killed |
| `u255.S1_member_already_on` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 2 | killed |
| `u255.S2_read_back_trusts_the_cache` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 3 | killed |
| `u255.S3_answer_absent_passes` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 1 | killed |
| `u255.S4_added_not_remembered` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 5 | killed |
| `u261.O2_account_drops_the_app` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 209 | 2 | killed |
| `u270.A1_failed_attempt_reopens` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 159 | 2 | killed |
| `u309-z.U10_delete_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 429 | 1 | killed |
| `u309-z.U7_created_needs_identifier` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 429 | 2 | killed |
| `u309-z.U8_served_forgets_membership` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 429 | 1 | killed |
| `u309.U11_delete_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 429 | 5 | killed |
| `u309.U9_delete_answered_false` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 429 | 6 | killed |
| `r1032.A10_reason_words_reworded` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 3 file(s) | 241 | 6 | killed |
| `r1032.A11_empty_album_narrows` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 1 | killed |
| `r1032.A1_adapter_ignores_any_agreeing` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 13 | killed |
| `r1032.A2_tie_always_broken` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 4 file(s) | 317 | 15 | killed |
| `r1032.A3_unreadable_tie_broken` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 3 | killed |
| `r1032.A6_first_listed_not_lowest` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 7 | killed |
| `r1032.A7_lowest_by_characters` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 1 | killed |
| `r1032.A8_album_narrow_drops_all` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 11 | killed |
| `r1032.A9_album_narrow_unfolded` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 1 | killed |
| `r1032.S1_protocol_default_on` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 15 | killed |
| `r1313.T1_account_skips_the_classifier` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 3 file(s) | 229 | 5 | killed |
| `r356-a.A10_provider_title_read_one_way_only` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r356-a.A11_row_title_read_one_way_only` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r356-a.A12_reason_outlives_its_match` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r356-a.A14_no_joiner_words` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r356-a.A1_first_agreeing_rather_than_the_only_one` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 27 | killed |
| `r356-a.A2_unreadable_track_no_longer_stops_rule_one` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 2 | killed |
| `r356-a.A3_any_hearted_rather_than_the_only_hearted` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 4 | killed |
| `r356-a.A4_hearts_asked_of_every_track` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r356-a.A5_withdrawn_track_is_a_candidate` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 2 | killed |
| `r356-a.A7_artist_not_compared` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 2 | killed |
| `r356-a.A8_first_billed_artist_not_required` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r356-a.A9_row_may_name_an_artist_nobody_bills` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r572.A2_first_named` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r572.A4_no_fold` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 3 | killed |
| `r572.A5_album_among_all` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r879-b.T1_one_track_never_asked_to_agree` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `u208.M19_adapter_never_records_tie` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 134 | 5 | killed |
| `u208.M20_adapter_stale_tie` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 134 | 1 | killed |
| `u208.M21_adapter_every_choice_a_tie` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 134 | 1 | killed |
| `u208.M22_adapter_hearts_half` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 134 | 1 | killed |
| `u27-reports-round-2.S5b_engine_default_drift` | `src/cratekit/modules/reports/duplicates.py` | user | 2 file(s) | 382 | 3 | killed |
| `r367.E1_a_failed_transfer_is_unread` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 283 | 15 | killed |
| `u48-author.P3_two_codes_collapsed_to_one` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 229 | 2 | killed |
| `r154-a.A3_named_shape_check` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 9 | killed |
| `r154-b.B1_named_mismatch` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 8 | killed |
| `r154-b.B7_walk_order` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 5 | killed |
| `r338-a.B8_contained_share_copied_twice` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 8 | killed |
| `r338-b.R4_empty_listing_read_as_held` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 1 | killed |
| `r338-b.R5_pulled_under_the_watch` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 1 | killed |
| `r338-b.R6_switch_ignored` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 1 | killed |
| `r338-b.R9_contained_restore_asks_about_a_share` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 2 | killed |
| `r367.G12_listing_results_are_discarded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 2 | killed |
| `r367.G1_always_copy_the_restored_sidecar` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 6 | killed |
| `r367.G3_membership_is_inverted` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 4 | killed |
| `r367.G4_the_inventory_restored_flag_is_ignored` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 4 | killed |
| `r367.G5_absent_sidecars_are_not_recorded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 2 | killed |
| `r592-b.B6_restore_mirror_carries_the_database` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 3 file(s) | 23216 | 0 (promoted) | zero |
| `u211.B1_backup_database_portion_refuses_alone` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 3 file(s) | 167 | 1 | killed |
| `u105-a.E10_parts_archived` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 1 | killed |
| `u105-a.E11_join_dir_removed` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 1 | killed |
| `u105-a.E12_join_rf64` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 1 | killed |
| `u105-a.E13_joined_suffix` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 5 | killed |
| `u105-a.E14_single_part_name` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 4 | killed |
| `u105-a.E15_payload_parts_conditional` | `src/cratekit/modules/tools/mastering.py` | maintainer | 3 file(s) | 248 | 1 | killed |
| `u105-a.E1_lufs_range_removed` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 4 | killed |
| `u105-a.E2_lufs_high_bound` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 2 | killed |
| `u105-a.E3_lufs_nan` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 2 | killed |
| `u105-a.E4_duplicate_part` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 1 | killed |
| `u105-a.E5_mixed_containers` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 1 | killed |
| `u105-a.E6_joined_output_exists` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 1 | killed |
| `u105-a.E7_layout_rate` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 1 | killed |
| `u105-a.E8_layout_channels` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 1 | killed |
| `u105-a.E9_layout_codec` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 1 | killed |
| `u311.C5_binaries_out_of_order` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 30 | killed |
| `u44-author-round-2.A1_archive_verify_dropped` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 246 | 1 | killed |
| `u44-author-round-2.A4_digest_reads_first_chunk_only` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 246 | 1 | killed |
| `u44-author.A2_archive_collision_skips` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 246 | 3 | killed |
| `u44-author.B1_output_unread` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 246 | 3 | killed |
| `u44-author.B2_output_existence_only` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 246 | 1 | killed |
| `u112-b.A6_exported_not_product_made` | `src/cratekit/organize/account.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u112.A2_pending_loses` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.A3_retired_unnumbered` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.A4_in_folder_listed` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.A7_no_proof_read` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 8 | killed |
| `u116.M9_yours_lists_moved` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 3 | killed |
| `u137-b.A3_marks_gate` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 5 | killed |
| `u137.A1_labels_gate` | `src/cratekit/organize/account.py` | user | 2 file(s) | 121 | 9 | killed |
| `u137.A2_sets_gate` | `src/cratekit/organize/account.py` | user | 2 file(s) | 121 | 10 | killed |
| `u137.A5_filing_for_yours` | `src/cratekit/organize/account.py` | user | 2 file(s) | 121 | 2 | killed |
| `u137.A8_labels_module_off` | `src/cratekit/organize/account.py` | user | 2 file(s) | 121 | 1 | killed |
| `u142.S13_unread_reads_as_none` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 1 | killed |
| `u142.S14_any_inspiration_proves_every_set` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 1 | killed |
| `u142.S15_second_proof_ignored` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 6 | killed |
| `u142.S16_pass_is_not_the_set` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 1 | killed |
| `u142.S17_proof_not_named` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 1 | killed |
| `u142.S18_wait_names_no_folder_always` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 3 | killed |
| `u142.S20_retitled_detail_called_marked` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 1 | killed |
| `u142.S23_prefix_only_said_as_a_move` | `src/cratekit/organize/account.py` | user | 1 file(s) | 97 | 1 | killed |
| `u143-e.C1_yours_empties` | `src/cratekit/organize/account.py` | user | 2 file(s) | 121 | 1 | killed |
| `r1031.M15_seen_not_seeded` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 168 | 3 | killed |
| `r1031.M16_report_records` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 168 | 2 | killed |
| `r1031.M17_apply_records_no_miss` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 71 | 5 | killed |
| `r1031.M18_unrecordable_ledger_refuses_the_plan` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 71 | 1 | killed |
| `r1031.M19_unfreezable_plan_refuses` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 71 | 1 | killed |
| `r1031.M20_signature_constant` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 71 | 1 | killed |
| `u147-d.A2_retired_unnamed` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 38 | 1 | killed |
| `u147-d.A3_twin_folders_read` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 38 | 1 | killed |
| `u147-d.A5_source_title` | `src/cratekit/organize/account_mirror.py` | user | 1 file(s) | 4 | 1 | killed |
| `u147-d.A6_file_code_trusted` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 38 | 1 | killed |
| `u150.A1_inbox_retires` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 70 | 1 | killed |
| `u150.A2_present_titled` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 70 | 1 | killed |
| `u150.A4_listed_step` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 163 | 1 | killed |
| `u150.A5_deletes_named` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 163 | 1 | killed |
| `u150.A7_landed_two_tracks` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 78 | 1 | killed |
| `u150.A8_landed_workflow` | `src/cratekit/organize/account_mirror.py` | maintainer | 2 file(s) | 78 | 1 | killed |
| `u204.A1_adopt_landed` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 224 | 1 | killed |
| `u207.M3_mirror_read_never_screens` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 71 | 1 | killed |
| `u222.M11_decided_freeze_shown` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 255 | 2 | killed |
| `u222.M12_unshown_not_said` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M19_stale_on_every_run` | `src/cratekit/organize/account_mirror.py` | maintainer | 6 file(s) | 255 | 1 | killed |
| `u222.M1_overlay_not_read` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 255 | 3 | killed |
| `u222.M20_every_step_reworded` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 255 | 2 | killed |
| `u222.M25_steps_not_frozen` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 255 | 6 | killed |
| `u227.R8_reader_not_passed` | `src/cratekit/organize/account_mirror.py` | user | 7 file(s) | 187 | 2 | killed |
| `u230.M18_titles_not_recorded` | `src/cratekit/organize/account_mirror.py` | user | 11 file(s) | 212 | 3 | killed |
| `u230.M19_every_title` | `src/cratekit/organize/account_mirror.py` | user | 11 file(s) | 212 | 1 | killed |
| `u230.M20_queue_not_passed` | `src/cratekit/organize/account_mirror.py` | user | 11 file(s) | 212 | 3 | killed |
| `u236.M10_reader_no_time_check` | `src/cratekit/organize/account_mirror.py` | user | 8 file(s) | 225 | 3 | killed |
| `u236.M11_reader_never_placed` | `src/cratekit/organize/account_mirror.py` | user | 8 file(s) | 225 | 1 | killed |
| `u236.M12_reader_short_branch` | `src/cratekit/organize/account_mirror.py` | user | 8 file(s) | 225 | 1 | killed |
| `u309-z2.U21_reading_unread_listed` | `src/cratekit/organize/account_mirror.py` | user | 5 file(s) | 118 | 1 | killed |
| `u309-z2.U22_keep_newest_time` | `src/cratekit/organize/account_mirror.py` | user | 4 file(s) | 126 | 1 | killed |
| `u309.U23_shared_once_error_cached` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 48 | 3 | killed |
| `u112-b.C7_outcome_always_ok` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.C1_report_asks` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 52 | killed |
| `u112.C5_unexpected_failure_stops` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.C6_failure_never_raised` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 3 | killed |
| `u137.C1_named_always` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 17 | killed |
| `u137.C2_only_dropped` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 23 | killed |
| `u137.C3_choices_dropped` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 1 | killed |
| `u222.M21_cli_message_unchanged` | `src/cratekit/organize/cli.py` | user | 6 file(s) | 255 | 2 | killed |
| `u222.M22_cli_detail_unchanged` | `src/cratekit/organize/cli.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M23_cli_empty_stale_reworded` | `src/cratekit/organize/cli.py` | user | 6 file(s) | 255 | 1 | killed |
| `u267.M1_report_shares_nothing` | `src/cratekit/organize/cli.py` | user | 3 file(s) | 149 | 5 | killed |
| `u267.M2_applying_run_shares` | `src/cratekit/organize/cli.py` | user | 2 file(s) | 111 | 1 | killed |
| `u267.M3_report_never_closes` | `src/cratekit/organize/cli.py` | user | 2 file(s) | 111 | 4 | killed |
| `u116.M10_year_check` | `src/cratekit/organize/filing.py` | user | 1 file(s) | 14 | 1 | killed |
| `u116.M12_nested_folders_ignored` | `src/cratekit/organize/filing.py` | user | 1 file(s) | 97 | 1 | killed |
| `u116.M13_utc_year` | `src/cratekit/organize/filing.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u116.M2_set_rule_dropped` | `src/cratekit/organize/filing.py` | user | 1 file(s) | 97 | 1 | killed |
| `u116.M5_ambiguous_moves_anyway` | `src/cratekit/organize/filing.py` | user | 1 file(s) | 97 | 1 | killed |
| `u116.M6_no_adopt` | `src/cratekit/organize/filing.py` | user | 1 file(s) | 97 | 2 | killed |
| `u131.K1_mine_made_only` | `src/cratekit/organize/filing.py` | user | 2 file(s) | 111 | 1 | killed |
| `u131.K2_exports_rule` | `src/cratekit/organize/filing.py` | user | 2 file(s) | 111 | 2 | killed |
| `u131.K3_product_made_left` | `src/cratekit/organize/filing.py` | user | 2 file(s) | 111 | 1 | killed |
| `u143-b.F1_debris_first` | `src/cratekit/organize/filing.py` | user | 3 file(s) | 166 | 16 | killed |
| `u143-b.F2_empty_unclaimed` | `src/cratekit/organize/filing.py` | user | 3 file(s) | 166 | 1 | killed |
| `u143-b.F4_legacy_record_stale` | `src/cratekit/organize/filing.py` | user | 3 file(s) | 166 | 1 | killed |
| `u242.M23_filing_dates_a_found_prefix` | `src/cratekit/organize/filing.py` | user | 3 file(s) | 198 | 3 | killed |
| `u309-z2.U18_part_way_step_again` | `src/cratekit/organize/filing.py` | user | 2 file(s) | 152 | 1 | killed |
| `u309-z2.U20_year_folder_reserved_once` | `src/cratekit/organize/filing.py` | user | 2 file(s) | 152 | 1 | killed |
| `u309.U19_part_way_totals` | `src/cratekit/organize/filing.py` | user | 2 file(s) | 152 | 2 | killed |
| `r1295.M10_unread_off_misses` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 4 | killed |
| `r1295.M11_again_drops_unread` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `r1295.M12_setrow_keeps_no_unread` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `r1295.M13_unread_miss_no_id` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 4 | killed |
| `r1295.M14_unread_miss_blank_title` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 3 | killed |
| `r1295.M15_plan_passes_no_unread` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 4 | killed |
| `r1295.M17_skip_guard` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `r1295.M1_refused_row_fatal` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 6 | killed |
| `r1295.M2_no_id_named` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1295.M3_read_positions_renumbered` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1295.M4_unread_positions_renumbered` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 3 | killed |
| `r1295.M5_all_unread_branch` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `r1295.M6_none_read_uncapped` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1295.M7_none_read_rest_uncounted` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1295.M8_none_read_withheld_dropped` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1295.M9_misses_unsorted` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-a.A1_skip_rule` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `u144-a.A2_two_of_one_name` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-a.A4_sets_folder_name` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `u144-a.A5_recorded_folder` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-a.A6_set_name_spelling` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-a.A7_only_matched` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 8 | killed |
| `u144-a.A8_empty_not_written` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `u144-b.B1_unnamed_membership` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-b.B2_stale_digest` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-b.B4_convergence_latch` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-b.B5_read_back_exact` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-b.B6_read_back_missing` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-b.B7_writes_the_members` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 8 | killed |
| `u144-b.B8_commit_recorded` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-c.C1_again_now_held` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-c.C2_folder_unread` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-c.C4_missed_coefficient` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u246.S5_inspiration_held_empty` | `src/cratekit/organize/inspiration.py` | user | 4 file(s) | 329 | 9 | killed |
| `u246.S6_inspiration_planned_live` | `src/cratekit/organize/inspiration.py` | user | 4 file(s) | 329 | 1 | killed |
| `r1289.M14_mirror_unread_branch` | `src/cratekit/organize/mirror_downloads.py` | user | 3 file(s) | 103 | 1 | killed |
| `r1289.M15_mirror_reads_whole` | `src/cratekit/organize/mirror_downloads.py` | user | 3 file(s) | 103 | 1 | killed |
| `r1289.M16_mirror_why` | `src/cratekit/organize/mirror_downloads.py` | user | 1 file(s) | 37 | 1 | killed |
| `r1289.M17_mirror_listing_refusal` | `src/cratekit/organize/mirror_downloads.py` | user | 1 file(s) | 37 | 1 | killed |
| `u204.D1_one_queue_per_track` | `src/cratekit/organize/mirror_downloads.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.D2_write_rereads_queue` | `src/cratekit/organize/mirror_downloads.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.D3_owned_recording` | `src/cratekit/organize/mirror_downloads.py` | user | 6 file(s) | 224 | 2 | killed |
| `u204.D4_never_lands_named` | `src/cratekit/organize/mirror_downloads.py` | user | 6 file(s) | 224 | 2 | killed |
| `u227.R10_one_approval` | `src/cratekit/organize/mirror_downloads.py` | user | 7 file(s) | 187 | 1 | killed |
| `u227.R23_person_digest` | `src/cratekit/organize/mirror_downloads.py` | user | 7 file(s) | 187 | 1 | killed |
| `u227.R9_before_queue` | `src/cratekit/organize/mirror_downloads.py` | user | 7 file(s) | 187 | 1 | killed |
| `u230.M15_source_blank` | `src/cratekit/organize/mirror_downloads.py` | user | 11 file(s) | 212 | 6 | killed |
| `u230.M16_unread_raises` | `src/cratekit/organize/mirror_downloads.py` | user | 11 file(s) | 212 | 1 | killed |
| `u267.M13_downloads_owned_opens_its_own` | `src/cratekit/organize/mirror_downloads.py` | user | 2 file(s) | 51 | 1 | killed |
| `u201-composites.C5_leave_nothing` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 187 | 6 | killed |
| `u201.O1_latch` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 187 | 1 | killed |
| `u201.O2_stale` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 187 | 1 | killed |
| `u201.O3_target_bucket` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 187 | 6 | killed |
| `u204.O2_unfavourite_leaves_months` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.O3_quarter_refused` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.O4_colour` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.O5_batch_live` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.O6_inbox_latch` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.O7_restore_detected` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u236.M13_write_records_no_month` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 225 | 6 | killed |
| `u236.M14_write_wrong_time` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 225 | 6 | killed |
| `u236.M15_settle_month_title` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 225 | 8 | killed |
| `u236.M16_settle_any_favourite` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 225 | 1 | killed |
| `u340.R17_edit_second_path_off` | `src/cratekit/organize/mirror_edits.py` | user | 3 file(s) | 103 | 1 | killed |
| `u340.R18_edit_off_other` | `src/cratekit/organize/mirror_edits.py` | user | 2 file(s) | 61 | 3 | killed |
| `r1031.M21_run_id_unchecked` | `src/cratekit/organize/mirror_frozen.py` | user | 2 file(s) | 134 | 1 | killed |
| `r1031.M22_record_binding_unchecked` | `src/cratekit/organize/mirror_frozen.py` | user | 2 file(s) | 134 | 2 | killed |

## Zero rows and what they owe

- `u226.M18_waited_unformatted` (maintainer facing): maintainer facing, composite not required
- `r592-b.B6_restore_mirror_carries_the_database` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u112-b.A6_exported_not_product_made` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u116.M13_utc_year` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u220.A14_multiset_agrees`

_settled: read any reading as holding what is known

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A14_multiset_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`

Old text:

```
            return sorted(reading) == sorted(known)
```

New text:

```
            return True
```

### `u220.A17_settle_once`

_settled: take one reading only, never again after a pause

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A17_settle_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_expected_one_is_read_again`
  - `tests/test_outbound_order.py::test_a_reading_that_never_agrees_with_the_expected_one_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_the_reading_after_adds_that_lags_them_is_read_again_before_the_first_move`

Old text:

```
        last: CratekitError | None = None
        for attempt in range(ORDER_REREADS + 1):
```

New text:

```
        last: CratekitError | None = None
        for attempt in range(1):
```

### `u220.A1_front_target`

order_tracks: move each track to the playlist's length instead of the front, the move whose landing depends on how the provider counts

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A1_front_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 12 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_every_move_is_to_the_front_where_both_ways_of_counting_agree`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`
  - `tests/test_outbound_order.py::test_the_tracks_before_the_kept_tail_are_moved_last_first`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`

Old text:

```
playlist.move_by_indices([at], 0)
```

New text:

```
playlist.move_by_indices([at], len(before))
```

### `u220.A23_pause_index`

_pause: index the pauses by the attempt with no repeat of the last

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A23_pause_index`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_more_412s_than_pauses_repeat_the_last_pause`

Old text:

```
    return ORDER_PAUSES[min(attempt, len(ORDER_PAUSES)) - 1]
```

New text:

```
    return ORDER_PAUSES[attempt - 1]
```

### `u226.M10_settle_lag_known_only`

_settled: a lagging window is read again only when something is known

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M10_settle_lag_known_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_never_catches_up_refuses_with_nothing_moved`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_an_order_whose_later_pages_lag_too_is_held_with_nothing_moved`

Old text:

```
                if problem == "window-lags":

```

New text:

```
                if problem == "window-lags" and known is not None:

```

### `u226.M11_settle_kept_ignored`

_settled: a caller's kept wording is ignored for the order's

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M11_settle_kept_ignored`
- Moved: _settled's if kept is None fallback became the parameter's default, no track was moved, since no caller ever passed pauses_from; ignoring the caller's wording is now a reassignment to that default at the top of _settled, the same effect the reverted condition had
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`

Old text:

```
        note = self._noting(identifier, after)
        last: CratekitError | None = None
        for attempt in range(ORDER_REREADS + 1):
```

New text:

```
        kept = "no track was moved"
        note = self._noting(identifier, after)
        last: CratekitError | None = None
        for attempt in range(ORDER_REREADS + 1):
```

### `u226.M13_removal_window_wrong`

_removal_read_back: a lagging window is read as a wrong track gone, refused at once

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M13_removal_window_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`

Old text:

```
                tracks = "window"

```

New text:

```
                tracks = None

```

### `u226.M15_wait_uncounted`

_paused: the pause is taken and not counted in the record

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M15_wait_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_pause_after_a_412_is_counted_in_the_moves_record`

Old text:

```
        self._sleep(seconds)
        note["waited"] += seconds

```

New text:

```
        self._sleep(seconds)

```

### `u226.M17_removal_positions_unsettled`

remove_tracks: the positions read once with no reread of a lag, as before round one's fix

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M17_removal_positions_unsettled`
- Moved: remove_tracks now reads its positions in one conditional expression instead of an if block, so the settled read is replaced by the single positions read under the same wanted condition
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`
- Collected: 54 against a baseline of 54
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`

Old text:

```
        playlist, before = (
            self._settled(
                identifier, None, after="removal positions", kept="nothing was taken off it"
            )
            if wanted
            else (None, [])
        )
```

New text:

```
        playlist = self._playlist(identifier) if wanted else None
        before = self._positions(identifier, playlist) if wanted else []
```

### `u226.M18_waited_unformatted`

_waited: seconds named as 7.0 rather than 7

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M18_waited_unformatted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return f"{seconds:g}"
```

New text:

```
    return f"{seconds}"
```

### `u226.M7_reading_takes_window`

_reading: the window read is the reading even when the unpaged read is whole

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M7_reading_takes_window`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_planned_from_a_lagging_window_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_and_unpaged_read_does_not_is_taken_as_done`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_an_order_planned_after_a_lagging_window_is_planned_from_the_unpaged_read`

Old text:

```
            unpaged if window == listing.WINDOW_UNPAGED else paged,
```

New text:

```
            paged,
```

### `u226.M8_unpaged_first`

_reading: the unpaged read taken before the window, so the window's tag is carried

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M8_unpaged_first`
- Moved: _reading in tidal_account.py now reads the window into paged in one line instead of through a tracks name, so the same two reads are swapped there, the unpaged one taken first
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_planned_from_a_lagging_window_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`

Old text:

```
        paged = [listing.row_id(track) for track in self._listed(playlist_id, playlist)]
        unpaged = [
            listing.row_id(track)
            for track in self._read(
                f"read the playlist {playlist_id}",
                lambda: listing.playlist_tracks_unpaged(playlist),
            )
        ]
```

New text:

```
        unpaged = [
            listing.row_id(track)
            for track in self._read(
                f"read the playlist {playlist_id}",
                lambda: listing.playlist_tracks_unpaged(playlist),
            )
        ]
        paged = [listing.row_id(track) for track in self._listed(playlist_id, playlist)]
```

### `u226.M9_positions_no_lag_refusal`

_positions: a lagging window is not refused, its positions taken

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M9_positions_no_lag_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_never_catches_up_refuses_with_nothing_moved`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_later_pages_lag_too_is_held_with_nothing_taken_off`
  - `tests/test_outbound_window_lag.py::test_an_order_whose_later_pages_lag_too_is_held_with_nothing_moved`

Old text:

```
        if window == listing.WINDOW_LAGS:
            raise _window_lags(str(playlist_id), "nothing was sent on that reading")
```

New text:

```
        if False:
            raise _window_lags(str(playlist_id), "nothing was sent on that reading")
```

### `u231.M4_resend_with_the_stale_tag`

adapter order: a 412's move is sent again without opening the playlist for its current tag

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M4_resend_with_the_stale_tag`
- Moved: the reopen after a 412 is still in order_tracks in tidal_account.py, but the retry loop now breaks on success instead of ending each 412 with continue, so the anchor is the pause line and the reopen; same reopen removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 6 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading`
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`
  - `tests/test_outbound_window_lag.py::test_the_pause_after_a_412_is_counted_in_the_moves_record`

Old text:

```
                    self._paused(note, _pause(stale))
                    playlist = self._playlist(identifier)

```

New text:

```
                    self._paused(note, _pause(stale))

```

### `u231.M5_positions_not_advanced`

adapter order: each move's position is read off the reading as it was, not with the moves before it applied

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M5_positions_not_advanced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 38 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading`
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_move_that_lands_anywhere_else_is_not_read_back_and_the_settle_reading_shows_it`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_holding_what_the_adds_left_in_another_order_is_not_stale`
  - `tests/test_outbound_order.py::test_a_reading_that_agrees_with_the_expected_one_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_expected_one_is_read_again`
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before0-order0]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before1-order1]`
  - ... and 23 more, see the JSON sidecar

Old text:

```
            now = _fronted(now, one)
            note["moved"] += 1
```

New text:

```
            note["moved"] += 1
```

### `u231.M6_settle_lag_taken`

adapter settle: a reading whose window lags is answered as the order

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M6_settle_lag_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_settle_reading_waits_then_reads_once_and_names_a_lag`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`

Old text:

```
        if window == listing.WINDOW_LAGS:
            note["window_lagged"] += 1
            note["outcome"] = "lags"
            return None
```

New text:

```
        if False:
            return None
```

### `u255.C4_held_before_read_and_playlist_keeps_the_hold`

M4 with _playlist's drop removed too: a failed tracks read leaves the opened object held, and the next membership read reuses nothing that drops it, drive H of round one

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `C4_held_before_read_and_playlist_keeps_the_hold`
- Moved: the span from _playlist's dropped hold to _membership's open is shorter now, with _listed moved out from between them and the _held docstring cut down; the same two edits are made, the drop in _playlist removed and the hold taken before the tracks read
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_open_that_fails_is_refused_on_its_own_retry_before_any_add_is_sent`
  - `tests/test_outbound_add_requests.py::test_another_write_through_the_adapter_drops_the_hold`

Old text:

```
        self._opened.pop(playlist_id, None)
        doing = f"open the playlist {playlist_id}"
        found = self._call(doing, lambda: self._session.playlist(playlist_id))
        if found is _ABSENT or found is None:
            raise account.provider_failure(
                LookupError(f"the provider has no playlist {playlist_id!r}"), doing
            )
        return found

    def _held(self, playlist_id: str) -> Any:
        """The playlist's held object, opened through :meth:`_playlist` only if none is held.

        ONE OPEN FOR A RUN OF ADDS (U255): an open is two GETs and the client's
        add reads the playlist again after its POST, so opening per add cost
        four requests a track. THE TAG AND THE POSITION COME FROM ONE ANSWER:
        the client's add sends the object's tag and puts the track at its
        length, both set by one read, which is why :meth:`_membership` reads the
        tracks through a copy and holds nothing until that read succeeds. A
        stale held tag is refused 412 with nothing changed (Sitting 62), and
        :meth:`add_to_playlist` then opens afresh.
        """
        held = self._opened.get(playlist_id)
        if held is None:
... truncated ...
```

New text:

```
        doing = f"open the playlist {playlist_id}"
        found = self._call(doing, lambda: self._session.playlist(playlist_id))
        if found is _ABSENT or found is None:
            raise account.provider_failure(
                LookupError(f"the provider has no playlist {playlist_id!r}"), doing
            )
        return found

    def _held(self, playlist_id: str) -> Any:
        """The playlist's held object, opened through :meth:`_playlist` only if none is held.

        ONE OPEN FOR A RUN OF ADDS (U255): an open is two GETs and the client's
        add reads the playlist again after its POST, so opening per add cost
        four requests a track. THE TAG AND THE POSITION COME FROM ONE ANSWER:
        the client's add sends the object's tag and puts the track at its
        length, both set by one read, which is why :meth:`_membership` reads the
        tracks through a copy and holds nothing until that read succeeds. A
        stale held tag is refused 412 with nothing changed (Sitting 62), and
        :meth:`add_to_playlist` then opens afresh.
        """
        held = self._opened.get(playlist_id)
        if held is None:
            held = self._playlist(playlist_
... truncated ...
```

### `u255.C8_no_open_before_and_retry_opens_raw`

M8 with the attempt's open made raw through the session: the first open then rides inside the add's attempts with no retry or refusal of its own

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `C8_no_open_before_and_retry_opens_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_an_open_that_fails_is_refused_on_its_own_retry_before_any_add_is_sent`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`

Old text:

```
        self._held(playlist_id)
        doing = f"add the track {identifier} to the playlist {playlist_id}"

        def attempt() -> Any:
            playlist = self._opened.get(playlist_id)
            if playlist is None:
                playlist = self._held(playlist_id)
            try:
```

New text:

```
        doing = f"add the track {identifier} to the playlist {playlist_id}"

        def attempt() -> Any:
            playlist = self._opened.get(playlist_id)
            if playlist is None:
                playlist = self._session.playlist(playlist_id)
            try:
```

### `u255.M10_failed_attempt_keeps_the_hold`

add_to_playlist attempt: keep the held object after a failed add, so the retry resends the refused tag

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M10_failed_attempt_keeps_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_refused_add_drops_the_hold_so_the_next_track_opens_afresh`
  - `tests/test_outbound_add_requests.py::test_a_track_added_elsewhere_meanwhile_lands_once_and_is_read_back`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`

Old text:

```
            except Exception:
                self._opened.pop(playlist_id, None)
                raise
```

New text:

```
            except Exception:
                raise
```

### `u255.M11_retry_opens_raw`

add_to_playlist attempt: the retry opens through the session with no retry of its own and no hold, round one's finding three

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M11_retry_opens_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`

Old text:

```
                playlist = self._held(playlist_id)
            try:
```

New text:

```
                playlist = self._session.playlist(playlist_id)
            try:
```

### `u255.M12_add_never_retried`

add_to_playlist: no retry at all, so a 412 on a stale held tag fails the item

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M12_add_never_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_playlist_read_one_write_behind_writes_nothing`
  - `tests/test_outbound_add_requests.py::test_a_track_added_elsewhere_meanwhile_lands_once_and_is_read_back`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_twice_fails_the_item_with_nothing_more_sent[412]`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_twice_fails_the_item_with_nothing_more_sent[503]`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`

Old text:

```
        added = self._call(doing, attempt)
```

New text:

```
        added = self._call(doing, attempt, retries=0)
```

### `u255.M13_add_retried_twice`

add_to_playlist: two retries, more than the policy allows a write

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M13_add_retried_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_playlist_read_one_write_behind_writes_nothing`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_twice_fails_the_item_with_nothing_more_sent[412]`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_twice_fails_the_item_with_nothing_more_sent[503]`

Old text:

```
        added = self._call(doing, attempt)
```

New text:

```
        added = self._call(doing, attempt, retries=2)
```

### `u255.M1_playlist_keeps_the_hold`

_playlist: drop nothing, so a member that opens and writes through its own object leaves the held one stale

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M1_playlist_keeps_the_hold`
- Moved: the hold dropped first is still in tidal_account._playlist, now followed by a doing string the open shares instead of the open call itself; same drop removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_open_that_fails_is_refused_on_its_own_retry_before_any_add_is_sent`
  - `tests/test_outbound_add_requests.py::test_another_write_through_the_adapter_drops_the_hold`

Old text:

```
        self._opened.pop(playlist_id, None)
        doing = f"open the playlist {playlist_id}"

```

New text:

```
        doing = f"open the playlist {playlist_id}"

```

### `u255.M2_membership_reads_the_held_object`

_membership: read the tracks through the opened object itself, so the client's tracks read overwrites its tag and leaves its length, round one's BLOCKING

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M2_membership_reads_the_held_object`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_playlist_read_one_write_behind_writes_nothing`
  - `tests/test_outbound_add_requests.py::test_a_tracks_read_one_write_behind_never_reaches_the_add`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`

Old text:

```
            tracks = self._listed(playlist_id, copy.copy(opened))
```

New text:

```
            tracks = self._listed(playlist_id, opened)
```

### `u255.M3_membership_holds_nothing`

_membership: never hold the opened object, so the first add opens again, K + 4 GETs

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M3_membership_holds_nothing`
- Moved: tidal_account._membership now lists its identifiers on one line through _identifier, so the line before the hold differs; same hold of the opened object removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 6 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_held_playlist_never_outlives_its_adapter`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[100]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[10]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[1]`
  - `tests/test_outbound_add_requests.py::test_two_playlists_added_to_in_turn_each_keep_their_own_held_object`

Old text:

```
            self._opened[playlist_id] = opened

```

New text:

```
(empty)
```

### `u255.M5_membership_reuses_the_hold`

_membership: read through a held object when one is held, so the read back of an answer without the track reads a held object, not a fresh open

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M5_membership_reuses_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_found_gone_forgets_the_membership_it_was_remembered_with`

Old text:

```
            opened = self._playlist(playlist_id)

```

New text:

```
            opened = self._opened.get(playlist_id) or self._playlist(playlist_id)

```

### `u255.M6_held_never_stores`

_held: open without holding, so the retry's fresh object is not kept and the next add opens again

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M6_held_never_stores`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_refused_add_drops_the_hold_so_the_next_track_opens_afresh`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_another_write_through_the_adapter_drops_the_hold`

Old text:

```
            self._opened[playlist_id] = held

```

New text:

```
(empty)
```

### `u255.M7_held_always_opens`

_held: ignore what is held and open every time

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M7_held_always_opens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 9 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_held_playlist_never_outlives_its_adapter`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[100]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[10]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[1]`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`
  - `tests/test_outbound_add_requests.py::test_two_playlists_added_to_in_turn_each_keep_their_own_held_object`

Old text:

```
        held = self._opened.get(playlist_id)

```

New text:

```
        held = None

```

### `u255.M9_every_attempt_opens`

add_to_playlist attempt: open afresh for every add, today's four requests a track

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M9_every_attempt_opens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 11 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_held_playlist_never_outlives_its_adapter`
  - `tests/test_outbound_add_requests.py::test_a_refused_add_drops_the_hold_so_the_next_track_opens_afresh`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_another_write_through_the_adapter_drops_the_hold`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[100]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[10]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[1]`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`
  - `tests/test_outbound_add_requests.py::test_two_playlists_added_to_in_turn_each_keep_their_own_held_object`

Old text:

```
            playlist = self._opened.get(playlist_id)
            if playlist is None:
                playlist = self._held(playlist_id)
```

New text:

```
            playlist = self._playlist(playlist_id)
            if playlist is None:
                playlist = self._held(playlist_id)
```

### `u255.S1_member_already_on`

add_to_playlist: send the add for a track the membership already holds, an existing guard

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `S1_member_already_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_track_already_on_the_playlist_makes_no_request_at_all`
  - `tests/test_outbound_tidal_account.py::test_a_member_already_on_the_playlist_makes_no_write`

Old text:

```
        if identifier in members:
            return
        self._held
```

New text:

```
        if False:
            return
        self._held
```

### `u255.S2_read_back_trusts_the_cache`

add_to_playlist: an answer without the track is checked against the cached membership, not read back, an existing guard

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `S2_read_back_trusts_the_cache`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_track_added_elsewhere_meanwhile_lands_once_and_is_read_back`
  - `tests/test_outbound_add_requests.py::test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses`
  - `tests/test_outbound_tidal_account.py::test_an_empty_answer_for_a_track_the_playlist_now_holds_is_not_a_failure`

Old text:

```
            del self._members[playlist_id]
            if identifier not in self._membership(playlist_id):
```

New text:

```
            if identifier not in self._membership(playlist_id):
```

### `u255.S3_answer_absent_passes`

add_to_playlist: a playlist gone mid add is not refused, an existing guard

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `S3_answer_absent_passes`
- Moved: the same guard in add_to_playlist; its provider failure is now built by the shared _gone helper, also used by add_tracks, so the anchor takes the call line before it to stay unique and the condition is reverted the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_add_to_a_playlist_deleted_mid_run_is_the_items_cause`

Old text:

```
        added = self._call(doing, attempt)
        if added is _ABSENT:
            raise _gone(playlist_id, doing)
```

New text:

```
        added = self._call(doing, attempt)
        if False:
            raise _gone(playlist_id, doing)
```

### `u255.S4_added_not_remembered`

add_to_playlist: a landed add is not appended to the membership, an existing guard

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `S4_added_not_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[100]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[10]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[1]`
  - `tests/test_outbound_tidal_account.py::test_a_member_already_on_the_playlist_makes_no_write`

Old text:

```
            return
        members.append(identifier)

```

New text:

```
            return

```

### `u261.O2_account_drops_the_app`

open_account: build the account without the held app client, so its ISRC lookups go to the account

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u261.json`, row `O2_account_drops_the_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`
- Collected: 209 against a baseline of 209
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`
  - `tests/test_provider_session_hold.py::test_the_app_client_is_held_with_the_session_and_asks_one_token`

Old text:

```
    return TidalAccount(held.client, cfg=cfg, catalogue=held.app)
```

New text:

```
    return TidalAccount(held.client, cfg=cfg, catalogue=None)
```

### `u270.A1_failed_attempt_reopens`

add_tracks: keep the object after a failed attempt, so the retry sends its stale tag and is refused 412 (round one's finding)

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u270.json`, row `A1_failed_attempt_reopens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`
- Collected: 159 against a baseline of 159
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_is_retried_on_a_fresh_open_and_recorded`
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_through_the_driver_finishes_the_job`

Old text:

```
                except Exception:
                    opened[0] = None
                    raise

            for start in range(0, len(lacking), ADD_CHUNK):
```

New text:

```
                except Exception:
                    raise

            for start in range(0, len(lacking), ADD_CHUNK):
```

### `u309-z.U10_delete_never_retried`

A playlist's delete is retried on a transient failure

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u309-z.json`, row `U10_delete_never_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_organize_root.py`, `tests/test_prune.py`, `tests/test_label_heard.py`, `tests/test_organize.py`
- Collected: 429 against a baseline of 429
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_delete_meeting_a_transient_failure_is_sent_once`

Old text:

```
        if self._call(doing, send, retries=0) is False:
```

New text:

```
        if self._call(doing, send) is False:
```

### `u309-z.U7_created_needs_identifier`

A playlist or folder the provider created with no identifier is taken as created

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u309-z.json`, row `U7_created_needs_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_organize_root.py`, `tests/test_prune.py`, `tests/test_label_heard.py`, `tests/test_organize.py`
- Collected: 429 against a baseline of 429
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_or_folder_created_with_no_identifier_is_not_taken_as_created[create_folder]`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_or_folder_created_with_no_identifier_is_not_taken_as_created[create_playlist]`

Old text:

```
    identifier = _identifier(created) if created is not _ABSENT else ""
    if not identifier:
```

New text:

```
    identifier = _identifier(created) if created is not _ABSENT else ""
    if False:
```

### `u309-z.U8_served_forgets_membership`

A playlist the provider no longer serves keeps its remembered membership

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u309-z.json`, row `U8_served_forgets_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_organize_root.py`, `tests/test_prune.py`, `tests/test_label_heard.py`, `tests/test_organize.py`
- Collected: 429 against a baseline of 429
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_found_gone_forgets_the_membership_it_was_remembered_with`

Old text:

```
        if found is _ABSENT or found is None:
            self._members.pop(identifier, None)
            return None
```

New text:

```
        if found is _ABSENT or found is None:
            return None
```

### `u309.U11_delete_read_back`

A delete the provider still serves afterwards is reported as a removal

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u309.json`, row `U11_delete_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_organize_root.py`, `tests/test_prune.py`, `tests/test_label_heard.py`, `tests/test_organize.py`
- Collected: 429 against a baseline of 429
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
            raise _refused(
```

New text:

```
        if False:
            raise _refused(
```

### `u309.U9_delete_answered_false`

A delete the provider answered False is read as sent

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u309.json`, row `U9_delete_answered_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_organize_root.py`, `tests/test_prune.py`, `tests/test_label_heard.py`, `tests/test_organize.py`
- Collected: 429 against a baseline of 429
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_delete_the_client_answers_false_is_a_failure`
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_label_heard.py::test_the_adapter_removes_a_vouched_playlist_and_reads_it_back_gone`
  - `tests/test_organize_root.py::test_the_adapter_removes_a_root_playlist_of_its_kind_and_reads_it_back_gone[served0-debris]`
  - `tests/test_organize_root.py::test_the_adapter_removes_a_root_playlist_of_its_kind_and_reads_it_back_gone[served1-empty]`
  - `tests/test_outbound_tidal_account.py::test_a_delete_meeting_a_transient_failure_is_sent_once`

Old text:

```
        if self._call(doing, send, retries=0) is False:
```

New text:

```
        if False:
```

### `r1032.A10_reason_words_reworded`

_among: reword the tie reason away from the constant the mirror reads

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A10_reason_words_reworded`
- Moved: _among moved from tidal_account.py into the Reads mixin in tidal_reads.py, which reads the constant as service.AGREEING_RELEASES, so the same sentence is reworded the same way there
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`, `tests/test_outbound_workers.py`
- Collected: 241 against a baseline of 241
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_tie_beside_a_release_that_cannot_be_read_is_left_out_and_asked_again`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_unreadable_release_beside_the_tie_still_refuses_with_any_agreeing`
  - `tests/test_outbound_tidal_account.py::test_releases_spelled_alike_stay_unmatched_and_the_reason_counts_them`
  - `tests/test_outbound_tidal_account.py::test_without_any_agreeing_the_same_tie_still_refuses_in_the_words_the_mirror_reads`

Old text:

```
            f"{named}{aside}, {len(agreeing)} {service.AGREEING_RELEASES} and the "
```

New text:

```
            f"{named}{aside}, {len(agreeing)} of them match this row's artist, title and version and the "
```

### `r1032.A11_empty_album_narrows`

_on_album: drop the empty tag guard, so a file with no album narrows a tie to the releases the provider left unnamed

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A11_empty_album_narrows`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_never_narrows_to_releases_with_no_album_name`

Old text:

```
        remote for remote in remotes if wanted and match.fold(_album_name(tracks[remote])) == wanted
```

New text:

```
        remote for remote in remotes if match.fold(_album_name(tracks[remote])) == wanted
```

### `r1032.A1_adapter_ignores_any_agreeing`

match_track: drop any_agreeing on its way to _among, so the adapter refuses the tie for the mirror too

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A1_adapter_ignores_any_agreeing`
- Moved: match_track moved from tidal_account.py into the Reads mixin in tidal_reads.py and its _among call is folded shallower; same any_agreeing dropped on its way to _among
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 13 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_release_that_does_not_agree_is_never_the_one_taken`
  - `tests/test_organize_mirror_tie.py::test_a_tie_between_agreeing_releases_is_mirrored_as_one_and_recorded`
  - `tests/test_organize_mirror_tie.py::test_a_tie_remembered_as_a_miss_before_the_tie_was_broken_is_asked_again`
  - `tests/test_organize_mirror_tie.py::test_the_next_refresh_keeps_the_chosen_release_and_asks_the_provider_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_none_of_the_tied_releases_still_takes_one`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_two_of_three_takes_the_lower_of_those_two`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_never_narrows_to_releases_with_no_album_name`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_take_the_lower_hearted_one_never_an_unhearted_one`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`

Old text:

```
                    any_agreeing=any_agreeing,
```

New text:

```
                    any_agreeing=False,
```

### `r1032.A2_tie_always_broken`

_among: break the tie whatever the caller asked, so a heart or a pair takes a release R-572 refuses

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A2_tie_always_broken`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_sync_pair.py`, `tests/test_organize_mirror_tie.py`
- Collected: 317 against a baseline of 317
- Kills: 15 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_neither_release_stays_unmatched_and_says_so`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing`
  - `tests/test_outbound_tidal_account.py::test_a_heart_on_a_release_the_row_does_not_name_decides_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_reason_does_not_outlive_the_match_it_was_about`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_releases_spelled_alike_stay_unmatched_and_the_reason_counts_them`
  - `tests/test_outbound_tidal_account.py::test_the_album_chooses_only_among_releases_that_agree_with_the_row`
  - `tests/test_outbound_tidal_account.py::test_the_album_never_overrides_a_heart_or_breaks_a_tie_between_two`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_spelled_alike_are_still_no_match`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_without_any_agreeing_the_same_tie_still_refuses_in_the_words_the_mirror_reads`

Old text:

```
        if any_agreeing and not unreadable:
```

New text:

```
        if not unreadable:
```

### `r1032.A3_unreadable_tie_broken`

_among: break a tie beside a candidate that could not be read

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A3_unreadable_tie_broken`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_tie_beside_a_release_that_cannot_be_read_is_left_out_and_asked_again`
  - `tests/test_outbound_tidal_account.py::test_a_refused_tie_is_never_said_to_be_broken`
  - `tests/test_outbound_tidal_account.py::test_an_unreadable_release_beside_the_tie_still_refuses_with_any_agreeing`

Old text:

```
        if any_agreeing and not unreadable:
```

New text:

```
        if any_agreeing:
```

### `r1032.A6_first_listed_not_lowest`

_lowest: take the first the provider lists, so the choice moves with the listing order

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A6_first_listed_not_lowest`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 7 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_release_that_does_not_agree_is_never_the_one_taken`
  - `tests/test_organize_mirror_tie.py::test_a_tie_between_agreeing_releases_is_mirrored_as_one_and_recorded`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_two_of_three_takes_the_lower_of_those_two`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`

Old text:

```
    return min(remotes, key=lambda remote: (len(remote), remote))
```

New text:

```
    return remotes[0]
```

### `r1032.A7_lowest_by_characters`

_lowest: order the identifiers as text, so 100 sorts before 99

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A7_lowest_by_characters`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`

Old text:

```
    return min(remotes, key=lambda remote: (len(remote), remote))
```

New text:

```
    return min(remotes)
```

### `r1032.A8_album_narrow_drops_all`

_on_album: when the album names none, answer the named list alone, empty

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A8_album_narrow_drops_all`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 11 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_release_that_does_not_agree_is_never_the_one_taken`
  - `tests/test_organize_mirror_tie.py::test_a_tie_between_agreeing_releases_is_mirrored_as_one_and_recorded`
  - `tests/test_organize_mirror_tie.py::test_a_tie_remembered_as_a_miss_before_the_tie_was_broken_is_asked_again`
  - `tests/test_organize_mirror_tie.py::test_the_next_refresh_keeps_the_chosen_release_and_asks_the_provider_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_none_of_the_tied_releases_still_takes_one`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_never_narrows_to_releases_with_no_album_name`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_take_the_lower_hearted_one_never_an_unhearted_one`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`

Old text:

```
    return named or remotes
```

New text:

```
    return named
```

### `r1032.A9_album_narrow_unfolded`

_on_album: compare the album unfolded, so case and spacing defeat the narrowing

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A9_album_narrow_unfolded`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_the_files_album_narrows_a_tie_under_the_products_own_fold`

Old text:

```
        remote for remote in remotes if wanted and match.fold(_album_name(tracks[remote])) == wanted
```

New text:

```
        remote for remote in remotes if wanted and _album_name(tracks[remote]) == album
```

### `r1032.S1_protocol_default_on`

TidalAccount.match_track: default any_agreeing on, so the hearts, the pairs and the exports, which never pass it, break the tie R-572 refuses

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `S1_protocol_default_on`
- Moved: match_track moved from TidalAccount in tidal_account.py to the Reads base class in tidal_reads.py, which TidalAccount inherits, with its keyword parameters packed onto two lines; the same any_agreeing default is turned on
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 15 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_neither_release_stays_unmatched_and_says_so`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing`
  - `tests/test_outbound_tidal_account.py::test_a_heart_on_a_release_the_row_does_not_name_decides_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_reason_does_not_outlive_the_match_it_was_about`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_releases_spelled_alike_stay_unmatched_and_the_reason_counts_them`
  - `tests/test_outbound_tidal_account.py::test_the_album_chooses_only_among_releases_that_agree_with_the_row`
  - `tests/test_outbound_tidal_account.py::test_the_album_never_overrides_a_heart_or_breaks_a_tie_between_two`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_spelled_alike_are_still_no_match`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_without_any_agreeing_the_same_tie_still_refuses_in_the_words_the_mirror_reads`

Old text:

```
        agree: bool = False, album: str = "", any_agreeing: bool = False,
    ) -> str | None:

```

New text:

```
        agree: bool = False, album: str = "", any_agreeing: bool = True,
    ) -> str | None:

```

### `r1313.T1_account_skips_the_classifier`

tidal_account._not_found: read the class names alone and stop asking classify_unavailable, so a 404 the account reads by status is retried

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1313.json`, row `T1_account_skips_the_classifier`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_outbound_tidal_account.py`
- Collected: 229 against a baseline of 229
- Kills: 5 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-account]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[account]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    return classify_unavailable(exc) is TrackOutcome.UNAVAILABLE_PERMANENT

```

New text:

```
    return False

```

### `r356-a.A10_provider_title_read_one_way_only`

Only the first reading of the provider's title is compared, so a version the provider spelled after a dash never agrees

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A10_provider_title_read_one_way_only`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_provider_title_that_reads_two_ways_agrees_under_either_too`

Old text:

```
for one in listed.readings}
```

New text:

```
for one in (listed,)}
```

### `r356-a.A11_row_title_read_one_way_only`

Only the first reading of the row's title is compared

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A11_row_title_read_one_way_only`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`

Old text:

```
for one in row.readings}
```

New text:

```
for one in (row,)}
```

### `r356-a.A12_reason_outlives_its_match`

A reason is not cleared when the row is matched again, so a row that resolved still says it could not be

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A12_reason_outlives_its_match`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_reason_does_not_outlive_the_match_it_was_about`

Old text:

```
        self._reasons.pop(key, None)

```

New text:

```
(empty)
```

### `r356-a.A14_no_joiner_words`

A row spelling two artists with feat no longer agrees with the track billing both

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A14_no_joiner_words`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two`

Old text:

```
_JOINERS = frozenset({"feat", "ft", "featuring", "with", "and", "vs", "x"})
```

New text:

```
_JOINERS = frozenset()
```

### `r356-a.A1_first_agreeing_rather_than_the_only_one`

Rule one takes the first agreeing track instead of requiring exactly one, which is the first result the unit's brief forbids

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A1_first_agreeing_rather_than_the_only_one`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 27 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_neither_release_stays_unmatched_and_says_so`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_two_of_three_takes_the_lower_of_those_two`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing`
  - `tests/test_outbound_tidal_account.py::test_a_heart_on_a_release_the_row_does_not_name_decides_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_lone_heart_and_a_lone_album_choose_as_they_always_did`
  - `tests/test_outbound_tidal_account.py::test_a_lone_release_a_lone_heart_or_a_lone_album_is_never_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_a_reason_does_not_outlive_the_match_it_was_about`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_release_the_account_already_hearts_is_the_one_an_export_adds`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - ... and 12 more, see the JSON sidecar

Old text:

```
        if len(agreeing) == 1 and not unreadable:
```

New text:

```
        if agreeing and not unreadable:
```

### `r356-a.A2_unreadable_track_no_longer_stops_rule_one`

A lone agreeing track is chosen beside one nobody could read

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A2_unreadable_track_no_longer_stops_rule_one`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_release_that_cannot_be_read_stops_a_lone_agreeing_one_from_being_chosen`
  - `tests/test_outbound_tidal_account.py::test_an_unreadable_track_stops_the_album_from_choosing_the_lone_agreeing_one`

Old text:

```
        if len(agreeing) == 1 and not unreadable:
```

New text:

```
        if len(agreeing) == 1:
```

### `r356-a.A3_any_hearted_rather_than_the_only_hearted`

Rule two takes the first hearted release when the account hearts two

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A3_any_hearted_rather_than_the_only_hearted`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_the_album_never_overrides_a_heart_or_breaks_a_tie_between_two`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_spelled_alike_are_still_no_match`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`

Old text:

```
        if len(hearted) == 1:
```

New text:

```
        if hearted:
```

### `r356-a.A4_hearts_asked_of_every_track`

Rule two reads the hearts of every track the ISRC named instead of the agreeing ones, so a heart on the radio edit chooses for the plain record

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A4_hearts_asked_of_every_track`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_heart_on_a_release_the_row_does_not_name_decides_nothing`

Old text:

```
        hearted = [remote for remote in agreeing if remote in hearts]
```

New text:

```
        hearted = [remote for remote in verdicts if remote in hearts]
```

### `r356-a.A5_withdrawn_track_is_a_candidate`

A track the provider will not play is compared like any other, with the version the client never read

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A5_withdrawn_track_is_a_candidate`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_track_the_provider_will_not_play_is_never_the_choice`
  - `tests/test_outbound_tidal_account.py::test_a_withdrawn_release_does_not_stop_the_one_that_plays_from_being_chosen`

Old text:

```
    return getattr(track, "available", True) is not False
```

New text:

```
    return True
```

### `r356-a.A7_artist_not_compared`

Agreement ignores the artist, so another act's record under the same title agrees

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A7_artist_not_compared`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two`
  - `tests/test_outbound_tidal_account.py::test_another_artist_under_the_same_title_does_not_agree`

Old text:

```
    if not _artist_agrees(row.artist, listed.artist, track):
        return False

```

New text:

```
(empty)
```

### `r356-a.A8_first_billed_artist_not_required`

A row naming only the guest agrees

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A8_first_billed_artist_not_required`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two`

Old text:

```
    return bool(first) and first <= ours and ours - billed <= _JOINERS
```

New text:

```
    return bool(first) and ours - billed <= _JOINERS
```

### `r356-a.A9_row_may_name_an_artist_nobody_bills`

A row billing a third act the track does not agrees

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A9_row_may_name_an_artist_nobody_bills`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two`

Old text:

```
    return bool(first) and first <= ours and ours - billed <= _JOINERS
```

New text:

```
    return bool(first) and first <= ours
```

### `r572.A2_first_named`

Take the first release the album names even when several do

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r572.json`, row `A2_first_named`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`

Old text:

```
        if len(named_album) == 1:
```

New text:

```
        if len(named_album) >= 1:
```

### `r572.A4_no_fold`

Compare the album raw rather than folded

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r572.json`, row `A4_no_fold`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_releases_spelled_alike_resolve_to_the_one_the_files_album_names`

Old text:

```
        wanted = match.fold(album)
```

New text:

```
        wanted = album
```

### `r572.A5_album_among_all`

Choose by album among every candidate, not only the agreeing ones

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r572.json`, row `A5_album_among_all`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_the_album_chooses_only_among_releases_that_agree_with_the_row`

Old text:

```
            remote for remote in agreeing if match.fold(_album_name(tracks[remote])) == wanted
```

New text:

```
            remote for remote in tracks if match.fold(_album_name(tracks[remote])) == wanted
```

### `r879-b.T1_one_track_never_asked_to_agree`

TidalAccount.match_track: return one track under a code whether or not agree is asked

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r879-b.json`, row `T1_one_track_never_asked_to_agree`
- Moved: the one track shortcut moved with match_track from TidalAccount in tidal_account.py to Reads in tidal_reads.py, one level shallower; the same not agree condition is dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_code_asked_to_agree_lists_its_one_track_only_when_it_is_the_row`

Old text:

```
            if len(tracks) == 1 and not agree:

```

New text:

```
            if len(tracks) == 1:

```

### `u208.M19_adapter_never_records_tie`

match_track: never record a broken tie

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u208.json`, row `M19_adapter_never_records_tie`
- Moved: Anchored where u309-replay-after-c.json replayed it: match_track moved from tidal_account.py into the Reads mixin in tidal_reads.py and its ISRC lookup lost a level of nesting; same branch reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 134 against a baseline of 134
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - `tests/test_sync_pair_tie.py::test_two_hearted_releases_take_the_lower_hearted_one`

Old text:

```
                elif tied:
                    self._ties.add(key)
```

New text:

```
                elif False:
                    self._ties.add(key)
```

### `u208.M20_adapter_stale_tie`

match_track: keep the last match's tie flag across a later match of the same row

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u208.json`, row `M20_adapter_stale_tie`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`

Old text:

```
        self._ties.discard(key)
```

New text:

```
        pass
```

### `u208.M21_adapter_every_choice_a_tie`

_among: call every any_agreeing choice a broken tie, an album naming one included

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u208.json`, row `M21_adapter_every_choice_a_tie`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_lone_release_a_lone_heart_or_a_lone_album_is_never_a_broken_tie`

Old text:

```
            return _lowest(narrowed), "", bool(hearted) or len(narrowed) > 1
```

New text:

```
            return _lowest(narrowed), "", True
```

### `u208.M22_adapter_hearts_half`

_among: drop the hearts half of the tie flag, so two hearts the album narrows to one are not a tie

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u208.json`, row `M22_adapter_hearts_half`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`

Old text:

```
            return _lowest(narrowed), "", bool(hearted) or len(narrowed) > 1
```

New text:

```
            return _lowest(narrowed), "", len(narrowed) > 1
```

### `u27-reports-round-2.S5b_engine_default_drift`

Drift the engine's own copy of the handler key away from the registry's

- File: `src/cratekit/modules/reports/duplicates.py`
- Source: `u27-reports-round-2.json`, row `S5b_engine_default_drift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/test_reports_cli.py`
- Collected: 382 against a baseline of 382
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_reports.py::test_every_item_carries_the_handler_key_the_registry_declares`
  - `tests/modules/test_reports.py::test_the_declared_handler_key_is_the_one_the_registry_carries`
  - `tests/test_reports_cli.py::test_the_two_copies_of_the_duplicate_handler_key_cannot_drift`

Old text:

```
HANDLER_KEY = "audit.duplicates"
```

New text:

```
HANDLER_KEY = "duplicates.audit"
```

### `r367.E1_a_failed_transfer_is_unread`

existing guard sample: run_restore returns results without reading return codes

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `E1_a_failed_transfer_is_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
- Kills: 15 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_database_copy_still_refuses_when_the_sidecar_is_absent`
  - `tests/modules/test_tools.py::test_a_rehearsed_restore_does_not_clear_the_live_sidecars`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_removes_stale_sidecars_before_copying`
  - `tests/modules/test_tools.py::test_the_sidecars_are_cleared_before_the_mirror_too`
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled_and_reported`

Old text:

```
        if result.returncode != 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
```

New text:

```
        if result.returncode == 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
```

### `u48-author.P3_two_codes_collapsed_to_one`

One code over both conditions, which is the discriminator this unit split

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P3_two_codes_collapsed_to_one`
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
ARCHIVE_PURGE_FAILED = "archive-purge-failed"
```

New text:

```
ARCHIVE_PURGE_FAILED = "archive-listing-failed"
```

### `r154-a.A3_named_shape_check`

Never refuse a named snapshot on shape, which is the finding itself: the traversal value reaches the remote path again

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-a.json`, row `A3_named_shape_check`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
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

### `r154-b.B1_named_mismatch`

Accept a named snapshot carrying ANY marker, which is the finding's real half: a well formed stamp from another library is pulled

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B1_named_mismatch`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
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

### `r154-b.B7_walk_order`

Walk oldest first, so the default pulls the OLDEST snapshot that is this library's

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B7_walk_order`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
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

### `r338-a.B8_contained_share_copied_twice`

_outside_share: read every layout as the outside one, so a share the mirror already carries is synced a second time

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B8_contained_share_copied_twice`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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

### `r338-b.R4_empty_listing_read_as_held`

share_is_held: read a listing that names nothing as a mirror, so a copy from an empty folder is planned and reported as pulled

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R4_empty_listing_read_as_held`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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
- Collected: 723 against a baseline of 723
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
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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

### `r338-b.R9_contained_restore_asks_about_a_share`

_plan_restore_inside_the_gates: treat every layout as the outside one on restore, so a contained library lists and pulls a share mirror it never wrote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R9_contained_restore_asks_about_a_share`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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

### `r367.G12_listing_results_are_discarded`

the listing runs and its names are thrown away, so every sidecar is treated as absent

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G12_listing_results_are_discarded`
- Moved: Anchored where u311-replay-after-a.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
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
- Collected: 283 against a baseline of 283
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
- Moved: Anchored where u311-replay-after-a.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
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
- Collected: 283 against a baseline of 283
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
- Collected: 283 against a baseline of 283
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

### `r592-b.B6_restore_mirror_carries_the_database`

_plan_restore_inside_the_gates: exclude volume clutter only from the restore mirror, so a mirror still holding the database lands it where the database half writes

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r592-b.json`, row `B6_restore_mirror_carries_the_database`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_backup_cli.py`, `tests/test_restore.py`
- Collected: 23216 against a baseline of 23216
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

### `u105-a.E10_parts_archived`

Stop archiving the parts, reporting each part as its own archive

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E10_parts_archived`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`

Old text:

```
    archives = tuple(archive_source(p, p.parent / ARCHIVE_DIRNAME) for p in paths)
```

New text:

```
    archives = tuple(paths)
```

### `u105-a.E11_join_dir_removed`

Leave the private join directory, and the joined set inside it, behind

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E11_join_dir_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_two_parts_produce_one_master_whose_duration_is_their_sum`

Old text:

```
        shutil.rmtree(join_dir, ignore_errors=True)
```

New text:

```
        pass
```

### `u105-a.E12_join_rf64`

Write a joined WAV without -rf64 auto

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E12_join_rf64`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_joined_wav_is_written_as_rf64_when_it_needs_to_be`

Old text:

```
    container = ("-rf64", "auto") if destination.suffix.lower() == ".wav" else ()
```

New text:

```
    container = ()
```

### `u105-a.E13_joined_suffix`

Name the joined set after the first part alone, colliding with part one's own master

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E13_joined_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 5 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_the_engine_refuses_an_existing_joined_master_before_archiving`
  - `tests/test_master_cli.py::test_the_parts_are_joined_in_the_order_given_and_never_sorted`
  - `tests/test_master_cli.py::test_two_parts_produce_one_master_whose_duration_is_their_sum`

Old text:

```
JOINED_SUFFIX = "_set"
```

New text:

```
JOINED_SUFFIX = ""
```

### `u105-a.E14_single_part_name`

Name a single recording's master as if it were joined

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E14_single_part_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 4 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`

Old text:

```
    paths = [Path(p) for p in parts]
    if len(paths) == 1:
        return output_path(paths[0], output_dir=output_dir)
```

New text:

```
    paths = [Path(p) for p in parts]
```

### `u105-a.E15_payload_parts_conditional`

Emit parts and archives in every report payload, single recordings included

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E15_payload_parts_conditional`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_one_input_masters_through_the_unchanged_engine_path`

Old text:

```
    if report.parts:
```

New text:

```
    if True:
```

### `u105-a.E1_lufs_range_removed`

Delete the target_lufs range check in Settings.__post_init__

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E1_lufs_range_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 4 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-4]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-71]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[nan]`
  - `tests/test_master_cli.py::test_the_engine_refuses_an_out_of_range_target_and_takes_the_bounds_inclusively`

Old text:

```
        if not low_lufs <= self.target_lufs <= high_lufs:
```

New text:

```
        if False:
```

### `u105-a.E2_lufs_high_bound`

Move the loud bound one LU louder, -5 to -4, a realistic nearby value

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E2_lufs_high_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-4]`
  - `tests/test_master_cli.py::test_the_engine_refuses_an_out_of_range_target_and_takes_the_bounds_inclusively`

Old text:

```
LUFS_RANGE = (-70.0, -5.0)
```

New text:

```
LUFS_RANGE = (-70.0, -4.0)
```

### `u105-a.E3_lufs_nan`

Rewrite the range check as two positive comparisons, which admit NaN

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E3_lufs_nan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[nan]`
  - `tests/test_master_cli.py::test_the_engine_refuses_an_out_of_range_target_and_takes_the_bounds_inclusively`

Old text:

```
        if not low_lufs <= self.target_lufs <= high_lufs:
```

New text:

```
        if self.target_lufs < low_lufs or self.target_lufs > high_lufs:
```

### `u105-a.E4_duplicate_part`

Delete the part-named-twice refusal in master_parts

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E4_duplicate_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_part_named_twice_or_in_another_container_refuses_before_any_command[twice]`

Old text:

```
        if key in seen:
```

New text:

```
        if False:
```

### `u105-a.E5_mixed_containers`

Delete the mixed-container refusal in master_parts

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E5_mixed_containers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_part_named_twice_or_in_another_container_refuses_before_any_command[containers]`

Old text:

```
    if len(containers) > 1:
```

New text:

```
    if False:
```

### `u105-a.E6_joined_output_exists`

Delete master_parts' own output-exists check, leaving master's later one

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E6_joined_output_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_the_engine_refuses_an_existing_joined_master_before_archiving`

Old text:

```
    target = planned_output(paths, output_dir=output_dir)
    if target.exists() and not overwrite:
```

New text:

```
    target = planned_output(paths, output_dir=output_dir)
    if False:
```

### `u105-a.E7_layout_rate`

Drop sample rate from the layout the parts must share, the brief's named hazard

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E7_layout_rate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_parts_at_different_sample_rates_refuse_before_anything_is_written`

Old text:

```
    shapes = {(p.sample_rate, p.sample_fmt, p.channels, p.codec) for p in probes}
```

New text:

```
    shapes = {(p.sample_fmt, p.channels, p.codec) for p in probes}
```

### `u105-a.E8_layout_channels`

Drop channel count from the layout the parts must share

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E8_layout_channels`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_parts_differing_in_any_copied_field_refuse[mono-beside-stereo]`

Old text:

```
    shapes = {(p.sample_rate, p.sample_fmt, p.channels, p.codec) for p in probes}
```

New text:

```
    shapes = {(p.sample_rate, p.sample_fmt, p.codec) for p in probes}
```

### `u105-a.E9_layout_codec`

Drop codec from the layout the parts must share

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u105-a.json`, row `E9_layout_codec`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone`

Old text:

```
    shapes = {(p.sample_rate, p.sample_fmt, p.channels, p.codec) for p in probes}
```

New text:

```
    shapes = {(p.sample_rate, p.sample_fmt, p.channels) for p in probes}
```

### `u311.C5_binaries_out_of_order`

The shared binary lookup answers its names in reverse, swapping ffmpeg and ffprobe

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u311.json`, row `C5_binaries_out_of_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 30 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_mastering_leaves_no_intermediate_behind`
  - `tests/modules/test_tools.py::test_mastering_leaves_the_source_byte_identical_and_archived`
  - `tests/modules/test_tools.py::test_mastering_reports_before_and_after_loudness`
  - `tests/modules/test_tools.py::test_the_mastering_payload_carries_a_version`
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`
  - `tests/test_master_cli.py::test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone`
  - `tests/test_master_cli.py::test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume`
  - `tests/test_master_cli.py::test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_joined_wav_is_written_as_rf64_when_it_needs_to_be`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - ... and 15 more, see the JSON sidecar

Old text:

```
        return [binaries.resolve(name) for name in names]
```

New text:

```
        return [binaries.resolve(name) for name in reversed(names)]
```

### `u44-author-round-2.A1_archive_verify_dropped`

Drop the post-copy digest verification, so a corrupt archive is reported safe

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author-round-2.json`, row `A1_archive_verify_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 246 against a baseline of 246
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy`

Old text:

```
    shutil.copy2(source, destination)
    if digest(destination) != source_digest:
```

New text:

```
    shutil.copy2(source, destination)
    if False:
```

### `u44-author-round-2.A4_digest_reads_first_chunk_only`

Digest only the first chunk, so two sets differing later in the file hash identically

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author-round-2.json`, row `A4_digest_reads_first_chunk_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 246 against a baseline of 246
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_impostor_matching_the_first_chunk_is_still_a_different_recording`

Old text:

```
        while True:
            block = handle.read(chunk)
            if not block:
                break
            hasher.update(block)
```

New text:

```
        hasher.update(handle.read(chunk))
```

### `u44-author.A2_archive_collision_skips`

Restore the source system's behaviour: an existing archive entry is skipped rather than verified

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author.json`, row `A2_archive_collision_skips`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 246 against a baseline of 246
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_archive_entry_with_the_same_name_and_different_content_refuses`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`
  - `tests/test_master_cli.py::test_an_impostor_matching_the_first_chunk_is_still_a_different_recording`

Old text:

```
    if destination.exists():
        if digest(destination) == source_digest:
            return destination
```

New text:

```
    if destination.exists():
        return destination
```

### `u44-author.B1_output_unread`

Drop the post-encode output check, restoring the success report over a file that is not there

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author.json`, row `B1_output_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 246 against a baseline of 246
- Kills: 3 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`

Old text:

```
    _wrote_or_refuse(target, "normalize-and-encode")
    return Report(
```

New text:

```
    return Report(
```

### `u44-author.B2_output_existence_only`

Check existence but not size, so a zero-byte encode still reports a saving of 1.0

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author.json`, row `B2_output_existence_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 246 against a baseline of 246
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`

Old text:

```
    if not target.exists() or target.stat().st_size == 0:
```

New text:

```
    if not target.exists():
```

### `u112-b.A6_exported_not_product_made`

An exported playlist the ledger records as product made is listed as the author's

- File: `src/cratekit/organize/account.py`
- Source: `u112-b.json`, row `A6_exported_not_product_made`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            | ledger.product_made_among(cfg, (one.playlist_id for one in listed))
```

New text:

```
            | frozenset()
```

### `u112.A2_pending_loses`

A pending intake file ranks below a retired one of the same pass

- File: `src/cratekit/organize/account.py`
- Source: `u112.json`, row `A2_pending_loses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_latest_retired_landing_wins_by_number_and_a_bracket_is_no_pattern`

Old text:

```
        return 1 << 30
```

New text:

```
        return 0
```

### `u112.A3_retired_unnumbered`

Every retired intake file ranks alike, so the first read wins rather than the latest

- File: `src/cratekit/organize/account.py`
- Source: `u112.json`, row `A3_retired_unnumbered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_latest_retired_landing_wins_by_number_and_a_bracket_is_no_pattern`

Old text:

```
    return int(number) if number.isdigit() else 1
```

New text:

```
    return 1
```

### `u112.A4_in_folder_listed`

An account playlist already in the author's own folder is listed as not organized

- File: `src/cratekit/organize/account.py`
- Source: `u112.json`, row `A4_in_folder_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_playlist_of_yours_already_in_a_folder_of_yours_is_not_listed`

Old text:

```
            or one.playlist_id in in_folders

```

New text:

```
(empty)
```

### `u112.A7_no_proof_read`

No intake file is read as a set's proof, so no downloaded set is ever archived

- File: `src/cratekit/organize/account.py`
- Source: `u112.json`, row `A7_no_proof_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 8 (killed)
- Killed:
  - `tests/test_organize.py::test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year`
  - `tests/test_organize.py::test_a_set_proven_by_its_intake_file_never_opens_the_database_for_inspiration`
  - `tests/test_organize.py::test_a_year_record_whose_folder_now_carries_the_sets_name_is_not_the_filings`
  - `tests/test_organize.py::test_aborting_rekordbox_and_applying_the_account_writes_only_the_account`
  - `tests/test_organize.py::test_an_unreadable_label_registry_refuses_the_label_step_alone`
  - `tests/test_organize.py::test_no_downloaded_sets_folder_is_made_once_and_the_year_folder_beside_it`
  - `tests/test_organize.py::test_one_step_of_each_kind_is_planned_in_its_own_area`
  - `tests/test_organize.py::test_one_steps_refusal_leaves_every_other_plan_on_screen`

Old text:

```
        xml = _proof(cfg, name)
```

New text:

```
        xml = None
```

### `u116.M9_yours_lists_moved`

_yours: a playlist the filing step moves is still listed as yours, not moved

- File: `src/cratekit/organize/account.py`
- Source: `u116.json`, row `M9_yours_lists_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_the_full_verb_lists_the_working_custom_and_never_the_root_steps_removals`

Old text:

```
            or one.playlist_id in moving

```

New text:

```
(empty)
```

### `u137-b.A3_marks_gate`

Plan the marks whatever the selection

- File: `src/cratekit/organize/account.py`
- Source: `u137-b.json`, row `A3_marks_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`

Old text:

```
    if area.wants(MARKS):
```

New text:

```
    if True:
```

### `u137.A1_labels_gate`

Plan the label steps whatever the selection

- File: `src/cratekit/organize/account.py`
- Source: `u137.json`, row `A1_labels_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 121 against a baseline of 121
- Kills: 9 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`
  - `tests/test_organize.py::test_only_file_plans_the_filing_alone_and_the_database_is_not_asked`
  - `tests/test_organize.py::test_only_mirror_plans_and_writes_the_mirror_alone_and_a_rerun_plans_nothing`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`

Old text:

```
    if area.wants(LABELS):
```

New text:

```
    if True:
```

### `u137.A2_sets_gate`

Plan the set archives whatever the selection

- File: `src/cratekit/organize/account.py`
- Source: `u137.json`, row `A2_sets_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 121 against a baseline of 121
- Kills: 10 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_an_unread_label_registry_refuses_the_filing_rather_than_plan_it_over_no_label`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`
  - `tests/test_organize.py::test_only_file_plans_the_filing_alone_and_the_database_is_not_asked`
  - `tests/test_organize.py::test_only_mirror_plans_and_writes_the_mirror_alone_and_a_rerun_plans_nothing`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`

Old text:

```
    if area.wants(SETS):
```

New text:

```
    if True:
```

### `u137.A5_filing_for_yours`

Skip the filing plan when yours is selected without file

- File: `src/cratekit/organize/account.py`
- Source: `u137.json`, row `A5_filing_for_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 121 against a baseline of 121
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`

Old text:

```
    if area.wants(FILE) or area.wants(YOURS):
```

New text:

```
    if area.wants(FILE):
```

### `u137.A8_labels_module_off`

Refuse the filing over an unread registry the profile does not use

- File: `src/cratekit/organize/account.py`
- Source: `u137.json`, row `A8_labels_module_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 121 against a baseline of 121
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_registry_the_profile_does_not_use_does_not_refuse_the_filing`

Old text:

```
            unfollowed if LABELS_MODULE in available else None,
```

New text:

```
            unfollowed,
```

### `u142.S13_unread_reads_as_none`

organize set step: read a database that cannot answer as holding no INSPIRATION playlist, so the set waits instead of refusing

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S13_unread_reads_as_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_two_inspiration_folders_refuse_the_unproven_set_alone`

Old text:

```
            try:
                held = inspired.get()
            except CratekitError as exc:
                area.steps.append(refused(key, title, exc.cause))
                continue
```

New text:

```
            try:
                held = inspired.get()
            except CratekitError:
                held = frozenset()
```

### `u142.S14_any_inspiration_proves_every_set`

organize set step: take any INSPIRATION playlist as proof for every set, not one of the set's own name

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S14_any_inspiration_proves_every_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_playlist_of_the_sets_name_outside_inspiration_or_removed_proves_nothing`

Old text:

```
            if held is None or name not in held:
```

New text:

```
            if held is None or not held:
```

### `u142.S15_second_proof_ignored`

organize set step: list a set with an INSPIRATION playlist of its name as waiting, the behaviour before this unit

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S15_second_proof_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`
  - `tests/test_organize.py::test_a_set_archived_by_its_inspiration_proof_stays_archived_once_that_playlist_goes`
  - `tests/test_organize.py::test_a_set_found_prefixed_by_the_migration_is_still_filed_by_the_archive`
  - `tests/test_organize.py::test_a_set_in_its_folder_with_its_built_title_is_taken_and_not_moved`
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`
  - `tests/test_organize.py::test_the_inspiration_proof_is_read_while_rekordbox_runs`

Old text:

```
            if held is None or name not in held:
```

New text:

```
            if True:
```

### `u142.S16_pass_is_not_the_set`

organize set step: record an INSPIRATION proven mark under another pass, so sync unmark with the set's name finds nothing

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S16_pass_is_not_the_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`

Old text:

```
                else set_cli.plan_archive_named(cfg, name, pass_name=name)
```

New text:

```
                else set_cli.plan_archive_named(cfg, name, pass_name="organize")
```

### `u142.S17_proof_not_named`

organize set step: name the set alone as the proof, so the gate does not say an INSPIRATION playlist proved it

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S17_proof_not_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`

Old text:

```
            proof = f"the INSPIRATION playlist {name}"
```

New text:

```
            proof = name
```

### `u142.S18_wait_names_no_folder_always`

_waiting: say no INSPIRATION folder is declared whatever the read answered

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S18_wait_names_no_folder_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize.py::test_a_playlist_of_the_sets_name_outside_inspiration_or_removed_proves_nothing`
  - `tests/test_organize.py::test_a_set_with_no_intake_file_named_for_it_waits_and_is_not_planned`
  - `tests/test_organize.py::test_a_taxonomy_with_no_inspiration_folder_waits_and_says_why`

Old text:

```
        if inspired is not None
        else "no INSPIRATION folder declared in the taxonomy to hold a playlist of its name"
```

New text:

```
        if inspired is None
        else "no INSPIRATION folder declared in the taxonomy to hold a playlist of its name"
```

### `u142.S20_retitled_detail_called_marked`

organize set step: call a set a person retitled in its folder marked

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S20_retitled_detail_called_marked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`

Old text:

```
        elif planned is not None and planned.left == sets.RETITLED:
```

New text:

```
        elif False:
```

### `u142.S23_prefix_only_said_as_a_move`

organize set step: say file it in the folder for a set already there with its built title, a prefix and no move

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S23_prefix_only_said_as_a_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_set_in_its_folder_with_its_built_title_is_taken_and_not_moved`

Old text:

```
        if archived.writes and planned.move:
```

New text:

```
        if archived.writes:
```

### `u143-e.C1_yours_empties`

Account: list an empty root playlist the root step removes as one of the author's

- File: `src/cratekit/organize/account.py`
- Source: `u143-e.json`, row `C1_yours_empties`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 121 against a baseline of 121
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_full_verb_lists_the_working_custom_and_never_the_root_steps_removals`

Old text:

```
        _yours(cfg, area, labels, catalogue_of, remote_of, moving | _empties(filed_of))
```

New text:

```
        _yours(cfg, area, labels, catalogue_of, remote_of, moving)
```

### `r1031.M15_seen_not_seeded`

add_steps: rebuild from the frozen library with no frozen matches, the review's row one

- File: `src/cratekit/organize/account_mirror.py`
- Source: `r1031.json`, row `M15_seen_not_seeded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`, `tests/test_organize.py`
- Collected: 168 against a baseline of 168
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_rematch_on_the_run_that_answers_asks_nothing_and_says_so`
  - `tests/test_organize_mirror_frozen.py::test_the_frozen_matches_answer_a_row_the_ledger_could_not_remember`
  - `tests/test_organize_mirror_frozen.py::test_the_frozen_matches_stand_over_a_link_recorded_between_the_acts`

Old text:

```
        seen=frozen.matches if frozen is not None else None,
```

New text:

```
        seen=None,
```

### `r1031.M16_report_records`

add_steps: record and freeze on a run that does not ask its gate

- File: `src/cratekit/organize/account_mirror.py`
- Source: `r1031.json`, row `M16_report_records`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`, `tests/test_organize.py`
- Collected: 168 against a baseline of 168
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen.py::test_a_report_records_no_link_no_miss_and_freezes_nothing`

Old text:

```
    elif run is not None and run.record:
```

New text:

```
    elif run is not None:
```

### `r1031.M17_apply_records_no_miss`

_apply: record no miss at the apply, so a plan with no run remembers nothing

- File: `src/cratekit/organize/account_mirror.py`
- Source: `r1031.json`, row `M17_apply_records_no_miss`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_coded_rows_miss_is_kept_whatever_its_file_does`
  - `tests/test_organize_mirror_frozen.py::test_a_file_that_gains_a_code_is_asked_again_and_an_unchanged_one_is_not`
  - `tests/test_organize_mirror_frozen.py::test_a_miss_over_a_candidate_that_could_not_be_read_is_never_remembered`
  - `tests/test_organize_mirror_frozen.py::test_a_refresh_asks_only_the_rows_new_since_the_last_and_names_the_rest_remembered`
  - `tests/test_organize_mirror_frozen.py::test_a_row_matched_later_loses_its_miss`

Old text:

```
            ledger.record_mirror_misses(cfg, matcher.missed)
            mirror.apply(cfg, account, planned, done, links=matcher.fresh)
```

New text:

```
            mirror.apply(cfg, account, planned, done, links=matcher.fresh)
```

### `r1031.M18_unrecordable_ledger_refuses_the_plan`

_record: let a ledger that cannot take the links escape the plan instead of saying so

- File: `src/cratekit/organize/account_mirror.py`
- Source: `r1031.json`, row `M18_unrecordable_ledger_refuses_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_ledger_that_cannot_take_the_links_leaves_the_plan_standing_and_says_so`

Old text:

```
    except CratekitError as exc:
        return f"{said}not frozen: what the plan matched could not be recorded ({exc.cause.message})"
```

New text:

```
    except ValueError as exc:
        return f"{said}not frozen: what the plan matched could not be recorded ({exc})"
```

### `r1031.M19_unfreezable_plan_refuses`

_record: let a frozen plan that cannot be written escape the plan instead of saying so

- File: `src/cratekit/organize/account_mirror.py`
- Source: `r1031.json`, row `M19_unfreezable_plan_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_plan_that_cannot_be_frozen_stands_and_the_apply_plans_afresh`

Old text:

```
    except OSError as exc:
        return f"{said}not frozen ({exc}), so the apply plans again"
```

New text:

```
    except ValueError as exc:
        return f"{said}not frozen ({exc}), so the apply plans again"
```

### `r1031.M20_signature_constant`

file_signature: answer one value for every readable file, so a rewritten file looks unchanged

- File: `src/cratekit/organize/account_mirror.py`
- Source: `r1031.json`, row `M20_signature_constant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_the_file_signature_moves_when_the_file_is_rewritten`

Old text:

```
        return f"{held.st_size}:{held.st_mtime_ns}"
```

New text:

```
        return "1:1"
```

### `u147-d.A2_retired_unnamed`

account_mirror.add_steps: a mirrored folder the library no longer holds is not listed

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u147-d.json`, row `A2_retired_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_library.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_folder_the_library_no_longer_holds_is_left_and_named`

Old text:

```
    for name in sorted(set(recorded) - held):
```

New text:

```
    for name in ():
```

### `u147-d.A3_twin_folders_read`

account_mirror.read_library: two rekordbox folders of one name are both mirrored into one

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u147-d.json`, row `A3_twin_folders_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_library.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_library.py::test_two_tree_folders_of_one_name_refuse_that_name_and_read_the_rest`

Old text:

```
        if counted[name] > 1:
```

New text:

```
        if counted[name] > 99:
```

### `u147-d.A5_source_title`

account_mirror.read_library: All Favorites takes the folder's prefix like every other playlist

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u147-d.json`, row `A5_source_title`
- Moved: the favorites folder titler stayed in account_mirror.read_library but sits one level shallower after the function was reshaped, so only its indentation changed; the same source title exemption is dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_library.py`
- Collected: 4 against a baseline of 4
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_library.py::test_every_genre_folder_and_the_favorites_folder_is_read_under_its_account_titles`

Old text:

```
                return shown if shown == source else mirror.title(name, shown)

```

New text:

```
                return mirror.title(name, shown)

```

### `u147-d.A6_file_code_trusted`

account_mirror.identify: a code read off the file does not ask the track to agree

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u147-d.json`, row `A6_file_code_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_library.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_code_read_off_the_file_asks_the_one_track_to_agree_and_a_database_code_does_not`

Old text:

```
            (isrc, album), agree = pair_cli.file_identity(cfg, row.path), True
```

New text:

```
            (isrc, album), agree = pair_cli.file_identity(cfg, row.path), False
```

### `u150.A1_inbox_retires`

account_mirror._inbox: read INBOX as an ordinary folder, so no batch that left it is ever removed

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u150.json`, row `A1_inbox_retires`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_library.py`, `tests/test_organize_mirror.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_the_inbox_folder_reads_each_batch_under_its_account_title_with_its_rows`

Old text:

```
        playlists=tuple(sources),
        retire=True,
```

New text:

```
        playlists=tuple(sources),
        retire=False,
```

### `u150.A2_present_titled`

account_mirror._inbox: hold INBOX's bare names as present instead of their account titles, so every still present title reads as gone

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u150.json`, row `A2_present_titled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_library.py`, `tests/test_organize_mirror.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_the_inbox_folder_reads_each_batch_under_its_account_title_with_its_rows`

Old text:

```
        present=frozenset(mirror.title(name, one) for one in live.present),
```

New text:

```
        present=frozenset(live.present),
```

### `u150.A4_listed_step`

account_mirror.add_steps: show no listed step for an INBOX not mirrored, so the gate is silent about it

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u150.json`, row `A4_listed_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize.py`
- Collected: 163 against a baseline of 163
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_an_inbox_that_cannot_be_read_is_listed_and_nothing_of_it_is_removed`

Old text:

```
    if library.inbox:
        area.steps.append(
```

New text:

```
    if False:
        area.steps.append(
```

### `u150.A5_deletes_named`

account_mirror.add_steps: name no playlist removal on the gate's deletes, so the gate says nothing is removed over one

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u150.json`, row `A5_deletes_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize.py`
- Collected: 163 against a baseline of 163
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_batch_the_rotation_moved_into_old_plans_the_removal_of_its_playlist_and_nothing_else`

Old text:

```
                for name, remote_id in planned.retire
            )
```

New text:

```
                for name, remote_id in ()
            )
```

### `u150.A7_landed_two_tracks`

landed_tracks: keep a row two records name two tracks for, so which track it is decides itself by record order

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u150.json`, row `A7_landed_two_tracks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_intake_land_labels_native.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_landed_tracks_reads_every_native_landings_provider_tracks`

Old text:

```
    return {cid: next(iter(found)) for cid, found in named.items() if len(found) == 1}
```

New text:

```
    return {cid: sorted(found)[0] for cid, found in named.items()}
```

### `u150.A8_landed_workflow`

landed_tracks: read every workflow's record, not only a native landing's

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u150.json`, row `A8_landed_workflow`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_intake_land_labels_native.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_landed_tracks_reads_every_native_landings_provider_tracks`

Old text:

```
        if record.workflow != native.WORKFLOW:
            continue
        held = record.detail.get(label_filing.PROVIDER_KEY)
```

New text:

```
        held = record.detail.get(label_filing.PROVIDER_KEY)
```

### `u204.A1_adopt_landed`

_read_edits: a landed row tied by its ISRC is not answered as the track the account holds

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u204.json`, row `A1_adopt_landed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_landed_track_the_provider_ties_to_another_release_is_still_filed`

Old text:

```
            matcher.adopt(content_id, remote)
```

New text:

```
            pass
```

### `u207.M3_mirror_read_never_screens`

account mirror read: the plans' rows are never screened

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u207.json`, row `M3_mirror_read_never_screens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_tie.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_the_plan_screens_every_code_its_rows_will_ask_before_asking_any`

Old text:

```
    matcher.screen(
```

New text:

```
    (lambda rows: 0)(
```

### `u222.M11_decided_freeze_shown`

_record: freeze a decided run's fresh plan as shown by its gate (review round one's BLOCKING)

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M11_decided_freeze_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_decided_run_with_no_frozen_plan_says_it_planned_afresh`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_plan_made_afresh_by_a_decided_run_is_never_read_as_what_the_gate_showed`

Old text:

```
            shown=not run.decided,
```

New text:

```
            shown=True,
```

### `u222.M12_unshown_not_said`

_stale: read a record no gate showed as one it did

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M12_unshown_not_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_plan_made_afresh_by_a_decided_run_is_never_read_as_what_the_gate_showed`

Old text:

```
    if frozen is not None and not frozen.shown:
```

New text:

```
    if False:
```

### `u222.M19_stale_on_every_run`

add_steps: carry stale lines on a gate's own run too

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M19_stale_on_every_run`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_the_gate_run_and_a_report_say_nothing_stale`

Old text:

```
    if run is not None and run.decided:
        area.stale.extend
```

New text:

```
    if run is not None:
        area.stale.extend
```

### `u222.M1_overlay_not_read`

read: never overlay the frozen snapshots, so the decided run reads the ledger's live snapshot as before U222 (sitting 66)

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M1_overlay_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_genre_edit_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_join_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_leave_the_library_took_between_the_acts_applies_the_approved_plan`

Old text:

```
    if frozen is not None:
        # THE GATE'S SNAPSHOTS
```

New text:

```
    if False:
        # THE GATE'S SNAPSHOTS
```

### `u222.M20_every_step_reworded`

_stale: reword the line said when nothing moved

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M20_every_step_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_write_outside_any_mirrored_playlist_between_the_acts_is_not_stale`
  - `tests/test_organize_mirror_frozen_u222.py::test_with_nothing_between_the_acts_the_apply_rebuilds_the_frozen_plan`

Old text:

```
            else "every step plans as the gate showed it"
```

New text:

```
            else "every step plans as its gate showed it"
```

### `u222.M25_steps_not_frozen`

_record: freeze no step, so a stale answer names every step as one the gate did not show

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M25_steps_not_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_the_gate_freezes_every_step_of_the_full_account_area`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_write_outside_any_mirrored_playlist_between_the_acts_is_not_stale`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_account_change_between_the_acts_is_stale_and_names_its_folder_and_playlist`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`
  - `tests/test_organize_mirror_frozen_u222.py::test_with_nothing_between_the_acts_the_apply_rebuilds_the_frozen_plan`

Old text:

```
            steps=area.steps,
```

New text:

```
            steps=(),
```

### `u227.R8_reader_not_passed`

_read_edits: decide without the landing places

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u227.json`, row `R8_reader_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 187 against a baseline of 187
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u227.py::test_a_queued_track_filed_elsewhere_by_its_tags_is_filed_where_the_account_put_it`
  - `tests/test_organize_mirror_edits_u227.py::test_the_landings_filing_by_the_real_producer_is_read_as_the_landings`

Old text:

```
        read, {remote: sorted(rows) for remote, rows in owner.items()}, landings
```

New text:

```
        read, {remote: sorted(rows) for remote, rows in owner.items()}
```

### `u230.M18_titles_not_recorded`

_read_edits: record no titles for the queue's remote playlists

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u230.json`, row `M18_titles_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_move_in_rekordbox_after_the_carry_still_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it`

Old text:

```
                titled[mine.remote_id] = source.name
```

New text:

```
                pass
```

### `u230.M19_every_title`

_read_edits: name every recorded playlist as the one that queued each track

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u230.json`, row `M19_every_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u230.py::test_a_job_queued_from_another_playlist_does_not_lift_the_edited_ones_base`

Old text:

```
        remote: frozenset(titled[one] for one in sources if one in titled)
```

New text:

```
        remote: frozenset(titled.values())
```

### `u230.M20_queue_not_passed`

_read_edits: decide without the queue

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u230.json`, row `M20_queue_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_move_in_rekordbox_after_the_carry_still_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it`

Old text:

```
landings, queued_on

```

New text:

```
landings, {}

```

### `u236.M10_reader_no_time_check`

read edits: hand the rule every recorded placement, whatever membership holds it (round one, finding 2)

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u236.json`, row `M10_reader_no_time_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_membership_a_person_took_off_and_put_back_by_hand_is_theirs`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_deleted_and_made_again_by_hand_is_a_persons_addition[False]`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_deleted_and_made_again_by_hand_is_a_persons_addition[True]`

Old text:

```
                remote for remote, at in recorded_placed.items() if at and added.get(remote) == at
```

New text:

```
                remote for remote, at in recorded_placed.items() if at
```

### `u236.M11_reader_never_placed`

read edits: hand the rule no placement on a playlist never mirrored, the month the write made

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u236.json`, row `M11_reader_never_placed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
                read.append(edits.Mirrored(place=place, rekordbox=frozenset(wanted), placed=ours))
```

New text:

```
                read.append(edits.Mirrored(place=place, rekordbox=frozenset(wanted)))
```

### `u236.M12_reader_short_branch`

read edits: drop the placements of a month whose listing failed (round one, finding 4)

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u236.json`, row `M12_reader_short_branch`
- Moved: the reader's two Mirrored constructions, one for a failed listing and one for a read listing, were merged into one that tests listing is None per field, so dropping the failed listing's placements is now placed left empty only when listing is None
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`

Old text:

```
                rekordbox_added=added,
                placed=ours,
```

New text:

```
                rekordbox_added=added,
                placed=ours if listing is not None else frozenset(),
```

### `u309-z2.U21_reading_unread_listed`

A rekordbox area step over an unread reading is planned instead of listed

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u309-z2.json`, row `U21_reading_unread_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_reading_whose_edits_went_unread_lists_the_step_and_says_why`

Old text:

```
    if reading.unread:
        return Step(key=kind, title=title, state=LISTED, detail=reading.unread)
    return reading
```

New text:

```
    return reading
```

### `u309-z2.U22_keep_newest_time`

The newest of two membership times is replaced by the older

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u309-z2.json`, row `U22_keep_newest_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_of_two_membership_times_for_one_track_the_newest_is_kept`

Old text:

```
    if at is not None and (held is None or at > held):
```

New text:

```
    if at is not None and (held is None or at < held):
```

### `u309.U23_shared_once_error_cached`

A refused open is retried by each step of the run instead of the refusal answering all of them

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u309.json`, row `U23_shared_once_error_cached`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize_mirror.py`
- Collected: 48 against a baseline of 48
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_an_open_that_refuses_refuses_each_step_as_its_own_open_did`
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`

Old text:

```
        if key not in self._held:
            try:
```

New text:

```
        if True:
            try:
```

### `u112-b.C7_outcome_always_ok`

A run that wrote nothing ends OK rather than as a no-op

- File: `src/cratekit/organize/cli.py`
- Source: `u112-b.json`, row `C7_outcome_always_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_run_that_writes_nothing_ends_as_a_no_op`

Old text:

```
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u112.C1_report_asks`

--report no longer returns before the gates, so a report asks and may write

- File: `src/cratekit/organize/cli.py`
- Source: `u112.json`, row `C1_report_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 52 (killed)
- Killed:
  - `tests/test_organize.py::test_a_label_playlist_is_the_label_steps_and_a_set_the_archives`
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_mark_put_back_is_no_mark_and_the_playlist_stays`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[False]`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[True]`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_a_playlist_of_the_sets_name_outside_inspiration_or_removed_proves_nothing`
  - `tests/test_organize.py::test_a_playlist_of_yours_already_in_a_folder_of_yours_is_not_listed`
  - `tests/test_organize.py::test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine`
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_a_registry_the_profile_does_not_use_does_not_refuse_the_filing`
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    if report:
        data = _report(areas, report=True, answers={})
```

New text:

```
    if False:
        data = _report(areas, report=True, answers={})
```

### `u112.C5_unexpected_failure_stops`

A step failing in a way the build does not expect stops every later approved step

- File: `src/cratekit/organize/cli.py`
- Source: `u112.json`, row `C5_unexpected_failure_stops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_step_that_fails_unexpectedly_lets_the_rest_run_and_is_raised_after`

Old text:

```
            step.error = refuse(
                "internal-error",
```

New text:

```
            raise
            step.error = refuse(
                "internal-error",
```

### `u112.C6_failure_never_raised`

An approved step that failed is never raised, so the run reads as a clean organize

- File: `src/cratekit/organize/cli.py`
- Source: `u112.json`, row `C6_failure_never_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize.py::test_a_provider_refusal_mid_pass_stops_and_names_what_moved[False]`
  - `tests/test_organize.py::test_a_provider_refusal_mid_pass_stops_and_names_what_moved[True]`
  - `tests/test_organize.py::test_a_step_that_fails_unexpectedly_lets_the_rest_run_and_is_raised_after`

Old text:

```
    if not failed:
        return
    wrote = [
```

New text:

```
    if True:
        return
    wrote = [
```

### `u137.C1_named_always`

Plan an area none of whose kinds is named

- File: `src/cratekit/organize/cli.py`
- Source: `u137.json`, row `C1_named_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 17 (killed)
- Killed:
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_run_resumed_with_no_account_answer_plans_the_mirror_afresh`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_an_unread_label_registry_refuses_the_filing_rather_than_plan_it_over_no_label`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_only_a_database_kind_asks_the_database_alone`
  - `tests/test_organize.py::test_only_file_moves_a_marked_playlist_as_the_full_verb_does_and_then_plans_nothing`
  - `tests/test_organize.py::test_only_file_plans_the_filing_alone_and_the_database_is_not_asked`
  - `tests/test_organize.py::test_only_mirror_plans_and_writes_the_mirror_alone_and_a_rerun_plans_nothing`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    return selection(kinds, only) != ()
```

New text:

```
    return True
```

### `u137.C2_only_dropped`

Read --only and then plan as if it were absent

- File: `src/cratekit/organize/cli.py`
- Source: `u137.json`, row `C2_only_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 23 (killed)
- Killed:
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_a_run_resumed_with_no_account_answer_plans_the_mirror_afresh`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_an_unread_label_registry_refuses_the_filing_rather_than_plan_it_over_no_label`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`
  - `tests/test_organize.py::test_only_a_database_kind_asks_the_database_alone`
  - `tests/test_organize.py::test_only_file_moves_a_marked_playlist_as_the_full_verb_does_and_then_plans_nothing`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    only = frozenset(chosen) if chosen else None
```

New text:

```
    only = None
```

### `u137.C3_choices_dropped`

Let the parser take any word as a kind

- File: `src/cratekit/organize/cli.py`
- Source: `u137.json`, row `C3_choices_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_an_unknown_kind_is_refused_by_name_before_anything_is_read`

Old text:

```
        choices=KINDS,

```

New text:

```
(empty)
```

### `u222.M21_cli_message_unchanged`

_ask: keep the gate's bare message on a stale answer

- File: `src/cratekit/organize/cli.py`
- Source: `u222.json`, row `M21_cli_message_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_without_the_frozen_plan_the_same_two_acts_are_refused_stale`

Old text:

```
                message=f"{cause.message}; {area.name}: " + "; ".join(area.stale),
```

New text:

```
                message=cause.message,
```

### `u222.M22_cli_detail_unchanged`

_ask: carry no stale lines in the refusal's detail

- File: `src/cratekit/organize/cli.py`
- Source: `u222.json`, row `M22_cli_detail_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`

Old text:

```
                detail={**dict(cause.detail or {}), "stale": list(area.stale)},
```

New text:

```
                detail=cause.detail,
```

### `u222.M23_cli_empty_stale_reworded`

_ask: reword a stale refusal whose area has nothing to add

- File: `src/cratekit/organize/cli.py`
- Source: `u222.json`, row `M23_cli_empty_stale_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_plan_that_moves_after_the_answer_is_stale_rather_than_applied`

Old text:

```
        if exc.cause.code != ExitCode.DECISION_STALE or not area.stale:
```

New text:

```
        if exc.cause.code != ExitCode.DECISION_STALE:
```

### `u267.M1_report_shares_nothing`

organize: the report makes no shared read, so every reader opens its own handle again, seven opens

- File: `src/cratekit/organize/cli.py`
- Source: `u267.json`, row `M1_report_shares_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`
- Collected: 149 against a baseline of 149
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_report_reads_inspiration_twice_through_one_handle_and_locks_nothing_meanwhile`
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
    one_read = rb_writer.SharedRead(cfg) if report else None
```

New text:

```
    one_read = None
```

### `u267.M2_applying_run_shares`

organize: the run that answers a gate makes a shared read too, so its plans read through one handle

- File: `src/cratekit/organize/cli.py`
- Source: `u267.json`, row `M2_applying_run_shares`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`

Old text:

```
    one_read = rb_writer.SharedRead(cfg) if report else None
```

New text:

```
    one_read = rb_writer.SharedRead(cfg)
```

### `u267.M3_report_never_closes`

organize: the finally closes no shared read, so the report leaves its handle and engine open

- File: `src/cratekit/organize/cli.py`
- Source: `u267.json`, row `M3_report_never_closes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
        if one_read is not None:
            one_read.close()
```

New text:

```
        if one_read is not None:
            pass
```

### `u116.M10_year_check`

year_of_mark: a stamp that is not a date is accepted as a year

- File: `src/cratekit/organize/filing.py`
- Source: `u116.json`, row `M10_year_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_playlist_whose_mark_has_no_year_is_filed_in_mine`

Old text:

```
    except ValueError:
        return ""
```

New text:

```
    except ValueError:
        return "2026"
```

### `u116.M12_nested_folders_ignored`

playlists_in_folders: nested folders are not walked, so a playlist two deep is read as at the root

- File: `src/cratekit/organize/filing.py`
- Source: `u116.json`, row `M12_nested_folders_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[True]`

Old text:

```
        pending.extend(remote.folder_folders(folder_id))
```

New text:

```
        pass
```

### `u116.M13_utc_year`

year_of_mark: the year is taken from the UTC stamp digits rather than local time

- File: `src/cratekit/organize/filing.py`
- Source: `u116.json`, row `M13_utc_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if when.tzinfo is not None:
        when = when.astimezone()
    return f"{when.year:04d}"
```

New text:

```
    return str(marked or "")[:4]
```

### `u116.M2_set_rule_dropped`

plan: a set playlist is no longer left to the archive

- File: `src/cratekit/organize/filing.py`
- Source: `u116.json`, row `M2_set_rule_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_label_playlist_is_the_label_steps_and_a_set_the_archives`

Old text:

```
        if identity in set_built:
            rows.append(Placement(identity, name, LEFT, why=SET_STEP))
```

New text:

```
        if False:
            rows.append(Placement(identity, name, LEFT, why=SET_STEP))
```

### `u116.M5_ambiguous_moves_anyway`

_year_folder: two folders named as the year adopt the first rather than leave

- File: `src/cratekit/organize/filing.py`
- Source: `u116.json`, row `M5_ambiguous_moves_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_two_root_folders_named_as_the_year_leave_its_playlists_reported`

Old text:

```
    if len(named) > 1:
```

New text:

```
    if len(named) > 9:
```

### `u116.M6_no_adopt`

_year_folder: a root folder named as the year is ignored and a second made

- File: `src/cratekit/organize/filing.py`
- Source: `u116.json`, row `M6_no_adopt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_a_year_folder_already_on_the_account_is_adopted_with_no_set_to_make_it`
  - `tests/test_organize.py::test_an_existing_year_folder_on_the_account_is_adopted_not_made_again`

Old text:

```
    if named:
        return YearFolder(year=year, action=sets.ADOPT, folder_id=named[0], stale=recorded)
```

New text:

```
    if False:
        return YearFolder(year=year, action=sets.ADOPT, folder_id=named[0], stale=recorded)
```

### `u131.K1_mine_made_only`

filing.plan: read a Mine adopted by its name for marks too, so a playlist leaves a folder a person made

- File: `src/cratekit/organize/filing.py`
- Source: `u131.json`, row `K1_mine_made_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_hand_made_folder_named_mine_is_adopted_and_never_emptied`

Old text:

```
    if mine.made and mine.folder_id:
```

New text:

```
    if mine.folder_id:
```

### `u131.K2_exports_rule`

filing.plan: drop the Exports rule, so an exported playlist is read as product made and left

- File: `src/cratekit/organize/filing.py`
- Source: `u131.json`, row `K2_exports_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_an_exported_playlist_the_product_made_is_not_listed_as_yours`
  - `tests/test_playlist_kinds.py::test_each_kind_lands_in_its_own_folder`

Old text:

```
        if identity in exported:
```

New text:

```
        if False:
```

### `u131.K3_product_made_left`

filing.plan: drop the product made leave, so a label's dated playlist is filed in Mine

- File: `src/cratekit/organize/filing.py`
- Source: `u131.json`, row `K3_product_made_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_playlist_matching_no_rule_is_listed_and_left`

Old text:

```
        if identity in made:
            rows.append(Placement(identity, name, LEFT, why=PRODUCT_MADE))
```

New text:

```
        if False:
            rows.append(Placement(identity, name, LEFT, why=PRODUCT_MADE))
```

### `u143-b.F1_debris_first`

Filing: drop the debris branch, so a debris copy is left as the label step's and the root step never sees it

- File: `src/cratekit/organize/filing.py`
- Source: `u143-b.json`, row `F1_debris_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_organize_root.py`, `tests/test_playlist_kinds.py`
- Collected: 166 against a baseline of 166
- Kills: 16 (killed)
- Killed:
  - `tests/test_organize.py::test_only_root_removes_debris_and_empties_on_the_gate_and_files_the_legacy_folder`
  - `tests/test_organize.py::test_the_full_verb_lists_the_working_custom_and_never_the_root_steps_removals`
  - `tests/test_organize_root.py::test_a_debris_copy_given_a_track_since_the_plan_is_kept_and_the_rest_removed`
  - `tests/test_organize_root.py::test_a_debris_copy_whose_tracks_could_not_all_be_read_is_left`
  - `tests/test_organize_root.py::test_a_debris_copy_with_a_track_the_label_folder_lacks_is_left_naming_it`
  - `tests/test_organize_root.py::test_a_debris_copy_with_no_listed_count_is_left_before_any_read`
  - `tests/test_organize_root.py::test_a_followed_labels_recorded_folder_is_read_whatever_it_is_called_now`
  - `tests/test_organize_root.py::test_a_label_folder_that_cannot_be_read_leaves_its_debris_and_refuses_nothing_else`
  - `tests/test_organize_root.py::test_a_label_folder_with_no_downloaded_playlist_proves_nothing`
  - `tests/test_organize_root.py::test_a_refusal_part_way_stops_and_names_what_was_removed`
  - `tests/test_organize_root.py::test_a_second_run_on_a_clean_root_plans_nothing`
  - `tests/test_organize_root.py::test_a_year_playlist_held_as_taken_with_no_prefix_proves_its_tracks_downloaded`
  - `tests/test_organize_root.py::test_an_empty_debris_copy_is_removed_as_empty`
  - `tests/test_organize_root.py::test_debris_with_no_label_folder_or_two_of_them_is_left_with_why`
  - `tests/test_organize_root.py::test_four_identical_debris_copies_with_every_track_filed_plan_four_removals`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if not claimed and is_library_debris(name):
```

New text:

```
        if False:
```

### `u143-b.F2_empty_unclaimed`

Filing: an empty playlist a ledger claims is read as empty too

- File: `src/cratekit/organize/filing.py`
- Source: `u143-b.json`, row `F2_empty_unclaimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_organize_root.py`, `tests/test_playlist_kinds.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_an_empty_playlist_the_product_made_or_a_placeholder_is_never_removed`

Old text:

```
        empty = not claimed and one.tracks == 0
```

New text:

```
        empty = one.tracks == 0
```

### `u143-b.F4_legacy_record_stale`

Year folder: reuse a recorded folder now named as a legacy year folder

- File: `src/cratekit/organize/filing.py`
- Source: `u143-b.json`, row `F4_legacy_record_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_organize_root.py`, `tests/test_playlist_kinds.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_year_record_whose_folder_now_carries_a_legacy_name_is_not_reused`

Old text:

```
        and not kinds.legacy_year(root[recorded])
    ):
```

New text:

```
    ):
```

### `u242.M23_filing_dates_a_found_prefix`

filing: read a taken entry the migration found as a dated mark, filing it by the migration's year

- File: `src/cratekit/organize/filing.py`
- Source: `u242.json`, row `M23_filing_dates_a_found_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_organize_root.py`, `tests/test_organize.py`
- Collected: 198 against a baseline of 198
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_root.py::test_filing_reads_a_stripped_hand_mark_as_it_read_the_prefixed_one`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_filing_reads_a_found_prefix_as_undated_and_a_pass_mark_as_dated`

Old text:

```
        if entry.held and entry.dated:
```

New text:

```
        if entry.held:
```

### `u309-z2.U18_part_way_step_again`

A filing or root apply failing part way no longer tells the person to run again

- File: `src/cratekit/organize/filing.py`
- Source: `u309-z2.json`, row `U18_part_way_step_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_organize_root.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_refusal_part_way_ends_its_steps_with_running_the_verb_again`

Old text:

```
        remedy=cause.remediation.remedy, steps=(*cause.remediation.steps, again),
```

New text:

```
        remedy=cause.remediation.remedy, steps=tuple(cause.remediation.steps),
```

### `u309-z2.U20_year_folder_reserved_once`

Each move into a year reserves that year's folder again

- File: `src/cratekit/organize/filing.py`
- Source: `u309-z2.json`, row `U20_year_folder_reserved_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_organize_root.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_two_moves_into_one_year_reserve_its_folder_once`

Old text:

```
    if year not in done.folders:
        done.folders[year] = reserve_year(
```

New text:

```
    if True:
        done.folders[year] = reserve_year(
```

### `u309.U19_part_way_totals`

A filing or root apply failing part way no longer carries what it moved in its detail

- File: `src/cratekit/organize/filing.py`
- Source: `u309.json`, row `U19_part_way_totals`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_organize_root.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_a_provider_refusal_mid_pass_stops_and_names_what_moved[True]`
  - `tests/test_organize_root.py::test_a_refusal_part_way_stops_and_names_what_was_removed`

Old text:

```
        detail={**dict(cause.detail), **done.totals()}, inner=cause,
```

New text:

```
        detail=dict(cause.detail), inner=cause,
```

### `r1295.M10_unread_off_misses`

_matched: an unread track is not among the set's misses

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M10_unread_off_misses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
    misses: list[Miss] = list(unread)
```

New text:

```
    misses: list[Miss] = []
```

### `r1295.M11_again_drops_unread`

again: the write re-decides without the unread tracks, so the approved plan reads stale

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M11_again_drops_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`

Old text:

```
                    row.withheld,
                    row_of,
                    row.unread,
```

New text:

```
                    row.withheld,
                    row_of,
                    (),
```

### `r1295.M12_setrow_keeps_no_unread`

_decided: the set row keeps no unread tracks for the write to decide from

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M12_setrow_keeps_no_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`

Old text:

```
        unread=unread,
    )
```

New text:

```
        unread=(),
    )
```

### `r1295.M13_unread_miss_no_id`

_unread_miss: the miss line names no track id

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M13_unread_miss_no_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
f"{one.why} (track {one.ref}), so it was not asked of the library"
```

New text:

```
f"{one.why}, so it was not asked of the library"
```

### `r1295.M14_unread_miss_blank_title`

_unread_miss: an absent title shown blank rather than as no title

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M14_unread_miss_blank_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
        one.title or "no title",
```

New text:

```
        one.title,
```

### `r1295.M15_plan_passes_no_unread`

plan: the readable sets are decided with no unread misses

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M15_plan_passes_no_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
                    tuple(_unread_miss(place, one) for place, one in listing.unread),
```

New text:

```
                    (),
```

### `r1295.M17_skip_guard`

plan (existing guard, sample): a set INSPIRATION already holds is read and planned again

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M17_skip_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_already_under_inspiration_is_skipped_and_its_tracks_never_read`

Old text:

```
        if name in held:
```

New text:

```
        if False:
```

### `r1295.M1_refused_row_fatal`

_read: every refused row raises again, so one untitled track leaves the whole set unread as on main

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M1_refused_row_fatal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_is_filed_unread_naming_each`
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
            one = intake_cli.set_aside(row)
            if not one.ref:
```

New text:

```
            one = intake_cli.set_aside(row)
            if True:
```

### `r1295.M2_no_id_named`

_read: a refused row with no provider id is named as a miss rather than leaving its set unread

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M2_no_id_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_whose_unread_track_carries_no_provider_id_is_still_filed_unread`

Old text:

```
            if not one.ref:
```

New text:

```
            if False:
```

### `r1295.M3_read_positions_renumbered`

_read: a read track's place counts only the rows read, so a miss after an unread row is misplaced

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M3_read_positions_renumbered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
            wanted.append((position, match.read_row(
```

New text:

```
            wanted.append((len(wanted) + 1, match.read_row(
```

### `r1295.M4_unread_positions_renumbered`

_read: an unread track's place counts only the unread rows

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M4_unread_positions_renumbered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`

Old text:

```
            unread.append((position, one))
```

New text:

```
            unread.append((len(unread) + 1, one))
```

### `r1295.M5_all_unread_branch`

plan: drop the every track unread branch, so such a set reads as one with no match

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M5_all_unread_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_is_filed_unread_naming_each`
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`

Old text:

```
        if listing.unread and not listing.wanted:
```

New text:

```
        if False:
```

### `r1295.M6_none_read_uncapped`

_none_read: name every unread track rather than the first five

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M6_none_read_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`

Old text:

```
listing.unread[:NAMED_UNREAD])
```

New text:

```
listing.unread)
```

### `r1295.M7_none_read_rest_uncounted`

_none_read: say nothing of the unread tracks past the fifth

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M7_none_read_rest_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`

Old text:

```
    if rest > 0:
```

New text:

```
    if False:
```

### `r1295.M8_none_read_withheld_dropped`

_none_read: say nothing of the tracks the provider withheld

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M8_none_read_withheld_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`

Old text:

```
    if listing.withheld:
        said +=
```

New text:

```
    if False:
        said +=
```

### `r1295.M9_misses_unsorted`

_matched: misses kept unread first rather than in set order

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M9_misses_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`

Old text:

```
tuple(sorted(misses, key=lambda miss: miss.position))
```

New text:

```
tuple(misses)
```

### `u144-a.A1_skip_rule`

Plan: drop the skip of a set INSPIRATION already holds, so it is read and planned again

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A1_skip_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_already_under_inspiration_is_skipped_and_its_tracks_never_read`

Old text:

```
        if name in held:
            rows.append(SetRow(name, playlist_id, folder, SKIP))
```

New text:

```
        if False:
            rows.append(SetRow(name, playlist_id, folder, SKIP))
```

### `u144-a.A2_two_of_one_name`

Plan: drop the two account sets of one name check, so both are read and planned

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A2_two_of_one_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_two_account_sets_of_one_name_are_both_left`

Old text:

```
        if named[name] > 1:
```

New text:

```
        if False:
```

### `u144-a.A4_sets_folder_name`

Account sets: read every root folder, not only a Downloaded Sets year or a recorded one

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A4_sets_folder_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_sets_folder_the_archive_recorded_is_read_whatever_it_is_called_now`
  - `tests/test_organize_inspiration.py::test_only_prefixed_playlists_in_a_downloaded_sets_folder_are_sets`

Old text:

```
        if not sets_folder(folder_name) and folder_id not in marked:
```

New text:

```
        if False:
```

### `u144-a.A5_recorded_folder`

Account sets: ignore the ledger's record, so a renamed sets folder is passed over

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A5_recorded_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_sets_folder_the_archive_recorded_is_read_whatever_it_is_called_now`

Old text:

```
        if not sets_folder(folder_name) and folder_id not in marked:
```

New text:

```
        if not sets_folder(folder_name):
```

### `u144-a.A6_set_name_spelling`

Account sets: write the stripped account name as it is, slash and all

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A6_set_name_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_the_name_written_is_the_account_name_without_its_prefix[DOWNLOADED 5_28_26 A b2b B / Night 10-18-5_28_26 A b2b B - Night 10-18]`

Old text:

```
            sets_found.append((folder_name, playlist_id, set_cli.set_name(stripped)))
```

New text:

```
            sets_found.append((folder_name, playlist_id, stripped))
```

### `u144-a.A7_only_matched`

Match: take a track with no row as a member, an empty id in the playlist

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A7_only_matched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 8 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_near_match_is_a_question_named_as_a_miss_and_never_written`
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_with_no_match_is_reported_and_no_empty_playlist_is_written`
  - `tests/test_organize_inspiration.py::test_a_step_whose_every_set_has_no_match_plans_nothing_and_writes_nothing`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`
  - `tests/test_organize_inspiration.py::test_eighteen_tracks_fifteen_in_the_library_plan_fifteen_and_name_three`
  - `tests/test_organize_inspiration.py::test_the_writer_refuses_a_membership_the_plan_did_not_name`

Old text:

```
        held, why = row_of(one)
        if held:
```

New text:

```
        held, why = row_of(one)
        if True:
```

### `u144-a.A8_empty_not_written`

Decide: plan a set with no match as a create, an empty playlist

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A8_empty_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_with_no_match_is_reported_and_no_empty_playlist_is_written`
  - `tests/test_organize_inspiration.py::test_a_step_whose_every_set_has_no_match_plans_nothing_and_writes_nothing`

Old text:

```
        action=CREATE if members else EMPTY,
```

New text:

```
        action=CREATE,
```

### `u144-b.B1_unnamed_membership`

Write guard: drop the refusal of a membership the approved plan did not name

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B1_unnamed_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_the_writer_refuses_a_membership_the_plan_did_not_name`

Old text:

```
        if unnamed:
```

New text:

```
        if False:
```

### `u144-b.B2_stale_digest`

Write guard: drop the digest comparison of the plan taken again on the write handle

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B2_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_given_its_inspiration_playlist_since_the_plan_is_stale`

Old text:

```
    if now.digest() != approved.digest():
```

New text:

```
    if False:
```

### `u144-b.B4_convergence_latch`

Write: drop the INSPIRATION tree's convergence latch before the session

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B4_convergence_latch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_convergence_latch_refuses_the_write_before_anything_is_written`

Old text:

```
        convergence.assert_tree_writable(cfg, db, approved.tree_id, tree_registry.read(cfg))
```

New text:

```
        pass
```

### `u144-b.B5_read_back_exact`

Read back: accept a made playlist holding rows the plan did not name, or out of order

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B5_read_back_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_read_back_holding_a_row_the_plan_did_not_name_is_refused`

Old text:

```
        if missing or (one.created and not exact):
```

New text:

```
        if missing:
```

### `u144-b.B6_read_back_missing`

Read back: accept a found playlist missing a planned row

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B6_read_back_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_read_back_holding_a_row_the_plan_did_not_name_is_refused`

Old text:

```
        if missing or (one.created and not exact):
```

New text:

```
        if one.created and not exact:
```

### `u144-b.B7_writes_the_members`

Write: add every member but the first

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B7_writes_the_members`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 8 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_readable_track_with_no_provider_id_is_matched_as_before`
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_with_no_match_is_reported_and_no_empty_playlist_is_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_eighteen_tracks_fifteen_in_the_library_plan_fifteen_and_name_three`
  - `tests/test_organize_inspiration.py::test_the_name_written_is_the_account_name_without_its_prefix[DOWNLOADED 5_28_26 A b2b B / Night 10-18-5_28_26 A b2b B - Night 10-18]`
  - `tests/test_organize_inspiration.py::test_the_name_written_is_the_account_name_without_its_prefix[DOWNLOADED 5_28_26 Probe DJ Femme House Mix 10-18-5_28_26 Probe DJ Femme House Mix 10-18]`

Old text:

```
        added = rb_writer.add_memberships(db, playlist, row.members)
```

New text:

```
        added = rb_writer.add_memberships(db, playlist, row.members[1:])
```

### `u144-b.B8_commit_recorded`

Record: record no commit, so a restore cannot weigh the session

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B8_commit_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_eighteen_tracks_fifteen_in_the_library_plan_fifteen_and_name_three`

Old text:

```
    made = [one for one in wrote if one.added or one.created]
```

New text:

```
    made = []
```

### `u144-c.C1_again_now_held`

B3 measured again after the stale test was tightened: a set given its INSPIRATION playlist since the plan is decided as before, not skipped

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-c.json`, row `C1_again_now_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_given_its_inspiration_playlist_since_the_plan_is_stale`

Old text:

```
                replace(row, action=SKIP, members=(), misses=(), withheld=0, why="")
                if now
```

New text:

```
                replace(row, action=SKIP, members=(), misses=(), withheld=0, why="")
                if False
```

### `u144-c.C2_folder_unread`

Account sets: let a folder listing refusal refuse the whole step instead of one folder

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-c.json`, row `C2_folder_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_sets_folder_that_cannot_be_listed_is_named_and_the_rest_still_plan`

Old text:

```
            listed = remote.folder_playlists(folder_id)
        except CratekitError as exc:
```

New text:

```
            listed = remote.folder_playlists(folder_id)
        except ZeroDivisionError as exc:
```

### `u144-c.C4_missed_coefficient`

Counts: leave the withheld tracks out of the tracks missed

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-c.json`, row `C4_missed_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_short_listing_counts_what_the_provider_withheld`

Old text:

```
            "tracks missed": sum(len(row.misses) + row.withheld for row in self.creates),
```

New text:

```
            "tracks missed": sum(len(row.misses) for row in self.creates),
```

### `u246.S5_inspiration_held_empty`

assert_read_back (inspiration): an empty set of live rows, so every planned row reads as missing and the write refuses

- File: `src/cratekit/organize/inspiration.py`
- Source: `u246.json`, row `S5_inspiration_held_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/test_u242_taken.py`, `tests/test_write_session.py`, `tests/test_organize.py`
- Collected: 329 against a baseline of 329
- Kills: 9 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_read_back_holding_a_row_the_plan_did_not_name_is_refused`
  - `tests/test_organize_inspiration.py::test_a_readable_track_with_no_provider_id_is_matched_as_before`
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_with_no_match_is_reported_and_no_empty_playlist_is_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_eighteen_tracks_fifteen_in_the_library_plan_fifteen_and_name_three`
  - `tests/test_organize_inspiration.py::test_the_name_written_is_the_account_name_without_its_prefix[DOWNLOADED 5_28_26 A b2b B / Night 10-18-5_28_26 A b2b B - Night 10-18]`
  - `tests/test_organize_inspiration.py::test_the_name_written_is_the_account_name_without_its_prefix[DOWNLOADED 5_28_26 Probe DJ Femme House Mix 10-18-5_28_26 Probe DJ Femme House Mix 10-18]`

Old text:

```
        held = set(live)
```

New text:

```
        held = set()
```

### `u246.S6_inspiration_planned_live`

assert_read_back (inspiration): the planned set built from the live rows, so the refusal names no unplanned row

- File: `src/cratekit/organize/inspiration.py`
- Source: `u246.json`, row `S6_inspiration_planned_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/test_u242_taken.py`, `tests/test_write_session.py`, `tests/test_organize.py`
- Collected: 329 against a baseline of 329
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_read_back_holding_a_row_the_plan_did_not_name_is_refused`

Old text:

```
            planned = set(one.members)
```

New text:

```
            planned = set(live)
```

### `r1289.M14_mirror_unread_branch`

mirror_downloads.plan: drop the unread branch, so an unread wanted track is named as one the provider did not list

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `r1289.json`, row `M14_mirror_unread_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_untitled_track_on_a_mirrored_playlist_is_named_and_the_others_queue`

Old text:

```
            if track in unread:
```

New text:

```
            if False:
```

### `r1289.M15_mirror_reads_whole`

mirror_downloads._catalogue_listing: read the playlist whole again (the declared reader is asked first), so one untitled row names every wanted track on it

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `r1289.json`, row `M15_mirror_reads_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_untitled_track_on_a_mirrored_playlist_is_named_and_the_others_queue`

Old text:

```
        return intake_cli.list_playlist_readable(found[0], playlist_id)
```

New text:

```
        intake_cli.list_playlist_declared(found[0], playlist_id)
        return intake_cli.list_playlist_readable(found[0], playlist_id)
```

### `r1289.M16_mirror_why`

mirror_downloads.plan: the unread track's why reworded so it does not carry the reader's words

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `r1289.json`, row `M16_mirror_why`
- Moved: the unread track's line stays in mirror_downloads.plan, whose named entry is now written on fewer lines, so the same words sit eight spaces shallower; same rewording
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_untitled_track_on_a_mirrored_playlist_is_named_and_the_others_queue`

Old text:

```
                    f"added on the account, but {unread[track].why}, so the "
```

New text:

```
                    f"added on the account, but it could not be read, so the "
```

### `r1289.M17_mirror_listing_refusal`

mirror_downloads.plan (existing guard, sample): a playlist the provider cannot list names nothing for its tracks

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `r1289.json`, row `M17_mirror_listing_refusal`
- Moved: the not queued entry mirror_downloads.plan names for a playlist the provider cannot list is now built by the shared _not_queued helper instead of an inline dict; the same loop over its tracks is emptied
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_playlist_the_provider_cannot_list_is_named_and_the_others_queue`

Old text:

```
                _not_queued(track, title, f"the provider could not list the playlist: {exc.cause.message}")
                for track in sorted(set(tracks))

```

New text:

```
                _not_queued(track, title, f"the provider could not list the playlist: {exc.cause.message}")
                for track in ()

```

### `u204.D1_one_queue_per_track`

mirror_downloads.plan: a track two playlists want is queued twice

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u204.json`, row `D1_one_queue_per_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_inbox_or_favorites_that_the_library_lacks_is_queued`

Old text:

```
        if decision.track in taken:
```

New text:

```
        if False:
```

### `u204.D2_write_rereads_queue`

mirror_downloads.write: two plans approved one after the other queue a track twice

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u204.json`, row `D2_write_rereads_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_two_plans_approved_one_after_the_other_queue_a_track_once`

Old text:

```
            fresh = {track: frozen for track, frozen in tracks.items() if track not in already}
```

New text:

```
            fresh = dict(tracks)
```

### `u204.D3_owned_recording`

mirror_downloads.plan: another release of an owned recording is queued

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u204.json`, row `D3_owned_recording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_recording_the_library_holds_in_no_playlist_is_never_queued`
  - `tests/test_organize_mirror_edits_u204.py::test_another_release_of_an_owned_recording_is_never_queued_nor_swapped`

Old text:

```
            rows = owned(frozen[track].get("isrc")) if track in frozen else ()
```

New text:

```
            rows = ()
```

### `u204.D4_never_lands_named`

mirror_downloads.outcomes: a finished download that found the track owned is said to await its landing

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u204.json`, row `D4_never_lands_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_finished_download_that_never_lands_is_never_said_to_await_one[missing-could not be fetched]`
  - `tests/test_organize_mirror_edits_u204.py::test_a_finished_download_that_never_lands_is_never_said_to_await_one[owned-already holds it]`

Old text:

```
                why = _NEVER_LANDS.get(str(report.get("state")))
```

New text:

```
                why = None
```

### `u227.R10_one_approval`

filed: every entry since the queue is the landing's, whatever its approval (round one's F1)

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u227.json`, row `R10_one_approval`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u227.py::test_a_refiling_through_adoption_after_the_landing_is_not_the_landings`

Old text:

```
            if entry.digest != first.digest:
                continue
```

New text:

```
            if False:
                continue
```

### `u227.R23_person_digest`

filed: read an approval a person gave adopt apply as the landing's (round two's F2)

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u227.json`, row `R23_person_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u227.py::test_a_persons_first_filing_after_a_landing_that_filed_nothing_is_not_the_landings`

Old text:

```
        if entry.tree == tree and entry.digest not in by_person:
```

New text:

```
        if entry.tree == tree:
```

### `u227.R9_before_queue`

filed: an entry applied before the track was queued is read as the landing's

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u227.json`, row `R9_before_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u227.py::test_a_filing_recorded_before_the_download_was_queued_is_not_the_landings`

Old text:

```
            and at >= after
```

New text:

```
            and True
```

### `u230.M15_source_blank`

queued_from: name no source for any job

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u230.json`, row `M15_source_blank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 6 (killed)
- Killed:
  - `tests/test_mirror_downloads_queued_from_u230.py::test_a_cancelled_job_another_source_and_another_library_name_nothing`
  - `tests/test_mirror_downloads_queued_from_u230.py::test_each_track_is_named_with_every_playlist_whose_job_queued_it`
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_job_queued_from_another_playlist_does_not_lift_the_edited_ones_base`
  - `tests/test_organize_mirror_edits_u230.py::test_a_move_in_rekordbox_after_the_carry_still_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it`

Old text:

```
            held.setdefault(str(remote), set()).add(source)
```

New text:

```
            held.setdefault(str(remote), set()).add("")
```

### `u230.M16_unread_raises`

queued_from: a queue that cannot be read raises, stopping the organize

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u230.json`, row `M16_unread_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_downloads_queued_from_u230.py::test_a_queue_that_cannot_be_read_names_nothing`

Old text:

```
    except (CratekitError, OSError, ValueError):
        return {}
    held: dict[str, set[str]] = {}
```

New text:

```
    except (CratekitError, OSError, ValueError):
        raise
    held: dict[str, set[str]] = {}
```

### `u267.M13_downloads_owned_opens_its_own`

mirror_downloads.plan: hand no shared read to the ISRC read, which then opens its own handle in the report

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u267.json`, row `M13_downloads_owned_opens_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_one_read.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_the_downloads_plan_reads_the_library_through_a_reports_one_handle`

Old text:

```
        owned = _owned(cfg, reading, one_read)
```

New text:

```
        owned = _owned(cfg, reading)
```

### `u201-composites.C5_leave_nothing`

plan: a move leaves no tree playlist, the thing O4 narrows

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201-composites.json`, row `C5_leave_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_library_moved_since_the_plan_writes_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_mirror_made_before_u201_is_agreed_by_its_first_run_and_an_edit_after_it_is_taken`
  - `tests/test_organize_mirror_edits.py::test_a_move_to_unsorted_clears_the_energy`
  - `tests/test_organize_mirror_edits.py::test_a_move_within_a_genre_keeps_the_genre_and_moves_the_energy_to_the_nearest`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
            leave_ids = [pid for pid in held if pid not in wanted and routed(tree.names[pid])]
```

New text:

```
            leave_ids = []
```

### `u201.O1_latch`

write: the tree's convergence latch is not asked

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O1_latch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_tree_the_product_latched_refuses_the_write_before_any_file_is_tagged`

Old text:

```
        convergence.assert_tree_writable(cfg, db, tree_id, registry)
```

New text:

```
        pass
```

### `u201.O2_stale`

_stale: a library moved since the plan is written

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O2_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_library_moved_since_the_plan_writes_nothing`

Old text:

```
    if approved.identity() != now.identity():
```

New text:

```
    if False:
```

### `u201.O3_target_bucket`

target_tags: a genre word filing into another bucket is taken

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O3_target_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_mirror_made_before_u201_is_agreed_by_its_first_run_and_an_edit_after_it_is_taken`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_the_tags_are_the_nearest_pair_routing_files_into_the_place[Minimal / Deep Tech-Low Energy-Deep House-9-expected6]`
  - `tests/test_organize_mirror_edits.py::test_the_tags_are_the_nearest_pair_routing_files_into_the_place[Tech House-Med-Deep House-2-expected0]`
  - `tests/test_organize_mirror_edits.py::test_the_tags_are_the_nearest_pair_routing_files_into_the_place[Tech House-None-Deep House-5-expected4]`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
        if routing.resolve_bucket(declared, word).bucket_id != bucket_id:
```

New text:

```
        if False:
```

### `u204.O2_unfavourite_leaves_months`

_plan_favourites: an unfavourite leaves All Favorites alone and stays in its months

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O2_unfavourite_leaves_months`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_removed_from_all_favorites_leaves_the_favorites_folder`

Old text:

```
            leave += [(pid, folder, name) for name, pid in filing if pid in held]
```

New text:

```
            leave += []
```

### `u204.O3_quarter_refused`

_plan_favourites: a favourite put in a quarter is filed into it

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O3_quarter_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_put_in_a_quarter_is_named_and_not_filed`

Old text:

```
            if placeholders.MONTH_LABEL.fullmatch(month) is None and month != placeholders.UNDATED:
```

New text:

```
            if False:
```

### `u204.O4_colour`

_plan_favourites: a favourite with no colour is not coloured Pink

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O4_colour`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_all_favorites_is_favourited_in_its_month_and_coloured`

Old text:

```
        takes = bool(pink) and decision.content_id in colour.sort_rows(db, pink, [decision.content_id]).to_colour
```

New text:

```
        takes = False
```

### `u204.O5_batch_live`

_plan_inbox: a batch no longer directly under INBOX is written as if it were

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O5_batch_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_batch_moved_into_old_since_the_plan_is_never_touched`

Old text:

```
        if len(found) != 1:
```

New text:

```
        if False:
```

### `u204.O6_inbox_latch`

write: an INBOX edit asks no intake tree latch

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O6_inbox_latch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_inbox_edit_over_a_latched_intake_tree_writes_nothing`

Old text:

```
    if edits.INBOX in touched:
```

New text:

```
    if False:
```

### `u204.O7_restore_detected`

write: a favourites only write detects no out of band restore

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O7_restore_detected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_favourites_only_write_detects_an_out_of_band_restore_and_asks_no_tree_latch`

Old text:

```
    if touched and not touched & {edits.GENRE, edits.INBOX}:
```

New text:

```
    if False:
```

### `u236.M13_write_records_no_month`

write: record no month placement, so settle records none

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M13_write_records_no_month`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
        if at:
            done.months.append((one.content_id, one.month, at))
```

New text:

```
        if False:
            done.months.append((one.content_id, one.month, at))
```

### `u236.M14_write_wrong_time`

write: record a time no membership carries

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M14_write_wrong_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
            done.months.append((one.content_id, one.month, at))
```

New text:

```
            done.months.append((one.content_id, one.month, at + "x"))
```

### `u236.M15_settle_month_title`

settle: record the placement under the month's bare name, not its account title

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M15_settle_month_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 8 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_hand_addition_after_the_placement_is_dropped_is_read_as_one`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_organize_after_the_favourite_puts_it_in_the_accounts_month`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
                mirror.title(decision.to.folder, month_of[decision.content_id][0]),
```

New text:

```
                month_of[decision.content_id][0],
```

### `u236.M16_settle_any_favourite`

settle: record a placement for a favourite put in a month on the account too

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M16_settle_any_favourite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`

Old text:

```
            and decision.to.primary
            and month_of.get(decision.content_id)
```

New text:

```
            and month_of.get(decision.content_id)
```

### `u340.R17_edit_second_path_off`

_plan_genre: read a track with two genres as one, so an account edit in one folder is taken as today

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u340.json`, row `R17_edit_second_path_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_organize_mirror_edits_u340.py`, `tests/test_organize_mirror_edits.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u340.py::test_a_band_move_in_one_folder_moves_the_energy_in_both_and_keeps_the_second_genre`

Old text:

```
        elif two is not None:
```

New text:

```
        elif False:
```

### `u340.R18_edit_off_other`

_second_genre_tags: drop the check that the edit left the other folder, so a take off of one folder is read as a no op

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u340.json`, row `R18_edit_off_other`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_organize_mirror_edits_u340.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u340.py::test_taking_it_off_one_folder_alone_is_listed_and_not_taken`
  - `tests/test_second_genre.py::test_an_edit_that_does_not_say_which_genre_changed_is_not_taken[off-first]`
  - `tests/test_second_genre.py::test_an_edit_that_does_not_say_which_genre_changed_is_not_taken[off-second]`

Old text:

```
        if other in left:
```

New text:

```
        if False:
```

### `r1031.M21_run_id_unchecked`

mirror_frozen._path: name a file from any run identifier

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `r1031.json`, row `M21_run_id_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_run_identifier_that_cannot_name_a_file_is_not_frozen`

Old text:

```
    if not _RUN_ID.match(run_id):
```

New text:

```
    if False:
```

### `r1031.M22_record_binding_unchecked`

mirror_frozen.load: rebuild from a record of another version or another run

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `r1031.json`, row `M22_record_binding_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`
- Collected: 134 against a baseline of 134
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_frozen_plan_of_another_version_or_run_is_not_rebuilt`
  - `tests/test_organize_mirror_frozen.py::test_each_folders_edit_rule_survives_the_freeze_and_a_version_3_record_is_planned_afresh`

Old text:

```
        if data.get("version") != VERSION or data.get("run_id") != run_id:
```

New text:

```
        if False:
```

