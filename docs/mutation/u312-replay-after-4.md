# Mutation table: u312-replay-after-4

Measured by `scripts/mutate.py` on 2026-11-23 10:41 UTC, branch `HEAD` at `55e2f3b6`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22479 collected. pytest invocations for this batch: 189.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 35, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `known/scratch.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22479 against 22479. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u206.M23_lookup_line_dropped` | `src/cratekit/cli/__init__.py` | user | 9 file(s) | 1130 | 3 | killed |
| `u206.M17_account_hit_ignored` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 9 file(s) | 1130 | 13 | killed |
| `r290-author.S07_rebuild_call_removed` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 126 | 6 | killed |
| `r290-author.S05_intake_call_removed` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 126 | 11 | killed |
| `r312.W6_type_not_carried` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 126 | 1 | killed |
| `r290-author.S02_acquire_download_call_removed` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 195 | 11 | killed |
| `r290-author.R2_backup_rebuild_drops_the_type` | `src/cratekit/backup/cli.py` | user | 2 file(s) | 215 | 2 | killed |
| `r290-author.S04_backup_call_removed` | `src/cratekit/backup/cli.py` | user | 2 file(s) | 215 | 11 | killed |
| `r290-author.S06_label_call_removed` | `src/cratekit/label/cli.py` | user | 2 file(s) | 208 | 17 | killed |
| `r290-author.S13_outbound_shell_call_removed` | `src/cratekit/modules/outbound/shell.py` | user | 2 file(s) | 249 | 18 | killed |
| `r290-author.S08_route_resort_call_removed` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 323 | 11 | killed |
| `r290-author.R1_retag_rebuild_drops_the_type` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 228 | 2 | killed |
| `r290-author.S11_tagging_shell_call_removed` | `src/cratekit/core/jobs.py` | user | 5 file(s) | 347 | 48 | killed |
| `r390-a.A2_retry_refuses_any_closed_job_with_a_cause` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 296 | 9 | killed |
| `u182.M13_identity_parse` | `src/cratekit/cli/jobs.py` | user | 2 file(s) | 155 | 3 | killed |
| `u101.G10_ungated_not_reported_in_judged_label` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 3 | killed |
| `u101.G11_keep_read_as_drop` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 12 | killed |
| `u101.G12_reported_share_not_the_taxonomys` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G13_family_count_off_by_one` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u101.G14_classified_counts_unjudged` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G17_refusal_silent_on_held` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G18_no_op_claims_held` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G1_held_is_listed` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 7 | killed |
| `u101.G20_summary_held_empty` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 5 | killed |
| `u101.G2_judged_per_release` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 10 | killed |
| `u101.G3_all_labels_one_group` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 4 | killed |
| `u101.G4_unlabelled_grouped_together` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G5_unread_label_judged` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G6_unread_from_every_label` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u101.G7_mixed_is_a_genre` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G8_case_is_a_difference` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G9_mapping_row_unread` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u308.L6_ended_outcome_ignored` | `src/cratekit/label/review_common.py` | user | 4 file(s) | 366 | 20 | killed |
| `u75-a.A1_kind_filter` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A3_nothing_accepted_before_the_catalogue` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A5_only_the_seams_exception_is_gone` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A6_no_identifier_is_not_asked_of_the_provider` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A7_each_row_read_alone` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B11_write_failure_is_the_verbs_refusal` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B1_outage_threshold` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B3_only_a_provider_failure_counts` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B7_same_recording_listed_once` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B9_name_digests_the_provenance` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 2 | killed |
| `u75-zeros.B6_missing_and_nothing_listable_refuses` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `r840-a.A2_a_name_is_not_asked_about` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 6 | killed |
| `r840-a.A3_unreadable_verdict_is_decided` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-a.A4_only_label_releases` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-a.A5_no_identifier_is_not_read` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-a.A6_another_items_release_is_not_read` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-a.A7_catalogue_opened_on_demand` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-a.A8_outage_bound` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-a.A9_an_answer_resets_the_count` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B10_unaddressed_is_keyed_by_item` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-b.B11_left_counts_what_was_not_reached` | `src/cratekit/label/artists_cli.py` | maintainer | 1 file(s) | 61 | 6 | killed |
| `r840-b.B1_only_the_seams_exception_is_not_served` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-b.B2_a_refusal_stops_the_run` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-b.B3_no_name_never_blanks` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B4_an_unread_release_refuses` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B5_decided_meanwhile_is_not_fine` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B6_put_right_meanwhile_is_kept` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B7_addresses_are_what_still_read_one` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 5 | killed |
| `r840-b.B8_only_the_artist_is_rewritten` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 3 | killed |
| `r840-b.B9_a_refusal_carries_why_each_read_failed` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-c.C1_the_function_is_handed_the_payload_as_it_stands` | `src/cratekit/core/review.py` | user | 2 file(s) | 137 | 34 | killed |
| `r840-c.C2_the_function_is_only_handed_an_open_item` | `src/cratekit/core/review.py` | user | 2 file(s) | 137 | 4 | killed |
| `r798-a.K1_the_first_rule_that_matches_wins` | `src/cratekit/core/routing.py` | user | 3 file(s) | 1150 | 3 | killed |
| `r798-d.K11_the_shared_matcher_reads_a_substring_needle` | `src/cratekit/core/routing.py` | user | 3 file(s) | 1150 | 101 | killed |
| `r798-a.K6_the_default_kind_is_one_a_rule_names` | `src/cratekit/core/taxonomy_build.py` | user | 3 file(s) | 1150 | 1 | killed |
| `r798-a.K8_a_kind_is_one_word` | `src/cratekit/core/taxonomy_build.py` | user | 3 file(s) | 1150 | 1 | killed |
| `u308.L5_extended_step_dropped` | `src/cratekit/label/review_common.py` | user | 3 file(s) | 247 | 8 | killed |
| `r835-b.M1_only_the_batch_years_marked` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-b.M5_deleted_folder_said` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-c.M4_recheck_before_rename_again` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-a.F4_recorded_and_refused_not_asked_again` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 5 | killed |
| `r1091.P6_kept_gone_read_as_release` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 124 | 34 | killed |
| `u191.M13_gone_refused` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 42 | killed |
| `r1115.M2_every_failure_for_good` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 5 | killed |
| `r1115.M4_retryable_is_not_for_good` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 4 | killed |
| `r1115.M5_declined_is_refused` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 8 | killed |
| `r1115.M7_done_counts_done` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 8 | killed |
| `u190.T3_stale_matches_folder` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 1 | killed |
| `u190.T4_name_answers_inline` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 2 | killed |
| `u303.L1_land_key_wrong` | `src/cratekit/cli/label_sync.py` | user | 2 file(s) | 134 | 60 | killed |
| `r432-a.A1_key_casefold` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 89 | 3 | killed |
| `r432-a.A3_lock_never_taken` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 89 | 17 | killed |
| `r432-a.A5_not_retryable` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 89 | 2 | killed |
| `r432-a.A8_holder_left_out` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 89 | 2 | killed |
| `r432-b.A4c_lock_outlives_its_with` | `src/cratekit/intake/landing.py` | user | 3 file(s) | 89 | 8 | killed |
| `r432-b.B5_lock_on_the_library_volume` | `src/cratekit/core/state_files.py` | user | 4 file(s) | 341 | 17 | killed |
| `r432-b.B6_lock_directory_renamed` | `src/cratekit/core/state_files.py` | maintainer | 4 file(s) | 341 | 1 | killed |
| `u77-c.C6_gate_manifest_bytes` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-c.C7_digest_handed_to_engine` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-c.C8_unfiled_rows_warned` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 254 | 2 | killed |
| `u77-a.A6_no_landed_file_guard` | `src/cratekit/intake/landing.py` | user | 6 file(s) | 254 | 5 | killed |
| `u16-round-8-independent.V9_relative_key_by_letter` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 612 | 11 | killed |
| `u265.M8_other_scorer` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2689 | 25 | killed |
| `r667-b.B1_same_recording_no_isrc` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 703 | 1 | killed |
| `r667.F2_isrc_version_not_settled` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 703 | 1 | killed |
| `r667.G13_isrc_not_consulted` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 703 | 16 | killed |
| `r667.G15_isrc_hit_skips_key` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 703 | 3 | killed |
| `r667.E1_title_head_kept` | `src/cratekit/acquire/match_library.py` | user | 3 file(s) | 703 | 33 | killed |
| `r667.G17_reader_drops_isrc` | `src/cratekit/acquire/match_library.py` | user | 3 file(s) | 703 | 17 | killed |
| `u305.M4_index_library_not_reexported` | `src/cratekit/acquire/match.py` | maintainer | 3 file(s) | 708 | 300 | killed |
| `u305.M5_wanted_not_reexported` | `src/cratekit/acquire/match.py` | maintainer | 3 file(s) | 673 | collection error | collect-error |
| `r1295.M16_set_aside_one_word` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 220 | 4 | killed |
| `r1420-b.B2_beyond_tail_unread_pinned` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 1 | killed |
| `r1420.B1_beyond_order_unread` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 8 | killed |
| `r1420.B3_beyond_removals_asked` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 3 | killed |
| `r1420.N1_fix_reverted` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 7 | killed |
| `r1420.N2_moves_begun_ignored` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 4 | killed |
| `r1420.N3_finish_read_too` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 2 | killed |
| `r1420.N5_order_always_read` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 6 | killed |
| `r1420.N6_call_site_never_reads_order` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 8 | killed |
| `r1404.S3_scope_every_pair` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 13 | killed |
| `r1416.M10_cli_account_write_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 12 | killed |
| `r1416.M7_cli_tells_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 4 | killed |
| `r1416.M8_cli_tells_not_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 2 | killed |
| `r1416.M9_cli_scope_key_only` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 119 | killed |
| `r1416.S3_scope_under_the_folder` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 119 | killed |
| `u234.O10_after_not_compared` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O11_after_not_replaced` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O12_kept_reading_of_any_run` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 2 | killed |
| `u234.O13_kept_reading_before_the_stop` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 2 | killed |
| `u234.O1_off_path_dropped_from_the_finish` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 21 | killed |
| `u234.O23_off_path_flag_on_every_finish` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O25_on_path_reading_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 5 | killed |
| `u234.O26_on_path_reading_keeps_the_order_after` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O27_settled_order_keeps_the_order_after` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O3_person_never_leads` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 10 | killed |
| `u234.O4_settled_order_read_as_moved` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 3 | killed |
| `u234.O5_unsettled_reading_read_as_settled` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 10 | killed |
| `u234.O6_reading_never_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 13 | killed |
| `u234.O8_moved_reading_not_kept_afresh` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O9_after_without_the_window` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O21_gate_says_on_path` | `src/cratekit/sync/pair_screen.py` | user | 21 file(s) | 762 | 2 | killed |
| `u234.O22_finishing_note_silent` | `src/cratekit/sync/pair_screen.py` | user | 21 file(s) | 762 | 3 | killed |
| `r1420.C1_continued_ignored` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 762 | 4 | killed |
| `r1420.C3_continued_read_after_the_mark` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 762 | 1 | killed |
| `r1420.C4_carried_record_unread` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 762 | 2 | killed |
| `r1420.E2_finish_agreed_dropped` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 762 | 10 | killed |
| `u234.S1_sample_finish_held_to_the_plans_reading` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 762 | 10 | killed |
| `r1394.P7_unknown_named_as_landed` | `src/cratekit/sync/pair_model.py` | user | 20 file(s) | 750 | 1 | killed |
| `r1394.P8_every_move_named_as_a_stop` | `src/cratekit/sync/pair_model.py` | user | 20 file(s) | 750 | 1 | killed |
| `r1394.P4_finish_from_landed` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 2 | killed |
| `r1394.P5_finish_from_any_path_reading` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 6 | killed |
| `u231.M15_pending_not_read` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 26 | killed |
| `u231.M16_shown_order_not_finished` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 3 | killed |
| `u231.M17_agreement_gap_ignored` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 1 | killed |
| `u231.M18_reading_before_the_moves_kept` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 1 | killed |
| `u231.M20_every_reading_kept` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 1 | killed |
| `u231.M22_root_playlist_named_gig_ready` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 1 | killed |
| `r1394.P1_counts_never_written` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 4 | killed |

## Row definitions

### `u206.M23_lookup_line_dropped`

_with_isrc_lookups: never add the isrc-lookups line

- File: `src/cratekit/cli/__init__.py`
- Source: `u206.json`, row `M23_lookup_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1130 against a baseline of 1130
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`

Old text:

```
    if remembered == 0 and asked == 0:
        return envelope
```

New text:

```
    if True:
        return envelope
```

### `u206.M17_account_hit_ignored`

TidalAccount._isrc_tracks: never use a remembered answer

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u206.json`, row `M17_account_hit_ignored`
- Moved: Anchored where u309-replay-after-e.json replayed it: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1130 against a baseline of 1130
- Kills: 13 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_choice_among_several_releases_is_made_from_a_remembered_answer_with_no_call`
  - `tests/test_isrc_cache.py::test_a_copy_run_redirecting_installation_state_shares_answers_through_the_override`
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_second_account_over_a_fresh_client_asks_nothing_for_an_answered_isrc`
  - `tests/test_isrc_cache.py::test_a_tie_remembered_is_still_refused_with_its_reason`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_the_catalogue_and_the_account_share_one_answer`
  - `tests/test_isrc_cache.py::test_the_process_counts_say_what_the_cache_settled_and_what_was_asked`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`

Old text:

```
        if held is not None:
            return held if held else _ABSENT
        # What the LAST attempt said
```

New text:

```
        if False:
            return held if held else _ABSENT
        # What the LAST attempt said
```

### `r290-author.S07_rebuild_call_removed`

Remove the one jobs.raise_for_state call from cli/rebuild.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/cli/rebuild.py`
- Source: `r290-author.json`, row `S07_rebuild_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 6 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[rebuild]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[rebuild]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[rebuild]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[rebuild]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[rebuild]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r290-author.S05_intake_call_removed`

Remove the one jobs.raise_for_state call from intake/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/intake/cli.py`
- Source: `r290-author.json`, row `S05_intake_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 11 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[intake.set]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.set]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r312.W6_type_not_carried`

_with_left_behind: rebuild as a plain CratekitError, dropping the blocked or cancelled type

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W6_type_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`

Old text:

```
    return rebuilt(
        error,
        replace(
            cause,
```

New text:

```
    return CratekitError(
        replace(
            cause,
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

### `r290-author.R2_backup_rebuild_drops_the_type`

Rebuild the backup rehearsal refusal as a plain CratekitError again, so a rehearsal the worker parked says failed

- File: `src/cratekit/backup/cli.py`
- Source: `r290-author.json`, row `R2_backup_rebuild_drops_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_backup_cli.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`

Old text:

```
    return rebuilt(
        error,
        replace(
```

New text:

```
    return CratekitError(
        replace(
```

### `r290-author.S04_backup_call_removed`

Remove the one jobs.raise_for_state call from backup/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/backup/cli.py`
- Source: `r290-author.json`, row `S04_backup_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_backup_cli.py`
- Collected: 215 against a baseline of 215
- Kills: 11 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r290-author.S06_label_call_removed`

Remove the one jobs.raise_for_state call from label/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/label/cli.py`
- Source: `r290-author.json`, row `S06_label_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_label_workers.py`
- Collected: 208 against a baseline of 208
- Kills: 17 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[sync.labels]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[label.import]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[sync.labels]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[sync.labels]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[label.import]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[sync.labels]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[sync.labels]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_rate_limited_listing_fails_its_item_as_retryable_and_the_job_says_resume`
  - `tests/test_label_workers.py::test_a_resume_of_a_cancelled_sweep_does_not_exit_ok_over_the_items_it_never_ran`
  - `tests/test_label_workers.py::test_a_resumed_job_rearms_the_rate_limited_label_and_not_the_settled_one`
  - ... and 2 more, see the JSON sidecar

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
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

### `r290-author.S08_route_resort_call_removed`

Remove the one jobs.raise_for_state call from write/routing_cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/write/routing_cli.py`
- Source: `r290-author.json`, row `S08_route_resort_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_routing_workers.py`
- Collected: 323 against a baseline of 323
- Kills: 11 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[route.resort]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[route.resort]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[converged]`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`
  - `tests/test_routing_workers.py::test_a_resume_whose_items_did_not_all_succeed_is_not_an_ok_exit[resort]`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r290-author.R1_retag_rebuild_drops_the_type`

Rebuild the retag refusal as a plain CratekitError again, so a retag parked after correcting a file says failed

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r290-author.json`, row `R1_retag_rebuild_drops_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`
- Collected: 228 against a baseline of 228
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`

Old text:

```
    return rebuilt(
        error,
        replace(
```

New text:

```
    return CratekitError(
        replace(
```

### `r290-author.S11_tagging_shell_call_removed`

Remove the one jobs.raise_for_state call from tagging/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `S11_tagging_shell_call_removed`
- Moved: Anchored where u325-replay-after.json replayed it: U298 replaced the resume tails of tagging.shell.advance, adopt.shell.advance, acquire fallback-fetch and master with core.jobs.resumed, which advance calls; its one raise_for_state call is the mapping each of those four shells made, and tests/test_job_outcome.py names that function as the shared tail. The tests are this row's own plus those of the three rows mapped to it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`, `tests/test_adopt_workers.py`, `tests/test_master_cli.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 347 against a baseline of 347
- Kills: 48 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.retag]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[label.judge]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[master]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[tag.folder]`
  - ... and 33 more, see the JSON sidecar

Old text:

```
    raise_for_state(job)
    return job, warnings
```

New text:

```
    get  # the mapping call, removed
    return job, warnings
```

### `r390-a.A2_retry_refuses_any_closed_job_with_a_cause`

the flag is not read: a cancelled job and a retryable failure are refused too

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A2_retry_refuses_any_closed_job_with_a_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_backup_cli.py`, `tests/test_outbound_workers.py`
- Collected: 296 against a baseline of 296
- Kills: 9 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_jobs.py::test_a_cancelled_job_can_be_resumed_and_a_succeeded_one_cannot`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_refused_request_fails_every_item_it_carried_and_the_resume_adds_each_once`
  - `tests/test_outbound_workers.py::test_a_resumed_export_counts_across_both_runs_and_each_item_once`

Old text:

```
    if current.cause is not None and not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
```

New text:

```
    if current.cause is not None:
        raise refuse(
            "job-not-retryable",
```

### `u182.M13_identity_parse`

playlist_identity: key on the raw source instead of the pass's reading

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M13_identity_parse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_sync_land.py`
- Collected: 155 against a baseline of 155
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[url-typed-by-hand-holds-the-swept-id]`
  - `tests/test_jobs.py::test_the_job_verbs_read_a_playlist_as_the_sweep_records_it`
  - `tests/test_sync_land.py::test_a_url_typed_by_hand_and_a_sweeps_id_are_one_playlist_on_the_left_open_row`

Old text:

```
        return catalogue.playlist_id(source)
```

New text:

```
        return source
```

### `u101.G10_ungated_not_reported_in_judged_label`

Drop the ungated branch in a judged label, so a release with no genre is listed silently

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G10_ungated_not_reported_in_judged_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_known_is_listed_with_a_failing_line`
  - `tests/test_label_approved.py::test_tracks_that_disagree_on_the_genre_are_not_judged_and_are_listed`

Old text:

```
            if outcome.ungated is not None:
```

New text:

```
            if False:
```

### `u101.G11_keep_read_as_drop`

Hold on the KEEP verdict instead of DROP

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G11_keep_read_as_drop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_family_exactly_at_the_share_belongs_and_is_listed`
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_genre_the_label_makes_enough_of_is_listed`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`
  - `tests/test_label_approved.py::test_the_default_human_output_names_a_held_release`

Old text:

```
            elif verdict is routing.GateVerdict.DROP and family and outcome.genre:
```

New text:

```
            elif verdict is routing.GateVerdict.KEEP and family and outcome.genre:
```

### `u101.G12_reported_share_not_the_taxonomys`

Report a share the taxonomy did not declare

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G12_reported_share_not_the_taxonomys`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`

Old text:

```
    share = declared.label_gate.out_of_place_share
```

New text:

```
    share = 0.2
```

### `u101.G13_family_count_off_by_one`

Report one more release of the family than there were

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G13_family_count_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`

Old text:

```
families.count(family), classified, share
```

New text:

```
families.count(family) + 1, classified, share
```

### `u101.G14_classified_counts_unjudged`

Count every release in the label as classified, including those with no genre

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G14_classified_counts_unjudged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`

Old text:

```
        classified = sum(1 for genre in genres if genre)
```

New text:

```
        classified = len(genres)
```

### `u101.G17_refusal_silent_on_held`

Drop the held clause from the nothing missing refusal

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G17_refusal_silent_on_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
            + (f" and passed the genre gate ({len(held)} more held by it)" if held else "")
```

New text:

```
            + ""
```

### `u101.G18_no_op_claims_held`

The no op wording ignores held releases and says the library holds everything read

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G18_no_op_claims_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`

Old text:

```
            f"held by it"
            if held
            else
```

New text:

```
            f"held by it"
            if False
            else
```

### `u101.G1_held_is_listed`

Drop the skip, so a release the gate held is resolved, offered and listed anyway

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G1_held_is_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
        if release.item_id in held:
            continue

```

New text:

```
(empty)
```

### `u101.G20_summary_held_empty`

The summary carries no held releases

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G20_summary_held_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`

Old text:

```
        held=[one.to_json() for one in held.values()],
```

New text:

```
        held=[],
```

### `u101.G2_judged_per_release`

Group every release under itself, so each is judged alone and nothing is ever held

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G2_judged_per_release`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_label_with_a_release_unread_this_run_is_not_judged_and_says_why`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_the_default_human_output_names_a_held_release`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return f"release:{release.release_id}"
```

### `u101.G3_all_labels_one_group`

Group every release under one key, so labels are judged against each other

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G3_all_labels_one_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return "all"
```

### `u101.G4_unlabelled_grouped_together`

Group every release naming no label under one key instead of judging each alone

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G4_unlabelled_grouped_together`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return release.label_id or release.label_name or "release:"
```

### `u101.G5_unread_label_judged`

Judge a label even when one of its releases was unread this run

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G5_unread_label_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_label_with_a_release_unread_this_run_is_not_judged_and_says_why`

Old text:

```
        if label in unread:
```

New text:

```
        if label in unread and False:
```

### `u101.G6_unread_from_every_label`

Treat every label as having an unread release whenever any release failed

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G6_unread_from_every_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
        if label in unread:
```

New text:

```
        if unread:
```

### `u101.G7_mixed_is_a_genre`

Rows that disagree yield their first genre instead of none

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G7_mixed_is_a_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_tracks_that_disagree_on_the_genre_are_not_judged_and_are_listed`

Old text:

```
    if len(said) > 1:
```

New text:

```
    if len(said) > 99:
```

### `u101.G8_case_is_a_difference`

Compare genres by exact text, so one genre in two cases reads as mixed

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G8_case_is_a_difference`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_one_genre_in_two_cases_is_one_genre_and_is_judged`

Old text:

```
            said.setdefault(text.casefold(), text)
```

New text:

```
            said.setdefault(text, text)
```

### `u101.G9_mapping_row_unread`

Read the genre by attribute only, so a mapping shaped row reports none

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G9_mapping_row_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`

Old text:

```
        value = row.get("genre") if isinstance(row, Mapping) else getattr(row, "genre", None)
```

New text:

```
        value = getattr(row, "genre", None)
```

### `u308.L6_ended_outcome_ignored`

review_common.ended: every review verb ends OK whatever outcome it reached

- File: `src/cratekit/label/review_common.py`
- Source: `u308.json`, row `L6_ended_outcome_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_artists.py`, `tests/test_label_genre_gate.py`, `tests/test_label_sync_go.py`
- Collected: 366 against a baseline of 366
- Kills: 20 (killed)
- Killed:
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_every_track_owned_is_a_no_op_and_writes_nothing`
  - `tests/test_label_approved.py::test_nothing_accepted_is_a_no_op_that_never_opens_the_catalogue`
  - `tests/test_label_artists.py::test_a_decided_item_reading_an_address_is_left_as_it_is[accepted]`
  - `tests/test_label_artists.py::test_a_decided_item_reading_an_address_is_left_as_it_is[rejected]`
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_a_release_decided_while_it_was_being_read_is_not_rewritten`
  - `tests/test_label_artists.py::test_a_release_the_provider_does_not_serve_is_counted_and_never_blanked`
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[   ]`
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[]`
  - `tests/test_label_artists.py::test_an_artist_put_right_meanwhile_is_not_overwritten`
  - `tests/test_label_artists.py::test_an_empty_queue_is_a_no_op_that_opens_no_catalogue`
  - `tests/test_label_artists.py::test_an_item_whose_artist_is_a_name_is_not_asked_about`
  - `tests/test_label_genre_gate.py::test_a_held_release_returned_to_review_is_filed_and_not_held_again`
  - `tests/test_label_genre_gate.py::test_a_release_filed_before_the_sweep_had_a_gate_is_asked_about_at_approval`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        data={"checks": checks, "summary": summary}, outcome=outcome, warnings=warnings
```

New text:

```
        data={"checks": checks, "summary": summary}, outcome=Outcome.OK, warnings=warnings
```

### `u75-a.A1_kind_filter`

Drop the kind filter, so an accepted harvested label name, which shares the queue, is read as a release

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A1_kind_filter`
- Moved: Anchored where u308-replay-after-a.json replayed it: the list_items keywords of _queued were joined onto one line, so the kind filter is the same keyword dropped from it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_an_accepted_harvested_label_shares_the_queue_and_is_not_a_release`

Old text:

```
        items, queue=str(Queue.LABEL_RELEASE), kinds=(sweep.KIND,), include_resolved=True,
```

New text:

```
        items, queue=str(Queue.LABEL_RELEASE), include_resolved=True,
```

### `u75-a.A3_nothing_accepted_before_the_catalogue`

Remove the early return, so a queue with nothing accepted resolves the catalogue and spends a login

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A3_nothing_accepted_before_the_catalogue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_nothing_accepted_is_a_no_op_that_never_opens_the_catalogue`

Old text:

```
    if not accepted:
        # ASKED BEFORE THE CATALOGUE IS RESOLVED
```

New text:

```
    if False:
        # ASKED BEFORE THE CATALOGUE IS RESOLVED
```

### `u75-a.A5_only_the_seams_exception_is_gone`

Catch LookupError again instead of the seam's own class, the review's first finding

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A5_only_the_seams_exception_is_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_lookup_error_that_is_not_the_seams_own_is_never_read_as_a_gone_release`

Old text:

```
    except catalogue.ReleaseUnresolvable as exc:
        return _Failed(release, GONE, str(exc))
```

New text:

```
    except LookupError as exc:
        return _Failed(release, GONE, str(exc))
```

### `u75-a.A6_no_identifier_is_not_asked_of_the_provider`

Remove the empty identifier guard, so the provider is asked for a release with no name

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A6_no_identifier_is_not_asked_of_the_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_an_accepted_item_naming_no_release_is_a_named_failure`

Old text:

```
    if not release.release_id:
        return _Failed(release, NO_IDENTIFIER, "the review item names no release identifier")

```

New text:

```
(empty)
```

### `u75-a.A7_each_row_read_alone`

Let one unreadable row escape, which costs the run instead of one line

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A7_each_row_read_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_one_unreadable_row_is_reported_and_the_rest_of_the_release_still_lists`

Old text:

```
        except match.UnreadableList as exc:
            unreadable.append(str(exc))
```

New text:

```
        except ZeroDivisionError as exc:
            unreadable.append(str(exc))
```

### `u75-b.B11_write_failure_is_the_verbs_refusal`

Remove the OSError conversion, so a full disk reaches a person as an internal error

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B11_write_failure_is_the_verbs_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_write_the_disk_refuses_is_the_verbs_refusal_and_not_an_internal_error`

Old text:

```
        except OSError as exc:
            # A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL.
```

New text:

```
        except ZeroDivisionError as exc:
            # A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL.
```

### `u75-b.B1_outage_threshold`

Raise the outage threshold from three to thirty, a realistic slip, so a dead provider is asked about every release

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B1_outage_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_provider_that_stopped_answering_is_not_asked_about_every_release`

Old text:

```
OUTAGE_AFTER = 3
```

New text:

```
OUTAGE_AFTER = 30
```

### `u75-b.B3_only_a_provider_failure_counts`

Count a gone release towards an outage

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B3_only_a_provider_failure_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_gone_release_does_not_count_towards_an_outage`

Old text:

```
            in_a_row = in_a_row + 1 if outcome.kind == PROVIDER else 0
```

New text:

```
            in_a_row = in_a_row + 1
```

### `u75-b.B7_same_recording_listed_once`

Remove the match id dedupe, so a single and its album list one recording twice

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B7_same_recording_listed_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_the_same_recording_on_two_releases_is_listed_once_under_the_first`

Old text:

```
            elif settled.match_id in seen:
                counts["duplicate"] += 1

```

New text:

```
(empty)
```

### `u75-b.B9_name_digests_the_provenance`

Digest the tracks alone, the review's fourth finding, so a corrected year meets the emitter's refusal

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B9_name_digests_the_provenance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_the_list_name_moves_with_anything_the_emitter_would_write`
  - `tests/test_label_approved.py::test_the_same_tracks_with_a_corrected_year_take_a_new_name_and_are_not_refused`

Old text:

```
        "provenance": [
            dataclasses.asdict(provenance[track["id"]]) for track in body["tracks"]
        ],
```

New text:

```
        "provenance": [],
```

### `u75-zeros.B6_missing_and_nothing_listable_refuses`

Remove the refusal for missing tracks none of which carries a provider identifier

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-zeros.json`, row `B6_missing_and_nothing_listable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_missing_tracks_none_of_which_can_be_asked_for_is_refused_and_not_a_no_op`

Old text:

```
    if missing and not listed:
```

New text:

```
    if False:
```

### `r840-a.A2_a_name_is_not_asked_about`

_listed: drop the address check, so every open label release is read from the provider and rewritten

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A2_a_name_is_not_asked_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_a_second_run_asks_about_nothing_the_first_repaired`
  - `tests/test_label_artists.py::test_an_item_whose_artist_is_a_name_is_not_asked_about`
  - `tests/test_label_artists.py::test_an_item_with_no_artist_at_all_is_not_an_address_and_is_not_said_to_have_one`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`
  - `tests/test_label_artists.py::test_the_provider_is_asked_once_for_each_repaired_item_and_never_for_the_others`

Old text:

```
        if not is_address(item.payload.get("artist")):
            done.counts[ALREADY_FINE] += 1
            continue
        if item.stored_verdict
```

New text:

```
        if item.stored_verdict
```

### `r840-a.A3_unreadable_verdict_is_decided`

_listed: drop the stored verdict check, so an item carrying a verdict this build cannot read is asked about

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A3_unreadable_verdict_is_decided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_item_carrying_a_verdict_this_build_cannot_read_is_left_and_not_asked_about`

Old text:

```
        if item.stored_verdict is not None:
            done.counts[DECIDED] += 1
            continue

```

New text:

```
(empty)
```

### `r840-a.A4_only_label_releases`

_listed: drop the kind from the selection, so another producer's item in the same queue is read as a release

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A4_only_label_releases`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_another_queues_item_reading_an_address_is_not_this_verbs`

Old text:

```
review.Predicate(queue=str(Queue.LABEL_RELEASE), kind=genre_gate.RELEASE_KIND)
```

New text:

```
review.Predicate(queue=str(Queue.LABEL_RELEASE))
```

### `r840-a.A5_no_identifier_is_not_read`

_walk: drop the empty identifier half of the unaddressed check, so an item filed under an empty identifier is asked for and reported as no longer served

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A5_no_identifier_is_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_item_filed_under_an_empty_identifier_is_not_asked_about`

Old text:

```
        if (
            not subject.release_id
            or genre_gate.release_item_id(subject.release_id) != subject.item_id
        ):
```

New text:

```
        if (
            genre_gate.release_item_id(subject.release_id) != subject.item_id
        ):
```

### `r840-a.A6_another_items_release_is_not_read`

_walk: drop the addressing half of the unaddressed check, so an item naming another item's release is given that release's artist

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A6_another_items_release_is_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_item_naming_another_items_release_is_not_given_that_releases_artist`
  - `tests/test_label_artists.py::test_two_items_naming_one_release_are_two_lines_under_two_keys`

Old text:

```
        if (
            not subject.release_id
            or genre_gate.release_item_id(subject.release_id) != subject.item_id
        ):
```

New text:

```
        if (
            not subject.release_id
        ):
```

### `r840-a.A7_catalogue_opened_on_demand`

_walk: open the catalogue before the walk, so a queue with no address in it logs in and can refuse on the credential

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A7_catalogue_opened_on_demand`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_an_empty_queue_is_a_no_op_that_opens_no_catalogue`

Old text:

```
    found: catalogue.Catalogue | None = None
    failed_in_a_row = 0
```

New text:

```
    found: catalogue.Catalogue | None = catalogue.resolve(cfg)
    failed_in_a_row = 0
```

### `r840-a.A8_outage_bound`

_walk: stop after four reads failing in a row and not three

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A8_outage_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_three_reads_failing_in_a_row_stop_the_run_and_say_what_was_left`

Old text:

```
        if failed_in_a_row >= catalogue.READS_FAILED_IN_A_ROW:
            # THE RUN STOPS
```

New text:

```
        if failed_in_a_row > catalogue.READS_FAILED_IN_A_ROW:
            # THE RUN STOPS
```

### `r840-a.A9_an_answer_resets_the_count`

_walk: never reset the count of failed reads, so three scattered failures stop the run as an outage

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A9_an_answer_resets_the_count`
- Moved: Anchored where u308-replay-after-a.json replayed it: the once used failed local was inlined, so the reset is the same conditional over the call itself
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_that_is_gone_does_not_count_towards_an_outage`
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`

Old text:

```
failed_in_a_row = failed_in_a_row + 1 if _repair_one(store, found, subject, done) else 0
```

New text:

```
failed_in_a_row = failed_in_a_row + (1 if _repair_one(store, found, subject, done) else 0)
```

### `r840-b.B10_unaddressed_is_keyed_by_item`

_Run.record: key a line by its item only when it names no release, so an item naming another item's release shares that release's key

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B10_unaddressed_is_keyed_by_item`
- Moved: Anchored where u308-replay-after-a.json replayed it: the key conditional was folded onto one line; the item key still turns on outcome being unaddressed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_two_items_naming_one_release_are_two_lines_under_two_keys`

Old text:

```
        key = f"item.{subject.item_id}" if outcome == UNADDRESSED else (
```

New text:

```
        key = f"item.{subject.item_id}" if not subject.release_id else (
```

### `r840-b.B11_left_counts_what_was_not_reached`

_with_counts: count left against every address and not against the items the run set out to read

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B11_left_counts_what_was_not_reached`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_catalogue_that_cannot_be_opened_refuses_and_repairs_nothing`
  - `tests/test_label_artists.py::test_a_release_the_provider_could_not_answer_for_is_left_and_the_run_refuses`
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_an_outage_over_the_last_releases_of_a_run_is_the_same_refusal`
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`
  - `tests/test_label_artists.py::test_three_reads_failing_in_a_row_stop_the_run_and_say_what_was_left`

Old text:

```
    left = listed - len(done.releases)
```

New text:

```
    left = done.addresses - done.counts[REPAIRED]
```

### `r840-b.B1_only_the_seams_exception_is_not_served`

_repair_one: catch LookupError where the seam's own exception is caught, so a client that could not parse a payload is reported as a release that is gone

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B1_only_the_seams_exception_is_not_served`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_lookup_error_that_is_not_the_seams_own_is_unread_and_never_not_served`

Old text:

```
    except catalogue.ReleaseUnresolvable as exc:
```

New text:

```
    except LookupError as exc:
```

### `r840-b.B2_a_refusal_stops_the_run`

_repair_one: drop the CratekitError passthrough, so an expired session is recorded as one unread release and the walk goes on asking

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B2_a_refusal_stops_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`

Old text:

```
        name = found.release_artist(subject.release_id)
    except CratekitError:
        raise
    except catalogue
```

New text:

```
        name = found.release_artist(subject.release_id)
    except catalogue
```

### `r840-b.B3_no_name_never_blanks`

_repair_one: write whatever the provider answered unless it is None, so a release it names no artist for has its address replaced by nothing

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B3_no_name_never_blanks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[   ]`
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[]`

Old text:

```
    name = _text(name)
    if not name:
```

New text:

```
    name = _text(name)
    if name is None:
```

### `r840-b.B4_an_unread_release_refuses`

_walk: refuse only when the outage bound was reached, so a run that left one or two releases unread exits clean

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B4_an_unread_release_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_lookup_error_that_is_not_the_seams_own_is_unread_and_never_not_served`
  - `tests/test_label_artists.py::test_a_release_the_provider_could_not_answer_for_is_left_and_the_run_refuses`

Old text:

```
    if done.counts[UNREAD]:
        # AFTER THE WALK
```

New text:

```
    if done.counts[UNREAD] >= catalogue.READS_FAILED_IN_A_ROW:
        # AFTER THE WALK
```

### `r840-b.B5_decided_meanwhile_is_not_fine`

_write: answer already fine whenever nothing was written, so an item decided during the read is said to have stopped reading an address

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B5_decided_meanwhile_is_not_fine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_decided_while_it_was_being_read_is_not_rewritten`
  - `tests/test_label_artists.py::test_a_release_that_left_review_while_it_was_being_read_is_not_filed_again`

Old text:

```
    return ALREADY_FINE if seen else DECIDED
```

New text:

```
    return ALREADY_FINE
```

### `r840-b.B6_put_right_meanwhile_is_kept`

_write: drop the address check on the payload as it stands, so an artist somebody typed during the read is overwritten by the provider's

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B6_put_right_meanwhile_is_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_artist_put_right_meanwhile_is_not_overwritten`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`

Old text:

```
        if not is_address(current.get("artist")):
            return None
        return {**current, "artist": name}
```

New text:

```
        return {**current, "artist": name}
```

### `r840-b.B7_addresses_are_what_still_read_one`

_Run.addresses: count every outcome, so an item that stopped reading an address, and every item that never did, is counted as one

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B7_addresses_are_what_still_read_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_an_artist_put_right_meanwhile_is_not_overwritten`
  - `tests/test_label_artists.py::test_an_item_whose_artist_is_a_name_is_not_asked_about`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`
  - `tests/test_label_artists.py::test_the_provider_is_asked_once_for_each_repaired_item_and_never_for_the_others`

Old text:

```
        return sum(n for outcome, n in self.counts.items() if outcome != ALREADY_FINE)
```

New text:

```
        return sum(self.counts.values())
```

### `r840-b.B8_only_the_artist_is_rewritten`

_write: write a payload holding the artist alone, so every other field of the item is lost

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B8_only_the_artist_is_rewritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_an_open_item_reading_an_address_is_given_the_name_and_nothing_else_moves`
  - `tests/test_label_artists.py::test_what_a_judging_job_stamped_meanwhile_is_kept`

Old text:

```
        return {**current, "artist": name}
```

New text:

```
        return {"artist": name}
```

### `r840-b.B9_a_refusal_carries_why_each_read_failed`

_Run.record: leave the sentence off the release's row, so a refusal, which carries no check line, says a read failed and not why

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B9_a_refusal_carries_why_each_read_failed`
- Moved: Anchored where u308-replay-after-a.json replayed it: the release row literal was written on one line; dropping the said key leaves the sentence off the row as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_the_provider_could_not_answer_for_is_left_and_the_run_refuses`
  - `tests/test_label_artists.py::test_an_open_item_reading_an_address_is_given_the_name_and_nothing_else_moves`

Old text:

```
            {**asdict(subject), "outcome": outcome, "artist": artist, "said": said}
```

New text:

```
            {**asdict(subject), "outcome": outcome, "artist": artist}
```

### `r840-c.C1_the_function_is_handed_the_payload_as_it_stands`

review.redescribe: hand the function an empty payload and not the stored one, so a caller changing one field writes that field alone

- File: `src/cratekit/core/review.py`
- Source: `r840-c.json`, row `C1_the_function_is_handed_the_payload_as_it_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`, `tests/test_label_judge.py`
- Collected: 137 against a baseline of 137
- Kills: 34 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_person_reads_each_release_without_asking_for_json`
  - `tests/test_label_artists.py::test_a_rewrite_given_a_function_is_handed_the_payload_and_writes_what_it_returns`
  - `tests/test_label_artists.py::test_a_second_run_asks_about_nothing_the_first_repaired`
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_an_imported_item_is_read_by_the_identifier_its_payload_carries`
  - `tests/test_label_artists.py::test_an_open_item_reading_an_address_is_given_the_name_and_nothing_else_moves`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`
  - `tests/test_label_artists.py::test_the_provider_is_asked_once_for_each_repaired_item_and_never_for_the_others`
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`
  - `tests/test_label_artists.py::test_two_items_naming_one_release_are_two_lines_under_two_keys`
  - `tests/test_label_artists.py::test_what_a_judging_job_stamped_meanwhile_is_kept`
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_fresh_answer_with_no_word_takes_the_old_words_off_the_item`
  - `tests/test_label_judge.py::test_a_label_marked_any_has_nothing_held_and_nobody_is_asked`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            wanted = payload(_payload_of(held["payload"]))
```

New text:

```
            wanted = payload({})
```

### `r840-c.C2_the_function_is_only_handed_an_open_item`

review.redescribe: read the payload of any item, so the function is called for one that is decided or carries a verdict this build cannot read

- File: `src/cratekit/core/review.py`
- Source: `r840-c.json`, row `C2_the_function_is_only_handed_an_open_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`, `tests/test_label_judge.py`
- Collected: 137 against a baseline of 137
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_decided_while_it_was_being_read_is_not_rewritten`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_a_decided_item[accepted]`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_a_decided_item[rejected]`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_an_item_with_an_unreadable_verdict`

Old text:

```
                "SELECT payload FROM review_items WHERE item_id = ? AND verdict IS NULL",
                (item_id,),
            ).fetchone()
            if held is None:
                return None
            wanted = payload(
```

New text:

```
                "SELECT payload FROM review_items WHERE item_id = ?",
                (item_id,),
            ).fetchone()
            if held is None:
                return None
            wanted = payload(
```

### `r798-a.K1_the_first_rule_that_matches_wins`

published_kind: read the published rules last first, so a word two rules could claim is given the later one's kind

- File: `src/cratekit/core/routing.py`
- Source: `r798-a.json`, row `K1_the_first_rule_that_matches_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_taxonomy.py`, `tests/test_routing_parity.py`
- Collected: 1150 against a baseline of 1150
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_published_word_is_matched_to_its_kind[first-rule-wins]`
  - `tests/test_label_genre_gate.py::test_a_published_word_is_matched_to_its_kind[long-rnb-is-not-the-blues-it-contains]`
  - `tests/test_label_genre_gate.py::test_every_measured_word_of_the_general_catalogue_is_a_kind`

Old text:

```
    for rule in taxonomy.label_gate.published:
```

New text:

```
    for rule in reversed(taxonomy.label_gate.published):
```

### `r798-d.K11_the_shared_matcher_reads_a_substring_needle`

_rule_matches: drop the any_of arm of the matcher the second review made one function of, so no rule of either table that names a substring claims a word

- File: `src/cratekit/core/routing.py`
- Source: `r798-d.json`, row `K11_the_shared_matcher_reads_a_substring_needle`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_taxonomy.py`, `tests/test_routing_parity.py`
- Collected: 1150 against a baseline of 1150
- Kills: 101 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[African Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Alternative]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Asian Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Blues]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Brazilian Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Christian]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Classical]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Country]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Cumbia]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Dance]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Electro]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Films/Games]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Folk]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Indian Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Jazz]`
  - ... and 86 more, see the JSON sidecar

Old text:

```
        or (rule.any_of and any(needle in value for needle in rule.any_of))
    )


def gate_decisions(
```

New text:

```
    )


def gate_decisions(
```

### `r798-a.K6_the_default_kind_is_one_a_rule_names`

_build_gate: accept a default kind no published rule names, so every label left at the default is never judged

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `r798-a.json`, row `K6_the_default_kind_is_one_a_rule_names`
- Moved: Anchored where u299-replay-after-2.json replayed it: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_taxonomy.py`, `tests/test_routing_parity.py`
- Collected: 1150 against a baseline of 1150
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_malformed_label_gate_is_refused_by_what_it_lacks[default-kind-no-rule-names]`

Old text:

```
    if published and default_kind != ANY_KIND and default_kind not in kinds:
```

New text:

```
    if False:
```

### `r798-a.K8_a_kind_is_one_word`

_build_published: accept a rule naming a kind in a shape the registry refuses, so the taxonomy declares a kind no label can be given

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `r798-a.json`, row `K8_a_kind_is_one_word`
- Moved: Anchored where u299-replay-after-3.json replayed it: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_taxonomy.py`, `tests/test_routing_parity.py`
- Collected: 1150 against a baseline of 1150
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_malformed_label_gate_is_refused_by_what_it_lacks[rule-kind-of-two-words]`

Old text:

```
        if not KIND_NAME.fullmatch(kind):
```

New text:

```
        if False:
```

### `u308.L5_extended_step_dropped`

review_common.extended: the step the review verbs add to a refusal is dropped

- File: `src/cratekit/label/review_common.py`
- Source: `u308.json`, row `L5_extended_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_artists.py`, `tests/test_label_sync_go.py`
- Collected: 247 against a baseline of 247
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`
  - `tests/test_label_artists.py::test_three_reads_failing_in_a_row_stop_the_run_and_say_what_was_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-held-release]`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-passed-release]`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park`

Old text:

```
    steps = (*cause.remediation.steps, step)
```

New text:

```
    steps = tuple(cause.remediation.steps)
```

### `r835-b.M1_only_the_batch_years_marked`

mark_cli._item: a year the landed batch did not file is marked anyway

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-b.json`, row `M1_only_the_batch_years_marked`
- Moved: Anchored where u308-replay-after-a.json replayed it: The same guard on the batch's years; its skip item is now built by the local skip helper, so the line after the if returns skip(...) rather than a dict literal.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_year_the_batch_did_not_file_is_left_alone`

Old text:

```
    if year.year not in filed:
        return skip(NOT_IN_BATCH,
```

New text:

```
    if False:
        return skip(NOT_IN_BATCH,
```

### `r835-b.M5_deleted_folder_said`

mark_cli.label_mark: a label folder deleted on the account is listed as if it were there, and the read fails every run

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-b.json`, row `M5_deleted_folder_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`

Old text:

```
            if shape.folder_id in remote.folders()
```

New text:

```
            if True
```

### `r835-c.M4_recheck_before_rename_again`

mark_cli.label_mark: a title changed between the plan and the write is renamed anyway

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-c.json`, row `M4_recheck_before_rename_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_title_changed_between_the_plan_and_the_write_is_not_renamed`

Old text:

```
            if now.get(identity) != item["built_as"]:
```

New text:

```
            if False:
```

### `r835-a.F4_recorded_and_refused_not_asked_again`

folders.plan: a track recorded as added or refused is asked for again, so one a person took off is put back and one refused is asked every run

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-a.json`, row `F4_recorded_and_refused_not_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_label_playlists.py::test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years`
  - `tests/test_label_playlists.py::test_a_second_run_over_an_unchanged_catalogue_plans_nothing`
  - `tests/test_label_playlists.py::test_a_track_taken_off_by_a_person_is_not_put_back`
  - `tests/test_label_playlists.py::test_a_track_the_provider_will_not_add_is_recorded_and_not_asked_again`

Old text:

```
            skip = held | asked
```

New text:

```
            skip = held
```

### `r1091.P6_kept_gone_read_as_release`

_read_one: answer a kept gone release as a release with no tracks, so it is counted undated rather than gone

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P6_kept_gone_read_as_release`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 34 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_batch_of_another_label_marks_nothing_and_reads_no_account`
  - `tests/test_label_playlists.py::test_a_folder_made_by_hand_at_the_root_is_adopted`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`
  - `tests/test_label_playlists.py::test_a_ledger_written_by_another_verb_keeps_the_label_shape`
  - `tests/test_label_playlists.py::test_a_mark_the_record_cannot_take_names_what_it_took_before`
  - `tests/test_label_playlists.py::test_a_mark_with_no_landed_file_refuses_before_anything`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_recorded_year_deleted_on_the_account_is_left_alone_not_refused`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_label_playlists.py::test_a_rejected_session_reading_a_recorded_year_is_raised_not_passed_over`
  - `tests/test_label_playlists.py::test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years`
  - `tests/test_label_playlists.py::test_a_second_mark_says_each_year_is_already_marked`
  - `tests/test_label_playlists.py::test_a_second_run_over_an_unchanged_catalogue_plans_nothing`
  - ... and 19 more, see the JSON sidecar

Old text:

```
        return None if held.gone else (held.tracks, held.year)
```

New text:

```
        return (held.tracks, held.year)
```

### `u191.M13_gone_refused`

_grouped: refuse the plan over a release the provider no longer has, instead of counting it

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M13_gone_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`, `tests/test_label_playlists.py`
- Collected: 80 against a baseline of 80
- Kills: 42 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_batch_of_another_label_marks_nothing_and_reads_no_account`
  - `tests/test_label_playlists.py::test_a_folder_made_by_hand_at_the_root_is_adopted`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`
  - `tests/test_label_playlists.py::test_a_ledger_written_by_another_verb_keeps_the_label_shape`
  - `tests/test_label_playlists.py::test_a_mark_the_record_cannot_take_names_what_it_took_before`
  - `tests/test_label_playlists.py::test_a_mark_with_no_landed_file_refuses_before_anything`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_recorded_year_deleted_on_the_account_is_left_alone_not_refused`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_label_playlists.py::test_a_rejected_session_reading_a_recorded_year_is_raised_not_passed_over`
  - `tests/test_label_playlists.py::test_a_renamed_label_is_a_different_plan_and_its_approval_is_stale`
  - `tests/test_label_playlists.py::test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years`
  - `tests/test_label_playlists.py::test_a_second_mark_says_each_year_is_already_marked`
  - ... and 27 more, see the JSON sidecar

Old text:

```
            gone += 1
            continue
```

New text:

```
            raise incomplete(entry, "gone")
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

### `u303.L1_land_key_wrong`

label_sync: the go's landing is read under the wrong key, so no tail is found

- File: `src/cratekit/cli/label_sync.py`
- Source: `u303.json`, row `L1_land_key_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land_beside.py`
- Collected: 134 against a baseline of 134
- Kills: 60 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_download_queued_by_hand_is_not_resumed_or_held_by_a_go`
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_fresh_go_with_nothing_new_names_an_unlanded_download_rather_than_end_quietly`
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - ... and 45 more, see the JSON sidecar

Old text:

```
    land = report.get(go.LAND_KEY) if isinstance(report, Mapping) else None
```

New text:

```
    land = report.get("landing") if isinstance(report, Mapping) else None
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

### `r432-b.B5_lock_on_the_library_volume`

config: declare the landing locks library scoped, which puts them on the volume that is commonly exFAT

- File: `src/cratekit/core/state_files.py`
- Source: `r432-b.json`, row `B5_lock_on_the_library_volume`
- Moved: Anchored where u299-replay-after-1.json replayed it: the same entry's root: an installation entry is an _installation call now, so the mutation respells it as a never restored _library entry (U299)
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`, `tests/test_config.py`
- Collected: 341 against a baseline of 341
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
    _installation(
        "landing_locks", "landing_locks",

```

New text:

```
    _library(
        "landing_locks", "landing_locks", SnapshotRole.NEVER_RESTORED,

```

### `r432-b.B6_lock_directory_renamed`

config: move the landing locks to another directory name under the state root

- File: `src/cratekit/core/state_files.py`
- Source: `r432-b.json`, row `B6_lock_directory_renamed`
- Moved: Anchored where u299-replay-after-1.json replayed it: the same entry's relative path, now the second argument of its _installation call in state_files (U299)
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`, `tests/test_config.py`
- Collected: 341 against a baseline of 341
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_the_batch_lock_is_on_the_state_disk_and_a_released_one_leaves_its_file`

Old text:

```
        "landing_locks", "landing_locks",

```

New text:

```
        "landing_locks", "landings",

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

### `u16-round-8-independent.V9_relative_key_by_letter`

Relative major or minor detected by matching letter instead of matching wheel number, so 8A vs 8B reads as outright disagreement and 8A vs 9A as relative

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V9_relative_key_by_letter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 612 against a baseline of 612
- Kills: 11 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_relative_key_disagreement_surfaces_rather_than_picking_one`
  - `tests/test_match_states.py::test_a_version_answer_never_settles_a_key_question_about_the_same_line`
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[another_version_spelling]`
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[artist_tag_credits_nobody]`
  - `tests/test_match_states.py::test_an_isrc_hit_still_asks_about_the_key`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[differs-then-relative]`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[relative-then-differs]`
  - `tests/test_match_states.py::test_one_answered_key_question_never_settles_another_one`
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-first]`
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-last]`

Old text:

```
    return Why.KEY_RELATIVE if left[0] == right[0] else Why.KEY_DIFFERS

```

New text:

```
    return Why.KEY_RELATIVE if left[1] == right[1] else Why.KEY_DIFFERS

```

### `u265.M8_other_scorer`

_approximate: score the sorted forms with WRatio instead of ratio, so scores and the floor's cut move

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M8_other_scorer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2689 against a baseline of 2689
- Kills: 25 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_track_deleted_on_purpose_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it`
  - `tests/test_intake_missing_search.py::test_an_accepted_candidate_the_library_now_holds_is_not_listed_again`
  - `tests/test_match_states.py::test_a_resemblance_below_the_floor_is_missing_rather_than_a_question`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_spelled_number_is_not_read_as_a_numeral[Four Tune-Fortune]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
        scorer=fuzz.ratio,
```

New text:

```
        scorer=fuzz.WRatio,
```

### `r667-b.B1_same_recording_no_isrc`

_same_recording: the ISRC clause removed, r667's G11 after its direct test

- File: `src/cratekit/acquire/match.py`
- Source: `r667-b.json`, row `B1_same_recording_no_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 703 against a baseline of 703
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[artist_tag_credits_nobody]`

Old text:

```
    return fold(wanted.artist) in held.members or _carries(held, token)
```

New text:

```
    return fold(wanted.artist) in held.members
```

### `r667.F2_isrc_version_not_settled`

_candidates_for: an ISRC hit at another version spelling is a version question on the candidate beside a key question on the match

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F2_isrc_version_not_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 703 against a baseline of 703
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[another_version_spelling]`

Old text:

```
        elif version_key != wanted.version_key and not _carries(first, token):
```

New text:

```
        elif version_key != wanted.version_key:
```

### `r667.G13_isrc_not_consulted`

resolve_one: never ask the index by ISRC, the engine before this unit

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G13_isrc_not_consulted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 703 against a baseline of 703
- Kills: 16 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says`
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_a_rows_isrc_is_folded_before_it_is_asked`
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[another_version_spelling]`
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[artist_tag_credits_nobody]`
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_title_disagrees_is_a_question_not_a_match`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_an_isrc_settled_row_lists_the_files_carrying_the_isrc_and_no_other`
  - `tests/test_match_states.py::test_an_isrc_under_another_artist_and_another_emoji_title_is_asked`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    carrying = index.held_by_isrc(isrc_token(wanted.isrc))
```

New text:

```
    carrying = ()
```

### `r667.G15_isrc_hit_skips_key`

resolve_one: an ISRC hit is matched before the key check runs

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G15_isrc_hit_skips_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 703 against a baseline of 703
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[another_version_spelling]`
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[artist_tag_credits_nobody]`
  - `tests/test_match_states.py::test_an_isrc_hit_still_asks_about_the_key`

Old text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}
        if disagreements == {None}:
```

New text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}
        if disagreements == {None} or settled:
```

### `r667.E1_title_head_kept`

Existing: _read_from_disk takes the title tag verbatim, the R-664 defect

- File: `src/cratekit/acquire/match_library.py`
- Source: `r667.json`, row `E1_title_head_kept`
- Moved: Anchored where u305-replay-after.json replayed it: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 703 against a baseline of 703
- Kills: 33 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac-tags1-row1]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[07A - 128 - Traumer, antraum, Anton - Hyaku.flac-tags2-row2]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[08A - 124 - Aurora Bloom - Sun Path.flac-tags0-row0]`
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says`
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_head_found_only_in_the_tag_carries_the_key_when_the_stem_has_none`
  - `tests/test_match_states.py::test_a_head_inside_the_title_tag_is_stripped_so_a_plain_provider_row_matches`
  - `tests/test_match_states.py::test_a_head_written_as_a_suffix_inside_the_tag_comes_off_as_it_does_from_the_stem`
  - `tests/test_match_states.py::test_a_headed_tag_titled_wholly_in_brackets_matches_the_provider_row`
  - `tests/test_match_states.py::test_a_headed_tag_with_a_lossy_marker_strips_under_the_librarys_template`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    tagged_title = naming.strip_heads(spelled_tag, template=template)
```

New text:

```
    tagged_title = spelled_tag
```

### `r667.G17_reader_drops_isrc`

_read_from_disk: the ISRC tag is read and not carried, so the index has nothing to be asked by

- File: `src/cratekit/acquire/match_library.py`
- Source: `r667.json`, row `G17_reader_drops_isrc`
- Moved: Anchored where u305-replay-after.json replayed it: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 703 against a baseline of 703
- Kills: 17 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says`
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_a_rows_isrc_is_folded_before_it_is_asked`
  - `tests/test_match_states.py::test_a_single_artist_file_is_indexed_once_and_the_rule_moves_nothing`
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[another_version_spelling]`
  - `tests/test_match_states.py::test_an_isrc_hit_asks_about_the_key_alone[artist_tag_credits_nobody]`
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_title_disagrees_is_a_question_not_a_match`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_an_isrc_settled_row_lists_the_files_carrying_the_isrc_and_no_other`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        isrc=isrc_token(read["isrc"]),
```

New text:

```
        isrc="",
```

### `u305.M4_index_library_not_reexported`

match: stop re-exporting index_library, so every caller of match.index_library and the intake suite's patch of it lose their target

- File: `src/cratekit/acquire/match.py`
- Source: `u305.json`, row `M4_index_library_not_reexported`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_library_reads_remembered.py`, `tests/intake/test_workers.py`
- Collected: 708 against a baseline of 708
- Kills: 300 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/intake/test_workers.py::test_a_hearts_job_freezes_when_each_heart_was_made_and_a_playlist_job_does_not`
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_resolution_with_nothing_missing_names_no_next_command`
  - `tests/intake/test_workers.py::test_a_second_identify_over_the_same_recording_makes_zero_transport_calls`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_tracklist_that_cannot_be_written_refuses_and_says_the_answers_were_kept`
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/intake/test_workers.py::test_an_offered_track_is_a_review_item_asked_once_however_often_it_is_redone`
  - `tests/intake/test_workers.py::test_answers_that_could_not_be_kept_are_said_on_both_verbs`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_identify_reports_the_coverage_rule_and_a_gap_is_paid_for_again_and_nothing_else_is`
  - `tests/intake/test_workers.py::test_identify_then_set_pays_for_recognition_once_and_the_job_says_it_cost_nothing`
  - ... and 285 more, see the JSON sidecar

Old text:

```
    index_library,

```

New text:

```
(empty)
```

### `u305.M5_wanted_not_reexported`

match: stop re-exporting Wanted, so the readers and every package building one through match lose it

- File: `src/cratekit/acquire/match.py`
- Source: `u305.json`, row `M5_wanted_not_reexported`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_listdoc.py`, `tests/test_isrc_screen.py`
- Collected: 673 against a baseline of 705
- Kills: 673 (collect-error)
- Note: collection changed: 673 collected against a baseline of 705. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_listdoc.py::test_a_declared_version_beside_an_embedded_one_round_trips_whole[Sun Path (Extended)]`
  - `tests/test_listdoc.py::test_a_declared_version_beside_an_embedded_one_round_trips_whole[Sun Path (feat. Mira) (Extended)]`
  - `tests/test_listdoc.py::test_a_duplicate_id_is_written_once_and_the_first_occurrence_wins`
  - `tests/test_listdoc.py::test_a_frozen_mapping_carries_no_version_so_none_is_written`
  - `tests/test_listdoc.py::test_a_hand_built_track_with_no_spelling_writes_its_title_and_version`
  - `tests/test_listdoc.py::test_a_listed_id_with_no_provenance_refuses_and_writes_nothing`
  - `tests/test_listdoc.py::test_a_manifest_row_reads_as_the_wanted_track_its_list_row_reads_as`
  - `tests/test_listdoc.py::test_a_manifest_that_is_not_there_is_refused_by_name`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[[]-not a manifest]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[\xff\xfe-not JSON]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"list": 1, "origin": "tidal", "tracks": []}-not a manifest]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 1, "rows": []}-no rows object]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 1, "rows": {"1": []}}-not an object]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 1, "rows": {"1": {"source": " "}}}-names no source]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 1, "rows": {"1": {"source": "label", "label_name": 7}}}-label_name]`
  - ... and 658 more, see the JSON sidecar
- Collection errors: `tests/test_isrc_screen.py`

Old text:

```
    Wanted,

```

New text:

```
(empty)
```

### `r1295.M16_set_aside_one_word`

set_aside: always names the title as the absent half, so an artistless track is misnamed

- File: `src/cratekit/intake/cli.py`
- Source: `r1295.json`, row `M16_set_aside_one_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/intake/test_workers.py`, `tests/test_sync_all.py`
- Collected: 220 against a baseline of 220
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
why=f"the account lists it with no {_absent(title)}"
```

New text:

```
why="the account lists it with no title"
```

### `r1420-b.B2_beyond_tail_unread_pinned`

sample: the part written check reads the kept tracks' order but not that this write's additions stand after them, measured again once a test pins it

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420-b.json`, row `B2_beyond_tail_unread_pinned`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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

### `r1420.N1_fix_reverted`

the check leaves the order unread once ordering is marked, as before R-1420, so a person's reorder after an order that moved nothing is written over

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N1_fix_reverted`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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

### `r1404.S3_scope_every_pair`

sample, U231: every pair keeps the account's order, so a root pair's account is written rekordbox's order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1404.json`, row `S3_scope_every_pair`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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

### `r1416.M10_cli_account_write_kept`

pair_cli: the account write reads the order as always kept, so a root pair's first sync writes rekordbox's order onto the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M10_cli_account_write_kept`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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

### `u234.O10_after_not_compared`

the order after a settled one leads whatever the reading now, so an order that moved again leads unsettled

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O10_after_not_compared`
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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

### `u234.O11_after_not_replaced`

an order after a settled one that moves again is not kept afresh, so the order it moved to is held for good

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O11_after_not_replaced`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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

### `u234.O23_off_path_flag_on_every_finish`

finishing_off_path is set on every finish, so the gate says off the path for one on it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O23_off_path_flag_on_every_finish`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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

### `u234.O9_after_without_the_window`

the order after a settled one leads on its next reading however soon

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O9_after_without_the_window`
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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

### `u234.O21_gate_says_on_path`

the gate line says on the path for an account read off it

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u234.json`, row `O21_gate_says_on_path`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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

### `r1420.C1_continued_ignored`

a continue of an order parked or stopped with the whole write before any move passes the adapter no listing to agree with

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `C1_continued_ignored`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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

### `u234.S1_sample_finish_held_to_the_plans_reading`

sample, R-1411: the finish is not held to the plan's reading, so the rest of an off path order is moved from whatever the adapter reads

- File: `src/cratekit/sync/pair_write.py`
- Source: `u234.json`, row `S1_sample_finish_held_to_the_plans_reading`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
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

### `r1394.P7_unknown_named_as_landed`

held message: a reading at a move whose landing is not known is named as before the moves accepted

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1394.json`, row `P7_unknown_named_as_landed`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
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

### `r1394.P4_finish_from_landed`

pending order: an agreed reading at the moves the provider accepted is finished from even with a move whose landing is not known after it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1394.json`, row `P4_finish_from_landed`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
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

### `u231.M15_pending_not_read`

plan: a pending order is planned as U225 would, with no agreement asked

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M15_pending_not_read`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
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

### `u231.M17_agreement_gap_ignored`

plan: a reading equal to the one kept agrees however soon after it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M17_agreement_gap_ignored`
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
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

### `u231.M18_reading_before_the_moves_kept`

plan: a reading kept before the moves began counts toward agreement

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M18_reading_before_the_moves_kept`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
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

### `r1394.P1_counts_never_written`

pair write: the recorder writes the moving step with no progress, sent and landed always 0

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P1_counts_never_written`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
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

