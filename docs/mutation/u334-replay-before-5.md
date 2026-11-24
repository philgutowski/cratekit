# Mutation table: u334-replay-before-5

Measured by `scripts/mutate.py` on 2026-11-24 04:12 UTC, branch `HEAD` at `89c9e120`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 351.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:12 UTC for commit `89c9e120f5d4`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 85, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u300.S21_mount_probe_local` | `src/cratekit/core/restore_recovery.py` | maintainer | 2 file(s) | 253 | 2 | killed |
| `u96-b.C1_engine_terminal` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 2 | killed |
| `u96-b.C2_engine_acknowledged` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `u96-b.C3_engine_occupied_target` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `u96-b.C4_engine_stub` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 5 | killed |
| `u96-b.C5_engine_library_is_mounted` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `r679-a.A1_supersede_guard_both_layers` | `src/cratekit/core/review.py` | user | 3 file(s) | 834 | 5 | killed |
| `r679-a.A8_actor_is_not_the_rule` | `src/cratekit/core/review.py` | user | 3 file(s) | 834 | 11 | killed |
| `r797-c.G7_a_folders_own_name_has_that_folder` | `src/cratekit/core/routing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r797-c.G8_a_map_row_is_a_style_sub` | `src/cratekit/core/routing.py` | user | 1 file(s) | 33 | 6 | killed |
| `r118-a.A2_enoent_refuses_too` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1592 | 169 | killed |
| `r1255.S2_absent_log_unread` | `src/cratekit/core/session.py` | user | 7 file(s) | 867 | 46 | killed |
| `r239-b.S11_readback_key_on` | `src/cratekit/core/session.py` | user | 7 file(s) | 724 | 1 | killed |
| `r375-a.S1_keep_is_ignored` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 38 | killed |
| `r375-a.S2_record_inside_the_watch` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 3 | killed |
| `r375-a.S3_a_raise_is_not_abandoned` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 13 | killed |
| `r375-a.S6_close_ignores_the_intent` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 11 | killed |
| `r1665.S15_recorded_before_the_copy_lands` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 316 | 72 | killed |
| `u272.E1_verified_ignores_verdict` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 642 | 11 | killed |
| `u272.E2_gate_trusts_manifest` | `src/cratekit/core/snapshot.py` | user | 7 file(s) | 642 | 9 | killed |
| `u272.S13_parents_before_children` | `src/cratekit/core/snapshot.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u953.M16_captured_paths_drops_the_playlist` | `src/cratekit/core/snapshot.py` | user | 4 file(s) | 303 | 73 | killed |
| `u953.M17_nearest_existing_asks_the_path_itself` | `src/cratekit/core/snapshot.py` | user | 3 file(s) | 209 | 118 | killed |
| `r432-b.B5_lock_on_the_library_volume` | `src/cratekit/core/state_files.py` | user | 4 file(s) | 342 | 17 | killed |
| `r432-b.B6_lock_directory_renamed` | `src/cratekit/core/state_files.py` | maintainer | 4 file(s) | 342 | 1 | killed |
| `u278.M1_gate_follows_state` | `src/cratekit/core/state_files.py` | user | 4 file(s) | 493 | 6 | killed |
| `u278.M3_pointer_reads_state_dir` | `src/cratekit/core/state_files.py` | user | 3 file(s) | 433 | 3 | killed |
| `u299.U1_installation_never_restored` | `src/cratekit/core/state_files.py` | user | 3 file(s) | 431 | 72 | killed |
| `u299.U5_library_snapshot_passed` | `src/cratekit/core/state_files.py` | user | 3 file(s) | 431 | 111 | killed |
| `r722.T9_lenient_open_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2994 | 306 | killed |
| `u249.M15_noting_reader_drops_field_failure` | `src/cratekit/core/tags.py` | user | 3 file(s) | 694 | 1 | killed |
| `u249.M16_noting_reader_drops_open_failure` | `src/cratekit/core/tags.py` | user | 3 file(s) | 694 | 2 | killed |
| `u249.M17_noting_reader_drops_unrecognised` | `src/cratekit/core/tags.py` | user | 3 file(s) | 694 | 3 | killed |
| `u249.M18_noting_reader_drops_unsupported` | `src/cratekit/core/tags.py` | maintainer | 3 file(s) | 694 | 1 | killed |
| `u249.M19_noting_reader_inverted` | `src/cratekit/core/tags.py` | user | 3 file(s) | 694 | 6 | killed |
| `u250.M5_word_reads_zero` | `src/cratekit/core/tags.py` | user | 3 file(s) | 215 | 1 | killed |
| `u250.M6_absent_raises` | `src/cratekit/core/tags.py` | user | 3 file(s) | 215 | 20 | killed |
| `u250.M8_conversion_learns_decimals` | `src/cratekit/core/tags.py` | user | 3 file(s) | 215 | 1 | killed |
| `r799-a.L6_a_word_is_matched_whatever_its_case` | `src/cratekit/core/taxonomy_build.py` | user | 3 file(s) | 511 | 48 | killed |
| `r431-a.A1_a_plain_row_gains_a_companion` | `src/cratekit/core/tombstone.py` | user | 6 file(s) | 1278 | 21 | killed |
| `r431-a.A2_one_kind_for_both` | `src/cratekit/core/tombstone.py` | user | 6 file(s) | 1278 | 17 | killed |
| `r239-b.S6_delete_key_off` | `src/cratekit/deletion/cli.py` | user | 7 file(s) | 724 | 1 | killed |
| `r431-a.A3_stripped_from_the_title_column` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1113 | 2 | killed |
| `r431-a.A5_the_companion_names_no_tombstone` | `src/cratekit/deletion/stores.py` | user | 6 file(s) | 1113 | 7 | killed |
| `r227.C4_export_limit_spelled` | `src/cratekit/export/cli.py` | user | 1 file(s) | 123 | 1 | killed |
| `r229.C1_the_offer_is_not_digested` | `src/cratekit/export/cli.py` | user | 1 file(s) | 123 | 1 | killed |
| `r229.C2_the_flag_declines_nothing` | `src/cratekit/export/cli.py` | user | 1 file(s) | 123 | 3 | killed |
| `r229.C3_no_remote_id_is_frozen` | `src/cratekit/export/cli.py` | user | 1 file(s) | 123 | 1 | killed |
| `r356-b.B9_export_item_report_drops_the_reason` | `src/cratekit/export/cli.py` | user | 1 file(s) | 113 | 1 | killed |
| `r850-a.E1_written_count` | `src/cratekit/export/cli.py` | user | 2 file(s) | 236 | 5 | killed |
| `r850-a.E2_unmatched_count` | `src/cratekit/export/cli.py` | user | 1 file(s) | 123 | 2 | killed |
| `r850-a.E3_listing_dropped` | `src/cratekit/export/cli.py` | user | 2 file(s) | 236 | 6 | killed |
| `r850-a.E4_reason_gate` | `src/cratekit/export/cli.py` | user | 2 file(s) | 236 | 1 | killed |
| `r850-a.E5_slug_is_no_reason` | `src/cratekit/export/cli.py` | user | 2 file(s) | 236 | 2 | killed |
| `r850-a.E6_no_match_sentence` | `src/cratekit/export/cli.py` | user | 2 file(s) | 236 | 2 | killed |
| `u131.K11_filing_in_digest` | `src/cratekit/export/cli.py` | user | 2 file(s) | 137 | 1 | killed |
| `u131.K13_unfiled_warning` | `src/cratekit/export/cli.py` | user | 1 file(s) | 123 | 2 | killed |
| `u270.C1_export_names_its_batch_form` | `src/cratekit/export/cli.py` | user | 4 file(s) | 290 | 7 | killed |
| `u270.C2_stop_while_planning` | `src/cratekit/export/cli.py` | user | 2 file(s) | 145 | 1 | killed |
| `u270.C3_refused_track_fails_its_item` | `src/cratekit/export/cli.py` | user | 2 file(s) | 145 | 1 | killed |
| `u270.C4_created_said_once` | `src/cratekit/export/cli.py` | user | 2 file(s) | 145 | 2 | killed |
| `u270.C5_unfiled_said_once` | `src/cratekit/export/cli.py` | user | 3 file(s) | 159 | 2 | killed |
| `u270.C6_one_tracks_failure_is_its_own` | `src/cratekit/export/cli.py` | user | 2 file(s) | 145 | 1 | killed |
| `u51-item-derivation.H1_export_item_not_payload` | `src/cratekit/export/cli.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u51-item-derivation.H3_frozen_config_ignored` | `src/cratekit/export/cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r836-g.C3_dangling_rows_are_rows` | `src/cratekit/export/prune_cli.py` | user | 5 file(s) | 404 | 1 | killed |
| `u142.S12_undeclared_reads_as_empty` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 97 | 1 | killed |
| `u267.M12_inspiration_set_folder_write_guard` | `src/cratekit/export/set_common.py` | maintainer | 2 file(s) | 70 | 1 | killed |
| `r227.C5_favorites_limit_spelled` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 239 | 1 | killed |
| `r424.B1_colored_key` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 239 | 1 | killed |
| `r424.B3_resume_standing` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 239 | 3 | killed |
| `r424.B4_warning_copied` | `src/cratekit/favorites/cli.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |
| `r856-a.F10_concluded_passed` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 1 | killed |
| `r856-a.F11_warning_total` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 2 | killed |
| `r856-a.F1_hearted_count` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 2 | killed |
| `r856-a.F2_already_count` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 1 | killed |
| `r856-a.F3_unmatched_count` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 1 | killed |
| `r856-a.F4_listing_dropped` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 2 | killed |
| `r856-a.F5_listing_off_reasons` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 2 | killed |
| `r856-a.F6_no_match_sentence` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 2 | killed |
| `r856-a.F7_names_from_listing` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 1 | killed |
| `r856-a.F8_item_listing` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 1 | killed |
| `r856-a.F9_item_reason_carried` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 1 | killed |
| `u51-item-derivation.A1b_colour_writer_passed` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 123 | 1 | killed |
| `u51-item-derivation.H2_hearts_item_not_payload` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 123 | 14 | killed |
| `u173.M21_gate_name` | `src/cratekit/intake/analyzed_cli.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1499.B08_kept_identity` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 5 | killed |
| `r1499.B09_unlistable` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.B10_plain_step_moves_out` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 2 | killed |
| `r1295.M16_set_aside_one_word` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 221 | 4 | killed |
| `r504-b.B1_verb_drops_short` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 596 | 3 | killed |
| `r504-b.B4_no_progress_block` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 596 | 5 | killed |
| `r504-b.B6_warning_reworded` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 596 | 3 | killed |
| `r679-b.D1_intake_gate_on_question_alone` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 834 | 2 | killed |
| `u249.M21_intake_reset_leaves_reader` | `src/cratekit/intake/cli.py` | maintainer | 3 file(s) | 128 | 1 | killed |
| `r740-b.E2_average_bpm_nonzero` | `src/cratekit/intake/collection_xml.py` | user | 5 file(s) | 113 | 16 | killed |
| `r770-d.S1_composite_the_splice_takes_a_stub` | `src/cratekit/intake/collection_xml.py` | user | 4 file(s) | 85 | 2 | killed |
| `r685-b.P1_place_files_rereads_the_registry` | `src/cratekit/intake/ingest.py` | maintainer | 1 file(s) | 23 | 1 | killed |
| `r740-b.I1_tag_key_first` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 89 | 3 | killed |
| `r740-b.I3_stem_is_the_title` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 89 | 2 | killed |
| `r740-b.I4_lossy_is_the_parameter` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 89 | 1 | killed |
| `r740-b.I5_body_marker_marks` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 89 | 1 | killed |
| `r740-c.I2_no_stem_fallback` | `src/cratekit/intake/ingest.py` | user | 4 file(s) | 89 | 1 | killed |
| `u150.F1_blank_ref_claims` | `src/cratekit/intake/label_filing.py` | user | 2 file(s) | 78 | 2 | killed |
| `r1467.M19_root_unreadable_refuses` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 276 | 1 | killed |
| `r1467.M20_retired_file_proves` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 276 | 1 | killed |
| `r1467.M21_native_record_proves` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 276 | 1 | killed |
| `r1467.M22_proof_is_a_file` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 276 | 1 | killed |
| `u188.M5_repeat_kept` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |
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
| `u110-c.C1_apply_playlist` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 201 | 8 | killed |
| `u110-c.C8_plain_dot` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 201 | 3 | killed |
| `u156.L25_shared_rule_near_match` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 69 | 1 | killed |
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
| `r679-b.D5_missing_per_row_gate_on_question_alone` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 834 | 1 | killed |
| `u173.M24_analyze_name` | `src/cratekit/intake/native.py` | user | 1 file(s) | 38 | 1 | killed |
| `u175.R1_account_ids_unrecorded` | `src/cratekit/intake/rotate.py` | user | 4 file(s) | 83 | 3 | killed |
| `u267.M11_rotation_opens_its_own` | `src/cratekit/intake/rotate_cli.py` | user | 2 file(s) | 44 | 4 | killed |
| `u144-c.C8_question_named` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 38 | 1 | killed |
| `u307.R18_no_match_drops_unanswered` | `src/cratekit/intake/set_playlist.py` | user | 3 file(s) | 177 | 1 | killed |
| `u107-c.S19_approved_superseded` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u108-c.G21_listing_skips_already` | `src/cratekit/label/approved_cli.py` | user | 4 file(s) | 364 | 2 | killed |
| `u108-c.G22_listing_excuse_applies` | `src/cratekit/label/approved_cli.py` | user | 4 file(s) | 364 | 1 | killed |
| `r382.M16_parser_moved_lowercase` | `src/cratekit/label/catalogue.py` | maintainer | 10 file(s) | 805 | 2 | killed |
| `r504-a.A10_block_listed` | `src/cratekit/label/catalogue.py` | user | 10 file(s) | 805 | 11 | killed |
| `r504-a.A8_withheld_sign` | `src/cratekit/label/catalogue.py` | user | 10 file(s) | 805 | 15 | killed |
| `r504-a.A9_summary_reworded` | `src/cratekit/label/catalogue.py` | user | 10 file(s) | 805 | 10 | killed |
| `r515-operator.S1_of_takes_bool` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r515-operator.S2_of_takes_non_int` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r515-operator.S4_of_short_at_count` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r515-operator.S5_of_short_over_count` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r515-operator.S6_cache_drops_short` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 95 | 1 | killed |
| `r840-c.C4_no_name_is_the_empty_string` | `src/cratekit/label/catalogue.py` | user | 2 file(s) | 354 | 4 | killed |
| `u308.L4_translated_swallows_refusal` | `src/cratekit/label/catalogue.py` | user | 4 file(s) | 467 | 8 | killed |
| `u62.C2_outage_as_credential` | `src/cratekit/label/catalogue.py` | user | 4 file(s) | 503 | 4 | killed |
| `u97-b.B3_label_path_raises_the_other_token` | `src/cratekit/label/catalogue.py` | user | 3 file(s) | 1611 | 1 | killed |
| `r259.L1_job_cache_read` | `src/cratekit/label/cli.py` | maintainer | 4 file(s) | 552 | 1 | killed |
| `r261.W1_worker_refuses` | `src/cratekit/label/cli.py` | user | 4 file(s) | 522 | 2 | killed |
| `r261.W2_remedy` | `src/cratekit/label/cli.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.W3_retryable` | `src/cratekit/label/cli.py` | user | 4 file(s) | 522 | 1 | killed |
| `r290-author.S06_label_call_removed` | `src/cratekit/label/cli.py` | user | 2 file(s) | 208 | 17 | killed |
| `r504-a.A11_boundary_refuses` | `src/cratekit/label/cli.py` | user | 4 file(s) | 0 | collection error | collect-error |
| `r504-a.A12_boundary_drops_short` | `src/cratekit/label/cli.py` | user | 4 file(s) | 552 | 5 | killed |
| `r515-operator.S14_harvest_no_warning` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u100-b.C10_added_message` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C1_name_accepted` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C2_to_accepted` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C3_outcome_always_ok` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 2 | killed |
| `u100-b.C4_empty_says_nothing` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C5_nameless_unreported` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C6_held_name_hidden` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C7_refused_reads_as_note` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u100-b.C9_dispatch` | `src/cratekit/label/cli.py` | user | 2 file(s) | 47 | 12 | killed |
| `u100-c.C8_refused_counted_present_after_fix` | `src/cratekit/label/cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `u109-b.B4_resume_dropped` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 47 | killed |
| `u109-b.B5_refusal_reason` | `src/cratekit/label/cli.py` | user | 2 file(s) | 1102 | 2 | killed |
| `u109-b.B6_message_drops_verb` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u109-b.B7_step_drops_verb` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u109-b.B8_itemless_branch` | `src/cratekit/label/cli.py` | user | 1 file(s) | 82 | 1 | killed |
| `u109-b.B9_queue_again` | `src/cratekit/label/cli.py` | user | 2 file(s) | 1102 | 2 | killed |
| `u341.G22_empty_registry_step` | `src/cratekit/label/cli.py` | user | 5 file(s) | 410 | 1 | killed |
| `u341.G4_unknown_genre_walks_every_label` | `src/cratekit/label/cli.py` | user | 5 file(s) | 410 | 5 | killed |
| `u341.G5_genre_shape_unchecked` | `src/cratekit/label/cli.py` | user | 5 file(s) | 410 | 4 | killed |
| `u341.G6_undeclared_never_said` | `src/cratekit/label/cli.py` | user | 5 file(s) | 410 | 1 | killed |
| `u341.G7_undeclared_inverted` | `src/cratekit/label/cli.py` | user | 5 file(s) | 410 | 2 | killed |
| `u341.G8_list_ignores_genre` | `src/cratekit/label/cli.py` | user | 5 file(s) | 410 | 3 | killed |
| `u341.G9_list_refuses_genre` | `src/cratekit/label/cli.py` | user | 5 file(s) | 410 | 3 | killed |
| `u52-item-derivation.H2_listing_passthrough_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u52-item-derivation.H4_verification_boundary_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 2 | killed |
| `u52-item-derivation.H6_empty_playlist_reports_ok` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 2 | killed |
| `u52-item-derivation.H7_unresolved_drops_nameless` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u52-item-derivation.I5_import_queues_no_item` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 4 | killed |
| `u52-item-derivation.I6_import_item_keyed_on_name` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 2 | killed |
| `u52-item-derivation.R1_itemless_job_drives` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 3 | killed |
| `u52-item-derivation.S1_errors_branch_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u52-zero-rows.H5_verifier_passthrough_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u99-b.B1_parser_limit_floor` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-b.B5_add_drops_seeds` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 11 | killed |
| `u99-b.B6_add_drops_limit` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 3 | killed |
| `u99-b.B7_set_drops_seeds` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 2 | killed |
| `u99-b.B8_list_json_empty` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 12 | killed |
| `u99-b.B9_detail_drops_seeds` | `src/cratekit/label/cli.py` | user | 3 file(s) | 293 | 1 | killed |
| `r888.C1_probe_ignores_held` | `src/cratekit/label/crawl.py` | user | 5 file(s) | 578 | 7 | killed |
| `r888.C2_probe_trusts_held` | `src/cratekit/label/crawl.py` | user | 5 file(s) | 578 | 1 | killed |
| `u191.M21_unsettled_answers_read` | `src/cratekit/label/dated.py` | user | 3 file(s) | 145 | 2 | killed |
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

## Zero rows and what they owe

- `u272.S13_parents_before_children` (maintainer facing): maintainer facing, composite not required
- `u51-item-derivation.H1_export_item_not_payload` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r424.B4_warning_copied` (maintainer facing): maintainer facing, composite not required
- `u188.M5_repeat_kept` (maintainer facing): maintainer facing, composite not required
- `u71-b.B13_unlink_destination` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u300.S21_mount_probe_local`

assert_library_volume_is_gone asks the part's own mount probe, so a patched probe is not asked

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u300.json`, row `S21_mount_probe_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`
  - `tests/test_restore_cli.py::test_the_verb_refuses_without_the_acceptance_flag`

Old text:

```
    probe = mount_probe or _restore()._is_mount_point
```

New text:

```
    probe = mount_probe or _is_mount_point
```

### `u96-b.C1_engine_terminal`

SAMPLE of the engine's guards, now reachable from a verb. bare_metal_session: disarm the controlling terminal refusal

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u96-b.json`, row `C1_engine_terminal`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_needs_a_terminal_and_an_explicit_decision`
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[nobody is at a terminal]`

Old text:

```
    if not probe():
        raise _refuse_target(
            "this invocation has no controlling terminal
```

New text:

```
    if False:
        raise _refuse_target(
            "this invocation has no controlling terminal
```

### `u96-b.C2_engine_acknowledged`

SAMPLE. bare_metal_session: disarm the acknowledgment refusal

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u96-b.json`, row `C2_engine_acknowledged`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_needs_a_terminal_and_an_explicit_decision`
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[the replacement was not accepted]`
  - `tests/test_restore_cli.py::test_the_verb_refuses_without_the_acceptance_flag`

Old text:

```
    if not acknowledged:
```

New text:

```
    if False:
```

### `u96-b.C3_engine_occupied_target`

SAMPLE. assert_recovery_target: disarm the refusal of a target that already holds a database

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u96-b.json`, row `C3_engine_occupied_target`
- Moved: Anchored where u300-replay-after-c.json replayed it: the same text, now in src/cratekit/core/restore_recovery.py, was in src/cratekit/core/restore.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    if existing and not replacing_existing:
```

New text:

```
    if False:
```

### `u96-b.C4_engine_stub`

SAMPLE. assert_recovery_target: disarm the refusal of the stub an unmounted volume leaves on the internal disk

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u96-b.json`, row `C4_engine_stub`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 253 against a baseline of 253
- Kills: 5 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stub_an_unmounted_volume_leaves_behind`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stubs_beside_and_beneath_the_mount_point[library 1-why1]`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stubs_beside_and_beneath_the_mount_point[library/Music-why0]`
  - `tests/test_restore.py::test_round2_the_real_mount_probe_is_armed_by_default`
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[the target is the stub on the internal disk]`

Old text:

```
    if (inside_configured or beside_configured) and not probe(where):
```

New text:

```
    if False:
```

### `u96-b.C5_engine_library_is_mounted`

SAMPLE. assert_library_volume_is_gone: answer gone when the library is mounted and is the recorded volume

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u96-b.json`, row `C5_engine_library_is_mounted`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_is_refused_while_the_library_is_reachable`
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[the library is still mounted]`
  - `tests/test_restore_cli.py::test_the_verb_refuses_while_the_library_is_mounted`

Old text:

```
    raise _refuse_target(
        f"the library at {cfg.library.root} is mounted and is the volume this "
```

New text:

```
    return preflight.MountState.NOT_MOUNTED
    raise _refuse_target(
        f"the library at {cfg.library.root} is mounted and is the volume this "
```

### `r679-a.A1_supersede_guard_both_layers`

supersede: drop the empty column condition from the read and the write together, so a person's verdict is overwritten

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A1_supersede_guard_both_layers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 834 against a baseline of 834
- Kills: 5 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_review_queue.py::test_supersede_never_overwrites_a_persons_verdict[accepted]`
  - `tests/test_review_queue.py::test_supersede_never_overwrites_a_persons_verdict[rejected]`
  - `tests/test_review_queue.py::test_supersede_never_overwrites_a_verdict_this_build_cannot_read`
  - `tests/test_review_queue.py::test_supersede_takes_several_identifiers_and_retires_only_the_open_ones_among_them`

Old text:

```
            f"SELECT item_id FROM review_items WHERE item_id IN ({marks}) "
            f"AND verdict IS NULL ORDER BY ordinal",
            wanted,
        )
    )
    if not open_ids:
        return ()
    now = timestamp()
    marks = ", ".join("?" for _ in open_ids)
    with store.immediate() as conn:
        conn.execute(
            f"UPDATE review_items SET verdict = ?, option = NULL, actor = ?, decided = ?, "
            f"updated = ? WHERE item_id IN ({marks}) AND verdict IS NULL",
```

New text:

```
            f"SELECT item_id FROM review_items WHERE item_id IN ({marks}) "
            f"ORDER BY ordinal",
            wanted,
        )
    )
    if not open_ids:
        return ()
    now = timestamp()
    marks = ", ".join("?" for _ in open_ids)
    with store.immediate() as conn:
        conn.execute(
            f"UPDATE review_items SET verdict = ?, option = NULL, actor = ?, decided = ?, "
            f"updated = ? WHERE item_id IN ({marks})",
```

### `r679-a.A8_actor_is_not_the_rule`

supersede: write a fixed word as the actor instead of the rule that owned the row

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A8_actor_is_not_the_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 834 against a baseline of 834
- Kills: 11 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`
  - `tests/test_review_queue.py::test_a_batch_resolution_does_not_touch_items_a_resolution_superseded`
  - `tests/test_review_queue.py::test_a_superseded_item_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_review_queue.py::test_an_export_carrying_the_third_verdict_imports_without_conflict`
  - `tests/test_review_queue.py::test_an_import_carries_the_machines_verdict_under_the_machines_rules`
  - `tests/test_review_queue.py::test_supersede_retires_an_open_item_naming_the_rule_and_it_leaves_the_open_list`
  - `tests/test_review_queue.py::test_supersede_takes_several_identifiers_and_retires_only_the_open_ones_among_them`

Old text:

```
            (str(Verdict.SUPERSEDED), rule, now, now, *open_ids),
```

New text:

```
            (str(Verdict.SUPERSEDED), "resolution", now, now, *open_ids),
```

### `r797-c.G7_a_folders_own_name_has_that_folder`

folder_of: count a track tagged with the source routed folder's own name as a word in its default sub

- File: `src/cratekit/core/routing.py`
- Source: `r797-c.json`, row `G7_a_folders_own_name_has_that_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_report_genres.py::test_the_source_routed_folders_own_name_has_that_folder`

Old text:

```
    if by_source is None or resolution.match is Match.PASSTHROUGH:
```

New text:

```
    if by_source is None:
```

### `r797-c.G8_a_map_row_is_a_style_sub`

folder_of: read every source string of a source routed folder as landing in its default

- File: `src/cratekit/core/routing.py`
- Source: `r797-c.json`, row `G8_a_map_row_is_a_style_sub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_report_genres.py`
- Collected: 33 against a baseline of 33
- Kills: 6 (killed)
- Killed:
  - `tests/test_report_genres.py::test_a_genre_filed_whole_in_its_sub_names_no_other_spelling`
  - `tests/test_report_genres.py::test_another_spelling_of_a_style_subs_own_name_is_counted_with_it`
  - `tests/test_report_genres.py::test_where_routing_files_a_genre_is_whether_it_has_a_folder_of_its_own[Alternative-expected2]`
  - `tests/test_report_genres.py::test_where_routing_files_a_genre_is_whether_it_has_a_folder_of_its_own[Indie Rock-expected3]`
  - `tests/test_report_genres.py::test_where_routing_files_a_genre_is_whether_it_has_a_folder_of_its_own[Punk-expected4]`
  - `tests/test_report_genres.py::test_where_routing_files_a_genre_is_whether_it_has_a_folder_of_its_own[Rock-expected5]`

Old text:

```
    if value in by_source.map:
```

New text:

```
    if False:
```

### `r118-a.A2_enoent_refuses_too`

A fresh installation with no index refuses instead of answering nothing recorded, so the product cannot be set up

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A2_enoent_refuses_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1592 against a baseline of 1592
- Kills: 169 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_bound_identifier_resolves_its_seams_at_call_time`
  - `tests/intake/test_recognition.py::test_the_keychain_credentials_are_read_by_name_and_a_missing_one_is_credential_missing`
  - `tests/intake/test_recognition.py::test_the_paid_path_will_not_run_without_the_section_and_the_gate_runs_first[no-credentials]`
  - `tests/intake/test_recognition.py::test_the_paid_path_will_not_run_without_the_section_and_the_gate_runs_first[no-section]`
  - `tests/intake/test_recognition.py::test_the_seam_binds_this_identifier_when_none_is_injected`
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/intake/test_workers.py::test_a_missing_recording_is_refused_by_name_and_a_tilde_is_expanded_before_the_look`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`
  - `tests/intake/test_workers.py::test_a_repeated_recording_in_one_set_is_one_item_per_play_and_one_per_fold`
  - `tests/intake/test_workers.py::test_a_second_identify_over_the_same_recording_makes_zero_transport_calls`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_set_nobody_recognised_is_an_honest_zero_that_says_what_it_cost`
  - `tests/intake/test_workers.py::test_a_set_where_chunks_got_no_answer_and_the_rest_named_nothing_is_a_failure_not_a_zero`
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`
  - ... and 154 more, see the JSON sidecar

Old text:

```
    except FileNotFoundError:
        return frozenset()
    except OSError as exc:
```

New text:

```
    except OSError as exc:
```

### `r1255.S2_absent_log_unread`

_listed: read a log that is not there as refused, so a library with no session refuses every write

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S2_absent_log_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`, `tests/test_doctor.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 867 against a baseline of 867
- Kills: 46 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_green_doctor_exits_zero`
  - `tests/test_doctor.py::test_a_headless_machine_that_opted_into_the_environment_fallback_is_not_red`
  - `tests/test_doctor.py::test_a_library_with_no_sessions_still_reports_a_clean_log`
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_doctor.py::test_no_ok_detail_claims_a_volume_the_run_never_identified`
  - `tests/test_doctor.py::test_the_backup_flags_are_recorded_without_a_question`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_strong_claim_survives_where_the_identity_really_was_compared`
  - `tests/test_doctor.py::test_the_wizard_on_a_clean_machine_produces_a_valid_config_and_a_green_doctor`
  - `tests/test_inbox_unmirrored.py::test_a_dated_playlist_with_no_batch_folder_still_says_so`
  - `tests/test_inbox_unmirrored.py::test_an_absent_session_log_is_no_record_at_all`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`
  - ... and 31 more, see the JSON sidecar

Old text:

```
        return os.listdir(directory)
    except FileNotFoundError:
        return None
```

New text:

```
        return os.listdir(directory)
    except FileNotFoundError:
        raise
```

### `r239-b.S11_readback_key_on`

the session read-back pins the old True default, which a plain database cannot open under

- File: `src/cratekit/core/session.py`
- Source: `r239-b.json`, row `S11_readback_key_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 724 against a baseline of 724
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
    open_fresh = reopen or (lambda: rb_writer.open_db(cfg=cfg))
```

New text:

```
    open_fresh = reopen or (lambda: rb_writer.open_db(cfg=cfg, unlock=True))
```

### `r375-a.S1_keep_is_ignored`

assert_gates: keep a record for nobody, so Keep.RECORD yields Gates.record None

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S1_keep_is_ignored`
- Moved: U953 inlined _recorded into assert_gates, so the record is now opened directly or left None, and asking for it under Keep.NOTHING is the same record kept for nobody
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 393 against a baseline of 393
- Kills: 38 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_restore.py::test_a_restore_the_analysis_watch_refuses_is_not_on_record_as_finished`
  - `tests/test_restore.py::test_the_recovery_session_closes_its_own_record_on_both_paths`
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_failure_mid_loop_leaves_nothing_pending_on_the_handle`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_tree_writer.py::test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts`
  - ... and 23 more, see the JSON sidecar

Old text:

```
            if keep is Keep.RECORD
            else None
```

New text:

```
            if keep is Keep.NOTHING
            else None
```

### `r375-a.S2_record_inside_the_watch`

assert_gates: open the record INSIDE the analysis watch, the ordering fault the review found, so it closes CLOSED before the watch judges

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S2_record_inside_the_watch`
- Moved: U953 inlined _recorded into assert_gates, so the record's whole open, close and abandon block now sits outside the watch, and nesting that block inside the watch is the same ordering fault
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 393 against a baseline of 393
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_a_restore_the_analysis_watch_refuses_is_not_on_record_as_finished`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_write_session.py::test_the_record_closes_after_the_analysis_watch_has_judged_the_session`

Old text:

```
        try:
            with analysis_files_unmoved(watched) if watched else nullcontext():
                yield Gates(
                    workflow=workflow,
                    lock=held,
                    acknowledgment=acknowledgment,
                    volume=volume,
                    intent=intent,
                    record=record,
                )
            if record is not None:
                close_session(
                    record,
                    resolved,
                    state=SessionState.CLOSED,
                    intent=intent,
                    identity_provider=identity_provider,
                    mount_enumerator=mount_enumerator,
                    now=now,
                )
        except BaseException:
            if record is not None:
                try:
                    close_session(record, resolved, state=SessionState.ABANDONED, now=now)
                except Exception:  # noqa: BLE001 - the session's own error is the one to surface
                    logger.warning(
                        "session %s could not be recorded as abandoned",
                        record.session_id,
                        exc_info=True,
   
... truncated ...
```

New text:

```
        with analysis_files_unmoved(watched) if watched else nullcontext():
            try:
                yield Gates(
                    workflow=workflow,
                    lock=held,
                    acknowledgment=acknowledgment,
                    volume=volume,
                    intent=intent,
                    record=record,
                )
                if record is not None:
                    close_session(
                        record,
                        resolved,
                        state=SessionState.CLOSED,
                        intent=intent,
                        identity_provider=identity_provider,
                        mount_enumerator=mount_enumerator,
                        now=now,
                    )
            except BaseException:
                if record is not None:
                    try:
                        close_session(record, resolved, state=SessionState.ABANDONED, now=now)
                    except Exception:  # noqa: BLE001 - the session's own error is the one to surface
                        logger.warning(
                            "session %s could not be recorded as abandoned",
                 
... truncated ...
```

### `r375-a.S3_a_raise_is_not_abandoned`

_recorded: drop the abandoning close, so a body that raised leaves its record OPEN

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S3_a_raise_is_not_abandoned`
- Moved: U953 inlined _recorded into assert_gates, so the abandoning close is now its own line there and replacing it with pass is the same record left open
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 393 against a baseline of 393
- Kills: 13 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_restore.py::test_a_restore_the_analysis_watch_refuses_is_not_on_record_as_finished`
  - `tests/test_restore.py::test_the_recovery_session_closes_its_own_record_on_both_paths`
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_tree_writer.py::test_a_membership_write_that_fails_is_abandoned_and_claims_no_commit`
  - `tests/test_tree_writer.py::test_a_write_that_fails_after_counting_a_membership_still_claims_no_commit`
  - `tests/test_tree_writer.py::test_the_write_commits_behind_a_verified_capture`
  - `tests/test_write_session.py::test_a_body_that_raises_closes_abandoned_and_its_own_error_surfaces`
  - `tests/test_write_session.py::test_a_clean_close_that_refuses_ends_abandoned_rather_than_open`
  - `tests/test_write_session.py::test_the_record_closes_after_the_analysis_watch_has_judged_the_session`

Old text:

```
                    close_session(record, resolved, state=SessionState.ABANDONED, now=now)
```

New text:

```
                    pass
```

### `r375-a.S6_close_ignores_the_intent`

_recorded: close every record as an ordinary WRITE, so a recovery's close is gated by the latch it is the remedy for

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S6_close_ignores_the_intent`
- Moved: U953 inlined _recorded into assert_gates, so the clean close is now there and passing Intent.WRITE to it is the same intent ignored
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 393 against a baseline of 393
- Kills: 11 (killed)
- Killed:
  - `tests/test_restore.py::test_a_coupled_file_the_capture_records_as_absent_is_removed_again`
  - `tests/test_restore.py::test_a_recovery_is_not_refused_by_the_latch_whose_remedy_it_is`
  - `tests/test_restore.py::test_a_rehearsal_reports_what_is_outstanding_rather_than_what_it_recorded`
  - `tests/test_restore.py::test_a_restore_returns_the_coupled_state_with_the_database`
  - `tests/test_restore.py::test_blocking_2_a_failure_mid_restore_is_a_structured_refusal`
  - `tests/test_restore.py::test_blocking_5_an_interrupted_restore_in_a_none_effect_window_latches`
  - `tests/test_restore.py::test_round2_a_completed_restore_discharges_an_earlier_interrupted_one`
  - `tests/test_restore.py::test_round2_repeating_a_failing_restore_does_not_accumulate_latches`
  - `tests/test_restore.py::test_round2_three_attempts_stage_their_logs_side_by_side`
  - `tests/test_restore.py::test_round6_the_performing_backstop_names_what_it_already_moved`
  - `tests/test_write_session.py::test_a_recovery_closes_as_a_recovery`

Old text:

```
                    state=SessionState.CLOSED,
                    intent=intent,
                    identity_provider=identity_provider,
```

New text:

```
                    state=SessionState.CLOSED,
                    intent=Intent.WRITE,
                    identity_provider=identity_provider,
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

### `u272.S13_parents_before_children`

_flush: walk top down, so a directory is flushed before the files in it

- File: `src/cratekit/core/snapshot.py`
- Source: `u272.json`, row `S13_parents_before_children`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
capture_root, topdown=False, onerror=_raise_walk_error
```

New text:

```
capture_root, topdown=True, onerror=_raise_walk_error
```

### `u953.M16_captured_paths_drops_the_playlist`

captured_paths leaves out the legacy playlist file, so restore no longer counts it among its targets and capture room omits it

- File: `src/cratekit/core/snapshot.py`
- Source: `u953.json`, row `M16_captured_paths_drops_the_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_snapshot.py`, `tests/test_snapshot_check_room_r1677.py`, `tests/test_restore_cli.py`
- Collected: 303 against a baseline of 303
- Kills: 73 (killed)
- Killed:
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
  - `tests/test_restore.py::test_a_restore_taken_after_the_cutover_marks_nothing`
  - ... and 58 more, see the JSON sidecar

Old text:

```
    return frozenset({*database_paths(cfg), *config.snapshot_sources(cfg), playlist})
```

New text:

```
    return frozenset({*database_paths(cfg), *config.snapshot_sources(cfg)})
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

### `u278.M1_gate_follows_state`

state_path: drop the gate's own resolution, so the gate follows a redirected CRATEKIT_STATE_DIR and a copy gets a fresh hour

- File: `src/cratekit/core/state_files.py`
- Source: `u278.json`, row `M1_gate_follows_state`
- Moved: the same text, now in src/cratekit/core/state_files.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_config.py`, `tests/test_isrc_cache.py`
- Collected: 493 against a baseline of 493
- Kills: 6 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_rehearsal_keeps_the_live_isrc_cache_and_restores_the_environment`
  - `tests/test_provider_budget.py::test_a_call_made_under_a_redirected_state_directory_is_counted_by_the_live_gate`
  - `tests/test_provider_budget.py::test_a_redirected_state_directory_still_resolves_the_one_gate`
  - `tests/test_provider_budget.py::test_a_rehearsal_spends_from_the_live_gate[False]`
  - `tests/test_provider_budget.py::test_a_rehearsal_spends_from_the_live_gate[True]`
  - `tests/test_provider_budget.py::test_the_pointer_names_where_the_gate_lives`

Old text:

```
        if key in _PROVIDER_GATE_KEYS:
            return provider_gate_dir() / entry.relative

```

New text:

```
(empty)
```

### `u278.M3_pointer_reads_state_dir`

provider_gate_dir: fall back to installation_state_dir, which honours CRATEKIT_STATE_DIR

- File: `src/cratekit/core/state_files.py`
- Source: `u278.json`, row `M3_pointer_reads_state_dir`
- Moved: the same text, now in src/cratekit/core/state_files.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_config.py`
- Collected: 433 against a baseline of 433
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_made_under_a_redirected_state_directory_is_counted_by_the_live_gate`
  - `tests/test_provider_budget.py::test_a_redirected_state_directory_still_resolves_the_one_gate`
  - `tests/test_provider_budget.py::test_a_rehearsal_spends_from_the_live_gate[False]`

Old text:

```
        return Path(override)
    return Path(platformdirs.user_state_dir(_APP_NAME))


#: The state entries resolved
```

New text:

```
        return Path(override)
    return installation_state_dir()


#: The state entries resolved
```

### `u299.U1_installation_never_restored`

_installation: an installation entry is captured with the library, coupled to a restore

- File: `src/cratekit/core/state_files.py`
- Source: `u299.json`, row `U1_installation_never_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_snapshot.py`, `tests/test_restore.py`
- Collected: 431 against a baseline of 431
- Kills: 72 (killed)
- Killed:
  - `tests/test_config.py::test_the_coupled_set_is_a_directory_boundary_rather_than_a_list`
  - `tests/test_config.py::test_the_locks_and_the_snapshot_store_are_not_in_the_coupled_set`
  - `tests/test_config.py::test_the_presence_index_lock_lives_beside_the_file_it_guards`
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
  - ... and 57 more, see the JSON sidecar

Old text:

```
        snapshot=SnapshotRole.NEVER_RESTORED,
        installation_area=area,
```

New text:

```
        snapshot=SnapshotRole.COUPLED,
        installation_area=area,
```

### `u299.U5_library_snapshot_passed`

_library: the snapshot role an entry names is replaced by COUPLED for every library entry

- File: `src/cratekit/core/state_files.py`
- Source: `u299.json`, row `U5_library_snapshot_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_snapshot.py`, `tests/test_restore.py`
- Collected: 431 against a baseline of 431
- Kills: 111 (killed)
- Killed:
  - `tests/test_config.py::test_each_named_entry_carries_its_declared_snapshot_role[energy_undo_log-never-restored]`
  - `tests/test_config.py::test_each_named_entry_carries_its_declared_snapshot_role[genre_tag_undo_log-never-restored]`
  - `tests/test_config.py::test_each_named_entry_carries_its_declared_snapshot_role[session_log-survives-rollback]`
  - `tests/test_config.py::test_each_named_entry_carries_its_declared_snapshot_role[snapshots-survives-rollback]`
  - `tests/test_config.py::test_the_locks_and_the_snapshot_store_are_not_in_the_coupled_set`
  - `tests/test_config.py::test_the_snapshot_store_does_not_nest_inside_what_it_snapshots`
  - `tests/test_restore.py::test_a_capture_that_failed_its_integrity_check_is_never_restored_from`
  - `tests/test_restore.py::test_a_capture_whose_manifest_names_a_path_outside_the_set_is_refused`
  - `tests/test_restore.py::test_a_completed_session_is_listed_with_its_timestamp_workflow_and_changes`
  - `tests/test_restore.py::test_a_coupled_file_the_capture_records_as_absent_is_removed_again`
  - `tests/test_restore.py::test_a_dry_run_and_a_real_run_walk_the_same_list_in_the_same_order`
  - `tests/test_restore.py::test_a_held_session_used_after_its_block_is_refused`
  - `tests/test_restore.py::test_a_later_session_that_committed_nothing_does_not_need_an_override`
  - `tests/test_restore.py::test_a_plan_built_before_a_later_commit_is_refused_at_run`
  - `tests/test_restore.py::test_a_pre_cutover_restore_leaves_the_next_session_refused`
  - ... and 96 more, see the JSON sidecar

Old text:

```
        why=why,
        snapshot=snapshot,
```

New text:

```
        why=why,
        snapshot=SnapshotRole.COUPLED,
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

### `u250.M5_word_reads_zero`

whole_number: read a stored value that is not a number as 0 rather than None, so a word files in the lowest band

- File: `src/cratekit/core/tags.py`
- Source: `u250.json`, row `M5_word_reads_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_tags.py`, `tests/test_rebuild.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_numeric_reading_converts_the_way_the_single_readers_convert`

Old text:

```
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
        return None
```

New text:

```
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
        return 0
```

### `u250.M6_absent_raises`

whole_number: drop the absent check, so an untagged file raises out of read_truth and abandons the derivation

- File: `src/cratekit/core/tags.py`
- Source: `u250.json`, row `M6_absent_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_tags.py`, `tests/test_rebuild.py`
- Collected: 215 against a baseline of 215
- Kills: 20 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_derivation_over_n_files_makes_n_opens`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[empty.flac-]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.aiff-FORM\x00\x00\x00\x04AIFX]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.m4a-\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.mp3-content1]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[truncated.wav-RIFF$\x00\x00\x00WAVEfmt ]`
  - `tests/test_rebuild_one_open.py::test_an_undecodable_field_reads_none_and_its_neighbours_still_read`
  - `tests/test_rebuild_one_open.py::test_an_unsupported_suffix_reads_absent_and_opens_nothing`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.flac]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.m4a]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.mp3]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.ogg]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.wav]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[untagged-.aiff]`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    if value is None:
        return None
    try:
        return int(value)
```

New text:

```
    try:
        return int(value)
```

### `u250.M8_conversion_learns_decimals`

whole_number: read a decimal as its whole part, so 7.0 files at energy 7 where today it reads None

- File: `src/cratekit/core/tags.py`
- Source: `u250.json`, row `M8_conversion_learns_decimals`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_tags.py`, `tests/test_rebuild.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_numeric_reading_converts_the_way_the_single_readers_convert`

Old text:

```
    try:
        return int(value)
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
```

New text:

```
    try:
        return int(float(value))
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
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
  - `tests/test_tag_remap.py::test_a_file_already_carrying_the_genre_wanted_agrees`
  - `tests/test_tag_remap.py::test_a_file_tagged_by_the_old_mapping_from_the_catalogues_pop_is_planned`
  - `tests/test_tag_remap.py::test_a_file_that_moved_since_the_plan_is_named_and_not_written`
  - `tests/test_tag_remap.py::test_a_file_the_writer_could_not_write_is_named_as_untouched_and_the_rest_are_written`
  - `tests/test_tag_remap.py::test_a_file_this_verb_rewrote_is_corrected_again_when_the_word_moves_again`
  - `tests/test_tag_remap.py::test_a_file_written_that_does_not_read_back_is_named_as_wrong`
  - `tests/test_tag_remap.py::test_a_genre_nobody_recorded_writing_is_left_alone_and_listed[Deep House]`
  - `tests/test_tag_remap.py::test_a_genre_nobody_recorded_writing_is_left_alone_and_listed[Pop]`
  - `tests/test_tag_remap.py::test_a_genre_nobody_recorded_writing_is_left_alone_and_listed[dance / pop]`
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_person_reads_the_counts_and_the_pairs_at_the_gate`
  - `tests/test_tag_remap.py::test_a_record_is_read_whether_or_not_the_queue_still_lists_its_job`
  - `tests/test_tag_remap.py::test_a_record_that_cannot_be_committed_is_named_and_the_file_stays_rewritten`
  - ... and 33 more, see the JSON sidecar

Old text:

```
            table.source: {row.word.lower(): row for row in table.words}
```

New text:

```
            table.source: {row.word: row for row in table.words}
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

### `r239-b.S6_delete_key_off`

delete review's open passes unlock=False

- File: `src/cratekit/deletion/cli.py`
- Source: `r239-b.json`, row `S6_delete_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 724 against a baseline of 724
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
    return rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
```

New text:

```
    return rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg, unlock=False)
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

### `r227.C4_export_limit_spelled`

export playlist judges against a seven spelled in the shell, not the configured limit

- File: `src/cratekit/export/cli.py`
- Source: `r227.json`, row `C4_export_limit_spelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[export.playlist]`

Old text:

```
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)
```

New text:

```
    age = source.export_age(exported, limit_days=7)
```

### `r229.C1_the_offer_is_not_digested`

The adoption never joins the confirm digest, so a confirmed update authorises a queue that creates

- File: `src/cratekit/export/cli.py`
- Source: `r229.json`, row `C1_the_offer_is_not_digested`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_export_that_adopts_nothing_digests_as_it_always_did`

Old text:

```
    if adopts:
        covered["adopts"] = adopts
```

New text:

```
    if False:
        covered["adopts"] = adopts
```

### `r229.C2_the_flag_declines_nothing`

The new playlist flag is read and ignored, so a wrong offer cannot be declined

- File: `src/cratekit/export/cli.py`
- Source: `r229.json`, row `C2_the_flag_declines_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_confirmed_adoption_does_not_authorise_a_create`
  - `tests/test_outbound_workers.py::test_new_playlist_declines_the_adoption_and_creates`
  - `tests/test_outbound_workers.py::test_two_orphaned_records_that_could_each_be_it_adopt_neither`

Old text:

```
        found = found.without_offer()
```

New text:

```
        pass
```

### `r229.C3_no_remote_id_is_frozen`

The job freezes no remote id, so nothing can follow a record that moves after the job is confirmed

- File: `src/cratekit/export/cli.py`
- Source: `r229.json`, row `C3_no_remote_id_is_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing`

Old text:

```
                REMOTE: found.own_remote_id or found.remote_id or None,
```

New text:

```
                REMOTE: None,
```

### `r356-b.B9_export_item_report_drops_the_reason`

The export item report writes no reason, so neither the artifact nor the envelope can say it

- File: `src/cratekit/export/cli.py`
- Source: `r356-b.json`, row `B9_export_item_report_drops_the_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`

Old text:

```
                "reason": row.reason,

```

New text:

```
(empty)
```

### `r850-a.E1_written_count`

export.summary: count written as the already list's length, so the answer's written count is the wrong list

- File: `src/cratekit/export/cli.py`
- Source: `r850-a.json`, row `E1_written_count`
- Moved: export.summary's counts were folded from a multi line dict onto one line in the same function; the same written count is taken from the already list
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 236 against a baseline of 236
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_workers.py::test_a_resumed_export_counts_across_both_runs_and_each_item_once`
  - `tests/test_outbound_workers.py::test_a_second_export_counts_what_the_playlist_already_held`
  - `tests/test_outbound_workers.py::test_an_export_where_every_track_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers`

Old text:

```
        "counts": {"written": len(added), "already": len(already), "unmatched": len(unmatched)},

```

New text:

```
        "counts": {"written": len(already), "already": len(already), "unmatched": len(unmatched)},

```

### `r850-a.E2_unmatched_count`

export.summary: count unmatched as the reason sentences, so a row the account said nothing about is not counted

- File: `src/cratekit/export/cli.py`
- Source: `r850-a.json`, row `E2_unmatched_count`
- Moved: export.summary's counts were folded from a multi line dict onto one line in the same function, where the old line had a twin in favorites/cli.py; the same unmatched count is taken from the reasons
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_resumed_export_counts_across_both_runs_and_each_item_once`
  - `tests/test_outbound_workers.py::test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers`

Old text:

```
        "counts": {"written": len(added), "already": len(already), "unmatched": len(unmatched)},

```

New text:

```
        "counts": {"written": len(added), "already": len(already), "unmatched": len(reasons)},

```

### `r850-a.E3_listing_dropped`

export.summary: build each unmatched row but never list it, so the answer counts a track it does not name

- File: `src/cratekit/export/cli.py`
- Source: `r850-a.json`, row `E3_listing_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 6 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope`
  - `tests/test_outbound_workers.py::test_a_resumed_export_counts_across_both_runs_and_each_item_once`
  - `tests/test_outbound_workers.py::test_an_export_the_provider_matches_nothing_of_says_so_in_the_envelope`
  - `tests/test_outbound_workers.py::test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_the_envelope_names_the_tracks_the_provider_could_not_match`

Old text:

```
            left_out.append(listed)
```

New text:

```
            pass
```

### `r850-a.E4_reason_gate`

export.summary: write a reason sentence for every unmatched row, so reasons carries rows the account said nothing about

- File: `src/cratekit/export/cli.py`
- Source: `r850-a.json`, row `E4_reason_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope`

Old text:

```
            if _said(item):
```

New text:

```
            if True:
```

### `r850-a.E5_slug_is_no_reason`

export._said: take the engine's slug unmatched as something the account said, so it is shown instead of the sentence

- File: `src/cratekit/export/cli.py`
- Source: `r850-a.json`, row `E5_slug_is_no_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope`
  - `tests/test_outbound_workers.py::test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers`

Old text:

```
    return "" if said == "unmatched" else said
```

New text:

```
    return said
```

### `r850-a.E6_no_match_sentence`

export._left_out: leave the reason empty when the account said nothing, so the row is listed with no reason

- File: `src/cratekit/export/cli.py`
- Source: `r850-a.json`, row `E6_no_match_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope`
  - `tests/test_outbound_workers.py::test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers`

Old text:

```
        "reason": _said(row) or NO_MATCH,
```

New text:

```
        "reason": _said(row),
```

### `u131.K11_filing_in_digest`

confirm_digest: leave the Exports filing out of the digest, so a changed folder does not make the answer stale

- File: `src/cratekit/export/cli.py`
- Source: `u131.json`, row `K11_filing_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_playlist_kinds.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_changed_exports_folder_makes_the_old_answer_stale`

Old text:

```
    if filing:
        covered["filing"] = filing
```

New text:

```
    if False:
        covered["filing"] = filing
```

### `u131.K13_unfiled_warning`

export concluded: drop the unfiled warning, so a playlist left at the root is never said

- File: `src/cratekit/export/cli.py`
- Source: `u131.json`, row `K13_unfiled_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - `tests/test_outbound_workers.py::test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning`

Old text:

```
        for reason in outbound.get("unfiled") or ()
```

New text:

```
        for reason in ()
```

### `u270.C1_export_names_its_batch_form`

export cli: the per item worker names no batch form

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C1_export_names_its_batch_form`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 290 against a baseline of 290
- Kills: 7 (killed)
- Killed:
  - `tests/test_handlers.py::test_the_export_worker_names_its_batch_form_at_the_providers_add_limit`
  - `tests/test_outbound_export_batches.py::test_a_job_of_two_hundred_and_fifty_tracks_makes_fifteen_requests`
  - `tests/test_outbound_export_batches.py::test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice`
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_through_the_driver_finishes_the_job`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_export_runs_to_done_and_the_ledger_records_every_add`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_refused_request_fails_every_item_it_carried_and_the_resume_adds_each_once`

Old text:

```
handle.batched = (handle_batch, BATCH)  # type: ignore[attr-defined]
```

New text:

```
handle.unbatched = (handle_batch, BATCH)  # type: ignore[attr-defined]
```

### `u270.C2_stop_while_planning`

run_export_items: never ask stop while a batch is planned, so a signal still sends the batch's add

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C2_stop_while_planning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_a_stop_asked_while_a_batch_is_planned_writes_none_of_it`

Old text:

```
        if stop():
            return None
```

New text:

```
        if False:
            return None
```

### `u270.C3_refused_track_fails_its_item`

run_export_items: report a track the provider would not add as an item done with nothing added

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C3_refused_track_fails_its_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_track_the_provider_would_not_add_fails_its_item_alone_and_is_never_recorded`

Old text:

```
        if refused:
            answered[track_id] = _refused(refused[0], report.remote_id)
            continue
```

New text:

```
        if False:
            answered[track_id] = _refused(refused[0], report.remote_id)
            continue
```

### `u270.C4_created_said_once`

run_export_items: every item of the batch that created the playlist reports the create

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C4_created_said_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_a_created_playlist_is_said_once_for_the_batch`
  - `tests/test_outbound_workers.py::test_an_export_runs_pending_to_done_and_its_artifact_reads_back`

Old text:

```
            "created": report.created and first_said,
```

New text:

```
            "created": report.created,
```

### `u270.C5_unfiled_said_once`

run_export_items: every item of the batch carries the filing warning, one per track in the summary

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C5_unfiled_said_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`, `tests/test_playlist_kinds.py`
- Collected: 159 against a baseline of 159
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - `tests/test_outbound_workers.py::test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning`

Old text:

```
            "unfiled": report.unfiled if first_said else "",
```

New text:

```
            "unfiled": report.unfiled,
```

### `u270.C6_one_tracks_failure_is_its_own`

run_export_items: a plain exception planning one track fails the whole batch

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C6_one_tracks_failure_is_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_resume_of_a_half_failed_export_does_not_exit_ok`

Old text:

```
        except Exception as exc:  # noqa: BLE001 - this track's outcome
```

New text:

```
        except CratekitError as exc:  # noqa: BLE001 - this track's outcome
```

### `u51-item-derivation.H1_export_item_not_payload`

The export handler reads the playlist key as its track, not the claimed item

- File: `src/cratekit/export/cli.py`
- Source: `u51-item-derivation.json`, row `H1_export_item_not_payload`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    report = run_export_item(payload, str(item.item_id), cfg, account.resolve(cfg))
```

New text:

```
    report = run_export_item(payload, str(payload[PLAYLIST]), cfg, account.resolve(cfg))
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

### `r836-g.C3_dangling_rows_are_rows`

export.prune_cli: a row the export names and does not carry is read as gone, so its track is taken off

- File: `src/cratekit/export/prune_cli.py`
- Source: `r836-g.json`, row `C3_dangling_rows_are_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_row_the_export_names_and_does_not_carry_keeps_its_track`

Old text:

```
        (*resolved.track_ids, *resolved.dangling),
```

New text:

```
        resolved.track_ids,
```

### `u142.S12_undeclared_reads_as_empty`

inspiration_names: answer an empty set when no INSPIRATION folder is declared, so the wait says no playlist rather than no folder

- File: `src/cratekit/export/set_cli.py`
- Source: `u142.json`, row `S12_undeclared_reads_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_taxonomy_with_no_inspiration_folder_waits_and_says_why`

Old text:

```
    if declared.inspiration is None:
        return None
    return frozenset(
```

New text:

```
    if declared.inspiration is None:
        return frozenset()
    return frozenset(
```

### `u267.M12_inspiration_set_folder_write_guard`

set_cli._inspiration_folder: drop the refusal of a shared read handed to an opener asked to write

- File: `src/cratekit/export/set_common.py`
- Source: `u267.json`, row `M12_inspiration_set_folder_write_guard`
- Moved: the same text, now in src/cratekit/export/set_common.py, was in src/cratekit/export/set_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_the_inspiration_opener_refuses_to_write_through_a_shared_read`

Old text:

```
    if one_read is not None and not read_only:
```

New text:

```
    if False:
```

### `r227.C5_favorites_limit_spelled`

sync favorites judges against a seven spelled in the shell

- File: `src/cratekit/favorites/cli.py`
- Source: `r227.json`, row `C5_favorites_limit_spelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_sync_all.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[sync.favorites]`

Old text:

```
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)
```

New text:

```
    age = source.export_age(exported, limit_days=7)
```

### `r424.B1_colored_key`

Restore the always empty colored key on each item report

- File: `src/cratekit/favorites/cli.py`
- Source: `r424.json`, row `B1_colored_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_sync_all.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_item_report_carries_no_empty_colored_list`

Old text:

```
        "already": list(report.already),
        "unmatched": list(report.unmatched),
```

New text:

```
        "already": list(report.already),
        "colored": list(report.colored),
        "unmatched": list(report.unmatched),
```

### `r424.B3_resume_standing`

Stop passing the standing warning into the resume branch

- File: `src/cratekit/favorites/cli.py`
- Source: `r424.json`, row `B3_resume_standing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_sync_all.py`
- Collected: 239 against a baseline of 239
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_the_resumed_sweep_says_the_same_thing_where_the_hearting_actually_happens`

Old text:

```
            standing=local_write_warning(),
```

New text:

```
(empty)
```

### `r424.B4_warning_copied`

Hand callers the module level dict instead of a copy per call

- File: `src/cratekit/favorites/cli.py`
- Source: `r424.json`, row `B4_warning_copied`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return (dict(LOCAL_WRITE_WARNING),)
```

New text:

```
    return (LOCAL_WRITE_WARNING,)
```

### `r856-a.F10_concluded_passed`

favorites.sync_favorites: pass no concluded hook to the resume, so a sweep with unmatched favourites carries no warning

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F10_concluded_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
            concluded=concluded,
```

New text:

```
            concluded=None,
```

### `r856-a.F11_warning_total`

favorites.concluded: state the unmatched count as the total, so the warning says 1 of the 1

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F11_warning_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_the_sweep_warning_counts_only_whole_numbers`

Old text:

```
                f"{missed} of the {total} favourite(s) in this sweep were not "
```

New text:

```
                f"{missed} of the {missed} favourite(s) in this sweep were not "
```

### `r856-a.F1_hearted_count`

favorites.summary: count hearted as the already list's length, so the answer's hearted count is the wrong list

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F1_hearted_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
            "hearted": len(hearted),
```

New text:

```
            "hearted": len(already),
```

### `r856-a.F2_already_count`

favorites.summary: count already hearted as zero, so a favourite hearted before is counted nowhere

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F2_already_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`

Old text:

```
            "already_hearted": len(already),
```

New text:

```
            "already_hearted": 0,
```

### `r856-a.F3_unmatched_count`

favorites.summary: count unmatched as the reason sentences, so a favourite the account said nothing about is not counted

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F3_unmatched_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
            "unmatched": len(unmatched),
```

New text:

```
            "unmatched": len(reasons),
```

### `r856-a.F4_listing_dropped`

favorites.summary: build each item's unmatched rows but never list them, so the answer counts a favourite it does not name

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F4_listing_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
        left_out.extend(_left_out(report, said))
```

New text:

```
        pass
```

### `r856-a.F5_listing_off_reasons`

favorites._left_out: list the rows reasons names instead of every unmatched row, so a favourite with no reason is left out

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F5_listing_off_reasons`
- Moved: The loop over the report's unmatched list now takes each identity as text directly; the same source, swapped for the rows the reasons name the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_report_written_before_the_listing_still_names_its_unmatched_rows`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
    for identity in map(str, report.get("unmatched") or ()):
```

New text:

```
    for identity in map(str, [one.get("row") for one in said]):
```

### `r856-a.F6_no_match_sentence`

favorites._left_out: leave the reason empty when the account gave none, so the line reads no reason given

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F6_no_match_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_report_written_before_the_listing_still_names_its_unmatched_rows`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
                "reason": str(one.get("reason") or "") or NO_MATCH,
```

New text:

```
                "reason": str(one.get("reason") or ""),
```

### `r856-a.F7_names_from_listing`

favorites._left_out: read names off reasons alone, so a new report's unmatched row with no reason has no artist or title

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F7_names_from_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
    for one in (*said, *(report.get("unmatched_tracks") or ())):
```

New text:

```
    for one in said:
```

### `r856-a.F8_item_listing`

favorites.run_heart_item: commit no unmatched_tracks, so an artifact names no unmatched row the account said nothing about

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F8_item_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
        "unmatched_tracks": [row_named(row, said.get(row, "")) for row in report.unmatched],
```

New text:

```
        "unmatched_tracks": [],
```

### `r856-a.F9_item_reason_carried`

favorites.run_heart_item: list every unmatched row with an empty reason, so the account's reason is lost from the listing

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F9_item_reason_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`

Old text:

```
        "unmatched_tracks": [row_named(row, said.get(row, "")) for row in report.unmatched],
```

New text:

```
        "unmatched_tracks": [row_named(row, "") for row in report.unmatched],
```

### `u51-item-derivation.A1b_colour_writer_passed`

Pass a REAL colour writer, which A1 could not: colors=None is the engine's own default, so removing the keyword changed nothing

- File: `src/cratekit/favorites/cli.py`
- Source: `u51-item-derivation.json`, row `A1b_colour_writer_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_no_colour_writer_reaches_the_engine_from_a_queued_sweep`

Old text:

```
    report = hearts.heart_back(cfg, remote, candidates, colors=None)
```

New text:

```
    class _Pink:
        def color_pink(self, row_id):
            return None

        def is_pink(self, row_id):
            return False

    report = hearts.heart_back(cfg, remote, candidates, colors=_Pink())
```

### `u51-item-derivation.H2_hearts_item_not_payload`

The sweep handler reads the playlist key as its row, not the claimed item

- File: `src/cratekit/favorites/cli.py`
- Source: `u51-item-derivation.json`, row `H2_hearts_item_not_payload`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 14 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_favourites_sweep_runs_to_done_and_hearts_every_matched_row`
  - `tests/test_outbound_workers.py::test_a_provider_that_already_hearts_a_row_is_reported_rather_than_written`
  - `tests/test_outbound_workers.py::test_a_second_sweep_writes_nothing_because_the_ledger_remembers`
  - `tests/test_outbound_workers.py::test_a_sweep_runs_with_rekordbox_open_and_never_opens_the_database`
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_an_item_report_carries_no_empty_colored_list`
  - `tests/test_outbound_workers.py::test_an_unmatched_favourite_is_reported_and_does_not_fail_its_item`
  - `tests/test_outbound_workers.py::test_no_colour_writer_reaches_the_engine_from_a_queued_sweep`
  - `tests/test_outbound_workers.py::test_the_handler_runs_against_the_frozen_configuration_not_the_current_one[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_resumed_sweep_says_the_same_thing_where_the_hearting_actually_happens`
  - `tests/test_outbound_workers.py::test_the_sweep_reaches_nothing_outside_the_add_only_protocol`

Old text:

```
    report = run_heart_item(payload, str(item.item_id), cfg, account.resolve(cfg))
```

New text:

```
    report = run_heart_item(payload, str(payload[PLAYLIST]), cfg, account.resolve(cfg))
```

### `u173.M21_gate_name`

analyzed_cli: the clear's gate renamed, so the skill's decide line names a gate that does not exist

- File: `src/cratekit/intake/analyzed_cli.py`
- Source: `u173.json`, row `M21_gate_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_each_gate_is_answered_by_its_own_name_and_option_the_adopt_before_the_clear`

Old text:

```
APPROVE_GATE = "inbox.analyzed.approve"
```

New text:

```
APPROVE_GATE = "inbox.analyzed.confirm"
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

### `r504-b.B1_verb_drops_short`

intake playlist favorites lists the hearts and throws the shortfall away

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B1_verb_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`

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
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`

Old text:

```
        extra = {"shortfall": short.block()} if short is not None else {}
```

New text:

```
        extra = {}
```

### `r504-b.B6_warning_reworded`

The warning names no numbers

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B6_warning_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`

Old text:

```
            f"the account's hearts listed short: {short.summary()}. The provider "
```

New text:

```
            f"the account's hearts listed short. The provider "
```

### `r679-b.D1_intake_gate_on_question_alone`

intake worker: gate the store on the needs-review state alone, the code before the fix round

- File: `src/cratekit/intake/cli.py`
- Source: `r679-b.json`, row `D1_intake_gate_on_question_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 834 against a baseline of 834
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_every_caller_of_adjudicate_gates_on_the_rows_that_touch_the_queue`

Old text:

```
    if not match_cli.touches_the_queue(found):
```

New text:

```
    if found.state is not match.MatchState.NEEDS_REVIEW:
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

### `u150.F1_blank_ref_claims`

label_filing._refs: let a manifest row with no id claim a file, so a file another row names records no track

- File: `src/cratekit/intake/label_filing.py`
- Source: `u150.json`, row `F1_blank_ref_claims`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_intake_land_labels_native.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_row_with_no_id_makes_no_claim_on_a_file_another_row_names`
  - `tests/test_organize_mirror_inbox.py::test_the_label_plans_refs_leave_out_a_target_two_rows_name_two_tracks`

Old text:

```
                if not ref:
                    continue
                for target in targets:
```

New text:

```
                for target in targets:
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

### `u188.M5_repeat_kept`

_mapped_back: keep a repeated pair instead of dropping it, so the refusal names the folder pair twice on a drive that never moved

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M5_repeat_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return tuple(
        dict.fromkeys(
            (
                (str(area.staging), str(planned.folder)),
                (str(scratch_target), str(target)),
                stored,
            )
        )
    )
```

New text:

```
    return (
        (str(area.staging), str(planned.folder)),
        (str(scratch_target), str(target)),
        stored,
    )
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

### `r679-b.D5_missing_per_row_gate_on_question_alone`

missing pass, per row grouping: gate on the needs-review state alone while the other call site still names the predicate

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r679-b.json`, row `D5_missing_per_row_gate_on_question_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 834 against a baseline of 834
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

### `u173.M24_analyze_name`

native: the queue playlist renamed, so the skill sends a session to a playlist no landing fills

- File: `src/cratekit/intake/native.py`
- Source: `u173.json`, row `M24_analyze_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_it_selects_the_playlist_every_landing_fills`

Old text:

```
ANALYZE = "Analyze"
```

New text:

```
ANALYZE = "Analysis"
```

### `u175.R1_account_ids_unrecorded`

rotate._named_ids: read no account playlist off a native landing record, so a dated playlist is no batch and is neither rotated nor mirrored

- File: `src/cratekit/intake/rotate.py`
- Source: `u175.json`, row `R1_account_ids_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`
- Collected: 83 against a baseline of 83
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_organize_mirror_inbox.py::test_a_passs_dated_account_playlist_is_mirrored_beside_its_batch_under_its_dated_name`

Old text:

```
    accounts = record.detail.get(native.INBOX_PLAYLISTS_KEY)
    if isinstance(accounts, list):
```

New text:

```
    accounts = None
    if isinstance(accounts, list):
```

### `u267.M11_rotation_opens_its_own`

rotate_cli.planned: ignore the shared read and open its own handle, a second open in the report

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `u267.json`, row `M11_rotation_opens_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_inbox_rotate.py`
- Collected: 44 against a baseline of 44
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
    db = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
```

New text:

```
    one_read = None
    db = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
```

### `u144-c.C8_question_named`

Library rows: name an unanswered question as a track the library lacks

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u144-c.json`, row `C8_question_named`
- Moved: the same answer for a track whose match waits on a person, now one entry of set_playlist.py's _NO_MATCH table, which U307 made of the branches
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
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

### `u307.R18_no_match_drops_unanswered`

set_playlist._NO_MATCH: a match nobody answered reads as no library file matching it

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u307.json`, row `R18_no_match_drops_unanswered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_removed.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_near_match_is_a_question_named_as_a_miss_and_never_written`

Old text:

```
_NO_MATCH = {match.MatchState.NEEDS_REVIEW: UNANSWERED, match.MatchState.SUPPRESSED: TOMBSTONED}
```

New text:

```
_NO_MATCH = {match.MatchState.SUPPRESSED: TOMBSTONED}
```

### `u107-c.S19_approved_superseded`

approved_cli._queued: count a superseded item as not yet answered

- File: `src/cratekit/label/approved_cli.py`
- Source: `u107-c.json`, row `S19_approved_superseded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_superseded_item_is_not_counted_as_waiting_by_label_approved`

Old text:

```
        elif item.verdict is not review.Verdict.SUPERSEDED:
```

New text:

```
        else:
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

### `r515-operator.S1_of_takes_bool`

Let ListingShortfall.of trust a bool as a declared count

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S1_of_takes_bool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_that_is_not_a_usable_count_leaves_nothing_to_compare[True]`

Old text:

```
        if isinstance(declared, bool) or not isinstance(declared, int) or declared <= 0:
```

New text:

```
        if not isinstance(declared, int) or declared <= 0:
```

### `r515-operator.S2_of_takes_non_int`

Let ListingShortfall.of trust a count that is not an integer

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S2_of_takes_non_int`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_that_is_not_a_usable_count_leaves_nothing_to_compare[10]`

Old text:

```
        if isinstance(declared, bool) or not isinstance(declared, int) or declared <= 0:
```

New text:

```
        if isinstance(declared, bool) or declared is None or declared <= 0:
```

### `r515-operator.S4_of_short_at_count`

Mint a shortfall when the listing reaches the count exactly

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S4_of_short_at_count`
- Moved: The early return for no shortfall became the condition of one expression; the mutation mints a shortfall when the listing reaches the count exactly, as listed > declared did.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_full_release_carries_no_shortfall`

Old text:

```
        return cls(declared=declared, listed=listed) if listed < declared else None

```

New text:

```
        return cls(declared=declared, listed=listed) if listed <= declared else None

```

### `r515-operator.S5_of_short_over_count`

Mint a shortfall when the listing runs past the count

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S5_of_short_over_count`
- Moved: The early return for no shortfall became the condition of one expression; the mutation mints a shortfall when the listing runs past the count, as listed == declared did.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_that_serves_more_than_its_declared_count_carries_no_shortfall`

Old text:

```
        return cls(declared=declared, listed=listed) if listed < declared else None

```

New text:

```
        return cls(declared=declared, listed=listed) if listed != declared else None

```

### `r515-operator.S6_cache_drops_short`

The caching release reader stores the rows and year but drops the shortfall

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S6_cache_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_short_release_is_counted_over_its_rows_and_the_question_says_the_shortfall`

Old text:

```
        answer = (tuple(rows), year, short)
```

New text:

```
        answer = (tuple(rows), year, None)
```

### `r840-c.C4_no_name_is_the_empty_string`

artist_name: answer with the text of whatever the artist's name attribute holds, so an object with no name reads None

- File: `src/cratekit/label/catalogue.py`
- Source: `r840-c.json`, row `C4_no_name_is_the_empty_string`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`
- Collected: 354 against a baseline of 354
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_with_no_artist_attribute_names_none`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[None-]`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held2-]`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held3-]`

Old text:

```
    return name if isinstance(name, str) else ""
```

New text:

```
    return str(name)
```

### `u308.L4_translated_swallows_refusal`

catalogue.translated: an adapter's own refusal is translated into the boundary's failure

- File: `src/cratekit/label/catalogue.py`
- Source: `u308.json`, row `L4_translated_swallows_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`, `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_favorites_backfill.py`
- Collected: 467 against a baseline of 467
- Kills: 8 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_refusal_raised_mid_crawl_passes_through_the_listing_boundary_unchanged`
  - `tests/test_favorites_backfill.py::test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_label_workers.py::test_a_cratekit_refusal_from_below_is_not_flattened_into_an_unreadable_playlist`
  - `tests/test_label_workers.py::test_a_refusal_the_artist_lookup_raises_in_kind_keeps_its_own_reason`
  - `tests/test_label_workers.py::test_a_refusal_the_harvest_verifier_raises_in_kind_keeps_its_own_reason`
  - `tests/test_label_workers.py::test_a_refusal_the_sweep_verifier_raises_in_kind_keeps_its_own_reason`

Old text:

```
    except passing:
        raise
    except Exception as exc:
```

New text:

```
    except Exception as exc:
```

### `u62.C2_outage_as_credential`

Refuse an unreachable provider as a credential problem

- File: `src/cratekit/label/catalogue.py`
- Source: `u62.json`, row `C2_outage_as_credential`
- Moved: The outage refusal is raised through the module helper _refused, which adds the same origin; the mutation swaps its reason as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/intake/test_workers.py`
- Collected: 503 against a baseline of 503
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[connection]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[server-error]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[timeout]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[unparseable-page]`

Old text:

```
    except ProviderUnavailable as exc:
        raise _refused(
            "unavailable-transient",

```

New text:

```
    except ProviderUnavailable as exc:
        raise _refused(
            "credential-missing",

```

### `u97-b.B3_label_path_raises_the_other_token`

catalogue.resolve: refuse a missing session with REAUTHENTICATE_PROVIDER, so a person who never had one is told theirs was rejected

- File: `src/cratekit/label/catalogue.py`
- Source: `u97-b.json`, row `B3_label_path_raises_the_other_token`
- Moved: The missing session refusal lost its default scope and its origin to the _refused helper; the remedy line is the same, and the mutation names the reauthenticate token.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1611 against a baseline of 1611
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_the_label_paths_refusal_carries_the_token_that_renders_the_procedure`

Old text:

```
            remedy=Remedy.AUTHENTICATE_PROVIDER,
            detail={"credential": str(secrets.Credential.PROVIDER_SESSION)},

```

New text:

```
            remedy=Remedy.REAUTHENTICATE_PROVIDER,
            detail={"credential": str(secrets.Credential.PROVIDER_SESSION)},

```

### `r259.L1_job_cache_read`

The worker never reuses the job's library view, one walk per label

- File: `src/cratekit/label/cli.py`
- Source: `r259.json`, row `L1_job_cache_read`
- Moved: The job library view is kept by the _kept_for helper the asking shares; the mutation hands it a fresh holder each time, so the held view is never read again, one walk per label.
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 552 against a baseline of 552
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_sweep_of_two_labels_walks_the_library_once`

Old text:

```
    return lambda: _kept_for(_JOB_LIBRARY, key, lambda: match_cli.library_view(cfg))

```

New text:

```
    return lambda: _kept_for({}, key, lambda: match_cli.library_view(cfg))

```

### `r261.W1_worker_refuses`

The worker returns success over a sweep that left something unread

- File: `src/cratekit/label/cli.py`
- Source: `r261.json`, row `W1_worker_refuses`
- Moved: The _refuse_unread helper had one caller and is now inline under the same unread check; the mutation never raises it.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
    if source.unread:
        # A crawl that skipped part of the label
```

New text:

```
    if False:
        # A crawl that skipped part of the label
```

### `r261.W2_remedy`

The refusal tells the person to resume even when only a missing method is unread

- File: `src/cratekit/label/cli.py`
- Source: `r261.json`, row `W2_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
        remedy=Remedy.RESUME_JOB if transient else Remedy.REPORT_DEFECT,
```

New text:

```
        remedy=Remedy.RESUME_JOB,
```

### `r261.W3_retryable`

The refusal is retryable whatever was unread

- File: `src/cratekit/label/cli.py`
- Source: `r261.json`, row `W3_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
        retryable=transient,
```

New text:

```
        retryable=True,
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

### `r515-operator.S14_harvest_no_warning`

A harvest over a short playlist carries no warning

- File: `src/cratekit/label/cli.py`
- Source: `r515-operator.json`, row `S14_harvest_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_harvest_over_a_short_playlist_offers_what_it_read_and_warns`

Old text:

```
        warnings=(harvest_withheld_warning(short, reference),) if short is not None else (),
```

New text:

```
        warnings=(),
```

### `u100-b.C10_added_message`

reword the added detail a person reads

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C10_added_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_person_reading_the_default_output_sees_what_was_added`

Old text:

```
        status, detail = "ok", f"{result.name}: added as {result.label_id}"
```

New text:

```
        status, detail = "ok", f"{result.name}: now followed as {result.label_id}"
```

### `u100-b.C1_name_accepted`

adopt no longer refuses a name argument and silently ignores it

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C1_name_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_adopt_with_a_name_or_a_field_refuses_and_writes_nothing[name]`

Old text:

```
    if ctx.args.name or ctx.args.new_name is not None:
```

New text:

```
    if ctx.args.new_name is not None:
```

### `u100-b.C2_to_accepted`

adopt no longer refuses --to and silently ignores it

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C2_to_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_adopt_with_a_name_or_a_field_refuses_and_writes_nothing[to]`

Old text:

```
    if ctx.args.name or ctx.args.new_name is not None:
```

New text:

```
    if ctx.args.name:
```

### `u100-b.C3_outcome_always_ok`

adopt reports ok when it added nothing

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C3_outcome_always_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_an_accepted_label_is_added_once_and_a_second_run_adds_none`
  - `tests/test_label_registry_adopt.py::test_nothing_accepted_writes_nothing_and_says_what_is_waiting`

Old text:

```
        outcome=Outcome.OK if added else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u100-b.C4_empty_says_nothing`

adopt over a queue with nothing accepted emits no check, so a person reads a blank answer

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C4_empty_says_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_nothing_accepted_writes_nothing_and_says_what_is_waiting`

Old text:

```
    if not checks:
        checks.append(
```

New text:

```
    if False:
        checks.append(
```

### `u100-b.C5_nameless_unreported`

adopt drops the failing check for an accepted item that names no label

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C5_nameless_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_an_accepted_item_naming_no_label_is_reported_not_skipped`

Old text:

```
        for item_id in found.nameless
```

New text:

```
        for item_id in ()
```

### `u100-b.C6_held_name_hidden`

the already held check no longer names the spelling the label is held under

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C6_held_name_hidden`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_carried_over_accented_label_is_not_filed_twice`

Old text:

```
        if result.held_name != result.name:
```

New text:

```
        if False:
```

### `u100-b.C7_refused_reads_as_note`

a name that yields no identifier is shown as a note rather than a failure

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C7_refused_reads_as_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`

Old text:

```
        status = "fail"
        detail = (
```

New text:

```
        status = "info"
        detail = (
```

### `u100-b.C9_dispatch`

the adopt action is never dispatched and falls through to the named actions

- File: `src/cratekit/label/cli.py`
- Source: `u100-b.json`, row `C9_dispatch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`
- Collected: 47 against a baseline of 47
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_carried_over_accented_label_is_not_filed_twice`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[case]`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[padding]`
  - `tests/test_label_registry_adopt.py::test_a_label_release_on_the_same_queue_is_not_adopted`
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`
  - `tests/test_label_registry_adopt.py::test_a_person_reading_the_default_output_sees_what_was_added`
  - `tests/test_label_registry_adopt.py::test_a_rejected_or_open_label_is_not_added`
  - `tests/test_label_registry_adopt.py::test_an_accepted_item_naming_no_label_is_reported_not_skipped`
  - `tests/test_label_registry_adopt.py::test_an_accepted_label_is_added_once_and_a_second_run_adds_none`
  - `tests/test_label_registry_adopt.py::test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry`
  - `tests/test_label_registry_adopt.py::test_nothing_accepted_writes_nothing_and_says_what_is_waiting`
  - `tests/test_label_registry_adopt.py::test_two_spellings_accepted_in_one_run_add_the_label_once`

Old text:

```
    if action == "adopt":
```

New text:

```
    if action == "adopted":
```

### `u100-c.C8_refused_counted_present_after_fix`

the summary lists a refused name as present, telling a script the registry holds it, re-measured after the fix round added its test

- File: `src/cratekit/label/cli.py`
- Source: `u100-c.json`, row `C8_refused_counted_present_after_fix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`

Old text:

```
                    if not result.added and result.refused is None
```

New text:

```
                    if not result.added
```

### `u109-b.B4_resume_dropped`

sync labels refuses even with --job, so a sweep queued before U109 can never run

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B4_resume_dropped`
- Moved: The retired refusal is raised through the module helper _refused, which passes the steps the same way; the mutation drops the resume branch ahead of it as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 47 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_catalogue_that_cannot_be_listed_fails_the_item_and_the_job`
  - `tests/test_label_workers.py::test_a_job_carrying_no_items_refuses_on_resume_and_is_left_open`
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_label_verb_will_not_drive_a_job_queued_for_another_verb`
  - `tests/test_label_workers.py::test_a_label_whose_catalogue_the_library_already_holds_offers_nothing`
  - `tests/test_label_workers.py::test_a_label_whose_crawl_listed_nothing_at_all_still_succeeds`
  - `tests/test_label_workers.py::test_a_label_whose_every_release_is_tombstoned_still_succeeds`
  - `tests/test_label_workers.py::test_a_listing_failure_that_is_not_a_rate_limit_stays_permanent`
  - `tests/test_label_workers.py::test_a_mixed_listing_of_tombstoned_and_unconfirmed_releases_is_a_label_with_nothing_new`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[artist-resolve]`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[listing-probe]`
  - `tests/test_label_workers.py::test_a_rate_limited_listing_fails_its_item_as_retryable_and_the_job_says_resume`
  - `tests/test_label_workers.py::test_a_rate_limited_verification_is_retryable_too`
  - `tests/test_label_workers.py::test_a_refusal_the_artist_lookup_raises_in_kind_keeps_its_own_reason`
  - `tests/test_label_workers.py::test_a_refusal_the_sweep_verifier_raises_in_kind_keeps_its_own_reason`
  - ... and 32 more, see the JSON sidecar

Old text:

```
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    raise _refused(
        "verb-retired",

```

New text:

```
    raise _refused(
        "verb-retired",

```

### `u109-b.B5_refusal_reason`

Refuse with the old empty registry slug instead of verb-retired

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B5_refusal_reason`
- Moved: The retired refusal is raised through the module helper _refused rather than refuse with an origin; the mutation swaps the reason as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`, `tests/test_cli_contract.py`
- Collected: 1102 against a baseline of 1102
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_retired_refusal_reads_nothing_so_a_fresh_install_gets_it_too`

Old text:

```
    raise _refused(
        "verb-retired",

```

New text:

```
    raise _refused(
        "label-registry-empty",

```

### `u109-b.B6_message_drops_verb`

Reword the refusal message so it no longer names crate label sync

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B6_message_drops_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`

Old text:

```
        f"by label with {GUIDED_VERB}, which asks before it downloads anything",
```

New text:

```
        "by label, asking before anything downloads",
```

### `u109-b.B7_step_drops_verb`

Drop the step that names the guided verb from the retired refusal

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B7_step_drops_verb`
- Moved: The steps are now positional arguments of _refused, one indent shallower than the steps tuple they were in; the mutation drops the step that names the guided verb.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`

Old text:

```
        f"take label releases with: {GUIDED_VERB}",
        "a sweep queued before this change still runs with: crate sync labels "

```

New text:

```
        "a sweep queued before this change still runs with: crate sync labels "

```

### `u109-b.B8_itemless_branch`

The itemless refusal tells a sweep job to queue the import again, never naming the guided verb

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B8_itemless_branch`
- Moved: The itemless refusal passes its steps positionally to _refused, so the conditional step sits one indent shallower; the mutation always takes the import branch as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`

Old text:

```
            if job.handler_key == sweep.HANDLER_KEY

```

New text:

```
            if False

```

### `u109-b.B9_queue_again`

The retired verb queues a sweep again: the refusal is replaced by a legacy enqueue over the registry

- File: `src/cratekit/label/cli.py`
- Source: `u109-b.json`, row `B9_queue_again`
- Moved: The retired refusal is raised through the module helper _refused; the mutation inserts the same legacy enqueue over the registry ahead of it.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`, `tests/test_cli_contract.py`
- Collected: 1102 against a baseline of 1102
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_refused_sweep_carries_no_warning_because_nothing_was_queued`
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`

Old text:

```
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    raise _refused(
        "verb-retired",

```

New text:

```
    if ctx.args.job:
        return _resume(ctx, ctx.args.job)
    held = labels.RegistryStore().load()
    if held.labels:
        return _queue(
            ctx,
            payload={"source_id": "labels", "run_id": ctx.run.run_id},
            item_ids=tuple(entry.label_id for entry in held.labels.values()),
        )
    raise _refused(
        "verb-retired",

```

### `u341.G22_empty_registry_step`

genre_group_or_refuse: with no label followed, tell the person to set a genre on a label that does not exist

- File: `src/cratekit/label/cli.py`
- Source: `u341.json`, row `G22_empty_registry_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_genre.py`, `tests/modules/test_labels.py`
- Collected: 410 against a baseline of 410
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_registry_list_with_a_genre_and_no_label_followed_says_to_follow_one`

Old text:

```
        if held.labels
        else (
```

New text:

```
        if True
        else (
```

### `u341.G4_unknown_genre_walks_every_label`

genre_group_or_refuse: a genre no label carries takes every followed label instead of refusing

- File: `src/cratekit/label/cli.py`
- Source: `u341.json`, row `G4_unknown_genre_walks_every_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_genre.py`, `tests/modules/test_labels.py`
- Collected: 410 against a baseline of 410
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_declared_genre_no_label_carries_refuses_as_a_group_of_none`
  - `tests/test_label_sync_genre.py::test_a_genre_asked_of_labels_that_carry_none_says_how_to_set_one`
  - `tests/test_label_sync_genre.py::test_a_genre_the_taxonomy_does_not_declare_refuses_naming_the_carried_genres`
  - `tests/test_label_sync_genre.py::test_a_refusal_whose_taxonomy_cannot_be_read_still_names_the_carried_genres`
  - `tests/test_label_sync_genre.py::test_registry_list_with_a_genre_no_label_carries_refuses`

Old text:

```
    group = held.of_genre(wanted)
```

New text:

```
    group = held.of_genre(wanted) or tuple(held.labels.values())
```

### `u341.G5_genre_shape_unchecked`

genre_group_or_refuse: skip the shape check, so an empty genre refuses as a group of none, not as no genre

- File: `src/cratekit/label/cli.py`
- Source: `u341.json`, row `G5_genre_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_genre.py`, `tests/modules/test_labels.py`
- Collected: 410 against a baseline of 410
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_shapeless_genre_refuses_naming_the_rule[ ]`
  - `tests/test_label_sync_genre.py::test_a_shapeless_genre_refuses_naming_the_rule[!?]`
  - `tests/test_label_sync_genre.py::test_a_shapeless_genre_refuses_naming_the_rule[Deep\x07House]`
  - `tests/test_label_sync_genre.py::test_a_shapeless_genre_refuses_naming_the_rule[aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa]`

Old text:

```
        wanted = labels.check_genre(genre)
    except CratekitError as exc:
```

New text:

```
        wanted = genre
    except CratekitError as exc:
```

### `u341.G6_undeclared_never_said`

_undeclared: never say the taxonomy routes the word only to its fallback

- File: `src/cratekit/label/cli.py`
- Source: `u341.json`, row `G6_undeclared_never_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_genre.py`, `tests/modules/test_labels.py`
- Collected: 410 against a baseline of 410
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_genre_the_taxonomy_does_not_declare_refuses_naming_the_carried_genres`

Old text:

```
    if routing.resolve_bucket(declared, genre).match is not routing.Match.FALLBACK:
```

New text:

```
    if True:
```

### `u341.G7_undeclared_inverted`

_undeclared: say the fallback clause of a genre the taxonomy routes, and not of one it does not

- File: `src/cratekit/label/cli.py`
- Source: `u341.json`, row `G7_undeclared_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_genre.py`, `tests/modules/test_labels.py`
- Collected: 410 against a baseline of 410
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_declared_genre_no_label_carries_refuses_as_a_group_of_none`
  - `tests/test_label_sync_genre.py::test_a_genre_the_taxonomy_does_not_declare_refuses_naming_the_carried_genres`

Old text:

```
    if routing.resolve_bucket(declared, genre).match is not routing.Match.FALLBACK:
```

New text:

```
    if routing.resolve_bucket(declared, genre).match is routing.Match.FALLBACK:
```

### `u341.G8_list_ignores_genre`

registry_cmd list: drop the group branch, so list --genre lists every label

- File: `src/cratekit/label/cli.py`
- Source: `u341.json`, row `G8_list_ignores_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_genre.py`, `tests/modules/test_labels.py`
- Collected: 410 against a baseline of 410
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_registry_list_with_a_genre_and_no_label_followed_says_to_follow_one`
  - `tests/test_label_sync_genre.py::test_registry_list_with_a_genre_lists_that_group_alone`
  - `tests/test_label_sync_genre.py::test_registry_list_with_a_genre_no_label_carries_refuses`

Old text:

```
        if genre is not None:
            return _group(ctx, store.load(), genre)
```

New text:

```
        if False:
            return _group(ctx, store.load(), genre)
```

### `u341.G9_list_refuses_genre`

registry_cmd: keep --genre in the fields list refuses, so list --genre is refused as a field to set

- File: `src/cratekit/label/cli.py`
- Source: `u341.json`, row `G9_list_refuses_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_genre.py`, `tests/modules/test_labels.py`
- Collected: 410 against a baseline of 410
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_registry_list_with_a_genre_and_no_label_followed_says_to_follow_one`
  - `tests/test_label_sync_genre.py::test_registry_list_with_a_genre_lists_that_group_alone`
  - `tests/test_label_sync_genre.py::test_registry_list_with_a_genre_no_label_carries_refuses`

Old text:

```
        (genre,) if action != "list" else ()
```

New text:

```
        (genre,)
```

### `u52-item-derivation.H2_listing_passthrough_gone`

REMOVE THE LAYER ALONE: an adapter's own CratekitError refusal is rewritten as an unreadable playlist

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H2_listing_passthrough_gone`
- Moved: The listing boundary is catalogue.translated, whose passing types (a CratekitError by default) are re-raised unchanged; the mutation passes nothing through at this site alone, so an adapter refusal is rewritten as an unreadable playlist.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_cratekit_refusal_from_below_is_not_flattened_into_an_unreadable_playlist`

Old text:

```
        detail={"playlist": reference, "kind": type(exc).__name__},
    )):
        playlist = found.playlist_for(reference)

```

New text:

```
        detail={"playlist": reference, "kind": type(exc).__name__},
    ), passing=()):
        playlist = found.playlist_for(reference)

```

### `u52-item-derivation.H4_verification_boundary_gone`

THE THIRD PROVIDER CALL: hand from_tracks the bare seam method, so a provider that went away mid playlist becomes internal-error with report-defect

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H4_verification_boundary_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_harvest_that_fails_mid_verification_names_what_it_already_offered`
  - `tests/test_label_workers.py::test_a_provider_that_fails_mid_verification_refuses_rather_than_reporting_a_defect`

Old text:

```
            verify=_label_verifier(found, reference),
```

New text:

```
            verify=found.check_label,
```

### `u52-item-derivation.H6_empty_playlist_reports_ok`

An empty playlist reports OK rather than NO_OP, so nothing found is indistinguishable from something found

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H6_empty_playlist_reports_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_empty_harvest_still_names_that_nothing_was_offered`
  - `tests/test_label_workers.py::test_an_empty_playlist_offers_nothing_and_reports_zero_rather_than_refusing`

Old text:

```
        outcome=Outcome.OK if report.offered else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u52-item-derivation.H7_unresolved_drops_nameless`

Count only the names a catalogue refused, so a playlist whose tracks carry no copyright string at all reports a clean zero unresolved

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H7_unresolved_drops_nameless`
- Moved: The nameless count now comes back on the harvest report, counted by from_tracks as the closure did, and the sum is inline in the envelope; the mutation counts only the refused names.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_track_with_no_copyright_string_is_counted_rather_than_dropped_silently`

Old text:

```
            "unresolved": len(report.dropped) + report.nameless,

```

New text:

```
            "unresolved": len(report.dropped),

```

### `u52-item-derivation.I5_import_queues_no_item`

THE ZERO ITEM RULE at the import end: queue the single label job with no items at all

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `I5_import_queues_no_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_import_queues_exactly_one_item_and_it_is_the_label_id`
  - `tests/test_label_workers.py::test_an_import_runs_its_one_item_to_done_through_the_same_worker`
  - `tests/test_label_workers.py::test_the_import_queues_without_a_warning_now_an_adapter_is_bound`
  - `tests/test_label_workers.py::test_the_unbound_warning_says_the_job_will_fail_at_the_provider_seam`

Old text:

```
        item_ids=(entry.label_id,),
```

New text:

```
        item_ids=(),
```

### `u52-item-derivation.I6_import_item_keyed_on_name`

The import's single item names the label by display name, which the worker then cannot resolve by id

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `I6_import_item_keyed_on_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_import_queues_exactly_one_item_and_it_is_the_label_id`
  - `tests/test_label_workers.py::test_an_import_runs_its_one_item_to_done_through_the_same_worker`

Old text:

```
        item_ids=(entry.label_id,),
```

New text:

```
        item_ids=(entry.name,),
```

### `u52-item-derivation.R1_itemless_job_drives`

Drive a label job with no items, which jobs.drive transitions straight to SUCCEEDED over a registry nothing was read from

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `R1_itemless_job_drives`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_job_carrying_no_items_refuses_on_resume_and_is_left_open`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_label_workers.py::test_the_itemless_refusal_of_an_import_still_says_queue_it_again`

Old text:

```
            _refuse_an_itemless_job(store, job)
```

New text:

```
            pass
```

### `u52-item-derivation.S1_errors_branch_gone`

A sweep that could not offer some of the releases it listed exits 0 and reports the job done

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `S1_errors_branch_gone`
- Moved: The errors refusal is raised through the module helper _refused, which adds the same origin; the mutation never raises it.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_increment_that_could_not_offer_every_release_fails_the_item`

Old text:

```
    if result.errors:
        raise _refused(
            "label-sweep-incomplete",

```

New text:

```
    if False:
        raise _refused(
            "label-sweep-incomplete",

```

### `u52-zero-rows.H5_verifier_passthrough_gone`

REMOVE THE LAYER ALONE: the verification boundary swallows an adapter's own refusal into label-playlist-unreadable

- File: `src/cratekit/label/cli.py`
- Source: `u52-zero-rows.json`, row `H5_verifier_passthrough_gone`
- Moved: The verification boundary is catalogue.translated, whose default passing type is CratekitError; the mutation passes nothing through at this site, so an adapter refusal is swallowed into label-playlist-unreadable as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_refusal_the_harvest_verifier_raises_in_kind_keeps_its_own_reason`

Old text:

```
    )):
            verdict = found.check_label(name)

```

New text:

```
    ), passing=()):
            verdict = found.check_label(name)

```

### `u99-b.B1_parser_limit_floor`

positive_limit: accept zero at the parser, so --track-limit 0 reaches the store

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B1_parser_limit_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_track_limit_below_one_refuses_at_the_parser[0]`

Old text:

```
    if value < 1:
        raise ValueError(f"{text!r} is not a positive track limit")
```

New text:

```
    if value < 0:
        raise ValueError(f"{text!r} is not a positive track limit")
```

### `u99-b.B5_add_drops_seeds`

registry_cmd add: pass no seeds to the store, so --seed on add is accepted and never written

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B5_add_drops_seeds`
- Moved: The add call now takes the shared field mapping, and its seeds are still passed by keyword; the mutation passes no seeds to add.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_a_new_label_creates_no_entry`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[   ]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id: 12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:-4]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`
  - `tests/test_label_registry_verbs.py::test_a_name_seed_that_merely_contains_id_is_stored`
  - `tests/test_label_registry_verbs.py::test_an_add_with_a_limit_and_two_seeds_round_trips_through_list`
  - `tests/test_label_registry_verbs.py::test_list_shows_the_limit_and_the_seeds_to_a_person`
  - `tests/test_label_registry_verbs.py::test_set_changes_one_field_and_keeps_the_rest`

Old text:

```
        label_id = store.add(name, seed_artists=tuple(seeds or ()), **fields)

```

New text:

```
        label_id = store.add(name, seed_artists=(), **fields)

```

### `u99-b.B6_add_drops_limit`

registry_cmd add: pass no track limit to the store, so --track-limit on add is accepted and never written

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B6_add_drops_limit`
- Moved: The track limit reaches add through the shared field mapping; the mutation overrides it with None for the add call alone, so --track-limit on add is never written, as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_an_add_with_a_limit_and_two_seeds_round_trips_through_list`
  - `tests/test_label_registry_verbs.py::test_list_shows_the_limit_and_the_seeds_to_a_person`
  - `tests/test_label_registry_verbs.py::test_set_seeds_replaces_the_list_and_keeps_the_limit`

Old text:

```
        label_id = store.add(name, seed_artists=tuple(seeds or ()), **fields)

```

New text:

```
        label_id = store.add(name, seed_artists=tuple(seeds or ()), **{**fields, "track_limit": None})

```

### `u99-b.B7_set_drops_seeds`

registry_cmd set: pass no seeds to edit, so set --seed reports an edit and writes nothing

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B7_set_drops_seeds`
- Moved: The set call now takes the shared field mapping and passes its seeds by keyword; the mutation passes no seeds to edit.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_set_refuses_and_writes_nothing`
  - `tests/test_label_registry_verbs.py::test_set_seeds_replaces_the_list_and_keeps_the_limit`

Old text:

```
        edited = store.edit(name, seed_artists=seeds, **fields)

```

New text:

```
        edited = store.edit(name, seed_artists=None, **fields)

```

### `u99-b.B8_list_json_empty`

registry_cmd list: report an empty summary.labels, so a reader that is not a person sees no fields

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B8_list_json_empty`
- Moved: The one use of the _labels_json helper is now inline in _answer: a listing reports every held field under labels, and the mutation reports an empty list there as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[   ]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id: 12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:-4]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`
  - `tests/test_label_registry_verbs.py::test_a_name_seed_that_merely_contains_id_is_stored`
  - `tests/test_label_registry_verbs.py::test_an_add_with_a_limit_and_two_seeds_round_trips_through_list`
  - `tests/test_label_registry_verbs.py::test_set_changes_one_field_and_keeps_the_rest`
  - `tests/test_label_registry_verbs.py::test_set_finds_an_accented_name_typed_in_decomposed_form`
  - `tests/test_label_registry_verbs.py::test_set_on_an_unknown_label_refuses_by_name_and_creates_nothing`
  - `tests/test_label_registry_verbs.py::test_set_seeds_replaces_the_list_and_keeps_the_limit`

Old text:

```
        summary["labels"] = [entry.to_json() for entry in held.labels.values()]

```

New text:

```
        summary["labels"] = []

```

### `u99-b.B9_detail_drops_seeds`

_detail: leave the seeds out of the check detail a person reads

- File: `src/cratekit/label/cli.py`
- Source: `u99-b.json`, row `B9_detail_drops_seeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_list_shows_the_limit_and_the_seeds_to_a_person`

Old text:

```
        parts.append("seeds " + " | ".join(entry.seed_artists))
```

New text:

```
        pass
```

### `r888.C1_probe_ignores_held`

crawl.can_list: a held roster is probed for paging methods, finds none, and the sweep refuses a readable label

- File: `src/cratekit/label/crawl.py`
- Source: `r888.json`, row `C1_probe_ignores_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_crawl_that_read_everything_still_succeeds`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`
  - `tests/test_label_tidal_catalogue.py::test_a_various_compilation_the_credited_artists_do_not_list_is_not_offered`
  - `tests/test_label_tidal_catalogue.py::test_discovery_from_a_copyright_matching_compilation_offers_the_credited_artist`
  - `tests/test_label_tidal_catalogue.py::test_the_crawl_probe_asks_a_held_object_what_it_holds`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_crawls_the_label_page_and_every_seed_through_the_listing`

Old text:

```
    if isinstance(artist, listing.HeldReleases):
        return any(artist.held(method) is not None for method in LISTING_METHODS)

```

New text:

```
(empty)
```

### `r888.C2_probe_trusts_held`

crawl.can_list: a held object holding no listing is read as listable, so its empty read passes as a quiet label

- File: `src/cratekit/label/crawl.py`
- Source: `r888.json`, row `C2_probe_trusts_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_the_crawl_probe_asks_a_held_object_what_it_holds`

Old text:

```
        return any(artist.held(method) is not None for method in LISTING_METHODS)
```

New text:

```
        return True
```

### `u191.M21_unsettled_answers_read`

taken_by_goes: read an answer no go has settled (existing guard, newly on this unit's path)

- File: `src/cratekit/label/dated.py`
- Source: `u191.json`, row `M21_unsettled_answers_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`, `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_dated.py::test_an_unsettled_or_not_now_answer_took_nothing`
  - `tests/test_label_playlists_releases.py::test_an_answer_no_go_has_taken_is_not_read`

Old text:

```
        if not isinstance(settled, Mapping):
            continue
```

New text:

```
        if not isinstance(settled, Mapping):
            settled = {"at": "2026-10-31T12:00:00+00:00"}
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

