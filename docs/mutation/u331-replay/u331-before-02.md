# Mutation table: u331-before-02

Measured by `scripts/mutate.py` on 2026-11-23 23:38 UTC, branch `HEAD` at `c0bb16a4`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22808 collected. pytest invocations for this batch: 174.

Full baseline: measured by this driver (the battery's verdict was not read: it was measured on another machine, or before this one last started).

Subset baselines: 53, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 48 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22808 against 22808. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r395.M10_vocals_literal` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 224 | 1 | killed |
| `sitting3.G12_columns_per_track` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 17 | 1 | killed |
| `u171.Z1_round_to_ceil` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 26 | 3 | killed |
| `u171.Z2_round_to_truncate` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 26 | 2 | killed |
| `u171.Z8_silence_is_undecodable` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 26 | 1 | killed |
| `u181.V1_unavailable_ignores_bound_loader` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 522 | 5 | killed |
| `u181.V2_torch_failure_kind` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 451 | 1 | killed |
| `u263.D18_vocal_reason` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 225 | 1 | killed |
| `u58-workers-and-wav.W1_voxlevel_zero` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 173 | 4 | killed |
| `u58-workers-and-wav.W2_decoder_seam_ignored` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 173 | 7 | killed |
| `u58-workers-and-wav.W3_undecodable_scored` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 173 | 2 | killed |
| `u58-workers-and-wav.W4_model_guard` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 173 | 2 | killed |
| `u58-workers-and-wav.W5_terminal_decoded` | `src/cratekit/analysis/vocals.py` | maintainer | 1 file(s) | 173 | 1 | killed |
| `u58-workers-and-wav.W7_undecodable_reason_reworded` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 173 | 1 | killed |
| `u58-zero-row-remeasured.W6_gender_constant` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 173 | 2 | killed |
| `u92-author.G1_guard_deleted` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 224 | 4 | killed |
| `u92-author.G2_cap_is_inclusive` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 224 | 1 | killed |
| `u92-author.G3_cap_coefficient` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 224 | 1 | killed |
| `u92-author.G4_cap_doubled` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 224 | 1 | killed |
| `u92-author.G5_guard_after_the_load` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 224 | 1 | killed |
| `u92-author.G6_stat_failure_is_oversize` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 224 | 8 | killed |
| `u92-author.G7_reason_reworded` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 224 | 1 | killed |
| `u92-author.G8_refused_file_tagged_zero` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 224 | 2 | killed |
| `u92-author.G9_warning_counts_the_wrong_reason` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 224 | 5 | killed |
| `r685-a.L2_an_unmounted_library_falls_back` | `src/cratekit/core/active_taxonomy.py` | user | 4 file(s) | 348 | 2 | killed |
| `r685-a.L3_a_copy_that_does_not_parse_falls_back` | `src/cratekit/core/active_taxonomy.py` | user | 2 file(s) | 128 | 5 | killed |
| `r685-a.L4_an_unreadable_copy_falls_back` | `src/cratekit/core/active_taxonomy.py` | user | 1 file(s) | 18 | 1 | killed |
| `r685-a.L6_a_permission_is_a_defect_to_report` | `src/cratekit/core/active_taxonomy.py` | user | 1 file(s) | 22808 | 0 (promoted) | zero |
| `r685-a.L7_a_parse_failure_names_a_defect` | `src/cratekit/core/active_taxonomy.py` | user | 1 file(s) | 18 | 1 | killed |
| `u247.M7_load_keyed_on_path_size_time` | `src/cratekit/core/active_taxonomy.py` | user | 4 file(s) | 291 | 2 | killed |
| `u247.M9_unmounted_guard_sample` | `src/cratekit/core/active_taxonomy.py` | user | 4 file(s) | 291 | 2 | killed |
| `r1917.V_r926_G1_first` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 12 | killed |
| `r301.F1_section_not_built` | `src/cratekit/core/config.py` | user | 2 file(s) | 319 | 5 | killed |
| `r345.A9_derive_on_load` | `src/cratekit/core/config.py` | user | 3 file(s) | 758 | 9 | killed |
| `r44-a.C4_identity_not_read` | `src/cratekit/core/config.py` | user | 2 file(s) | 583 | 2 | killed |
| `r790-c.C2_config_built` | `src/cratekit/core/config.py` | user | 2 file(s) | 291 | 1 | killed |
| `r926.G10_no_temporary_allowance` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 135 | 17 | killed |
| `r926.G11_mkdir_before_check` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 3 | killed |
| `r926.G12_message_drops_path` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 5 | killed |
| `r926.G2_checks_the_shipped_tool` | `src/cratekit/core/config.py` | user | 4 file(s) | 310 | 2 | killed |
| `r926.G3_document_check_dropped` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 4 | killed |
| `r926.G4_document_gets_temporary` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 4 | killed |
| `r926.G5_atomic_write_unchecked` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 2 | killed |
| `r926.G6_lock_unchecked` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 1 | killed |
| `r926.G7_no_root_allows_all` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 6 | killed |
| `r926.G8_target_unresolved` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 310 | 1 | killed |
| `r926.G9_temporary_unresolved` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 22808 | 0 (promoted) | zero |
| `u107-a.S01_record_not_json` | `src/cratekit/core/config.py` | user | 1 file(s) | 95 | 2 | killed |
| `u206.M25_lock_skipped` | `src/cratekit/core/config.py` | maintainer | 9 file(s) | 1130 | 1 | killed |
| `u254.C1_append_unsynced` | `src/cratekit/core/config.py` | user | 4 file(s) | 963 | 1 | killed |
| `u254.C2_append_one_write` | `src/cratekit/core/config.py` | user | 4 file(s) | 963 | 1 | killed |
| `u254.C3_append_test_root` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 963 | 2 | killed |
| `u254.C4_append_not_append` | `src/cratekit/core/config.py` | user | 4 file(s) | 963 | 54 | killed |
| `u272.C1_no_flush` | `src/cratekit/core/config.py` | user | 7 file(s) | 641 | 14 | killed |
| `u272.C2_full_flush_error_swallowed` | `src/cratekit/core/config.py` | user | 7 file(s) | 641 | 1 | killed |
| `u272.C3_full_flush_then_sync` | `src/cratekit/core/config.py` | maintainer | 7 file(s) | 641 | 1 | killed |
| `u272.C4_full_flush_never_asked` | `src/cratekit/core/config.py` | user | 7 file(s) | 641 | 5 | killed |
| `u272.C5_eio_counts_as_unsupported` | `src/cratekit/core/config.py` | user | 7 file(s) | 641 | 1 | killed |
| `u272.C6_no_plain_sync` | `src/cratekit/core/config.py` | user | 7 file(s) | 641 | 12 | killed |
| `u272.C7_error_names_no_path` | `src/cratekit/core/config.py` | user | 7 file(s) | 641 | 1 | killed |
| `u298.H10_flock_exclusive_hardens` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 352 | 3 | killed |
| `u298.H11_read_json_refuses_garbage` | `src/cratekit/core/config.py` | user | 2 file(s) | 352 | 4 | killed |
| `u298.H12_read_json_map_shape` | `src/cratekit/core/config.py` | user | 2 file(s) | 352 | 4 | killed |
| `u298.H7_held_translates_acquisition` | `src/cratekit/core/config.py` | user | 2 file(s) | 352 | 1 | killed |
| `u298.H8_lock_within_takes_lock` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 352 | 3 | killed |
| `u299.U13_from_dict_applies_overrides` | `src/cratekit/core/config.py` | user | 2 file(s) | 269 | 4 | killed |
| `u329.R1_config_remedy_drifts_from_the_canonical_text` | `src/cratekit/core/config.py` | user | 4 file(s) | 1526 | 8 | killed |
| `u132.P1_collision_hold` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 5 | killed |
| `u132.P3_candidate_loader_hold` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 2 | killed |
| `u132.P4_version_raise` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 18 | killed |
| `u132.P6_cut_equality` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 1 | killed |
| `u132.P7_child_tables` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 30 | killed |
| `u132.P8_present_skip` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 21 | killed |
| `u133-a-rerun.P5_vocabulary_owner` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 1 | killed |
| `u133-a-rerun.P8_held_by_whole_copy` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 2 | killed |
| `u133-a.P10_keyword_note_for_held` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 1 | killed |
| `u133-a.P13_remedy_keyword` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 1 | killed |
| `u133-a.P1_first_place_only` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 2 | killed |
| `u133-a.P2_one_spelling_per_place` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 1 | killed |
| `u133-a.P3_map_row_label` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 1 | killed |
| `u133-a.P4_vocabulary_row_named` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 1 | killed |
| `u133-a.P7_designed_sharing` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 2 | killed |
| `u133-a.P9_keyword_note_gone` | `src/cratekit/core/taxonomy_upgrade.py` | user | 1 file(s) | 51 | 3 | killed |
| `u244.M24_upgrade_keeps_a_held_table` | `src/cratekit/core/taxonomy_upgrade.py` | user | 2 file(s) | 468 | 22 | killed |
| `r1037.N1_landed_not_recorded` | `src/cratekit/intake/native.py` | user | 3 file(s) | 119 | 33 | killed |
| `r1037.N2_joined_not_made` | `src/cratekit/intake/native.py` | user | 3 file(s) | 119 | 5 | killed |
| `r1037.N3_identity_wrong` | `src/cratekit/intake/native.py` | user | 3 file(s) | 119 | 21 | killed |
| `r1037.N4_size_not_read` | `src/cratekit/intake/native.py` | user | 3 file(s) | 119 | 12 | killed |
| `r1037.N5_count_before_commit` | `src/cratekit/intake/native.py` | user | 3 file(s) | 119 | 1 | killed |
| `r1037.N6_before_empty` | `src/cratekit/intake/native.py` | user | 3 file(s) | 119 | 5 | killed |
| `r1844.N13_landing_writes_no_uuid` | `src/cratekit/intake/native.py` | user | 2 file(s) | 86 | 5 | killed |
| `r746-b.N3_folder_path_not_restamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `r746-b.N4_device_not_restamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `r777.N16_pass_not_recorded` | `src/cratekit/intake/native.py` | user | 6 file(s) | 197 | 1 | killed |
| `r923.N1_landing_sets_nothing` | `src/cratekit/intake/native.py` | user | 6 file(s) | 197 | 1 | killed |
| `u113-c.C1_native_batch_always` | `src/cratekit/intake/native.py` | user | 2 file(s) | 60 | 6 | killed |
| `u113-c.C2_native_batch_keeps_claimed` | `src/cratekit/intake/native.py` | user | 2 file(s) | 60 | 7 | killed |
| `u113-c.C3_native_found_by_name` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u113-c.C4_native_record_unnamed` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 3 | killed |
| `u115.F1_landing_keeps_random_id` | `src/cratekit/intake/native.py` | user | 6 file(s) | 197 | 27 | killed |
| `u120.N3_identity_without_hearts` | `src/cratekit/intake/native.py` | user | 1 file(s) | 13 | 1 | killed |
| `u121.S21_landing_skips_set` | `src/cratekit/intake/native.py` | user | 1 file(s) | 56 | 15 | killed |
| `u121.S22_record_unnamed` | `src/cratekit/intake/native.py` | user | 1 file(s) | 56 | 5 | killed |
| `u126.F3_counts_undigested` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 1 | killed |
| `u126.P2_not_shown` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 4 | killed |
| `u126.R1_binding_value_kept` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 37 | killed |
| `u126.R2_fill_if_null` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 37 | killed |
| `u126.R3_check_skipped` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 2 | killed |
| `u126.R5_read_back_file_id` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 37 | killed |
| `u126.S1_file_id_kept` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 38 | killed |
| `u126.S2_defaults_left_null` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 1 | killed |
| `u127-b.N6b_digest_blind_to_vox` | `src/cratekit/intake/native.py` | user | 9 file(s) | 253 | 1 | killed |
| `u127.N10_record_silent` | `src/cratekit/intake/native.py` | user | 9 file(s) | 253 | 1 | killed |
| `u127.N11_missing_unreported` | `src/cratekit/intake/native.py` | user | 9 file(s) | 253 | 1 | killed |
| `u127.N12_unscored_dropped` | `src/cratekit/intake/native.py` | user | 9 file(s) | 253 | 1 | killed |
| `u127.N14_read_back_skipped` | `src/cratekit/intake/native.py` | user | 9 file(s) | 253 | 4 | killed |
| `u127.N7_digest_blind_to_cut` | `src/cratekit/intake/native.py` | user | 9 file(s) | 253 | 1 | killed |
| `u127.N8_tag_never_written` | `src/cratekit/intake/native.py` | user | 9 file(s) | 253 | 6 | killed |
| `u127.N9_tag_every_added` | `src/cratekit/intake/native.py` | user | 9 file(s) | 253 | 50 | killed |
| `u128-b.N1_native_owned_unwritten` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 3 | killed |
| `u128-b.N2_native_record_no_pass` | `src/cratekit/intake/native.py` | user | 7 file(s) | 210 | 2 | killed |
| `u135.A14_set_order_reverses` | `src/cratekit/intake/native.py` | user | 2 file(s) | 65 | 2 | killed |
| `u135.A1_removed_namesake_written_into` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A2_set_order_falls_to_name_order` | `src/cratekit/intake/native.py` | user | 1 file(s) | 9 | 1 | killed |
| `u135.A8_job_key_not_stamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 9 | 4 | killed |
| `u146-c.N2_owned_not_written` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 2 | killed |
| `u146-e.N3_owned_out_of_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 22808 | 0 (promoted) | zero |
| `u150.F2_record_provider` | `src/cratekit/intake/native.py` | user | 2 file(s) | 78 | 1 | killed |
| `u153.N1_restamp_id_text` | `src/cratekit/intake/native.py` | user | 2 file(s) | 25 | 7 | killed |
| `u153.N3_landing_colour_owned` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u156.L18_digest_native` | `src/cratekit/intake/native.py` | user | 2 file(s) | 90 | 3 | killed |
| `u156.L19_write_called` | `src/cratekit/intake/native.py` | user | 2 file(s) | 90 | 17 | killed |
| `u156.L20_recorded` | `src/cratekit/intake/native.py` | user | 2 file(s) | 90 | 3 | killed |
| `u157.N2_digest_rows` | `src/cratekit/intake/native.py` | user | 3 file(s) | 126 | 1 | killed |
| `u157.N3_no_write` | `src/cratekit/intake/native.py` | user | 3 file(s) | 126 | 3 | killed |
| `u157.N4_trust_the_writer` | `src/cratekit/intake/native.py` | user | 3 file(s) | 126 | 1 | killed |
| `u157.N5_no_record` | `src/cratekit/intake/native.py` | user | 3 file(s) | 126 | 1 | killed |
| `u161.P1_path_back_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 3 | killed |
| `u161.P2_parent_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 2 | killed |
| `u161.P3_file_name_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u161.P4_device_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u161.P5_master_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u161.S1_playlist_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u161.S2_columns_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u163.W12_readback_active` | `src/cratekit/intake/native.py` | user | 3 file(s) | 275 | 1 | killed |
| `u163.W13_identified_words` | `src/cratekit/intake/native.py` | user | 3 file(s) | 275 | 1 | killed |
| `u163.W14_album_artist_link` | `src/cratekit/intake/native.py` | user | 3 file(s) | 275 | 2 | killed |
| `u163.W4_year_written` | `src/cratekit/intake/native.py` | user | 3 file(s) | 275 | 1 | killed |
| `u163.W7_unmoved` | `src/cratekit/intake/native.py` | user | 3 file(s) | 275 | 1 | killed |
| `u163.W8_mint_once` | `src/cratekit/intake/native.py` | user | 3 file(s) | 275 | 1 | killed |
| `u163.W9_creations_named` | `src/cratekit/intake/native.py` | user | 3 file(s) | 275 | 23 | killed |
| `u164.R1_record_filed` | `src/cratekit/intake/native.py` | user | 3 file(s) | 75 | 7 | killed |
| `u165.N1_digest` | `src/cratekit/intake/native.py` | user | 4 file(s) | 98 | 1 | killed |
| `u166.A4_no_add` | `src/cratekit/intake/native.py` | user | 7 file(s) | 185 | 14 | killed |
| `u166.A5_present_rows_too` | `src/cratekit/intake/native.py` | user | 7 file(s) | 185 | 1 | killed |
| `u166.A6_always_create` | `src/cratekit/intake/native.py` | user | 7 file(s) | 185 | 2 | killed |
| `u166.A7_record_count` | `src/cratekit/intake/native.py` | user | 7 file(s) | 185 | 5 | killed |
| `u166.A8_digest_key` | `src/cratekit/intake/native.py` | user | 7 file(s) | 185 | 1 | killed |
| `u173.M24_analyze_name` | `src/cratekit/intake/native.py` | user | 1 file(s) | 32 | 1 | killed |
| `u307.R23_batch_order_keeps_claimed` | `src/cratekit/intake/native.py` | user | 3 file(s) | 69 | 7 | killed |
| `r1184.M21_guess_wiring` | `src/cratekit/tagging/guess_cli.py` | user | 3 file(s) | 289 | 1 | killed |
| `u172.B1_library_read_for_nothing` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.B2_unknown_pass_silent` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.B3_pass_ignored` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.B4_outcome_ok_always` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 4 | killed |
| `u172.B5_missing_folder_walked` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 1 | killed |

## Zero rows and what they owe

- `r685-a.L6_a_permission_is_a_defect_to_report` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r926.G9_temporary_unresolved` (maintainer facing): maintainer facing, composite not required
- `u146-e.N3_owned_out_of_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r395.M10_vocals_literal`

Put the old bare pip literal back in the vocals install text

- File: `src/cratekit/analysis/vocals.py`
- Source: `r395.json`, row `M10_vocals_literal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_slim_worker_refuses_at_the_queue_rather_than_reporting_done`

Old text:

```
    return extras.install_command("vocals")
```

New text:

```
    return "pip install 'cratekit[vocals]'"
```

### `sitting3.G12_columns_per_track`

Resolve the columns per track after the decode instead of once at load

- File: `src/cratekit/analysis/vocals.py`
- Source: `sitting3.json`, row `G12_columns_per_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`

Old text:

```
        _VOCAL_COLUMNS = class_indices(model)
        _VOCAL_MODEL = model

```

New text:

```
        _VOCAL_COLUMNS = None
        _VOCAL_MODEL = model

```

### `u171.Z1_round_to_ceil`

vocals.analyse: stamp a trace under half a percent as 1 by rounding the presence up

- File: `src/cratekit/analysis/vocals.py`
- Source: `u171.json`, row `Z1_round_to_ceil`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 26 against a baseline of 26
- Kills: 3 (killed)
- Killed:
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.0008-0]`
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.0049-0]`
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.014-1]`

Old text:

```
    result["voxlevel"] = int(round(score.presence))
```

New text:

```
    result["voxlevel"] = int(-(-score.presence // 1))
```

### `u171.Z2_round_to_truncate`

vocals.analyse: truncate the presence instead of rounding, so 0.6 percent stamps 0

- File: `src/cratekit/analysis/vocals.py`
- Source: `u171.json`, row `Z2_round_to_truncate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_vocal_zeros.py::test_a_sung_lead_shaped_like_a64s_known_vocals_scores_above_the_cut`
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.006-1]`

Old text:

```
    result["voxlevel"] = int(round(score.presence))
```

New text:

```
    result["voxlevel"] = int(score.presence)
```

### `u171.Z8_silence_is_undecodable`

vocal.decode seam in vocals.analyse: a silent decode reported as undecodable rather than heard as 0

- File: `src/cratekit/analysis/vocals.py`
- Source: `u171.json`, row `Z8_silence_is_undecodable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocal_zeros.py::test_silence_is_heard_and_scores_zero_rather_than_no_score`

Old text:

```
    if samples is None:
        return _inactive(result, REASON_AUDIO_UNDECODABLE)
```

New text:

```
    if samples is None or not samples.any():
        return _inactive(result, REASON_AUDIO_UNDECODABLE)
```

### `u181.V1_unavailable_ignores_bound_loader`

vocals.unavailable: ask missing_requirement even with a loader bound, so a bound fake reads as unable

- File: `src/cratekit/analysis/vocals.py`
- Source: `u181.json`, row `V1_unavailable_ignores_bound_loader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`, `tests/test_doctor.py`
- Collected: 522 against a baseline of 522
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_pass_whose_vocal_model_can_score_says_so_and_asks_nothing`
  - `tests/test_sync_land.py::test_the_analyze_step_rescores_after_analyze_run_and_before_the_restamp`
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`
  - `tests/test_sync_land.py::test_the_outbound_hearts_write_stays_behind_its_own_gate`
  - `tests/test_vocals_cli.py::test_the_one_test_takes_a_bound_loader_as_able`

Old text:

```
    return None if loader_bound() else missing_requirement()
```

New text:

```
    return missing_requirement()
```

### `u181.V2_torch_failure_kind`

vocals.requirement: a torch that will not import is named as missing files, so doctor offers no reinstall

- File: `src/cratekit/analysis/vocals.py`
- Source: `u181.json`, row `V2_torch_failure_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_doctor.py`
- Collected: 451 against a baseline of 451
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_probe_names_a_missing_extra_as_the_extra`

Old text:

```
        return (
            MISSING_EXTRA,
            f"the 'vocals' extra is not usable here ({type(exc).__name__}: {exc}); {install()}",
        )
```

New text:

```
        return (
            MISSING_FILES,
            f"the 'vocals' extra is not usable here ({type(exc).__name__}: {exc}); {install()}",
        )
```

### `u263.D18_vocal_reason`

vocals.analyse: let a missing decoder fail the item rather than name it

- File: `src/cratekit/analysis/vocals.py`
- Source: `u263.json`, row `D18_vocal_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`, `tests/test_analysis_workers.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_the_vocal_pass_names_the_missing_decoder`

Old text:

```
    except DecoderMissing:
        return _inactive(result, REASON_NO_DECODER)
```

New text:

```
    except DecoderMissing:
        raise
```

### `u58-workers-and-wav.W1_voxlevel_zero`

The original defect: score every track voxlevel 0 with a model loaded

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W1_voxlevel_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_exactly_at_the_cap_is_still_decoded`
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_run_batch_threads_the_decoder_through_to_the_vocal_pass`

Old text:

```
    result["voxlevel"] = int(round(score.presence))
```

New text:

```
    result["voxlevel"] = 0
```

### `u58-workers-and-wav.W2_decoder_seam_ignored`

Ignore the bound decoder and always use the shipped one

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W2_decoder_seam_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_exactly_at_the_cap_is_still_decoded`
  - `tests/test_analysis_workers.py::test_a_model_whose_inference_raises_is_a_named_absence_with_the_head_intact`
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_a_run_with_the_model_loaded_carries_no_vocal_warning`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_run_batch_threads_the_decoder_through_to_the_vocal_pass`
  - `tests/test_analysis_workers.py::test_the_decoder_receives_the_partials_path`

Old text:

```
    decoder = _DECODER
    if decoder is None:
        from cratekit.analysis.vocal import decode

        decoder = decode
    return decoder(path)
```

New text:

```
    from cratekit.analysis.vocal import decode

    return decode(path)
```

### `u58-workers-and-wav.W3_undecodable_scored`

Drop the guard that reports a failed decode instead of scoring it

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W3_undecodable_scored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero`
  - `tests/test_analysis_workers.py::test_a_size_that_cannot_be_read_is_not_oversize_and_the_decode_path_reports`

Old text:

```
    if samples is None:
        return _inactive(result, REASON_AUDIO_UNDECODABLE)

```

New text:

```
(empty)
```

### `u58-workers-and-wav.W4_model_guard`

Drop the guard for a model that did not load

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W4_model_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_model_that_did_not_load_is_a_named_absence`
  - `tests/test_analysis_workers.py::test_a_run_with_no_model_loaded_warns_on_the_envelope`

Old text:

```
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)

```

New text:

```
(empty)
```

### `u58-workers-and-wav.W5_terminal_decoded`

Decode a track whose head was terminal anyway

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W5_terminal_decoded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_terminal_head_is_not_decoded_at_all`

Old text:

```
    if result.get("terminal") is not None:
        return _inactive(result, REASON_HEAD_TERMINAL)

```

New text:

```
(empty)
```

### `u58-workers-and-wav.W7_undecodable_reason_reworded`

Reword the undecodable reason, do not append

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W7_undecodable_reason_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero`

Old text:

```
REASON_AUDIO_UNDECODABLE = "vocal-audio-undecodable"
```

New text:

```
REASON_AUDIO_UNDECODABLE = "vocal-audio-unreadable"
```

### `u58-zero-row-remeasured.W6_gender_constant`

Report every scored track's gender as U

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-zero-row-remeasured.json`, row `W6_gender_constant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`

Old text:

```
    result["voxgender"] = score.gender
```

New text:

```
    result["voxgender"] = "U"
```

### `u92-author.G1_guard_deleted`

Delete the oversize guard from analyse entirely, which is main's state

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G1_guard_deleted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 224 against a baseline of 224
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`
  - `tests/test_analysis_workers.py::test_an_oversize_file_is_refused_without_loading_the_model`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

New text:

```
(empty)
```

### `u92-author.G2_cap_is_inclusive`

Refuse a file exactly AT the cap, strictly greater becomes greater or equal

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G2_cap_is_inclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_exactly_at_the_cap_is_still_decoded`

Old text:

```
        return Path(path).stat().st_size > VOCAL_MAX_BYTES
```

New text:

```
        return Path(path).stat().st_size >= VOCAL_MAX_BYTES
```

### `u92-author.G3_cap_coefficient`

Megabytes instead of mebibytes, a realistic nearby value off by 4.9 percent

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G3_cap_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_shipped_oversize_cap_is_two_hundred_and_fifty_mebibytes`

Old text:

```
VOCAL_MAX_BYTES = 250 * 1024 * 1024
```

New text:

```
VOCAL_MAX_BYTES = 250 * 1000 * 1000
```

### `u92-author.G4_cap_doubled`

Double the cap to 500 mebibytes, which still refuses something and refuses it late

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G4_cap_doubled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_shipped_oversize_cap_is_two_hundred_and_fifty_mebibytes`

Old text:

```
VOCAL_MAX_BYTES = 250 * 1024 * 1024
```

New text:

```
VOCAL_MAX_BYTES = 500 * 1024 * 1024
```

### `u92-author.G5_guard_after_the_load`

Move the guard behind the model load, the brief's literal reading, which this unit did not take

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G5_guard_after_the_load`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_oversize_file_is_refused_without_loading_the_model`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)
    model = _load()
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)

```

New text:

```
    model = _load()
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

### `u92-author.G6_stat_failure_is_oversize`

A size that cannot be read answers oversize, so a missing file names the wrong remedy

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G6_stat_failure_is_oversize`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 224 against a baseline of 224
- Kills: 8 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis.py::test_analyse_scores_the_singing_columns_not_the_first_three`
  - `tests/test_analysis_workers.py::test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero`
  - `tests/test_analysis_workers.py::test_a_model_that_did_not_load_is_a_named_absence`
  - `tests/test_analysis_workers.py::test_a_model_whose_inference_raises_is_a_named_absence_with_the_head_intact`
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_a_size_that_cannot_be_read_is_not_oversize_and_the_decode_path_reports`
  - `tests/test_analysis_workers.py::test_the_decoder_receives_the_partials_path`

Old text:

```
    except (OSError, TypeError, ValueError):
        return False

```

New text:

```
    except (OSError, TypeError, ValueError):
        return True

```

### `u92-author.G7_reason_reworded`

Reword the reason slug, never append, since the suite asserts with equality and with in

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G7_reason_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`

Old text:

```
REASON_AUDIO_TOO_LARGE = "vocal-audio-too-large"
```

New text:

```
REASON_AUDIO_TOO_LARGE = "vocal-file-oversize"
```

### `u92-author.G8_refused_file_tagged_zero`

Tag the refused file voxlevel 0 the way the source system did, instead of leaving an absence

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G8_refused_file_tagged_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

New text:

```
    if is_oversize(result.get("path")):
        result = _inactive(result, REASON_AUDIO_TOO_LARGE)
        result["voxlevel"] = 0
        result["voxgender"] = "U"
        result["voxgenderconf"] = 0
        return result

```

### `u92-author.G9_warning_counts_the_wrong_reason`

unscored_warning counts size refusals, so an oversize file is reported as a missing model

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G9_warning_counts_the_wrong_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 224 against a baseline of 224
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`
  - `tests/test_analysis_workers.py::test_a_run_with_no_model_loaded_warns_on_the_envelope`
  - `tests/test_analysis_workers.py::test_an_oversize_track_is_never_warned_about_as_a_missing_model`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    count = int(summary.get("by_vocal_reason", {}).get(REASON_MODEL_UNAVAILABLE, 0))
```

New text:

```
    count = int(summary.get("by_vocal_reason", {}).get(REASON_AUDIO_TOO_LARGE, 0))
```

### `r685-a.L2_an_unmounted_library_falls_back`

Drop the library root check, so an absent volume reads as no active copy and routes by the shipped template

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `r685-a.json`, row `L2_an_unmounted_library_falls_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`, `tests/test_routing_workers.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`
- Collected: 348 against a baseline of 348
- Kills: 2 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[library-root-absent]`
  - `tests/test_active_taxonomy.py::test_a_library_unmounted_after_a_good_load_still_refuses`

Old text:

```
        if not cfg.library.root.is_dir():

```

New text:

```
        if False:

```

### `r685-a.L3_a_copy_that_does_not_parse_falls_back`

An active copy that fails validation is replaced by the shipped template instead of refused

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `r685-a.json`, row `L3_a_copy_that_does_not_parse_falls_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`, `tests/test_rebuild.py`
- Collected: 128 against a baseline of 128
- Kills: 5 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_that_breaks_after_a_good_load_refuses`
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[copy-not-a-taxonomy]`
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[copy-not-toml]`
  - `tests/test_active_taxonomy.py::test_a_copy_that_does_not_parse_refuses_on_every_load`
  - `tests/test_rebuild.py::test_an_active_taxonomy_that_cannot_be_read_is_not_compared_and_opens_nothing`

Old text:

```
    try:
        return taxonomy.load_taxonomy(text)
    except taxonomy.TaxonomyError as exc:
        raise refuse(

```

New text:

```
    try:
        return taxonomy.load_taxonomy(text)
    except taxonomy.TaxonomyError as exc:
        return _shipped(cfg.taxonomy.template)
        raise refuse(

```

### `r685-a.L4_an_unreadable_copy_falls_back`

An active copy that cannot be read is replaced by the shipped template instead of refused

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `r685-a.json`, row `L4_an_unreadable_copy_falls_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[copy-not-text]`

Old text:

```
    except (OSError, UnicodeDecodeError) as exc:
        raise refuse(

```

New text:

```
    except (OSError, UnicodeDecodeError) as exc:
        return _shipped(cfg.taxonomy.template)
        raise refuse(

```

### `r685-a.L6_a_permission_is_a_defect_to_report`

The unreadable branch always says report a defect, never grant access

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `r685-a.json`, row `L6_a_permission_is_a_defect_to_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`
- Collected: 22808 against a baseline of 22808
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),

```

New text:

```
            remedy=Remedy.REPORT_DEFECT,

```

### `r685-a.L7_a_parse_failure_names_a_defect`

The parse refusal's remedy moves from run setup to report a defect, disagreeing with doctor

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `r685-a.json`, row `L7_a_parse_failure_names_a_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[copy-not-toml]`

Old text:

```
            f"the active taxonomy template at {path} is not usable: {exc}",
            remedy=Remedy.RUN_SETUP,

```

New text:

```
            f"the active taxonomy template at {path} is not usable: {exc}",
            remedy=Remedy.REPORT_DEFECT,

```

### `u247.M7_load_keyed_on_path_size_time`

active_taxonomy.load: remember the answer by the copy's path, size and modification time, the identity METHOD's second pattern warns of

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `u247.json`, row `M7_load_keyed_on_path_size_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_active_taxonomy.py`, `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 291 against a baseline of 291
- Kills: 2 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_rewritten_between_two_loads_is_read_and_judged_again`
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`

Old text:

```
    path, text = read_text(cfg)
    if text is None:
        return _shipped(cfg.taxonomy.template)
    try:
        return taxonomy.load_taxonomy(text)
```

New text:

```
    memo = load.__dict__.setdefault("by_file", {})
    where = config.state_path("taxonomy_active", cfg)
    try:
        held = where.stat()
        key = (str(where), held.st_size, held.st_mtime_ns)
    except OSError:
        key = None
    if key is not None and key in memo:
        return memo[key]
    path, text = read_text(cfg)
    if text is None:
        return _shipped(cfg.taxonomy.template)
    try:
        if key is not None:
            memo[key] = taxonomy.load_taxonomy(text)
        return taxonomy.load_taxonomy(text)
```

### `u247.M9_unmounted_guard_sample`

active_taxonomy.read_text: drop the unmounted volume refusal, a sample of the existing guard the memo sits behind

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `u247.json`, row `M9_unmounted_guard_sample`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_active_taxonomy.py`, `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 291 against a baseline of 291
- Kills: 2 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[library-root-absent]`
  - `tests/test_active_taxonomy.py::test_a_library_unmounted_after_a_good_load_still_refuses`

Old text:

```
        if not cfg.library.root.is_dir():
```

New text:

```
        if False:
```

### `r1917.V_r926_G1_first`

The brief's verification, r926.G1_never_checks replayed (first of two in a row on one container): the guard returns at once, so every write the file aims outside lands, and the file must remove it

- File: `src/cratekit/core/config.py`
- Source: `r1917.json`, row `V_r926_G1_first`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 12 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_link_inside_the_root_aimed_outside_it_is_refused`
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_path_resolution_that_leaves_the_root_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[durable-append]`
  - `tests/test_config_test_root.py::test_the_configuration_is_not_allowed_the_system_temporary_folder`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    if "pytest" not in sys.modules:
        return
    root = _TEST_WRITE_ROOT
```

New text:

```
    if True:
        return
    root = _TEST_WRITE_ROOT
```

### `r301.F1_section_not_built`

The recognition section is never read from the file, so every install gets the default

- File: `src/cratekit/core/config.py`
- Source: `r301.json`, row `F1_section_not_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/intake/test_workers.py`
- Collected: 319 against a baseline of 319
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_configured_host_and_month_are_the_ones_every_paid_call_meets[identify]`
  - `tests/intake/test_workers.py::test_the_configured_host_and_month_are_the_ones_every_paid_call_meets[set]`
  - `tests/test_config.py::test_the_fingerprint_changes_when_any_value_changes[recognition-host-identify-eu-west-1.acrcloud.com]`
  - `tests/test_config.py::test_the_fingerprint_changes_when_any_value_changes[recognition-monthly_calls-250]`
  - `tests/test_config.py::test_the_recognition_defaults_bound_the_month_and_name_one_region`

Old text:

```
        recognition=_build(RecognitionConfig, data.get("recognition") or {}),
```

New text:

```
        recognition=RecognitionConfig(),
```

### `r345.A9_derive_on_load`

from_dict: do not derive backup.remote from the destinations

- File: `src/cratekit/core/config.py`
- Source: `r345.json`, row `A9_derive_on_load`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 758 against a baseline of 758
- Kills: 9 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_an_rclone_remote_is_accepted`
  - `tests/test_config.py::test_an_unset_backup_destination_stays_allowed[full]`
  - `tests/test_config.py::test_an_unset_backup_destination_stays_allowed[slim]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[Sicherung_\xfc]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[b2]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[gdrive-2.old]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[me@gdrive]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[my drive]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[work+home]`

Old text:

```
            overrides={"remote": derived_backup_remote(data)},
```

New text:

```
            overrides=None,
```

### `r44-a.C4_identity_not_read`

Never read a rule's identity in, so every configured rule arrives unrecorded

- File: `src/cratekit/core/config.py`
- Source: `r44-a.json`, row `C4_identity_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_deletion.py`
- Collected: 583 against a baseline of 583
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_prefix_rule_carries_the_identity_of_the_volume_it_points_at`
  - `tests/test_deletion.py::test_the_rules_the_pass_builds_from_configuration_carry_each_recorded_identity`

Old text:

```
                    volume_id=entry.get(PREFIX_VOLUME_IDENTITY_KEY),
```

New text:

```
                    volume_id=None,
```

### `r790-c.C2_config_built`

from_dict: ignore the labels section and always take the default

- File: `src/cratekit/core/config.py`
- Source: `r790-c.json`, row `C2_config_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_config.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`

Old text:

```
        labels=_build(LabelsConfig, data.get("labels") or {}),
```

New text:

```
        labels=LabelsConfig(),
```

### `r926.G10_no_temporary_allowance`

The primitives lose the system temporary allowance, the strict rule the review round measured at 101 refusals

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G10_no_temporary_allowance`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_provider_gate.py`
- Collected: 135 against a baseline of 135
- Kills: 17 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_scratch_write_in_the_system_temporary_folder_lands_without_a_root`
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_client_session_as_the_park`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[excludes-another-processs-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[names-rate-limit-answers]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[reports-its-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[survives-a-refusal]`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[the-hours-line-U278]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_client_session_attaches_the_gate_before_the_login_goes_out`
  - `tests/test_provider_gate.py::test_client_session_with_no_gate_still_paces_at_the_defaults`
  - `tests/test_provider_gate.py::test_each_opener_paces_with_the_frozen_configuration[account]`
  - `tests/test_provider_gate.py::test_each_opener_paces_with_the_frozen_configuration[catalogue]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    if system_temporary:
        allowed.append(
```

New text:

```
    if False:
        allowed.append(
```

### `r926.G11_mkdir_before_check`

save creates the configuration directory before the lock is built, so a refused write leaves a directory behind

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G11_mkdir_before_check`
- Moved: Same lines in save; U298 renamed _mkdir_private to the public mkdir_private
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 3 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_path_resolution_that_leaves_the_root_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`

Old text:

```
    with _write_lock(target):
        mkdir_private(target.parent)
        atomic_write_bytes(config.to_toml_bytes(), target)
```

New text:

```
    mkdir_private(target.parent)
    with _write_lock(target):
        atomic_write_bytes(config.to_toml_bytes(), target)
```

### `r926.G12_message_drops_path`

The no root refusal stops naming the path it refused

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G12_message_drops_path`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 5 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
            f"refused to write {path}: this process is "
            f"running under pytest and no test root is registered, so the "
```

New text:

```
            f"refused to write the file: this process is "
            f"running under pytest and no test root is registered, so the "
```

### `r926.G2_checks_the_shipped_tool`

The guard runs in a process without pytest too, so the shipped tool refuses every configuration save

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G2_checks_the_shipped_tool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 2 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_process_without_pytest_loaded_is_never_checked`
  - `tests/test_config_update.py::test_three_real_processes_writing_at_once_all_keep_their_answers`

Old text:

```
    if "pytest" not in sys.modules:
        return
    root = _TEST_WRITE_ROOT
```

New text:

```
    if False:
        return
    root = _TEST_WRITE_ROOT
```

### `r926.G3_document_check_dropped`

_write_lock no longer checks, so the configuration document is held only by the primitives' temporary allowance

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G3_document_check_dropped`
- Moved: Same lines in _write_lock; U298 renamed _exclusive_lock to the public exclusive_lock
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 4 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_the_configuration_is_not_allowed_the_system_temporary_folder`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    _refuse_write_outside_test_root(path)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

New text:

```
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

### `r926.G4_document_gets_temporary`

The configuration document is given the system temporary allowance the primitives have

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G4_document_gets_temporary`
- Moved: Same lines in _write_lock; U298 renamed _exclusive_lock to the public exclusive_lock
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 4 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_the_configuration_is_not_allowed_the_system_temporary_folder`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    _refuse_write_outside_test_root(path)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

New text:

```
    _refuse_write_outside_test_root(path, system_temporary=True)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

### `r926.G5_atomic_write_unchecked`

atomic_write_bytes no longer checks, so a ledger or token write from an unisolated test lands anywhere

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G5_atomic_write_unchecked`
- Moved: Same lines in atomic_write_bytes; U298 renamed _mkdir_private to the public mkdir_private
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 2 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[atomic-write]`

Old text:

```
    _refuse_write_outside_test_root(path, system_temporary=True)
    mkdir_private(path.parent)
    fd, tmp = tempfile.mkstemp(
```

New text:

```
    mkdir_private(path.parent)
    fd, tmp = tempfile.mkstemp(
```

### `r926.G6_lock_unchecked`

_exclusive_lock no longer checks, so a session lock from an unisolated test is created anywhere

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G6_lock_unchecked`
- Moved: Same lines in the lock's __enter__; U298 renamed the class to exclusive_lock and _mkdir_private to mkdir_private
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 1 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`

Old text:

```
        _refuse_write_outside_test_root(self.path, system_temporary=True)
        mkdir_private(self.path.parent)
```

New text:

```
        mkdir_private(self.path.parent)
```

### `r926.G7_no_root_allows_all`

With no root registered the allowed set is the filesystem root, so the R-926 probe writes the live config again

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G7_no_root_allows_all`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 6 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    allowed = [] if root is None else [root.resolve()]
```

New text:

```
    allowed = [Path(os.sep)] if root is None else [root.resolve()]
```

### `r926.G8_target_unresolved`

The target is compared as spelled, so a link inside the root aimed outside it passes

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G8_target_unresolved`
- Moved: Same lines in _refuse_write_outside_test_root; U298 renamed _is_inside to the public is_inside
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 1 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_link_inside_the_root_aimed_outside_it_is_refused`

Old text:

```
    target = path.resolve()
    if any(is_inside(target, each) for each in allowed):
```

New text:

```
    target = path
    if any(is_inside(target, each) for each in allowed):
```

### `r926.G9_temporary_unresolved`

The system temporary directory is compared as spelled, /var against /private/var on macOS, so every scratch write is refused

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G9_temporary_unresolved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_provider_gate.py`
- Collected: 22808 against a baseline of 22808
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        allowed.append(Path(tempfile.gettempdir()).resolve())
```

New text:

```
        allowed.append(Path(tempfile.gettempdir()))
```

### `u107-a.S01_record_not_json`

sync_cli.load_record: read a record that is not JSON as an empty one, so every question is asked again and every answer is lost

- File: `src/cratekit/core/config.py`
- Source: `u107-a.json`, row `S01_record_not_json`
- Moved: U298 replaced label/sync_cli.load_record's own JSON read with config.read_json_map over config.read_json; the not JSON refusal is read_json's, and answering absent there makes load_record return its empty record, the same outcome the original return of _empty gave
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_record_that_cannot_be_read_refuses_rather_than_asking_everything_again`
  - `tests/test_label_sync.py::test_the_labels_sweep_refuses_an_unreadable_record_before_any_login`

Old text:

```
    except ValueError as exc:
        raise unusable("it is not JSON") from exc


def read_json_map(
```

New text:

```
    except ValueError as exc:
        return False, None


def read_json_map(
```

### `u206.M25_lock_skipped`

Cache._locked: yield as held without taking the lock

- File: `src/cratekit/core/config.py`
- Source: `u206.json`, row `M25_lock_skipped`
- Moved: U298 replaced isrc_cache.Cache._locked's body with config.lock_within, which _locked now returns; the same non blocking flock in the same poll loop, so dropping it yields held without the lock
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1130 against a baseline of 1130
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_two_writer_processes_leave_one_readable_file_holding_both`

Old text:

```
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                had = True
```

New text:

```
            try:
                had = True
```

### `u254.C1_append_unsynced`

append_durable_bytes: return without syncing the appended record

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C1_append_unsynced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 963 against a baseline of 963
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_every_append_is_synced_before_the_mark_returns`

Old text:

```
            view = view[os.write(fd, view) :]
        os.fsync(fd)
```

New text:

```
            view = view[os.write(fd, view) :]
```

### `u254.C2_append_one_write`

append_durable_bytes: make one write call and drop what it did not take

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C2_append_one_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 963 against a baseline of 963
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_the_system_writes_in_pieces_still_lands_whole`

Old text:

```
        while view:
            view = view[os.write(fd, view) :]
```

New text:

```
        if view:
            view = view[os.write(fd, view) :]
```

### `u254.C3_append_test_root`

append_durable_bytes: drop the test root refusal

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C3_append_test_root`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 963 against a baseline of 963
- Kills: 2 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[durable-append]`

Old text:

```
    _refuse_write_outside_test_root(path, system_temporary=True)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

New text:

```
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

### `u254.C4_append_not_append`

append_durable_bytes: open for writing at the start of the file rather than its end

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C4_append_not_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 963 against a baseline of 963
- Kills: 54 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[1]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[2]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[3]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[4]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_does_not_parse_the_ledger_it_appends_to`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_journal_this_process_never_wrote_appends`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_ledger_written_before_u254_keeps_every_record`
  - `tests/test_adopt_apply_journal_u254.py::test_a_re_mark_replaces_the_earlier_record_as_the_document_did`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_another_process_appended_is_kept`
  - `tests/test_adopt_apply_journal_u254.py::test_a_revert_after_a_partial_apply_restores_what_it_wrote`
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_tail_left_inside_one_clock_tick_is_still_cut`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_the_system_writes_in_pieces_still_lands_whole`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-1]`
  - ... and 39 more, see the JSON sidecar

Old text:

```
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

New text:

```
    fd = os.open(path, os.O_WRONLY)
```

### `u272.C1_no_flush`

flush_to_disk: open and close the path and flush nothing

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C1_no_flush`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 14 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_a_directory_is_flushed_through_the_same_call`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[EINVAL]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTSUP]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTTY]`
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`
  - `tests/test_snapshot_flush_u272.py::test_a_plain_sync_that_fails_raises`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed`
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one`
  - `tests/test_snapshot_flush_u272.py::test_the_manifest_is_followed_by_a_flush_of_the_directory_that_holds_it`
  - `tests/test_snapshot_flush_u272.py::test_where_no_full_flush_exists_the_plain_sync_is_the_flush`

Old text:

```
    try:
        _flush_descriptor(fd)
    except OSError as exc:
```

New text:

```
    try:
        pass
    except OSError as exc:
```

### `u272.C2_full_flush_error_swallowed`

_flush_descriptor: fall back to the plain sync on every error of the full flush, an I/O error included

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C2_full_flush_error_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`

Old text:

```
            if exc.errno not in _FULL_FLUSH_UNSUPPORTED:
                raise
```

New text:

```
            if False:
                raise
```

### `u272.C3_full_flush_then_sync`

_flush_descriptor: drop the return after a full flush, so the plain sync runs as well

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C3_full_flush_then_sync`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one`

Old text:

```
            _full_flush(fd, _FULL_FLUSH)
            return
```

New text:

```
            _full_flush(fd, _FULL_FLUSH)
```

### `u272.C4_full_flush_never_asked`

_flush_descriptor: never ask for the full flush, the plain sync on every platform

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C4_full_flush_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 5 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[EINVAL]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTSUP]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTTY]`
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one`

Old text:

```
    if _FULL_FLUSH is not None:
        try:
```

New text:

```
    if False:
        try:
```

### `u272.C5_eio_counts_as_unsupported`

_FULL_FLUSH_UNSUPPORTED: count an I/O error as a filesystem without the full flush

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C5_eio_counts_as_unsupported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`

Old text:

```
frozenset({errno.ENOTSUP, errno.EOPNOTSUPP, errno.EINVAL, errno.ENOTTY})
```

New text:

```
frozenset({errno.ENOTSUP, errno.EOPNOTSUPP, errno.EINVAL, errno.ENOTTY, errno.EIO})
```

### `u272.C6_no_plain_sync`

_flush_descriptor: drop the plain sync, so a platform without the full flush flushes nothing

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C6_no_plain_sync`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 12 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_a_directory_is_flushed_through_the_same_call`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[EINVAL]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTSUP]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTTY]`
  - `tests/test_snapshot_flush_u272.py::test_a_plain_sync_that_fails_raises`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed`
  - `tests/test_snapshot_flush_u272.py::test_the_manifest_is_followed_by_a_flush_of_the_directory_that_holds_it`
  - `tests/test_snapshot_flush_u272.py::test_where_no_full_flush_exists_the_plain_sync_is_the_flush`

Old text:

```
                raise
    os.fsync(fd)

```

New text:

```
                raise

```

### `u272.C7_error_names_no_path`

flush_to_disk: raise a flush error as it came, naming no file

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C7_error_names_no_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 641 against a baseline of 641
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_plain_sync_that_fails_raises`

Old text:

```
        if exc.filename is not None:
            raise
        raise OSError(exc.errno, exc.strerror or str(exc), str(path)) from exc
```

New text:

```
        raise
```

### `u298.H10_flock_exclusive_hardens`

flock_exclusive: a lock file left at another mode is never hardened

- File: `src/cratekit/core/config.py`
- Source: `u298.json`, row `H10_flock_exclusive_hardens`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 352 against a baseline of 352
- Kills: 3 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_waiting_lock_that_fails_closes_its_handle_and_leaves_as_itself[failure0]`
  - `tests/test_shared_homes.py::test_a_waiting_lock_that_fails_closes_its_handle_and_leaves_as_itself[failure1]`
  - `tests/test_shared_homes.py::test_the_waiting_lock_hardens_its_file_before_it_locks_and_returns_the_holder`

Old text:

```
        handle = os.fdopen(descriptor, "r+b")
        harden(target)
```

New text:

```
        handle = os.fdopen(descriptor, "r+b")
```

### `u298.H11_read_json_refuses_garbage`

read_json: a document that is not JSON reads as an empty record

- File: `src/cratekit/core/config.py`
- Source: `u298.json`, row `H11_read_json_refuses_garbage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 352 against a baseline of 352
- Kills: 4 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_document_that_does_not_parse_is_refused_and_never_read_as_empty[\xff\xfe\x00]`
  - `tests/test_shared_homes.py::test_a_document_that_does_not_parse_is_refused_and_never_read_as_empty[]`
  - `tests/test_shared_homes.py::test_a_document_that_does_not_parse_is_refused_and_never_read_as_empty[{not json]`
  - `tests/test_shared_homes.py::test_bytes_that_are_not_text_leave_the_platform_read_as_the_decoding_failure_they_are`

Old text:

```
        return True, json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise unusable("it could not be opened") from exc
    except ValueError as exc:
        raise unusable("it is not JSON") from exc
```

New text:

```
        return True, json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise unusable("it could not be opened") from exc
    except ValueError:
        return True, {}
```

### `u298.H12_read_json_map_shape`

read_json_map: a list at the top level is handed on as a record

- File: `src/cratekit/core/config.py`
- Source: `u298.json`, row `H12_read_json_map_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 352 against a baseline of 352
- Kills: 4 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_document_that_is_no_map_is_refused_by_what_it_is["words"-str]`
  - `tests/test_shared_homes.py::test_a_document_that_is_no_map_is_refused_by_what_it_is[3-int]`
  - `tests/test_shared_homes.py::test_a_document_that_is_no_map_is_refused_by_what_it_is[[]-list]`
  - `tests/test_shared_homes.py::test_a_document_that_is_no_map_is_refused_by_what_it_is[null-NoneType]`

Old text:

```
    if not isinstance(raw, Mapping):
        raise unusable(f"the document is a {type(raw).__name__}, not a map")
```

New text:

```
(empty)
```

### `u298.H7_held_translates_acquisition`

held: a lock another holder has leaves as the lock error, not the store's own refusal

- File: `src/cratekit/core/config.py`
- Source: `u298.json`, row `H7_held_translates_acquisition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 352 against a baseline of 352
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_lock_that_cannot_be_taken_is_refused_in_the_stores_own_words`

Old text:

```
    except ConfigLockUnavailable as exc:
        raise refused(exc) from exc
```

New text:

```
    except ConfigLockUnavailable:
        raise
```

### `u298.H8_lock_within_takes_lock`

lock_within: reads the lock as had without taking it, so two writers interleave

- File: `src/cratekit/core/config.py`
- Source: `u298.json`, row `H8_lock_within_takes_lock`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 352 against a baseline of 352
- Kills: 3 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_lock_another_holds_is_asked_for_until_the_wait_is_spent_and_then_given_up`
  - `tests/test_shared_homes.py::test_a_lock_freed_during_the_wait_is_had_at_the_next_look`
  - `tests/test_shared_homes.py::test_a_lock_had_in_time_is_yielded_as_had_and_its_file_is_private_and_stays`

Old text:

```
        had = fcntl is None
```

New text:

```
        had = True
```

### `u299.U13_from_dict_applies_overrides`

config.from_dict: the overrides are left to validation, so the built config keeps the file's root

- File: `src/cratekit/core/config.py`
- Source: `u299.json`, row `U13_from_dict_applies_overrides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_config_test_root.py`
- Collected: 269 against a baseline of 269
- Kills: 4 (killed)
- Killed:
  - `tests/test_config.py::test_a_relocated_root_carries_the_database_that_sat_under_it`
  - `tests/test_config.py::test_a_save_under_a_relocation_writes_a_file_that_loads_again`
  - `tests/test_config.py::test_the_backup_destination_check_reads_the_effective_mapping`
  - `tests/test_config.py::test_the_prefix_map_survives_a_remount_because_it_interpolates`

Old text:

```
    data = _apply_env_overrides(data)
    problems = validate(data)
```

New text:

```
    problems = validate(data)
```

### `u329.R1_config_remedy_drifts_from_the_canonical_text`

config.Remedy is a vocabulary of its own again, its run-setup token spelled differently from the canonical one

- File: `src/cratekit/core/config.py`
- Source: `u329.json`, row `R1_config_remedy_drifts_from_the_canonical_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_reserved_causes.py`
- Collected: 1526 against a baseline of 1526
- Kills: 8 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_an_unconfigured_machine_refuses_with_a_precondition_and_a_remedy`
  - `tests/test_cli_contract.py::test_every_module_declaring_its_own_remedies_stays_inside_one_vocabulary`
  - `tests/test_cli_contract.py::test_every_module_local_remedy_renders_to_something_a_user_can_act_on`
  - `tests/test_config_update.py::test_two_wizards_answering_one_key_differently_refuse_and_write_nothing`
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  - `tests/test_reserved_causes.py::test_the_static_enum_rule_agrees_with_the_interpreter_over_the_whole_package`
  - `tests/test_reserved_causes.py::test_upgrade_cratekit_is_declared_twice_and_this_table_reserves_one_meaning`

Old text:

```
from cratekit.core.exit_codes import Remedy as Remedy

```

New text:

```
from cratekit.core.exit_codes import Remedy as _Canonical

Remedy = __import__("enum").StrEnum("Remedy", {m.name: m.value.replace("run-setup", "run-set-up") for m in _Canonical})

```

### `u132.P1_collision_hold`

The planner adds a bucket whose words another bucket of the copy's files

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u132.json`, row `P1_collision_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 5 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_vocabulary_row_whose_tag_files_where_the_template_shares_the_word_is_not_named`
  - `tests/test_taxonomy_upgrade.py::test_every_bucket_of_the_copy_filing_a_word_is_named_not_the_first`
  - `tests/test_taxonomy_upgrade.py::test_jazz_is_held_while_non_electronic_still_files_its_words_and_every_place_is_named`
  - `tests/test_taxonomy_upgrade.py::test_one_place_filing_a_word_under_two_spellings_names_both_in_one_sentence`
  - `tests/test_taxonomy_upgrade.py::test_soul_is_held_while_rnb_still_files_its_words_until_the_hand_edit`

Old text:

```
                if clashes:

```

New text:

```
                if False:

```

### `u132.P3_candidate_loader_hold`

A candidate that makes the copy fail to load is added anyway

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u132.json`, row `P3_candidate_loader_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_second_playlist_class_under_another_id_holds_favorites`
  - `tests/test_taxonomy_upgrade.py::test_a_version_line_the_planner_cannot_find_holds_the_raise_and_what_needs_it`

Old text:

```
            loaded = _loads(placed)
            if isinstance(loaded, list):

```

New text:

```
            loaded = _loads(placed)
            if False:

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

### `u132.P6_cut_equality`

A cut that parses to something else than the shipped entry is returned

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u132.json`, row `P6_cut_equality`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_cut_that_parses_to_something_else_refuses`

Old text:

```
            if parsed[0] != shipped[0]:

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

### `u133-a-rerun.P5_vocabulary_owner`

A vocabulary row is named by its tag alone, whichever bucket files that tag

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u133-a-rerun.json`, row `P5_vocabulary_owner`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_vocabulary_row_whose_tag_files_where_the_template_shares_the_word_is_not_named`

Old text:

```
            if (row.bucket, row.tag.casefold().strip()) in clashing:

```

New text:

```
            if row.tag.casefold().strip() in {word for _owner, word in clashing}:

```

### `u133-a-rerun.P8_held_by_whole_copy`

Only the copy's first bucket filing a word is asked about, as the setdefault before U133 did across buckets

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u133-a-rerun.json`, row `P8_held_by_whole_copy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_vocabulary_row_whose_tag_files_where_the_template_shares_the_word_is_not_named`
  - `tests/test_taxonomy_upgrade.py::test_every_bucket_of_the_copy_filing_a_word_is_named_not_the_first`

Old text:

```
            filed.setdefault(word, []).extend((bucket.id, s, w) for s, w in places)

```

New text:

```
            filed.setdefault(word, list((bucket.id, s, w) for s, w in places))

```

### `u133-a.P10_keyword_note_for_held`

A keyword rule of a bucket the plan does not add is spoken of too

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u133-a.json`, row `P10_keyword_note_for_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_jazz_is_held_while_non_electronic_still_files_its_words_and_every_place_is_named`

Old text:

```
        if rule.bucket not in added:
            continue

```

New text:

```
(empty)
```

### `u133-a.P13_remedy_keyword`

Doctor's remedy drops the keyword rule sentence

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u133-a.json`, row `P13_remedy_keyword`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_the_hand_edit_the_hold_names_lets_jazz_in_on_the_next_run`

Old text:

```
    parts.extend(found.keywords)

```

New text:

```
(empty)
```

### `u133-a.P1_first_place_only`

A word filed in several places of one bucket names only the first, as before U133

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u133-a.json`, row `P1_first_place_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_jazz_is_held_while_non_electronic_still_files_its_words_and_every_place_is_named`
  - `tests/test_taxonomy_upgrade.py::test_one_place_filing_a_word_under_two_spellings_names_both_in_one_sentence`

Old text:

```
        places = found.setdefault(word.casefold().strip(), [])
        if (word, where) not in places:
            places.append((word, where))

```

New text:

```
        places = found.setdefault(word.casefold().strip(), [])
        if not places:
            places.append((word, where))

```

### `u133-a.P2_one_spelling_per_place`

One place filing a word under two spellings names only the first, the review's finding 3

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u133-a.json`, row `P2_one_spelling_per_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_one_place_filing_a_word_under_two_spellings_names_both_in_one_sentence`

Old text:

```
        if (word, where) not in places:
            places.append((word, where))

```

New text:

```
        if all(known != where for _spelling, known in places):
            places.append((word, where))

```

### `u133-a.P3_map_row_label`

A source map row is labelled as the sub it files into, merging two hand edits into one sentence

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u133-a.json`, row `P3_map_row_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_jazz_is_held_while_non_electronic_still_files_its_words_and_every_place_is_named`

Old text:

```
add(source, f"{bucket.id}, its source map row to {sub_id}")
```

New text:

```
add(source, f"{bucket.id}, its sub {sub_id}")
```

### `u133-a.P4_vocabulary_row_named`

A vocabulary row writing a clashing word is not named in the hold

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u133-a.json`, row `P4_vocabulary_row_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_jazz_is_held_while_non_electronic_still_files_its_words_and_every_place_is_named`

Old text:

```
            if (row.bucket, row.tag.casefold().strip()) in clashing:

```

New text:

```
            if False:

```

### `u133-a.P7_designed_sharing`

A word the shipped template files in both places counts as a clash (U132's P2, re-measured in its rewritten form)

- File: `src/cratekit/core/taxonomy_upgrade.py`
- Source: `u133-a.json`, row `P7_designed_sharing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_vocabulary_row_whose_tag_files_where_the_template_shares_the_word_is_not_named`
  - `tests/test_taxonomy_upgrade.py::test_a_word_the_shipped_template_files_twice_is_not_a_clash`

Old text:

```
            if word in designed.get(owner, set()):
                continue

```

New text:

```
(empty)
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

### `r1037.N1_landed_not_recorded`

_record_landing_commit: never write collection_landed, so no landed row is ever offered

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N1_landed_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 119 against a baseline of 119
- Kills: 33 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landing_of_another_database_offers_nothing`
  - `tests/test_delete_landed_removed.py::test_a_landing_one_of_whose_playlists_is_gone_offers_nothing`
  - `tests/test_delete_landed_removed.py::test_a_landing_record_with_no_update_count_offers_nothing[12]`
  - `tests/test_delete_landed_removed.py::test_a_landing_record_with_no_update_count_offers_nothing[None]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    if landed is not None:
        record.detail[LANDED_ROWS_KEY] = dict(landed)
```

New text:

```
    if False:
        record.detail[LANDED_ROWS_KEY] = dict(landed)
```

### `r1037.N2_joined_not_made`

_landed_rows: record every playlist the rows joined, made or already there

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N2_joined_not_made`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 119 against a baseline of 119
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_restored_landing_into_a_playlist_already_there_is_never_offered`

Old text:

```
    playlists = sorted({str(one) for one in joined if one and str(one) not in before})
```

New text:

```
    playlists = sorted({str(one) for one in joined if one})
```

### `r1037.N3_identity_wrong`

_landed_rows: record no database identity

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N3_identity_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 119 against a baseline of 119
- Kills: 21 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_a_restore_to_before_the_landing_offers_nothing_and_the_screen_counts_it`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        "database_identity": plan.master_db_id,
```

New text:

```
        "database_identity": "",
```

### `r1037.N4_size_not_read`

_landed_rows: record no file size, so no landed file can be proved by its size

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N4_size_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 119 against a baseline of 119
- Kills: 12 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned`
  - `tests/test_delete_landed_removed.py::test_the_landing_record_names_every_row_it_made_as_the_database_holds_it`

Old text:

```
                    "columns": {name: _plain(getattr(content, name, None)) for name in LANDED_COLUMNS},
```

New text:

```
                    "columns": {name: _plain(getattr(content, name, None)) for name in LANDED_COLUMNS if name != "FileSize"},
```

### `r1037.N5_count_before_commit`

_landed_rows: record a count short of the one the commit left

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N5_count_before_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_the_landing_record_names_every_row_it_made_as_the_database_holds_it`

Old text:

```
        sequence = int(db.get_local_usn())
```

New text:

```
        sequence = int(db.get_local_usn()) - 1
```

### `r1037.N6_before_empty`

apply_rows: read no playlist before the landing, so a playlist already there is recorded as made

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N6_before_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 119 against a baseline of 119
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_restored_landing_into_a_playlist_already_there_is_never_offered`

Old text:

```
        playlists_before = frozenset(str(row.ID) for row in db.get_playlist())
```

New text:

```
        playlists_before = frozenset()
```

### `r1844.N13_landing_writes_no_uuid`

native landing: the record names each row with an empty UUID

- File: `src/cratekit/intake/native.py`
- Source: `r1844.json`, row `N13_landing_writes_no_uuid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`
- Collected: 86 against a baseline of 86
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_the_landing_record_names_each_row_by_the_uuid_the_database_holds`

Old text:

```
                    LANDED_UUID_KEY: str(getattr(content, "UUID", None) or ""),
```

New text:

```
                    LANDED_UUID_KEY: "",
```

### `r746-b.N3_folder_path_not_restamped`

_restamp: the row keeps the path the binding stored, the planned path is never put on it

- File: `src/cratekit/intake/native.py`
- Source: `r746-b.json`, row `N3_folder_path_not_restamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_folder_path_is_stored_under_the_base_drive_rekordbox_records`

Old text:

```
    if str(content.FolderPath) != row.folder_path:
        content.FolderPath = row.folder_path
```

New text:

```
    if False:
        content.FolderPath = row.folder_path
```

### `r746-b.N4_device_not_restamped`

_restamp: the row keeps the device the binding chose

- File: `src/cratekit/intake/native.py`
- Source: `r746-b.json`, row `N4_device_not_restamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_landed_rows_carry_what_rekordbox_loads_and_no_analysis_value`

Old text:

```
    if str(content.DeviceID) != plan.device_id:
        content.DeviceID = plan.device_id
```

New text:

```
    if False:
        content.DeviceID = plan.device_id
```

### `r777.N16_pass_not_recorded`

The native landing's commit no longer records the pass

- File: `src/cratekit/intake/native.py`
- Source: `r777.json`, row `N16_pass_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`

Old text:

```
    if plan.pass_name:
        record.detail[PASS_KEY] = plan.pass_name
```

New text:

```
    if False:
        record.detail[PASS_KEY] = plan.pass_name
```

### `r923.N1_landing_sets_nothing`

The native landing no longer sets rekordbox's defaults on a row it creates

- File: `src/cratekit/intake/native.py`
- Source: `r923.json`, row `N1_landing_sets_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_landed_rows_carry_what_rekordbox_loads_and_no_analysis_value`

Old text:

```
        if getattr(content, column, None) is None:
```

New text:

```
        if False:
```

### `u113-c.C1_native_batch_always`

The native write always makes the batch playlist, empty when every row was claimed

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C1_native_batch_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`
- Collected: 60 against a baseline of 60
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`

Old text:

```
            if ordered or not accounts:
```

New text:

```
            if True:
```

### `u113-c.C2_native_batch_keeps_claimed`

The native batch playlist holds the claimed rows too

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C2_native_batch_keeps_claimed`
- Moved: the same guard, the claimed test of the batch walk, now one comprehension in native.py's _batch_order (U307 folded the loop)
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`
- Collected: 60 against a baseline of 60
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`

Old text:

```
        dict.fromkeys(by_target[one] for one in targets if one in by_target and one not in claimed)
```

New text:

```
        dict.fromkeys(by_target[one] for one in targets if one in by_target)
```

### `u113-c.C3_native_found_by_name`

An account playlist is found by its name under INBOX and added to, rather than created

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C3_native_found_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`

Old text:

```
                created = db.create_playlist(one.name, parent=anchor)
```

New text:

```
                created = rb_writer.ensure_playlist(db, one.name, anchor)
```

### `u113-c.C4_native_record_unnamed`

The native landing record does not list the account playlists by identifier

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C4_native_record_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`

Old text:

```
        record.detail[INBOX_PLAYLISTS_KEY] = [
```

New text:

```
        record.detail["inbox_playlists_unread"] = [
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

### `u120.N3_identity_without_hearts`

identity: the digest leaves the hearts out

- File: `src/cratekit/intake/native.py`
- Source: `u120.json`, row `N3_identity_without_hearts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_the_hearts_are_in_the_digest_so_another_set_is_another_plan`

Old text:

```
    favorites = {"favorites": plan.favorites.identity()} if plan.favorites is not None else {}
```

New text:

```
    favorites = {}
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

### `u126.F3_counts_undigested`

Digest the value alone, so the counts the screen shows can change under an approval

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `F3_counts_undigested`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_link_its_count_the_playlist_and_each_file_move_the_digest`

Old text:

```
            {"value": plan.link.value, "carriers": plan.link.carriers, "rows": plan.link.rows}
```

New text:

```
            {"value": plan.link.value}
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

### `u126.R3_check_skipped`

Skip the read back's ContentLink check

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R3_check_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - `tests/test_intake_land_native.py::test_assert_rows_identified_holds_the_file_id_and_the_link_to_the_ones_planned`

Old text:

```
        if landed.content_link is None or row.content_link != landed.content_link
```

New text:

```
        if False
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

### `u126.S2_defaults_left_null`

Sample, R-923: drop the defaults fill, so the binding's NULLs stay

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `S2_defaults_left_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_landed_rows_carry_what_rekordbox_loads_and_no_analysis_value`

Old text:

```
        if getattr(content, column, None) is None:
            setattr(content, column, value)
```

New text:

```
        pass
```

### `u127-b.N6b_digest_blind_to_vox`

Drop each added row's score and answer from the digest, after the engine test

- File: `src/cratekit/intake/native.py`
- Source: `u127-b.json`, row `N6b_digest_blind_to_vox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_engine_digest_covers_each_rows_score_and_answer`

Old text:

```
                "rows": [[str(row.target), row.voxlevel, row.vox] for row in plan.to_add()],
```

New text:

```
                "rows": [[str(row.target)] for row in plan.to_add()],
```

### `u127.N10_record_silent`

Record no commit under the vocals key, so a restore cannot count the tags

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N10_record_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`

Old text:

```
    if vox_written > 0:
```

New text:

```
    if vox_written > 10**6:
```

### `u127.N11_missing_unreported`

Never report a planned tag that adoption does not read back

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N11_missing_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`

Old text:

```
            row.target for row, content_id in added_ids if row.vox and content_id not in voxed
```

New text:

```
            row.target for row, content_id in added_ids if False
```

### `u127.N12_unscored_dropped`

Name no unscored file on the landed record

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N12_unscored_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`

Old text:

```
    unscored = {row.target for row in plan.vox_unscored()}
```

New text:

```
    unscored = set()
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

### `u127.N7_digest_blind_to_cut`

Drop the cut from the digest

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N7_digest_blind_to_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_screen_counts_the_tagged_rows_and_the_digest_moves_with_a_tag_and_the_cut`

Old text:

```
                "cut": plan.vox_cut,
```

New text:

```
                "cut": None,
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

### `u128-b.N1_native_owned_unwritten`

The native commit joins no owned row to its playlist, the new rows alone

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N1_native_owned_unwritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
                        member.content_id
                        if member.target is None
```

New text:

```
                        ""
                        if member.target is None
```

### `u128-b.N2_native_record_no_pass`

The native landing's record names no pass, so a rerun cannot find what it mirrored

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N2_native_record_no_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`

Old text:

```
                ingest.INBOX_PASS_KEY: plan.pass_name or "",
```

New text:

```
                ingest.INBOX_PASS_KEY: "",
```

### `u135.A14_set_order_reverses`

INBOX set-order walk appends members in reverse position order

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A14_set_order_reverses`
- Moved: the same walk over the set's members in position order, now in native.py's _batch_order (U307 folded the loop)
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

### `u146-c.N2_owned_not_written`

apply_rows: the owned hearts are planned and shown and never written

- File: `src/cratekit/intake/native.py`
- Source: `u146-c.json`, row `N2_owned_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
                pairs.extend((one.content_id, one.month) for one in plan.favorites.owned)
```

New text:

```
(empty)
```

### `u146-e.N3_owned_out_of_digest`

FavoritesPlan.identity: the owned hearts are not digested, so an answer given for one set of them stands for another

- File: `src/cratekit/intake/native.py`
- Source: `u146-e.json`, row `N3_owned_out_of_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 22808 against a baseline of 22808
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if self.owned:
            identity["owned"] = [
```

New text:

```
        if self.owned and False:
            identity["owned"] = [
```

### `u150.F2_record_provider`

native._record_commit: write no provider tracks on the landing's record

- File: `src/cratekit/intake/native.py`
- Source: `u150.json`, row `F2_record_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_the_record_names_each_landed_rows_provider_track_for_the_account_mirror`

Old text:

```
        record.detail[label_filing.PROVIDER_KEY] = dict(labels_written.provider)
```

New text:

```
        pass
```

### `u153.N1_restamp_id_text`

native _restamp: do not coerce the minted ID to text, so a colour on an existing row cannot flush beside a new one

- File: `src/cratekit/intake/native.py`
- Source: `u153.json`, row `N1_restamp_id_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 25 against a baseline of 25
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it`
  - `tests/test_intake_land_hearts_native.py::test_a_source_at_the_root_takes_its_months_beside_it`
  - `tests/test_intake_land_hearts_native.py::test_once_a_band_holds_the_heart_the_additive_refresh_puts_it_in_that_folders_favorites`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
    content.ID = str(content.ID)
```

New text:

```
    content.ID = content.ID
```

### `u153.N3_landing_colour_owned`

native apply: drop the owned hearts from the colour set, so an owned heart is placed but not coloured

- File: `src/cratekit/intake/native.py`
- Source: `u153.json`, row `N3_landing_colour_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
                to_colour.extend(plan.favorites.colour)
```

New text:

```
                to_colour.extend([])
```

### `u156.L18_digest_native`

native.identity: leave the label plan out of the landing's digest

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L18_digest_native`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 90 against a baseline of 90
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_year_playlist_made_after_the_answer_makes_the_answer_stale`
  - `tests/test_intake_land_labels_native.py::test_the_digest_moves_with_the_manifests_bytes`
  - `tests/test_intake_land_labels_native.py::test_the_label_source_moves_the_digest_and_an_answer_for_one_is_stale_for_another`

Old text:

```
    filed = {"labels": label_filing.identity(plan.labels)} if plan.labels is not None else {}
```

New text:

```
    filed = {}
```

### `u156.L19_write_called`

apply_rows: plan the labels and never write them

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L19_write_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 90 against a baseline of 90
- Kills: 17 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_batch_of_two_labels_and_an_unregistered_seller_files_each_under_its_own`
  - `tests/test_intake_land_labels_native.py::test_a_file_left_in_staging_is_filed_nowhere_and_not_said_to_be_in_the_intake_playlist[2021]`
  - `tests/test_intake_land_labels_native.py::test_a_file_left_in_staging_is_filed_nowhere_and_not_said_to_be_in_the_intake_playlist[None]`
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2020]`
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2021]`
  - `tests/test_intake_land_labels_native.py::test_a_file_with_no_date_tag_is_named_on_the_screen_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_label_folder_spelled_decomposed_is_the_same_folder`
  - `tests/test_intake_land_labels_native.py::test_a_labelled_file_with_no_year_is_named_and_a_decomposed_label_is_the_composed_folder`
  - `tests/test_intake_land_labels_native.py::test_a_manifest_files_its_matched_rows_under_label_and_year_and_names_the_unmatched`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_a_removed_year_playlist_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_intake_land_labels_native.py::test_an_existing_year_playlist_gains_members_and_loses_none`
  - `tests/test_intake_land_labels_native.py::test_an_undated_file_the_move_refused_is_said_not_to_have_landed`
  - `tests/test_intake_land_labels_native.py::test_label_files_each_file_once_under_the_year_its_date_tag_names`
  - `tests/test_intake_land_labels_native.py::test_one_label_spelled_two_ways_is_one_folder_and_a_file_two_rows_file_names_both_years`
  - ... and 2 more, see the JSON sidecar

Old text:

```
                labels_written = label_filing.write(db, plan.labels, by_target=by_target)
```

New text:

```
                labels_written = None
```

### `u156.L20_recorded`

_record_landing_commit: write the labels and record nothing of them on the session

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L20_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 90 against a baseline of 90
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_manifest_files_its_matched_rows_under_label_and_year_and_names_the_unmatched`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_the_same_files_landed_again_add_no_second_membership`

Old text:

```
    if labels_written is not None:
        label_filing.record_commit(record, labels_written, cfg)
```

New text:

```
    if False:
        label_filing.record_commit(record, labels_written, cfg)
```

### `u157.N2_digest_rows`

identity: the dyn block names each row's answer only, not its drift or verdict

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N2_digest_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_engine_digest_covers_each_rows_drift_verdict_and_answer`

Old text:

```
[str(row.target), row.drift, row.drift_verdict, row.dyn]
```

New text:

```
[str(row.target), row.dyn]
```

### `u157.N3_no_write`

apply: the dyn tag is never written

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N3_no_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 126 against a baseline of 126
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_landed_row_is_tagged_dyn_exactly_when_its_drift_reads_variable[exactly-at-the-cut]`
  - `tests/test_intake_land_dyn_native.py::test_a_landed_row_is_tagged_dyn_exactly_when_its_drift_reads_variable[moving]`
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection`

Old text:

```
            dyn_written = _tag_dyn(db, added_ids)
```

New text:

```
            dyn_written = 0
```

### `u157.N4_trust_the_writer`

apply: report each row's dyn from the plan, not the read back

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N4_trust_the_writer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_tag_written_under_a_removed_value_is_said_and_never_counted`

Old text:

```
                    dyn=content_id in dyned,
```

New text:

```
                    dyn=row.dyn,
```

### `u157.N5_no_record`

_record_landing_commit: record no dyn tags on the session

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N5_no_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection`

Old text:

```
    if dyn_written > 0:
        session.record_commit(
```

New text:

```
    if False:
        session.record_commit(
```

### `u161.P1_path_back_in_digest`

native.identity: digest str(plan.database) again, the line U161 removed, so a copy rehearsal can never match

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P1_path_back_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_decision_recorded_against_the_path_bearing_digest_is_stale_and_writes_nothing`
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "database": str(plan.database),
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

### `u161.P2_parent_in_digest`

native.identity: digest the database's folder under another key, a path the old key's name check would not see

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P2_parent_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "where": str(plan.database.parent),
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

### `u161.P3_file_name_in_digest`

native.identity: digest the database's file name alone, which a copy named differently from master.db would not share

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P3_file_name_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "file": plan.database.name,
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

### `u161.P4_device_out`

native.identity: drop the device, so an answer for one library is not stale for another with the same master id

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P4_device_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "master_db_id": plan.master_db_id,
```

### `u161.P5_master_out`

native.identity: drop the master id, the other half of the library identity that replaced the path

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P5_master_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "device": plan.device_id,
```

### `u161.S1_playlist_out`

native.identity: drop the batch playlist's name from the engine digest (sample of an existing guard)

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `S1_playlist_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`

Old text:

```
        "playlist": plan.playlist,
        "batch_playlist": plan.batch_playlist_id,
```

New text:

```
        "batch_playlist": plan.batch_playlist_id,
```

### `u161.S2_columns_out`

native.identity: drop each row's columns from the engine digest (sample of an existing guard)

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `S2_columns_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`

Old text:

```
                "content_id": row.content_id,
                "columns": row.columns(),
```

New text:

```
                "content_id": row.content_id,
```

### `u163.W12_readback_active`

_words_back: read the artist through any row, tombstones included

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W12_readback_active`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_the_read_back_takes_no_word_through_a_tombstoned_lookup_row`

Old text:

```
            f"LEFT JOIN {rb_writer.ARTIST_TABLE} a ON a.ID = c.{ARTIST_COLUMN} AND a.{active} "
```

New text:

```
            f"LEFT JOIN {rb_writer.ARTIST_TABLE} a ON a.ID = c.{ARTIST_COLUMN} "
```

### `u163.W13_identified_words`

assert_rows_identified: never compare the words read back

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W13_identified_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_landed_row_whose_word_reads_back_wrong_is_refused`

Old text:

```
        if row.words.get(column) != want
```

New text:

```
        if False
```

### `u163.W14_album_artist_link`

_Mints._mint: mint an album with no album artist

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W14_album_artist_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`
  - `tests/test_intake_land_words.py::test_an_album_links_the_one_its_album_artist_holds`

Old text:

```
        if word.table == rb_writer.ALBUM_TABLE:
            columns[ALBUM_ARTIST]
```

New text:

```
        if False:
            columns[ALBUM_ARTIST]
```

### `u163.W4_year_written`

_Mints.link: drop the ReleaseYear write

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W4_year_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`

Old text:

```
        if row.year is not None:
            setattr(content, YEAR_COLUMN, row.year)
```

New text:

```
        if False:
            setattr(content, YEAR_COLUMN, row.year)
```

### `u163.W7_unmoved`

_assert_words_unmoved: never refuse a word that moved since the plan

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W7_unmoved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_minted_by_another_hand_since_the_plan_refuses_and_writes_nothing`

Old text:

```
            if _rows_of(now) != _rows_of(word):
```

New text:

```
            if False:
```

### `u163.W8_mint_once`

_Mints.id_of: mint a new word again for every row

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W8_mint_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`

Old text:

```
        if key not in self._made:
            self._made[key] = self._mint(word)
```

New text:

```
        if True:
            self._made[key] = self._mint(word)
```

### `u163.W9_creations_named`

apply_rows: name only the content table in creations, so a mint is refused

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W9_creations_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 23 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[None]`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_file_id_lies_once]`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - `tests/test_intake_land_native.py::test_a_second_approved_run_over_the_landed_files_adds_nothing`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[sql2-djmdMixerParam]`
  - `tests/test_intake_land_native.py::test_folder_path_is_stored_under_the_base_drive_rekordbox_records`
  - `tests/test_intake_land_native.py::test_the_landed_rows_carry_what_rekordbox_loads_and_no_analysis_value`
  - `tests/test_intake_land_native.py::test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - ... and 8 more, see the JSON sidecar

Old text:

```
                db, creations=(rb_writer.CONTENT_TABLE, *mints.tables())
```

New text:

```
                db, creations=(rb_writer.CONTENT_TABLE,)
```

### `u164.R1_record_filed`

_record_landing_commit: never record the filed batch and its folder

- File: `src/cratekit/intake/native.py`
- Source: `u164.json`, row `R1_record_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_rehearse.py`
- Collected: 75 against a baseline of 75
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_landing_on_the_27th_lands_in_its_year_folder_under_its_subject`
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_folder_holds_is_refused_at_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`

Old text:

```
    if plan.folder is not None and plan.batch:
        record.detail[FILED_BATCH_KEY]
```

New text:

```
    if False:
        record.detail[FILED_BATCH_KEY]
```

### `u165.N1_digest`

identity: leave the predictions out of the digest

- File: `src/cratekit/intake/native.py`
- Source: `u165.json`, row `N1_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_rehearsal_digests_as_the_live_landing_that_files_and_land_only_apart`

Old text:

```
        {"filing": [one.identity() for one in plan.filing]} if plan.filing is not None else {}
```

New text:

```
        {}
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

### `u166.A5_present_rows_too`

apply_rows: add every row the plan names, present ones too

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A5_present_rows_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses`

Old text:

```
                        db, analyze, [content_id for _row, content_id in added_ids]
```

New text:

```
                        db, analyze, list(by_target.values())
```

### `u166.A6_always_create`

_analyze_row: make a new Analyze every landing

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A6_always_create`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses`
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`

Old text:

```
    return found if found is not None else db.create_playlist(ANALYZE, parent=anchor)
```

New text:

```
    return db.create_playlist(ANALYZE, parent=anchor)
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

### `u166.A8_digest_key`

identity: leave the found Analyze out of the digest

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A8_digest_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses`

Old text:

```
    analyze = {"analyze": plan.analyze_playlist_id} if plan.to_add() else {}
```

New text:

```
    analyze = {}
```

### `u173.M24_analyze_name`

native: the queue playlist renamed, so the skill sends a session to a playlist no landing fills

- File: `src/cratekit/intake/native.py`
- Source: `u173.json`, row `M24_analyze_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 32 against a baseline of 32
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

### `u307.R23_batch_order_keeps_claimed`

native._batch_order: rows an account playlist claimed join the batch playlist as well

- File: `src/cratekit/intake/native.py`
- Source: `u307.json`, row `R23_batch_order_keeps_claimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_u135_set_inbox_join.py`
- Collected: 69 against a baseline of 69
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`

Old text:

```
by_target[one] for one in targets if one in by_target and one not in claimed)
```

New text:

```
by_target[one] for one in targets if one in by_target)
```

### `r1184.M21_guess_wiring`

tag guess: drop the own name sentence from the off taxonomy warning

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `r1184.json`, row `M21_guess_wiring`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 289 against a baseline of 289
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_folders_own_name_in_another_case_is_named_with_its_one_answer`

Old text:

```
                    + taxonomy_word.own_names(declared, found.off_taxonomy)

```

New text:

```
(empty)
```

### `u172.B1_library_read_for_nothing`

signals: read the library and the pass even when no file needs a genre

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B1_library_read_for_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_folder_that_needs_no_guess_opens_no_library`

Old text:

```
    if not any(one.readable and not one.genre for one in staged):
```

New text:

```
    if False:
```

### `u172.B2_unknown_pass_silent`

_playlists: read a pass no job carries as no playlists, the round 1 defect

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B2_unknown_pass_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_pass_no_job_carries_is_said_and_never_read_as_no_playlists`

Old text:

```
        if not batch_name.pass_jobs(cfg, pass_name):
```

New text:

```
        if False:
```

### `u172.B3_pass_ignored`

signals: never read the pass's playlists

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B3_pass_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_pass_no_job_carries_is_said_and_never_read_as_no_playlists`
  - `tests/test_tag_guess.py::test_a_pass_that_cannot_be_read_is_said_and_the_artist_still_votes`
  - `tests/test_tag_guess.py::test_the_pass_names_the_playlists_that_vote`

Old text:

```
    if pass_name:
        playlists, playlists_unread
```

New text:

```
    if False:
        playlists, playlists_unread
```

### `u172.B4_outcome_ok_always`

tag_guess: answer OK when nothing was written

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B4_outcome_ok_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_that_will_not_take_its_genre_is_never_reported_guessed`
  - `tests/test_tag_guess.py::test_a_folder_that_needs_no_guess_opens_no_library`
  - `tests/test_tag_guess.py::test_a_report_writes_nothing_and_says_what_a_run_would`
  - `tests/test_tag_guess.py::test_no_pass_reads_no_playlist`

Old text:

```
        outcome=Outcome.OK if written else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u172.B5_missing_folder_walked`

tag_guess: drop the refusal of a folder that is not there

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B5_missing_folder_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_folder_that_is_not_there_refuses`

Old text:

```
    if not root.is_dir():
```

New text:

```
    if False:
```

