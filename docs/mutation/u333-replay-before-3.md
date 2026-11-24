# Mutation table: u333-replay-before-3

Measured by `scripts/mutate.py` on 2026-11-24 05:15 UTC, branch `HEAD` at `35e9a825`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 435.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 05:15 UTC for commit `35e9a825cd73`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 56, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u185.R5_taxonomy_refusal` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 31 | 1 | killed |
| `u244.M24_upgrade_keeps_a_held_table` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 417 | 1 | killed |
| `u331.S14_upgrade_loads_the_taxonomy_loader_at_top` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 161 | 1 | killed |
| `r431-a.A1_a_plain_row_gains_a_companion` | `src/cratekit/core/tombstone.py` | user | 1 file(s) | 331 | 11 | killed |
| `r235-a.M11_session_lock_dropped` | `src/cratekit/core/tree_registry.py` | user | 1 file(s) | 26 | 1 | killed |
| `r235-a.M12_second_record_replaces` | `src/cratekit/core/tree_registry.py` | user | 1 file(s) | 26 | 1 | killed |
| `r235-a.M13_snapshot_check_dropped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 11 | killed |
| `r235-a.M1_unreadable_log_skipped` | `src/cratekit/core/tree_registry.py` | user | 1 file(s) | 26 | 2 | killed |
| `r235-a.M2_margin_zero` | `src/cratekit/core/tree_registry.py` | user | 1 file(s) | 26 | 1 | killed |
| `r235-a.M3_margin_two_days` | `src/cratekit/core/tree_registry.py` | user | 1 file(s) | 26 | 1 | killed |
| `r235-a.M4_unparseable_start_predates` | `src/cratekit/core/tree_registry.py` | user | 1 file(s) | 26 | 1 | killed |
| `r235-a.M5_updates_not_counted` | `src/cratekit/core/tree_registry.py` | user | 1 file(s) | 26 | 1 | killed |
| `r235-a.M6_any_tree_counts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M7_zero_count_counts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M8_open_run_reverts` | `src/cratekit/core/tree_registry.py` | user | 1 file(s) | 26 | 1 | killed |
| `r235-a.M9_library_guard_removed` | `src/cratekit/core/tree_registry.py` | user | 1 file(s) | 26 | 4 | killed |
| `r235-b.M14_empty_export_accepted` | `src/cratekit/core/tree_registry.py` | user | 1 file(s) | 40 | 1 | killed |
| `r501-a.T1_precheck_excusal` | `src/cratekit/core/tree_registry.py` | user | 1 file(s) | 34 | 4 | killed |
| `r787.S1_set_drops_intake` | `src/cratekit/core/tree_registry.py` | user | 1 file(s) | 40 | 7 | killed |
| `u953.M2_registry_cause_remedy_fixed` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 115 | 2 | killed |
| `u243.D10_prefix_order_fewest_first` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 22 | 1 | killed |
| `u243.D11_refusal_names_no_prefix` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 22 | 3 | killed |
| `u243.D12_refusal_offers_no_rule` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 2 | killed |
| `u243.D1_id_class_takes_a_dot` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 22 | 2 | killed |
| `u243.D2_end_anchor_is_dollar` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 22 | 1 | killed |
| `u243.D3_no_end_anchor` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 22 | 4 | killed |
| `u243.D4_search_not_match` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 22 | 1 | killed |
| `u243.D5_spelling_not_asked` | `src/cratekit/deletion/candidates.py` | user | 2 file(s) | 353 | 17 | killed |
| `u243.D6_disk_not_asked` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 22 | 5 | killed |
| `u243.D7_an_error_reads_as_absent` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 22 | 3 | killed |
| `u243.D8_something_there_reads_as_absent` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 22 | 1 | killed |
| `u243.D9_streaming_still_counted_unmapped` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 22 | 3 | killed |
| `u310.P1_identifiable` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 331 | 3 | killed |
| `u310.P2_declined` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 331 | 4 | killed |
| `u310.P3_ambiguous_version` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 331 | 3 | killed |
| `u310.P4_collides_with_active_row` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 331 | 5 | killed |
| `u310.P5_size_matches` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 331 | 2 | killed |
| `u310.P6_still_referenced` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 331 | 4 | killed |
| `u310.P7_anchor_moved_mid_walk` | `src/cratekit/deletion/candidates.py` | user | 1 file(s) | 331 | 1 | killed |
| `r1844.N17_screen_silent` | `src/cratekit/deletion/cli.py` | user | 1 file(s) | 42 | 6 | killed |
| `u243.D14_screen_never_says_ignored` | `src/cratekit/deletion/cli.py` | user | 2 file(s) | 353 | 2 | killed |
| `u310.G1_abort_moves_nothing` | `src/cratekit/deletion/cli.py` | user | 1 file(s) | 331 | 2 | killed |
| `u310.G3_recorded_reject_honoured` | `src/cratekit/deletion/cli.py` | user | 1 file(s) | 331 | 1 | killed |
| `r1037.M1_identity_unchecked` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 1 | killed |
| `r1037.M7_earlier_landing_kept` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 1 | killed |
| `r1037.M8_playlist_ids_live_only` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 9 | killed |
| `r1844.N10_numbered_ignored` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 2 | killed |
| `r1844.N11_marked_uuid_unread` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 2 | killed |
| `r1844.N12_record_uuid_unread` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 5 | killed |
| `r1844.N1_uuid_proof_dropped` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 5 | killed |
| `r1844.N2_id_alone_proves` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 3 | killed |
| `r1844.N3_empty_uuid_proves` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 1 | killed |
| `r1844.N4_playlist_proof_dropped` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 11 | killed |
| `r1844.N5_any_playlist_proves` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 1 | killed |
| `r1844.N6_no_playlist_proves` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 5 | killed |
| `r1844.N7_held_rows_read_absent` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 33 | killed |
| `r1844.N8_nothing_absent_listed` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 1 | killed |
| `r1844.N9_rolled_back_unlisted` | `src/cratekit/deletion/library.py` | user | 1 file(s) | 42 | 7 | killed |
| `r1037.M10_landed_not_joined` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 42 | 14 | killed |
| `r1037.M11_sightings_never_forgotten` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 42 | 1 | killed |
| `r1037.M12_playlists_always_held` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 42 | 8 | killed |
| `r1037.M9_recorded_not_excluded` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 42 | 1 | killed |
| `r1844.N14_uuids_not_passed` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 42 | 4 | killed |
| `r1844.N15_baseline_count_lost` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 42 | 1 | killed |
| `r1844.N16_review_count_lost` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 42 | 5 | killed |
| `r44-b.R1_rules_drop_identity` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `r44-b.R2_no_gate_at_the_plan` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 4 | killed |
| `r44-b.R3_no_look_at_the_loop_top` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 2 | killed |
| `r44-b.R4_no_look_after_the_recheck` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `r44-b.R5_both_looks_gone` | `src/cratekit/deletion/run.py` | maintainer | 1 file(s) | 331 | 4 | killed |
| `r44-b.X1_library_root_gate` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `r44-b.X2_suspect_anchor` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 2 | killed |
| `u310.A10_unrecorded_move_put_back` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 5 | killed |
| `u310.A11_unproved_anchor_retires_nothing` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `u310.A12_only_answered_items_move` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `u310.A13_fresh_playlist_read` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 2 | killed |
| `u310.A14_reference_set_complete` | `src/cratekit/deletion/run.py` | user | 2 file(s) | 353 | 2 | killed |
| `u310.A1_gates_asserted` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `u310.A2_volume_before_the_answer` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 2 | killed |
| `u310.A3_reject_moves_nothing` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 4 | killed |
| `u310.A4_planned_deletable` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `u310.A5_fresh_decline_snapshot` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `u310.A7_recheck_still_deletable` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `u310.A8_shown_path_is_the_moved_path` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 2 | killed |
| `u310.A9_volume_refusal_stops_the_run` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `u27-reports-round-3-fixes.F4_absent_flag_never_set` | `src/cratekit/deletion/trash.py` | user | 1 file(s) | 417 | 1 | killed |
| `u310.T1_trash_usable` | `src/cratekit/deletion/trash.py` | user | 1 file(s) | 331 | 2 | killed |
| `r1037.M13_sight_renumbers` | `src/cratekit/deletion/watermark.py` | user | 1 file(s) | 42 | 3 | killed |
| `r1037.M14_sight_at_the_watermark` | `src/cratekit/deletion/watermark.py` | user | 1 file(s) | 42 | 15 | killed |
| `r1037.M15_sight_keeps_held` | `src/cratekit/deletion/watermark.py` | user | 1 file(s) | 42 | 2 | killed |
| `r1037.M16_advance_drops_sightings` | `src/cratekit/deletion/watermark.py` | user | 1 file(s) | 42 | 2 | killed |
| `r1037.M17_sightings_unchecked` | `src/cratekit/deletion/watermark.py` | user | 1 file(s) | 42 | 1 | killed |
| `r1037.M18_sighting_value_unchecked` | `src/cratekit/deletion/watermark.py` | user | 1 file(s) | 42 | 1 | killed |
| `r1037.M19_version_two_refused` | `src/cratekit/deletion/watermark.py` | user | 2 file(s) | 373 | 111 | killed |
| `u270.C1_export_names_its_batch_form` | `src/cratekit/export/cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `u51-item-derivation.H3_frozen_config_ignored` | `src/cratekit/export/cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `u142.S8_gate_stale_said_without_a_write` | `src/cratekit/export/set_archive.py` | user | 1 file(s) | 63 | 1 | killed |
| `r837-b.B5_unmatched_warning` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 63 | 2 | killed |
| `u309-z.U14_backfill_abort_writes_nothing` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 63 | 1 | killed |
| `u309-z.U15_backfill_skips_planless` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 63 | 1 | killed |
| `u309-z.U16_backfill_names_only_what_wrote` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 63 | 1 | killed |
| `u309-z.U17_backfill_first_failure_raised_as_is` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 63 | 1 | killed |
| `u140.B10_queued_day_name_dropped` | `src/cratekit/export/set_common.py` | user | 1 file(s) | 29 | 2 | killed |
| `r572.Z1_set_drop_album` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 1 | killed |
| `r837-b.B1_ref_only_from_the_provider` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 1 | killed |
| `r837-b.B2_isrc_route` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 1 | killed |
| `r837-b.B3_accepted_in_review` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 2 | killed |
| `r837-b.B4_sole_exact_listed` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 20 | killed |
| `r879-b.S10_unnamed_exact_said_to_resemble_nothing` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 1 | killed |
| `r879-b.S4_several_codes_take_one` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 1 | killed |
| `r879-b.S5_codes_from_every_version` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 1 | killed |
| `r879-b.S6_absent_music_folder_unsaid` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 1 | killed |
| `r879-b.S7_library_before_a_persons_answer` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 1 | killed |
| `r879-b.S8_several_needs_three` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 2 | killed |
| `r879-b.S9_ambiguous_full_said_as_bound` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 1 | killed |
| `r1017.M12_twin_message_names_to` | `src/cratekit/export/set_rename.py` | user | 1 file(s) | 29 | 1 | killed |
| `r1017.M1_no_recorded_names` | `src/cratekit/export/set_rename.py` | user | 1 file(s) | 29 | 5 | killed |
| `r1017.M2_recorded_before_frozen` | `src/cratekit/export/set_rename.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B6_mark_refusal_dropped` | `src/cratekit/export/set_rename.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B7_twin_refusal_dropped` | `src/cratekit/export/set_rename.py` | user | 1 file(s) | 29 | 4 | killed |
| `u140.B8_flag_conflict_dropped` | `src/cratekit/export/set_rename.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B9_abort_applies` | `src/cratekit/export/set_rename.py` | user | 1 file(s) | 29 | 1 | killed |
| `u146-a.B10_job_no_date_dated_by_account` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u146-a.B11_listing_always_asked` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 3 | killed |
| `u146-a.B12_landing_takes_keyless_rows` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 12 | 1 | killed |
| `u146-a.B1_carried_states` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 7 | killed |
| `u146-a.B3_already_ignores_filed` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 3 | killed |
| `u146-a.B4_already_ignores_source` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u146-a.B5_removed_counts_a_live_row` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u146-a.B9_whole_and_short_swapped` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 4 | killed |
| `u146-b.B13_first_of_two_rows` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 12 | 1 | killed |
| `u146-b.B14_plan_owned_keeps_held_hearts` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 12 | 1 | killed |
| `u153.B1_read_back_grey` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 21 | killed |
| `u153.B2_record_colour_only` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `u153.B3_member_order_isdigit` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 31 | 1 | killed |
| `r228-operator.D11_non_pink_outside` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 4 | killed |
| `r228-operator.D12_missing_pink_queued` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 2 | killed |
| `r228-operator.D4_union_playlist_first` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `r228-operator.D5_pink_missing_dropped` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 2 | killed |
| `r228-operator.D6_empty_after_colour` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `r228-operator.D7_colour_unread_warned` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `r228-operator.D8_from_colour_zero` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 5 | killed |
| `r228-operator.D9_from_playlist_zero` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 4 | killed |
| `u153.C1_is_uncoloured_narrowed` | `src/cratekit/favorites/colour.py` | user | 2 file(s) | 98 | 2 | killed |
| `u153.C2_sort_rows_dedup` | `src/cratekit/favorites/colour.py` | user | 1 file(s) | 67 | 1 | killed |
| `u153.C3_sort_rows_missing_row` | `src/cratekit/favorites/colour.py` | user | 1 file(s) | 67 | 1 | killed |
| `u153.C4_sort_rows_uncoloured_branch` | `src/cratekit/favorites/colour.py` | user | 2 file(s) | 98 | 10 | killed |
| `u153.C6_write_pink_fill_only` | `src/cratekit/favorites/colour.py` | user | 1 file(s) | 67 | 2 | killed |
| `u153.C7_write_pink_reports_write` | `src/cratekit/favorites/colour.py` | user | 2 file(s) | 98 | 5 | killed |
| `u180.M14_root_refused` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 35 | 1 | killed |
| `u180.M15_digest_is_the_target_order` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 35 | 1 | killed |
| `u180.M17_confined_seated_position` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 35 | 1 | killed |
| `u180.M18_confined_unplanned_rows` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 35 | 2 | killed |
| `u180.M19_confined_memberships` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 35 | 1 | killed |
| `u180.M21_confinement_called` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 35 | 1 | killed |
| `u180.M22_read_back_compares` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 35 | 1 | killed |
| `u120.T2_naive_is_utc` | `src/cratekit/favorites/placeholders.py` | user | 1 file(s) | 67 | 1 | killed |
| `u145.M1_month_off_by_one` | `src/cratekit/favorites/placeholders.py` | user | 3 file(s) | 113 | 33 | killed |
| `u146-b.B16_undated_is_no_filing` | `src/cratekit/favorites/placeholders.py` | user | 1 file(s) | 31 | 1 | killed |
| `u146-e.B17_month_label_wrong` | `src/cratekit/favorites/placeholders.py` | user | 1 file(s) | 31 | 5 | killed |
| `u180.M1_source_first` | `src/cratekit/favorites/placeholders.py` | user | 2 file(s) | 102 | 11 | killed |
| `u180.M2_newest_first_sign` | `src/cratekit/favorites/placeholders.py` | user | 2 file(s) | 102 | 18 | killed |
| `u180.M3_year_coefficient` | `src/cratekit/favorites/placeholders.py` | user | 2 file(s) | 102 | 3 | killed |
| `u180.M4_month_must_be_plain` | `src/cratekit/favorites/placeholders.py` | user | 2 file(s) | 102 | 2 | killed |
| `u180.M5_undated_rank` | `src/cratekit/favorites/placeholders.py` | user | 2 file(s) | 102 | 2 | killed |
| `u180.M6_undated_after_others` | `src/cratekit/favorites/placeholders.py` | user | 1 file(s) | 35 | 2 | killed |
| `u120.P1_live_plain_attribute` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 4 | killed |
| `u120.P2_two_sources_accepted` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 2 | killed |
| `u120.P4_into_source_always` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 3 | killed |
| `u120.P7_bypass_only_when_absent` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 3 | killed |
| `u120.P8_source_name_default` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 1 | killed |
| `u145.M2_placement_undated` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 98 | 21 | killed |
| `u146-b.B15_any_playlist_files` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 31 | 1 | killed |
| `u153.P1_into_colour_flag` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 98 | 11 | killed |
| `u153.P3_writes_colours` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 98 | 4 | killed |
| `u153.P4_identity_pink` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 1 | killed |
| `u153.P5_recolour_dedup` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 98 | 3 | killed |
| `u153.P6_place_pink_guard` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 80 | 2 | killed |
| `u180.M11_new_month_seated` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 102 | 6 | killed |
| `u180.M12_new_month_knows_the_source` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 102 | 5 | killed |
| `u180.M13_never_above_all_favorites` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 1 | killed |
| `u180.M7_children_live_only` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 102 | 3 | killed |
| `u180.M8_slots_lift_shared` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 102 | 4 | killed |
| `u180.M9_seat_skips_unmoved` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 35 | 7 | killed |
| `u308.M16_root_reads_any_parent` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 1 | killed |
| `u119.V1_ack_after_plan` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 46 | 1 | killed |
| `u120-b.B4r_stale_not_refused` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 31 | 2 | killed |
| `u145.C2_unplanned_playlist_admitted` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C5_content_unchecked` | `src/cratekit/favorites/spine.py` | user | 2 file(s) | 68 | 2 | killed |
| `u145.C6_existing_playlist_change_admitted` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.V1_gate_on_nothing` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 33 | 2 | killed |
| `u180-m25.M25_read_back_asserted` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 35 | 1 | killed |
| `u180.M20_confined_content` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 35 | 1 | killed |
| `u308.M10_commit_unrecorded` | `src/cratekit/favorites/spine.py` | user | 2 file(s) | 64 | 3 | killed |
| `u308.M11_confinement_off` | `src/cratekit/favorites/spine.py` | user | 2 file(s) | 68 | 2 | killed |
| `u308.M13_made_rows_refused` | `src/cratekit/favorites/spine.py` | user | 2 file(s) | 68 | 15 | killed |
| `u308.M14_bookkeeping_always_admitted` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 35 | 2 | killed |
| `u308.M15_unverified_answer_passed` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 35 | 2 | killed |
| `u308.M1_gate_first_skipped` | `src/cratekit/favorites/spine.py` | user | 2 file(s) | 77 | 7 | killed |
| `u308.M2_declined_gate_drops_warnings` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 35 | 1 | killed |
| `u308.M3_backup_ack_skipped` | `src/cratekit/favorites/spine.py` | user | 4 file(s) | 145 | 4 | killed |
| `u308.M4_totals_not_merged` | `src/cratekit/favorites/spine.py` | user | 4 file(s) | 145 | 9 | killed |
| `u308.M5_read_back_skipped` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 35 | 1 | killed |
| `u308.M6_write_handle_not_closed` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 35 | 1 | killed |
| `u308.M7_empty_roots_admitted` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 35 | 1 | killed |
| `u308.M8_restore_not_detected` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 35 | 1 | killed |
| `u308.M9_landed_raise_unrecorded` | `src/cratekit/favorites/spine.py` | user | 1 file(s) | 35 | 1 | killed |
| `u145-s2.S2b_removed_member_read_live` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C1_unplanned_membership_admitted` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 3 | killed |
| `u145.C3_parent_unchecked` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.C4_changed_membership_admitted` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S10_unemptied_retired` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S11_unemptied_asks_taken_back` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S12_retirement_admits_memberships_only` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 13 | killed |
| `u145.S13_retirement_confined_to_nothing` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 13 | killed |
| `u145.S1_any_name_is_a_quarter` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 8 | killed |
| `u145.S3_last_dated_mention_wins` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S4_account_never_asked` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S5_job_dates_ignored` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 11 | killed |
| `u145.S6_rehearted_is_taken_back` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S7_taken_back_placed` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u145.S9_digest_covers_the_months_state` | `src/cratekit/favorites/split.py` | user | 1 file(s) | 33 | 1 | killed |
| `u113-a.A2_queue_order` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 23216 | 0 (promoted) | zero |
| `u113-a.A3_no_pass_splits_nothing` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u113-a.A8_pending_any_state` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 26 | 1 | killed |
| `u120.B2_first_mention_wins` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 44 | 2 | killed |
| `u128-b.A6b_abandoned_counts` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 26 | 1 | killed |
| `u128-b.A8b_ambiguous_is_an_answer` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 26 | 1 | killed |
| `u128-b.A9b_emptied_left_lost` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 26 | 1 | killed |
| `u128.A10_no_warning` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 42 | 5 | killed |
| `u128.A1_owned_not_mirrored` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 42 | 9 | killed |
| `u128.A2_rerun_unseen` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 42 | 2 | killed |
| `u128.A3_rerun_keeps_owned` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 16 | 1 | killed |
| `u128.A4_untied_carried_silent` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 42 | 2 | killed |
| `u128.A7_any_pass_counts` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 42 | 2 | killed |
| `u145.M3_landing_heart_undated` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 13 | 9 | killed |
| `u145.M4_states_carried_only` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 64 | 8 | killed |
| `u146-b.A1_superseded_ignored` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 12 | 1 | killed |
| `u146-b.A2_owned_reads_carried` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 12 | 8 | killed |
| `u146-b.A3_report_paths_dropped` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 12 | 7 | killed |
| `u166.C10_live_filter` | `src/cratekit/intake/analyzed.py` | user | 1 file(s) | 14 | 5 | killed |
| `u166.C1_removed_row` | `src/cratekit/intake/analyzed.py` | user | 1 file(s) | 14 | 1 | killed |
| `u166.C2_analysed_flag` | `src/cratekit/intake/analyzed.py` | user | 1 file(s) | 14 | 1 | killed |
| `u166.C3_analysis_path` | `src/cratekit/intake/analyzed.py` | user | 1 file(s) | 14 | 1 | killed |
| `u166.C4_blank_path` | `src/cratekit/intake/analyzed.py` | user | 1 file(s) | 14 | 1 | killed |
| `u166.C5_missing_row` | `src/cratekit/intake/analyzed.py` | user | 1 file(s) | 14 | 1 | killed |
| `u166.C6_stale_check` | `src/cratekit/intake/analyzed.py` | user | 1 file(s) | 14 | 1 | killed |
| `u166.C7_clear_waits_too` | `src/cratekit/intake/analyzed.py` | user | 1 file(s) | 14 | 3 | killed |
| `u166.C8_read_back_lost` | `src/cratekit/intake/analyzed.py` | user | 1 file(s) | 14 | 1 | killed |
| `u166.C9_read_back_kept` | `src/cratekit/intake/analyzed.py` | user | 1 file(s) | 14 | 2 | killed |
| `u259.M1_judge_no_row` | `src/cratekit/intake/analyzed.py` | user | 1 file(s) | 14 | 1 | killed |
| `u259.M5_member_reads_nothing` | `src/cratekit/intake/analyzed.py` | user | 1 file(s) | 14 | 6 | killed |
| `u166.C12_ack_first` | `src/cratekit/intake/analyzed_cli.py` | user | 1 file(s) | 14 | 1 | killed |
| `u166.C13_read_back_call` | `src/cratekit/intake/analyzed_cli.py` | user | 1 file(s) | 14 | 1 | killed |
| `u110-a.A2_favorites_word` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 20 | 2 | killed |
| `u110-a.A5_several_labels` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 20 | 1 | killed |
| `u110-a.A6_folder_safe` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 20 | 1 | killed |
| `u110-a.A7_join_order` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 20 | 2 | killed |
| `u110-a.A8_labels_first` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 20 | 1 | killed |
| `u113-a.A4_batch_name_not_taken` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 26 | 2 | killed |
| `u113-a.A5_landing_names_its_own` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 26 | 1 | killed |
| `u154.R5_unreadable_record_fails_open` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 23 | 1 | killed |
| `u164.B1_taken_recorded` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 73 | 3 | killed |
| `u164.B2_native_names` | `src/cratekit/intake/batch_name.py` | user | 2 file(s) | 50 | 2 | killed |
| `u175.N1_date_first` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 69 | 41 | killed |
| `u175.N2_no_date` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 69 | 41 | killed |
| `u175.N3_date_form` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 69 | 41 | killed |
| `u175.N4_clock_not_seam` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 69 | 41 | killed |
| `u175.N7_held_not_held` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 69 | 8 | killed |
| `u175.N8_counter_before_date` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 69 | 9 | killed |
| `u175.N9_landing_not_held` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 26 | 1 | killed |
| `r1709.M23_intake_exact_by_token` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 2 | killed |
| `r879-a.C10_offset_counts_pages_not_rows` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 63 | 4 | killed |
| `r879-a.C11_sole_exact_ignores_full` | `src/cratekit/intake/candidates.py` | user | 2 file(s) | 113 | 4 | killed |
| `r879-a.C1_full_reads_total_not_last_page` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 63 | 5 | killed |
| `r879-a.C2_walk_ignores_short_page` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 63 | 6 | killed |
| `r879-a.C3_settled_early_without_ambiguity` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 63 | 2 | killed |
| `r879-a.C4_settled_early_without_unreadable` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 63 | 1 | killed |
| `r879-a.C6_settled_early_without_several` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 63 | 1 | killed |
| `r879-a.C7_bound_off_by_one` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 63 | 2 | killed |
| `r879-a.C9_read_pages_forgets_last_page` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 63 | 5 | killed |
| `r879-b.C5r_settled_early_without_unnamed_exact` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 63 | 1 | killed |
| `r879-b.C8r_ceiling_coefficient` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 63 | 1 | killed |
| `u307.R14_search_pages_default_one_page` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 63 | 7 | killed |
| `u307.R15_search_pages_constant_off_by_one` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 63 | 1 | killed |
| `u307.R25_toggle_imported_at_top` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 57 | 1 | killed |
| `u79-a.A1_ambiguous_listed` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 2 | killed |
| `u79-a.A2_full_page_listed` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-a.A3_unreadable_ignored` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-a.A4_no_identifier_listed` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 2 | killed |
| `u79-a.A5_two_exact_picked` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 3 | killed |
| `u79-b.B1_floor_halved` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-b.B2_score_before_exact` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-b.B3_no_identifier_offered` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 2 | killed |
| `u79-b.B4_rejected_read_as_accepted` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-b.B5_unspecific_yes_takes_first` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-b.B6_option_track_mismatch` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-b.B8_open_item_searched_again` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `r290-author.S05_intake_call_removed` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 126 | 11 | killed |
| `r431-b.B10_an_older_payload_reads_as_solo` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `r431-b.B9_the_freeze_drops_the_field` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `r504-b.B1_verb_drops_short` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `r504-b.B4_no_progress_block` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 40 | 4 | killed |
| `r504-b.B5_noop_silent` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `r504-b.B6_warning_reworded` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `r515-operator.S10_intake_all_withheld_quiet` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `r515-operator.S11_intake_playlist_no_warning` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 40 | 4 | killed |
| `u103-b.C8_set_no_op_carries_warnings` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `u113-a.A7_payload_drops_name` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 42 | 32 | killed |
| `r770-b.B5_file_verb_never_takes_the_native_path` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 16 | killed |
| `r770-b.B6_export_taken_on_a_native_tree` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-b.B7_staging_not_asked_first` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-b.B8_target_spelled_as_resolved` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-c.C1_unplaceable_file_reaches_the_gate` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-c.C2_untyped_suffix_reaches_the_gate` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-c.C5_playlist_named_for_the_whole_file_name` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 3 | killed |
| `r770-d.C6_digest_without_the_collection_plan` | `src/cratekit/intake/file_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u165.F1_reset_cache` | `src/cratekit/intake/filing.py` | user | 1 file(s) | 10 | 1 | killed |
| `u165.F2_compare` | `src/cratekit/intake/filing.py` | user | 1 file(s) | 10 | 1 | killed |
| `u165.F3_differing_files` | `src/cratekit/intake/filing.py` | user | 1 file(s) | 10 | 1 | killed |
| `u165.F4_vox_predicted` | `src/cratekit/intake/filing.py` | user | 1 file(s) | 10 | 1 | killed |
| `u165.F6_unplaced` | `src/cratekit/intake/filing.py` | user | 1 file(s) | 10 | 1 | killed |
| `r501-c.M1_export_name_check` | `src/cratekit/intake/imported_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-c.M2_export_identity_check` | `src/cratekit/intake/imported_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-c.M3_missing_is_not_imported` | `src/cratekit/intake/imported_cli.py` | user | 1 file(s) | 34 | 4 | killed |
| `r501-c.M4_nothing_recorded` | `src/cratekit/intake/imported_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-c.M5_retire_name_guard` | `src/cratekit/intake/imported_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-c.M6_retire_link_guard` | `src/cratekit/intake/imported_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-d.M10_waiting_legacy` | `src/cratekit/intake/imported_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-d.M11_close_refusal_reported` | `src/cratekit/intake/imported_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-d.M13_waiting_needs_export` | `src/cratekit/intake/imported_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-d.M7_retire_next_free_name` | `src/cratekit/intake/imported_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-d.M9_waiting_capture` | `src/cratekit/intake/imported_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r773-b.P1_proof_granted_whatever_the_export_names` | `src/cratekit/intake/imported_cli.py` | user | 2 file(s) | 128 | 6 | killed |
| `u307.R11_imported_session_ignored` | `src/cratekit/intake/imported_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-b.I1_rollback_abandon` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 34 | 3 | killed |
| `r501-b.I2_rollback_unlink` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-b.I3_rollback_fresh_only` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-b.I4_mark_awaiting` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 61 | 23 | killed |
| `r770-a.A1_switch_reads_the_other_mode` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 77 | 57 | killed |
| `r770-a.A2_unreachable_root_is_read_anyway` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 60 | 3 | killed |
| `r770-a.A3_assertion_refuses_nothing` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-a.A4_refusal_asks_for_a_defect_report` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-a.A5_tree_built_without_the_refusal` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-a.A6_splice_asks_only_after_the_export` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 1 | killed |
| `u113-b.B2_batch_keeps_claimed` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 26 | 9 | killed |
| `u113-b.B3_record_unnamed` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 26 | 3 | killed |
| `u113-b.B4_steps_name_one` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 26 | 1 | killed |
| `u128-b.B4_bridge_owned_dropped` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 26 | 1 | killed |
| `u128-b.B5_bridge_record_no_account` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 26 | 2 | killed |
| `r1056.F1_no_fold` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F2_empty_year_counts` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F3_any_label_counts` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 4 | killed |
| `r1056.F4_non_list_read_as_empty` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F5_non_dict_entry_skipped` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F6_text_year_accepted` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 2 | killed |
| `r1056.F7_bool_tracks_accepted` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F8_no_zero_pad` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `u156.L10_staging_dropped` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 1 | killed |
| `u156.L11_unlanded_named` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 2 | killed |
| `u156.L12_empty_year` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 1 | killed |
| `u156.L13_tree_reused` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 4 | killed |
| `u156.L14_folder_reused` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 6 | killed |
| `u156.L15_year_reused` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 5 | killed |
| `u156.L16_live_at_write` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 1 | killed |
| `u156.L17_digest_years` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 1 | killed |
| `u156.L1_year_bound` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 3 | killed |
| `u156.L21_read_back` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 1 | killed |
| `u156.L2_bridge_guard` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 1 | killed |
| `u156.L3_wrong_kind` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 1 | killed |
| `u156.L4_two_of_a_name` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 1 | killed |
| `u156.L5_nfc_fold` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 3 | killed |
| `u156.L6_removed_nodes` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 1 | killed |
| `u156.L7_year_boundary` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 1 | killed |
| `u156.L8_year_anchor` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 2 | killed |
| `u156.L9_no_year_named` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 4 | killed |

## Zero rows and what they owe

- `u113-a.A2_queue_order` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u113-a.A3_no_pass_splits_nothing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u185.R5_taxonomy_refusal`

load_taxonomy: accept a declared tree displayed as DEADCA7

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u185.json`, row `R5_taxonomy_refusal`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_tree_declared_with_the_folders_name_is_refused_so_none_adopts_it[tree-BY GENRE + ENERGY]`

Old text:

```
        elif node.display in FOREIGN_ROOT_NAMES:
```

New text:

```
        elif node.display in FOREIGN_ROOT_NAMES and False:
```

### `u244.M24_upgrade_keeps_a_held_table`

_vocabularies: do not pass over a vocabulary table the copy already declares

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u244.json`, row `M24_upgrade_keeps_a_held_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_current_copy_with_every_entry_is_ok`

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

### `u331.S14_upgrade_loads_the_taxonomy_loader_at_top`

core/taxonomy_upgrade: import the active taxonomy loader at the top again, so crate doctor --help loads the foreign tree with it

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u331.json`, row `S14_upgrade_loads_the_taxonomy_loader_at_top`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_doctor_help_loads_the_doctor_and_only_what_the_doctor_itself_imports`

Old text:

```
from cratekit.core import config, taxonomy

```

New text:

```
from cratekit.core import active_taxonomy, config, taxonomy  # noqa: F401

```

### `r431-a.A1_a_plain_row_gains_a_companion`

uncredited_title answers the stripped title even when nothing was stripped, so a plain deletion writes a companion

- File: `src/cratekit/core/tombstone.py`
- Source: `r431-a.json`, row `A1_a_plain_row_gains_a_companion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 11 (killed)
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

Old text:

```
    return stripped if dropped else ""
```

New text:

```
    return stripped
```

### `r235-a.M11_session_lock_dropped`

a revert holds the registry lock and not the session lock

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M11_session_lock_dropped`
- Moved: Same with statement in revert_cutover; U298 renamed config._exclusive_lock to exclusive_lock
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_the_revert_holds_the_session_lock_while_it_asks_and_writes`

Old text:

```
    with session.session_lock(cfg), config.exclusive_lock(lock_path(cfg)):
```

New text:

```
    with config.exclusive_lock(lock_path(cfg)):
```

### `r235-a.M12_second_record_replaces`

record_cutover replaces a tree already recorded native instead of refusing

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M12_second_record_replaces`
- Moved: the same guard in the same file and function, its comment cut to its rule and reason by U300's prose pass, so the text the row names changed and the condition it falsifies did not
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_tree_already_recorded_is_not_recorded_again`

Old text:

```
        if standing is not None and standing.mode == Mode.DATABASE:
            # Asked under the lock, so two cutovers of one tree cannot both pass.
```

New text:

```
        if False:
            # Asked under the lock, so two cutovers of one tree cannot both pass.
```

### `r235-a.M13_snapshot_check_dropped`

the verified snapshot check is no longer in the precheck table

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M13_snapshot_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`
- Collected: 66 against a baseline of 66
- Kills: 11 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_leave_intake_xml-cutover-xml-pending-no-pending-intake-xml]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_open_a_run-cutover-open-run-no-open-run]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_export-cutover-export-missing-fresh-export]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_snapshot-cutover-snapshot-missing-verified-snapshot]`
  - `tests/test_cutover_cli.py::test_the_plan_names_the_root_and_approval_records_that_tree_alone`
  - `tests/test_cutover_cli.py::test_two_failing_prechecks_are_both_named_on_one_run`
  - `tests/test_cutover_precheck.py::test_a_missing_snapshot_blocks_the_flip`
  - `tests/test_cutover_precheck.py::test_an_unverified_capture_does_not_count_as_a_snapshot`
  - `tests/test_cutover_precheck.py::test_the_report_and_the_assertion_refuse_with_one_cause`
  - `tests/test_cutover_precheck.py::test_the_report_carries_each_refusal_and_does_not_stop_at_the_first`
  - `tests/test_cutover_precheck.py::test_the_report_names_every_check_in_the_order_the_assertion_refuses`

Old text:

```
    ("fresh-export", _export_refusal),
    ("verified-snapshot", _snapshot_refusal),
)
```

New text:

```
    ("fresh-export", _export_refusal),
)
```

### `r235-a.M1_unreadable_log_skipped`

the registry gates no longer refuse on a session record they cannot read, so a torn record reads as no open run and no native write

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M1_unreadable_log_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_record_nobody_can_read_refuses_the_flip_rather_than_reading_as_no_open_run`
  - `tests/test_cutover_precheck.py::test_a_record_nobody_can_read_refuses_the_revert_rather_than_reading_as_no_write`

Old text:

```
    parsed, unreadable = session.scan_log(cfg)
    if unreadable:
```

New text:

```
    parsed, unreadable = session.scan_log(cfg)
    if False:
```

### `r235-a.M2_margin_zero`

the native write margin is no days, so a write whose universal time date is the day before the cutover day is left out

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M2_margin_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_write_that_cannot_be_shown_to_predate_the_cutover_counts[2026-07-31T23:50:00Z]`

Old text:

```
NATIVE_WRITE_MARGIN = timedelta(days=1)
```

New text:

```
NATIVE_WRITE_MARGIN = timedelta(days=0)
```

### `r235-a.M3_margin_two_days`

the native write margin is two days, so a write two days before the cutover day still counts

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M3_margin_two_days`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_the_day_before_the_margin_is_the_first_day_left_out`

Old text:

```
NATIVE_WRITE_MARGIN = timedelta(days=1)
```

New text:

```
NATIVE_WRITE_MARGIN = timedelta(days=2)
```

### `r235-a.M4_unparseable_start_predates`

a session start nothing can parse is read as before the cutover, so its write does not count

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M4_unparseable_start_predates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_write_that_cannot_be_shown_to_predate_the_cutover_counts[not a timestamp]`

Old text:

```
    except ValueError:
        return False
    return began < cutover_on - NATIVE_WRITE_MARGIN
```

New text:

```
    except ValueError:
        return True
    return began < cutover_on - NATIVE_WRITE_MARGIN
```

### `r235-a.M5_updates_not_counted`

only a creation counts as a native write, an update does not

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M5_updates_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_update_counts_as_a_native_write_as_a_creation_does`

Old text:

```
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
```

New text:

```
            change.tree == tree_id and change.created > 0
```

### `r235-a.M6_any_tree_counts`

a write to any tree counts as a write to this one

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M6_any_tree_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_write_to_another_tree_does_not_close_this_trees_door`
  - `tests/test_cutover_precheck.py::test_a_session_that_wrote_nothing_to_this_tree_leaves_the_revert_open`

Old text:

```
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
```

New text:

```
            (change.created > 0 or change.updated > 0)
```

### `r235-a.M7_zero_count_counts`

a record naming the tree with nothing added counts as a native write

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M7_zero_count_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_write_to_another_tree_does_not_close_this_trees_door`
  - `tests/test_cutover_precheck.py::test_a_session_that_wrote_nothing_to_this_tree_leaves_the_revert_open`

Old text:

```
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
```

New text:

```
            change.tree == tree_id
```

### `r235-a.M8_open_run_reverts`

a revert no longer refuses over an open run

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M8_open_run_reverts`
- Moved: U953 folded this module's refuse calls into the _refuse builder, so the open run test of assert_revertible now guards raise _refuse and disabling it is the same revert over an open run
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`

Old text:

```
    if open_runs:
        raise _refuse(
            "cutover-open-run",
```

New text:

```
    if False:
        raise _refuse(
            "cutover-open-run",
```

### `r235-a.M9_library_guard_removed`

revert_cutover no longer asserts the tree is revertible, leaving only the verb's own check

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M9_library_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`
- Collected: 26 against a baseline of 26
- Kills: 4 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_record_nobody_can_read_refuses_the_revert_rather_than_reading_as_no_write`
  - `tests/test_cutover_precheck.py::test_a_revert_after_a_native_write_is_refused_by_the_library_itself`
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`
  - `tests/test_cutover_precheck.py::test_the_revert_holds_the_session_lock_while_it_asks_and_writes`

Old text:

```
        assert_revertible(cfg, tree_id)
        updated = read(cfg).without_record(tree_id)
```

New text:

```
        updated = read(cfg).without_record(tree_id)
```

### `r235-b.M14_empty_export_accepted`

an export of no bytes passes the fresh export check

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-b.json`, row `M14_empty_export_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_an_empty_export_is_no_export`

Old text:

```
    if export_path.is_file() and export_path.stat().st_size != 0:
```

New text:

```
    if export_path.is_file():
```

### `r501-a.T1_precheck_excusal`

tree_registry.assert_cutover_ready: drop the excusal, so a proven landing refuses the cutover for ever, which is R-501 itself

- File: `src/cratekit/core/tree_registry.py`
- Source: `r501-a.json`, row `T1_precheck_excusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_intake_file_ends_pending_and_is_settled_the_same_way`
  - `tests/test_intake_imported.py::test_the_precheck_excuses_a_verified_run_holding_no_capture`

Old text:

```
        if not record.terminal and not session.owes_only_deferred_routing(record)
```

New text:

```
        if not record.terminal
```

### `r787.S1_set_drops_intake`

cutover_trees returns the routing tree alone, the list doctor held before R-787

- File: `src/cratekit/core/tree_registry.py`
- Source: `r787.json`, row `S1_set_drops_intake`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 7 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_tree_the_taxonomy_does_not_declare_is_refused`
  - `tests/test_cutover_cli.py::test_doctor_and_the_verb_read_one_set_of_cutover_trees`
  - `tests/test_cutover_cli.py::test_doctor_fails_on_a_native_record_the_cutover_would_refuse_to_create`
  - `tests/test_cutover_cli.py::test_doctor_reads_a_native_inbox_record_as_ok`
  - `tests/test_cutover_cli.py::test_doctor_reads_an_inbox_the_verb_cut_over_as_ok`
  - `tests/test_cutover_cli.py::test_the_catalogue_tree_is_refused_as_not_rebuildable`
  - `tests/test_cutover_cli.py::test_the_intake_tree_cuts_over_on_the_same_answer_as_the_routing_tree`

Old text:

```
    return frozenset({declared.tree.id, declared.intake.id})
```

New text:

```
    return frozenset({declared.tree.id})
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

### `u243.D10_prefix_order_fewest_first`

reference_set: unmapped prefixes sorted fewest first, so the refusal names the smallest groups

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D10_prefix_order_fewest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_an_unmapped_local_path_still_refuses_and_names_its_prefix_and_rule`

Old text:

```
key=lambda pair: (-pair[1], pair[0])
```

New text:

```
key=lambda pair: (pair[1], pair[0])
```

### `u243.D11_refusal_names_no_prefix`

assert_complete: the prefixes are left out of the refusal's sentence

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D11_refusal_names_no_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`
- Collected: 22 against a baseline of 22
- Kills: 3 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_refusal_names_at_most_five_prefixes_and_counts_the_rest`
  - `tests/test_deletion_streaming.py::test_an_unmapped_local_path_still_refuses_and_names_its_prefix_and_rule`
  - `tests/test_deletion_streaming.py::test_delete_review_still_refuses_an_unmapped_local_row_beside_streaming_rows`

Old text:

```
        f"cannot resolve{f' ({under})' if under else ''}, "
```

New text:

```
        f"cannot resolve, "
```

### `u243.D12_refusal_offers_no_rule`

assert_complete: the location_prefix_map step is not offered

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D12_refusal_offers_no_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`
- Collected: 353 against a baseline of 353
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_refusal_with_no_dead_anchor_offers_no_directory_to_mount`
  - `tests/test_deletion_streaming.py::test_an_unmapped_local_path_still_refuses_and_names_its_prefix_and_rule`

Old text:

```
                for prefix, count in named
            ),
```

New text:

```
                for prefix, count in ()
            ),
```

### `u243.D1_id_class_takes_a_dot`

_STREAMING_LOCATION: the id class takes any character but a slash, so /v4/catalog/tracks/123.flac/ is excused

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D1_id_class_takes_a_dot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123.flac/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/12_3/]`

Old text:

```
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[A-Za-z0-9]+/?\Z")
```

New text:

```
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[^/]+/?\Z")
```

### `u243.D2_end_anchor_is_dollar`

_STREAMING_LOCATION: \Z becomes $, which also accepts a trailing newline

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D2_end_anchor_is_dollar`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123/\n]`

Old text:

```
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[A-Za-z0-9]+/?\Z")
```

New text:

```
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[A-Za-z0-9]+/?$")
```

### `u243.D3_no_end_anchor`

_STREAMING_LOCATION: no end anchor, so /v4/catalog/tracks/123/track.flac is excused

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D3_no_end_anchor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`
- Collected: 22 against a baseline of 22
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123.flac/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123/\n]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123/track.flac]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/12_3/]`

Old text:

```
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[A-Za-z0-9]+/?\Z")
```

New text:

```
_STREAMING_LOCATION = re.compile(r"/v4/catalog/tracks/[A-Za-z0-9]+")
```

### `u243.D4_search_not_match`

_streaming: search rather than match, so a spelling under another directory is excused

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D4_search_not_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/Elsewhere/v4/catalog/tracks/123/]`

Old text:

```
    if not _STREAMING_LOCATION.match(text):
```

New text:

```
    if not _STREAMING_LOCATION.search(text):
```

### `u243.D5_spelling_not_asked`

_streaming: the spelling test is dropped, so every unmapped row with nothing at it is excused

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D5_spelling_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`
- Collected: 353 against a baseline of 353
- Kills: 17 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_prefix_rule_whose_target_is_not_there_refuses_rather_than_proving_nothing`
  - `tests/test_deletion.py::test_a_refusal_with_no_dead_anchor_offers_no_directory_to_mount`
  - `tests/test_deletion.py::test_an_unresolvable_active_row_makes_the_whole_run_refuse`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/Elsewhere/v4/catalog/tracks/123/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/V4/catalog/tracks/123/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4//catalog/tracks/123/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/albums/123/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks//]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123.flac/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123/\n]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/123/track.flac]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/12_3/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v4/catalog/tracks/]`
  - `tests/test_deletion_streaming.py::test_a_path_shaped_only_near_a_streaming_row_still_refuses[/v5/catalog/tracks/123/]`
  - `tests/test_deletion_streaming.py::test_a_refusal_names_at_most_five_prefixes_and_counts_the_rest`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    if not _STREAMING_LOCATION.match(text):
        return False
```

New text:

```
    if False:
        return False
```

### `u243.D6_disk_not_asked`

_streaming: the stat is not asked, so a streaming spelling with a file at it is excused

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D6_disk_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`
- Collected: 22 against a baseline of 22
- Kills: 5 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_is_asked_about_on_the_disk`
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[None]`
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[answer1]`
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[answer2]`
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[answer3]`

Old text:

```
    try:
        stat(text)
    except FileNotFoundError:
        return True
    except (OSError, ValueError):
        return False
    return False
```

New text:

```
    return True
```

### `u243.D7_an_error_reads_as_absent`

_streaming: a stat error other than not found reads as nothing there, failing open

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D7_an_error_reads_as_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`
- Collected: 22 against a baseline of 22
- Kills: 3 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[answer1]`
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[answer2]`
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[answer3]`

Old text:

```
    except (OSError, ValueError):
        return False
    return False
```

New text:

```
    except (OSError, ValueError):
        return True
    return False
```

### `u243.D8_something_there_reads_as_absent`

_streaming: a stat that answers, a file or directory at the spelling, reads as nothing there

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D8_something_there_reads_as_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_streaming_spelling_with_anything_at_it_still_refuses[None]`

Old text:

```
    except (OSError, ValueError):
        return False
    return False
```

New text:

```
    except (OSError, ValueError):
        return False
    return True
```

### `u243.D9_streaming_still_counted_unmapped`

reference_set: a streaming row is counted but also left unmapped, so the run still refuses

- File: `src/cratekit/deletion/candidates.py`
- Source: `u243.json`, row `D9_streaming_still_counted_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`
- Collected: 22 against a baseline of 22
- Kills: 3 (killed)
- Killed:
  - `tests/test_deletion_streaming.py::test_a_library_with_streaming_rows_offers_the_removed_file`
  - `tests/test_deletion_streaming.py::test_an_unmapped_local_path_still_refuses_and_names_its_prefix_and_rule`
  - `tests/test_deletion_streaming.py::test_delete_review_trashes_a_removed_file_beside_streaming_rows`

Old text:

```
                streaming.append(row.content_id)
                continue
```

New text:

```
                streaming.append(row.content_id)
```

### `u310.P1_identifiable`

categorize: drop the identifiability proof, so a row no tombstone can name is offered

- File: `src/cratekit/deletion/candidates.py`
- Source: `u310.json`, row `P1_identifiable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 3 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable`
  - `tests/test_deletion.py::test_a_row_that_could_never_carry_a_tombstone_is_not_offered_as_deletable`
  - `tests/test_deletion.py::test_a_row_with_no_artist_and_no_title_is_never_deletable`

Old text:

```
        if not identifiable(row):
```

New text:

```
        if False:
```

### `u310.P2_declined`

categorize: drop the decline proof, so a declined file is offered again

- File: `src/cratekit/deletion/candidates.py`
- Source: `u310.json`, row `P2_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_decline_recorded_between_the_plan_and_the_move_stops_the_move`
  - `tests/test_deletion.py::test_a_declined_file_is_absent_from_the_next_run_and_returns_when_revoked`
  - `tests/test_deletion.py::test_a_declined_row_holds_the_watermark_and_lets_it_go_when_revoked`
  - `tests/test_deletion.py::test_a_revoke_that_cannot_reopen_the_item_leaves_the_decline_standing`

Old text:

```
        if declined(row):
```

New text:

```
        if False:
```

### `u310.P3_ambiguous_version`

categorize: drop the ambiguous version proof, so a tombstone for one recording suppresses another

- File: `src/cratekit/deletion/candidates.py`
- Source: `u310.json`, row `P3_ambiguous_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 3 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
  - `tests/test_deletion.py::test_the_collision_is_looked_for_across_the_whole_walk_not_the_offered_rows`
  - `tests/test_deletion.py::test_two_recordings_that_land_on_one_identity_are_refused_rather_than_suppressed`

Old text:

```
        if ambiguous(row):
```

New text:

```
        if False:
```

### `u310.P4_collides_with_active_row`

categorize: drop the active row collision proof, so a file a live row points at is offered

- File: `src/cratekit/deletion/candidates.py`
- Source: `u310.json`, row `P4_collides_with_active_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 5 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_confirmed_item_invalidated_before_the_move_is_refused_at_move_time`
  - `tests/test_deletion.py::test_a_file_an_active_row_also_points_at_is_a_collision_in_every_spelling[same]`
  - `tests/test_deletion.py::test_a_hard_link_from_an_active_row_is_a_collision`
  - `tests/test_deletion.py::test_a_recorded_prefix_the_map_covers_resolves_on_both_sides`
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`

Old text:

```
        if claimed:
```

New text:

```
        if False:
```

### `u310.P5_size_matches`

categorize: drop the size proof, so a file of another size is taken for the one the row named

- File: `src/cratekit/deletion/candidates.py`
- Source: `u310.json`, row `P5_size_matches`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_file_of_a_different_size_is_never_deletable`
  - `tests/test_deletion.py::test_only_deletable_candidates_are_ever_offered`

Old text:

```
        if row.size is None or int(stats.st_size) != int(row.size):
```

New text:

```
        if row.size is None:
```

### `u310.P6_still_referenced`

categorize: drop the playlist proof, so a file a playlist still holds is offered

- File: `src/cratekit/deletion/candidates.py`
- Source: `u310.json`, row `P6_still_referenced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_file_a_playlist_still_references_is_not_trashed`
  - `tests/test_deletion.py::test_a_membership_walk_that_comes_back_short_refuses_rather_than_freeing_the_file`
  - `tests/test_deletion.py::test_a_playlist_that_claims_the_file_between_the_review_and_the_move_stops_it`
  - `tests/test_deletion.py::test_a_playlist_that_takes_the_file_after_the_plan_stops_the_move`

Old text:

```
        if row.content_id in referenced:
```

New text:

```
        if False:
```

### `u310.P7_anchor_moved_mid_walk`

categorize: drop the refusal of a walk whose anchor moved, so answers off two filesystems stand

- File: `src/cratekit/deletion/candidates.py`
- Source: `u310.json`, row `P7_anchor_moved_mid_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_volume_that_goes_away_mid_categorization_refuses_rather_than_retiring`

Old text:

```
    moved = anchors.changed()
    if moved:
```

New text:

```
    moved = anchors.changed()
    if False:
```

### `r1844.N17_screen_silent`

the gate's screen never shows the landings read as rolled back

- File: `src/cratekit/deletion/cli.py`
- Source: `r1844.json`, row `N17_screen_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 6 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_restore_to_before_the_landing_offers_nothing_and_the_screen_counts_it`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_every_row_gone_and_the_playlist_deleted_by_hand_is_kept_and_counted`
  - `tests/test_delete_landed_removed.py::test_the_first_review_counts_a_landing_already_rolled_back`

Old text:

```
    if found.rolled_back:
```

New text:

```
    if False:
```

### `u243.D14_screen_never_says_ignored`

deletion.cli._shown: the count of rows excused as no local file is never put on the gate screen

- File: `src/cratekit/deletion/cli.py`
- Source: `u243.json`, row `D14_screen_never_says_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`
- Collected: 353 against a baseline of 353
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_deletion_streaming.py::test_delete_review_trashes_a_removed_file_beside_streaming_rows`

Old text:

```
    if ignored:
        shown["ignored, not local files"] = ignored
```

New text:

```
    if False:
        shown["ignored, not local files"] = ignored
```

### `u310.G1_abort_moves_nothing`

review: drop the abort answer, so an aborted gate still trashes

- File: `src/cratekit/deletion/cli.py`
- Source: `u310.json`, row `G1_abort_moves_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`

Old text:

```
        if option == "abort":
```

New text:

```
        if False:
```

### `u310.G3_recorded_reject_honoured`

review: the gate accepts every offered item, a recorded reject included

- File: `src/cratekit/deletion/cli.py`
- Source: `u310.json`, row `G3_recorded_reject_honoured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`

Old text:

```
                if item.verdict is None:
```

New text:

```
                if True:
```

### `r1037.M1_identity_unchecked`

landed_absences: read a landing record of any database, so another library's landed rows are offered here

- File: `src/cratekit/deletion/library.py`
- Source: `r1037.json`, row `M1_identity_unchecked`
- Moved: the record preamble of landed_absences and recorded_removals is now one generator, _records, whose record is named recorded; the identity check is dropped from it, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_of_another_database_offers_nothing`

Old text:

```
        if str(recorded.get("database_identity") or "") != str(database_identity):
            continue
        sequence = recorded.get("sequence")
```

New text:

```
        sequence = recorded.get("sequence")
```

### `r1037.M7_earlier_landing_kept`

landed_absences: keep the earlier of two landings naming one row

- File: `src/cratekit/deletion/library.py`
- Source: `r1037.json`, row `M7_earlier_landing_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_one_row_two_landings_name_keeps_the_later_landings_count`

Old text:

```
            if seen is None or seen.landed < sequence:
```

New text:

```
            if seen is None or seen.landed > sequence:
```

### `r1037.M8_playlist_ids_live_only`

playlist_ids: count no playlist at all, so every landing reads as rolled back

- File: `src/cratekit/deletion/library.py`
- Source: `r1037.json`, row `M8_playlist_ids_live_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 9 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered`
  - `tests/test_delete_landed_removed.py::test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned`

Old text:

```
    return frozenset(str(getattr(row, "ID", "")) for row in playlists if getattr(row, "ID", None))
```

New text:

```
    return frozenset()
```

### `r1844.N10_numbered_ignored`

LandedRead.unasked: count every rolled back landing, a batch already offered and tidied included

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N10_numbered_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 2 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
        return sum(1 for rows in self.rolled_back if rows - asked)
```

New text:

```
        return sum(1 for rows in self.rolled_back if rows)
```

### `r1844.N11_marked_uuid_unread`

read_collection: keep the UUID of live rows only, so a marked landed row no longer proves its landing

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N11_marked_uuid_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 2 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_read_collection_keeps_each_rows_uuid_read_only`

Old text:

```
        uuids[_identifier(row, "ID")] = _text(row, "UUID")
        if not trees.soft_delete_marker(row):
```

New text:

```
        if not trees.soft_delete_marker(row):
            uuids[_identifier(row, "ID")] = _text(row, "UUID")
```

### `r1844.N12_record_uuid_unread`

landed_absences: the record's UUID is not read, so no row proves its landing

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N12_record_uuid_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
            uuid = entry.get(LANDED_UUID_KEY)
```

New text:

```
            uuid = entry.get("UUID")
```

### `r1844.N1_uuid_proof_dropped`

_landing_stands: never read a landed row held under its UUID as proof, so a landing whose playlist was deleted by hand is read as rolled back (the defect)

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N1_uuid_proof_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
    if any(uuid and uuids.get(content_id) == uuid for content_id, _columns, uuid in rows):
```

New text:

```
    if False:
```

### `r1844.N2_id_alone_proves`

_landing_stands: a row held under the landed id proves the landing whatever its UUID, so a later import's id reads a rolled back landing as standing

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N2_id_alone_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 3 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
    if any(uuid and uuids.get(content_id) == uuid for content_id, _columns, uuid in rows):
```

New text:

```
    if any(content_id in uuids for content_id, _columns, uuid in rows):
```

### `r1844.N3_empty_uuid_proves`

_landing_stands: a row recorded with no UUID matches a held row holding none

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N3_empty_uuid_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
    if any(uuid and uuids.get(content_id) == uuid for content_id, _columns, uuid in rows):
```

New text:

```
    if any(uuids.get(content_id) == uuid for content_id, _columns, uuid in rows):
```

### `r1844.N4_playlist_proof_dropped`

_landing_stands: every playlist held no longer proves the landing, so a lone landed track removed while its playlist stays is never offered

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N4_playlist_proof_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 11 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered`
  - `tests/test_delete_landed_removed.py::test_one_row_two_landings_name_keeps_the_later_landings_count`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned`

Old text:

```
    return all(playlist_held(str(one)) for one in playlists)
```

New text:

```
    return False
```

### `r1844.N5_any_playlist_proves`

_landing_stands: one playlist of the landing held is enough, not all of them

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N5_any_playlist_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_one_of_whose_playlists_is_gone_offers_nothing`

Old text:

```
    return all(playlist_held(str(one)) for one in playlists)
```

New text:

```
    return any(playlist_held(str(one)) for one in playlists)
```

### `r1844.N6_no_playlist_proves`

_landing_stands: a landing that made no playlist reads as standing, so a rolled back landing into a playlist already there is offered

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N6_no_playlist_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_restored_landing_into_a_playlist_already_there_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
    if not isinstance(playlists, (list, tuple)) or not playlists:
```

New text:

```
    if not isinstance(playlists, (list, tuple)):
```

### `r1844.N7_held_rows_read_absent`

landed_absences: a landed row the database holds is read as absent, so a live track's file is offered

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N7_held_rows_read_absent`
- Moved: the formatter split the over long comprehension; the held filter is dropped, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 33 (killed)
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
  - ... and 18 more, see the JSON sidecar

Old text:

```
            (content_id, columns) for content_id, columns, _uuid in rows if content_id not in held
```

New text:

```
            (content_id, columns) for content_id, columns, _uuid in rows
```

### `r1844.N8_nothing_absent_listed`

landed_absences: a landing with every row held is still weighed and listed as rolled back

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N8_nothing_absent_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`

Old text:

```
        if not absent:
            continue

```

New text:

```
(empty)
```

### `r1844.N9_rolled_back_unlisted`

landed_absences: a landing read as rolled back is not listed, so the gate never counts it

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N9_rolled_back_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 7 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_restore_to_before_the_landing_offers_nothing_and_the_screen_counts_it`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_every_row_gone_and_the_playlist_deleted_by_hand_is_kept_and_counted`
  - `tests/test_delete_landed_removed.py::test_only_a_landing_that_names_an_absent_row_and_shows_no_proof_is_counted`
  - `tests/test_delete_landed_removed.py::test_the_first_review_counts_a_landing_already_rolled_back`

Old text:

```
            rolled_back.append(frozenset(content_id for content_id, _columns in absent))
```

New text:

```
            pass
```

### `r1037.M10_landed_not_joined`

plan: leave the absent landed rows out of the removals, which is the defect R-1037 names

- File: `src/cratekit/deletion/run.py`
- Source: `r1037.json`, row `M10_landed_not_joined`
- Moved: the replace call collapsed onto one argument line; the landed absences are not joined, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 14 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned`

Old text:

```
        seen, removed=seen.removed + tuple(one.row(mark.absent[key]) for key, one in absent.items())
```

New text:

```
        seen, removed=seen.removed
```

### `r1037.M11_sightings_never_forgotten`

plan: tell the sightings no row is held, so a row a restore put back keeps its old number

- File: `src/cratekit/deletion/run.py`
- Source: `r1037.json`, row `M11_sightings_never_forgotten`
- Moved: the sight call collapsed onto one line; nothing is held present, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered`

Old text:

```
    mark = marks.sight(database_identity=identity, absent=absent, present=held, counter=counter)
```

New text:

```
    mark = marks.sight(database_identity=identity, absent=absent, present=(), counter=counter)
```

### `r1037.M12_playlists_always_held`

_playlists_held: answer every playlist held, so a rolled back landing is offered

- File: `src/cratekit/deletion/run.py`
- Source: `r1037.json`, row `M12_playlists_always_held`
- Moved: the once only playlist read is now functools.cache over the ids; every playlist reads as held, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 8 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_one_of_whose_playlists_is_gone_offers_nothing`
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_restore_to_before_the_landing_offers_nothing_and_the_screen_counts_it`
  - `tests/test_delete_landed_removed.py::test_a_rolled_back_landing_is_kept_by_its_playlist_whatever_the_count`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_every_row_gone_and_the_playlist_deleted_by_hand_is_kept_and_counted`
  - `tests/test_delete_landed_removed.py::test_the_first_review_counts_a_landing_already_rolled_back`

Old text:

```
    return lambda playlist_id: playlist_id in ids()
```

New text:

```
    return lambda playlist_id: True
```

### `r1037.M9_recorded_not_excluded`

plan: a row sync removed recorded is read again as a landed absence, so one row is two candidates

- File: `src/cratekit/deletion/run.py`
- Source: `r1037.json`, row `M9_recorded_not_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`

Old text:

```
        present=held | {row.content_id for row in recorded},
```

New text:

```
        present=held,
```

### `r1844.N14_uuids_not_passed`

run.plan: the held rows' UUIDs are not handed to the landed row reader

- File: `src/cratekit/deletion/run.py`
- Source: `r1844.json`, row `N14_uuids_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 4 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`

Old text:

```
        uuids=seen.uuids,
```

New text:

```
        uuids={},
```

### `r1844.N15_baseline_count_lost`

run.plan: the run that baselines carries no rolled back count

- File: `src/cratekit/deletion/run.py`
- Source: `r1844.json`, row `N15_baseline_count_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_the_first_review_counts_a_landing_already_rolled_back`

Old text:

```
            baselined_over=len(seen.removed),
            rolled_back=landings.unasked(mark.absent),
```

New text:

```
            baselined_over=len(seen.removed),
```

### `r1844.N16_review_count_lost`

run.plan: an ordinary review carries no rolled back count

- File: `src/cratekit/deletion/run.py`
- Source: `r1844.json`, row `N16_review_count_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_restore_to_before_the_landing_offers_nothing_and_the_screen_counts_it`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_every_row_gone_and_the_playlist_deleted_by_hand_is_kept_and_counted`

Old text:

```
        ambiguous=ambiguous,
        rolled_back=landings.unasked(mark.absent),
```

New text:

```
        ambiguous=ambiguous,
```

### `r44-b.R1_rules_drop_identity`

Build the pass's rules from configuration without each rule's recorded identity

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `R1_rules_drop_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_the_rules_the_pass_builds_from_configuration_carry_each_recorded_identity`

Old text:

```
        locations.PrefixRule(source, target, volume_id)
```

New text:

```
        locations.PrefixRule(source, target)
```

### `r44-b.R2_no_gate_at_the_plan`

Drop the assertion of every mapped target before the plan resolves a path

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `R2_no_gate_at_the_plan`
- Moved: the seams now travel as one mapping and the call is one line; it is deleted, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_deletion.py::test_a_file_under_the_library_root_asks_nothing_of_any_rule_before_it_moves`
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`
  - `tests/test_deletion.py::test_a_volume_holding_only_removed_rows_does_not_settle_off_an_empty_mount_point`

Old text:

```
    session.assert_mapped_volume_identities(cfg, rules, **seams)

```

New text:

```
(empty)
```

### `r44-b.R3_no_look_at_the_loop_top`

Drop the look at the top of the apply loop, before a retirement or a settlement of the plan's answer

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `R3_no_look_at_the_loop_top`
- Moved: the seven line volume call became a functools.partial named look, bound to the configuration, the rules and the seams; the loop top's call is deleted, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_retires_nothing_nobody_answered_for`
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`

Old text:

```
            look(item)

```

New text:

```
(empty)
```

### `r44-b.R4_no_look_after_the_recheck`

Drop the look after the re-check, before its answer is settled or moved on

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `R4_no_look_after_the_recheck`
- Moved: the same partial; the call after the re-check is deleted, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`

Old text:

```
            look(fresh)

```

New text:

```
(empty)
```

### `r44-b.R5_both_looks_gone`

Composite for R3 and R4: make the per file look a no-op, so only the plan's gate stands

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `R5_both_looks_gone`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_retires_nothing_nobody_answered_for`
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_stops_a_confirmed_move`
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_deletion.py::test_a_file_in_a_volume_nested_under_the_rules_target_is_not_moved`

Old text:

```
    if answered.resolved is None:
        return
    resolved = locations.resolve_recorded_path(
```

New text:

```
    return
    resolved = locations.resolve_recorded_path(
```

### `r44-b.X1_library_root_gate`

Existing guard, sampled: drop the library root's own volume assertion from the pass

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `X1_library_root_gate`
- Moved: the seams now travel as one mapping; the library root's identity check is deleted, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_decoy_volume_at_the_configured_path_refuses_before_anything_resolves`

Old text:

```
    session.assert_volume_identity(cfg, **seams)
    session.assert_mapped_volume_identities(cfg, rules, **seams)
```

New text:

```
    session.assert_mapped_volume_identities(cfg, rules, **seams)
```

### `r44-b.X2_suspect_anchor`

Existing guard, sampled: never hold a row because its anchor proved nothing

- File: `src/cratekit/deletion/run.py`
- Source: `r44-b.json`, row `X2_suspect_anchor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_stale_empty_mount_point_writes_no_tombstone_and_retires_no_row`
  - `tests/test_deletion.py::test_an_unanswered_removal_under_a_stale_mount_point_is_not_retired_either`

Old text:

```
    return answered.anchor is not None and answered.anchor in references.suspect_anchors
```

New text:

```
    return False
```

### `u310.A10_unrecorded_move_put_back`

apply: a move whose tombstone cannot be written is left in the Trash

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A10_unrecorded_move_put_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 5 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_file_that_cannot_be_put_back_refuses_naming_both_paths`
  - `tests/test_deletion.py::test_a_tombstone_that_cannot_be_written_puts_the_file_back`
  - `tests/test_deletion.py::test_an_interrupt_during_the_store_write_still_puts_the_file_back[ctrl-c]`
  - `tests/test_deletion.py::test_an_interrupt_during_the_store_write_still_puts_the_file_back[sigterm]`
  - `tests/test_deletion.py::test_an_interrupt_while_putting_the_file_back_still_names_both_paths`

Old text:

```
            trash.recover(target, original)
```

New text:

```
            pass
```

### `u310.A11_unproved_anchor_retires_nothing`

apply: an unanswered removal whose anchor proved nothing still retires its row

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A11_unproved_anchor_retires_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_an_unanswered_removal_under_a_stale_mount_point_is_not_retired_either`

Old text:

```
                return item.handled and not held
```

New text:

```
                return item.handled
```

### `u310.A12_only_answered_items_move`

_verdicts: keep unanswered items, so a file nobody confirmed reaches the move

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A12_only_answered_items_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_an_item_nobody_has_answered_holds_the_watermark_where_it_is`

Old text:

```
            if item.resolved
```

New text:

```
            if True
```

### `u310.A13_fresh_playlist_read`

apply: the re-check reads no playlist, so a file a playlist took after the plan is moved

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A13_fresh_playlist_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_decline_recorded_between_the_plan_and_the_move_stops_the_move`
  - `tests/test_deletion.py::test_a_playlist_that_takes_the_file_after_the_plan_stops_the_move`

Old text:

```
        referenced = library.playlist_referenced(db.get_playlist_songs())
```

New text:

```
        referenced = frozenset()
```

### `u310.A14_reference_set_complete`

plan: drop the completeness check of the reference set, so a dead prefix rule proves candidates unreferenced

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A14_reference_set_complete`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`
- Collected: 353 against a baseline of 353
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_dead_prefix_rule_stops_the_whole_pass_before_anything_is_offered`
  - `tests/test_deletion_streaming.py::test_delete_review_still_refuses_an_unmapped_local_row_beside_streaming_rows`

Old text:

```
    candidate_rules.assert_complete(references)

```

New text:

```
(empty)
```

### `u310.A1_gates_asserted`

apply: run without the session gates

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A1_gates_asserted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_the_apply_refuses_without_the_backup_acknowledgment`

Old text:

```
    with session.assert_gates(cfg, workflow=DELETION_WORKFLOW, analysis_roots=watched, **seams):
```

New text:

```
    with __import__("contextlib").nullcontext():
```

### `u310.A2_volume_before_the_answer`

apply: act on an answer without asserting the volume first

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A2_volume_before_the_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_retires_nothing_nobody_answered_for`
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`

Old text:

```
            look(item)
            verdict = decided.get(_item_id(item))
```

New text:

```
            verdict = decided.get(_item_id(item))
```

### `u310.A3_reject_moves_nothing`

apply: a rejected answer is not recorded as a decline and falls through to the move

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A3_reject_moves_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_rejected_item_becomes_a_decline_and_the_file_stays`
  - `tests/test_deletion.py::test_a_revoke_that_cannot_reopen_the_item_leaves_the_decline_standing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_revoking_a_decline_puts_the_file_back_in_front_of_a_person`

Old text:

```
            if verdict.verdict is review.Verdict.REJECTED:
```

New text:

```
            if False:
```

### `u310.A4_planned_deletable`

apply: skip the plan's own refusal of a row no longer deletable

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A4_planned_deletable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`

Old text:

```
            if not item.deletable:
```

New text:

```
            if False:
```

### `u310.A5_fresh_decline_snapshot`

apply: the re-check ignores a decline recorded after the plan

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A5_fresh_decline_snapshot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_decline_recorded_between_the_plan_and_the_move_stops_the_move`

Old text:

```
                declined=declined_now,
```

New text:

```
                declined=lambda _row: False,
```

### `u310.A7_recheck_still_deletable`

apply: move a file the re-check no longer calls deletable

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A7_recheck_still_deletable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_playlist_that_takes_the_file_after_the_plan_stops_the_move`

Old text:

```
            if not fresh.deletable or fresh.resolved is None:
```

New text:

```
            if fresh.resolved is None:
```

### `u310.A8_shown_path_is_the_moved_path`

apply: move a file whose path differs from the one the person confirmed

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A8_shown_path_is_the_moved_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_corrected_prefix_rule_lets_the_confirmed_deletion_through_on_the_retry`
  - `tests/test_deletion.py::test_a_verdict_does_not_travel_to_whatever_the_row_resolves_to_later`

Old text:

```
            if shown and locations.norm_for_compare(shown) != locations.norm_for_compare(
```

New text:

```
            if False and locations.norm_for_compare(shown) != locations.norm_for_compare(
```

### `u310.A9_volume_refusal_stops_the_run`

apply: a Trash refusal of any scope costs one file rather than stopping the run

- File: `src/cratekit/deletion/run.py`
- Source: `u310.json`, row `A9_volume_refusal_stops_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_trash_refusal_wider_than_one_name_stops_the_run`

Old text:

```
                if exc.cause.scope is not Scope.ITEM:
```

New text:

```
                if False:
```

### `u27-reports-round-3-fixes.F4_absent_flag_never_set`

Never mark an absent Trash as absent, so doctor cannot tell it from an unwritable one

- File: `src/cratekit/deletion/trash.py`
- Source: `u27-reports-round-3-fixes.json`, row `F4_absent_flag_never_set`
- Moved: the call collapsed onto one argument line; the absent flag is never set, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_two_probe_answers_that_made_the_false_red_are_really_different`

Old text:

```
            layout, False, f"{target} is not a directory", absent=not target.exists()
```

New text:

```
            layout, False, f"{target} is not a directory", absent=False
```

### `u310.T1_trash_usable`

assert_usable: accept a Trash the probe called unusable

- File: `src/cratekit/deletion/trash.py`
- Source: `u310.json`, row `T1_trash_usable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_trash_on_another_filesystem_is_refused_before_a_byte_moves`
  - `tests/test_deletion.py::test_a_volume_with_no_usable_trash_refuses_rather_than_deleting`

Old text:

```
    if not status.usable or status.layout is None:
```

New text:

```
    if status.layout is None:
```

### `r1037.M13_sight_renumbers`

sight: number a row again at every run, so it moves past every advance and is offered again

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M13_sight_renumbers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 3 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_an_advance_and_a_rebaseline_keep_and_drop_the_sightings_as_their_database_says`

Old text:

```
                if content_id in kept or content_id in held:
                    continue
                kept[str(content_id)] = int(counter)
```

New text:

```
                if content_id in held:
                    continue
                kept[str(content_id)] = int(counter)
```

### `r1037.M14_sight_at_the_watermark`

sight: number a new sighting at the watermark, so every outright removal is hidden

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M14_sight_at_the_watermark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 15 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered`
  - `tests/test_delete_landed_removed.py::test_an_advance_and_a_rebaseline_keep_and_drop_the_sightings_as_their_database_says`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned`

Old text:

```
                kept[str(content_id)] = int(counter)
```

New text:

```
                kept[str(content_id)] = existing.sequence
```

### `r1037.M15_sight_keeps_held`

sight: drop no sighting of a row held again

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M15_sight_keeps_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 2 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_row_restored_live_is_forgotten_and_its_second_removal_is_offered`
  - `tests/test_delete_landed_removed.py::test_an_advance_and_a_rebaseline_keep_and_drop_the_sightings_as_their_database_says`

Old text:

```
            kept = {key: value for key, value in existing.absent.items() if key not in held}
```

New text:

```
            kept = dict(existing.absent)
```

### `r1037.M16_advance_drops_sightings`

advance: write the position without the sightings, so the next run renumbers and re-offers

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M16_advance_drops_sightings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 2 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_an_advance_and_a_rebaseline_keep_and_drop_the_sightings_as_their_database_says`

Old text:

```
                absent=dict(existing.absent) if existing is not None else {},
```

New text:

```
                absent={},
```

### `r1037.M17_sightings_unchecked`

_recognize: accept sightings of any shape

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M17_sightings_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_the_watermark_reads_version_one_as_no_sightings_and_refuses_a_bad_one`

Old text:

```
        if not isinstance(absent, Mapping):
            raise self._unusable(f"its sightings are a {type(absent).__name__}, not a mapping")
```

New text:

```
        if not isinstance(absent, Mapping):
            absent = {}
```

### `r1037.M18_sighting_value_unchecked`

_recognize: accept a sighting that is not a whole number

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M18_sighting_value_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_the_watermark_reads_version_one_as_no_sightings_and_refuses_a_bad_one`

Old text:

```
            if isinstance(sighted, bool) or not isinstance(sighted, int):
```

New text:

```
            if False:
```

### `r1037.M19_version_two_refused`

_recognize: read only version 1, so this build refuses its own document

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M19_version_two_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`
- Collected: 373 against a baseline of 373
- Kills: 111 (killed)
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
  - ... and 96 more, see the JSON sidecar

Old text:

```
READABLE_VERSIONS = frozenset({1, WATERMARK_VERSION})
```

New text:

```
READABLE_VERSIONS = frozenset({1})
```

### `u270.C1_export_names_its_batch_form`

export cli: the per item worker names no batch form

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C1_export_names_its_batch_form`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_the_export_worker_names_its_batch_form_at_the_providers_add_limit`

Old text:

```
handle.batched = (handle_batch, BATCH)  # type: ignore[attr-defined]
```

New text:

```
handle.unbatched = (handle_batch, BATCH)  # type: ignore[attr-defined]
```

### `u51-item-derivation.H3_frozen_config_ignored`

KTD9: the export handler loads a fresh configuration instead of using the frozen one

- File: `src/cratekit/export/cli.py`
- Source: `u51-item-derivation.json`, row `H3_frozen_config_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_no_declared_handler_loads_a_fresh_configuration`

Old text:

```
    report = run_export_item(payload, str(item.item_id), cfg, account.resolve(cfg))
```

New text:

```
    report = run_export_item(
        payload, str(item.item_id), config.load(), account.resolve(cfg)
    )
```

### `u142.S8_gate_stale_said_without_a_write`

export archive gate: say a stale record is replaced even when nothing is written

- File: `src/cratekit/export/set_archive.py`
- Source: `u142.json`, row `S8_gate_stale_said_without_a_write`
- Moved: the same text, now in src/cratekit/export/set_archive.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`

Old text:

```
    if planned.stale_folder and planned.writes:
```

New text:

```
    if planned.stale_folder:
```

### `r837-b.B5_unmatched_warning`

set_cli._unmatched_warnings: a set that left tracks out answers with no warning naming them (R-850)

- File: `src/cratekit/export/set_cli.py`
- Source: `r837-b.json`, row `B5_unmatched_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_approved_the_account_holds_a_private_playlist_of_four_in_order`
  - `tests/test_export_set.py::test_five_rows_with_one_unmatched_plan_four_and_name_the_fifth`

Old text:

```
    if not planned.unmatched:
        return []
    return [
```

New text:

```
    if True:
        return []
    return [
```

### `u309-z.U14_backfill_abort_writes_nothing`

A backfill whose gate was aborted applies its plans anyway

- File: `src/cratekit/export/set_cli.py`
- Source: `u309-z.json`, row `U14_backfill_abort_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_backfill_whose_gate_was_aborted_applies_nothing`

Old text:

```
    if option != "apply" or not payload["totals"]["writes"]:
```

New text:

```
    if not payload["totals"]["writes"]:
```

### `u309-z.U15_backfill_skips_planless`

A backfill applies a plan that writes nothing

- File: `src/cratekit/export/set_cli.py`
- Source: `u309-z.json`, row `U15_backfill_skips_planless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_backfill_skips_the_planless_and_names_only_what_wrote`

Old text:

```
            if not one.writes:
                continue
            _data, more, wrote = apply(cfg, one)
```

New text:

```
            _data, more, wrote = apply(cfg, one)
```

### `u309-z.U16_backfill_names_only_what_wrote`

A backfill names a set as done though its apply wrote nothing

- File: `src/cratekit/export/set_cli.py`
- Source: `u309-z.json`, row `U16_backfill_names_only_what_wrote`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_backfill_skips_the_planless_and_names_only_what_wrote`

Old text:

```
            if wrote:
                done.append(one.name)
```

New text:

```
            done.append(one.name)
```

### `u309-z.U17_backfill_first_failure_raised_as_is`

A backfill failing before anything landed is wrapped as a part way failure rather than raised as it was

- File: `src/cratekit/export/set_cli.py`
- Source: `u309-z.json`, row `U17_backfill_first_failure_raised_as_is`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_backfill_failing_before_anything_landed_raises_it_as_is`

Old text:

```
        if not done:
            raise
        before = f"before this failed the backfill already {said.did} {', '.join(done)}"
```

New text:

```
        before = f"before this failed the backfill already {said.did} {', '.join(done)}"
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

### `r572.Z1_set_drop_album`

export set stops passing the album to match_track

- File: `src/cratekit/export/set_match.py`
- Source: `r572.json`, row `Z1_set_drop_album`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_held_files_album_tag_is_handed_to_the_account_with_its_isrc`

Old text:

```
                    remote, said = _isrc_match(
                        account, identity, one, code, agree=True, album=album
                    )
```

New text:

```
                    remote, said = _isrc_match(
                        account, identity, one, code, agree=True
                    )
```

### `r837-b.B1_ref_only_from_the_provider`

set_cli.match_rows: a list document's row identifier is trusted whatever its origin, so a Spotify id is handed to the account

- File: `src/cratekit/export/set_match.py`
- Source: `r837-b.json`, row `B1_ref_only_from_the_provider`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_another_sources_identifier_is_never_handed_to_the_account`

Old text:

```
            if one.ref and one.origin == match.TIDAL:
```

New text:

```
            if one.ref:
```

### `r837-b.B2_isrc_route`

set_cli.match_rows: a row's ISRC is never asked of the account, so it goes to the text search

- File: `src/cratekit/export/set_match.py`
- Source: `r837-b.json`, row `B2_isrc_route`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match`

Old text:

```
            if one.isrc:
```

New text:

```
            if False:
```

### `r837-b.B3_accepted_in_review`

set_cli.match_rows: a candidate accepted in review is not used, so the row is left out

- File: `src/cratekit/export/set_match.py`
- Source: `r837-b.json`, row `B3_accepted_in_review`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_candidate_accepted_in_review_is_used_and_not_searched_for_again`
  - `tests/test_export_set.py::test_a_persons_answer_in_review_wins_over_the_librarys_file`

Old text:

```
                if answered.state == candidates.ACCEPTED and answered.track is not None:
```

New text:

```
                if False:
```

### `r837-b.B4_sole_exact_listed`

set_cli.match_rows: the one exact search candidate is never listed, so every typed row is left out

- File: `src/cratekit/export/set_match.py`
- Source: `r837-b.json`, row `B4_sole_exact_listed`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 20 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_a_name_with_a_slash_finds_the_set_it_named_at_build`
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_export_set.py::test_an_exact_match_on_the_second_page_alone_is_listed`
  - `tests/test_export_set.py::test_approved_the_account_holds_a_private_playlist_of_four_in_order`
  - ... and 5 more, see the JSON sidecar

Old text:

```
            sole = candidates.sole_exact(answer)
```

New text:

```
            sole = None
```

### `r879-b.S10_unnamed_exact_said_to_resemble_nothing`

_not_chosen: count only identified exact matches before saying none resembles it

- File: `src/cratekit/export/set_match.py`
- Source: `r879-b.json`, row `S10_unnamed_exact_said_to_resemble_nothing`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_exact_match_with_no_identifier_is_not_said_to_resemble_nothing`

Old text:

```
        if any(one.exact for one in answer.candidates):
```

New text:

```
        if exact:
```

### `r879-b.S4_several_codes_take_one`

file_isrc: take one of several distinct codes the held copies carry

- File: `src/cratekit/export/set_match.py`
- Source: `r879-b.json`, row `S4_several_codes_take_one`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_held_copies_carrying_different_isrcs_ask_the_account_nothing`

Old text:

```
        if len(codes) == 1:
```

New text:

```
        if codes:
```

### `r879-b.S5_codes_from_every_version`

file_isrc: read the code of every held version, not only the matched files

- File: `src/cratekit/export/set_match.py`
- Source: `r879-b.json`, row `S5_codes_from_every_version`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_another_versions_isrc_is_not_the_rows`

Old text:

```
            if str(held.path) in paths and held.isrc
```

New text:

```
            if held.isrc
```

### `r879-b.S6_absent_music_folder_unsaid`

file_isrc: drop the absent music folder check, so an unmounted volume reads as a library holding nothing

- File: `src/cratekit/export/set_match.py`
- Source: `r879-b.json`, row `S6_absent_music_folder_unsaid`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_absent_music_folder_is_said_and_never_read_as_holding_nothing`

Old text:

```
        if not self.music.is_dir():
```

New text:

```
        if False:
```

### `r879-b.S7_library_before_a_persons_answer`

match_rows: let the library's file pre-empt a person's answer in review

- File: `src/cratekit/export/set_match.py`
- Source: `r879-b.json`, row `S7_library_before_a_persons_answer`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_persons_answer_in_review_wins_over_the_librarys_file`

Old text:

```
            answered = candidates.settled(items, one)
```

New text:

```
            answered = None if not one.isrc and library.file_isrc(one)[0] else candidates.settled(items, one)
```

### `r879-b.S8_several_needs_three`

_not_chosen: say several only from three distinct exact matches

- File: `src/cratekit/export/set_match.py`
- Source: `r879-b.json`, row `S8_several_needs_three`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_second_distinct_exact_match_on_the_next_page_leaves_it_out_as_several`
  - `tests/test_export_set.py::test_two_exact_candidates_are_not_chosen_between`

Old text:

```
    elif exact > 1:
```

New text:

```
    elif exact > 2:
```

### `r879-b.S9_ambiguous_full_said_as_bound`

_not_chosen: say two readings only with an exact match, so a full first page of an ambiguous row is said as the bound

- File: `src/cratekit/export/set_match.py`
- Source: `r879-b.json`, row `S9_ambiguous_full_said_as_bound`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_title_read_two_ways_on_a_full_page_says_so_and_not_the_bound`

Old text:

```
    if answer.ambiguous and (exact or answer.full):
```

New text:

```
    if answer.ambiguous and exact:
```

### `r1017.M12_twin_message_names_to`

Refusal: name the held playlist under the new name rather than the name it is recorded under

- File: `src/cratekit/export/set_rename.py`
- Source: `r1017.json`, row `M12_twin_message_names_to`
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
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
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
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
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
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
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_playlist_the_archive_marked_is_refused_rather_than_retitled`

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

### `u146-a.B10_job_no_date_dated_by_account`

gather: a row whose job dated it nowhere is dated from the account, so the backfill and the landing file one heart in two places

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B10_job_no_date_dated_by_account`
- Moved: The nested check of a row frozen with no date key folded into one condition with the account's date; the same not heart.known test, turned into the job's no date the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`

Old text:

```
        if not heart.known and (when := listing.dates.get(heart.ref)) is not None:
```

New text:

```
        if heart.hearted is None and (when := listing.dates.get(heart.ref)) is not None:
```

### `u146-a.B11_listing_always_asked`

gather: the account is listed even when no heart needs placing

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B11_listing_always_asked`
- Moved: gather now answers an unplanned BackfillPlan rather than a Gathered; the same early return before the account is listed when no heart needs placing.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_an_unreadable_account_refuses_only_when_a_heart_needs_placing`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`

Old text:

```
    if not candidates:
        return replace(left, taken_back=tuple(taken), already=already)
```

New text:

```
    if not candidates and False:
        return replace(left, taken_back=tuple(taken), already=already)
```

### `u146-a.B12_landing_takes_keyless_rows`

owned_in_library: a row whose job froze no date key is placed by the landing, into Undated for good

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B12_landing_takes_keyless_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_owned_hearts_an_empty_landing_cannot_place_alone_are_no_write`

Old text:

```
    known = [row for row in rows if row.known and row.paths]
```

New text:

```
    known = [row for row in rows if row.paths]
```

### `u146-a.B1_carried_states`

carried: the backfill reads only the carried states again, so an owned heart is never placed

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B1_carried_states`
- Moved: The read of every hearts job's rows in every state moved into backfill.reported, which carried (and the split) now call; the same states=None argument, dropped the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 7 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`

Old text:

```
                rows.extend(account_playlists.carried_hearts(store, job, states=None))
```

New text:

```
                rows.extend(account_playlists.carried_hearts(store, job))
```

### `u146-a.B3_already_ignores_filed`

gather: a heart All Favorites holds is already placed whatever its month, so a heart with no month never takes one

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B3_already_ignores_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_a_heart_the_landing_placed_without_a_month_takes_it_from_the_backfill`

Old text:

```
        if content_id in in_source and content_id in filed:
```

New text:

```
        if content_id in in_source:
```

### `u146-a.B4_already_ignores_source`

gather: a heart a month holds is already placed whatever All Favorites holds, so a heart out of All Favorites is never put back nor named

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B4_already_ignores_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`

Old text:

```
        if content_id in in_source and content_id in filed:
```

New text:

```
        if content_id in filed:
```

### `u146-a.B5_removed_counts_a_live_row`

gather: a removed membership beside a live one reads as taken back, so a heart put back by hand never takes its month

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B5_removed_counts_a_live_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`

Old text:

```
    removed = placement.members_marked_removed(db, home.source_id) - in_source
```

New text:

```
    removed = placement.members_marked_removed(db, home.source_id)
```

### `u146-a.B9_whole_and_short_swapped`

gather: a heart a whole listing lacks is held back and one a short listing lacks is taken back

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B9_whole_and_short_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated`
  - `tests/test_favorites_backfill.py::test_a_heart_the_account_dates_nowhere_goes_to_undated_and_one_it_no_longer_carries_is_taken_back`
  - `tests/test_favorites_backfill.py::test_a_listing_with_no_published_count_holds_back_a_heart_it_lacks`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`

Old text:

```
            if listing.whole:
```

New text:

```
            if not listing.whole:
```

### `u146-b.B13_first_of_two_rows`

owned_in_library: a file two active rows claim answers with the first, so a duplicate import joins All Favorites by a guess

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-b.json`, row `B13_first_of_two_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_owned_hearts_an_empty_landing_cannot_place_alone_are_no_write`

Old text:

```
    by_path = native.single_rows_for(db, cfg, paths)
```

New text:

```
    by_path = native.content_ids_for(db, cfg, paths)
```

### `u146-b.B14_plan_owned_keeps_held_hearts`

plan_owned: an owned heart All Favorites holds is planned too, so an empty landing gives it a month

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-b.json`, row `B14_plan_owned_keeps_held_hearts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_owned_hearts_an_empty_landing_cannot_place_alone_are_no_write`

Old text:

```
        one for one in owned_in_library(cfg, db, rows) if one.content_id not in in_source
```

New text:

```
        one for one in owned_in_library(cfg, db, rows)
```

### `u153.B1_read_back_grey`

backfill _read_back: invert the Pink check, so a row that reads Pink is called a disagreement and the verb refuses

- File: `src/cratekit/favorites/backfill.py`
- Source: `u153.json`, row `B1_read_back_grey`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 21 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_carried_heart_whose_row_sits_deep_is_placed_now_the_path_rule_is_gone`
  - `tests/test_favorites_backfill.py::test_a_date_the_job_froze_wins_over_the_accounts`
  - `tests/test_favorites_backfill.py::test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_a_heart_the_account_dates_nowhere_goes_to_undated_and_one_it_no_longer_carries_is_taken_back`
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`
  - `tests/test_favorites_backfill.py::test_a_heart_two_jobs_carried_is_one_heart_with_the_dated_jobs_date`
  - `tests/test_favorites_backfill.py::test_a_hearts_job_whose_reports_cannot_be_read_is_skipped_and_named`
  - `tests/test_favorites_backfill.py::test_a_listing_with_no_published_count_holds_back_a_heart_it_lacks`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        if str(getattr(colour.find_row(db, row), colour.COLUMN, "") or "") != pink
```

New text:

```
        if str(getattr(colour.find_row(db, row), colour.COLUMN, "") or "") == pink
```

### `u153.B2_record_colour_only`

backfill record: do not record a colour-only commit, so a run that only coloured leaves no session record

- File: `src/cratekit/favorites/backfill.py`
- Source: `u153.json`, row `B2_record_colour_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`

Old text:

```
    if placed.added <= 0 and not placed.coloured:
```

New text:

```
    if placed.added <= 0:
```

### `u153.B3_member_order_isdigit`

backfill _member_order: sort every id as an int, so a non-numeric id raises and takes the plan down

- File: `src/cratekit/favorites/backfill.py`
- Source: `u153.json`, row `B3_member_order_isdigit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_member_order_is_numeric_and_tolerates_a_non_numeric_id`

Old text:

```
        content_ids, key=lambda c: (0, int(c), "") if str(c).isdigit() else (1, 0, str(c))
```

New text:

```
        content_ids, key=lambda c: (0, int(c), "")
```

### `r228-operator.D11_non_pink_outside`

union_with_pink: queue every export row, not only pink and playlist

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D11_non_pink_outside`
- Moved: The two dedup loops of union_with_pink became one dict.fromkeys over the playlist then the pink rows the export carries; the second source swapped for every export row the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_the_gate_names_colour_and_playlist_counts`
  - `tests/test_favorites_pink.py::test_union_leaves_non_pink_outside_playlist_out`
  - `tests/test_favorites_pink.py::test_union_names_pink_rows_the_export_lacks`
  - `tests/test_favorites_pink.py::test_union_offers_pink_outside_playlist_and_keeps_playlist_non_pink`

Old text:

```
        track_ids=tuple(dict.fromkeys([*playlist.track_ids, *in_export])),
```

New text:

```
        track_ids=tuple(dict.fromkeys([*playlist.track_ids, *library.entries])),
```

### `r228-operator.D12_missing_pink_queued`

union_with_pink: queue pink rows the export lacks

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D12_missing_pink_queued`
- Moved: The loop that split pink rows by whether the export carries them became a comprehension; the same membership test, dropped so every pink row is queued.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`
  - `tests/test_favorites_pink.py::test_union_names_pink_rows_the_export_lacks`

Old text:

```
    in_export = [track_id for track_id in pink_ids if track_id in library.entries]
```

New text:

```
    in_export = [track_id for track_id in pink_ids]
```

### `r228-operator.D4_union_playlist_first`

union_with_pink: emit pink only rows before playlist members

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D4_union_playlist_first`
- Moved: The two dedup loops became one dict.fromkeys whose order is the playlist then the pink rows; the same order, swapped so pink only rows come first.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`

Old text:

```
        track_ids=tuple(dict.fromkeys([*playlist.track_ids, *in_export])),
```

New text:

```
        track_ids=tuple(dict.fromkeys([*in_export, *playlist.track_ids])),
```

### `r228-operator.D5_pink_missing_dropped`

union_with_pink: drop pink rows the export lacks instead of naming them

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D5_pink_missing_dropped`
- Moved: The else branch that named a pink row the export lacks became the pink_missing comprehension; emptied the same way, so the missing rows are dropped instead of named.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`
  - `tests/test_favorites_pink.py::test_union_names_pink_rows_the_export_lacks`

Old text:

```
        pink_missing=tuple(track_id for track_id in pink_ids if track_id not in library.entries),
```

New text:

```
        pink_missing=(),
```

### `r228-operator.D6_empty_after_colour`

resolve_sweep: read colour before resolving the playlist, so empty All Favorites is rescued by pink

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D6_empty_after_colour`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_resolve_sweep_refuses_empty_favorites_before_colour`

Old text:

```
    library = source.read_library(exported)
    resolved = source.resolve(library, wanted)
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        pink_ids = read_pink_track_ids(loaded)
    return exported, union_with_pink(library, resolved, pink_ids)
```

New text:

```
    library = source.read_library(exported)
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        pink_ids = read_pink_track_ids(loaded)
    try:
        resolved = source.resolve(library, wanted)
    except Exception:
        resolved = source.ResolvedPlaylist(key=wanted, name=wanted, track_ids=())
    return exported, union_with_pink(library, resolved, pink_ids)
```

### `r228-operator.D7_colour_unread_warned`

resolve_sweep: swallow a colour read refusal and sweep the playlist alone

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D7_colour_unread_warned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_resolve_sweep_propagates_the_colour_reads_own_cause`

Old text:

```
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        pink_ids = read_pink_track_ids(loaded)
    return exported, union_with_pink(library, resolved, pink_ids)
```

New text:

```
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        try:
            pink_ids = read_pink_track_ids(loaded)
        except Exception:
            pink_ids = ()
    return exported, union_with_pink(library, resolved, pink_ids)
```

### `r228-operator.D8_from_colour_zero`

union_with_pink: always report from_colour as zero

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D8_from_colour_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 5 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`
  - `tests/test_favorites_pink.py::test_the_gate_names_colour_and_playlist_counts`
  - `tests/test_favorites_pink.py::test_union_leaves_non_pink_outside_playlist_out`
  - `tests/test_favorites_pink.py::test_union_names_pink_rows_the_export_lacks`
  - `tests/test_favorites_pink.py::test_union_offers_pink_outside_playlist_and_keeps_playlist_non_pink`

Old text:

```
        from_colour=len(in_export),
```

New text:

```
        from_colour=0,
```

### `r228-operator.D9_from_playlist_zero`

union_with_pink: always report from_playlist as zero

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D9_from_playlist_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`
  - `tests/test_favorites_pink.py::test_the_gate_names_colour_and_playlist_counts`
  - `tests/test_favorites_pink.py::test_union_leaves_non_pink_outside_playlist_out`
  - `tests/test_favorites_pink.py::test_union_offers_pink_outside_playlist_and_keeps_playlist_non_pink`

Old text:

```
        from_playlist=len(playlist.track_ids),
```

New text:

```
        from_playlist=0,
```

### `u153.C1_is_uncoloured_narrowed`

is_uncoloured: only None counts as unset, so a '0' colour reads coloured and is held not written

- File: `src/cratekit/favorites/colour.py`
- Source: `u153.json`, row `C1_is_uncoloured_narrowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_favorites_placement.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_the_colour_module_sorts_rows_by_what_they_carry`

Old text:

```
    return value in rb_writer.FIELD_EMPTIES[COLUMN]
```

New text:

```
    return value is None
```

### `u153.C2_sort_rows_dedup`

sort_rows: drop the seen check, so a row named twice is sorted and coloured twice

- File: `src/cratekit/favorites/colour.py`
- Source: `u153.json`, row `C2_sort_rows_dedup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_the_colour_module_sorts_rows_by_what_they_carry`

Old text:

```
        if key in seen:
            continue
```

New text:

```
        if False:
            continue
```

### `u153.C3_sort_rows_missing_row`

sort_rows: do not skip a row the handle cannot find, so an absent id reaches getattr

- File: `src/cratekit/favorites/colour.py`
- Source: `u153.json`, row `C3_sort_rows_missing_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_the_colour_module_sorts_rows_by_what_they_carry`

Old text:

```
        row = find_row(db, key)
        if row is None:
            continue
```

New text:

```
        row = find_row(db, key)
        if row is None:
            to_colour.append(key)
            continue
```

### `u153.C4_sort_rows_uncoloured_branch`

sort_rows: treat every row as uncoloured, so a coloured row is coloured not held

- File: `src/cratekit/favorites/colour.py`
- Source: `u153.json`, row `C4_sort_rows_uncoloured_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_favorites_placement.py`
- Collected: 98 against a baseline of 98
- Kills: 10 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`
  - `tests/test_favorites_backfill.py::test_a_member_coloured_by_hand_between_the_two_acts_is_refused_by_the_write`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_unreadable_account_refuses_only_when_a_heart_needs_placing`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_a_recolour_row_takes_pink_and_no_membership`
  - `tests/test_favorites_placement.py::test_a_row_coloured_by_hand_between_two_plans_moves_the_digest`
  - `tests/test_favorites_placement.py::test_the_colour_module_sorts_rows_by_what_they_carry`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`

Old text:

```
        if is_uncoloured(current):
            to_colour.append(key)
```

New text:

```
        if True:
            to_colour.append(key)
```

### `u153.C6_write_pink_fill_only`

write_pink: drop the is_uncoloured re-check, so a colour a person chose is overwritten

- File: `src/cratekit/favorites/colour.py`
- Source: `u153.json`, row `C6_write_pink_fill_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_the_colour_module_sorts_rows_by_what_they_carry`
  - `tests/test_favorites_placement.py::test_the_write_leaves_a_row_coloured_by_hand_after_the_plan`

Old text:

```
        if row is None or not is_uncoloured(getattr(row, COLUMN, None)):
            continue
```

New text:

```
        if row is None:
            continue
```

### `u153.C7_write_pink_reports_write`

write_pink: report every row as coloured, including one the policy skipped

- File: `src/cratekit/favorites/colour.py`
- Source: `u153.json`, row `C7_write_pink_reports_write`
- Moved: The policy's decision is compared where it is made rather than through a local; the same is WRITE test before a row is reported, negated the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_favorites_placement.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_a_recolour_row_takes_pink_and_no_membership`
  - `tests/test_favorites_placement.py::test_the_colour_module_sorts_rows_by_what_they_carry`
  - `tests/test_favorites_placement.py::test_the_write_colours_the_planned_rows_and_only_those`

Old text:

```
        if rb_writer.write_metadata_field(row, OWNER, COLUMN, pink) is rb_writer.Decision.WRITE:
            written.append(str(content_id))
```

New text:

```
        if rb_writer.write_metadata_field(row, OWNER, COLUMN, pink) is not rb_writer.Decision.WRITE:
            written.append(str(content_id))
```

### `u180.M14_root_refused`

plan: an All Favorites at the playlist root is not refused, so the verb answers over no folder

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M14_root_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_no_favorites_folder_refuses_by_name_and_writes_nothing`

Old text:

```
    if not home.folder_id:
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `u180.M15_digest_is_the_target_order`

identity: the digest covers the set of rows and not their order, so a target that moved keeps its digest

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M15_digest_is_the_target_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_digest_moves_when_the_target_order_moves_and_not_otherwise`

Old text:

```
            "order": [one.row for one in self.children],
```

New text:

```
            "order": sorted(one.row for one in self.children),
```

### `u180.M17_confined_seated_position`

order_violations: a seated row is not asked whether it took its planned position

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M17_confined_seated_position`
- Moved: The seated row checks became a comprehension feeding spine.drift; the same position test as its last condition, dropped the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[not-made]`

Old text:

```
        or int(row[seq_at] or 0) != slot
    ]
```

New text:

```
    ]
```

### `u180.M18_confined_unplanned_rows`

order_violations: any playlist row may change its position and bookkeeping, planned or not

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M18_confined_unplanned_rows`
- Moved: Which existing row may move its bookkeeping columns is now the predicate handed to spine.drift, which allows spine.BOOKKEEPING only where it holds; the same key in planned test, made true for every row.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[source-moved]`
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[unplanned-move]`

Old text:

```
        moves=lambda key: key in planned,
```

New text:

```
        moves=lambda key: True,
```

### `u180.M19_confined_memberships`

order_violations: a membership that changed is not a violation

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M19_confined_memberships`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[membership-changed]`

Old text:

```
        if before.memberships[key] != after.memberships[key]:
```

New text:

```
        if False:
```

### `u180.M21_confinement_called`

apply: the commit is not confined from SQL, so a write beyond the positions lands

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M21_confinement_called`
- Moved: The commit witness is now spine.witnessed, one indent shallower, and the one use of assert_order_confined was inlined as the spine.confined call it made over order_violations; the same confinement before the commit, replaced by a no-op the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_writer_refuses_an_order_that_reached_a_name`

Old text:

```
            spine.confined(
                db,
                lambda after: order_violations(
```

New text:

```
            (lambda *a, **k: None)(
                db,
                lambda after: order_violations(
```

### `u180.M22_read_back_compares`

_read_back: the folder read back is never compared with the plan, so a clean answer is given over any order

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M22_read_back_compares`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_read_back_names_a_folder_that_does_not_read_in_the_planned_order`

Old text:

```
    if found == wanted:
        return ()
```

New text:

```
    if True:
        return ()
```

### `u120.T2_naive_is_utc`

as_utc: a naive moment is returned as it is rather than taken as UTC

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u120.json`, row `T2_naive_is_utc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_frozen_date_reads_back_and_junk_reads_as_no_date`

Old text:

```
    if moment.tzinfo is None:
        return moment.replace(tzinfo=timezone.utc)
```

New text:

```
    if moment.tzinfo is None:
        return moment
```

### `u145.M1_month_off_by_one`

month_of: the month is off by one, October named 2026-09

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u145.json`, row `M1_month_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_split.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 113 against a baseline of 113
- Kills: 33 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_plan_over_a_library_already_placed_writes_nothing`
  - `tests/test_favorites_placement.py::test_a_row_named_twice_folds_to_its_first_mention`
  - `tests/test_favorites_placement.py::test_no_quarter_is_named_by_the_placement_any_more`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment0-2026-01]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment1-2026-03]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment2-2026-04]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment3-2026-10]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment4-2026-12]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment5-2026-07]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment6-2026-11]`
  - `tests/test_favorites_placement.py::test_the_month_is_the_utc_month[moment7-2027-01]`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_the_plan_reads_what_each_heart_already_has_and_what_it_would_make`
  - `tests/test_favorites_placement.py::test_the_plans_digest_covers_each_months_row_found_or_to_be_made`
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    return f"{utc.year:04d}-{utc.month:02d}"
```

New text:

```
    return f"{utc.year:04d}-{utc.month - 1:02d}"
```

### `u146-b.B16_undated_is_no_filing`

is_filing: Undated is not a filing playlist, so a heart the split filed there is given a second month

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u146-b.json`, row `B16_undated_is_no_filing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`

Old text:

```
        text == UNDATED
        or MONTH_LABEL
```

New text:

```
        False
        or MONTH_LABEL
```

### `u146-e.B17_month_label_wrong`

MONTH_LABEL: a month playlist does not read as a month, so every placed heart is planned again with nothing to add

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u146-e.json`, row `B17_month_label_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 5 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_unreadable_account_refuses_only_when_a_heart_needs_placing`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`

Old text:

```
MONTH_LABEL = re.compile(r"\d{4}-(?:0[1-9]|1[0-2])")
```

New text:

```
MONTH_LABEL = re.compile(r"\d{4}-(?:0[1-9]|1[0-2])-")
```

### `u180.M1_source_first`

folder_rank: All Favorites ranks as any other playlist, so it is no longer first

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u180.json`, row `M1_source_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_favorites_placement.py`
- Collected: 102 against a baseline of 102
- Kills: 11 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_folder_already_in_order_plans_no_writes_and_opens_no_gate`
  - `tests/test_favorites_order.py::test_a_folder_named_as_a_month_is_not_a_month`
  - `tests/test_favorites_order.py::test_a_folder_oldest_first_reads_newest_first_with_all_favorites_first_and_undated_last`
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_a_non_month_playlist_keeps_its_relative_place_after_the_months`
  - `tests/test_favorites_order.py::test_a_soft_deleted_month_is_neither_moved_nor_counted`
  - `tests/test_favorites_order.py::test_only_a_row_whose_position_changes_is_written`
  - `tests/test_favorites_order.py::test_the_order_takes_the_positions_the_live_children_hold_and_no_other`
  - `tests/test_favorites_order.py::test_the_read_back_names_a_folder_that_does_not_read_in_the_planned_order`
  - `tests/test_favorites_placement.py::test_the_folder_rank_reads_all_favorites_then_months_newest_first_then_undated[2026-11-True-True-rank1]`
  - `tests/test_favorites_placement.py::test_the_folder_rank_reads_all_favorites_then_months_newest_first_then_undated[All Favorites-True-True-rank0]`

Old text:

```
    if source:
        return (RANK_SOURCE, 0)
```

New text:

```
    if False:
        return (RANK_SOURCE, 0)
```

### `u180.M2_newest_first_sign`

folder_rank: the months rank oldest first, the order the brief replaces

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u180.json`, row `M2_newest_first_sign`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_favorites_placement.py`
- Collected: 102 against a baseline of 102
- Kills: 18 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_folder_already_in_order_plans_no_writes_and_opens_no_gate`
  - `tests/test_favorites_order.py::test_a_folder_oldest_first_reads_newest_first_with_all_favorites_first_and_undated_last`
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_a_non_month_playlist_keeps_its_relative_place_after_the_months`
  - `tests/test_favorites_order.py::test_a_second_run_after_the_order_asks_nothing`
  - `tests/test_favorites_order.py::test_a_soft_deleted_month_is_neither_moved_nor_counted`
  - `tests/test_favorites_order.py::test_only_a_row_whose_position_changes_is_written`
  - `tests/test_favorites_order.py::test_the_order_takes_the_positions_the_live_children_hold_and_no_other`
  - `tests/test_favorites_order.py::test_the_read_back_names_a_folder_that_does_not_read_in_the_planned_order`
  - `tests/test_favorites_order.py::test_the_splits_months_land_in_order`
  - `tests/test_favorites_order.py::test_the_verb_refuses_an_answer_the_read_back_does_not_hold`
  - `tests/test_favorites_order.py::test_the_writer_refuses_an_order_that_reached_a_name`
  - `tests/test_favorites_placement.py::test_a_month_made_in_a_folder_out_of_order_lands_above_every_older_month`
  - `tests/test_favorites_placement.py::test_a_newer_month_ranks_above_an_older_one_across_a_year`
  - `tests/test_favorites_placement.py::test_a_removed_sibling_keeps_its_position_when_a_month_is_seated`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        return (RANK_MONTH, -(int(year) * 12 + int(month)))
```

New text:

```
        return (RANK_MONTH, (int(year) * 12 + int(month)))
```

### `u180.M3_year_coefficient`

folder_rank: a year weighs ten months rather than twelve, so December reads above the January after it

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u180.json`, row `M3_year_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_favorites_placement.py`
- Collected: 102 against a baseline of 102
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_newer_month_ranks_above_an_older_one_across_a_year`
  - `tests/test_favorites_placement.py::test_the_folder_rank_reads_all_favorites_then_months_newest_first_then_undated[2025-12-False-True-rank3]`
  - `tests/test_favorites_placement.py::test_the_folder_rank_reads_all_favorites_then_months_newest_first_then_undated[2026-11-False-True-rank2]`

Old text:

```
        return (RANK_MONTH, -(int(year) * 12 + int(month)))
```

New text:

```
        return (RANK_MONTH, -(int(year) * 10 + int(month)))
```

### `u180.M4_month_must_be_plain`

folder_rank: a folder or smart list named as a month ranks as a month and is moved between the months

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u180.json`, row `M4_month_must_be_plain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_favorites_placement.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_folder_named_as_a_month_is_not_a_month`
  - `tests/test_favorites_placement.py::test_the_folder_rank_reads_all_favorites_then_months_newest_first_then_undated[2026-11-False-False-rank5]`

Old text:

```
    if plain and MONTH_LABEL.fullmatch(text) is not None:
```

New text:

```
    if MONTH_LABEL.fullmatch(text) is not None:
```

### `u180.M5_undated_rank`

folder_rank: Undated ranks with the other playlists rather than directly after the months

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u180.json`, row `M5_undated_rank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_favorites_placement.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_non_month_playlist_keeps_its_relative_place_after_the_months`
  - `tests/test_favorites_placement.py::test_the_folder_rank_reads_all_favorites_then_months_newest_first_then_undated[Undated-False-True-rank4]`

Old text:

```
    if plain and text == UNDATED:
        return (RANK_UNDATED, 0)
```

New text:

```
    if plain and text == UNDATED:
        return (RANK_OTHER, 0)
```

### `u180.M6_undated_after_others`

RANK_UNDATED: Undated reads after every other playlist rather than before them

- File: `src/cratekit/favorites/placeholders.py`
- Source: `u180.json`, row `M6_undated_after_others`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_a_non_month_playlist_keeps_its_relative_place_after_the_months`

Old text:

```
RANK_UNDATED = 2
```

New text:

```
RANK_UNDATED = 4
```

### `u120.P1_live_plain_attribute`

_live_plain: a folder or a smart playlist counts as plain

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P1_live_plain_attribute`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_smart_playlist_of_the_months_name_is_not_written_to_and_a_plain_one_is_made`
  - `tests/test_favorites_placement.py::test_no_source_or_two_or_the_wrong_kind_refuses_under_u119s_reason[folder]`
  - `tests/test_favorites_placement.py::test_no_source_or_two_or_the_wrong_kind_refuses_under_u119s_reason[smart]`
  - `tests/test_favorites_placement.py::test_the_home_is_the_one_plain_live_source_its_folder_and_the_months_there`

Old text:

```
if int(getattr(row, "Attribute", -1) or 0) == 0 and not rb_writer.node_removed(row)
```

New text:

```
if int(getattr(row, "Attribute", -1) or 0) >= 0 and not rb_writer.node_removed(row)
```

### `u120.P2_two_sources_accepted`

resolve_home: two live sources are accepted and the first chosen

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P2_two_sources_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_playlist_of_the_sources_name_inside_deadca7s_folder_is_not_a_second_source`
  - `tests/test_favorites_placement.py::test_no_source_or_two_or_the_wrong_kind_refuses_under_u119s_reason[two]`

Old text:

```
    if len(live) != 1:
        count =
```

New text:

```
    if len(live) < 1:
        count =
```

### `u120.P4_into_source_always`

plan_placements: every heart is planned into the source whether it is there or not

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P4_into_source_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_plan_over_a_library_already_placed_writes_nothing`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_the_plan_reads_what_each_heart_already_has_and_what_it_would_make`

Old text:

```
                into_source=key not in in_source,
```

New text:

```
                into_source=True,
```

### `u120.P7_bypass_only_when_absent`

place: the source memberships are inserted directly rather than through add_memberships

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P7_bypass_only_when_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_members_marked_removedhip_in_the_month_is_added_again_live`
  - `tests/test_favorites_placement.py::test_place_adds_to_the_source_and_to_each_month_making_an_absent_one`
  - `tests/test_favorites_placement.py::test_placing_the_same_heart_twice_adds_nothing_twice`

Old text:

```
    added_source = len(rb_writer.add_memberships(db, source, ordered))
```

New text:

```
    added_source = 0
    for content_id in ordered:
        db.add_to_playlist(source, content_id)
        added_source += 1
```

### `u120.P8_source_name_default`

source_name: the outbound default is answered whatever the class declares

- File: `src/cratekit/favorites/placement.py`
- Source: `u120.json`, row `P8_source_name_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_the_source_is_the_classs_playlist_else_the_outbound_default`

Old text:

```
    if sub is not None and sub.signal_playlist:
        return sub.signal_playlist
    return outbound_source.DEFAULT_FAVORITES_PLAYLIST
```

New text:

```
    del sub
    return outbound_source.DEFAULT_FAVORITES_PLAYLIST
```

### `u145.M2_placement_undated`

plan_placements: every heart is planned into Undated, its date ignored

- File: `src/cratekit/favorites/placement.py`
- Source: `u145.json`, row `M2_placement_undated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_favorites_placement.py`
- Collected: 98 against a baseline of 98
- Kills: 21 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_carried_heart_whose_row_sits_deep_is_placed_now_the_path_rule_is_gone`
  - `tests/test_favorites_backfill.py::test_a_date_the_job_froze_wins_over_the_accounts`
  - `tests/test_favorites_backfill.py::test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_a_heart_the_landing_placed_without_a_month_takes_it_from_the_backfill`
  - `tests/test_favorites_backfill.py::test_a_heart_two_jobs_carried_is_one_heart_with_the_dated_jobs_date`
  - `tests/test_favorites_backfill.py::test_a_hearts_job_whose_reports_cannot_be_read_is_skipped_and_named`
  - `tests/test_favorites_backfill.py::test_a_listing_with_no_published_count_holds_back_a_heart_it_lacks`
  - `tests/test_favorites_backfill.py::test_a_month_playlist_deleted_between_the_plan_and_the_write_is_another_plan`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_backfill.py::test_the_plan_lists_exactly_the_landed_hearts_and_the_approval_places_them`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        month = placeholders.month_label(hearted)
```

New text:

```
        month = placeholders.month_label(None)
```

### `u146-b.B15_any_playlist_files`

filed: any playlist beside the source files a heart, so one at the root beside another playlist never takes its month

- File: `src/cratekit/favorites/placement.py`
- Source: `u146-b.json`, row `B15_any_playlist_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`

Old text:

```
        if row != home.source_id and placeholders.is_filing(name):
```

New text:

```
        if row != home.source_id:
```

### `u153.P1_into_colour_flag`

plan_placements: never mark a placement for colour, so no heart takes Pink

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P1_into_colour_flag`
- Moved: The placements are rebuilt with dataclasses.replace rather than field by field; the same into_colour flag from the rows the colour read says take Pink, set False the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_favorites_placement.py`
- Collected: 98 against a baseline of 98
- Kills: 11 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`
  - `tests/test_favorites_backfill.py::test_a_member_coloured_by_hand_between_the_two_acts_is_refused_by_the_write`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_unreadable_account_refuses_only_when_a_heart_needs_placing`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_a_heart_named_as_a_heart_is_not_listed_again_as_a_recolour`
  - `tests/test_favorites_placement.py::test_a_row_coloured_by_hand_between_two_plans_moves_the_digest`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_the_write_colours_the_planned_rows_and_only_those`
  - `tests/test_favorites_placement.py::test_the_write_leaves_a_row_coloured_by_hand_after_the_plan`

Old text:

```
replace(one, into_colour=one.content_id in takes)
```

New text:

```
replace(one, into_colour=False)
```

### `u153.P3_writes_colours`

PlacementPlan.writes: ignore the colour count, so a colour-only plan reports no write and ends NO_OP

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P3_writes_colours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_favorites_placement.py`
- Collected: 98 against a baseline of 98
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_a_recolour_row_takes_pink_and_no_membership`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`

Old text:

```
        return self.adds > 0 or self.colours > 0
```

New text:

```
        return self.adds > 0
```

### `u153.P4_identity_pink`

identity: drop the Pink row from the digest, so a colour change between plan and write is not caught

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P4_identity_pink`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`

Old text:

```
            "pink": self.pink,
```

New text:

```
            "pink": "",
```

### `u153.P5_recolour_dedup`

plan_placements recolour: drop the not-in-seen check, so a heart also named as a recolour is listed twice

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P5_recolour_dedup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_favorites_placement.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_placement.py::test_a_heart_named_as_a_heart_is_not_listed_again_as_a_recolour`

Old text:

```
            if row in titles and row not in seen
```

New text:

```
            if row in titles
```

### `u153.P6_place_pink_guard`

place: colour even with no Pink id, so write_pink blanks a colour by setting it to the empty id

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P6_place_pink_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_with_no_pink_row_the_plan_places_and_colours_nothing_and_says_why`
  - `tests/test_intake_land_hearts_native.py::test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made`

Old text:

```
    if pink and to_colour:
```

New text:

```
    if to_colour:
```

### `u180.M11_new_month_seated`

month_row: a month made under the folder is left at the end, the behaviour before U180

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M11_new_month_seated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_favorites_placement.py`
- Collected: 102 against a baseline of 102
- Kills: 6 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_the_splits_months_land_in_order`
  - `tests/test_favorites_placement.py::test_a_month_is_never_seated_above_all_favorites`
  - `tests/test_favorites_placement.py::test_a_month_made_in_a_folder_out_of_order_lands_above_every_older_month`
  - `tests/test_favorites_placement.py::test_a_removed_sibling_keeps_its_position_when_a_month_is_seated`
  - `tests/test_favorites_placement.py::test_place_makes_a_new_month_directly_under_all_favorites_in_an_ordered_folder`

Old text:

```
    if parent is not None:
        _seat_new(db, made, parent_id, source_id)
```

New text:

```
    if False:
        _seat_new(db, made, parent_id, source_id)
```

### `u180.M12_new_month_knows_the_source`

_seat_new: the month just made is ranked as any other playlist, so it is seated at the end of the folder

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M12_new_month_knows_the_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_favorites_placement.py`
- Collected: 102 against a baseline of 102
- Kills: 5 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_landing_that_makes_a_new_month_puts_it_directly_under_all_favorites`
  - `tests/test_favorites_order.py::test_the_splits_months_land_in_order`
  - `tests/test_favorites_placement.py::test_a_month_made_in_a_folder_out_of_order_lands_above_every_older_month`
  - `tests/test_favorites_placement.py::test_a_removed_sibling_keeps_its_position_when_a_month_is_seated`
  - `tests/test_favorites_placement.py::test_place_makes_a_new_month_directly_under_all_favorites_in_an_ordered_folder`

Old text:

```
    mine = rank(made, source_id)
```

New text:

```
    mine = (placeholders.RANK_OTHER, 0)
```

### `u180.M13_never_above_all_favorites`

_seat_new: the slot is looked for from the top of the folder, so a month can be seated above All Favorites, the round one finding

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M13_never_above_all_favorites`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_month_is_never_seated_above_all_favorites`

Old text:

```
        (n for n, row in enumerate(others) if n >= floor and rank(row, source_id) > mine),
```

New text:

```
        (n for n, row in enumerate(others) if rank(row, source_id) > mine),
```

### `u180.M7_children_live_only`

children: a soft deleted child is read, ranked and moved like a live one

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M7_children_live_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_favorites_placement.py`
- Collected: 102 against a baseline of 102
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_soft_deleted_month_is_neither_moved_nor_counted`
  - `tests/test_favorites_order.py::test_the_order_takes_the_positions_the_live_children_hold_and_no_other`
  - `tests/test_favorites_placement.py::test_a_removed_sibling_keeps_its_position_when_a_month_is_seated`

Old text:

```
        for row in db.get_playlist(ParentID=str(folder_id))
        if not rb_writer.node_removed(row)
```

New text:

```
        for row in db.get_playlist(ParentID=str(folder_id))
        if True
```

### `u180.M8_slots_lift_shared`

slots: a position two rows share is not lifted apart, so the order is written with a tie rekordbox can read either way

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M8_slots_lift_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_favorites_placement.py`
- Collected: 102 against a baseline of 102
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_order_takes_the_positions_the_live_children_hold_and_no_other`
  - `tests/test_favorites_placement.py::test_the_slots_are_the_rows_own_positions_with_a_shared_one_lifted[held3-given3]`
  - `tests/test_favorites_placement.py::test_the_slots_are_the_rows_own_positions_with_a_shared_one_lifted[held4-given4]`
  - `tests/test_favorites_placement.py::test_the_slots_are_the_rows_own_positions_with_a_shared_one_lifted[held5-given5]`

Old text:

```
        given.append(value if not given or value > given[-1] else given[-1] + 1)
```

New text:

```
        given.append(value)
```

### `u180.M9_seat_skips_unmoved`

seat: every row is written, its position unchanged or not

- File: `src/cratekit/favorites/placement.py`
- Source: `u180.json`, row `M9_seat_skips_unmoved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 7 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_folder_oldest_first_reads_newest_first_with_all_favorites_first_and_undated_last`
  - `tests/test_favorites_order.py::test_a_non_month_playlist_keeps_its_relative_place_after_the_months`
  - `tests/test_favorites_order.py::test_a_second_run_after_the_order_asks_nothing`
  - `tests/test_favorites_order.py::test_a_soft_deleted_month_is_neither_moved_nor_counted`
  - `tests/test_favorites_order.py::test_only_a_row_whose_position_changes_is_written`
  - `tests/test_favorites_order.py::test_the_order_takes_the_positions_the_live_children_hold_and_no_other`
  - `tests/test_favorites_order.py::test_the_verb_refuses_an_answer_the_read_back_does_not_hold`

Old text:

```
        if seq_of(row) == slot:
            continue
        row.Seq = slot
```

New text:

```
        row.Seq = slot
```

### `u308.M16_root_reads_any_parent`

placement._sits_under: a month under a folder is found at the playlist root

- File: `src/cratekit/favorites/placement.py`
- Source: `u308.json`, row `M16_root_reads_any_parent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_row_under_a_folder_is_not_at_the_root_and_a_root_row_is_under_no_folder`

Old text:

```
    return held in rb_writer.ROOT_PARENT_SENTINELS if at_root else held == parent_id
```

New text:

```
    return held in rb_writer.ROOT_PARENT_SENTINELS or held == parent_id
```

### `u119.V1_ack_after_plan`

favorites_refresh: the backup acknowledgment is not read before the gate

- File: `src/cratekit/favorites/spine.py`
- Source: `u119.json`, row `V1_ack_after_plan`
- Moved: The refresh verb runs through spine.run, which reads the backup acknowledgment before it builds the plan; the same line ahead of the plan, removed the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

    plan = planned()
```

New text:

```
    plan = planned()
```

### `u120-b.B4r_stale_not_refused`

apply: a plan whose digest moved is written anyway

- File: `src/cratekit/favorites/spine.py`
- Source: `u120-b.json`, row `B4r_stale_not_refused`
- Moved: The backfill's stale digest check moved into spine.fresh, which every favourites writer calls with its own wording; the same comparison of the replanned digest against the approved one, disabled the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_month_playlist_deleted_between_the_plan_and_the_write_is_another_plan`
  - `tests/test_favorites_backfill.py::test_the_write_itself_refuses_a_plan_whose_home_moved_with_no_gate_in_front`

Old text:

```
    if again.digest != approved.digest:
```

New text:

```
    if False:
```

### `u145.C2_unplanned_playlist_admitted`

addition_violations: a playlist row the plan did not make is admitted

- File: `src/cratekit/favorites/spine.py`
- Source: `u145.json`, row `C2_unplanned_playlist_admitted`
- Moved: The unplanned playlist row check of addition_violations is now spine.drift's, the made rows handed in; the same loop over rows added but not made, emptied the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[unplanned playlist-unplanned djmdPlaylist row 'x']`

Old text:

```
    for key in sorted(set(after.playlists) - set(before.playlists) - set(made)):
```

New text:

```
    for key in sorted(set()):
```

### `u145.C5_content_unchecked`

addition_violations: a changed content row is admitted

- File: `src/cratekit/favorites/spine.py`
- Source: `u145.json`, row `C5_content_unchecked`
- Moved: split's addition_violations now builds its content check through spine.drift, which order's confinement shares; the same comparison of the content table before and after
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_favorites_split.py`
- Collected: 68 against a baseline of 68
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[content-changed]`
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[content-djmdContent row changed]`

Old text:

```
    if before.content != after.content:
```

New text:

```
    if False:
```

### `u145.C6_existing_playlist_change_admitted`

addition_violations: an existing playlist row that changed beyond its bookkeeping is admitted

- File: `src/cratekit/favorites/spine.py`
- Source: `u145.json`, row `C6_existing_playlist_change_admitted`
- Moved: The check of an existing playlist row changing beyond what it may change is now spine.drift's, the allowed columns taken off first; the same test of what is left, disabled the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[quarter renamed-row 'q' changed ['Name']]`

Old text:

```
        moved -= BOOKKEEPING if moves(key) else frozenset()
        if moved:
```

New text:

```
        moved -= BOOKKEEPING if moves(key) else frozenset()
        if False:
```

### `u145.V1_gate_on_nothing`

favorites_split: a library with no quarter is still put to the gate

- File: `src/cratekit/favorites/spine.py`
- Source: `u145.json`, row `V1_gate_on_nothing`
- Moved: The split verb's nothing to write check before the gate is spine.run's first check, taken for every verb that does not ask the gate first; disabling it opens a gate over a library with no quarter.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_library_with_no_quarter_never_walks_the_library_or_asks_the_account`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`

Old text:

```
    if not (gate_first or plan.writes):
```

New text:

```
    if False:
```

### `u180-m25.M25_read_back_asserted`

favorites_order: a read back that disagrees with the plan is not refused, measured again once a test drove the verb's refusal

- File: `src/cratekit/favorites/spine.py`
- Source: `u180-m25.json`, row `M25_read_back_asserted`
- Moved: The verb's read back refusal moved into spine.run, which calls the engine's assert_read_back on the write's result; for the order verb that engine is favorites.order.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_verb_refuses_an_answer_the_read_back_does_not_hold`

Old text:

```
    engine.assert_read_back(result)
```

New text:

```
    pass
```

### `u180.M20_confined_content`

order_violations: a content row that changed is not a violation

- File: `src/cratekit/favorites/spine.py`
- Source: `u180.json`, row `M20_confined_content`
- Moved: The content check of order_violations and addition_violations is now spine.drift's, with the writer named in the message; the same comparison, disabled the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[content-changed]`

Old text:

```
    if before.content != after.content:
        violations.append(
            f"a {rb_writer.CONTENT_TABLE} row changed, and {touches} touches no track"
```

New text:

```
    if False:
        violations.append(
            f"a {rb_writer.CONTENT_TABLE} row changed, and {touches} touches no track"
```

### `u308.M10_commit_unrecorded`

spine.witnessed: a commit that landed cleanly is never recorded

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M10_commit_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_favorites_split.py`
- Collected: 64 against a baseline of 64
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_backfill.py::test_the_record_carries_the_placement_under_the_favourites_key`
  - `tests/test_favorites_split.py::test_the_record_carries_both_commits_under_the_favourites_key`

Old text:

```
            raise
    landed()
```

New text:

```
            raise
    pass
```

### `u308.M11_confinement_off`

spine.confined: a write that reached what its plan did not name commits

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M11_confinement_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_favorites_split.py`
- Collected: 68 against a baseline of 68
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_writer_refuses_an_order_that_reached_a_name`
  - `tests/test_favorites_split.py::test_the_writer_refuses_a_membership_the_plan_did_not_name`

Old text:

```
    violations = violations_of(rb_writer.node_tables(db))
    if violations:
```

New text:

```
    violations = violations_of(rb_writer.node_tables(db))
    if False:
```

### `u308.M13_made_rows_refused`

spine.drift: the playlists a plan makes read as unplanned rows

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M13_made_rows_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`, `tests/test_favorites_split.py`
- Collected: 68 against a baseline of 68
- Kills: 15 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_splits_months_land_in_order`
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_planned_addition_into_a_made_month_is_confined`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_quarter_whose_member_its_month_lacks_is_not_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`
  - `tests/test_favorites_split.py::test_no_content_row_tempo_or_grid_is_written`
  - `tests/test_favorites_split.py::test_the_record_carries_both_commits_under_the_favourites_key`

Old text:

```
    for key in sorted(set(after.playlists) - set(before.playlists) - set(made)):
```

New text:

```
    for key in sorted(set(after.playlists) - set(before.playlists)):
```

### `u308.M14_bookkeeping_always_admitted`

spine.drift: a row the plan does not move may change its position and stamps

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M14_bookkeeping_always_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[source-moved]`
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[unplanned-move]`

Old text:

```
        moved -= BOOKKEEPING if moves(key) else frozenset()
```

New text:

```
        moved -= BOOKKEEPING
```

### `u308.M15_unverified_answer_passed`

spine.verified: an answer the database does not hold is reported as written

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M15_unverified_answer_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_read_back_names_a_folder_that_does_not_read_in_the_planned_order`
  - `tests/test_favorites_order.py::test_the_verb_refuses_an_answer_the_read_back_does_not_hold`

Old text:

```
    if done.disagreements:
        raise refuse(
            "session-committed-unverified",
```

New text:

```
    if False:
        raise refuse(
            "session-committed-unverified",
```

### `u308.M1_gate_first_skipped`

spine.run: backfill and refresh no longer ask the gate first when nothing is to write

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M1_gate_first_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`
- Collected: 77 against a baseline of 77
- Kills: 7 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_unreadable_account_refuses_only_when_a_heart_needs_placing`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_backfill.py::test_with_nothing_landed_the_gate_is_still_asked_and_nothing_is_written`
  - `tests/test_genre_favorites.py::test_the_verb_over_a_mirror_already_true_asks_and_then_writes_nothing`

Old text:

```
    if not (gate_first or plan.writes):
```

New text:

```
    if not plan.writes:
```

### `u308.M2_declined_gate_drops_warnings`

spine.run: a declined gate drops the warnings the plan carried

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M2_declined_gate_drops_warnings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_declined_gate_keeps_the_warnings_the_plan_carried`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=engine.facts(plan)) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
```

New text:

```
    if ctx.gate.require(spec, plan=data, context=engine.facts(plan)) != "approve":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[])
```

### `u308.M3_backup_ack_skipped`

spine.run: the four favourites verbs plan and ask without the backup acknowledgment

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M3_backup_ack_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_favorites_order.py`, `tests/test_favorites_split.py`, `tests/test_genre_favorites.py`
- Collected: 145 against a baseline of 145
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`
  - `tests/test_favorites_order.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`
  - `tests/test_favorites_split.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`
  - `tests/test_genre_favorites.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)
```

New text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    pass
```

### `u308.M4_totals_not_merged`

spine.run: a write's totals are left out of the envelope

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M4_totals_not_merged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_favorites_order.py`, `tests/test_favorites_split.py`, `tests/test_genre_favorites.py`
- Collected: 145 against a baseline of 145
- Kills: 9 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_a_heart_the_landing_placed_without_a_month_takes_it_from_the_backfill`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_backfill.py::test_the_plan_lists_exactly_the_landed_hearts_and_the_approval_places_them`
  - `tests/test_favorites_backfill.py::test_with_no_pink_row_the_backfill_places_the_hearts_and_warns`
  - `tests/test_favorites_order.py::test_a_folder_oldest_first_reads_newest_first_with_all_favorites_first_and_undated_last`
  - `tests/test_favorites_order.py::test_only_a_row_whose_position_changes_is_written`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_genre_favorites.py::test_the_verb_asks_its_explicit_gate_then_adds_and_removes_and_reads_back`

Old text:

```
        data={**data, "totals": {**data["totals"], **totals}},
```

New text:

```
        data={**data, "totals": data["totals"]},
```

### `u308.M5_read_back_skipped`

spine.run: a write is reported without its read back

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M5_read_back_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_verb_refuses_an_answer_the_read_back_does_not_hold`

Old text:

```
    result = written(plan)
    engine.assert_read_back(result)
```

New text:

```
    result = written(plan)
```

### `u308.M6_write_handle_not_closed`

spine.handle: the write handle opens with rekordbox running

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M6_write_handle_not_closed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_write_handle_requires_rekordbox_closed_and_the_read_handle_does_not`

Old text:

```
        db = rb_writer.open_db(path, require_closed=True, cfg=cfg)
```

New text:

```
        db = rb_writer.open_db(path, require_closed=False, cfg=cfg)
```

### `u308.M7_empty_roots_admitted`

spine.watched: a writer watches no analysis root and reports itself clean

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M7_empty_roots_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_writer_given_no_analysis_root_refuses_to_watch_nothing`

Old text:

```
    roots = [Path(root) for root in analysis_roots]
    if not roots:
```

New text:

```
    roots = [Path(root) for root in analysis_roots]
    if False:
```

### `u308.M8_restore_not_detected`

spine.prepared: a write records a fingerprint over a database recovered out of band

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M8_restore_not_detected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_shared_writer_start_detects_an_out_of_band_restore`

Old text:

```
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))
    return roots, planned
```

New text:

```
    return roots, planned
```

### `u308.M9_landed_raise_unrecorded`

spine.witnessed: a commit that landed and then raised is never recorded

- File: `src/cratekit/favorites/spine.py`
- Source: `u308.json`, row `M9_landed_raise_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_commit_that_landed_and_then_raised_is_recorded_once`

Old text:

```
            if witness.landed:
                landed()
```

New text:

```
            if False:
                landed()
```

### `u145-s2.S2b_removed_member_read_live`

quarters: a membership rekordbox marked removed counts as a member

- File: `src/cratekit/favorites/split.py`
- Source: `u145-s2.json`, row `S2b_removed_member_read_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`

Old text:

```
            if not rb_writer.membership_removed(song)
        ]
        found.append(Quarter(
```

New text:

```
            if True
        ]
        found.append(Quarter(
```

### `u145.C1_unplanned_membership_admitted`

addition_violations: a membership added into a month for a row the plan did not name is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C1_unplanned_membership_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 3 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[unplanned row-puts row '2']`
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[wrong playlist-puts row '1' in playlist 'q']`
  - `tests/test_favorites_split.py::test_the_writer_refuses_a_membership_the_plan_did_not_name`

Old text:

```
        if row[m_marker] or content_id not in wanted.get(owner, set()):
```

New text:

```
        if row[m_marker]:
```

### `u145.C3_parent_unchecked`

addition_violations: a made month under another parent is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C3_parent_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[wrong parent-not a live plain playlist named '2026-10' under 'f']`

Old text:

```
            or str(row[parent_at]) != str(parent)
```

New text:

```
            or False
```

### `u145.C4_changed_membership_admitted`

addition_violations: an existing membership that changed is admitted

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `C4_changed_membership_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_an_addition_the_plan_did_not_name_is_a_violation[changed membership-row 's1' changed]`

Old text:

```
        if before.memberships[key] != after.memberships[key]:
```

New text:

```
        if False:
```

### `u145.S10_unemptied_retired`

apply: a quarter whose member its month lacks is retired all the same

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S10_unemptied_retired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_quarter_whose_member_its_month_lacks_is_not_retired`

Old text:

```
        unemptied = _unemptied(db, planned, rows)
        if unemptied:
```

New text:

```
        unemptied = _unemptied(db, planned, rows)
        if False:
```

### `u145.S11_unemptied_asks_taken_back`

_unemptied: a taken back member is asked of a month it has none in

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S11_unemptied_asks_taken_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`

Old text:

```
            if content_id in month_of
            and content_id not in held.get(month_of[content_id], frozenset())
```

New text:

```
            if content_id not in held.get(month_of[content_id], frozenset())
```

### `u145.S12_retirement_admits_memberships_only`

apply: the retirement's commit admits a removed membership and no removed playlist

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S12_retirement_admits_memberships_only`
- Moved: The retirement's commit sits inside spine.witnessed, one indent shallower; the same guarded commit admitting REMOVALS, narrowed the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 13 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`
  - `tests/test_favorites_split.py::test_no_content_row_tempo_or_grid_is_written`
  - `tests/test_favorites_split.py::test_the_record_carries_both_commits_under_the_favourites_key`

Old text:

```
            rb_writer.commit_guarded(db, removals=REMOVALS)
```

New text:

```
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
```

### `u145.S13_retirement_confined_to_nothing`

apply: the node confinement is told no quarter is removed

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S13_retirement_confined_to_nothing`
- Moved: The node confinement call sits inside spine.witnessed, one indent shallower, its arguments on one line; the same removed list of the quarters' rows, emptied the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 13 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`
  - `tests/test_favorites_split.py::test_no_content_row_tempo_or_grid_is_written`
  - `tests/test_favorites_split.py::test_the_record_carries_both_commits_under_the_favourites_key`

Old text:

```
                db, before, moved={}, removed=[one.playlist_id for one in planned.quarters]
```

New text:

```
                db, before, moved={}, removed=[]
```

### `u145.S1_any_name_is_a_quarter`

quarters: every playlist beside the source but Undated is a quarter, All Favorites and the months included

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S1_any_name_is_a_quarter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 8 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_library_with_no_quarter_never_walks_the_library_or_asks_the_account`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`
  - `tests/test_favorites_split.py::test_the_record_carries_both_commits_under_the_favourites_key`

Old text:

```
        if not placeholders.QUARTER_LABEL.fullmatch(name):
```

New text:

```
        if name == placeholders.UNDATED:
```

### `u145.S3_last_dated_mention_wins`

_job_rows: a heart's last dated mention wins over its first

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S3_last_dated_mention_wins`
- Moved: _job_rows now loops over backfill.reported's rows, so the loop is two levels shallower; the same first dated mention rule, loosened the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`

Old text:

```
        if row.hearted is not None and row.ref not in found:
```

New text:

```
        if row.hearted is not None:
```

### `u145.S4_account_never_asked`

date_members: a member no job dates is never looked for on the account

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S4_account_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`

Old text:

```
    rest = wanted - set(by_row)
    if rest:
```

New text:

```
    rest = wanted - set(by_row)
    if False:
```

### `u145.S5_job_dates_ignored`

_job_rows: no hearts job row is read, so every date comes from the account

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S5_job_dates_ignored`
- Moved: _job_rows now loops over backfill.reported's rows, so the loop is two levels shallower; the same test that a job row carries a date, inverted the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 11 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_every_sync_froze_again_is_resolved_once_with_its_first_dated_mention`
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`
  - `tests/test_favorites_split.py::test_a_member_no_job_dates_takes_the_accounts_date_and_one_dated_nowhere_goes_to_undated`
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`
  - `tests/test_favorites_split.py::test_a_member_two_quarters_hold_is_one_member_and_both_quarters_retire`
  - `tests/test_favorites_split.py::test_a_month_already_there_is_added_to_and_a_member_it_holds_is_not_added_twice`
  - `tests/test_favorites_split.py::test_a_quarter_of_seventeen_splits_into_fifteen_and_two_and_is_retired`
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`
  - `tests/test_favorites_split.py::test_a_track_taken_out_of_a_quarter_by_hand_goes_to_no_month`

Old text:

```
        if row.hearted is not None and row.ref not in found:
```

New text:

```
        if row.hearted is None and row.ref not in found:
```

### `u145.S6_rehearted_is_taken_back`

taken_back: a heart removed and added back live is still taken back

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S6_rehearted_is_taken_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_heart_taken_back_and_hearted_again_is_not_taken_back`

Old text:

```
    return frozenset(removed - placement.members(db, home.source_id))
```

New text:

```
    return frozenset(removed)
```

### `u145.S7_taken_back_placed`

_planned: a member the author took back is put in its month all the same

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S7_taken_back_placed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_member_taken_out_of_all_favorites_goes_to_no_month_and_its_quarter_still_retires`

Old text:

```
    members = tuple(one for one in every if one.content_id not in gone)
```

New text:

```
    members = tuple(one for one in every)
```

### `u145.S9_digest_covers_the_months_state`

identity: the digest covers what the months hold, so a run stopped after its additions plans another digest

- File: `src/cratekit/favorites/split.py`
- Source: `u145.json`, row `S9_digest_covers_the_months_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`

Old text:

```
            "taken_back": [one.content_id for one in self.taken_back],
        }
```

New text:

```
            "taken_back": [one.content_id for one in self.taken_back],
            "held": {name: sorted(ids) for name, ids in self.held.items()},
        }
```

### `u113-a.A2_queue_order`

The account playlists are taken newest job first, the order the store lists them

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A2_queue_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 23216 against a baseline of 23216
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
- Collected: 23216 against a baseline of 23216
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

### `u120.B2_first_mention_wins`

prefer_dated: a later mention that knows its date does not replace a first that does not

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u120.json`, row `B2_first_mention_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_two_jobs_carried_is_one_heart_with_the_dated_jobs_date`
  - `tests/test_intake_land_hearts_native.py::test_the_pass_jobs_hearts_are_read_from_the_job_and_a_playlist_job_claims_no_heart`

Old text:

```
    return held is None or (not held.known and row.known)
```

New text:

```
    return held is None
```

### `u128-b.A6b_abandoned_counts`

Rerun of A6 after its test: count every landing record as standing

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128-b.json`, row `A6b_abandoned_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
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
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
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
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
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
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 42 against a baseline of 42
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
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 42 against a baseline of 42
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
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 42 against a baseline of 42
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

### `u128.A3_rerun_keeps_owned`

On a rerun, keep the owned members and the left rows instead of the new files alone

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A3_rerun_keeps_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
            if rerun:
                continue
            if row.state != OWNED:
```

New text:

```
            if row.state != OWNED:
```

### `u128.A4_untied_carried_silent`

A carried row no planned file answers is silently absent rather than left

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A4_untied_carried_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 42 against a baseline of 42
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
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 42 against a baseline of 42
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

### `u145.M3_landing_heart_undated`

Hearted.month: a landed heart whose job dated it goes to Undated

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u145.json`, row `M3_landing_heart_undated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 13 against a baseline of 13
- Kills: 9 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - `tests/test_intake_land_hearts_native.py::test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it`
  - `tests/test_intake_land_hearts_native.py::test_a_source_at_the_root_takes_its_months_beside_it`
  - `tests/test_intake_land_hearts_native.py::test_once_a_band_holds_the_heart_the_additive_refresh_puts_it_in_that_folders_favorites`
  - `tests/test_intake_land_hearts_native.py::test_the_hearts_are_in_the_digest_so_another_set_is_another_plan`
  - `tests/test_intake_land_hearts_native.py::test_the_pass_jobs_hearts_are_read_from_the_job_and_a_playlist_job_claims_no_heart`
  - `tests/test_intake_land_hearts_native.py::test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made`

Old text:

```
        return placeholders.month_label(self.hearted) if self.known else None
```

New text:

```
        return placeholders.UNDATED if self.known else None
```

### `u145.M4_states_carried_only`

carried_hearts: states=None still reads only the carried states, so an owned row dates nothing

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u145.json`, row `M4_states_carried_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_favorites_split.py`
- Collected: 64 against a baseline of 64
- Kills: 8 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`

Old text:

```
        if states is not None and report.get("state") not in states:
```

New text:

```
        if report.get("state") not in (states or CARRIED_STATES):
```

### `u146-b.A1_superseded_ignored`

owned_hearts: an older pass places its owned hearts though a later hearts job ran, putting back a heart dropped since

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u146-b.json`, row `A1_superseded_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_landing_an_older_pass_places_no_owned_heart_once_a_later_hearts_job_ran`

Old text:

```
    if superseded:
        return ()
```

New text:

```
    if superseded and False:
        return ()
```

### `u146-b.A2_owned_reads_carried`

owned_hearts: reads the carried states, so the landing finds no owned heart

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u146-b.json`, row `A2_owned_reads_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_the_account_dates_nowhere_goes_to_undated`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`

Old text:

```
    return hearts(cfg, pass_name, states=frozenset({OWNED}))
```

New text:

```
    return hearts(cfg, pass_name)
```

### `u146-b.A3_report_paths_dropped`

carried_hearts: the report's files are not carried on the row, so no owned heart has a row to place

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u146-b.json`, row `A3_report_paths_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_the_account_dates_nowhere_goes_to_undated`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`

Old text:

```
                known=intake_cli.HEARTED in said,
                paths=tuple(str(path) for path in (report.get("paths") or ())),
```

New text:

```
                known=intake_cli.HEARTED in said,
                paths=(),
```

### `u166.C10_live_filter`

live_members: count a removed membership as held

- File: `src/cratekit/intake/analyzed.py`
- Source: `u166.json`, row `C10_live_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
    if False:
        return Member(content_id=content_id, title="", action=WAIT, why=NO_ROW)
```

### `u259.M5_member_reads_nothing`

analyzed.member: judge no row instead of the row read by ID, so the clear reads every member as missing

- File: `src/cratekit/intake/analyzed.py`
- Source: `u259.json`, row `M5_member_reads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
- Kills: 6 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_with_no_analysis_path_or_analysed_unset_stays`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`
  - `tests/test_inbox_analyzed.py::test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name`
  - `tests/test_inbox_analyzed.py::test_nothing_analysed_asks_a_late_analysis_is_stale_a_track_held_twice_clears_once_then_nothing`

Old text:

```
    return judge(content_id, db.get_content(ID=content_id))
```

New text:

```
    return judge(content_id, None)
```

### `u166.C12_ack_first`

inbox_analyzed: drop the backup acknowledgment before the plan

- File: `src/cratekit/intake/analyzed_cli.py`
- Source: `u166.json`, row `C12_ack_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)
```

New text:

```
    pass
```

### `u166.C13_read_back_call`

inbox_analyzed: skip the read back after the commit

- File: `src/cratekit/intake/analyzed_cli.py`
- Source: `u166.json`, row `C13_read_back_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`

Old text:

```
    analyzed.assert_read_back(plan, cleared)
```

New text:

```
    pass
```

### `u110-a.A2_favorites_word`

A hearts job says Tidal playlists instead of Favorites

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A2_favorites_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_job_the_pass_lost_does_not_name_the_batch`
  - `tests/test_intake_land_names.py::test_each_kind_of_pass_job_says_its_own_word`

Old text:

```
        return FAVORITES if source_id == intake_cli.FAVORITES_SOURCE_ID else PLAYLISTS
```

New text:

```
        return PLAYLISTS
```

### `u110-a.A5_several_labels`

A manifest naming several labels is named for its first label, not Labels

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A5_several_labels`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_label_rows_name_one_label_by_its_name_and_several_as_labels`

Old text:

```
else LABELS
```

New text:

```
else next(iter(named.values()))
```

### `u110-a.A6_folder_safe`

A label name's slash and colon reach the folder name unreplaced

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A6_folder_safe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_label_rows_name_one_label_by_its_name_and_several_as_labels`

Old text:

```
_UNSAFE.sub("-", text)
```

New text:

```
text
```

### `u110-a.A7_join_order`

Several pass words are joined alphabetically instead of in the fixed order

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A7_join_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_job_the_pass_lost_does_not_name_the_batch`
  - `tests/test_intake_land_names.py::test_several_words_are_joined_in_one_order_whatever_order_they_arrive_in`

Old text:

```
    ordered = [word for word in _ORDER if word in present]
```

New text:

```
    ordered = [word for word in sorted(present) if word in _ORDER]
```

### `u110-a.A8_labels_first`

Label rows lose their precedence over the pass's jobs

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A8_labels_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_label_go_landing_for_one_label_is_named_for_the_date_and_that_label`

Old text:

```
    said = label_words(label_rows)
    if said is not None:
        return said
    if pass_name:
```

New text:

```
    if pass_name:
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

### `u154.R5_unreadable_record_fails_open`

an unreadable session record is dropped and a shelved name reads free

- File: `src/cratekit/intake/batch_name.py`
- Source: `u154.json`, row `R5_unreadable_record_fails_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_apply_moves_the_folder_rewrites_the_paths_keeps_the_rest_and_the_name_stays_taken`

Old text:

```
    if unreadable:
        raise refuse(

```

New text:

```
    if False:
        raise refuse(

```

### `u164.B1_taken_recorded`

taken: read the music folder alone, as before U164

- File: `src/cratekit/intake/batch_name.py`
- Source: `u164.json`, row `B1_taken_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_shelve.py`
- Collected: 73 against a baseline of 73
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_second_unnamed_landing_that_day_takes_two_for_its_playlist_and_its_folder`
  - `tests/test_intake_land_native.py::test_two_unnamed_landings_on_one_day_are_two_playlists_and_never_one`
  - `tests/test_intake_shelve.py::test_apply_moves_the_folder_rewrites_the_paths_keeps_the_rest_and_the_name_stays_taken`

Old text:

```
    return os.path.lexists(landing.target_dir(cfg, name)) or name in recorded
```

New text:

```
    return os.path.lexists(landing.target_dir(cfg, name))
```

### `u164.B2_native_names`

recorded_names: read shelve records alone and skip native landings

- File: `src/cratekit/intake/batch_name.py`
- Source: `u164.json`, row `B2_native_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_second_unnamed_landing_that_day_takes_two_for_its_playlist_and_its_folder`
  - `tests/test_intake_land_native.py::test_two_unnamed_landings_on_one_day_are_two_playlists_and_never_one`

Old text:

```
        elif record.workflow == native.WORKFLOW:
            for key in (native.BATCH_PLAYLIST_KEY, native.FILED_BATCH_KEY):
```

New text:

```
        elif False:
            for key in (native.BATCH_PLAYLIST_KEY, native.FILED_BATCH_KEY):
```

### `u175.N1_date_first`

dated: put the date before the account's name, the order Phillip declined

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N1_date_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
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
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
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
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
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
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
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
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
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
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
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
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
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

### `r1709.M23_intake_exact_by_token`

intake's exact flag compares the token, so a search for a drop answered by a fire is listed and downloaded

- File: `src/cratekit/intake/candidates.py`
- Source: `r1709.json`, row `M23_intake_exact_by_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact[the-same-emoji]`
  - `tests/test_intake_missing_search.py::test_two_emoji_rows_are_each_searched_and_listed`

Old text:

```
    return frozenset((one.distinct, one.version_key) for one in wanted.readings)

```

New text:

```
    return frozenset((one.recording, one.version_key) for one in wanted.readings)

```

### `r879-a.C10_offset_counts_pages_not_rows`

search_pages: ask offset 1, 2 for the next pages instead of 50, 100

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C10_offset_counts_pages_not_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`
  - `tests/test_export_set.py::test_the_page_bound_reached_leaves_it_out_and_says_so`

Old text:

```
        pages.append(tuple(search(len(pages) * TRACK_SEARCH_PAGE)))
```

New text:

```
        pages.append(tuple(search(len(pages))))
```

### `r879-a.C11_sole_exact_ignores_full`

sole_exact (existing, sampled): drop the full page condition, so a bound reached answer lists its one exact candidate

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C11_sole_exact_ignores_full`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_intake_missing_search.py`
- Collected: 113 against a baseline of 113
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_the_page_bound_reached_leaves_it_out_and_says_so`
  - `tests/test_export_set.py::test_the_walk_never_asks_past_the_providers_ceiling_of_300`
  - `tests/test_intake_missing_search.py::test_a_full_page_is_never_the_whole_answer_so_its_one_exact_hit_is_offered`

Old text:

```
    if answer.ambiguous or answer.full:
```

New text:

```
    if answer.ambiguous:
```

### `r879-a.C1_full_reads_total_not_last_page`

Answer.full: read the total hits rather than the last page, so a walk that read a full page then a short one still reads as cut short

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C1_full_reads_total_not_last_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_an_exact_match_on_the_second_page_alone_is_listed`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`
  - `tests/test_export_set.py::test_the_same_exact_track_served_again_on_the_next_page_is_one`

Old text:

```
        last = self.hits if self.last_page is None else self.last_page
```

New text:

```
        last = self.hits
```

### `r879-a.C2_walk_ignores_short_page`

search_pages: drop the stop on a short page, so the walk asks every page to the bound

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C2_walk_ignores_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_a_held_file_whose_isrc_the_account_cannot_name_is_searched_and_said`
  - `tests/test_export_set.py::test_a_held_file_with_no_isrc_is_searched_and_says_so`
  - `tests/test_export_set.py::test_a_short_first_page_is_read_once`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`

Old text:

```
        if not answer.full or _settled_early(answer) or len(pages) >= bound:
```

New text:

```
        if _settled_early(answer) or len(pages) >= bound:
```

### `r879-a.C3_settled_early_without_ambiguity`

_settled_early: drop the ambiguous title, so a title read two ways reads on past a full page

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C3_settled_early_without_ambiguity`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_title_read_two_ways_on_a_full_page_says_so_and_not_the_bound`
  - `tests/test_export_set.py::test_a_title_that_reads_two_ways_reads_no_second_page`

Old text:

```
        answer.ambiguous
        or bool(answer.unreadable)
```

New text:

```
        bool(answer.unreadable)
```

### `r879-a.C4_settled_early_without_unreadable`

_settled_early: drop the unreadable row, so a page with one reads on

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C4_settled_early_without_unreadable`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_unreadable_row_on_a_full_page_reads_no_second_page`

Old text:

```
        or bool(answer.unreadable)

```

New text:

```
        or False

```

### `r879-a.C6_settled_early_without_several`

_settled_early: drop two distinct exact candidates, so a settled several reads a second page

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C6_settled_early_without_several`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_two_exact_matches_on_the_first_page_read_no_second`

Old text:

```
        or len(answer.exact_refs) > 1

```

New text:

```
        or len(answer.exact_refs) > 2

```

### `r879-a.C7_bound_off_by_one`

search_pages: let the bound allow one page more, so the walk asks offset 300, past the ceiling

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C7_bound_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_page_bound_reached_leaves_it_out_and_says_so`
  - `tests/test_export_set.py::test_the_walk_never_asks_past_the_providers_ceiling_of_300`

Old text:

```
        if not answer.full or _settled_early(answer) or len(pages) >= bound:
```

New text:

```
        if not answer.full or _settled_early(answer) or len(pages) > bound:
```

### `r879-a.C9_read_pages_forgets_last_page`

read_pages: carry no last page, so a two page answer is judged on its total

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C9_read_pages_forgets_last_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_an_exact_match_on_the_second_page_alone_is_listed`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`
  - `tests/test_export_set.py::test_the_same_exact_track_served_again_on_the_next_page_is_one`

Old text:

```
    return replace(answer, pages=len(pages), last_page=len(pages[-1]) if pages else 0)
```

New text:

```
    return replace(answer, pages=len(pages), last_page=None)
```

### `r879-b.C5r_settled_early_without_unnamed_exact`

rerun of C5 after its zero: _settled_early drops the exact candidate with no identifier

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-b.json`, row `C5r_settled_early_without_unnamed_exact`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_exact_match_with_no_identifier_on_a_full_page_reads_no_second_page`

Old text:

```
        or any(not one.track.ref for one in exact)

```

New text:

```
        or False

```

### `r879-b.C8r_ceiling_coefficient`

rerun of C8 after its zero: SEARCH_CEILING 300 to 350, so the derived bound is seven pages

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-b.json`, row `C8r_ceiling_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_walk_never_asks_past_the_providers_ceiling_of_300`

Old text:

```
SEARCH_CEILING = 300
```

New text:

```
SEARCH_CEILING = 350
```

### `u307.R14_search_pages_default_one_page`

candidates.search_pages: the default bound is one page, not as many as fit under the ceiling, so a full first page refuses the row

- File: `src/cratekit/intake/candidates.py`
- Source: `u307.json`, row `R14_search_pages_default_one_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 7 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_a_second_distinct_exact_match_on_the_next_page_leaves_it_out_as_several`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_an_exact_match_on_the_second_page_alone_is_listed`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`
  - `tests/test_export_set.py::test_the_page_bound_reached_leaves_it_out_and_says_so`
  - `tests/test_export_set.py::test_the_same_exact_track_served_again_on_the_next_page_is_one`

Old text:

```
    bound = SEARCH_CEILING // TRACK_SEARCH_PAGE if bound is None else bound
```

New text:

```
    bound = 1 if bound is None else bound
```

### `u307.R15_search_pages_constant_off_by_one`

candidates.__getattr__: SEARCH_PAGES answers one page more than the walk reads, so the constant and the default bound disagree

- File: `src/cratekit/intake/candidates.py`
- Source: `u307.json`, row `R15_search_pages_constant_off_by_one`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_page_bound_reached_leaves_it_out_and_says_so`

Old text:

```
        return SEARCH_CEILING // TRACK_SEARCH_PAGE
    raise AttributeError
```

New text:

```
        return SEARCH_CEILING // TRACK_SEARCH_PAGE + 1
    raise AttributeError
```

### `u307.R25_toggle_imported_at_top`

candidates: import the label catalogue's page size at the top of the module again, so intake reaches a toggleable package at import

- File: `src/cratekit/intake/candidates.py`
- Source: `u307.json`, row `R25_toggle_imported_at_top`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`

Old text:

```
from cratekit.acquire import match

```

New text:

```
from cratekit.acquire import match
from cratekit.label.catalogue import TRACK_SEARCH_PAGE as _TOP_PAGE  # noqa: F401

```

### `u79-a.A1_ambiguous_listed`

A title that reads two ways is listed on one candidate without a person

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A1_ambiguous_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_title_with_two_readings_is_never_listed_on_one_candidate[the-title-reading]`
  - `tests/test_intake_missing_search.py::test_a_title_with_two_readings_is_never_listed_on_one_candidate[the-version-reading]`

Old text:

```
    if answer.ambiguous or answer.full:
        return None
```

New text:

```
    if answer.full:
        return None
```

### `u79-a.A2_full_page_listed`

A full page is read as the whole answer, so its one exact hit is listed

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A2_full_page_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_full_page_is_never_the_whole_answer_so_its_one_exact_hit_is_offered`

Old text:

```
    if answer.ambiguous or answer.full:
        return None
```

New text:

```
    if answer.ambiguous:
        return None
```

### `u79-a.A3_unreadable_ignored`

A row of the answer that could not be read no longer stops a listing

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A3_unreadable_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_beside_a_row_that_cannot_be_read_is_offered`

Old text:

```
    if answer.unreadable or not exact:
```

New text:

```
    if not exact:
```

### `u79-a.A4_no_identifier_listed`

Exact candidates carrying no identifier are one distinct value and are listed

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A4_no_identifier_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_exact_hits_with_no_identifier_are_reported_as_that_and_not_as_no_resemblance`
  - `tests/test_intake_missing_search.py::test_the_only_exact_candidate_carrying_no_identifier_is_not_listed`

Old text:

```
    if any(not one.track.ref for one in exact):
        return None
```

New text:

```
    if False:
        return None
```

### `u79-a.A5_two_exact_picked`

Two exact candidates list the first, the pick the brief forbids

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A5_two_exact_picked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_under_the_floor_of_nothing_is_still_first`
  - `tests/test_intake_missing_search.py::test_more_candidates_than_the_screen_holds_are_truncated_and_counted`
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
    if len({one.track.ref for one in exact}) != 1:
```

New text:

```
    if len({one.track.ref for one in exact}) < 1:
```

### `u79-b.B1_floor_halved`

The floor's value is halved, so a weaker hit is shown

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B1_floor_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_no_candidate_for_any_row_refuses_rather_than_reading_as_nothing_to_do`

Old text:

```
CANDIDATE_FLOOR = 60.0
```

New text:

```
CANDIDATE_FLOOR = 30.0
```

### `u79-b.B2_score_before_exact`

A near miss scoring 100 leads an exact candidate

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B2_score_before_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_under_the_floor_of_nothing_is_still_first`

Old text:

```
            (not one.exact, -one.score, position, one)
```

New text:

```
            (False, -one.score, position, one)
```

### `u79-b.B3_no_identifier_offered`

A candidate with no identifier is offered as an option

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B3_no_identifier_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_beside_an_exact_one_with_no_identifier_is_offered`
  - `tests/test_intake_missing_search.py::test_exact_hits_with_no_identifier_are_reported_as_that_and_not_as_no_resemblance`

Old text:

```
            if one.track.ref and (one.exact or one.score >= CANDIDATE_FLOOR)
        ),
        key=
```

New text:

```
            if (one.exact or one.score >= CANDIDATE_FLOOR)
        ),
        key=
```

### `u79-b.B4_rejected_read_as_accepted`

A rejected row falls through to the accepted path and its one candidate is listed

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B4_rejected_read_as_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_rejected_row_is_reported_and_never_searched_again`

Old text:

```
    if held.verdict is review.Verdict.REJECTED:
```

New text:

```
    if False:
```

### `u79-b.B5_unspecific_yes_takes_first`

An acceptance naming none of several candidates lists the first

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B5_unspecific_yes_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
    if chosen is None and len(held.options) == 1:
```

New text:

```
    if chosen is None and len(held.options) >= 1:
```

### `u79-b.B6_option_track_mismatch`

An accepted option whose detail names another track is listed as that track

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B6_option_track_mismatch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_accepted_option_that_does_not_carry_its_own_track_lists_nothing`

Old text:

```
    if track is None or not track.ref or track.ref != option.option_id:
```

New text:

```
    if track is None or not track.ref:
```

### `u79-b.B8_open_item_searched_again`

A row already in front of a person is searched for again

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B8_open_item_searched_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_near_miss_is_offered_with_its_score_and_is_not_listed`

Old text:

```
    if held.verdict is None:
        return Proposal(
```

New text:

```
    if held.verdict is None:
        return None
    if held.verdict is None:
        return Proposal(
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

### `r431-b.B10_an_older_payload_reads_as_solo`

A payload frozen before the field existed thaws as billing one artist and asks for a companion

- File: `src/cratekit/intake/cli.py`
- Source: `r431-b.json`, row `B10_an_older_payload_reads_as_solo`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`

Old text:

```
        several_artists=bool(said.get("several_artists", True)),
```

New text:

```
        several_artists=bool(said.get("several_artists", False)),
```

### `r431-b.B9_the_freeze_drops_the_field`

The intake freeze stops carrying several_artists, so the worker resolves from a track that never looked

- File: `src/cratekit/intake/cli.py`
- Source: `r431-b.json`, row `B9_the_freeze_drops_the_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`

Old text:

```
        "several_artists": row.several_artists,
```

New text:

```
(empty)
```

### `r504-b.B1_verb_drops_short`

intake playlist favorites lists the hearts and throws the shortfall away

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B1_verb_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
            tracks, short = list_favorites(found)
```

New text:

```
            tracks, short = list_favorites(found)[0], None
```

### `r504-b.B4_no_progress_block`

The verb carries no shortfall block under progress

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B4_no_progress_block`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
        extra = {"shortfall": short.block()} if short is not None else {}
```

New text:

```
        extra = {}
```

### `r504-b.B5_noop_silent`

Every heart withheld is the quiet no-op again, with no warning

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B5_noop_silent`
- Moved: Anchored where u325-replay-after.json replayed it: Same no-tracks return in intake_playlist; U298 replaced the local _no_op with cli.output.no_job
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
                data=no_job("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
                warnings=warnings,
            )
```

New text:

```
                data=no_job("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
            )
```

### `r504-b.B6_warning_reworded`

The warning names no numbers

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B6_warning_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
            f"the account's hearts listed short: {short.summary()}. The provider "
```

New text:

```
            f"the account's hearts listed short. The provider "
```

### `r515-operator.S10_intake_all_withheld_quiet`

An intake playlist with every track withheld is a quiet no op

- File: `src/cratekit/intake/cli.py`
- Source: `r515-operator.json`, row `S10_intake_all_withheld_quiet`
- Moved: Anchored where u325-replay-after.json replayed it: Same no-tracks return in intake_playlist; U298 replaced the local _no_op with cli.output.no_job
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
        if not tracks:
            return ctx.envelope(
                data=no_job("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
                warnings=warnings,
```

New text:

```
        if not tracks:
            return ctx.envelope(
                data=no_job("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
```

### `r515-operator.S11_intake_playlist_no_warning`

An intake playlist listed short carries no warning

- File: `src/cratekit/intake/cli.py`
- Source: `r515-operator.json`, row `S11_intake_playlist_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
        warnings = (warned(short),) if short is not None else ()
```

New text:

```
        warnings = ()
```

### `u103-b.C8_set_no_op_carries_warnings`

Drop the warnings from intake set's nothing identified envelope

- File: `src/cratekit/intake/cli.py`
- Source: `u103-b.json`, row `C8_set_no_op_carries_warnings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
                outcome=Outcome.NO_OP,
                warnings=warnings,
            )
```

New text:

```
                outcome=Outcome.NO_OP,
            )
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

### `u165.F1_reset_cache`

file_landed: plan over the cached collection without forgetting it (round one's test)

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F1_reset_cache`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_collection_read_before_the_commit_does_not_hide_the_landed_rows`

Old text:

```
    collection.reset_cache()

```

New text:

```
    pass

```

### `u165.F2_compare`

file_landed: never compare the plan after the commit with the prediction

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F2_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_plan_after_the_commit_that_differs_files_nothing_and_says_so`

Old text:

```
        if now != one.place:
```

New text:

```
        if False:
```

### `u165.F3_differing_files`

file_landed: file even when a row differs from its prediction

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F3_differing_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_plan_after_the_commit_that_differs_files_nothing_and_says_so`

Old text:

```
    if differing:
        return Filed(state=FILED_DIFFERENTLY
```

New text:

```
    if False:
        return Filed(state=FILED_DIFFERENTLY
```

### `u165.F4_vox_predicted`

predict: never predict the vocal sub

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F4_vox_predicted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`

Old text:

```
vox=row.vox),
```

New text:

```
vox=False),
```

### `u165.F6_unplaced`

_refuse_unplaced: never refuse a landed row the tree writer could not place

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F6_unplaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_landed_row_the_tree_could_not_place_refuses_before_the_ledger_is_marked`

Old text:

```
    if not membership.skipped:
        return
    unplaced = sorted({str(match.requested) for match in membership.skipped})
    raise refuse(
        "adopt-entries-failed",
        f"{len(unplaced)} landed row(s)
```

New text:

```
    if True:
        return
    unplaced = sorted({str(match.requested) for match in membership.skipped})
    raise refuse(
        "adopt-entries-failed",
        f"{len(unplaced)} landed row(s)
```

### `r501-c.M1_export_name_check`

imported_cli.read_export: drop the refusal of an export carrying an intake file's name, leaving only the identity check

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M1_export_name_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`

Old text:

```
    if any(export.name.endswith(suffix) for suffix in tree_registry.PENDING_XML_SUFFIXES):
        raise _refuse_export(
```

New text:

```
    if False:
        raise _refuse_export(
```

### `r501-c.M2_export_identity_check`

imported_cli.read_export: drop the refusal of the file a waiting run names, so a link to the intake file proves its own import

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M2_export_identity_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`

Old text:

```
        if artifact and _same_file(export, Path(artifact)):
```

New text:

```
        if False:
```

### `r501-c.M3_missing_is_not_imported`

imported_cli.settle: ignore missing tracks, so an export taken before the import proves it

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M3_missing_is_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`

Old text:

```
    if missing:
        return {
```

New text:

```
    if False:
        return {
```

### `r501-c.M4_nothing_recorded`

imported_cli.settle: drop the unverifiable answer, so a run the ledger names no file for is proven by any export

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M4_nothing_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`

Old text:

```
    if not landed:
        # NOTHING RECORDED IS NOT NOTHING OWED.
```

New text:

```
    if False:
        # NOTHING RECORDED IS NOT NOTHING OWED.
```

### `r501-c.M5_retire_name_guard`

imported_cli.retire: rename any file a record names, whatever it is called

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M5_retire_name_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_retiring_renames_only_a_plain_file_this_product_named`

Old text:

```
    if not any(artifact.name.endswith(suffix) for suffix in tree_registry.PENDING_XML_SUFFIXES):
        raise refuse(
            "internal-error",
```

New text:

```
    if False:
        raise refuse(
            "internal-error",
```

### `r501-c.M6_retire_link_guard`

imported_cli.retire: follow a link instead of refusing it

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M6_retire_link_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_retiring_renames_only_a_plain_file_this_product_named`

Old text:

```
    if artifact.is_symlink() or not artifact.is_file():
        return None
    if not any(
```

New text:

```
    if not artifact.is_file():
        return None
    if not any(
```

### `r501-d.M10_waiting_legacy`

imported_cli._waiting: look only for awaiting-import, so every landing made before the fix is left where it was

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M10_waiting_legacy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`

Old text:

```
    if record.state is session.SessionState.AWAITING_IMPORT:
        return True
    return (
```

New text:

```
    if record.state is session.SessionState.AWAITING_IMPORT:
        return True
    return False and (
```

### `r501-d.M11_close_refusal_reported`

imported_cli._close_if_nothing_is_owed: raise the gated close's refusal, ending the verb after the file is retired and the proof recorded

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M11_close_refusal_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`

Old text:

```
    except CratekitError as exc:
        return {"closed": False, "close_refused": exc.cause.reason, "why": exc.cause.message}
```

New text:

```
    except CratekitError:
        raise
```

### `r501-d.M13_waiting_needs_export`

imported_cli.intake_imported: drop the refusal when a run is waiting and no export is named, so the verb answers no-op over a waiting run

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M13_waiting_needs_export`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`

Old text:

```
    if waiting and export is None:
        raise _no_export(waiting)
```

New text:

```
    if waiting and export is None:
        waiting = []
```

### `r501-d.M7_retire_next_free_name`

imported_cli.retire: never take the next free name, so a second retirement lands on the first

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M7_retire_next_free_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_retiring_never_lands_on_another_file`

Old text:

```
        while not naming.claim_target(target):
```

New text:

```
        while False:
```

### `r501-d.M9_waiting_capture`

imported_cli._waiting: drop the no capture condition, so an open destructive session is taken for a landing

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M9_waiting_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`

Old text:

```
        record.state is session.SessionState.OPEN
        and record.snapshot_path is None
        and record.pending is None
```

New text:

```
        record.state is session.SessionState.OPEN
        and record.pending is None
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

### `u307.R11_imported_session_ignored`

imported_cli._considered: ignore --session, so every intake run is considered and an unknown run is not refused

- File: `src/cratekit/intake/imported_cli.py`
- Source: `u307.json`, row `R11_imported_session_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`

Old text:

```
        if record.workflow != ingest.INTAKE_WORKFLOW or wanted not in (None, record.session_id):
```

New text:

```
        if record.workflow != ingest.INTAKE_WORKFLOW:
```

### `r501-b.I1_rollback_abandon`

ingest.place_files: drop the abandon in the rollback, so a refused call leaves its session non terminal

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I1_rollback_abandon`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
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
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
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
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`
- Collected: 61 against a baseline of 61
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

### `r770-a.A1_switch_reads_the_other_mode`

IntakeMedium.native: answer native for a tree on the bridge and bridge for a native one

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A1_switch_reads_the_other_mode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
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
- Ran: `tests/test_intake_land.py`, `tests/test_intake_writers_native.py`
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
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
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
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
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
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
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
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
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

### `u156.L10_staging_dropped`

supported_only: keep the targets a landing leaves in staging, so a year playlist plans members no row answers

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L10_staging_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_left_in_staging_is_filed_nowhere_and_not_said_to_be_in_the_intake_playlist[2021]`

Old text:

```
        held = tuple(target for target in one.targets if target in kept)
```

New text:

```
        held = one.targets
```

### `u156.L11_unlanded_named`

write: drop the member whose file did not land without naming it

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L11_unlanded_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2020]`
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2021]`

Old text:

```
            if held:
                ids.append(held)
            else:
                left.append(
```

New text:

```
            if held:
                ids.append(held)
            elif False:
                left.append(
```

### `u156.L12_empty_year`

write: make a year playlist even when no member of it landed

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L12_empty_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2020]`

Old text:

```
        if ids:
            wanted.append((one, tuple(dict.fromkeys(ids))))
```

New text:

```
        wanted.append((one, tuple(dict.fromkeys(ids))))
```

### `u156.L13_tree_reused`

write: make a new tree folder even when the plan found one, so Record Labels doubles

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L13_tree_reused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2020]`
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2021]`
  - `tests/test_intake_land_labels_native.py::test_an_existing_year_playlist_gains_members_and_loses_none`
  - `tests/test_intake_land_labels_native.py::test_the_same_files_landed_again_add_no_second_membership`

Old text:

```
    if plan.tree_folder:
        tree = _live_row(
```

New text:

```
    if False:
        tree = _live_row(
```

### `u156.L14_folder_reused`

write: make a new label folder even when the plan found one

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L14_folder_reused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2020]`
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2021]`
  - `tests/test_intake_land_labels_native.py::test_a_label_folder_spelled_decomposed_is_the_same_folder`
  - `tests/test_intake_land_labels_native.py::test_a_removed_year_playlist_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_intake_land_labels_native.py::test_an_existing_year_playlist_gains_members_and_loses_none`
  - `tests/test_intake_land_labels_native.py::test_the_same_files_landed_again_add_no_second_membership`

Old text:

```
            if planned:
                folder = _live_row(
```

New text:

```
            if False:
                folder = _live_row(
```

### `u156.L15_year_reused`

write: make a new year playlist even when the plan found one, so the year doubles

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L15_year_reused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2020]`
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2021]`
  - `tests/test_intake_land_labels_native.py::test_an_existing_year_playlist_gains_members_and_loses_none`
  - `tests/test_intake_land_labels_native.py::test_the_same_files_landed_again_add_no_second_membership`
  - `tests/test_intake_land_labels_native.py::test_the_write_refuses_a_planned_node_removed_since_the_plan`

Old text:

```
        if one.playlist_id:
            playlist = _live_row(
```

New text:

```
        if False:
            playlist = _live_row(
```

### `u156.L16_live_at_write`

_live_row: take a planned node removed since the plan, so the write files into a playlist nobody sees

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L16_live_at_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_the_write_refuses_a_planned_node_removed_since_the_plan`

Old text:

```
    if row is None or rb_writer.node_removed(row) or not _of_kind(row, folder=folder):
```

New text:

```
    if row is None:
```

### `u156.L17_digest_years`

identity: leave the year playlists out of the digest, so an answer survives a playlist made since

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L17_digest_years`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_year_playlist_made_after_the_answer_makes_the_answer_stale`

Old text:

```
        "years": [one.identity() for one in plan.years],
```

New text:

```
        "years": [],
```

### `u156.L1_year_bound`

_read_year: take any four digits as a release year, so a 0000 placeholder files under year 0

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L1_year_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_the_year_is_the_date_tags_leading_four_digits_and_no_year_is_named_with_why[0000-None-names 0, which is no release year]`
  - `tests/test_intake_land_labels_native.py::test_the_year_is_the_date_tags_leading_four_digits_and_no_year_is_named_with_why[1899-01-01-None-names 1899]`
  - `tests/test_intake_land_labels_native.py::test_the_year_is_the_date_tags_leading_four_digits_and_no_year_is_named_with_why[2999-None-names 2999]`

Old text:

```
    if not FIRST_YEAR <= year <= _today().year + 1:
```

New text:

```
    if False:
```

### `u156.L21_read_back`

assert_read_back: accept a year playlist that does not hold what the plan named

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L21_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_an_answer_the_database_does_not_hold_is_refused`

Old text:

```
        missing = [content for content in one.ids if content not in live]
        if missing:
```

New text:

```
        missing = [content for content in one.ids if content not in live]
        if False:
```

### `u156.L2_bridge_guard`

_catalog_node: drop the refusal of a library whose intake tree is on the bridge, so the tree is appended beside an intake file

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L2_bridge_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_the_plan_refuses_a_library_whose_intake_tree_is_on_the_bridge`

Old text:

```
    if declared is None or not medium.native:
```

New text:

```
    if declared is None:
```

### `u156.L3_wrong_kind`

_sole: drop the refusal of a node of the other kind, so a playlist named for the label stands where its folder belongs

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L3_wrong_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_tree_the_label_write_cannot_take_is_refused_before_the_gate`

Old text:

```
        if not _of_kind(row, folder=folder):
```

New text:

```
        if False:
```

### `u156.L4_two_of_a_name`

_sole: admit two siblings of one name, so the first the query yields is written into

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L4_two_of_a_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_tree_the_label_write_cannot_take_is_refused_before_the_gate`

Old text:

```
    if len(named) > 1:
```

New text:

```
    if len(named) > 2:
```

### `u156.L5_nfc_fold`

_folded: compare names as stored, so a decomposed label folder is not found and a second is made

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L5_nfc_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_label_folder_spelled_decomposed_is_the_same_folder`
  - `tests/test_intake_land_labels_native.py::test_a_labelled_file_with_no_year_is_named_and_a_decomposed_label_is_the_composed_folder`
  - `tests/test_intake_land_labels_native.py::test_one_label_spelled_two_ways_is_one_folder_and_a_file_two_rows_file_names_both_years`

Old text:

```
    return unicodedata.normalize("NFC", name)
```

New text:

```
    return name
```

### `u156.L6_removed_nodes`

_live_children: keep removed nodes, so a playlist a person deleted in rekordbox is written into

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L6_removed_nodes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_removed_year_playlist_is_not_added_to_and_a_live_one_is_made`

Old text:

```
    return [row for row in under if not rb_writer.node_removed(row)]
```

New text:

```
    return under
```

### `u156.L7_year_boundary`

_YEAR: drop the digit boundary, so 20210305 reads as 2021

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L7_year_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_the_year_is_the_date_tags_leading_four_digits_and_no_year_is_named_with_why[20210305-None-None]`

Old text:

```
_YEAR = re.compile(r"^\s*(\d{4})(?!\d)")
```

New text:

```
_YEAR = re.compile(r"^\s*(\d{4})")
```

### `u156.L8_year_anchor`

year_of: search the tag rather than read its head, so a year anywhere in the text is taken

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L8_year_anchor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_with_no_date_tag_is_named_on_the_screen_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_the_year_is_the_date_tags_leading_four_digits_and_no_year_is_named_with_why[March 2021-None-None]`

Old text:

```
    found = _YEAR.match(stored)
```

New text:

```
    found = re.search(r"(\d{4})(?!\d)", stored)
```

### `u156.L9_no_year_named`

plan_for_label: file a file with no year under a year of none instead of naming it

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L9_no_year_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_left_in_staging_is_filed_nowhere_and_not_said_to_be_in_the_intake_playlist[None]`
  - `tests/test_intake_land_labels_native.py::test_a_file_with_no_date_tag_is_named_on_the_screen_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_screen_with_nothing_to_file_says_so`
  - `tests/test_intake_land_labels_native.py::test_an_undated_file_the_move_refused_is_said_not_to_have_landed`

Old text:

```
        year, why = _read_year(source)
        if year is None:
```

New text:

```
        year, why = _read_year(source)
        if False:
```

