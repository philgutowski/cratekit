# Mutation table: u331-before-b-01

Measured by `scripts/mutate.py` on 2026-11-23 23:05 UTC, branch `HEAD` at `c0bb16a4`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22808 collected. pytest invocations for this batch: 203.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 23:05 UTC for commit `c0bb16a4eaf3`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 40, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22808 against 22808. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1255.T1_tree_registry_clause` | `src/cratekit/core/tree_registry.py` | user | 3 file(s) | 119 | 2 | killed |
| `r235-a.M11_session_lock_dropped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M12_second_record_replaces` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M13_snapshot_check_dropped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 11 | killed |
| `r235-a.M1_unreadable_log_skipped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M2_margin_zero` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M3_margin_two_days` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M4_unparseable_start_predates` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M5_updates_not_counted` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M6_any_tree_counts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M7_zero_count_counts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M8_open_run_reverts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M9_library_guard_removed` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 4 | killed |
| `r235-b.M14_empty_export_accepted` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r501-a.T1_precheck_excusal` | `src/cratekit/core/tree_registry.py` | user | 5 file(s) | 134 | 4 | killed |
| `r787.S1_set_drops_intake` | `src/cratekit/core/tree_registry.py` | user | 20 file(s) | 2616 | 7 | killed |
| `u953.M2_registry_cause_remedy_fixed` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 115 | 2 | killed |
| `r1037.M10_landed_not_joined` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 14 | killed |
| `r1037.M11_sightings_never_forgotten` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 1 | killed |
| `r1037.M12_playlists_always_held` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 8 | killed |
| `r1037.M9_recorded_not_excluded` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1844.N14_uuids_not_passed` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 4 | killed |
| `r1844.N15_baseline_count_lost` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 1 | killed |
| `r1844.N16_review_count_lost` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 5 | killed |
| `r431-a.A15_the_verb_lifts_through_the_store` | `src/cratekit/deletion/run.py` | user | 2 file(s) | 366 | 6 | killed |
| `r44-b.R1_rules_drop_identity` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `r44-b.R2_no_gate_at_the_plan` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 4 | killed |
| `r44-b.R3_no_look_at_the_loop_top` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 2 | killed |
| `r44-b.R4_no_look_after_the_recheck` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `r44-b.R5_both_looks_gone` | `src/cratekit/deletion/run.py` | maintainer | 1 file(s) | 331 | 4 | killed |
| `r44-b.X1_library_root_gate` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 1 | killed |
| `r44-b.X2_suspect_anchor` | `src/cratekit/deletion/run.py` | user | 1 file(s) | 331 | 2 | killed |
| `u310.A10_unrecorded_move_put_back` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 5 | killed |
| `u310.A11_unproved_anchor_retires_nothing` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 1 | killed |
| `u310.A12_only_answered_items_move` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 1 | killed |
| `u310.A13_fresh_playlist_read` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 2 | killed |
| `u310.A14_reference_set_complete` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 2 | killed |
| `u310.A1_gates_asserted` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 1 | killed |
| `u310.A2_volume_before_the_answer` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 2 | killed |
| `u310.A3_reject_moves_nothing` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 4 | killed |
| `u310.A4_planned_deletable` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 1 | killed |
| `u310.A5_fresh_decline_snapshot` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 1 | killed |
| `u310.A7_recheck_still_deletable` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 1 | killed |
| `u310.A8_shown_path_is_the_moved_path` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 2 | killed |
| `u310.A9_volume_refusal_stops_the_run` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 388 | 1 | killed |
| `u120.P1_live_plain_attribute` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 4 | killed |
| `u120.P2_two_sources_accepted` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 2 | killed |
| `u120.P4_into_source_always` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 3 | killed |
| `u120.P7_bypass_only_when_absent` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 3 | killed |
| `u120.P8_source_name_default` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 1 | killed |
| `u145.M2_placement_undated` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 98 | 21 | killed |
| `u146-b.B15_any_playlist_files` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 31 | 1 | killed |
| `u153.P1_into_colour_flag` | `src/cratekit/favorites/placement.py` | user | 3 file(s) | 111 | 11 | killed |
| `u153.P3_writes_colours` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 98 | 4 | killed |
| `u153.P4_identity_pink` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 98 | 1 | killed |
| `u153.P5_recolour_dedup` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 98 | 3 | killed |
| `u153.P6_place_pink_guard` | `src/cratekit/favorites/placement.py` | user | 3 file(s) | 111 | 2 | killed |
| `u180.M11_new_month_seated` | `src/cratekit/favorites/placement.py` | user | 5 file(s) | 179 | 6 | killed |
| `u180.M12_new_month_knows_the_source` | `src/cratekit/favorites/placement.py` | user | 5 file(s) | 179 | 5 | killed |
| `u180.M13_never_above_all_favorites` | `src/cratekit/favorites/placement.py` | user | 5 file(s) | 179 | 1 | killed |
| `u180.M7_children_live_only` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 102 | 3 | killed |
| `u180.M8_slots_lift_shared` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 102 | 4 | killed |
| `u180.M9_seat_skips_unmoved` | `src/cratekit/favorites/placement.py` | user | 2 file(s) | 102 | 7 | killed |
| `u185.R3_favorites_home` | `src/cratekit/favorites/placement.py` | user | 1 file(s) | 67 | 1 | killed |
| `u308.M16_root_reads_any_parent` | `src/cratekit/favorites/placement.py` | user | 3 file(s) | 131 | 1 | killed |
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
| `r770-c.C3_failure_past_the_gate_loses_its_reason` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-c.C4_failure_past_the_gate_loses_its_remedy` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 33 | 1 | killed |
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
| `u307.R6_refuse_past_drops_inner_message` | `src/cratekit/intake/landing.py` | user | 4 file(s) | 109 | 4 | killed |
| `u71-b.B10_occupied_at_move` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 2 | killed |
| `u71-b.B11_nothing_moved` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71-b.B12_take_back_folder` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 39 | 1 | killed |
| `u71-b.B13_unlink_destination` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 22808 | 0 (promoted) | zero |
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
| `u198.D10_twins` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D11_two_homes` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D2_favorites_home` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 3 | killed |
| `u198.D3_held` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D4_skip` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 3 | killed |
| `u198.D5_smart` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D6_released` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D7_twice` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D8_top_names` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D9_foreign` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 2 | killed |
| `u202.D1_skip` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D2_two_tops` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D3_longest` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D5_name_taken` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D6_favourites` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u216.M11_paired_raw` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 6 | killed |
| `u216.M12_empty_rest` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 1 | killed |
| `u216.M1_held_record_ignored` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 7 | killed |
| `u216.M2_created_folder_by_time` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 2 | killed |
| `u216.M3_no_moment_reads_new` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 1 | killed |
| `u216.M4_no_time_reads_new` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 3 | killed |
| `u216.M5_naive_time_trusted` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 2 | killed |
| `u216.M6_equal_moment_new` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 1 | killed |
| `u216.M7_time_rule_off` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 3 | killed |
| `u216.M8_moment_latest` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 1 | killed |
| `u216.M9_moment_naive_kept` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 1 | killed |
| `u242.M25_copy_needs_the_prefix` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 76 | 1 | killed |
| `u242.M27_copy_pool_reads_no_taken` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 76 | 1 | killed |
| `u304-b.S15_favourites_home_judged_without_the_foreign_check` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 114 | 1 | killed |
| `u304-b.S7_walk_keeps_removed_nodes` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 114 | 1 | killed |
| `u304.S8_walk_root_sentinel` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 114 | 87 | killed |

## Zero rows and what they owe

- `u71-b.B13_unlink_destination` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

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

### `r235-a.M11_session_lock_dropped`

a revert holds the registry lock and not the session lock

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M11_session_lock_dropped`
- Moved: Same with statement in revert_cutover; U298 renamed config._exclusive_lock to exclusive_lock
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
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
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
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
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
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
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
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
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
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
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
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
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
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
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
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
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
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
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
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
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
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
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
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
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
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
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_import_coexistence.py`, `tests/test_xml_splice_golden.py`
- Collected: 2616 against a baseline of 2616
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

### `r1037.M10_landed_not_joined`

plan: leave the absent landed rows out of the removals, which is the defect R-1037 names

- File: `src/cratekit/deletion/run.py`
- Source: `r1037.json`, row `M10_landed_not_joined`
- Moved: the replace call collapsed onto one argument line; the landed absences are not joined, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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

### `r1844.N14_uuids_not_passed`

run.plan: the held rows' UUIDs are not handed to the landed row reader

- File: `src/cratekit/deletion/run.py`
- Source: `r1844.json`, row `N14_uuids_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`
- Collected: 388 against a baseline of 388
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
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`
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
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 111 against a baseline of 111
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
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`
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
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`
- Collected: 98 against a baseline of 98
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
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`
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
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 111 against a baseline of 111
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
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`, `tests/test_favorites_split.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_favorites_backfill.py`
- Collected: 179 against a baseline of 179
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
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`, `tests/test_favorites_split.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_favorites_backfill.py`
- Collected: 179 against a baseline of 179
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
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`, `tests/test_favorites_split.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_favorites_backfill.py`
- Collected: 179 against a baseline of 179
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
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
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
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
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
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_order.py`
- Collected: 102 against a baseline of 102
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

### `u185.R3_favorites_home`

resolve_home: count a playlist of the source's name inside the folder

- File: `src/cratekit/favorites/placement.py`
- Source: `u185.json`, row `R3_favorites_home`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_playlist_of_the_sources_name_inside_deadca7s_folder_is_not_a_second_source`

Old text:

```
    live = foreign_tree.outside(
        _live_plain(list(db.get_playlist(Name=name))), list(db.get_playlist())
    )
```

New text:

```
    live = _live_plain(list(db.get_playlist(Name=name)))
```

### `u308.M16_root_reads_any_parent`

placement._sits_under: a month under a folder is found at the playlist root

- File: `src/cratekit/favorites/placement.py`
- Source: `u308.json`, row `M16_root_reads_any_parent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`, `tests/test_favorites_split.py`
- Collected: 131 against a baseline of 131
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

### `u307.R6_refuse_past_drops_inner_message`

landing.refuse_past: leave the inner failure's own sentence out of the message, so a person reads what was left but not what failed

- File: `src/cratekit/intake/landing.py`
- Source: `u307.json`, row `R6_refuse_past_drops_inner_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_land_dyn_native.py`, `tests/test_intake_writers_native.py`
- Collected: 109 against a baseline of 109
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
- Collected: 22808 against a baseline of 22808
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

### `u198.D10_twins`

pair_discover: a twins folder is walked

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D10_twins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_cratekits_own_trees_and_the_favorites_folder_are_never_discovered`

Old text:

```
        if _attribute(top) == FOLDER and TWIN_FOLDER.fullmatch(top_name):
```

New text:

```
        if False:
```

### `u198.D11_two_homes`

pair_discover: two favourites playlists read as one home, hidden

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D11_two_homes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_two_favourites_playlists_leave_both_folders_out_and_say_so`

Old text:

```
        if len(named) > 1
```

New text:

```
        if len(named) > 2
```

### `u198.D2_favorites_home`

pair_discover: the one favourites home is walked like any folder

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D2_favorites_home`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_favourites_name_inside_another_apps_folder_does_not_unsettle_the_home`
  - `tests/test_sync_pair_discover.py::test_a_favourites_playlist_at_the_root_is_not_discovered`
  - `tests/test_sync_pair_discover.py::test_cratekits_own_trees_and_the_favorites_folder_are_never_discovered`

Old text:

```
            if not unsure:
                return
```

New text:

```
            if False:
                return
```

### `u198.D3_held`

pair_discover: a playlist a pair holds is found again

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D3_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_paired_playlist_is_not_listed_on_a_later_run`

Old text:

```
        if node_id in held:
            return
```

New text:

```
        if False:
            return
```

### `u198.D4_skip`

pair_discover: a playlist under a skipped folder is found

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D4_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_an_archive_playlist_is_listed_and_never_written`
  - `tests/test_sync_pair_discover.py::test_the_skip_list_is_the_configurations`
  - `tests/test_sync_pair_discover.py::test_two_favourites_playlists_leave_both_folders_out_and_say_so`

Old text:

```
        if skip_why:
```

New text:

```
        if False:
```

### `u198.D5_smart`

pair_discover: a smart playlist is found as a plain one

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D5_smart`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_smart_playlist_is_listed_not_paired`

Old text:

```
        if attribute != PLAIN:
```

New text:

```
        if False:
```

### `u198.D6_released`

pair_discover: a released playlist is found again

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D6_released`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_on_the_account_unpairs_stays_and_is_not_made_again`

Old text:

```
        if node_id in gone:
```

New text:

```
        if False:
```

### `u198.D7_twice`

pair_discover: two playlists of one title are both found

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D7_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_two_playlists_taking_one_title_refuse_that_title_only`

Old text:

```
        if counted[one.title] > 1:
```

New text:

```
        if counted[one.title] > 2:
```

### `u198.D8_top_names`

pair_discover: a top folder the taxonomy names is walked

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D8_top_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_cratekits_own_trees_and_the_favorites_folder_are_never_discovered`

Old text:

```
        if top_id in roots or top_name in names or top_id in foreign:
```

New text:

```
        if top_id in roots or top_id in foreign:
```

### `u198.D9_foreign`

pair_discover: another app's top folder is walked

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D9_foreign`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_favourites_name_inside_another_apps_folder_does_not_unsettle_the_home`
  - `tests/test_sync_pair_discover.py::test_another_apps_top_folder_is_never_discovered`

Old text:

```
        if top_id in roots or top_name in names or top_id in foreign:
```

New text:

```
        if top_id in roots or top_name in names:
```

### `u202.D1_skip`

home_of: a folder the skip list names is made in

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D1_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_home_of_refuses_each_place_it_cannot_decide`

Old text:

```
        if folder in set(str(one) for one in skip):
```

New text:

```
        if False:
```

### `u202.D2_two_tops`

home_of: two top folders of the name, the first is taken

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D2_two_tops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_home_of_refuses_each_place_it_cannot_decide`

Old text:

```
        if len(top) > 1:
```

New text:

```
        if len(top) > 2:
```

### `u202.D3_longest`

home_of: the shortest subfolder name is read first

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D3_longest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_home_of_reads_the_longest_subfolder_and_strips_the_prefix`

Old text:

```
            longest = max(len(named(row)) for row in fits)
```

New text:

```
            longest = min(len(named(row)) for row in fits)
```

### `u202.D5_name_taken`

home_of: a name the folder already holds is made again beside it

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D5_name_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_playlist_of_the_name_no_pair_holds_is_left_and_named`

Old text:

```
    if here:
        where = " / ".join(path) or "the rekordbox root"
```

New text:

```
    if False:
        where = " / ".join(path) or "the rekordbox root"
```

### `u202.D6_favourites`

home_of: the folder holding the favourites is made in

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D6_favourites`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_home_of_refuses_the_folder_holding_the_favourites`

Old text:

```
            _attribute(row) == PLAIN
            and named(row) == favorites
            and str(getattr(row, "ParentID", "") or "") in above
```

New text:

```
            False
```

### `u216.M11_paired_raw`

downloaded_copy: compare the paired title as it stands, its folder prefix kept

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M11_paired_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_in_a_created_folder_is_named_a_copy`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_downloaded_copy_names_the_paired_title_it_copies`

Old text:

```
        if name_of(folder, one).casefold() == wanted:
```

New text:

```
        if one.casefold() == wanted:
```

### `u216.M12_empty_rest`

downloaded_copy: a title with nothing left after the prefix copies a playlist titled as the folder alone

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M12_empty_rest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_downloaded_copy_names_the_paired_title_it_copies`

Old text:

```
    if not wanted:
        return ""
    for one in sorted
```

New text:

```
    for one in sorted
```

### `u216.M1_held_record_ignored`

before_adoption: a playlist the record says the folder held reads as new, so it is made in rekordbox

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M1_held_record_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_before_adoption_reads_the_record_first`

Old text:

```
        if account_id in held:
            return (
```

New text:

```
        if False:
            return (
```

### `u216.M2_created_folder_by_time`

before_adoption: drop the created folder answer, so an unrecorded created folder is read by time and its new playlists named

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M2_created_folder_by_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_created_folder_without_a_record_still_brings_in`
  - `tests/test_sync_pair_adopted.py::test_before_adoption_reads_the_record_first`

Old text:

```
    if created:
        return ""
    unrecorded = (
```

New text:

```
    unrecorded = (
```

### `u216.M3_no_moment_reads_new`

before_adoption: an unrecorded folder with no made pair to date it reads every playlist as new

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M3_no_moment_reads_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`

Old text:

```
    if adopted is None:
        return (
```

New text:

```
    if adopted is None:
        return "" if True else (
```

### `u216.M4_no_time_reads_new`

before_adoption: a playlist with no creation time in an unrecorded folder reads as new

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M4_no_time_reads_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_a_creation_time_without_a_zone_is_no_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_or_a_creation_time_every_unpaired_playlist_is_named`

Old text:

```
    if made is None or made.tzinfo is None:
        return (
```

New text:

```
    if made is None or made.tzinfo is None:
        return "" if True else (
```

### `u216.M5_naive_time_trusted`

before_adoption: a creation time without a zone is compared as given

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M5_naive_time_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_a_creation_time_without_a_zone_is_no_time`

Old text:

```
    if made is None or made.tzinfo is None:
```

New text:

```
    if made is None:
```

### `u216.M6_equal_moment_new`

before_adoption: a playlist made at the adoption moment itself reads as new

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M6_equal_moment_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`

Old text:

```
    if made <= adopted:
```

New text:

```
    if made < adopted:
```

### `u216.M7_time_rule_off`

before_adoption: an unrecorded folder's playlist with a time never reads as held

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M7_time_rule_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_creation_time_decides`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_moment_is_read_from_this_folders_own_pairs`

Old text:

```
    if made <= adopted:
```

New text:

```
    if False:
```

### `u216.M8_moment_latest`

adoption_moment: the latest mark rather than the earliest, so a playlist made between two marks reads as held before

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M8_moment_latest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_the_adoption_moment_is_the_earliest_readable_mark`

Old text:

```
    return min(found) if found else None
```

New text:

```
    return max(found) if found else None
```

### `u216.M9_moment_naive_kept`

adoption_moment: keep a mark without a zone, which cannot be compared with the account's times

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M9_moment_naive_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_the_adoption_moment_is_the_earliest_readable_mark`

Old text:

```
        if moment.tzinfo is not None:
            found.append(moment)
```

New text:

```
        found.append(moment)
```

### `u242.M25_copy_needs_the_prefix`

pair discovery: read a copy only by its prefix, so a stripped copy is made in rekordbox again

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u242.json`, row `M25_copy_needs_the_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_pair_adopted.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_pairing_techno_with_a_stripped_former_downloaded_techno`

Old text:

```
    if not prefixed and not taken:
```

New text:

```
    if not prefixed:
```

### `u242.M27_copy_pool_reads_no_taken`

pair discovery: a taken title with no prefix reads every taken playlist beside it, so two of one name are each the other's copy

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u242.json`, row `M27_copy_pool_reads_no_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_pair_adopted.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_prefixed_copy_beside_a_taken_original_is_still_its_copy`

Old text:

```
        if other_id != account_id and not (plain_taken and other_id in held)
```

New text:

```
        if other_id != account_id
```

### `u304-b.S15_favourites_home_judged_without_the_foreign_check`

pair_discover.discover: a playlist named as the favourites one inside another app's folder counts as the Favorites home; S9's composite, the foreign check S9 hands every node to, removed

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u304-b.json`, row `S15_favourites_home_judged_without_the_foreign_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_adopted.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_favourites_name_inside_another_apps_folder_does_not_unsettle_the_home`

Old text:

```
        for row in foreign_tree.outside(
            [r for r in live if _attribute(r) == PLAIN and str(getattr(r, "Name", "") or "") == favorites],
            every,
        )
```

New text:

```
        for row in [r for r in live if _attribute(r) == PLAIN and str(getattr(r, "Name", "") or "") == favorites]
```

### `u304-b.S7_walk_keeps_removed_nodes`

pair_discover._live_children: a removed playlist is read as live (again, with test_a_playlist_deleted_in_rekordbox_is_never_found)

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u304-b.json`, row `S7_walk_keeps_removed_nodes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_adopted.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_in_rekordbox_is_never_found`

Old text:

```
    live = [row for row in every if not rb_writer.node_removed(row)]
    children: dict[str, list[Any]] = {}
```

New text:

```
    live = list(every)
    children: dict[str, list[Any]] = {}
```

### `u304.S8_walk_root_sentinel`

pair_discover._live_children: a node under the root sentinel is not filed under the root

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u304.json`, row `S8_walk_root_sentinel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_adopted.py`
- Collected: 114 against a baseline of 114
- Kills: 87 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_created_folder_without_a_record_still_brings_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_in_a_created_folder_is_named_a_copy`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_playlist_no_pair_names_still_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_a_created_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_the_adopted_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_a_creation_time_without_a_zone_is_no_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_or_a_creation_time_every_unpaired_playlist_is_named`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_creation_time_decides`
  - ... and 72 more, see the JSON sidecar

Old text:

```
        if parent in rb_writer.ROOT_PARENT_SENTINELS:
            parent = ""
        children.setdefault(parent, []).append(row)
    return every, live, children
```

New text:

```
        children.setdefault(parent, []).append(row)
    return every, live, children
```

