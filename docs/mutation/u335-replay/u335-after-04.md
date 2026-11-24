# Mutation table: u335-after-04

Measured by `scripts/mutate.py` on 2026-11-24 06:16 UTC, branch `HEAD` at `1a401a39`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23223 collected. pytest invocations for this batch: 291.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 06:16 UTC for commit `1a401a39247d`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 72, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23223 against 23223. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r44-a.S5_not_destructive` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 5 | killed |
| `r44-a.S6_oserror_escapes` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 2 | killed |
| `r44-a.S7_probe_the_target` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 3 | killed |
| `r44-a.S8_wording_held_to` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 1 | killed |
| `r44-a.S9_offer_to_record_nested` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 1 | killed |
| `u300.S17_mapped_reasons_local` | `src/cratekit/core/session_volumes.py` | maintainer | 1 file(s) | 148 | 1 | killed |
| `u329.P8_session_volumes_wrong_family` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 19 | killed |
| `r1665-b.S14_sources_unchecked_again` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S10_walk_before_empty` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S15_recorded_before_the_copy_lands` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 72 | killed |
| `r1665.S1_guard_removed` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 8 | killed |
| `r1665.S2_guard_ignored` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 8 | killed |
| `r1665.S3_removal_unseen` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 4 | killed |
| `r1665.S4_rewrite_unseen` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 3 | killed |
| `r1665.S5_size_not_identity` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S6_mtime_not_identity` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S7_directories_unwalked` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S8_walk_after_fails_open` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.S9_walk_before_fails_open` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1677-b.C11_database_only` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 1 | killed |
| `r1677.C10_unreadable_passes` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 1 | killed |
| `r1677.C13_no_temporary_directory_passes` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 1 | killed |
| `r1677.C1_no_measure` | `src/cratekit/core/snapshot.py` | user | 6 file(s) | 282 | 8 | killed |
| `r1677.C3_store_not_passed` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 98 | 2 | killed |
| `r1677.C4_sum_dropped` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 98 | 1 | killed |
| `r1677.C7_no_ancestor_walk` | `src/cratekit/core/snapshot.py` | user | 3 file(s) | 73 | 46 | killed |
| `r1677.C8_no_headroom` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 4 | killed |
| `r1677.C9_boundary` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 50 | 2 | killed |
| `r1677.K1_room_path_unrecorded` | `src/cratekit/core/snapshot.py` | user | 5 file(s) | 257 | 2 | killed |
| `r1677.K2_room_path_silent` | `src/cratekit/core/snapshot.py` | user | 5 file(s) | 257 | 3 | killed |
| `r1677.K3_other_copy_failure_verified` | `src/cratekit/core/snapshot.py` | user | 5 file(s) | 257 | 1 | killed |
| `r1677.N1_every_failure_is_room` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 56 | 4 | killed |
| `r1677.N2_quota_dropped` | `src/cratekit/core/snapshot.py` | user | 2 file(s) | 56 | 2 | killed |
| `r1677.V1_verify_swallows` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 98 | 3 | killed |
| `r1677.V2_verify_does_not_ask` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 98 | 2 | killed |
| `u272.E1_verified_ignores_verdict` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 642 | 11 | killed |
| `u272.E2_gate_trusts_manifest` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 642 | 9 | killed |
| `u953.M17_nearest_existing_asks_the_path_itself` | `src/cratekit/core/snapshot.py` | user | 3 file(s) | 209 | 118 | killed |
| `u293.S1_reentrant` | `src/cratekit/core/staging_lock.py` | user | 4 file(s) | 237 | 6 | killed |
| `u293.S2_second_holder_refused` | `src/cratekit/core/staging_lock.py` | user | 4 file(s) | 237 | 5 | killed |
| `r432-b.B5_lock_on_the_library_volume` | `src/cratekit/core/state_files.py` | user | 4 file(s) | 342 | 17 | killed |
| `r432-b.B6_lock_directory_renamed` | `src/cratekit/core/state_files.py` | maintainer | 4 file(s) | 342 | 1 | killed |
| `u299.U7_library_extras_passed` | `src/cratekit/core/state_files.py` | user | 4 file(s) | 463 | 34 | killed |
| `r722.T8_lenient_energy_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2994 | 1 | killed |
| `r722.T9_lenient_open_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2994 | 306 | killed |
| `u249.M15_noting_reader_drops_field_failure` | `src/cratekit/core/tags.py` | user | 3 file(s) | 694 | 1 | killed |
| `u249.M16_noting_reader_drops_open_failure` | `src/cratekit/core/tags.py` | user | 3 file(s) | 694 | 2 | killed |
| `u249.M17_noting_reader_drops_unrecognised` | `src/cratekit/core/tags.py` | user | 3 file(s) | 694 | 3 | killed |
| `u249.M18_noting_reader_drops_unsupported` | `src/cratekit/core/tags.py` | maintainer | 3 file(s) | 694 | 1 | killed |
| `u249.M19_noting_reader_inverted` | `src/cratekit/core/tags.py` | user | 3 file(s) | 694 | 6 | killed |
| `u301.T1_refuse_unknown_admits_a_field` | `src/cratekit/core/tags.py` | user | 3 file(s) | 169 | 1 | killed |
| `u247.M1_memo_removed` | `src/cratekit/core/taxonomy.py` | user | 4 file(s) | 293 | 10 | killed |
| `u247.M6_key_is_the_size` | `src/cratekit/core/taxonomy.py` | user | 4 file(s) | 293 | 9 | killed |
| `r799-a.L4_a_word_declared_twice_is_refused` | `src/cratekit/core/taxonomy_build.py` | user | 3 file(s) | 511 | 4 | killed |
| `r799-a.L5_a_table_nothing_reads_is_refused` | `src/cratekit/core/taxonomy_build.py` | user | 3 file(s) | 511 | 4 | killed |
| `r799-a.L6_a_word_is_matched_whatever_its_case` | `src/cratekit/core/taxonomy_build.py` | user | 3 file(s) | 511 | 48 | killed |
| `u118-b.A1_tag_beats_route` | `src/cratekit/core/taxonomy_build.py` | user | 3 file(s) | 1070 | 4 | killed |
| `u155.T12_sources_type` | `src/cratekit/core/taxonomy_build.py` | user | 60 file(s) | 6759 | 2 | killed |
| `r799-a.L1_a_too_coarse_tag_is_refused` | `src/cratekit/core/taxonomy_model.py` | user | 3 file(s) | 511 | 3 | killed |
| `r799-a.L2_a_bare_bucket_name_is_refused` | `src/cratekit/core/taxonomy_model.py` | user | 3 file(s) | 511 | 11 | killed |
| `u132.P4_version_raise` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 18 | killed |
| `u132.P7_child_tables` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 30 | killed |
| `u132.P8_present_skip` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 21 | killed |
| `u133-a.P9_keyword_note_gone` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 3 | killed |
| `u244.M24_upgrade_keeps_a_held_table` | `src/cratekit/core/taxonomy_upgrade.py` | user | 2 file(s) | 468 | 22 | killed |
| `r1184.M10_off_taxonomy_exact` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `r1184.M11_edit_own_name_flag` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 4 | killed |
| `r1184.M12_bare_asks_word_first` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `r1184.M13_bare_step_names_word` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `r1184.M14_step_command_words` | `src/cratekit/core/taxonomy_word.py` | user | 3 file(s) | 289 | 5 | killed |
| `r1184.M15_own_names_none` | `src/cratekit/core/taxonomy_word.py` | user | 3 file(s) | 289 | 3 | killed |
| `r1184.M16_own_names_empty` | `src/cratekit/core/taxonomy_word.py` | user | 3 file(s) | 289 | 1 | killed |
| `r1184.M1_own_folder_exact_first` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 2 | killed |
| `r1184.M2_own_folder_casefold` | `src/cratekit/core/taxonomy_word.py` | user | 3 file(s) | 289 | 15 | killed |
| `r1184.M3_files_by_name` | `src/cratekit/core/taxonomy_word.py` | user | 3 file(s) | 289 | 8 | killed |
| `r1184.M4_filed_now_keyword` | `src/cratekit/core/taxonomy_word.py` | user | 3 file(s) | 289 | 1 | killed |
| `r1184.M5_answer_branch` | `src/cratekit/core/taxonomy_word.py` | user | 3 file(s) | 289 | 4 | killed |
| `r1184.M6_alias_other_folder` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 3 | killed |
| `r1184.M7_alias_own_bare` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 2 | killed |
| `r1184.M8_alias_own_block` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 4 | killed |
| `r1184.M9_off_taxonomy_own_block` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 4 | killed |
| `u194.W10_folder_rates` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u194.W12_string_escape` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u194.W13_inline_joiner` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u194.W1_off_taxonomy_any_word` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 14 | killed |
| `u194.W2_decline_not_too_coarse` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 7 | killed |
| `u194.W3_fallback_not_too_coarse` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 5 | killed |
| `u194.W5_saved_alias_rerun` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 4 | killed |
| `u194.W7_genre_casefold_unique` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u194.W8_folder_already_declared` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 4 | killed |
| `u194.W9_folder_like_default` | `src/cratekit/core/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `r431-a.A1_a_plain_row_gains_a_companion` | `src/cratekit/core/tombstone.py` | user | 6 file(s) | 1278 | 21 | killed |
| `r431-a.A2_one_kind_for_both` | `src/cratekit/core/tombstone.py` | user | 6 file(s) | 1278 | 17 | killed |
| `r1255.T1_tree_registry_clause` | `src/cratekit/core/tree_registry.py` | user | 3 file(s) | 119 | 2 | killed |
| `u953.M2_registry_cause_remedy_fixed` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 115 | 2 | killed |
| `r1844.N7_held_rows_read_absent` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 456 | 35 | killed |
| `r1037.M9_recorded_not_excluded` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 456 | 2 | killed |
| `r431-a.A15_the_verb_lifts_through_the_store` | `src/cratekit/deletion/run.py` | user | 2 file(s) | 366 | 6 | killed |
| `r431-a.A10_the_shared_companion_goes_with_the_first_lift` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1113 | 4 | killed |
| `r431-a.A11_a_lifted_tombstone_still_accounts` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1113 | 3 | killed |
| `r431-a.A12_the_named_tombstone_accounts_for_itself` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1113 | 6 | killed |
| `r431-a.A13_accounting_by_stripping_alone` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1113 | 1 | killed |
| `r431-a.A14_accounting_by_pointer_alone` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1113 | 1 | killed |
| `r431-a.A3_stripped_from_the_title_column` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1113 | 2 | killed |
| `r431-a.A4_the_tombstone_names_no_companion` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1113 | 2 | killed |
| `r431-a.A5_the_companion_names_no_tombstone` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1113 | 7 | killed |
| `r1037.M19_version_two_refused` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 456 | 114 | killed |
| `u129-author.A12_archive_backfill_swallows_all` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `u140.B10_queued_day_name_dropped` | `src/cratekit/export/set_common.py` | user | 1 file(s) | 29 | 2 | killed |
| `r1017.M12_twin_message_names_to` | `src/cratekit/export/set_rename.py` | user | 4 file(s) | 174 | 1 | killed |
| `r1017.M1_no_recorded_names` | `src/cratekit/export/set_rename.py` | user | 4 file(s) | 174 | 5 | killed |
| `r1017.M2_recorded_before_frozen` | `src/cratekit/export/set_rename.py` | user | 4 file(s) | 174 | 1 | killed |
| `u140.B6_mark_refusal_dropped` | `src/cratekit/export/set_rename.py` | user | 2 file(s) | 85 | 2 | killed |
| `u140.B7_twin_refusal_dropped` | `src/cratekit/export/set_rename.py` | user | 1 file(s) | 29 | 4 | killed |
| `u140.B8_flag_conflict_dropped` | `src/cratekit/export/set_rename.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B9_abort_applies` | `src/cratekit/export/set_rename.py` | user | 1 file(s) | 29 | 1 | killed |
| `u113-a.A2_queue_order` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 23223 | 0 (promoted) | zero |
| `u113-a.A3_no_pass_splits_nothing` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 23223 | 0 (promoted) | zero |
| `u113-a.A8_pending_any_state` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 26 | 1 | killed |
| `u128-b.A6b_abandoned_counts` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 55 | 1 | killed |
| `u128-b.A8b_ambiguous_is_an_answer` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 55 | 1 | killed |
| `u128-b.A9b_emptied_left_lost` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 55 | 1 | killed |
| `u128.A10_no_warning` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 55 | 5 | killed |
| `u128.A1_owned_not_mirrored` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 55 | 9 | killed |
| `u128.A2_rerun_unseen` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 55 | 2 | killed |
| `u128.A4_untied_carried_silent` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 55 | 2 | killed |
| `u128.A7_any_pass_counts` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 55 | 2 | killed |
| `r1255.B1_batch_name_clause` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 68 | 2 | killed |
| `u113-a.A4_batch_name_not_taken` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 26 | 2 | killed |
| `u113-a.A5_landing_names_its_own` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 26 | 1 | killed |
| `u175.N1_date_first` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 69 | 41 | killed |
| `u175.N2_no_date` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 69 | 41 | killed |
| `u175.N3_date_form` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 69 | 41 | killed |
| `u175.N4_clock_not_seam` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 69 | 41 | killed |
| `u175.N7_held_not_held` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 69 | 8 | killed |
| `u175.N8_counter_before_date` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 69 | 9 | killed |
| `u175.N9_landing_not_held` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 56 | 1 | killed |
| `u179.N1_one_label_only_when_all_named` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 54 | 3 | killed |
| `r1499.B01_pass_suffix` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.B02_pass_handler` | `src/cratekit/intake/beside.py` | maintainer | 6 file(s) | 325 | 2 | killed |
| `r1499.B03_pass_step` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 6 | killed |
| `r1499.B04_pass_maybe_renamed` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.B05_arrived_items` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 4 | killed |
| `r1499.B06_arrived_count` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.B08_kept_identity` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 5 | killed |
| `r1499.B09_unlistable` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.B10_plain_step_moves_out` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 2 | killed |
| `r1264.M22_readable_dates` | `src/cratekit/intake/cli.py` | user | 4 file(s) | 190 | 6 | killed |
| `r1295.M16_set_aside_one_word` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 221 | 4 | killed |
| `u113-a.A7_payload_drops_name` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 42 | 32 | killed |
| `u129-author.A3_abort_still_writes` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `u213.M11_unreadable_said_isrc` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 3 | killed |
| `u213.M13_unidentified_any` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 3 | killed |
| `u213.M6_readable_refuses_nameless` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 2 | killed |
| `u213.M9_readable_order_holds_unread` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 3 | killed |
| `u249.M21_intake_reset_leaves_reader` | `src/cratekit/intake/cli.py` | maintainer | 3 file(s) | 128 | 1 | killed |
| `r740-b.E2_average_bpm_nonzero` | `src/cratekit/intake/collection_xml.py` | user | 5 file(s) | 113 | 16 | killed |
| `r770-d.S1_composite_the_splice_takes_a_stub` | `src/cratekit/intake/collection_xml.py` | user | 4 file(s) | 85 | 2 | killed |
| `u37-author-light.G1_stub_listing` | `src/cratekit/intake/collection_xml.py` | user | 2 file(s) | 12 | 1 | killed |
| `u37-author-light.G3_gridless_bpm` | `src/cratekit/intake/collection_xml.py` | user | 2 file(s) | 51 | 1 | killed |
| `r770-b.B5_file_verb_never_takes_the_native_path` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 16 | killed |
| `r770-b.B6_export_taken_on_a_native_tree` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-b.B7_staging_not_asked_first` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-b.B8_target_spelled_as_resolved` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-c.C1_unplaceable_file_reaches_the_gate` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-c.C2_untyped_suffix_reaches_the_gate` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-c.C5_playlist_named_for_the_whole_file_name` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 3 | killed |
| `r770-d.C6_digest_without_the_collection_plan` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1950.C02_file_landed_compares_second_entry` | `src/cratekit/intake/filing.py` | user | 2 file(s) | 16 | 1 | killed |
| `u165.F5_report_failed` | `src/cratekit/intake/filing.py` | user | 1 file(s) | 23223 | 0 (promoted) | zero |
| `r773-b.P1_proof_granted_whatever_the_export_names` | `src/cratekit/intake/imported_cli.py` | user | 2 file(s) | 128 | 6 | killed |
| `r501-b.I4_mark_awaiting` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 134 | 23 | killed |
| `r685-b.P1_place_files_rereads_the_registry` | `src/cratekit/intake/ingest.py` | maintainer | 1 file(s) | 23 | 1 | killed |
| `r740-b.I1_tag_key_first` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 89 | 3 | killed |
| `r740-b.I3_stem_is_the_title` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 89 | 2 | killed |
| `r740-b.I4_lossy_is_the_parameter` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 89 | 1 | killed |
| `r740-b.I5_body_marker_marks` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 89 | 1 | killed |
| `r740-c.I2_no_stem_fallback` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 89 | 1 | killed |
| `r770-a.A1_switch_reads_the_other_mode` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 77 | 57 | killed |
| `r770-a.A2_unreachable_root_is_read_anyway` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 60 | 3 | killed |
| `r770-a.A3_assertion_refuses_nothing` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-a.A4_refusal_asks_for_a_defect_report` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-a.A5_tree_built_without_the_refusal` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-a.A6_splice_asks_only_after_the_export` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 1 | killed |
| `u113-b.B2_batch_keeps_claimed` | `src/cratekit/intake/ingest.py` | user | 3 file(s) | 73 | 9 | killed |
| `u113-b.B3_record_unnamed` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 26 | 3 | killed |
| `u113-b.B4_steps_name_one` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 53 | 1 | killed |
| `u128-b.B4_bridge_owned_dropped` | `src/cratekit/intake/ingest.py` | user | 8 file(s) | 204 | 1 | killed |
| `u128-b.B5_bridge_record_no_account` | `src/cratekit/intake/ingest.py` | user | 8 file(s) | 204 | 2 | killed |
| `u37-author-light.G4_staging` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 8 | 1 | killed |
| `r1056.F1_no_fold` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F2_empty_year_counts` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F3_any_label_counts` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 4 | killed |
| `r1056.F4_non_list_read_as_empty` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F5_non_dict_entry_skipped` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F6_text_year_accepted` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 2 | killed |
| `r1056.F7_bool_tracks_accepted` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F8_no_zero_pad` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1467.M19_root_unreadable_refuses` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 276 | 1 | killed |
| `r1467.M20_retired_file_proves` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 276 | 1 | killed |
| `r1467.M21_native_record_proves` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 276 | 1 | killed |
| `r1467.M22_proof_is_a_file` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 276 | 1 | killed |
| `r677-b.V4_after_the_stale_test` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 1 | killed |
| `r677.V1_no_preflight_before_the_gate` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 7 | killed |
| `r677.V2_preflight_on_a_plan_of_nothing` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 1 | killed |
| `r677.V3_refusal_never_replaces_the_gate` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 5 | killed |
| `r677.V5_preflight_raises_directly` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 2 | killed |
| `r677.V6_manifest_rows_not_handed_over` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 1 | killed |
| `u110-b.B2_name_names_file` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 18 | killed |
| `u110-b.B7_name_overrides` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 27 | killed |
| `u113-b.B7_digest_blind_to_split` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 53 | 2 | killed |
| `u113-b.B8_pending_names_unheld` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u121-b.S20r_bridge_set` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `u127.L6_bridge_ignores_calibration` | `src/cratekit/intake/land_cli.py` | user | 11 file(s) | 454 | 1 | killed |
| `u128-b.B3_owned_unresolved_at_gate` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 26 | 4 | killed |

## Zero rows and what they owe

- `u113-a.A2_queue_order` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u113-a.A3_no_pass_splits_nothing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u165.F5_report_failed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r44-a.S5_not_destructive`

Assert a rule target at read strength, where an unreadable or unrecorded identity is tolerated

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S5_not_destructive`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 5 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`
  - `tests/test_write_session.py::test_a_provider_that_cannot_read_the_identity_to_hand_over_is_a_refusal_too`
  - `tests/test_write_session.py::test_a_rule_target_whose_identity_cannot_be_read_refuses`
  - `tests/test_write_session.py::test_a_target_outside_the_root_with_nothing_recorded_refuses_and_hands_over_the_identity`
  - `tests/test_write_session.py::test_the_seams_handed_in_are_the_seams_used`

Old text:

```
                expected_rule_identity(cfg, rule),
                destructive=True,
```

New text:

```
                expected_rule_identity(cfg, rule),
                destructive=False,
```

### `r44-a.S6_oserror_escapes`

Let an OSError from the walk or the identity read escape the gate instead of becoming a refusal

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S6_oserror_escapes`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_provider_that_cannot_read_the_identity_to_hand_over_is_a_refusal_too`
  - `tests/test_write_session.py::test_a_way_to_the_target_this_account_cannot_walk_is_a_refusal_and_not_a_traceback`

Old text:

```
    except OSError as exc:
        # Could not look is its own refusal, not an internal defect.
```

New text:

```
    except KeyboardInterrupt as exc:
        # Could not look is its own refusal, not an internal defect.
```

### `r44-a.S7_probe_the_target`

Probe the rule's target for a file instead of the file's own directory, so a volume nested under the target is never seen

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S7_probe_the_target`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 3 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_deletion.py::test_a_file_in_a_volume_nested_under_the_rules_target_is_not_moved`
  - `tests/test_write_session.py::test_the_file_is_proved_where_the_file_is_and_not_where_the_rule_points`

Old text:

```
        rules[index],
        Path(path).parent,
```

New text:

```
        rules[index],
        Path(rules[index].target or "/"),
```

### `r44-a.S8_wording_held_to`

Say the volume was recorded on the rule when the identity compared was the library's

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S8_wording_held_to`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`

Old text:

```
    return "the library's volume, which a target inside the library root is held to"
```

New text:

```
    return "the volume recorded on that rule"
```

### `r44-a.S9_offer_to_record_nested`

Offer to record the foreign volume's identity on a rule that recorded none

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S9_offer_to_record_nested`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`

Old text:

```
        if rule.volume_id and observed:
```

New text:

```
        if observed:
```

### `u300.S17_mapped_reasons_local`

the mapped volume gate reads the part's own reason table, so a patched table is not read

- File: `src/cratekit/core/session_volumes.py`
- Source: `u300.json`, row `S17_mapped_reasons_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`
- Collected: 148 against a baseline of 148
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_verdict_in_neither_table_fails_rather_than_wearing_the_mismatch_slug`

Old text:

```
            reason = _session()._MAPPED_REASONS[status.state]
```

New text:

```
            reason = _MAPPED_REASONS[status.state]
```

### `u329.P8_session_volumes_wrong_family`

session_volumes binds _session to the writer's accessor, so every _session().name reads the wrong module

- File: `src/cratekit/core/session_volumes.py`
- Source: `u329.json`, row `P8_session_volumes_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 19 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_different_disk_at_a_mapped_target_stops_the_apply_before_any_file_moves`
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_retires_nothing_nobody_answered_for`
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_stops_a_confirmed_move`
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_deletion.py::test_a_file_in_a_volume_nested_under_the_rules_target_is_not_moved`
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`
  - `tests/test_deletion.py::test_a_volume_holding_only_removed_rows_does_not_settle_off_an_empty_mount_point`
  - `tests/test_write_session.py::test_a_different_disk_at_a_rules_target_refuses_and_names_the_rule`
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`
  - `tests/test_write_session.py::test_a_provider_that_cannot_read_the_identity_to_hand_over_is_a_refusal_too`
  - `tests/test_write_session.py::test_a_recorded_volume_mounted_somewhere_else_says_where`
  - `tests/test_write_session.py::test_a_recorded_volume_that_is_not_mounted_anywhere_has_its_own_slug`
  - `tests/test_write_session.py::test_a_rule_target_whose_identity_cannot_be_read_refuses`
  - `tests/test_write_session.py::test_a_target_outside_the_root_with_nothing_recorded_refuses_and_hands_over_the_identity`
  - `tests/test_write_session.py::test_a_verdict_in_neither_table_fails_rather_than_wearing_the_mismatch_slug`
  - ... and 4 more, see the JSON sidecar

Old text:

```
from cratekit.core.session_call_time import session as _session
```

New text:

```
from cratekit.core.rb_call_time import writer as _session
```

### `r1665-b.S14_sources_unchecked_again`

assert_sources_present: never refuse, measured again after the zero in r1665.md was given its test, so a restore accepts a capture missing files

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665-b.json`, row `S14_sources_unchecked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_lost_its_log_after_the_verdict_is_refused_by_the_plan[-wal]`

Old text:

```
    if not absent:
        return
    raise refuse(
```

New text:

```
    if True:
        return
    raise refuse(
```

### `r1665.S10_walk_before_empty`

capture: a walk before the check that fails answers an empty capture

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S10_walk_before_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_cannot_be_walked_around_its_check_is_not_recorded_verified[before]`

Old text:

```
        copied = None

```

New text:

```
        copied = {}

```

### `r1665.S15_recorded_before_the_copy_lands`

capture: record a companion as captured whether or not it landed

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S15_recorded_before_the_copy_lands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 72 (killed)
- Killed:
  - `tests/test_restore.py::test_a_capture_whose_manifest_names_a_path_outside_the_set_is_refused`
  - `tests/test_restore.py::test_a_coupled_file_the_capture_records_as_absent_is_removed_again`
  - `tests/test_restore.py::test_a_dry_run_and_a_real_run_walk_the_same_list_in_the_same_order`
  - `tests/test_restore.py::test_a_held_session_used_after_its_block_is_refused`
  - `tests/test_restore.py::test_a_later_session_that_committed_nothing_does_not_need_an_override`
  - `tests/test_restore.py::test_a_plan_built_before_a_later_commit_is_refused_at_run`
  - `tests/test_restore.py::test_a_pre_cutover_restore_leaves_the_next_session_refused`
  - `tests/test_restore.py::test_a_rehearsal_never_clears_the_live_companion_files`
  - `tests/test_restore.py::test_a_rehearsal_reports_what_is_outstanding_rather_than_what_it_recorded`
  - `tests/test_restore.py::test_a_restore_lists_every_effect_it_cannot_undo_and_blocks_convergence`
  - `tests/test_restore.py::test_a_restore_predating_a_cutover_marks_that_tree_unconverged`
  - `tests/test_restore.py::test_a_restore_refuses_while_rekordbox_holds_the_database`
  - `tests/test_restore.py::test_a_restore_replaces_exactly_the_derived_coupled_set`
  - `tests/test_restore.py::test_a_restore_returns_a_modified_database_to_its_pre_session_bytes`
  - `tests/test_restore.py::test_a_restore_returns_the_coupled_state_with_the_database`
  - ... and 57 more, see the JSON sidecar

Old text:

```
                source=path, captured=landed if landed.exists() else None, directory=False
```

New text:

```
                source=path, captured=landed, directory=False
```

### `r1665.S1_guard_removed`

capture: never ask whether the check changed the capture

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S1_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 8 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_cannot_be_walked_around_its_check_is_not_recorded_verified[after]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_changes_the_captured_database_is_not_recorded_verified[resizes-at-its-own-time]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_changes_the_captured_database_is_not_recorded_verified[rewrites-at-its-own-size]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_changes_the_captured_database_is_not_recorded_verified[rewrites]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_companion_is_not_recorded_verified[-shm]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_companion_is_not_recorded_verified[-wal]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_coupled_file_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_an_empty_captured_directory_is_not_recorded_verified`

Old text:

```
    if verdict and copied is not None:
        changed
```

New text:

```
    if False:
        changed
```

### `r1665.S2_guard_ignored`

capture: log what the check changed and keep the verdict

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S2_guard_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 8 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_cannot_be_walked_around_its_check_is_not_recorded_verified[after]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_changes_the_captured_database_is_not_recorded_verified[resizes-at-its-own-time]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_changes_the_captured_database_is_not_recorded_verified[rewrites-at-its-own-size]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_changes_the_captured_database_is_not_recorded_verified[rewrites]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_companion_is_not_recorded_verified[-shm]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_companion_is_not_recorded_verified[-wal]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_coupled_file_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_an_empty_captured_directory_is_not_recorded_verified`

Old text:

```
                "; ".join(changed[:20]),
            )
            verdict = False
```

New text:

```
                "; ".join(changed[:20]),
            )
            verdict = verdict
```

### `r1665.S3_removal_unseen`

_changed_by_the_check: a removed entry is not a change

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S3_removal_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 4 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_companion_is_not_recorded_verified[-shm]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_companion_is_not_recorded_verified[-wal]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_a_captured_coupled_file_is_not_recorded_verified`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_an_empty_captured_directory_is_not_recorded_verified`

Old text:

```
            changed.append(f"{path} was removed")
```

New text:

```
            pass
```

### `r1665.S4_rewrite_unseen`

_changed_by_the_check: a rewritten entry is not a change

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S4_rewrite_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 3 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_changes_the_captured_database_is_not_recorded_verified[resizes-at-its-own-time]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_changes_the_captured_database_is_not_recorded_verified[rewrites-at-its-own-size]`
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_changes_the_captured_database_is_not_recorded_verified[rewrites]`

Old text:

```
        elif after[path] != identity:
```

New text:

```
        elif False:
```

### `r1665.S5_size_not_identity`

_walked: identify a file by its modification time alone

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S5_size_not_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_changes_the_captured_database_is_not_recorded_verified[resizes-at-its-own-time]`

Old text:

```
(status.st_size, status.st_mtime_ns)
```

New text:

```
(0, status.st_mtime_ns)
```

### `r1665.S6_mtime_not_identity`

_walked: identify a file by its size alone

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S6_mtime_not_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_changes_the_captured_database_is_not_recorded_verified[rewrites-at-its-own-size]`

Old text:

```
(status.st_size, status.st_mtime_ns)
```

New text:

```
(status.st_size, 0)
```

### `r1665.S7_directories_unwalked`

_walked: record no directory

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S7_directories_unwalked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_that_removes_an_empty_captured_directory_is_not_recorded_verified`

Old text:

```
            found[here / name] = None

```

New text:

```
            pass

```

### `r1665.S8_walk_after_fails_open`

_changed_by_the_check: a walk after the check that fails answers no change

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S8_walk_after_fails_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_cannot_be_walked_around_its_check_is_not_recorded_verified[after]`

Old text:

```
        return [f"the capture could not be walked again: {exc}"]
```

New text:

```
        return []
```

### `r1665.S9_walk_before_fails_open`

capture: verify although the walk before the check failed

- File: `src/cratekit/core/snapshot.py`
- Source: `r1665.json`, row `S9_walk_before_fails_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_cannot_be_walked_around_its_check_is_not_recorded_verified[before]`

Old text:

```
        if record.database is not None and copied is not None

```

New text:

```
        if record.database is not None

```

### `r1677-b.C11_database_only`

assert_room_for_check: measure the database alone, leaving out its companions and the playlist file the copy takes

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677-b.json`, row `C11_database_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_the_measure_counts_every_file_the_check_copies_not_the_database_alone`

Old text:

```
    needed = sum(_allocated_size(member) for member in rb_writer.file_set(database))
```

New text:

```
    needed = _allocated_size(Path(database))
```

### `r1677.C10_unreadable_passes`

assert_room_for_check: a volume that will not report its room passes rather than refusing

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C10_unreadable_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_that_will_not_report_its_room_refuses`

Old text:

```
    if available is None:
        raise refuse(
            "snapshot-check-temp-full",
            f"the free space on the volume holding the temporary directory {scratch} "
```

New text:

```
    if available is None:
        return needed
        raise refuse(
            "snapshot-check-temp-full",
            f"the free space on the volume holding the temporary directory {scratch} "
```

### `r1677.C13_no_temporary_directory_passes`

assert_room_for_check: no temporary directory at all passes the measure, so the capture is taken and left unverified

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C13_no_temporary_directory_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_no_temporary_directory_at_all_refuses_before_anything_is_written`

Old text:

```
        scratch = rb_writer.disposable_root()
    except OSError as exc:
        raise refuse(
```

New text:

```
        scratch = rb_writer.disposable_root()
    except OSError as exc:
        return 0
        raise refuse(
```

### `r1677.C1_no_measure`

capture: never measure the throwaway's room, so a full temporary volume reads as a failed check again (the card's defect)

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C1_no_measure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_restore.py`, `tests/test_intake_land_rehearse.py`
- Collected: 282 against a baseline of 282
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_shared_with_the_store_must_hold_both`
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_that_will_not_report_its_room_refuses`
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_too_small_for_the_check_refuses_before_anything_is_written`
  - `tests/test_snapshot_check_room_r1677.py::test_no_temporary_directory_at_all_refuses_before_anything_is_written`
  - `tests/test_snapshot_check_room_r1677.py::test_one_byte_short_on_the_temporary_volume_refuses`
  - `tests/test_snapshot_check_room_r1677.py::test_the_measure_counts_every_file_the_check_copies_not_the_database_alone`
  - `tests/test_snapshot_check_room_r1677.py::test_the_room_refusal_is_a_precondition_not_a_defect`

Old text:

```
    if verifier is None:
        assert_room_for_check(database_paths(cfg)[0], store=(destination_root, estimate))
```

New text:

```
    if False:
        assert_room_for_check(database_paths(cfg)[0], store=(destination_root, estimate))
```

### `r1677.C3_store_not_passed`

capture: measure the throwaway without the store, so a shared volume is asked for the throwaway alone

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C3_store_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_intake_land_rehearse.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_shared_with_the_store_must_hold_both`

Old text:

```
        assert_room_for_check(database_paths(cfg)[0], store=(destination_root, estimate))
```

New text:

```
        assert_room_for_check(database_paths(cfg)[0], store=None)
```

### `r1677.C4_sum_dropped`

assert_room_for_check: never add the capture's estimate on a shared volume

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C4_sum_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_intake_land_rehearse.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_shared_with_the_store_must_hold_both`

Old text:

```
    total = needed + (store[1] if store is not None and shared else 0)
```

New text:

```
    total = needed
```

### `r1677.C7_no_ancestor_walk`

_device: stat the path itself, so a store not yet made has no device and counts as shared

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C7_no_ancestor_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`, `tests/test_snapshot_wal_r1665.py`
- Collected: 73 against a baseline of 73
- Kills: 46 (killed)
- Killed:
  - `tests/test_snapshot.py::test_a_capture_is_a_snapshot_directory_as_far_as_pruning_is_concerned`
  - `tests/test_snapshot.py::test_a_capture_that_verifies_is_the_only_one_anything_may_commit_behind`
  - `tests/test_snapshot.py::test_a_manifest_from_a_later_build_is_refused_rather_than_guessed_at`
  - `tests/test_snapshot.py::test_a_missing_database_refuses_in_the_library_class_rather_than_crashing`
  - `tests/test_snapshot.py::test_a_verifier_that_raises_counts_as_not_having_verified`
  - `tests/test_snapshot.py::test_a_world_readable_source_does_not_produce_a_world_readable_capture`
  - `tests/test_snapshot.py::test_an_absent_source_is_recorded_as_absent_rather_than_failing`
  - `tests/test_snapshot.py::test_an_unreadable_manifest_refuses_rather_than_reporting_an_empty_capture`
  - `tests/test_snapshot.py::test_every_declared_source_appears_in_the_capture_record`
  - `tests/test_snapshot.py::test_every_file_and_directory_in_a_capture_is_private_under_any_umask`
  - `tests/test_snapshot.py::test_the_capture_store_is_never_captured_by_a_capture`
  - `tests/test_snapshot.py::test_the_database_and_the_coupled_directory_land_under_one_stamp`
  - `tests/test_snapshot.py::test_the_files_the_engine_keeps_beside_the_database_travel_with_it`
  - `tests/test_snapshot.py::test_the_verdict_survives_a_round_trip_through_the_manifest`
  - `tests/test_snapshot.py::test_writing_a_second_capture_into_an_existing_stamp_refuses`
  - ... and 31 more, see the JSON sidecar

Old text:

```
    while not probe.exists() and probe.parent != probe:
```

New text:

```
    while False:
```

### `r1677.C8_no_headroom`

assert_room_for_check: require the bare estimate, without the capture's headroom

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C8_no_headroom`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`
- Collected: 50 against a baseline of 50
- Kills: 4 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_shared_with_the_store_must_hold_both`
  - `tests/test_snapshot_check_room_r1677.py::test_a_temporary_volume_too_small_for_the_check_refuses_before_anything_is_written`
  - `tests/test_snapshot_check_room_r1677.py::test_one_byte_short_on_the_temporary_volume_refuses`
  - `tests/test_snapshot_check_room_r1677.py::test_the_measure_counts_every_file_the_check_copies_not_the_database_alone`

Old text:

```
    available = free_bytes if free_bytes is not None else _free_bytes(scratch)
    required = int(total * headroom)
```

New text:

```
    available = free_bytes if free_bytes is not None else _free_bytes(scratch)
    required = int(total)
```

### `r1677.C9_boundary`

assert_room_for_check: refuse exactly enough room, the boundary moved by one

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C9_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_shared_volume_with_room_for_both_captures_verified`
  - `tests/test_snapshot_check_room_r1677.py::test_exactly_enough_room_on_the_temporary_volume_captures_verified`

Old text:

```
    if available >= required:
        return needed
    sharing = (
```

New text:

```
    if available > required:
        return needed
    sharing = (
```

### `r1677.K1_room_path_unrecorded`

capture: refuse for no room without first rewriting the manifest unverified

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `K1_room_path_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[no-space]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[quota]`

Old text:

```
            _record_unverified(record, manifest)
            raise no_room from failed
```

New text:

```
            raise no_room from failed
```

### `r1677.K2_room_path_silent`

capture: a copy with no room is a plain unverified capture, not refused under the room slug

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `K2_room_path_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[no-space]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[quota]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_stand_in_verifier_raising_the_copy_failure_is_refused_under_the_room_slug`

Old text:

```
            _record_unverified(record, manifest)
            raise no_room from failed
```

New text:

```
            verdict = False
```

### `r1677.K3_other_copy_failure_verified`

capture: a copy that failed for another reason is recorded VERIFIED, the merge blocker the card names

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `K3_other_copy_failure_verified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_fails_for_another_reason_is_unverified_not_a_room_message`

Old text:

```
        logger.warning("the capture integrity check could not run, so it did not pass: %s", failed)
        verdict = False
```

New text:

```
        logger.warning("the capture integrity check could not run, so it did not pass: %s", failed)
        verdict = True
```

### `r1677.N1_every_failure_is_room`

check_had_no_room: read every copy failure as no room, so a permission error is told as a full volume

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `N1_every_failure_is_room`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_intake_land_rehearse.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[its copy otherwise]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_fails_for_another_reason_is_unverified_not_a_room_message`
  - `tests/test_snapshot_check_room_r1677.py::test_only_a_full_volume_or_quota_is_read_as_no_room[13-False]`
  - `tests/test_snapshot_check_room_r1677.py::test_only_a_full_volume_or_quota_is_read_as_no_room[5-False]`

Old text:

```
    if code not in _NO_ROOM_ERRNOS:
        return None
```

New text:

```
    if False:
        return None
```

### `r1677.N2_quota_dropped`

_NO_ROOM_ERRNOS: leave out a reached quota, so it is a plain unverified capture

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `N2_quota_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_intake_land_rehearse.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[quota]`
  - `tests/test_snapshot_check_room_r1677.py::test_only_a_full_volume_or_quota_is_read_as_no_room[122-True]`

Old text:

```
    code for code in (errno.ENOSPC, getattr(errno, "EDQUOT", None)) if code is not None
```

New text:

```
    code for code in (errno.ENOSPC,) if code is not None
```

### `r1677.V1_verify_swallows`

_verify: let the copy failure fall into the catch all, so it is a plain unverified capture again

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `V1_verify_swallows`
- Moved: Text anchored again by U300, which replayed it as written here and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[no-space]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[quota]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_stand_in_verifier_raising_the_copy_failure_is_refused_under_the_room_slug`

Old text:

```
    except rb_writer.IntegrityCheckCopyFailed:
        # No verdict at all, which the capture names (R-1677).
        raise
```

New text:

```
    except rb_writer.IntegrityCheckCopyFailed:
        return False
```

### `r1677.V2_verify_does_not_ask`

_verify: call the real check without asking for the copy failure, so a full volume answers False

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `V2_verify_does_not_ask`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[no-space]`
  - `tests/test_snapshot_check_room_r1677.py::test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified[quota]`

Old text:

```
            return bool(rb_writer.integrity_ok(database, raise_copy_failure=True))
```

New text:

```
            return bool(rb_writer.integrity_ok(database, raise_copy_failure=False))
```

### `u272.E1_verified_ignores_verdict`

existing guard sample, Capture.verified: true whenever a database was captured, whatever the verdict

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `E1_verified_ignores_verdict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 642 against a baseline of 642
- Kills: 11 (killed)
- Killed:
  - `tests/test_restore.py::test_a_capture_that_failed_its_integrity_check_is_never_restored_from`
  - `tests/test_snapshot.py::test_a_capture_that_verifies_is_the_only_one_anything_may_commit_behind`
  - `tests/test_snapshot.py::test_a_verifier_that_raises_counts_as_not_having_verified`
  - `tests/test_snapshot.py::test_the_verdict_survives_a_round_trip_through_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a companion file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a coupled file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the capture directory]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the database]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the store]`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_write_session.py::test_a_capture_that_failed_its_check_blocks_the_commit_behind_it`

Old text:

```
        return self.database is not None and self.integrity_verified
```

New text:

```
        return self.database is not None
```

### `u272.E2_gate_trusts_manifest`

existing guard sample, assert_verified: pass whenever the database file is there

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `E2_gate_trusts_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 642 against a baseline of 642
- Kills: 9 (killed)
- Killed:
  - `tests/test_restore.py::test_a_capture_that_failed_its_integrity_check_is_never_restored_from`
  - `tests/test_snapshot.py::test_a_capture_that_verifies_is_the_only_one_anything_may_commit_behind`
  - `tests/test_snapshot.py::test_a_verifier_that_raises_counts_as_not_having_verified`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a companion file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[a coupled file]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the capture directory]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the database]`
  - `tests/test_snapshot_flush_u272.py::test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified[the store]`
  - `tests/test_write_session.py::test_a_capture_that_failed_its_check_blocks_the_commit_behind_it`

Old text:

```
    if record.verified and record.database is not None and record.database.exists():
```

New text:

```
    if record.database is not None and record.database.exists():
```

### `u953.M17_nearest_existing_asks_the_path_itself`

nearest_existing stops at the path even when it does not exist, so capacity and permission are asked of nothing

- File: `src/cratekit/core/snapshot.py`
- Source: `u953.json`, row `M17_nearest_existing_asks_the_path_itself`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_snapshot.py`, `tests/test_snapshot_check_room_r1677.py`
- Collected: 209 against a baseline of 209
- Kills: 118 (killed)
- Killed:
  - `tests/test_restore.py::test_a_capture_that_failed_its_integrity_check_is_never_restored_from`
  - `tests/test_restore.py::test_a_capture_whose_manifest_names_a_path_outside_the_set_is_refused`
  - `tests/test_restore.py::test_a_completed_session_is_listed_with_its_timestamp_workflow_and_changes`
  - `tests/test_restore.py::test_a_coupled_file_the_capture_records_as_absent_is_removed_again`
  - `tests/test_restore.py::test_a_dry_run_and_a_real_run_walk_the_same_list_in_the_same_order`
  - `tests/test_restore.py::test_a_held_session_used_after_its_block_is_refused`
  - `tests/test_restore.py::test_a_later_session_that_committed_nothing_does_not_need_an_override`
  - `tests/test_restore.py::test_a_plan_built_before_a_later_commit_is_refused_at_run`
  - `tests/test_restore.py::test_a_pre_cutover_restore_leaves_the_next_session_refused`
  - `tests/test_restore.py::test_a_provider_that_raises_deletes_nothing`
  - `tests/test_restore.py::test_a_rehearsal_never_clears_the_live_companion_files`
  - `tests/test_restore.py::test_a_rehearsal_reports_what_is_outstanding_rather_than_what_it_recorded`
  - `tests/test_restore.py::test_a_restore_handed_an_ordinary_write_session_is_refused`
  - `tests/test_restore.py::test_a_restore_lists_every_effect_it_cannot_undo_and_blocks_convergence`
  - `tests/test_restore.py::test_a_restore_predating_a_cutover_marks_that_tree_unconverged`
  - ... and 103 more, see the JSON sidecar

Old text:

```
    while not probe.exists() and probe.parent != probe:
```

New text:

```
    while False and not probe.exists() and probe.parent != probe:
```

### `u293.S1_reentrant`

held: a process holding the lock takes it again on a second descriptor and refuses itself

- File: `src/cratekit/core/staging_lock.py`
- Source: `u293.json`, row `S1_reentrant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_staging_lock.py`, `tests/test_sync_night.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 237 against a baseline of 237
- Kills: 6 (killed)
- Killed:
  - `tests/test_staging_lock.py::test_one_process_holds_it_again_by_count_and_releases_at_the_outermost`
  - `tests/test_sync_night.py::test_a_night_pass_reaches_the_landing_gate_and_answers_nothing_but_the_name_confirm`
  - `tests/test_sync_night.py::test_a_night_pass_that_needs_the_acknowledgment_stops_there_and_mints_none`
  - `tests/test_sync_night.py::test_a_night_pass_the_vocal_model_cannot_score_waits_at_that_gate_and_queues_nothing`
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_waiting_at_its_gate`
  - `tests/test_sync_night.py::test_a_track_the_download_refused_is_named_in_the_record`

Old text:

```
    if _HANDLE is not None:
```

New text:

```
    if False:
```

### `u293.S2_second_holder_refused`

held: a second holder goes on beside the first rather than refusing

- File: `src/cratekit/core/staging_lock.py`
- Source: `u293.json`, row `S2_second_holder_refused`
- Moved: Same refusal in held; U298 moved the non blocking flock into config.lock_now, which returns whether the lock was had, and the raise now sits under if not had, one level shallower, still the refusal of a second holder
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_staging_lock.py`, `tests/test_sync_night.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 237 against a baseline of 237
- Kills: 5 (killed)
- Killed:
  - `tests/test_staging_lock.py::test_a_holder_that_cannot_be_read_still_refuses`
  - `tests/test_staging_lock.py::test_a_second_holder_refuses_naming_the_first`
  - `tests/test_sync_night.py::test_a_label_go_refuses_while_another_pass_holds_the_lock`
  - `tests/test_sync_night.py::test_a_pass_by_hand_refuses_while_the_night_holds_the_lock`
  - `tests/test_sync_night.py::test_another_pass_holding_the_staging_lock_refuses_the_night_naming_it`

Old text:

```
            raise _held_error(what or verb, _read_holder(handle.read()), path) from None
```

New text:

```
            pass
```

### `r432-b.B5_lock_on_the_library_volume`

config: declare the landing locks library scoped, which puts them on the volume that is commonly exFAT

- File: `src/cratekit/core/state_files.py`
- Source: `r432-b.json`, row `B5_lock_on_the_library_volume`
- Moved: Anchored where u299-replay-after-1.json replayed it: the same entry's root: an installation entry is an _installation call now, so the mutation respells it as a never restored _library entry (U299)
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_landing_labels.py`, `tests/test_config.py`
- Collected: 342 against a baseline of 342
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
- Collected: 342 against a baseline of 342
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

### `u299.U7_library_extras_passed`

_library: the rollback effects, decision stores and sidecars an entry declares are dropped

- File: `src/cratekit/core/state_files.py`
- Source: `u299.json`, row `U7_library_extras_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_snapshot.py`, `tests/test_review_queue.py`, `tests/test_tombstones.py`
- Collected: 463 against a baseline of 463
- Kills: 34 (killed)
- Killed:
  - `tests/test_config.py::test_a_restore_writes_back_the_log_and_never_the_shared_memory_index`
  - `tests/test_config.py::test_the_capture_set_includes_the_databases_sqlite_sidecars`
  - `tests/test_config.py::test_the_one_ported_shape_keyed_by_a_display_name_is_flagged_for_rekeying`
  - `tests/test_config.py::test_the_sidecars_are_declared_on_the_entry_rather_than_listed_by_a_consumer`
  - `tests/test_review_queue.py::test_a_decision_store_lands_owner_only_whatever_the_umask`
  - `tests/test_review_queue.py::test_a_decline_suppresses_and_is_revocable`
  - `tests/test_review_queue.py::test_a_record_whose_payload_is_not_a_mapping_refuses_rather_than_raising`
  - `tests/test_review_queue.py::test_a_revoked_suppression_can_be_recorded_again`
  - `tests/test_review_queue.py::test_a_store_this_build_cannot_recognize_refuses_and_is_never_overwritten[a record that is not a mapping]`
  - `tests/test_review_queue.py::test_a_store_this_build_cannot_recognize_refuses_and_is_never_overwritten[a record whose identifier key was renamed]`
  - `tests/test_review_queue.py::test_a_store_this_build_cannot_recognize_refuses_and_is_never_overwritten[a record whose payload is not a mapping]`
  - `tests/test_review_queue.py::test_a_store_this_build_cannot_recognize_refuses_and_is_never_overwritten[a top level list]`
  - `tests/test_review_queue.py::test_a_store_this_build_cannot_recognize_refuses_and_is_never_overwritten[a top level scalar]`
  - `tests/test_review_queue.py::test_a_store_this_build_cannot_recognize_refuses_and_is_never_overwritten[a version this build does not know]`
  - `tests/test_review_queue.py::test_a_store_this_build_cannot_recognize_refuses_and_is_never_overwritten[another store's document]`
  - ... and 19 more, see the JSON sidecar

Old text:

```
        snapshot=snapshot,
        **extra,
    )
```

New text:

```
        snapshot=snapshot,
    )
```

### `r722.T8_lenient_energy_raises`

read_energy_from_file stops folding a failed read into None

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T8_lenient_energy_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2994 against a baseline of 2994
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
    try:
        return read_energy_checked(path)
    except TagReadFailed as exc:
        log.debug("energy read failed for %s: %s", path, exc)
        return None
```

New text:

```
    return read_energy_checked(path)
```

### `r722.T9_lenient_open_raises`

The lenient reader raises when mutagen cannot open a file

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T9_lenient_open_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2994 against a baseline of 2994
- Kills: 306 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_row_the_library_already_holds_is_not_fetched`
  - `tests/test_analysis_workers.py::test_run_batch_threads_the_decoder_through_to_the_vocal_pass`
  - `tests/test_match_states.py::test_a_candidate_shows_a_key_that_is_true_of_every_path_it_carries`
  - `tests/test_match_states.py::test_a_candidate_whose_title_folds_to_something_keeps_its_identifier`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_key_that_disagrees_outright_is_a_different_answer`
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_lossy_marker_the_template_declares_is_stripped_from_the_recording`
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - ... and 291 more, see the JSON sidecar

Old text:

```
        if strict:
            raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
        log.debug("tag read failed for %s: %s", path, exc)
```

New text:

```
        raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
```

### `u249.M15_noting_reader_drops_field_failure`

_read_tags: note no failure for one undecodable field, so a partly failed read is remembered

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M15_noting_reader_drops_field_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 694 against a baseline of 694
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_noting_reader_answers_what_the_lenient_reader_answers_and_says_what_failed`

Old text:

```
            if failed is not None:
                failed.append(f"{key}: {type(exc).__name__}: {exc}")
            values[field] = None
```

New text:

```
            values[field] = None
```

### `u249.M16_noting_reader_drops_open_failure`

_read_tags: note no failure for a container mutagen could not open, so a moment's I/O error is remembered

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M16_noting_reader_drops_open_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 694 against a baseline of 694
- Kills: 2 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_failed_is_not_remembered`
  - `tests/test_library_reads_remembered.py::test_the_noting_reader_answers_what_the_lenient_reader_answers_and_says_what_failed`

Old text:

```
        if failed is not None:
            failed.append(f"{type(exc).__name__}: {exc}")
        return absent
```

New text:

```
        return absent
```

### `u249.M17_noting_reader_drops_unrecognised`

_read_tags: note no failure for a container mutagen did not recognise

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M17_noting_reader_drops_unrecognised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 694 against a baseline of 694
- Kills: 3 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[empty.m4a]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[empty.ogg]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[zeros.opus]`

Old text:

```
        if failed is not None:
            failed.append("not a container the tag library recognises")
        return absent
```

New text:

```
        return absent
```

### `u249.M18_noting_reader_drops_unsupported`

_read_tags: note no failure for a container this module does not read

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M18_noting_reader_drops_unsupported`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 694 against a baseline of 694
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[short.aac]`

Old text:

```
        if failed is not None:
            failed.append(str(exc))
        return absent
```

New text:

```
        return absent
```

### `u249.M19_noting_reader_inverted`

read_tags_noting: report a failed read as whole

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M19_noting_reader_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 694 against a baseline of 694
- Kills: 6 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[empty.m4a]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[empty.ogg]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[short.aac]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[zeros.opus]`
  - `tests/test_library_reads_remembered.py::test_a_read_that_failed_is_not_remembered`
  - `tests/test_library_reads_remembered.py::test_the_noting_reader_answers_what_the_lenient_reader_answers_and_says_what_failed`

Old text:

```
    return values, not failed
```

New text:

```
    return values, True
```

### `u301.T1_refuse_unknown_admits_a_field`

_refuse_unknown: never refuse, so write_tags of bpm writes nothing and answers True

- File: `src/cratekit/core/tags.py`
- Source: `u301.json`, row `T1_refuse_unknown_admits_a_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tags.py`, `tests/test_no_beatgrid_ever.py`, `tests/test_tagging_engine.py`
- Collected: 169 against a baseline of 169
- Kills: 1 (killed)
- Killed:
  - `tests/test_tags.py::test_writing_a_tempo_field_raises_rather_than_returning_false`

Old text:

```
    unknown = set(names) - set(FIELDS)
    if unknown:
```

New text:

```
    unknown = set(names) - set(FIELDS)
    if False:
```

### `u247.M1_memo_removed`

load_taxonomy: call the unremembered parse, so every load parses its text again, as main did

- File: `src/cratekit/core/taxonomy.py`
- Source: `u247.json`, row `M1_memo_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_active_taxonomy.py`, `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 10 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_read_again_with_the_same_text_is_not_parsed_again`
  - `tests/test_active_taxonomy.py::test_a_copy_rewritten_between_two_loads_is_read_and_judged_again`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_tag_workers.py::test_a_retag_parses_the_active_taxonomy_once_however_many_files_it_corrects`
  - `tests/test_tag_workers.py::test_a_sweep_parses_the_active_taxonomy_once_however_many_files_it_tags`
  - `tests/test_taxonomy.py::test_an_edit_that_keeps_the_length_is_a_different_text_and_is_parsed_again`
  - `tests/test_taxonomy.py::test_the_memo_holds_eight_texts_and_parses_the_first_again_after_a_ninth`
  - `tests/test_taxonomy.py::test_the_same_text_is_parsed_once_and_answers_what_a_fresh_parse_builds`
  - `tests/test_taxonomy.py::test_the_three_texts_an_upgrade_reads_are_each_parsed_once`
  - `tests/test_taxonomy.py::test_two_texts_are_each_parsed_once_and_each_answers_its_own`

Old text:

```
    return _parsed(text)

```

New text:

```
    return _parsed.__wrapped__(text)

```

### `u247.M6_key_is_the_size`

load_taxonomy: key the memo on the text's length, so an edit that keeps the length is answered with the old declaration

- File: `src/cratekit/core/taxonomy.py`
- Source: `u247.json`, row `M6_key_is_the_size`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_active_taxonomy.py`, `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 9 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_rewritten_between_two_loads_is_read_and_judged_again`
  - `tests/test_active_taxonomy.py::test_two_libraries_each_answer_their_own_copy`
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_tag_workers.py::test_a_retag_parses_the_active_taxonomy_once_however_many_files_it_corrects`
  - `tests/test_taxonomy.py::test_an_edit_that_keeps_the_length_is_a_different_text_and_is_parsed_again`
  - `tests/test_taxonomy.py::test_the_memo_holds_eight_texts_and_parses_the_first_again_after_a_ninth`
  - `tests/test_taxonomy.py::test_the_three_texts_an_upgrade_reads_are_each_parsed_once`
  - `tests/test_taxonomy.py::test_two_texts_are_each_parsed_once_and_each_answers_its_own`

Old text:

```
    return _parsed(text)

```

New text:

```
    by_size = load_taxonomy.__dict__.setdefault("by_size", {})
    if len(text) not in by_size:
        by_size[len(text)] = _parsed(text)
    return by_size[len(text)]

```

### `r799-a.L4_a_word_declared_twice_is_refused`

loader: let the second row for one word replace the first

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `r799-a.json`, row `L4_a_word_declared_twice_is_refused`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocabulary.py`, `tests/test_published_genre.py`, `tests/test_tag_remap.py`
- Collected: 511 against a baseline of 511
- Kills: 4 (killed)
- Killed:
  - `tests/test_vocabulary.py::test_a_word_declared_twice_is_refused_whatever_its_case[ POP ]`
  - `tests/test_vocabulary.py::test_a_word_declared_twice_is_refused_whatever_its_case[Pop]`
  - `tests/test_vocabulary.py::test_a_word_declared_twice_is_refused_whatever_its_case[pop]`
  - `tests/test_vocabulary.py::test_every_problem_in_a_table_is_reported_at_once`

Old text:

```
            if word.lower() in seen:
```

New text:

```
            if False:
```

### `r799-a.L5_a_table_nothing_reads_is_refused`

loader: accept a table under a name no source is read through

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `r799-a.json`, row `L5_a_table_nothing_reads_is_refused`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocabulary.py`, `tests/test_published_genre.py`, `tests/test_tag_remap.py`
- Collected: 511 against a baseline of 511
- Kills: 4 (killed)
- Killed:
  - `tests/test_vocabulary.py::test_a_table_nothing_would_read_is_refused_and_not_ignored[bandcamp]`
  - `tests/test_vocabulary.py::test_a_table_nothing_would_read_is_refused_and_not_ignored[beatport]`
  - `tests/test_vocabulary.py::test_a_table_nothing_would_read_is_refused_and_not_ignored[dezer]`
  - `tests/test_vocabulary.py::test_a_table_nothing_would_read_is_refused_and_not_ignored[traxsource]`

Old text:

```
        if source not in VOCABULARY_SOURCES:
```

New text:

```
        if False:
```

### `r799-a.L6_a_word_is_matched_whatever_its_case`

loader: index a row under its word as spelled, not folded

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `r799-a.json`, row `L6_a_word_is_matched_whatever_its_case`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocabulary.py`, `tests/test_published_genre.py`, `tests/test_tag_remap.py`
- Collected: 511 against a baseline of 511
- Kills: 48 (killed)
- Killed:
  - `tests/test_published_genre.py::test_the_shipped_template_files_the_catalogues_measured_words[Alternative]`
  - `tests/test_published_genre.py::test_the_shipped_template_files_the_catalogues_measured_words[Country]`
  - `tests/test_tag_remap.py::test_a_file_tagged_by_the_old_mapping_from_the_catalogues_pop_is_planned[already-wanted]`
  - `tests/test_tag_remap.py::test_a_file_tagged_by_the_old_mapping_from_the_catalogues_pop_is_planned[changed-since-to-Deep House]`
  - `tests/test_tag_remap.py::test_a_file_tagged_by_the_old_mapping_from_the_catalogues_pop_is_planned[changed-since-to-Pop]`
  - `tests/test_tag_remap.py::test_a_file_tagged_by_the_old_mapping_from_the_catalogues_pop_is_planned[changed-since-to-dance / pop]`
  - `tests/test_tag_remap.py::test_a_file_tagged_by_the_old_mapping_from_the_catalogues_pop_is_planned[the-bare-alternative-as-rock]`
  - `tests/test_tag_remap.py::test_a_file_tagged_by_the_old_mapping_from_the_catalogues_pop_is_planned[the-catalogues-pop]`
  - `tests/test_tag_remap.py::test_a_file_tagged_by_the_old_mapping_from_the_catalogues_pop_is_planned[two-records-of-one-word-and-source]`
  - `tests/test_tag_remap.py::test_a_file_that_moved_since_the_plan_is_named_and_not_written`
  - `tests/test_tag_remap.py::test_a_file_the_writer_could_not_write_is_named_as_untouched_and_the_rest_are_written`
  - `tests/test_tag_remap.py::test_a_file_this_verb_rewrote_is_corrected_again_when_the_word_moves_again`
  - `tests/test_tag_remap.py::test_a_file_written_that_does_not_read_back_is_named_as_wrong`
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_person_reads_the_counts_and_the_pairs_at_the_gate`
  - ... and 33 more, see the JSON sidecar

Old text:

```
            table.source: {row.word.lower(): row for row in table.words}
```

New text:

```
            table.source: {row.word: row for row in table.words}
```

### `u118-b.A1_tag_beats_route`

A bucket's tagging only word no longer wins over another bucket's routing alias, so Trap / Wave tags as the breaks bucket

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u118-b.json`, row `A1_tag_beats_route`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_adopt_split_place.py`, `tests/test_routing_parity.py`
- Collected: 1070 against a baseline of 1070
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_each_word_tags_as_the_folder_the_author_gave_it_and_the_tag_routes_there[Trap / Wave-Hip-Hop]`
  - `tests/test_routing_parity.py::test_tagging_matches_the_old_tagger_except_on_a_declared_refusal[trap / wave]`
  - `tests/test_routing_parity.py::test_the_three_strings_the_two_old_tables_flatly_contradicted[Trap / Wave-Hip-Hop]`
  - `tests/test_taxonomy.py::test_a_tagging_only_word_wins_over_another_buckets_routing_alias`

Old text:

```
            tagged[key] = bucket.id
            tagging[key] = (bucket.id, None)
```

New text:

```
            tagged[key] = bucket.id
            tagging.setdefault(key, (bucket.id, None))
```

### `u155.T12_sources_type`

_sources: take any value as the sources, a bare string read letter by letter

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T12_sources_type`
- Moved: Anchored where u299-replay-after-10.json replayed it: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_active_taxonomy.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_placement.py`, `tests/test_foreign_tree.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_genre_retag.py`, `tests/test_genre_sub.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`, `tests/test_label_genre_gate.py`, `tests/test_landing_labels.py`, `tests/test_metadata_policy.py`, `tests/test_no_beatgrid_ever.py`, `tests/test_organize.py`, `tests/test_published_genre.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_report_genres.py`, `tests/test_reports_cli.py`, `tests/test_routing_parity.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_lint.py`, `tests/test_sync_pair.py`, `tests/test_tag_remap.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tagging_engine.py`, `tests/test_taxonomy.py`, `tests/test_taxonomy_upgrade.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_vocabulary.py`, `tests/test_xml_splice_golden.py`
- Collected: 6759 against a baseline of 6759
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_sources_must_be_a_non_empty_list_of_words[Rominimal]`
  - `tests/test_genre_sub.py::test_sources_must_be_a_non_empty_list_of_words[sources2]`

Old text:

```
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        return ()
    return tuple(raw)
```

New text:

```
    return tuple(raw or ())
```

### `r799-a.L1_a_too_coarse_tag_is_refused`

loader: accept a vocabulary row whose tag the taxonomy calls too coarse

- File: `src/cratekit/core/taxonomy_model.py`
- Source: `r799-a.json`, row `L1_a_too_coarse_tag_is_refused`
- Moved: the same text, now in src/cratekit/core/taxonomy_model.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocabulary.py`, `tests/test_published_genre.py`, `tests/test_tag_remap.py`
- Collected: 511 against a baseline of 511
- Kills: 3 (killed)
- Killed:
  - `tests/test_vocabulary.py::test_a_tag_the_taxonomy_calls_too_coarse_is_refused[Electronic]`
  - `tests/test_vocabulary.py::test_a_tag_the_taxonomy_calls_too_coarse_is_refused[Electronica / Other]`
  - `tests/test_vocabulary.py::test_a_tag_the_taxonomy_calls_too_coarse_is_refused[Electronica]`

Old text:

```
    if tag in fallback.too_coarse_as_source:
        return None, (
```

New text:

```
    if False:
        return None, (
```

### `r799-a.L2_a_bare_bucket_name_is_refused`

named folder: answer a by source bucket's default sub for a tag with no row in its map, so the bare name names a folder

- File: `src/cratekit/core/taxonomy_model.py`
- Source: `r799-a.json`, row `L2_a_bare_bucket_name_is_refused`
- Moved: the same text, now in src/cratekit/core/taxonomy_model.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocabulary.py`, `tests/test_published_genre.py`, `tests/test_tag_remap.py`
- Collected: 511 against a baseline of 511
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_tagged_by_the_old_mapping_from_the_catalogues_pop_is_planned[a-word-with-no-folder-now]`
  - `tests/test_tag_remap.py::test_a_run_that_leaves_a_file_says_how_many_and_why_on_every_path`
  - `tests/test_vocabulary.py::test_a_word_the_aliases_answer_with_a_bare_bucket_name_is_declined[Bollywood]`
  - `tests/test_vocabulary.py::test_a_word_the_aliases_answer_with_a_bare_bucket_name_is_declined[Indie Rock]`
  - `tests/test_vocabulary.py::test_a_word_the_aliases_answer_with_a_bare_bucket_name_is_declined[Latin]`
  - `tests/test_vocabulary.py::test_a_word_the_aliases_answer_with_a_bare_bucket_name_is_declined[Punk]`
  - `tests/test_vocabulary.py::test_a_word_the_aliases_answer_with_a_bare_bucket_name_is_declined[World Music]`
  - `tests/test_vocabulary.py::test_an_alias_of_such_a_bucket_with_no_row_in_its_map_is_refused`
  - `tests/test_vocabulary.py::test_every_problem_in_a_table_is_reported_at_once`
  - `tests/test_vocabulary.py::test_the_bare_name_of_a_bucket_that_files_by_source_is_refused`
  - `tests/test_vocabulary.py::test_the_guard_is_taken_with_the_table_and_not_with_its_rows`

Old text:

```
    sub = bucket.sub_by_source.map.get(tag)
    if sub is None:
```

New text:

```
    sub = bucket.sub_by_source.map.get(tag, bucket.sub_by_source.default)
    if sub is None:
```

### `u132.P4_version_raise`

The schema version is never raised

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u132.json`, row `P4_version_raise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 18 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_copy_edited_between_the_answer_and_the_write_is_refused_as_stale`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_that_does_not_read_back_is_replaced_by_the_one_it_replaced`
  - `tests/test_taxonomy_upgrade.py::test_a_crlf_copy_is_kept_byte_for_byte_and_upgraded_in_its_own_line_ending`
  - `tests/test_taxonomy_upgrade.py::test_a_crlf_copy_plans_the_digest_its_lf_twin_does`
  - `tests/test_taxonomy_upgrade.py::test_a_rerun_plans_nothing`
  - `tests/test_taxonomy_upgrade.py::test_a_restore_that_fails_says_so_and_names_the_backup`
  - `tests/test_taxonomy_upgrade.py::test_a_second_run_plans_nothing_and_asks_nothing`
  - `tests/test_taxonomy_upgrade.py::test_a_version_2_copy_gains_favorites_and_soul_in_place_and_keeps_every_line`
  - `tests/test_taxonomy_upgrade.py::test_a_version_line_the_planner_cannot_find_holds_the_raise_and_what_needs_it`
  - `tests/test_taxonomy_upgrade.py::test_an_abort_writes_nothing`
  - `tests/test_taxonomy_upgrade.py::test_an_edit_after_the_second_plan_is_refused_as_stale`
  - `tests/test_taxonomy_upgrade.py::test_an_edited_bucket_is_left_alone`
  - `tests/test_taxonomy_upgrade.py::test_headers_that_cannot_be_matched_to_entries_put_the_block_at_the_end`
  - `tests/test_taxonomy_upgrade.py::test_mixed_line_endings_are_written_as_lf_and_said`
  - `tests/test_taxonomy_upgrade.py::test_soul_is_held_while_rnb_still_files_its_words_until_the_hand_edit`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    if active.schema_version < shipped.schema_version:

```

New text:

```
    if False:

```

### `u132.P7_child_tables`

A bucket's cut stops at its first child table

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u132.json`, row `P7_child_tables`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 30 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_copy_edited_between_the_answer_and_the_write_is_refused_as_stale`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_made_before_u133_takes_the_discogs_table_and_loads_after_the_holds_edits`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_that_does_not_read_back_is_replaced_by_the_one_it_replaced`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_with_no_jazz_keyword_rule_is_told_it_has_none`
  - `tests/test_taxonomy_upgrade.py::test_a_crlf_copy_is_kept_byte_for_byte_and_upgraded_in_its_own_line_ending`
  - `tests/test_taxonomy_upgrade.py::test_a_crlf_copy_plans_the_digest_its_lf_twin_does`
  - `tests/test_taxonomy_upgrade.py::test_a_rerun_plans_nothing`
  - `tests/test_taxonomy_upgrade.py::test_a_restore_that_fails_says_so_and_names_the_backup`
  - `tests/test_taxonomy_upgrade.py::test_a_second_run_plans_nothing_and_asks_nothing`
  - `tests/test_taxonomy_upgrade.py::test_a_version_2_copy_gains_favorites_and_soul_in_place_and_keeps_every_line`
  - `tests/test_taxonomy_upgrade.py::test_a_version_line_the_planner_cannot_find_holds_the_raise_and_what_needs_it`
  - `tests/test_taxonomy_upgrade.py::test_a_vocabulary_row_whose_tag_files_where_the_template_shares_the_word_is_not_named`
  - `tests/test_taxonomy_upgrade.py::test_a_word_the_shipped_template_files_twice_is_not_a_clash`
  - `tests/test_taxonomy_upgrade.py::test_an_abort_writes_nothing`
  - `tests/test_taxonomy_upgrade.py::test_an_edit_after_the_second_plan_is_refused_as_stale`
  - ... and 15 more, see the JSON sidecar

Old text:

```
            if not later.startswith(child):

```

New text:

```
            if True:

```

### `u132.P8_present_skip`

An entry the copy already declares is planned again

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u132.json`, row `P8_present_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 21 (killed)
- Killed:
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
  - `tests/test_taxonomy_upgrade.py::test_one_place_filing_a_word_under_two_spellings_names_both_in_one_sentence`
  - ... and 6 more, see the JSON sidecar

Old text:

```
            if entry_id in present[kind]:

```

New text:

```
            if False:

```

### `u133-a.P9_keyword_note_gone`

The plan never carries the sentence about the copy's keyword rule

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u133-a.json`, row `P9_keyword_note_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 3 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_copy_with_no_jazz_keyword_rule_is_told_it_has_none`
  - `tests/test_taxonomy_upgrade.py::test_the_hand_edit_the_hold_names_lets_jazz_in_on_the_next_run`
  - `tests/test_taxonomy_upgrade.py::test_the_upgrade_that_adds_jazz_says_the_copys_keyword_rule_is_left`

Old text:

```
        keywords=_keyword_rules(tuple(added[BUCKET]), active, shipped),

```

New text:

```
        keywords=(),

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

### `r1184.M10_off_taxonomy_exact`

off_taxonomy: drop the exact name refusal, so a folder's name exactly falls to the tagging tier

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M10_off_taxonomy_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_declined_word_that_is_a_folders_name_is_a_folder_already_declared`

Old text:

```
    exact = declared.bucket_for_display(word)
    if exact is not None:
```

New text:

```
    exact = declared.bucket_for_display(word)
    if False:
```

### `r1184.M11_edit_own_name_flag`

alias: mark the own name plan as an ordinary one, so the no change sentence claims a tagging alias

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M11_edit_own_name_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 4 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_answered_by_its_own_folder[Breaks / D&B / Dubstep]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_answered_by_its_own_folder[breaks / d&b / dubstep]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_answered_by_its_own_folder[breaks_dnb_dubstep]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_retagged_to_the_exact_name`

Old text:

```
before=text, after=text, own_name=True
```

New text:

```
before=text, after=text, own_name=False
```

### `r1184.M12_bare_asks_word_first`

alias: drop asking the word before the bare folder refusal, so a too coarse word is offered the folder verb

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M12_bare_asks_word_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-word-to-a-bare-folder]`

Old text:

```
        off_taxonomy(declared, spelled)
        raise Refused(
            BARE_FOLDER,
```

New text:

```
        raise Refused(
            BARE_FOLDER,
```

### `r1184.M13_bare_step_names_word`

alias: the bare folder step names the folder verb without the word

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M13_bare_step_names_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[bare-folder-step-names-the-folder-verb]`

Old text:

```
{FOLDER_VERB} {shlex.join((spelled,))}"
```

New text:

```
{FOLDER_VERB}"
```

### `r1184.M14_step_command_words`

own_name_answer: the step's command names the folder only, not the word

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M14_step_command_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 289 against a baseline of 289
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_folders_own_name_in_another_case_is_named_with_its_one_answer`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`
  - `tests/test_taxonomy_word.py::test_a_file_carrying_a_folders_own_name_is_never_retagged`
  - `tests/test_taxonomy_word.py::test_the_folder_refusal_of_an_own_name_names_the_alias_that_answers_it`
  - `tests/test_taxonomy_word.py::test_the_warnings_name_each_own_name_with_its_one_answer`

Old text:

```
{shlex.join((word, bucket.display))}
```

New text:

```
{shlex.join((bucket.display,))}
```

### `r1184.M15_own_names_none`

own_names: drop the guard on an unread taxonomy

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M15_own_names_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 289 against a baseline of 289
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_off_taxonomy_warning_names_a_folders_own_name_with_its_one_answer`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`
  - `tests/test_taxonomy_word.py::test_the_warnings_name_each_own_name_with_its_one_answer`

Old text:

```
    if declared is None:
        return ""
    said = []
```

New text:

```
    said = []
```

### `r1184.M16_own_names_empty`

own_names: drop the empty answer, so every warning ends with an empty own name sentence

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M16_own_names_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 289 against a baseline of 289
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_the_warnings_name_each_own_name_with_its_one_answer`

Old text:

```
    if not said:
        return ""
    return ". A word
```

New text:

```
    return ". A word
```

### `r1184.M1_own_folder_exact_first`

own_folder: drop the exact name guard, so a folder's name exactly is read as its own name in another case

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M1_own_folder_exact_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_declined_word_that_is_a_folders_name_is_a_folder_already_declared`
  - `tests/test_taxonomy_word.py::test_a_folders_name_exactly_already_has_a_place`

Old text:

```
    if declared.bucket_for_display(word) is not None:
        return None
    folded = word.casefold()
```

New text:

```
    folded = word.casefold()
```

### `r1184.M2_own_folder_casefold`

own_folder: compare the name exactly rather than in any case, so no word is ever a folder's own name in another case

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M2_own_folder_casefold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 289 against a baseline of 289
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_folders_own_name_in_another_case_is_named_with_its_one_answer`
  - `tests/test_tag_workers.py::test_the_off_taxonomy_warning_names_a_folders_own_name_with_its_one_answer`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`
  - `tests/test_taxonomy_word.py::test_a_file_carrying_a_folders_own_name_is_never_retagged`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_answered_by_its_own_folder[Breaks / D&B / Dubstep]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_answered_by_its_own_folder[breaks / d&b / dubstep]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_answered_by_its_own_folder[breaks_dnb_dubstep]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_refused_to_any_other_folder[AFRO HOUSE]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_refused_to_any_other_folder[breaks / d&b / dubstep]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_refused_to_any_other_folder[nonelectronic]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_retagged_to_the_exact_name`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_its_folder_cannot_take_is_refused_with_its_step`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_whose_folder_files_nothing_by_its_name_is_refused_truly`
  - `tests/test_taxonomy_word.py::test_the_folder_refusal_of_an_own_name_names_the_alias_that_answers_it`
  - `tests/test_taxonomy_word.py::test_the_warnings_name_each_own_name_with_its_one_answer`

Old text:

```
b.display.casefold() == folded), None)
```

New text:

```
b.display == word), None)
```

### `r1184.M3_files_by_name`

files_by_name: say every folder's name files a track by itself, so nonelectronic is retagged NonElectronic

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M3_files_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 289 against a baseline of 289
- Kills: 8 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_off_taxonomy_warning_names_a_folders_own_name_with_its_one_answer`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_its_folder_cannot_take_is_refused_with_its_step`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_whose_folder_files_nothing_by_its_name_is_refused_truly`
  - `tests/test_taxonomy_word.py::test_an_alias_to_a_folder_whose_name_files_nothing_by_itself_is_refused[Electronica / Other]`
  - `tests/test_taxonomy_word.py::test_an_alias_to_a_folder_whose_name_files_nothing_by_itself_is_refused[NonElectronic]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[bare-folder-step-names-the-folder-verb]`
  - `tests/test_taxonomy_word.py::test_the_bare_folder_refusal_names_the_folder_verb_as_its_step`
  - `tests/test_taxonomy_word.py::test_the_folder_refusal_of_an_own_name_names_the_alias_that_answers_it`

Old text:

```
    return declared.named_folder(bucket.display) == (bucket.id, None)


def _filed_now
```

New text:

```
    return True


def _filed_now
```

### `r1184.M4_filed_now_keyword`

_filed_now: drop the keyword rule branch, so a keyword filed word is said to be filed by a routing alias

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M4_filed_now_keyword`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 289 against a baseline of 289
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_whose_folder_files_nothing_by_its_name_is_refused_truly`

Old text:

```
    if found.match is routing.Match.FUZZY:
        return f"in {where} by the keyword rule {found.matched_on!r}"

```

New text:

```
(empty)
```

### `r1184.M5_answer_branch`

own_name_answer: offer the alias to the folder even when its name files nothing by itself

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M5_answer_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 289 against a baseline of 289
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_off_taxonomy_warning_names_a_folders_own_name_with_its_one_answer`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_its_folder_cannot_take_is_refused_with_its_step`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_whose_folder_files_nothing_by_its_name_is_refused_truly`
  - `tests/test_taxonomy_word.py::test_the_folder_refusal_of_an_own_name_names_the_alias_that_answers_it`

Old text:

```
    if files_by_name(declared, bucket):
        command
```

New text:

```
    if True:
        command
```

### `r1184.M6_alias_other_folder`

alias: drop the refusal of an own name to another folder, so it plans its own folder's retag under another name

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M6_alias_other_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 3 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_carrying_a_folders_own_name_is_never_retagged`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_refused_to_any_other_folder[AFRO HOUSE]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_refused_to_any_other_folder[breaks / d&b / dubstep]`

Old text:

```
        if own.id != target.id:
            raise Refused(
```

New text:

```
        if False:
            raise Refused(
```

### `r1184.M7_alias_own_bare`

alias: drop the refusal of an own name whose folder files nothing by its name

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M7_alias_own_bare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_its_folder_cannot_take_is_refused_with_its_step`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_whose_folder_files_nothing_by_its_name_is_refused_truly`

Old text:

```
        if not files_by_name(declared, own):
            raise Refused(OWN_NAME, said, step=step)
```

New text:

```
        if False:
            raise Refused(OWN_NAME, said, step=step)
```

### `r1184.M8_alias_own_block`

alias: drop the own name branch whole, so the alias takes the path main took

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M8_alias_own_block`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 4 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_answered_by_its_own_folder[Breaks / D&B / Dubstep]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_answered_by_its_own_folder[breaks / d&b / dubstep]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_answered_by_its_own_folder[breaks_dnb_dubstep]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_retagged_to_the_exact_name`

Old text:

```
    own = own_folder(declared, spelled)
    if own is not None:
```

New text:

```
    own = own_folder(declared, spelled)
    if False:
```

### `r1184.M9_off_taxonomy_own_block`

off_taxonomy: drop the own name refusal, so the folder verb plans a second folder of that name

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `r1184.json`, row `M9_off_taxonomy_own_block`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 4 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_refused_to_any_other_folder[AFRO HOUSE]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_refused_to_any_other_folder[breaks / d&b / dubstep]`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_refused_to_any_other_folder[nonelectronic]`
  - `tests/test_taxonomy_word.py::test_the_folder_refusal_of_an_own_name_names_the_alias_that_answers_it`

Old text:

```
    own = own_folder(declared, word)
    if own is not None:
        said, step = own_name_answer(declared, word, own)
        raise
```

New text:

```
    own = own_folder(declared, word)
    if False:
        said, step = own_name_answer(declared, word, own)
        raise
```

### `u194.W10_folder_rates`

folder: never write rates = false, so a folder like Jazz is given a star rating its model never had

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `u194.json`, row `W10_folder_rates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_like_names_the_bucket_the_folder_takes_its_priors_from`

Old text:

```
    if not like.rates:
        out.append("rates = false\n")
```

New text:

```
    if False:
        out.append("rates = false\n")
```

### `u194.W12_string_escape`

_string: write the word between quotes unescaped, so a quote or a backslash in it breaks the copy

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `u194.json`, row `W12_string_escape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_word_with_a_quote_is_written_as_a_toml_string_that_reads_back`

Old text:

```
    return json.dumps(value, ensure_ascii=False)
```

New text:

```
    return f'"{value}"' 
```

### `u194.W13_inline_joiner`

_with_tag_alias: join an inline array without a comma

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `u194.json`, row `W13_inline_joiner`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_an_alias_joins_an_array_written_on_one_line`

Old text:

```
            joiner = "" if body.endswith("[") else ", " if not body.endswith(",") else " "
```

New text:

```
            joiner = "" if body.endswith("[") else " "
```

### `u194.W1_off_taxonomy_any_word`

off_taxonomy: answer every word as off taxonomy, so a too coarse or already filed word becomes an alias or a folder

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `u194.json`, row `W1_off_taxonomy_any_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 14 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_too_coarse_word_is_refused_before_the_gate`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[alias-already-saved-to-another-genre]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[fallback-says-a-hand-alias-would-override]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-alias-Electro]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-alias-Electronic]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-alias-Electronica]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-alias-Experimental]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-alias-Other]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-folder-Electro]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-folder-Electronic]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-folder-Experimental]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-folder-Other]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-word-to-a-bare-folder]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[word-already-tagged-names-where]`

Old text:

```
    said = routing.suggest_tag(declared, word)
    if said.off_taxonomy:
        return said
```

New text:

```
    said = routing.suggest_tag(declared, word)
    if True:
        return said
```

### `u194.W2_decline_not_too_coarse`

off_taxonomy: drop the decline branch, so a word tagging refuses by rule is called already filed

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `u194.json`, row `W2_decline_not_too_coarse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 7 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_too_coarse_word_is_refused_before_the_gate`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-alias-Electronic]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-alias-Electronica]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-alias-Other]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-folder-Electronic]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-folder-Other]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-word-to-a-bare-folder]`

Old text:

```
    if said.decline is not None:
        raise Refused(
```

New text:

```
    if False:
        raise Refused(
```

### `u194.W3_fallback_not_too_coarse`

off_taxonomy: drop the fallback branch, so a word the taxonomy files in its fallback on purpose is called already filed

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `u194.json`, row `W3_fallback_not_too_coarse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 5 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[fallback-says-a-hand-alias-would-override]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-alias-Electro]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-alias-Experimental]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-folder-Electro]`
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[too-coarse-folder-Experimental]`

Old text:

```
    if said.bucket_id == fallback:
```

New text:

```
    if False:
```

### `u194.W5_saved_alias_rerun`

alias: drop the short circuit for an alias already saved to the genre, so a rerun after a partial write is refused

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `u194.json`, row `W5_saved_alias_rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 4 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_that_will_not_take_the_genre_is_named_and_the_rerun_finishes`
  - `tests/test_taxonomy_word.py::test_an_alias_is_saved_tags_the_word_as_the_genre_and_moves_nothing_else`
  - `tests/test_taxonomy_word.py::test_nothing_to_do_does_not_claim_a_file_it_could_not_read`
  - `tests/test_taxonomy_word.py::test_the_alias_is_saved_and_the_file_retagged`

Old text:

```
    if declared.tagging_alias(spelled.lower()) == (target.id, None):
```

New text:

```
    if False:
```

### `u194.W7_genre_casefold_unique`

genre: take the first bucket whose name matches in another case rather than only a unique one

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `u194.json`, row `W7_genre_casefold_unique`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_an_answer_the_planner_cannot_give_is_refused_with_why[genre-in-a-case-two-folders-share]`

Old text:

```
    if len(folded) == 1:
        return folded[0]
```

New text:

```
    if folded:
        return folded[-1]
```

### `u194.W8_folder_already_declared`

folder: drop the short circuit for a folder already declared, so a second run of the same answer is refused

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `u194.json`, row `W8_folder_already_declared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 4 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_declined_word_that_is_a_folders_name_is_a_folder_already_declared`
  - `tests/test_taxonomy_word.py::test_a_folders_name_exactly_already_has_a_place`
  - `tests/test_taxonomy_word.py::test_a_genre_folder_is_made_in_the_form_jazz_has_and_the_word_routes_into_it`
  - `tests/test_taxonomy_word.py::test_the_genre_folder_is_made_and_the_files_route_into_it`

Old text:

```
    made = declared.bucket_for_display(spelled)
    if made is not None:
```

New text:

```
    made = declared.bucket_for_display(spelled)
    if False:
```

### `u194.W9_folder_like_default`

folder: take the fallback's priors by default rather than those of the bucket the word routes to now

- File: `src/cratekit/core/taxonomy_word.py`
- Source: `u194.json`, row `W9_folder_like_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_word_fuzzy_routed_to_a_real_bucket_takes_that_buckets_priors`

Old text:

```
        like = declared.bucket(routing.resolve_bucket(declared, spelled).bucket_id)
```

New text:

```
        like = declared.bucket(declared.fallback.bucket)
```

### `r431-a.A1_a_plain_row_gains_a_companion`

uncredited_title answers the stripped title even when nothing was stripped, so a plain deletion writes a companion

- File: `src/cratekit/core/tombstone.py`
- Source: `r431-a.json`, row `A1_a_plain_row_gains_a_companion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_deletion.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1278 against a baseline of 1278
- Kills: 21 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_confirmed_removal_the_person_deleted_in_the_finder_does_not_block_the_next_one`
  - `tests/test_deletion.py::test_a_file_moved_by_hand_after_the_confirmation_is_recorded_rather_than_retired_silently`
  - `tests/test_deletion.py::test_a_listing_says_which_suppressions_moved_no_file`
  - `tests/test_deletion.py::test_a_run_interrupted_after_trashing_resumes_without_re_offering`
  - `tests/test_deletion.py::test_a_tombstone_that_cannot_be_written_puts_the_file_back`
  - `tests/test_deletion.py::test_an_interrupt_during_the_store_write_still_puts_the_file_back[ctrl-c]`
  - `tests/test_deletion.py::test_an_interrupt_during_the_store_write_still_puts_the_file_back[sigterm]`
  - `tests/test_deletion.py::test_one_file_deleted_by_hand_under_a_healthy_anchor_is_still_settled`
  - `tests/test_deletion.py::test_the_listing_carries_the_column_value_a_missed_tombstone_was_built_from`
  - `tests/test_deletion.py::test_tombstone_list_revokes_and_then_shows_the_lifted_record`
  - `tests/test_deletion.py::test_tombstone_list_shows_what_the_deletion_pass_suppressed`
  - `tests/test_match_states.py::test_a_deletion_of_the_plain_record_writes_no_companion`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`
  - `tests/test_tombstones.py::test_a_revoked_tombstone_stays_listable_so_the_two_cases_can_be_told_apart`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_two_records_and_a_plain_one_is_one`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return stripped if dropped else ""
```

New text:

```
    return stripped
```

### `r431-a.A2_one_kind_for_both`

The companion is recorded under the tombstone's own kind, where every verbatim lookup lands on it

- File: `src/cratekit/core/tombstone.py`
- Source: `r431-a.json`, row `A2_one_kind_for_both`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_deletion.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1278 against a baseline of 1278
- Kills: 17 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`
  - `tests/test_uncredited_tombstone.py::test_a_companion_already_lifted_keeps_the_lift_it_was_given`
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_never_the_answer_to_a_verbatim_lookup`
  - `tests/test_uncredited_tombstone.py::test_a_companion_lifted_alone_does_not_come_back_behind_a_persons_back`
  - `tests/test_uncredited_tombstone.py::test_a_companion_never_says_a_run_recorded_a_different_rows_deletion`
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_two_records_and_a_plain_one_is_one`
  - `tests/test_uncredited_tombstone.py::test_a_second_deletion_leaves_the_shared_companion_exactly_as_it_stood`
  - `tests/test_uncredited_tombstone.py::test_a_shared_companion_survives_a_lift_even_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_deleting_again_after_a_full_lift_suppresses_both_halves_again`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_credited_tombstone_lifts_its_companion`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_plain_tombstone_touches_no_companion_it_does_not_own`
  - `tests/test_uncredited_tombstone.py::test_lifting_the_companion_alone_leaves_the_tombstone_standing`
  - ... and 2 more, see the JSON sidecar

Old text:

```
KIND_VERSION_UNCREDITED = "version-uncredited"
```

New text:

```
KIND_VERSION_UNCREDITED = "version"
```

### `r1255.T1_tree_registry_clause`

tree_registry._whole_log: word the refusal with the old count, not the clause

- File: `src/cratekit/core/tree_registry.py`
- Source: `r1255.json`, row `T1_tree_registry_clause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_tree_registry.py`, `tests/test_cutover_precheck.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_an_unreadable_record_keeps_its_own_refusal`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[open-None-<lambda>-readable2-so whether a run is still open was not established]`

Old text:

```
            f"{session.unread_clause(unreadable, cfg)}, so {so}; refusing rather than "
```

New text:

```
            f"the session log holds {len(unreadable)} entries this build cannot read, so {so}; refusing rather than "
```

### `u953.M2_registry_cause_remedy_fixed`

tree_registry's _cause answers every unreadable registry with run doctor, dropping the upgrade remedy for a newer schema

- File: `src/cratekit/core/tree_registry.py`
- Source: `u953.json`, row `M2_registry_cause_remedy_fixed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_writers_native.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_tree_still_on_the_bridge_refuses_and_marks_nothing`
  - `tests/test_intake_writers_native.py::test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy`

Old text:

```
        remediation=Remediation(remedy=remedy),
```

New text:

```
        remediation=Remediation(remedy=Remedy.RUN_DOCTOR),
```

### `r1844.N7_held_rows_read_absent`

landed_absences: a landed row the database holds is read as absent, so a live track's file is offered

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N7_held_rows_read_absent`
- Moved: Anchored where u310-replay-after-c.json replayed it: the formatter split the over long comprehension; the held filter is dropped, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 456 against a baseline of 456
- Kills: 35 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_is_one_candidate`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`
  - `tests/test_delete_landed_removed.py::test_a_landing_a_restore_rolled_back_offers_nothing`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landing_of_another_database_offers_nothing`
  - ... and 20 more, see the JSON sidecar

Old text:

```
            (content_id, columns) for content_id, columns, _uuid in rows if content_id not in held
```

New text:

```
            (content_id, columns) for content_id, columns, _uuid in rows
```

### `r1037.M9_recorded_not_excluded`

plan: a row sync removed recorded is read again as a landed absence, so one row is two candidates

- File: `src/cratekit/deletion/run.py`
- Source: `r1037.json`, row `M9_recorded_not_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 456 against a baseline of 456
- Kills: 2 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`

Old text:

```
        present=held | {row.content_id for row in recorded},
```

New text:

```
        present=held,
```

### `r431-a.A15_the_verb_lifts_through_the_store`

run.revoke lifts a tombstone through the store and not through stores.revoke_tombstone, so no companion goes

- File: `src/cratekit/deletion/run.py`
- Source: `r431-a.json`, row `A15_the_verb_lifts_through_the_store`
- Moved: only the comment above the guarded line changed; the verb lifts through the opened store, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_uncredited_tombstone.py`
- Collected: 366 against a baseline of 366
- Kills: 6 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_found_by_its_pointer_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_one_write_and_so_is_lifting_it`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_credited_tombstone_lifts_its_companion`
  - `tests/test_uncredited_tombstone.py::test_the_shared_companion_is_also_found_in_the_other_order`

Old text:

```
                # (R-431); tombstones are read first, never needing the declines.
                return stores.revoke_tombstone(cfg, suppression_id, actor=actor)
```

New text:

```
                # (R-431); tombstones are read first, never needing the declines.
                return held.revoke(suppression_id, actor=actor)
```

### `r431-a.A10_the_shared_companion_goes_with_the_first_lift`

Lifting takes every companion the tombstone accounts for, whoever else still does

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A10_the_shared_companion_goes_with_the_first_lift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1113 against a baseline of 1113
- Kills: 4 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_shared_companion_survives_a_lift_even_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_the_shared_companion_is_also_found_in_the_other_order`

Old text:

```
    return tuple(sorted(mine - still_accounted_for))
```

New text:

```
    return tuple(sorted(mine))
```

### `r431-a.A11_a_lifted_tombstone_still_accounts`

A tombstone that was itself lifted still holds the shared companion, so the second lift strands it

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A11_a_lifted_tombstone_still_accounts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1113 against a baseline of 1113
- Kills: 3 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_the_shared_companion_is_also_found_in_the_other_order`

Old text:

```
            and other.suppressing
            and other.suppression_id != named.suppression_id
```

New text:

```
            and other.suppression_id != named.suppression_id
```

### `r431-a.A12_the_named_tombstone_accounts_for_itself`

The tombstone being lifted counts as still accounting, so no companion is ever lifted

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A12_the_named_tombstone_accounts_for_itself`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1113 against a baseline of 1113
- Kills: 6 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_found_by_its_pointer_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_one_write_and_so_is_lifting_it`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_credited_tombstone_lifts_its_companion`
  - `tests/test_uncredited_tombstone.py::test_the_shared_companion_is_also_found_in_the_other_order`

Old text:

```
            and other.suppressing
            and other.suppression_id != named.suppression_id
```

New text:

```
            and other.suppressing
```

### `r431-a.A13_accounting_by_stripping_alone`

_accounts_for drops the pointer, so a moved stripping rule strands a companion and takes a shared one

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A13_accounting_by_stripping_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1113 against a baseline of 1113
- Kills: 1 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_found_by_its_pointer_when_the_stripping_rule_has_moved`

Old text:

```
    found = {str(credited.payload.get(UNCREDITED_ID_FIELD) or "")}
```

New text:

```
    found = {""}
```

### `r431-a.A14_accounting_by_pointer_alone`

_accounts_for drops the stripping, so a tombstone with no pointer accounts for nothing

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A14_accounting_by_pointer_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1113 against a baseline of 1113
- Kills: 1 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`

Old text:

```
    if stripped:
        found.add(
```

New text:

```
    if stripped and not stripped:
        found.add(
```

### `r431-a.A3_stripped_from_the_title_column`

The companion is stripped from the Title column and not from the composed identity, so a mix name in the version column is lost

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A3_stripped_from_the_title_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1113 against a baseline of 1113
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_uncredited_tombstone.py::test_the_companion_is_built_from_the_composed_title_not_the_title_column`

Old text:

```
    stripped = tombstone.uncredited_title(verbatim["title"])
```

New text:

```
    stripped = tombstone.uncredited_title(tombstone.fold(row.title))
```

### `r431-a.A4_the_tombstone_names_no_companion`

The tombstone's pointer to its companion is written empty

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A4_the_tombstone_names_no_companion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1113 against a baseline of 1113
- Kills: 2 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_found_by_its_pointer_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_the_listing_links_the_two_halves_of_one_deletion_in_both_directions`

Old text:

```
            UNCREDITED_ID_FIELD: uncredited_id,
```

New text:

```
            UNCREDITED_ID_FIELD: "",
```

### `r431-a.A5_the_companion_names_no_tombstone`

The companion's pointer back is dropped from its payload, so the listing cannot link the pair

- File: `src/cratekit/deletion/stores.py`
- Source: `r431-a.json`, row `A5_the_companion_names_no_tombstone`
- Moved: the companion's payload is now built into a local before the write, so its indentation changed; the credited id is emptied, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_intake_missing.py`, `tests/test_label_approved.py`, `tests/test_match_states.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 1113 against a baseline of 1113
- Kills: 7 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_two_records_and_a_plain_one_is_one`
  - `tests/test_uncredited_tombstone.py::test_a_second_deletion_leaves_the_shared_companion_exactly_as_it_stood`
  - `tests/test_uncredited_tombstone.py::test_the_listing_links_the_two_halves_of_one_deletion_in_both_directions`

Old text:

```
        CREDITED_ID_FIELD: review.suppression_id_for(
            tombstone.STORE_KEY, tombstone.KIND_VERSION, identity
        ),
```

New text:

```
        CREDITED_ID_FIELD: "",
```

### `r1037.M19_version_two_refused`

_recognize: read only version 1, so this build refuses its own document

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M19_version_two_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 456 against a baseline of 456
- Kills: 114 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_is_one_candidate`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`
  - `tests/test_delete_landed_removed.py::test_a_landing_a_restore_rolled_back_offers_nothing`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landing_of_another_database_offers_nothing`
  - ... and 99 more, see the JSON sidecar

Old text:

```
READABLE_VERSIONS = frozenset({1, WATERMARK_VERSION})
```

New text:

```
READABLE_VERSIONS = frozenset({1})
```

### `u129-author.A12_archive_backfill_swallows_all`

Catch Exception around plan_archive so a credential refusal becomes a warning

- File: `src/cratekit/export/set_cli.py`
- Source: `u129-author.json`, row `A12_archive_backfill_swallows_all`
- Moved: the backfill's soft skip is still in set_cli._export_archive_backfill, its warning now built by the shared warning helper from a said string; same catch widened to Exception
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_archive_backfill_refuses_a_credential_error`

Old text:

```
        except CratekitError as exc:
            # Soft skip per set, as a landing's _plan_set_archive does. A
            # CredentialError (not a CratekitError) still refuses the verb.
            said = f"{name}: {exc.cause.message}"
            warnings.append(warning("export-archive-backfill-refused", said))
            continue

```

New text:

```
        except Exception as exc:
            said = f"{name}: {exc}"
            warnings.append(warning("export-archive-backfill-refused", said))
            continue

```

### `u140.B10_queued_day_name_dropped`

_names_for_job stops giving the queued day's form, which is the name the Signal set was exported under

- File: `src/cratekit/export/set_common.py`
- Source: `u140.json`, row `B10_queued_day_name_dropped`
- Moved: the same text, now in src/cratekit/export/set_common.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_backfill_after_the_rename_plans_no_twin_and_a_named_export_adds_to_it`
  - `tests/test_export_set_rename.py::test_a_job_with_no_frozen_name_is_found_by_the_queued_day_and_refrozen`

Old text:

```
    if landing is not None and landing != posted:
        found.append(set_name(set_playlist.playlist_name(words, on=landing)))

```

New text:

```
    if False:
        found.append(set_name(set_playlist.playlist_name(words, on=landing)))

```

### `r1017.M12_twin_message_names_to`

Refusal: name the held playlist under the new name rather than the name it is recorded under

- File: `src/cratekit/export/set_rename.py`
- Source: `r1017.json`, row `M12_twin_message_names_to`
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`

Old text:

```
            f"{planned.playlist.remote_id} under {planned.playlist.name!r} and "
```

New text:

```
            f"{planned.playlist.remote_id} under {to!r} and "
```

### `r1017.M1_no_recorded_names`

Rename: drop the names the landings recorded from the names looked up, the defect R-1017 names

- File: `src/cratekit/export/set_rename.py`
- Source: `r1017.json`, row `M1_no_recorded_names`
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 174 against a baseline of 174
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old`
  - `tests/test_export_set_rename.py::test_the_backfill_plans_no_twin_after_a_rename_by_the_landing_record`
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`
  - `tests/test_export_set_rename.py::test_two_playlists_under_two_older_names_are_a_twin_not_a_choice`

Old text:

```
    recorded = tuple(set_name(one) for one in set_playlist.recorded_names(cfg, job.job_id))
```

New text:

```
    recorded = ()
```

### `r1017.M2_recorded_before_frozen`

Rename: rank the landing names ahead of the frozen name an earlier rename chose

- File: `src/cratekit/export/set_rename.py`
- Source: `r1017.json`, row `M2_recorded_before_frozen`
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`

Old text:

```
            for one in (set_name(frozen) if frozen else "", *recorded, *_names_for_job(job))
```

New text:

```
            for one in (*recorded, set_name(frozen) if frozen else "", *_names_for_job(job))
```

### `u140.B6_mark_refusal_dropped`

plan_rename retitles a playlist the archive marked

- File: `src/cratekit/export/set_rename.py`
- Source: `u140.json`, row `B6_mark_refusal_dropped`
- Moved: Anchored where u309-replay-after-d.json replayed it: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 85 against a baseline of 85
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_playlist_the_archive_marked_is_refused_rather_than_retitled`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`

Old text:

```
        if mark is not None:
            raise _rename_unresolved(

```

New text:

```
        if False:
            raise _rename_unresolved(

```

### `u140.B7_twin_refusal_dropped`

plan_rename names the twin and goes on to adopt the record under the new name

- File: `src/cratekit/export/set_rename.py`
- Source: `u140.json`, row `B7_twin_refusal_dropped`
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_is_refused_rather_than_adopted`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old`
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`
  - `tests/test_export_set_rename.py::test_two_playlists_under_two_older_names_are_a_twin_not_a_choice`

Old text:

```
    if planned.twin is not None:

```

New text:

```
    if False:

```

### `u140.B8_flag_conflict_dropped`

export set --rename accepts a tracklist or --name beside it

- File: `src/cratekit/export/set_rename.py`
- Source: `u140.json`, row `B8_flag_conflict_dropped`
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_rename_with_a_tracklist_or_name_is_refused_before_anything`

Old text:

```
    if ctx.args.tracklist is not None or ctx.args.name is not None:

```

New text:

```
    if False:

```

### `u140.B9_abort_applies`

the rename writes when the gate was answered abort

- File: `src/cratekit/export/set_rename.py`
- Source: `u140.json`, row `B9_abort_applies`
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_an_aborted_rename_writes_nothing`

Old text:

```
    option = ctx.gate.require(gate, plan=built.payload, context=built.shown)
    if option != "apply" or not built.writes:

```

New text:

```
    option = ctx.gate.require(gate, plan=built.payload, context=built.shown)
    if not built.writes:

```

### `u113-a.A2_queue_order`

The account playlists are taken newest job first, the order the store lists them

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A2_queue_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 23223 against a baseline of 23223
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        queued = sorted(
            batch_name.pass_jobs(cfg, pass_name), key=lambda job: (job.created, job.job_id)
        )
```

New text:

```
        queued = batch_name.pass_jobs(cfg, pass_name)
```

### `u113-a.A3_no_pass_splits_nothing`

A landing given no pass still splits, by every named job on the library

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A3_no_pass_splits_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 23223 against a baseline of 23223
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not pass_name or not files:
        return ()
    found = sources(cfg, pass_name)
```

New text:

```
    if not files:
        return ()
    found = sources(cfg, pass_name or "")
```

### `u113-a.A8_pending_any_state`

Names held by intake files are read from records whatever their state, not only those awaiting import

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A8_pending_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`

Old text:

```
        and record.state is session.SessionState.AWAITING_IMPORT
```

New text:

```
        and record.state is not session.SessionState.AWAITING_IMPORT
```

### `u128-b.A6b_abandoned_counts`

Rerun of A6 after its test: count every landing record as standing

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128-b.json`, row `A6b_abandoned_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_the_intake_record_names_each_playlist_and_its_batch_folder`

Old text:

```
        if record.workflow == ingest.INTAKE_WORKFLOW and record.state in standing
```

New text:

```
        if record.workflow == ingest.INTAKE_WORKFLOW
```

### `u128-b.A8b_ambiguous_is_an_answer`

Rerun of A8 after its test: take the first of two active rows as the owned row

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128-b.json`, row `A8b_ambiguous_is_an_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_file_two_active_rows_claim_is_no_owned_row`

Old text:

```
                if matched.outcome is trees.MatchOutcome.AMBIGUOUS:
                    answer = ("", AMBIGUOUS_ROWS)
                    continue
```

New text:

```
                if matched.outcome is trees.MatchOutcome.AMBIGUOUS:
                    answer = (str(matched.content_ids[0]), "")
                    break
```

### `u128-b.A9b_emptied_left_lost`

Rerun of A9 after its test: drop the left rows of a claim left holding nothing

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128-b.json`, row `A9b_emptied_left_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_claim_left_holding_nothing_still_answers_its_left_rows`

Old text:

```
            emptied.extend((one.name, row) for row in left)
```

New text:

```
            pass
```

### `u128.A10_no_warning`

Give no left out warning however many rows were left

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A10_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 55 against a baseline of 55
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`

Old text:

```
    if not left:
        return []
    named_rows
```

New text:

```
    if True:
        return []
    named_rows
```

### `u128.A1_owned_not_mirrored`

Drop every owned member from the claim, U113's new tracks only rule

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A1_owned_not_mirrored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 55 against a baseline of 55
- Kills: 9 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_export_rewritten_after_the_gate_moves_nothing`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`
  - `tests/test_intake_land_account_playlists.py::test_the_engine_reads_the_owned_entries_again_before_the_first_move`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`

Old text:

```
            if row.paths not in seen:
                seen.add(row.paths)
                members.append(_member(row))
```

New text:

```
            if row.paths not in seen:
                seen.add(row.paths)
```

### `u128.A2_rerun_unseen`

Never read a playlist as already mirrored by this pass, so a rerun mirrors the owned tracks again

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A2_rerun_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 55 against a baseline of 55
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_rerun_of_the_same_pass_is_a_no_op`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
        rerun = source.playlist_id in again
```

New text:

```
        rerun = False
```

### `u128.A4_untied_carried_silent`

A carried row no planned file answers is silently absent rather than left

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A4_untied_carried_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 55 against a baseline of 55
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
                if not tied:
                    left.append(_left(row, NOT_BROUGHT))
```

New text:

```
                if not tied:
                    pass
```

### `u128.A7_any_pass_counts`

Read a playlist as mirrored when any pass landed it, not only this one

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A7_any_pass_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 55 against a baseline of 55
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_rerun_of_the_same_pass_is_a_no_op`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`

Old text:

```
        and entry.get(PASS_KEY) == pass_name
```

New text:

```
        and entry.get(PASS_KEY) is not None
```

### `r1255.B1_batch_name_clause`

batch_name._records: word the refusal with the old count, not the clause

- File: `src/cratekit/intake/batch_name.py`
- Source: `r1255.json`, row `B1_batch_name_clause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_intake_shelve.py`, `tests/test_inbox_rotate.py`
- Collected: 68 against a baseline of 68
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_an_unreadable_record_keeps_its_own_refusal`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[closed-detail1-<lambda>-2026-10-20 Tidal playlists 2-so no batch name can be called free]`

Old text:

```
            f"{session.unread_clause(unreadable, cfg)}, so no batch name can be called "
```

New text:

```
            f"the session log holds {len(unreadable)} entries this build cannot read, so no batch name can be called "
```

### `u113-a.A4_batch_name_not_taken`

An account playlist may take the batch's own name

- File: `src/cratekit/intake/batch_name.py`
- Source: `u113-a.json`, row `A4_batch_name_not_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_an_account_playlist_whose_dated_name_is_the_batchs_takes_two`
  - `tests/test_intake_land_account_playlists.py::test_inbox_names_counts_past_every_name_inbox_holds_and_this_landing_took`

Old text:

```
    taken = {*held, batch}
```

New text:

```
    taken = {*held}
```

### `u113-a.A5_landing_names_its_own`

Two account playlists of one name in one landing share it

- File: `src/cratekit/intake/batch_name.py`
- Source: `u113-a.json`, row `A5_landing_names_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_inbox_names_counts_past_every_name_inbox_holds_and_this_landing_took`

Old text:

```
        taken.add(candidate)
        named.append(candidate)
```

New text:

```
        named.append(candidate)
```

### `u175.N1_date_first`

dated: put the date before the account's name, the order Phillip declined

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N1_date_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 69 against a baseline of 69
- Kills: 41 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_playlist_is_inbox_slash_analyze_and_no_account_playlist_takes_its_name`
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_then_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_matches_by_name_and_an_unlisted_log_is_named_as_one`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_then_a_lost_track_is_left`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_in_account_order_and_once`
  - `tests/test_inbox_refill.py::test_two_playlists_of_the_accounts_name_are_neither_filled_and_one_is_found_by_it`
  - `tests/test_intake_land_account_playlists.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing`
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - ... and 26 more, see the JSON sidecar

Old text:

```
    return f"{account_name} {day.isoformat()}"
```

New text:

```
    return f"{day.isoformat()} {account_name}"
```

### `u175.N2_no_date`

dated: return the account's name alone, undated as before U175

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N2_no_date`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 69 against a baseline of 69
- Kills: 41 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_playlist_is_inbox_slash_analyze_and_no_account_playlist_takes_its_name`
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_then_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_matches_by_name_and_an_unlisted_log_is_named_as_one`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_then_a_lost_track_is_left`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_in_account_order_and_once`
  - `tests/test_inbox_refill.py::test_two_playlists_of_the_accounts_name_are_neither_filled_and_one_is_found_by_it`
  - `tests/test_intake_land_account_playlists.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing`
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - ... and 26 more, see the JSON sidecar

Old text:

```
    return f"{account_name} {day.isoformat()}"
```

New text:

```
    return account_name
```

### `u175.N3_date_form`

dated: write the date as the account's own month_day_year form rather than ISO

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N3_date_form`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 69 against a baseline of 69
- Kills: 41 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_playlist_is_inbox_slash_analyze_and_no_account_playlist_takes_its_name`
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_then_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_matches_by_name_and_an_unlisted_log_is_named_as_one`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_then_a_lost_track_is_left`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_in_account_order_and_once`
  - `tests/test_inbox_refill.py::test_two_playlists_of_the_accounts_name_are_neither_filled_and_one_is_found_by_it`
  - `tests/test_intake_land_account_playlists.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing`
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - ... and 26 more, see the JSON sidecar

Old text:

```
    return f"{account_name} {day.isoformat()}"
```

New text:

```
    return f"{account_name} {day.month}_{day.day:02d}_{day.year % 100:02d}"
```

### `u175.N4_clock_not_seam`

inbox_names: read the system clock rather than the landing's today seam, so the playlist's date can differ from the batch's

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N4_clock_not_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 69 against a baseline of 69
- Kills: 41 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_playlist_is_inbox_slash_analyze_and_no_account_playlist_takes_its_name`
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_then_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_matches_by_name_and_an_unlisted_log_is_named_as_one`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_then_a_lost_track_is_left`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_in_account_order_and_once`
  - `tests/test_inbox_refill.py::test_two_playlists_of_the_accounts_name_are_neither_filled_and_one_is_found_by_it`
  - `tests/test_intake_land_account_playlists.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing`
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - ... and 26 more, see the JSON sidecar

Old text:

```
    on = today()
```

New text:

```
    on = date.today()
```

### `u175.N7_held_not_held`

inbox_names: stop holding what INBOX holds, so a second landing the same day adds into the first's playlist

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N7_held_not_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 69 against a baseline of 69
- Kills: 8 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_playlist_is_inbox_slash_analyze_and_no_account_playlist_takes_its_name`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_inbox_names_counts_past_every_name_inbox_holds_and_this_landing_took`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_names_each_playlist_as_the_bridge_does`

Old text:

```
    taken = {*held, batch}
```

New text:

```
    taken = {batch}
```

### `u175.N8_counter_before_date`

inbox_names: count from the undated name, so a held name becomes Sunset Warmup 2 with no date

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N8_counter_before_date`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 69 against a baseline of 69
- Kills: 9 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_playlist_is_inbox_slash_analyze_and_no_account_playlist_takes_its_name`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_an_account_playlist_whose_dated_name_is_the_batchs_takes_two`
  - `tests/test_intake_land_account_playlists.py::test_inbox_names_counts_past_every_name_inbox_holds_and_this_landing_took`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_names_each_playlist_as_the_bridge_does`

Old text:

```
            candidate = f"{base} {count}"
        taken.add(candidate)
```

New text:

```
            candidate = f"{account_name} {count}"
        taken.add(candidate)
```

### `u175.N9_landing_not_held`

inbox_names: do not hold a name an earlier playlist of the same landing took, so two account playlists of one name share one INBOX playlist

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N9_landing_not_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_inbox_names_counts_past_every_name_inbox_holds_and_this_landing_took`

Old text:

```
            candidate = f"{base} {count}"
        taken.add(candidate)
```

New text:

```
            candidate = f"{base} {count}"
        pass
```

### `u179.N1_one_label_only_when_all_named`

bandcamp name: name the batch for its one label even when a file carries none

- File: `src/cratekit/intake/batch_name.py`
- Source: `u179.json`, row `N1_one_label_only_when_all_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_intake_land_names.py`
- Collected: 54 against a baseline of 54
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_batch_of_a_label_and_an_unregistered_seller_files_by_tag_under_a_plain_name`
  - `tests/test_sync_bandcamp.py::test_a_file_whose_tags_cannot_be_read_is_unread_not_ungenred_and_names_no_label`
  - `tests/test_sync_bandcamp.py::test_the_batch_name_is_the_one_label_every_file_names_or_plain[labels3-Bandcamp]`

Old text:

```
    if len(named) == 1 and not unnamed:
```

New text:

```
    if len(named) == 1:
```

### `r1499.B01_pass_suffix`

pass_of: any download list's name is a sync pass

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B01_pass_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_only_a_download_over_a_synced_list_is_a_passes`

Old text:

```
    if name == listed or not name.endswith(SYNCED_SUFFIX):
```

New text:

```
    if name == listed:
```

### `r1499.B02_pass_handler`

pass_of: any handler's job over a list is a pass's download

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B02_pass_handler`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_passes_own_downloads_are_this_librarys_over_its_own_list_by_name`
  - `tests/test_sync_land_beside.py::test_only_a_download_over_a_synced_list_is_a_passes`

Old text:

```
    if job.handler_key != DOWNLOAD_KEY:
        return None
```

New text:

```
    if False:
        return None
```

### `r1499.B03_pass_step`

Waiting.step: a sync pass's download is named as a plain one, with no continue command

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B03_pass_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_fresh_go_beside_a_sync_passes_download_names_its_continue_command`
  - `tests/test_sync_land_beside.py::test_an_earlier_pass_renamed_at_its_gate_is_named_by_its_pass`
  - `tests/test_sync_land_beside.py::test_an_earlier_passes_unlanded_download_refuses_a_new_pass_naming_how_it_lands`
  - `tests/test_sync_land_staged.py::test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_an_unlanded_first_refuses_before_any_download_is_refused`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses`

Old text:

```
        if self.pass_name is not None and self.pass_run is not None:
```

New text:

```
        if False:
```

### `r1499.B04_pass_maybe_renamed`

beside: a sync pass whose tail may have renamed files no download names is never named

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B04_pass_maybe_renamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_earlier_pass_renamed_at_its_gate_is_named_by_its_pass`

Old text:

```
            name = pass_of(job) if run is None else None
```

New text:

```
            name = None
```

### `r1499.B05_arrived_items`

arrived: a new finished item of another download is not read

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B05_arrived_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_a_gos_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_gos_tail_that_fails_while_a_download_arrives_says_its_record_was_not_kept`

Old text:

```
    new = sorted({job_id for job_id, _item in after.items - before.items})
```

New text:

```
    new = []
```

### `r1499.B06_arrived_count`

arrived: a change in the count of files a landing takes is not read

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B06_arrived_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_a_person_put_there_while_the_tail_ran_refuses_its_landing`

Old text:

```
    if not new and after.count == before.count:
        return None
```

New text:

```
    if not new:
        return None
```

### `r1499.B08_kept_identity`

beside (sample of the lifted guards): files no download names are all read as own when a record exists

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B08_kept_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_ran_still_refuses_a_file_more_than_its_own_renamed`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_left_reads_no_file_put_there_since_as_its_own`
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_file_the_passes_tail_left_and_then_changed_is_not_its_own`

Old text:

```
        unnamed = [path for path in unnamed if identity(path) not in kept]
```

New text:

```
        unnamed = []
```

### `r1499.B09_unlistable`

beside (sample of the lifted guards): an unlistable folder reads as empty

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B09_unlistable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_staging_folder_that_cannot_be_listed_refuses_rather_than_hold_nothing`

Old text:

```
    except OSError as exc:
        raise refuse(
            "intake-list-unusable",
            f"the staging folder {folder} could not be listed ({exc}), so whether it "
```

New text:

```
    except OSError:
        held = set()
    if False:
        raise refuse(
            "intake-list-unusable",
            f"the staging folder {folder} could not be listed, so whether it "
```

### `r1499.B10_plain_step_moves_out`

Waiting.step: a plain download's step says to land it in place, which lands the batch with it

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B10_plain_step_moves_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_plain_download_in_the_folder_refuses_a_fresh_go_before_the_gate`
  - `tests/test_sync_land_beside.py::test_a_plain_download_beside_the_pass_refuses_naming_it`

Old text:

```
f"move the tracks of job {self.job_id} out of {folder}, and land them on "
```

New text:

```
f"land the tracks of job {self.job_id} in {folder}, and land them on "
```

### `r1264.M22_readable_dates`

list_playlist_readable: give no added dates, so a pair's later change calls read every time as unknown

- File: `src/cratekit/intake/cli.py`
- Source: `r1264.json`, row `M22_readable_dates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_merge.py`
- Collected: 190 against a baseline of 190
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
        dates=_added_dates(rows, tracks),
```

New text:

```
        dates={},
```

### `r1295.M16_set_aside_one_word`

set_aside: always names the title as the absent half, so an artistless track is misnamed

- File: `src/cratekit/intake/cli.py`
- Source: `r1295.json`, row `M16_set_aside_one_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/intake/test_workers.py`, `tests/test_sync_all.py`
- Collected: 221 against a baseline of 221
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

### `u113-a.A7_payload_drops_name`

queue_playlist is handed the name and records nothing

- File: `src/cratekit/intake/cli.py`
- Source: `u113-a.json`, row `A7_payload_drops_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 42 against a baseline of 42
- Kills: 32 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing`
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists.py::test_a_rerun_of_the_same_pass_is_a_no_op`
  - `tests/test_intake_land_account_playlists.py::test_a_row_that_only_resembles_a_file_does_not_claim_it`
  - `tests/test_intake_land_account_playlists.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists.py::test_an_account_playlist_whose_dated_name_is_the_batchs_takes_two`
  - `tests/test_intake_land_account_playlists.py::test_an_answer_given_for_one_split_is_stale_for_another`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_export_rewritten_after_the_gate_moves_nothing`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`
  - `tests/test_intake_land_account_playlists.py::test_sync_all_records_the_name_the_account_listed_on_each_playlist_job`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    if name:
        payload[PLAYLIST_NAME] = name
```

New text:

```
    if name and False:
        payload[PLAYLIST_NAME] = name
```

### `u129-author.A3_abort_still_writes`

Apply the account playlist even when the gate said abort

- File: `src/cratekit/intake/cli.py`
- Source: `u129-author.json`, row `A3_abort_still_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_an_abort_on_the_account_gate_queues_the_set_and_writes_no_playlist`

Old text:

```
    if option != "apply" or not built.writes:
        return notes, built.payload

```

New text:

```
    if not built.writes:
        return notes, built.payload

```

### `u213.M11_unreadable_said_isrc`

Unreadable.said: name the track with no ISRC, so the backfill cannot find it by its code

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M11_unreadable_said_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
        return {"artist": self.artist, "title": self.title, "isrc": self.isrc}
```

New text:

```
        return {"artist": self.artist, "title": self.title, "isrc": ""}
```

### `u213.M13_unidentified_any`

_refuse_unidentified: refuse only when more than one row carries no id

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M13_unidentified_any`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_hearts_listing_that_fails_refuses_and_queues_nothing[no-id-by-position]`
  - `tests/intake/test_workers.py::test_a_row_the_reader_refuses_refuses_the_playlist_and_queues_nothing[no-identifier-by-position]`
  - `tests/test_sync_twins.py::test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned`

Old text:

```
    if missing:
        raise _unusable(
```

New text:

```
    if len(missing) > 1:
        raise _unusable(
```

### `u213.M6_readable_refuses_nameless`

list_playlist_readable: drop the refusal of a row carrying no provider id, so it is silently dropped from the listing

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M6_readable_refuses_nameless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_sync_twins.py::test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned`

Old text:

```
    _refuse_unidentified(nameless)
    tracks = frozen_rows(tuple(read))
```

New text:

```
    tracks = frozen_rows(tuple(read))
```

### `u213.M9_readable_order_holds_unread`

list_playlist_readable: order only the tracks that read, so a twin's snapshot drops the unread track

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M9_readable_order_holds_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
        order.setdefault(ref, None)
        try:
            read.append(match.read_row(row, origin=match.TIDAL, position=position))
```

New text:

```
        try:
            read.append(match.read_row(row, origin=match.TIDAL, position=position))
            order.setdefault(ref, None)
```

### `u249.M21_intake_reset_leaves_reader`

intake.cli.reset_cache: clear the drive's view and leave the reader's memory

- File: `src/cratekit/intake/cli.py`
- Source: `u249.json`, row `M21_intake_reset_leaves_reader`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_sync_unmark.py`, `tests/intake/test_workers.py`
- Collected: 128 against a baseline of 128
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[intake]`

Old text:

```
    _RESOLVED.clear()
    match.reset_cache()
```

New text:

```
    _RESOLVED.clear()
```

### `r740-b.E2_average_bpm_nonzero`

existing guard sample: the intake row's AverageBpm literal becomes a tempo

- File: `src/cratekit/intake/collection_xml.py`
- Source: `r740-b.json`, row `E2_average_bpm_nonzero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_collection_xml.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 113 against a baseline of 113
- Kills: 16 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_average_bpm_is_gridless_inizio_no_tempo_child_and_the_bytes_crlf`
  - `tests/intake/test_pipeline.py::test_single_file_ingest_uses_no_network`
  - `tests/test_landing_head.py::test_a_second_landing_of_the_same_file_renders_the_same_name`
  - `tests/test_landing_head.py::test_a_title_analyze_run_measured_lands_as_its_title_tag_gives_it_with_no_head[a-provider-key-tag]`
  - `tests/test_landing_head.py::test_a_title_analyze_run_measured_lands_as_its_title_tag_gives_it_with_no_head[no-title-tag]`
  - `tests/test_landing_head.py::test_a_title_analyze_run_measured_lands_as_its_title_tag_gives_it_with_no_head[titled]`
  - `tests/test_landing_head.py::test_intake_file_names_its_track_from_the_same_head`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[01A - 112 - Ain't Gonna Hurt Nobody.flac-fields0-01A - 112 - Ain't Gonna Hurt Nobody-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields4-05B - 98 - Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields5-05B - 98 - Body-8A]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[08A - 124 - [MP3] Body.flac-fields8-08A - 124 - [MP3] Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body [MP3].flac-fields7-Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields1-08A - 124 - Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields2-08A - 124 - Body-3B]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields3-08A - 124 - Body-Am]`
  - ... and 1 more, see the JSON sidecar

Old text:

```
Year="0" AverageBpm="0.00"
```

New text:

```
Year="0" AverageBpm="112.00"
```

### `r770-d.S1_composite_the_splice_takes_a_stub`

COMPOSITE for r770-a's S1, which was a zero: collection_xml.splice_tracks does not refuse a U22 stub listing, with place_files' own refusal left in place. The driver pairs only inside one batch, so the pairing is recorded in r770-notes.md

- File: `src/cratekit/intake/collection_xml.py`
- Source: `r770-d.json`, row `S1_composite_the_splice_takes_a_stub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_landing.py`, `tests/test_intake_imported.py`, `tests/intake/test_collection_xml.py`
- Collected: 85 against a baseline of 85
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_a_u22_stub_listing_is_not_a_splice_target`
  - `tests/test_landing.py::test_an_export_that_cannot_be_spliced_is_refused_before_any_move[stub]`

Old text:

```
    if is_stub_listing(raw):
```

New text:

```
    if False:
```

### `u37-author-light.G1_stub_listing`

Treat a U22 stub listing as a spliceable Fresh Export

- File: `src/cratekit/intake/collection_xml.py`
- Source: `u37-author-light.json`, row `G1_stub_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_a_u22_stub_listing_is_not_a_splice_target`

Old text:

```
    if is_stub_listing(raw):
        raise refuse(
            "intake-export-is-stub",
```

New text:

```
    if False and is_stub_listing(raw):
        raise refuse(
            "intake-export-is-stub",
```

### `u37-author-light.G3_gridless_bpm`

Write a real AverageBpm instead of the gridless constant

- File: `src/cratekit/intake/collection_xml.py`
- Source: `u37-author-light.json`, row `G3_gridless_bpm`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_average_bpm_is_gridless_inizio_no_tempo_child_and_the_bytes_crlf`

Old text:

```
Year="0" AverageBpm="0.00"
```

New text:

```
Year="0" AverageBpm="124.00"
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

### `r1950.C02_file_landed_compares_second_entry`

intake filing: file_landed keys every entry by content id, so a two genre track is compared against its second folder and reported filed differently

- File: `src/cratekit/intake/filing.py`
- Source: `r1950.json`, row `C02_file_landed_compares_second_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre_guards_counts.py`, `tests/test_intake_land_filing.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre_guards_counts.py::test_a_landed_two_genre_track_files_as_its_first_folder_predicts`

Old text:

```
found = {entry.content_id: entry for entry in plan.firsts()}
```

New text:

```
found = {entry.content_id: entry for entry in plan.entries}
```

### `u165.F5_report_failed`

file_landed: report a filing whose entries failed as filed

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F5_report_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 23223 against a baseline of 23223
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if report.failed:
        return Filed(
            state=NOT_FILED,
```

New text:

```
    if False:
        return Filed(
            state=NOT_FILED,
```

### `r773-b.P1_proof_granted_whatever_the_export_names`

settle, existing: find no landed track missing, so any export proves any import

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r773-b.json`, row `P1_proof_granted_whatever_the_export_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_intake_imported.py`
- Collected: 128 against a baseline of 128
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_against_an_export_taken_before_the_import`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`

Old text:

```
    missing = [entry for entry in landed if entry.track not in held]
```

New text:

```
    missing = []
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
- Collected: 89 against a baseline of 89
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
- Collected: 89 against a baseline of 89
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
- Collected: 89 against a baseline of 89
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
- Collected: 89 against a baseline of 89
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
- Collected: 89 against a baseline of 89
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
- Collected: 204 against a baseline of 204
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
- Collected: 204 against a baseline of 204
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

### `r1056.F1_no_fold`

years_filed: compare the label unfolded, so a decomposed spelling is another label

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F1_no_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_label_spelled_decomposed_on_either_side_is_the_same_label`

Old text:

```
        if _folded(named) == wanted and tracks > 0:
```

New text:

```
        if named == label and tracks > 0:
```

### `r1056.F2_empty_year_counts`

years_filed: count a year whose entry held no track

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F2_empty_year_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_year_filed_under_another_label_or_holding_no_track_is_not_marked`

Old text:

```
        if _folded(named) == wanted and tracks > 0:
```

New text:

```
        if _folded(named) == wanted and tracks >= 0:
```

### `r1056.F3_any_label_counts`

years_filed: count a year filed under any label

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F3_any_label_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_label_batch_landed_natively_with_a_manifest_is_marked_by_its_pass`
  - `tests/test_label_mark_native.py::test_a_label_is_compared_exactly_otherwise`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[another-label]`
  - `tests/test_label_mark_native.py::test_a_year_filed_under_another_label_or_holding_no_track_is_not_marked`

Old text:

```
        if _folded(named) == wanted and tracks > 0:
```

New text:

```
        if tracks > 0:
```

### `r1056.F4_non_list_read_as_empty`

years_filed: read a labels value that is not a list as nothing filed

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F4_non_list_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-string]`

Old text:

```
    if not isinstance(filed, list):
        return None
```

New text:

```
    if not isinstance(filed, list):
        return frozenset()
```

### `r1056.F5_non_dict_entry_skipped`

years_filed: skip an entry that is not a mapping rather than refuse the record

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F5_non_dict_entry_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-list-of-strings]`

Old text:

```
        if not isinstance(entry, dict):
            return None
```

New text:

```
        if not isinstance(entry, dict):
            continue
```

### `r1056.F6_text_year_accepted`

years_filed: accept any year value, so a text year is read rather than refused

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F6_text_year_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-bool-year]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-text-year]`

Old text:

```
            or not isinstance(year, int)
            or isinstance(year, bool)
```

New text:

```
            or year is None
```

### `r1056.F7_bool_tracks_accepted`

years_filed: accept a boolean track count

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F7_bool_tracks_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-bool-tracks]`

Old text:

```
            or not isinstance(tracks, int)
            or isinstance(tracks, bool)
```

New text:

```
            or not isinstance(tracks, int)
```

### `r1056.F8_no_zero_pad`

years_filed: spell a year unpadded, unlike the ledger

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F8_no_zero_pad`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_year_is_four_digits_as_the_ledger_spells_it`

Old text:

```
            years.add(f"{year:04d}")
```

New text:

```
            years.add(str(year))
```

### `r1467.M19_root_unreadable_refuses`

pass_landed: read a library root that cannot be read as a pass that never landed

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M19_root_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_an_unreadable_library_root_refuses_rather_than_read_the_pass_as_landed`

Old text:

```
    except OSError as exc:
        raise refuse(
            "library-root-unreachable",
```

New text:

```
    except OSError as exc:
        return False
        raise refuse(
            "library-root-unreachable",
```

### `r1467.M20_retired_file_proves`

pass_landed: read only a pending intake file, so a retired one proves nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M20_retired_file_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_retired_intake_file_proves_the_pass`

Old text:

```
            if unretired_name(entry.name) == wanted and entry.is_file():
```

New text:

```
            if entry.name == wanted and entry.is_file():
```

### `r1467.M21_native_record_proves`

pass_landed: never read the native landing's record

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M21_native_record_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_track_no_download_names_refuses_the_fresh_go_and_only_an_unproven_go_is_named[native]`

Old text:

```
    return bool(native.landings_of_pass(cfg, name))
```

New text:

```
    return False
```

### `r1467.M22_proof_is_a_file`

pass_landed: a directory named as the intake file proves the pass

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M22_proof_is_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_landing_proof_of_another_pass_proves_nothing`

Old text:

```
            if unretired_name(entry.name) == wanted and entry.is_file():
```

New text:

```
            if unretired_name(entry.name) == wanted:
```

### `r677-b.V4_after_the_stale_test`

any gate refusal, a stale answer included, is replaced by the preflight refusal

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677-b.json`, row `V4_after_the_stale_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`

Old text:

```
        if unusable is not None and exc.cause.remediation.remedy is Remedy.ANSWER_DECISION:
```

New text:

```
        if unusable is not None:
```

### `r677.V1_no_preflight_before_the_gate`

the original defect: the plan read never asks the engine, so a missing export reaches the gate

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V1_no_preflight_before_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_absent-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_no_intake_folder-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_not_a_collection-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
    if planned.items:
        try:
```

New text:

```
    if False:
        try:
```

### `r677.V2_preflight_on_a_plan_of_nothing`

an empty staging folder is refused over the export instead of shown as a plan of nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V2_preflight_on_a_plan_of_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`

Old text:

```
    if planned.items:
        try:
```

New text:

```
    if True:
        try:
```

### `r677.V3_refusal_never_replaces_the_gate`

the preflight refusal is caught and dropped, so the gate is offered over an unusable export

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V3_refusal_never_replaces_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_absent-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_no_intake_folder-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_not_a_collection-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`

Old text:

```
        if unusable is not None and exc.cause.remediation.remedy is Remedy.ANSWER_DECISION:
            raise unusable from None
```

New text:

```
        if False:
            raise unusable from None
```

### `r677.V5_preflight_raises_directly`

the preflight refusal is raised at once, so a recorded abort over a missing export refuses instead of ending in nothing done

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V5_preflight_raises_directly`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_what_went_missing`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`

Old text:

```
        except CratekitError as exc:
            unusable = exc
```

New text:

```
        except CratekitError as exc:
            raise exc
```

### `r677.V6_manifest_rows_not_handed_over`

the plan read asks the export check without the manifest's label rows, so a label layout the export cannot take reaches the gate

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V6_manifest_rows_not_handed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`

Old text:

```
                label_rows=manifest.rows if manifest is not None else (),
```

New text:

```
                label_rows=(),
```

### `u110-b.B2_name_names_file`

--name alone no longer names the intake file, breaking a landing typed the old way

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B2_name_names_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
- Kills: 18 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    if name is not None:
        return name
    return default_name
```

New text:

```
    return default_name
```

### `u110-b.B7_name_overrides`

--name is ignored and the default name is always taken

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B7_name_overrides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
- Kills: 27 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_refused_file_is_warned_and_marked`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_every_target_taken]`
  - `tests/test_intake_land_names.py::test_name_and_pass_together_name_the_batch_and_the_file_apart`
  - `tests/test_intake_land_names.py::test_name_overrides_and_names_the_intake_file_when_no_pass_is_given`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - ... and 12 more, see the JSON sidecar

Old text:

```
        ctx.args.name
        if ctx.args.name is not None
        else batch_name.readable(
```

New text:

```
        batch_name.readable(
```

### `u113-b.B7_digest_blind_to_split`

The xml gate's digest does not cover the split, so an answer given for one carries out another

- File: `src/cratekit/intake/land_cli.py`
- Source: `u113-b.json`, row `B7_digest_blind_to_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_an_answer_given_for_one_split_is_stale_for_another`
  - `tests/test_intake_land_account_playlists.py::test_an_export_rewritten_after_the_gate_moves_nothing`

Old text:

```
        identity["playlists"] = [claimed.identity() for claimed in split]
```

New text:

```
        pass
```

### `u113-b.B8_pending_names_unheld`

Names an intake file still waiting on its import holds are not held

- File: `src/cratekit/intake/land_cli.py`
- Source: `u113-b.json`, row `B8_pending_names_unheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`

Old text:

```
    taken = (*(held if isinstance(held, tuple) else ()), *account_playlists.pending_names(cfg))
```

New text:

```
    taken = held if isinstance(held, tuple) else ()
```

### `u121-b.S20r_bridge_set`

intake_land: --set on a bridge tree is not refused, the batch lands with no playlist

- File: `src/cratekit/intake/land_cli.py`
- Source: `u121-b.json`, row `S20r_bridge_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_on_the_bridge_given_set_is_refused_by_name_before_anything_moves`

Old text:

```
    if ctx.args.set_job:
        set_playlist.assert_native(medium, landing=True)
```

New text:

```
    if False:
        set_playlist.assert_native(medium, landing=True)
```

### `u127.L6_bridge_ignores_calibration`

The bridge names the vocals verb as owed on an uncalibrated library

- File: `src/cratekit/intake/land_cli.py`
- Source: `u127.json`, row `L6_bridge_ignores_calibration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
    if cut is None:
        return f"{BRIDGE_VOX_NONE}, and {native.VOX_UNCALIBRATED}"
```

New text:

```
    if False:
        return f"{BRIDGE_VOX_NONE}, and {native.VOX_UNCALIBRATED}"
```

### `u128-b.B3_owned_unresolved_at_gate`

The bridge verb does not find the owned tracks in the export before the gate

- File: `src/cratekit/intake/land_cli.py`
- Source: `u128-b.json`, row `B3_owned_unresolved_at_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists.py::test_a_rerun_of_the_same_pass_is_a_no_op`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`

Old text:

```
    split, emptied = landing.owned_in_export(cfg, split, export)
```

New text:

```
    emptied = ()
```

