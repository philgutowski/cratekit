# Mutation table: u334-replay-before-1

Measured by `scripts/mutate.py` on 2026-11-24 03:55 UTC, branch `HEAD` at `ba9492d2`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 298.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 03:55 UTC for commit `ba9492d22626`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 35, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u173.M10_gate_abort` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u173.M12_job_verb` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 2 | killed |
| `u173.M13_output_flag_after_verb` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u173.M14_scope_value` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u173.M15_postcheck_scope_dropped` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u173.M1_mode_dynamic` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 3 | killed |
| `u173.M2_vocal_on` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 2 | killed |
| `u173.M3_key_off` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 3 | killed |
| `u173.M4_precision_row_dropped` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 3 | killed |
| `u173.M5_wrong_playlist` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u173.M6_agent_name` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u173.M7_waiting_code` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u173.M8_suspect_code` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u173.M9_precheck_code` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u319.M1_ok_on_a_suspect_check` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u319.M3_radar_value` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u319.M4_auto_wait_counts_the_batch` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u319.M5_cancel_becomes_ok` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 2 | killed |
| `u319.M6_restart_at_step_two` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u319.M7_key_column_unread` | `.claude/skills/rekordbox-visit/SKILL.md` | user | 1 file(s) | 38 | 1 | killed |
| `u158.M4_shallow_checkout` | `.github/workflows/ci.yml` | maintainer | 1 file(s) | 102 | 1 | killed |
| `u158.M5_head_not_passed` | `.github/workflows/ci.yml` | maintainer | 1 file(s) | 102 | 1 | killed |
| `u158.M6_pull_request_from_previous_tip` | `.github/workflows/ci.yml` | maintainer | 1 file(s) | 102 | 1 | killed |
| `u158.M7_no_base_refuses` | `.github/workflows/ci.yml` | maintainer | 1 file(s) | 102 | 1 | killed |
| `u158.M8_zero_tip_judged` | `.github/workflows/ci.yml` | maintainer | 1 file(s) | 102 | 1 | killed |
| `u251.W2_dist_load` | `pyproject.toml` | maintainer | 3 file(s) | 204 | 2 | killed |
| `u269.M1_lxml_declared_again` | `pyproject.toml` | maintainer | 1 file(s) | 18 | 1 | killed |
| `u269.M2_unused_dependency_by_another_import_name` | `pyproject.toml` | maintainer | 1 file(s) | 18 | 1 | killed |
| `u269.M4_comment_names_the_missing_file` | `pyproject.toml` | maintainer | 1 file(s) | 18 | 1 | killed |
| `u269.M5_comment_names_a_missing_function` | `pyproject.toml` | maintainer | 1 file(s) | 18 | 1 | killed |
| `u269.M6_heavy_dependency_in_the_core` | `pyproject.toml` | maintainer | 1 file(s) | 18 | 1 | killed |
| `u269.M8_comment_names_a_missing_doc` | `pyproject.toml` | maintainer | 1 file(s) | 18 | 1 | killed |
| `u124-b19.B19_audit_reads_folder` | `scripts/board.py` | maintainer | 2 file(s) | 150 | 1 | killed |
| `u124.B10_validate_first` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B11_relanded_title` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 2 | killed |
| `u124.B12_highest_not_count` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 6 | killed |
| `u124.B13_separator` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B14_files_deleted` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 4 | killed |
| `u124.B15_closing_reads_folder` | `scripts/board.py` | maintainer | 2 file(s) | 150 | 3 | killed |
| `u124.B17_land_on_main_only` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B18_behind_origin` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B1_untracked_filter` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B2_readme_excluded` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 2 | killed |
| `u124.B3_name_order` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 3 | killed |
| `u124.B4_fence_open` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 2 | killed |
| `u124.B5_unknown_key` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B6_required_keys` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 6 | killed |
| `u124.B7_issue_values` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B8_numbered_title` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u124.B9_empty_body` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u158.M1_card_not_judged` | `scripts/board.py` | maintainer | 1 file(s) | 102 | 2 | killed |
| `u158.M2_any_branch_names_a_card` | `scripts/board.py` | maintainer | 1 file(s) | 102 | 1 | killed |
| `u158.M3_implied_close_not_a_reference` | `scripts/board.py` | maintainer | 1 file(s) | 102 | 2 | killed |
| `u313.B2_landed_twice` | `scripts/board.py` | maintainer | 2 file(s) | 55 | 2 | killed |
| `u313.B5_owed_unit_closes` | `scripts/board.py` | maintainer | 2 file(s) | 150 | 41 | killed |
| `u313.B6_refusal_exit_code` | `scripts/board.py` | maintainer | 2 file(s) | 55 | 4 | killed |
| `u314.L1_archives_unread` | `scripts/board.py` | maintainer | 3 file(s) | 157 | 7 | killed |
| `u314.L2_landing_never_archives` | `scripts/board.py` | maintainer | 2 file(s) | 55 | 1 | killed |
| `u314.L3_archive_header_undercounted` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 4 | killed |
| `u314.L5_duplicate_heading_passes` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u314.L6_misnamed_archive_passes` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u314.L7_removed_heading_reversed` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u314.L8_unchanged_ignored` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u314.L9_archives_at_rev_unread` | `scripts/board.py` | maintainer | 1 file(s) | 48 | 1 | killed |
| `u328.B1_board_reads_the_registry_alone` | `scripts/board.py` | maintainer | 9 file(s) | 949 | 1 | killed |
| `u328.B2_board_reads_the_parts_alone` | `scripts/board.py` | maintainer | 9 file(s) | 949 | 1 | killed |
| `u330.A4_path_keys_not_skipped` | `scripts/board.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u330.A6_non_units_mapped` | `scripts/board.py` | maintainer | 9 file(s) | 949 | 1 | killed |
| `u59.B1_per_message_split` | `scripts/board.py` | user | 1 file(s) | 102 | 1 | killed |
| `u59.B2_raw_true_on_range` | `scripts/board.py` | user | 1 file(s) | 102 | 1 | killed |
| `u59.B3_unit_mapping_ignored` | `scripts/board.py` | user | 1 file(s) | 102 | 1 | killed |
| `u59.B4_guess_caveat_dropped` | `scripts/board.py` | maintainer | 1 file(s) | 102 | 1 | killed |
| `u59.B6_duplicate_unit_kept` | `scripts/board.py` | maintainer | 1 file(s) | 102 | 2 | killed |
| `u59.B8_missing_file_raises` | `scripts/board.py` | maintainer | 1 file(s) | 102 | 1 | killed |
| `u81-round-2.B5_owed_argument_ignored` | `scripts/board.py` | user | 1 file(s) | 102 | 2 | killed |
| `u81-round-3.B5_audit_drops_the_detector` | `scripts/board.py` | user | 1 file(s) | 102 | 1 | killed |
| `u81-round-3.B5_audit_exit_code` | `scripts/board.py` | user | 1 file(s) | 102 | 1 | killed |
| `u81-round-3.B5_owed_default_dropped` | `scripts/board.py` | user | 1 file(s) | 102 | 2 | killed |
| `u81.B5_composite` | `scripts/board.py` | maintainer | 7 file(s) | 2390 | 1 | killed |
| `u81.B5_contradictions_by_number` | `scripts/board.py` | user | 1 file(s) | 102 | 3 | killed |
| `u81.B5_residual_repoint_dropped` | `scripts/board.py` | user | 1 file(s) | 102 | 1 | killed |
| `u271-measured.B7_boot_unrecorded` | `scripts/cloud_battery.py` | maintainer | 2 file(s) | 201 | 14 | killed |
| `u271-measured.B8_ran_uncounted` | `scripts/cloud_battery.py` | maintainer | 2 file(s) | 201 | 10 | killed |
| `r1917.D1_root_listing_blind` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 3 | killed |
| `r1917.D2_root_check_skipped` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 2 | killed |
| `r1917.D3_kind_not_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `r1917.D4_stand_in_ignored` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 3 | killed |
| `r1917.D5_unreadable_root_accepted` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `r1917.D6_removed_unnamed` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `r343-composites.C2_no_timestamps_no_hash` | `scripts/mutate.py` | user | 1 file(s) | 143 | 1 | killed |
| `r343-composites.C3_path_only` | `scripts/mutate.py` | user | 1 file(s) | 143 | 1 | killed |
| `r343.G10_guard_not_checked_on_timeout` | `scripts/mutate.py` | user | 1 file(s) | 143 | 1 | killed |
| `r343.G1_guard_never_fires` | `scripts/mutate.py` | user | 1 file(s) | 143 | 4 | killed |
| `r343.G4_existence_not_fingerprinted` | `scripts/mutate.py` | user | 1 file(s) | 143 | 1 | killed |
| `r343.G5_row_loop_swallows_the_leak` | `scripts/mutate.py` | user | 1 file(s) | 143 | 2 | killed |
| `r343.G6_run_pytest_skips_the_check` | `scripts/mutate.py` | user | 1 file(s) | 143 | 4 | killed |
| `r343.G7_label_not_carried` | `scripts/mutate.py` | user | 1 file(s) | 143 | 4 | killed |
| `r343.G9_directories_not_fingerprinted` | `scripts/mutate.py` | user | 1 file(s) | 143 | 1 | killed |
| `r343.R1_config_override_ignored` | `scripts/mutate.py` | user | 1 file(s) | 143 | 1 | killed |
| `r343.R2_roots_not_deduplicated` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `r343.S1_no_home_redirect` | `scripts/mutate.py` | user | 1 file(s) | 143 | 2 | killed |
| `r343.S2_no_config_dir_override` | `scripts/mutate.py` | user | 1 file(s) | 143 | 2 | killed |
| `r343.S3_no_state_dir_override` | `scripts/mutate.py` | user | 1 file(s) | 143 | 2 | killed |
| `r343.S4_no_xdg_config_redirect` | `scripts/mutate.py` | user | 1 file(s) | 143 | 2 | killed |
| `u200.M10_driver_unreadable_read_as_complete` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u200.M9_driver_skips_shallow_check` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u251.W5_count_summed_over_workers` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 2 | killed |
| `u268.W10_driver_reads_cut_baseline` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 37 | killed |
| `u271-measured.D10_empty_count_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u271-measured.D11_verdict_disagreement_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 2 | killed |
| `u271-measured.D12_red_record_read_green` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u271-measured.D13_no_known_file_layer` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u271-measured.D14_read_named_measured` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 2 | killed |
| `u271-measured.D15_early_stop_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 2 | killed |
| `u271-measured.D16_edited_run_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u271-measured.D1_commit_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 2 | killed |
| `u271-measured.D2_run_cleanliness_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u271-measured.D3_tree_now_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u271-measured.D4_unreadable_status_read_as_clean` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u271-measured.D5_boot_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u271-measured.D6_checkout_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u271-measured.D7_interpreter_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u271-measured.D8_known_file_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u271-measured.D9_interrupted_run_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u273.D1_driver_placeless_read` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 4 | killed |
| `u273.D2_driver_tmpdir_inherited` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 4 | killed |
| `u273.D3_driver_no_rerun` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 4 | killed |
| `u273.D4_driver_reruns_every_subset` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 4 | killed |
| `u273.D5_driver_place_unchecked_upfront` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 2 | killed |
| `u273.D6_driver_errored_kept` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u273.D7_driver_lost_place_runs_elsewhere` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u273.D8_driver_disk_needed_without_rerun` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u297.D1_replay_row_without_a_source` | `scripts/mutate.py` | user | 1 file(s) | 143 | 1 | killed |
| `u297.D2_cap_lifted_for_every_pass` | `scripts/mutate.py` | user | 1 file(s) | 143 | 3 | killed |
| `u297.D3_mapped_to_no_row` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u297.D4_a_measured_row_loses_its_source` | `scripts/mutate.py` | maintainer | 2 file(s) | 220 | 2 | killed |
| `u297.D5_a_replay_resumed_from_anywhere` | `scripts/mutate.py` | user | 1 file(s) | 143 | 2 | killed |
| `u297.D6_sources_taken_on_trust` | `scripts/mutate.py` | user | 1 file(s) | 143 | 1 | killed |
| `u313.D10_shallow_clone_measured` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u313.D11_red_baseline_measured` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 6 | killed |
| `u313.D12_header_unchecked` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 6 | killed |
| `u313.D13_null_control_ignored` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u313.D14_restore_failure_exit` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u313.D15_invalid_batch_exit` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u313.D1_quiet_flag_kept` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 2 | killed |
| `u313.D2_collect_drift_unread` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 2 | killed |
| `u313.D3_subset_zero_not_promoted` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 3 | killed |
| `u313.D4_bytecode_written` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 9 | killed |
| `u313.D5_node_id_cut_at_space` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u313.D8_dirty_target_measured` | `scripts/mutate.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u313.D6_restore_unverified` | `scripts/mutate_table.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u313.D7_file_not_restored` | `scripts/mutate_table.py` | maintainer | 1 file(s) | 143 | 31 | killed |
| `u313.D9_dirty_status_unread` | `scripts/mutate_table.py` | maintainer | 1 file(s) | 143 | 1 | killed |
| `u296.M13_own_verbs_dangle` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 92 | 5 | killed |
| `u296.M16_prune_adds_lines` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 66 | 5 | killed |
| `u296.M18_vendored_tree_read` | `scripts/refactor_measure.py` | maintainer | 3 file(s) | 123 | 8 | killed |
| `u296.M1_block_size` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 66 | 15 | killed |
| `u296.M8_interface_list_ignored` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 92 | 12 | killed |
| `u331.M01_use_as_written_dropped` | `scripts/refactor_measure.py` | maintainer | 2 file(s) | 92 | 42 | killed |
| `u159.M1_off_main_cut` | `scripts/release.py` | maintainer | 1 file(s) | 45 | 1 | killed |
| `u159.M2_dirty_tree_cut` | `scripts/release.py` | maintainer | 1 file(s) | 45 | 1 | killed |
| `u159.M3_behind_origin_cut` | `scripts/release.py` | maintainer | 1 file(s) | 45 | 2 | killed |
| `u159.M4_red_battery_cut` | `scripts/release.py` | maintainer | 1 file(s) | 45 | 2 | killed |
| `u159.M5_other_commit_verdict` | `scripts/release.py` | maintainer | 1 file(s) | 45 | 1 | killed |
| `u159.M7_unit_is_patch` | `scripts/release.py` | maintainer | 1 file(s) | 45 | 6 | killed |
| `u215.M10_main_sync_re_bare` | `scripts/release.py` | user | 1 file(s) | 45 | 1 | killed |
| `u215.M11_version_at_since` | `scripts/release.py` | user | 1 file(s) | 45 | 1 | killed |
| `u215.M12_crossed_tag` | `scripts/release.py` | user | 1 file(s) | 45 | 2 | killed |
| `u215.M13_crossed_tag_tip_excluded` | `scripts/release.py` | user | 1 file(s) | 45 | 2 | killed |
| `u215.M14_tip_needs_since` | `scripts/release.py` | user | 1 file(s) | 45 | 1 | killed |
| `u215.M15_ref_names_a_commit` | `scripts/release.py` | user | 1 file(s) | 45 | 1 | killed |
| `u215.M16_notes_empty_range` | `scripts/release.py` | user | 1 file(s) | 45 | 1 | killed |
| `u215.M18_reversed_range` | `scripts/release.py` | user | 1 file(s) | 45 | 1 | killed |
| `u215.M19_claim_filter_lands` | `scripts/release.py` | user | 1 file(s) | 45 | 1 | killed |
| `u215.M1_whole_range` | `scripts/release.py` | user | 1 file(s) | 45 | 7 | killed |
| `u215.M2_main_sync_never_lands` | `scripts/release.py` | user | 1 file(s) | 45 | 9 | killed |
| `u215.M3_off_line_landing_subject` | `scripts/release.py` | user | 1 file(s) | 45 | 3 | killed |
| `u215.M4_off_line_any_merge` | `scripts/release.py` | user | 1 file(s) | 45 | 3 | killed |
| `u215.M5_head_in_range` | `scripts/release.py` | user | 1 file(s) | 45 | 1 | killed |
| `u215.M6_landing_taker_first` | `scripts/release.py` | user | 1 file(s) | 45 | 1 | killed |
| `u215.M7_claim_every_landing_taker` | `scripts/release.py` | user | 1 file(s) | 45 | 2 | killed |
| `u215.M8_fast_forward_head` | `scripts/release.py` | user | 1 file(s) | 45 | 1 | killed |
| `u215.M9_landing_re_residual` | `scripts/release.py` | user | 1 file(s) | 45 | 1 | killed |
| `u124.S1_head_fixed` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 209 | 2 | killed |
| `u124.S2_sections` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 209 | 1 | killed |
| `u124.S3_record_opener` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 209 | 1 | killed |
| `u124.S4_wired` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 209 | 5 | killed |
| `u124.S5_only_restart` | `scripts/scan_repo.py` | maintainer | 2 file(s) | 209 | 10 | killed |
| `u257.M2_gate_never_passes` | `scripts/scan_repo.py` | user | 2 file(s) | 175 | 22 | killed |
| `u257.M4_no_quote_landing` | `scripts/scan_repo.py` | user | 2 file(s) | 175 | 20 | killed |
| `u257.M5_no_whitespace_walk` | `scripts/scan_repo.py` | user | 2 file(s) | 175 | 3 | killed |
| `u28-skills-independent.X1_placeholder_exemption` | `scripts/scan_repo.py` | user | 1 file(s) | 161 | 10 | killed |
| `u957.M10_host_lookbehind_hyphen` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 1 | killed |
| `u957.M11_user_at_host_dropped` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 2 | killed |
| `u957.M12_user_at_host_any` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 1 | killed |
| `u957.M13_scp_form_loose` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 3 | killed |
| `u957.M14_list_exemption_off` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 1 | killed |
| `u957.M15_list_exemption_wide` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 1 | killed |
| `u957.M16_cloud_relaxes_declared` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 2 | killed |
| `u957.M17_scheme_read_as_scp` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 1 | killed |
| `u957.M18_method_call_read_as_host` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 1 | killed |
| `u957.M19_occurrences_case_exact` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 22 | killed |
| `u957.M1_declared_wins` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 2 | killed |
| `u957.M20_file_url_read_as_host` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 2 | killed |
| `u957.M21_drive_path_read_as_unc` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 3 | killed |
| `u957.M22_host_end_narrow` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 8 | killed |
| `u957.M2_shape_only_ignored` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 22 | killed |
| `u957.M3_segment_check_dropped` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 5 | killed |
| `u957.M4_segment_case_exact` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 4 | killed |
| `u957.M5_home_segments_not_collected` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 3 | killed |
| `u957.M6_placeholder_segments_collected` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 1 | killed |
| `u957.M7_inner_capital_ignored` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 2 | killed |
| `u957.M8_list_case_exact` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 5 | killed |
| `u957.M9_lan_suffix_dropped` | `scripts/scan_repo.py` | maintainer | 3 file(s) | 213 | 1 | killed |
| `r1313.A1_classifier_failure_alone` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 370 | 7 | killed |
| `r1313.A2_status_before_no_file_landed` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 370 | 2 | killed |
| `r1313.A3_classifier_name_on_any_link` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 370 | 1 | killed |
| `r705-b.S7_acquire_one_softens_the_park_at_the_lookup` | `src/cratekit/acquire/adapter.py` | user | 1 file(s) | 118 | 1 | killed |
| `r705-b.S8_acquire_one_softens_the_park_at_the_fetch` | `src/cratekit/acquire/adapter.py` | user | 1 file(s) | 118 | 1 | killed |
| `u269.M3_only_import_hidden_from_the_tree` | `src/cratekit/acquire/bandcamp.py` | maintainer | 1 file(s) | 18 | 1 | killed |
| `r1115.M1_failed_needs_a_failure` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 1 | killed |
| `r1115.M2_every_failure_for_good` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 5 | killed |
| `r1115.M3_nothing_left_to_run` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 1 | killed |
| `r1115.M4_retryable_is_not_for_good` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 4 | killed |
| `r1115.M5_declined_is_refused` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 8 | killed |
| `r1115.M6_landed_needs_a_track` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 3 | killed |
| `r1115.M7_done_counts_done` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 8 | killed |
| `r1115.M8_failed_names_the_failures` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 2 | killed |
| `r668-a.M11_no_frozen_list_skip` | `src/cratekit/acquire/cli.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u108-c.G25_drive_maps_ending` | `src/cratekit/acquire/cli.py` | user | 7 file(s) | 476 | 31 | killed |
| `u169.A2_any_permanent_declined` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 7 | killed |
| `u169.A3_worker_never_declines` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 9 | killed |
| `u169.A4_no_declined_warning` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 4 | killed |
| `u42-author.W2_unreadable_reported` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 229 | 2 | killed |
| `r679-b.D2_fallback_gate_on_question_alone` | `src/cratekit/acquire/fallback_cli.py` | user | 3 file(s) | 834 | 1 | killed |
| `r1313.I1_cache_failure_alone` | `src/cratekit/acquire/isrc_cache.py` | user | 4 file(s) | 403 | 5 | killed |
| `r1313.I2_cache_keeps_any_status` | `src/cratekit/acquire/isrc_cache.py` | user | 4 file(s) | 403 | 3 | killed |
| `u206-b.M2b_disabled_recall_composite` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1131 | 8 | killed |
| `u206.M11_unreadable_answer_kept` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1131 | 4 | killed |
| `u68.D1_unlisted_on_blank_ref` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 3 | killed |
| `u68.D2_first_id_wins` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 2 | killed |
| `u68.D3_ref_stripped` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 2 | killed |
| `u68.D4_reader_check` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 3 | killed |
| `u68.F1_different_file_refused` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 3 | killed |
| `u68.M1_manifest_version` | `src/cratekit/acquire/listdoc.py` | maintainer | 1 file(s) | 61 | 2 | killed |
| `u68.N1_slash` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 1 | killed |
| `u68.N2_surrounding_space` | `src/cratekit/acquire/listdoc.py` | maintainer | 1 file(s) | 61 | 1 | killed |
| `u68.N3_dot_names` | `src/cratekit/acquire/listdoc.py` | maintainer | 1 file(s) | 61 | 2 | killed |
| `u68.P1_missing_provenance` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 1 | killed |
| `u68.P2_blank_source` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 1 | killed |
| `u68.T1_version_written` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 6 | killed |
| `u68.T2_isrc_written` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 4 | killed |
| `u68.T3_key_written` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 1 | killed |
| `u68.W1_other_service_unlisted` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 1 | killed |
| `u68.W2_raw_title_candidate` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 2 | killed |
| `u73-b.C1_refs_only_when_several` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 1 | killed |
| `u73-b.C2_refs_written` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 2 | killed |
| `u77-c.C1_manifest_version` | `src/cratekit/acquire/listdoc.py` | user | 6 file(s) | 254 | 2 | killed |
| `u77-c.C2_manifest_version_bool` | `src/cratekit/acquire/listdoc.py` | maintainer | 6 file(s) | 254 | 1 | killed |
| `u77-c.C3_not_a_manifest` | `src/cratekit/acquire/listdoc.py` | user | 6 file(s) | 254 | 3 | killed |

## Zero rows and what they owe

- `u330.A4_path_keys_not_skipped` (maintainer facing): maintainer facing, composite not required
- `r668-a.M11_no_frozen_list_skip` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `u173.M10_gate_abort`

skill step 7: the clear's gate answered abort, so the analysed rows are never cleared

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M10_gate_abort`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_each_gate_is_answered_by_its_own_name_and_option_the_adopt_before_the_clear`

Old text:

```
inbox.analyzed.approve apply
```

New text:

```
inbox.analyzed.approve abort
```

### `u173.M12_job_verb`

skill step 1.1: a verb the parser does not know, the lint's rule g

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M12_job_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_lint_reads_the_skills_commands_at_all`
  - `tests/test_rekordbox_visit_skill.py::test_the_skill_passes_the_shipped_skills_lint`

Old text:

```
crate job list --state running
```

New text:

```
crate jobs list --state running
```

### `u173.M13_output_flag_after_verb`

skill step 1.5: the global --output flag after the verb, where the parser refuses it

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M13_output_flag_after_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_skill_passes_the_shipped_skills_lint`

Old text:

```
       crate --output json analyze check
```

New text:

```
       crate analyze check --output json
```

### `u173.M14_scope_value`

skill step 1.5: the scope it must read named inbox, a value the check never writes

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M14_scope_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_json_fields_it_reads_are_the_check_s`

Old text:

```
Read `data.summary.scope` first. It must read `analyze`
```

New text:

```
Read `data.summary.scope` first. It must read `inbox`
```

### `u173.M15_postcheck_scope_dropped`

skill step 7: the post check stops confirming its scope, so a verdict over other rows is read as the visit's

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M15_postcheck_scope_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_json_fields_it_reads_are_the_check_s`

Old text:

```
`data.summary.scope` must still read `analyze`.
```

New text:

```
`data.summary.scope` names the rows it read.
```

### `u173.M1_mode_dynamic`

skill table: Analysis Mode Normal to Dynamic, the setting sitting 47 ran on by mistake

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M1_mode_dynamic`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_dialog_is_read_against_the_one_table_with_no_field_left_unread`
  - `tests/test_rekordbox_visit_skill.py::test_the_settings_agree_with_the_step_crate_sync_land_prints`
  - `tests/test_rekordbox_visit_skill.py::test_the_settings_are_the_brief_s_standard`

Old text:

```
| Analysis Mode | Normal |
```

New text:

```
| Analysis Mode | Dynamic |
```

### `u173.M2_vocal_on`

skill table: Vocal off to on, against the brief's standard

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M2_vocal_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_dialog_is_read_against_the_one_table_with_no_field_left_unread`
  - `tests/test_rekordbox_visit_skill.py::test_the_settings_are_the_brief_s_standard`

Old text:

```
| Vocal | off |
```

New text:

```
| Vocal | on |
```

### `u173.M3_key_off`

skill table: KEY on to off, the other setting sitting 47 met wrong

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M3_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_dialog_is_read_against_the_one_table_with_no_field_left_unread`
  - `tests/test_rekordbox_visit_skill.py::test_the_settings_agree_with_the_step_crate_sync_land_prints`
  - `tests/test_rekordbox_visit_skill.py::test_the_settings_are_the_brief_s_standard`

Old text:

```
| KEY | on |
```

New text:

```
| KEY | off |
```

### `u173.M4_precision_row_dropped`

skill table: the High precision row left out, so the dialog's remembered value stands

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M4_precision_row_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_dialog_is_read_against_the_one_table_with_no_field_left_unread`
  - `tests/test_rekordbox_visit_skill.py::test_the_settings_agree_with_the_step_crate_sync_land_prints`
  - `tests/test_rekordbox_visit_skill.py::test_the_settings_are_the_brief_s_standard`

Old text:

```
| High precision | off |

```

New text:

```
(empty)
```

### `u173.M5_wrong_playlist`

skill step 2: select a playlist named Analyse rather than the one every landing fills

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M5_wrong_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_it_selects_the_playlist_every_landing_fills`

Old text:

```
`Analyze` directly under it.
```

New text:

```
`Analyse` directly under it.
```

### `u173.M6_agent_name`

skill step 6: wait on a process name the agent does not run under, so the agent is never seen

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M6_agent_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_it_waits_on_the_processes_the_product_watches`

Old text:

```
    pgrep -x rekordboxAgent

```

New text:

```
    pgrep -x rekordbox-agent

```

### `u173.M7_waiting_code`

skill step 7: waiting read as exit 30, so a 12 matches no branch

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M7_waiting_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_exit_codes_it_branches_on_are_the_check_s`

Old text:

```
- **12, waiting.**
```

New text:

```
- **30, waiting.**
```

### `u173.M8_suspect_code`

skill step 7: suspect read as exit 12, so a suspect visit reads as rows still waiting

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M8_suspect_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_exit_codes_it_branches_on_are_the_check_s`

Old text:

```
- **27, suspect.**
```

New text:

```
- **12, suspect.**
```

### `u173.M9_precheck_code`

skill step 1.5: the pre check goes on at exit 0, the code for nothing waiting

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u173.json`, row `M9_precheck_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_exit_codes_it_branches_on_are_the_check_s`

Old text:

```
It must exit 12 with
```

New text:

```
It must exit 0 with
```

### `u319.M1_ok_on_a_suspect_check`

skill: OK the dialog on a check that exited 27, whose rows Auto Analysis leaves alone

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u319.json`, row `M1_ok_on_a_suspect_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_ok_only_on_every_field_equal_and_a_waiting_check`

Old text:

```
   - **Every field equal, and the check in step 1.5 exited 12**: write the
```

New text:

```
   - **Every field equal, and the check in step 1.5 exited 12 or 27**: write the
```

### `u319.M3_radar_value`

skill: a field beyond the table read against another value than sitting 101's

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u319.json`, row `M3_radar_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_dialog_is_read_against_the_one_table_with_no_field_left_unread`

Old text:

```
   (BPM range 78 to 155, Cloud Analysis off, Radar Analysis on); any other
```

New text:

```
   (BPM range 78 to 155, Cloud Analysis on, Radar Analysis on); any other
```

### `u319.M4_auto_wait_counts_the_batch`

skill: the Auto Analysis wait counts the batch, which stalls on every analysed row left in the playlist

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u319.json`, row `M4_auto_wait_counts_the_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_auto_analysis_wait_counts_the_rows_not_analysed`

Old text:

```
     step 4 says, with `expected` the `data.summary.not_analysed` count from
     step 1.5, not the batch. Then go to step 5.
```

New text:

```
     step 4 says, with `expected` the batch from step 1.5. Then go to
     step 5.
```

### `u319.M5_cancel_becomes_ok`

skill: a dialog whose fields differ is answered OK, analysing on other fields

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u319.json`, row `M5_cancel_becomes_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_ok_only_on_every_field_equal_and_a_waiting_check`
  - `tests/test_rekordbox_visit_skill.py::test_the_visit_never_changes_the_setting`

Old text:

```
Cancel, never OK, and touch no field of the dialog. Then wait thirty
```

New text:

```
OK, and touch no field of the dialog. Then wait thirty
```

### `u319.M6_restart_at_step_two`

skill: a wrong run restarts at step 2 on a stale check

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u319.json`, row `M6_restart_at_step_two`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_a_wrong_run_restarts_from_the_check`

Old text:

```
and start again from step 1.5, so the check is read again before step 2:
```

New text:

```
and start again from step 2, with the check as it was read before:
```

### `u319.M7_key_column_unread`

skill: done clears rows whose Key column is empty, an Auto run with KEY off

- File: `.claude/skills/rekordbox-visit/SKILL.md`
- Source: `u319.json`, row `M7_key_column_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_done_reads_the_key_column_before_the_clear`

Old text:

```
  read it here: `data.summary.key_filled` must equal
  `data.summary.analysed`.
```

New text:

```
  read it here: `data.summary.key_filled` may be below
  `data.summary.analysed`.
```

### `u158.M4_shallow_checkout`

ci.yml: drop the full history checkout, so the range is the tip alone

- File: `.github/workflows/ci.yml`
- Source: `u158.json`, row `M4_shallow_checkout`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_closing_check_reads_full_history_in_ci`

Old text:

```
        with:
          fetch-depth: 0

```

New text:

```
(empty)
```

### `u158.M5_head_not_passed`

ci.yml: judge a pull request's range without its head, so its merge's close is unread

- File: `.github/workflows/ci.yml`
- Source: `u158.json`, row `M5_head_not_passed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_ci_step_judges_a_pull_request_from_its_base_with_its_head`

Old text:

```
            python scripts/board.py closing --since "$PR_BASE" --pull-request-head "$PR_HEAD_REF"
```

New text:

```
            python scripts/board.py closing --since "$PR_BASE"
```

### `u158.M6_pull_request_from_previous_tip`

ci.yml: judge a pull request from the event's previous tip rather than its base

- File: `.github/workflows/ci.yml`
- Source: `u158.json`, row `M6_pull_request_from_previous_tip`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_ci_step_judges_a_pull_request_from_its_base_with_its_head`

Old text:

```
            python scripts/board.py closing --since "$PR_BASE" --pull-request-head "$PR_HEAD_REF"
```

New text:

```
            python scripts/board.py closing --since "$PUSHED_FROM" --pull-request-head "$PR_HEAD_REF"
```

### `u158.M7_no_base_refuses`

ci.yml: a pull request event with no base sha fails the step instead of saying why

- File: `.github/workflows/ci.yml`
- Source: `u158.json`, row `M7_no_base_refuses`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_pull_request_event_with_no_base_sha_exits_0_and_says_why`

Old text:

```
              echo "pull request event carries no base sha; nothing to judge"
              exit 0
```

New text:

```
              echo "pull request event carries no base sha; nothing to judge"
              exit 1
```

### `u158.M8_zero_tip_judged`

ci.yml: a created ref's all zero previous tip is handed to the check as a range

- File: `.github/workflows/ci.yml`
- Source: `u158.json`, row `M8_zero_tip_judged`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_push_with_no_previous_tip_exits_0_and_says_why[0000000000000000000000000000000000000000]`

Old text:

```
            ""|0000000000000000000000000000000000000000)
```

New text:

```
            "")
```

### `u251.W2_dist_load`

pyproject addopts: name --dist load in its place, the default written out

- File: `pyproject.toml`
- Source: `u251.json`, row `W2_dist_load`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_suite_distribution.py`, `tests/test_mutation_driver.py`, `tests/test_cloud_battery.py`
- Collected: 204 against a baseline of 204
- Kills: 2 (killed)
- Killed:
  - `tests/test_suite_distribution.py::test_the_mutation_driver_passes_the_distribution_on`
  - `tests/test_suite_distribution.py::test_the_suite_runs_on_every_core_and_steals_queued_work`

Old text:

```
addopts = "-q -n auto --dist worksteal"
```

New text:

```
addopts = "-q -n auto --dist load"
```

### `u269.M1_lxml_declared_again`

pyproject.toml: declare lxml in the slim core again, which nothing under src imports

- File: `pyproject.toml`
- Source: `u269.json`, row `M1_lxml_declared_again`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_packaging.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_packaging.py::test_every_core_dependency_is_imported_by_the_package`

Old text:

```
    "rapidfuzz>=3.0",      # three-state match scoring (R11)

```

New text:

```
    "rapidfuzz>=3.0",      # three-state match scoring (R11)
    "lxml>=5.0",           # rekordbox XML parsing

```

### `u269.M2_unused_dependency_by_another_import_name`

pyproject.toml: declare python-dateutil in the core, installed here and imported as dateutil, which nothing under src imports

- File: `pyproject.toml`
- Source: `u269.json`, row `M2_unused_dependency_by_another_import_name`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_packaging.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_packaging.py::test_every_core_dependency_is_imported_by_the_package`

Old text:

```
    "rapidfuzz>=3.0",      # three-state match scoring (R11)

```

New text:

```
    "rapidfuzz>=3.0",      # three-state match scoring (R11)
    "python-dateutil>=2.8",

```

### `u269.M4_comment_names_the_missing_file`

pyproject.toml: the slim core comment names tests/test_slim_core.py again, a file that does not exist

- File: `pyproject.toml`
- Source: `u269.json`, row `M4_comment_names_the_missing_file`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_packaging.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_packaging.py::test_every_path_pyproject_names_exists`

Old text:

```
# tests/test_packaging.py::test_slim_core_carries_no_dsp_web_or_ml_dependency
# fails the build
```

New text:

```
# tests/test_slim_core.py
# fails the build
```

### `u269.M5_comment_names_a_missing_function`

pyproject.toml: the slim core comment names a test function test_packaging.py does not define

- File: `pyproject.toml`
- Source: `u269.json`, row `M5_comment_names_a_missing_function`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_packaging.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_packaging.py::test_every_path_pyproject_names_exists`

Old text:

```
# tests/test_packaging.py::test_slim_core_carries_no_dsp_web_or_ml_dependency
# fails the build
```

New text:

```
# tests/test_packaging.py::test_slim_core_is_slim
# fails the build
```

### `u269.M6_heavy_dependency_in_the_core`

pyproject.toml: declare numpy in the slim core, the existing slim core guard's case

- File: `pyproject.toml`
- Source: `u269.json`, row `M6_heavy_dependency_in_the_core`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_packaging.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_packaging.py::test_slim_core_carries_no_dsp_web_or_ml_dependency`

Old text:

```
    "rapidfuzz>=3.0",      # three-state match scoring (R11)

```

New text:

```
    "rapidfuzz>=3.0",      # three-state match scoring (R11)
    "numpy>=1.24",

```

### `u269.M8_comment_names_a_missing_doc`

pyproject.toml: the slim core comment names docs/dependencies.md, which does not exist, the round one widening of the path guard to docs and vendor

- File: `pyproject.toml`
- Source: `u269.json`, row `M8_comment_names_a_missing_doc`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_packaging.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_packaging.py::test_every_path_pyproject_names_exists`

Old text:

```
# fails the build if one appears. Every line here is also imported somewhere
# under src/cratekit, which
```

New text:

```
# fails the build if one appears (docs/dependencies.md). Every line here is
# also imported somewhere under src/cratekit, which
```

### `u124-b19.B19_audit_reads_folder`

audit stops counting a malformed residual file as a contradiction, rerun after the audit test landed

- File: `scripts/board.py`
- Source: `u124-b19.json`, row `B19_audit_reads_folder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_pending_units.py`
- Collected: 150 against a baseline of 150
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_audit_counts_a_residual_file_that_cannot_land_as_a_contradiction`

Old text:

```
        clashes = clashes + malformed
```

New text:

```
        clashes = clashes
```

### `u124.B10_validate_first`

a malformed file is skipped instead of stopping the landing, so the good ones land

- File: `scripts/board.py`
- Source: `u124.json`, row `B10_validate_first`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_landing_that_cannot_number_every_file_writes_nothing[files1-u1-b.md]`

Old text:

```
    if problems:
        raise ValueError("; ".join(problems))
    if not parsed:
```

New text:

```
    if not parsed:
```

### `u124.B11_relanded_title`

a title the ledger already holds is numbered again

- File: `scripts/board.py`
- Source: `u124.json`, row `B11_relanded_title`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`
  - `tests/test_restart_and_residual_files.py::test_a_landing_that_cannot_number_every_file_writes_nothing[files0-R-12 already]`

Old text:

```
    if again:
        raise ValueError("; ".join(again))
```

New text:

```
(empty)
```

### `u124.B12_highest_not_count`

the next number is the ledger's count plus one rather than its highest plus one

- File: `scripts/board.py`
- Source: `u124.json`, row `B12_highest_not_count`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 6 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`
  - `tests/test_restart_and_residual_files.py::test_an_untracked_draft_is_neither_judged_nor_landed`
  - `tests/test_restart_and_residual_files.py::test_the_landing_refuses_off_main_and_behind_origin`
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order0]`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order1]`

Old text:

```
    number = max(titles, default=0)
```

New text:

```
    number = len(titles)
```

### `u124.B13_separator`

landed entries lose the separator line

- File: `scripts/board.py`
- Source: `u124.json`, row `B13_separator`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`

Old text:

```
        text = text.rstrip("\n") + "\n\n---\n\n"
```

New text:

```
        text = text.rstrip("\n") + "\n\n"
```

### `u124.B14_files_deleted`

a landed file is left in the folder

- File: `scripts/board.py`
- Source: `u124.json`, row `B14_files_deleted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 4 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order0]`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order1]`

Old text:

```
    for path, _, _ in parsed:
        path.unlink()
```

New text:

```
    for path, _, _ in parsed:
        pass
```

### `u124.B15_closing_reads_folder`

closing stops reading the residual folder

- File: `scripts/board.py`
- Source: `u124.json`, row `B15_closing_reads_folder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_pending_units.py`
- Collected: 150 against a baseline of 150
- Kills: 3 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[hook]`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[range]`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[unreadable range]`

Old text:

```
    malformed = residual_file_problems()
    if not problems and not malformed:
```

New text:

```
    malformed = []
    if not problems and not malformed:
```

### `u124.B17_land_on_main_only`

residuals --land runs on any branch

- File: `scripts/board.py`
- Source: `u124.json`, row `B17_land_on_main_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_landing_refuses_off_main_and_behind_origin`

Old text:

```
    if branch != "main":
        print(
            f"board: residuals are numbered on main
```

New text:

```
    if branch == "never":
        print(
            f"board: residuals are numbered on main
```

### `u124.B18_behind_origin`

residuals --land numbers on a main behind origin/main

- File: `scripts/board.py`
- Source: `u124.json`, row `B18_behind_origin`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_landing_refuses_off_main_and_behind_origin`

Old text:

```
    if behind.returncode == 0 and behind.stdout.strip() not in ("", "0"):
```

New text:

```
    if behind.returncode == 0 and behind.stdout.strip() not in ("", "0") and False:
```

### `u124.B1_untracked_filter`

residual_files returns every file, git's index ignored, so an untracked draft is judged and landed

- File: `scripts/board.py`
- Source: `u124.json`, row `B1_untracked_filter`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_an_untracked_draft_is_neither_judged_nor_landed`

Old text:

```
    if listed.returncode != 0:
        return paths

```

New text:

```
    if listed.returncode == 0 or listed.returncode != 0:
        return paths

```

### `u124.B2_readme_excluded`

the README is read as a residual file

- File: `scripts/board.py`
- Source: `u124.json`, row `B2_readme_excluded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`
  - `tests/test_restart_and_residual_files.py::test_the_shipped_residual_folder_holds_only_files_that_can_land`

Old text:

```
    paths = sorted(p for p in folder.glob("*.md") if p.name != "README.md")
```

New text:

```
    paths = sorted(p for p in folder.glob("*.md"))
```

### `u124.B3_name_order`

files land in folder listing order rather than name order

- File: `scripts/board.py`
- Source: `u124.json`, row `B3_name_order`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 3 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_the_number_given_at_landing_is_one_past_the_ledgers_highest`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order0]`
  - `tests/test_restart_and_residual_files.py::test_two_units_built_from_one_base_land_in_either_order[order1]`

Old text:

```
    paths = sorted(p for p in folder.glob("*.md") if p.name != "README.md")
```

New text:

```
    paths = sorted((p for p in folder.glob("*.md") if p.name != "README.md"), reverse=True)
```

### `u124.B4_fence_open`

a file with no opening fence is not refused

- File: `scripts/board.py`
- Source: `u124.json`, row `B4_fence_open`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[**The mechanism.** No frontmatter at all.\n-does not open]`
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[title: T\nfound: today.\n---\n\nBody.\n-does not open]`

Old text:

```
    if not lines or lines[0] != "---":
        raise ValueError("does not open with a frontmatter fence")
```

New text:

```
    if not lines:
        raise ValueError("does not open with a frontmatter fence")
```

### `u124.B5_unknown_key`

an unknown frontmatter key is accepted

- File: `scripts/board.py`
- Source: `u124.json`, row `B5_unknown_key`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\ntitle: T\nfound: today.\nfond: typo\n---\n\nBody.\n-fond]`

Old text:

```
        if key not in RESIDUAL_REQUIRED and key not in RESIDUAL_OPTIONAL:
```

New text:

```
        if key not in RESIDUAL_REQUIRED and key not in RESIDUAL_OPTIONAL and False:
```

### `u124.B6_required_keys`

a missing title or found line is accepted

- File: `scripts/board.py`
- Source: `u124.json`, row `B6_required_keys`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 6 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\nfound: today.\n---\n\nBody.\n-no title]`
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\ntitle: No found line\n---\n\nBody.\n-no found]`
  - `tests/test_restart_and_residual_files.py::test_audit_counts_a_residual_file_that_cannot_land_as_a_contradiction`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[hook]`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[range]`
  - `tests/test_restart_and_residual_files.py::test_closing_refuses_a_landing_whose_residual_file_lacks_its_frontmatter[unreadable range]`

Old text:

```
        if not meta.get(key):
            raise ValueError(f"frontmatter has no {key}")
```

New text:

```
        if key not in meta and False:
            raise ValueError(f"frontmatter has no {key}")
```

### `u124.B7_issue_values`

issue takes any value

- File: `scripts/board.py`
- Source: `u124.json`, row `B7_issue_values`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\ntitle: T\nfound: today.\nissue: maybe\n---\n\nBody.\n-issue]`

Old text:

```
        if key in meta and meta[key] not in allowed:
```

New text:

```
        if key in meta and meta[key] not in allowed and False:
```

### `u124.B8_numbered_title`

the number shape widened back to any leading R number

- File: `scripts/board.py`
- Source: `u124.json`, row `B8_numbered_title`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[text9-None]`

Old text:

```
    if re.match(r"R-\d+\.", meta["title"]):
```

New text:

```
    if re.match(r"R-\d+", meta["title"]):
```

### `u124.B9_empty_body`

a file with frontmatter and no body is accepted

- File: `scripts/board.py`
- Source: `u124.json`, row `B9_empty_body`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_residual_file_the_landing_could_not_read_is_named[---\ntitle: T\nfound: today.\n---\n\n\n-no body]`

Old text:

```
    if not body.strip():
        raise ValueError("has frontmatter and no body")
```

New text:

```
    if body is None:
        raise ValueError("has frontmatter and no body")
```

### `u158.M1_card_not_judged`

cmd_closing: never judge the card a pull request's head names, so an owed unit merges

- File: `scripts/board.py`
- Source: `u158.json`, row `M1_card_not_judged`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_pull_request_range_closing_a_unit_still_owed_is_refused`
  - `tests/test_pending_units.py::test_the_card_a_head_names_is_judged_even_when_the_range_is_unreadable`

Old text:

```
        if card is not None:
```

New text:

```
        if False:
```

### `u158.M2_any_branch_names_a_card`

pull_request_card: read a card off any owner/N-slug branch, not only a cloud one

- File: `scripts/board.py`
- Source: `u158.json`, row `M2_any_branch_names_a_card`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_only_a_cloud_branch_names_the_card_its_merge_closes[feature/36-x-None]`

Old text:

```
CLOUD_BRANCH_RE = re.compile(r"^cloud/(\d+)-")
```

New text:

```
CLOUD_BRANCH_RE = re.compile(r"^\w+/(\d+)-")
```

### `u158.M3_implied_close_not_a_reference`

cmd_closing: write the implied trailer without its hash, so it closes nothing

- File: `scripts/board.py`
- Source: `u158.json`, row `M3_implied_close_not_a_reference`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_pull_request_range_closing_a_unit_still_owed_is_refused`
  - `tests/test_pending_units.py::test_the_card_a_head_names_is_judged_even_when_the_range_is_unreadable`

Old text:

```
            problems += unresolved_closes(f"Closes #{card}", raw=False)
```

New text:

```
            problems += unresolved_closes(f"Closes {card}", raw=False)
```

### `u313.B2_landed_twice`

land_residuals: number a file whose title the ledger already holds, so a file that came back through a conflict lands twice

- File: `scripts/board.py`
- Source: `u313.json`, row `B2_landed_twice`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_board_residual_search.py`
- Collected: 55 against a baseline of 55
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`
  - `tests/test_restart_and_residual_files.py::test_a_landing_that_cannot_number_every_file_writes_nothing[files0-R-12 already]`

Old text:

```
        if meta["title"] in held
```

New text:

```
        if meta["title"] in held and False
```

### `u313.B5_owed_unit_closes`

unresolved_closes: pass a unit a register still owes a module, so a closing trailer closes it early

- File: `scripts/board.py`
- Source: `u313.json`, row `B5_owed_unit_closes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 150 against a baseline of 150
- Kills: 41 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closing_trailer_is_refused_while_a_register_still_owes_that_unit`
  - `tests/test_pending_units.py::test_a_hash_leading_body_line_survives_the_range_check`
  - `tests/test_pending_units.py::test_a_pull_request_range_closing_a_unit_still_owed_is_refused`
  - `tests/test_pending_units.py::test_a_refusal_names_what_the_package_actually_contains`
  - `tests/test_pending_units.py::test_an_issue_number_is_resolved_to_its_unit_when_the_board_says_they_differ`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Close #36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Closed #36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Closes #36, #33]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Closes #36.]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Closes #36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Closes GH-36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Closes: #36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Fix #36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Fixed #36]`
  - `tests/test_pending_units.py::test_every_spelling_github_closes_on_is_refused[Fixes #36]`
  - ... and 26 more, see the JSON sidecar

Old text:

```
        if not modules:
```

New text:

```
        if modules or not modules:
```

### `u313.B6_refusal_exit_code`

_refuse: print the refusal and return 0, so a refused residuals command reads as done

- File: `scripts/board.py`
- Source: `u313.json`, row `B6_refusal_exit_code`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_board_residual_search.py`
- Collected: 55 against a baseline of 55
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_a_missing_ledger_is_refused_never_read_as_no_match`
  - `tests/test_board_residual_search.py::test_the_command_prints_hits_and_refuses_an_empty_search`
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`
  - `tests/test_restart_and_residual_files.py::test_the_landing_refuses_off_main_and_behind_origin`

Old text:

```
    print(f"board: {message}", file=sys.stderr)
    return code
```

New text:

```
    print(f"board: {message}", file=sys.stderr)
    return 0
```

### `u314.L1_archives_unread`

ledger_files: read the working file alone, so search, the highest number and the title check never see an archive

- File: `scripts/board.py`
- Source: `u314.json`, row `L1_archives_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`, `tests/test_restart_and_residual_files.py`, `tests/test_pending_units.py`
- Collected: 157 against a baseline of 157
- Kills: 7 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_a_search_reads_every_archive_and_says_where_each_hit_is`
  - `tests/test_pending_units.py::test_the_residual_heading_reader_reads_the_document_as_it_is_written`
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`
  - `tests/test_restart_and_residual_files.py::test_check_refuses_a_file_over_the_limit_and_archives_that_overlap`
  - `tests/test_restart_and_residual_files.py::test_check_refuses_a_heading_in_two_archives_and_a_misnamed_one`
  - `tests/test_restart_and_residual_files.py::test_the_archive_moves_every_entry_byte_for_byte_and_a_rerun_changes_nothing`

Old text:

```
    return sorted((ledger.parent / "ledger").glob("*.md"), key=first) + [ledger]
```

New text:

```
    return [ledger]
```

### `u314.L2_landing_never_archives`

land_residuals: append without archiving, so the working file grows past the limit

- File: `scripts/board.py`
- Source: `u314.json`, row `L2_landing_never_archives`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_board_residual_search.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`

Old text:

```
    ledger.write_text(text)
    archive_ledger(ledger)
```

New text:

```
    ledger.write_text(text)
```

### `u314.L3_archive_header_undercounted`

archive_ledger: count a two line header where four are written, so an archive can pass the limit

- File: `scripts/board.py`
- Source: `u314.json`, row `L3_archive_header_undercounted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 4 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`
  - `tests/test_restart_and_residual_files.py::test_check_refuses_a_heading_in_two_archives_and_a_misnamed_one`
  - `tests/test_restart_and_residual_files.py::test_the_archive_moves_every_entry_byte_for_byte_and_a_rerun_changes_nothing`
  - `tests/test_restart_and_residual_files.py::test_the_working_file_archives_at_one_line_over_the_limit_and_not_at_it`

Old text:

```
        while last < count - 1 and 4 + len(body(first, last + 1)) <= LEDGER_LIMIT:
```

New text:

```
        while last < count - 1 and 2 + len(body(first, last + 1)) <= LEDGER_LIMIT:
```

### `u314.L5_duplicate_heading_passes`

ledger_problems: never report a heading held by two files

- File: `scripts/board.py`
- Source: `u314.json`, row `L5_duplicate_heading_passes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_check_refuses_a_heading_in_two_archives_and_a_misnamed_one`

Old text:

```
            if number in where:
```

New text:

```
            if False:
```

### `u314.L6_misnamed_archive_passes`

ledger_problems: never compare an archive's name with the range it holds

- File: `scripts/board.py`
- Source: `u314.json`, row `L6_misnamed_archive_passes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_check_refuses_a_heading_in_two_archives_and_a_misnamed_one`

Old text:

```
        if path != ledger and (not numbers or path.name != _archive_name(numbers[0], numbers[-1])):
```

New text:

```
        if path != ledger and not numbers:
```

### `u314.L7_removed_heading_reversed`

ledger_problems: look for headings added since the revision rather than removed, so a removed heading passes

- File: `scripts/board.py`
- Source: `u314.json`, row `L7_removed_heading_reversed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`

Old text:

```
    missing = [f"R-{n}" for n in sorted(set(before) - set(now))]
```

New text:

```
    missing = [f"R-{n}" for n in sorted(set(now) - set(before))]
```

### `u314.L8_unchanged_ignored`

ledger_problems: never report an entry that differs from the revision, so the move's byte comparison passes anything

- File: `scripts/board.py`
- Source: `u314.json`, row `L8_unchanged_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`

Old text:

```
    if unchanged and changed:
```

New text:

```
    if False:
```

### `u314.L9_archives_at_rev_unread`

_ledger_at: read only the working file at the revision, so a heading removed from an archive passes the check against it

- File: `scripts/board.py`
- Source: `u314.json`, row `L9_archives_at_rev_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`

Old text:

```
    for name in [*(n for n in listed.stdout.split() if n.endswith(".md")), ledger.name]:
```

New text:

```
    for name in [ledger.name]:
```

### `u328.B1_board_reads_the_registry_alone`

planned_units: read cli/registry.py and none of its parts, so a planned_in marker in a part owes nothing and a closing trailer passes

- File: `scripts/board.py`
- Source: `u328.json`, row `B1_board_reads_the_registry_alone`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`, `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_residual_search.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`, `tests/test_vocals_cli.py`, `tests/test_adoption.py`
- Collected: 949 against a baseline of 949
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_planned_marker_in_a_part_of_the_registry_is_read`

Old text:

```
    parts = sorted((ROOT / "src" / "cratekit" / "cli").glob("registry*.py"))
```

New text:

```
    parts = sorted((ROOT / "src" / "cratekit" / "cli").glob("registry.py"))
```

### `u328.B2_board_reads_the_parts_alone`

planned_units: read the registry_*.py parts and not cli/registry.py, so its own markers and the constants it defines are lost

- File: `scripts/board.py`
- Source: `u328.json`, row `B2_board_reads_the_parts_alone`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`, `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_residual_search.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`, `tests/test_vocals_cli.py`, `tests/test_adoption.py`
- Collected: 949 against a baseline of 949
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_planned_marker_in_a_part_of_the_registry_is_read`

Old text:

```
    parts = sorted((ROOT / "src" / "cratekit" / "cli").glob("registry*.py"))
```

New text:

```
    parts = sorted((ROOT / "src" / "cratekit" / "cli").glob("registry_*.py"))
```

### `u330.A4_path_keys_not_skipped`

_near_misses: stop skipping path: keys, so a filesystem key is read as a dotted module

- File: `scripts/board.py`
- Source: `u330.json`, row `A4_path_keys_not_skipped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    for module in (m for m in modules if not m.startswith("path:")):
```

New text:

```
    for module in modules:
```

### `u330.A6_non_units_mapped`

units_by_issue_number: map every titled issue, not only units, so a residual titled U-like shadows a unit

- File: `scripts/board.py`
- Source: `u330.json`, row `A6_non_units_mapped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`, `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_residual_search.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`, `tests/test_vocals_cli.py`, `tests/test_adoption.py`
- Collected: 949 against a baseline of 949
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_unit_to_issue_map_is_read_off_the_titles_and_drops_a_duplicate`

Old text:

```
        match = re.match(r"U(\d+)\b", node["title"]) if node["unit"] else None
```

New text:

```
        match = re.match(r"U(\d+)\b", node["title"])
```

### `u59.B1_per_message_split`

Concatenate the range again, manufacturing a trailer across two commits

- File: `scripts/board.py`
- Source: `u59.json`, row `B1_per_message_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closing_reference_is_never_manufactured_across_two_commit_messages`

Old text:

```
            ["git", "log", "--format=%B%x00", f"{args.since}..HEAD"],
```

New text:

```
            ["git", "log", "--format=%B", f"{args.since}..HEAD"],
```

### `u59.B2_raw_true_on_range`

Strip comments on the CI path, which can only delete a real trailer

- File: `scripts/board.py`
- Source: `u59.json`, row `B2_raw_true_on_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_hash_leading_body_line_survives_the_range_check`

Old text:

```
                problems += unresolved_closes(message, raw=False)
```

New text:

```
                problems += unresolved_closes(message, raw=True)
```

### `u59.B3_unit_mapping_ignored`

Ignore the supplied issue-to-unit map, restoring the number conflation

- File: `scripts/board.py`
- Source: `u59.json`, row `B3_unit_mapping_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_an_issue_number_is_resolved_to_its_unit_when_the_board_says_they_differ`

Old text:

```
        uid = reference if units is None else units.get(reference)
```

New text:

```
        uid = reference
```

### `u59.B4_guess_caveat_dropped`

Stop saying the unit number was guessed, so the reader trusts it

- File: `scripts/board.py`
- Source: `u59.json`, row `B4_guess_caveat_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_network_free_path_says_that_it_guessed_the_unit_number`

Old text:

```
        if units is None and reference == uid:
```

New text:

```
        if False:
```

### `u59.B6_duplicate_unit_kept`

Let a duplicated unit number resolve to whichever issue was seen last

- File: `scripts/board.py`
- Source: `u59.json`, row `B6_duplicate_unit_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_register_owing_a_unit_with_no_issue_at_all_is_silence_not_a_crash`
  - `tests/test_pending_units.py::test_the_unit_to_issue_map_is_read_off_the_titles_and_drops_a_duplicate`

Old text:

```
    return {unit: number for unit, number in seen.items() if unit not in duplicated}
```

New text:

```
    return seen
```

### `u59.B8_missing_file_raises`

Let a missing message file raise instead of refusing with a sentence

- File: `scripts/board.py`
- Source: `u59.json`, row `B8_missing_file_raises`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_missing_message_file_refuses_with_a_sentence_not_a_traceback`

Old text:

```
        if not path.is_file():
```

New text:

```
        if False:
```

### `u81-round-2.B5_owed_argument_ignored`

Ignore a supplied register and always read the live one

- File: `scripts/board.py`
- Source: `u81-round-2.json`, row `B5_owed_argument_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closed_unit_a_register_still_owes_is_the_contradiction_the_audit_exits_2_on`
  - `tests/test_pending_units.py::test_the_register_defaults_to_the_live_one_when_no_caller_supplies_it`

Old text:

```
    owed = owed_by_unit() if owed is None else owed
    issues_by_unit = units_by_issue_number(graph)
```

New text:

```
    owed = owed_by_unit()
    issues_by_unit = units_by_issue_number(graph)
```

### `u81-round-3.B5_audit_drops_the_detector`

Have the audit find no contradictions at all, keeping its drift report

- File: `scripts/board.py`
- Source: `u81-round-3.json`, row `B5_audit_drops_the_detector`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`

Old text:

```
    clashes = contradictions(graph)
```

New text:

```
    clashes = []
```

### `u81-round-3.B5_audit_exit_code`

Report a contradiction as exit 1, the code that sends a session to sync

- File: `scripts/board.py`
- Source: `u81-round-3.json`, row `B5_audit_exit_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`

Old text:

```
    return 2 if clashes else 1
```

New text:

```
    return 1
```

### `u81-round-3.B5_owed_default_dropped`

Collapse the no-register default into a falsy test, so an empty register reads as none

- File: `scripts/board.py`
- Source: `u81-round-3.json`, row `B5_owed_default_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`
  - `tests/test_pending_units.py::test_the_register_defaults_to_the_live_one_when_no_caller_supplies_it`

Old text:

```
    owed = owed_by_unit() if owed is None else owed
    issues_by_unit = units_by_issue_number(graph)
```

New text:

```
    owed = owed or {}
    issues_by_unit = units_by_issue_number(graph)
```

### `u81.B5_composite`

What B5 does hold: report a contradiction over an OPEN issue as well

- File: `scripts/board.py`
- Source: `u81.json`, row `B5_composite`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_mutation_driver.py`, `tests/test_pool_sizing.py`, `tests/test_restore.py`
- Collected: 2390 against a baseline of 2390
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closed_unit_a_register_still_owes_is_the_contradiction_the_audit_exits_2_on`

Old text:

```
        if node and node["unit"] and node["closed"]:
```

New text:

```
        if node and node["unit"]:
```

### `u81.B5_contradictions_by_number`

Index the graph by unit number again in contradictions()

- File: `scripts/board.py`
- Source: `u81.json`, row `B5_contradictions_by_number`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 3 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_closed_unit_a_register_still_owes_is_the_contradiction_the_audit_exits_2_on`
  - `tests/test_pending_units.py::test_the_audit_reports_a_contradiction_as_exit_2_and_drift_as_exit_1`
  - `tests/test_pending_units.py::test_the_register_defaults_to_the_live_one_when_no_caller_supplies_it`

Old text:

```
        number = issues_by_unit.get(uid)
        node = graph.get(number) if number is not None else None
```

New text:

```
        node = graph.get(uid)
```

### `u81.B5_residual_repoint_dropped`

Return only the register contradictions, dropping the repointed residuals

- File: `scripts/board.py`
- Source: `u81.json`, row `B5_residual_repoint_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pending_units.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_pending_units.py::test_a_repointed_residual_issue_is_reported_through_the_same_call`

Old text:

```
    return found + repointed_residuals(graph)
```

New text:

```
    return found
```

### `u271-measured.B7_boot_unrecorded`

record_run: record no boot id, which the driver then reads as another machine

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B7_boot_unrecorded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`, `tests/test_mutation_driver.py`
- Collected: 201 against a baseline of 201
- Kills: 14 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_clean_verdict_for_this_commit_stands_for_the_full_baseline_and_says_so`
  - `tests/test_mutation_driver.py::test_a_red_verdict_for_this_commit_refuses_the_batch`
  - `tests/test_mutation_driver.py::test_a_run_that_stopped_early_with_exit_one_is_not_read`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-collection-error-read-clean]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-verdict-its-ids-contradict]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[an-edited-run]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[an-interrupted-run]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-checkout]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-interpreter]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-known-failures-file]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[fewer-ran-than-collected]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[no-count-of-what-ran]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[nothing-collected]`
  - `tests/test_mutation_driver.py::test_the_command_line_reads_the_verdict_and_measures_on_request`

Old text:

```
        "boot_id": boot_id(),
```

New text:

```
        "boot_id": "",
```

### `u271-measured.B8_ran_uncounted`

the reporting plugin: count no test as having reported

- File: `scripts/cloud_battery.py`
- Source: `u271-measured.json`, row `B8_ran_uncounted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cloud_battery.py`, `tests/test_mutation_driver.py`
- Collected: 201 against a baseline of 201
- Kills: 10 (killed)
- Killed:
  - `tests/test_cloud_battery.py::test_a_baseline_header_names_its_place_and_lists_its_tests_on_disk`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[serial]`
  - `tests/test_cloud_battery.py::test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run[workers]`
  - `tests/test_cloud_battery.py::test_each_run_records_every_key_the_driver_reads`
  - `tests/test_mutation_driver.py::test_a_clean_verdict_for_this_commit_stands_for_the_full_baseline_and_says_so`
  - `tests/test_mutation_driver.py::test_a_red_verdict_for_this_commit_refuses_the_batch`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-collection-error-read-clean]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-verdict-its-ids-contradict]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[an-edited-run]`
  - `tests/test_mutation_driver.py::test_the_command_line_reads_the_verdict_and_measures_on_request`

Old text:

```
    _RAN.add(report.nodeid)
```

New text:

```
    pass
```

### `r1917.D1_root_listing_blind`

top_level_entries lists nothing, so every entry added under the filesystem root goes unseen

- File: `scripts/mutate.py`
- Source: `r1917.json`, row `D1_root_listing_blind`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 3 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_name_added_removed_or_retyped_under_the_root_is_a_leak_and_a_deeper_write_is_not`
  - `tests/test_mutation_driver.py::test_an_entry_added_directly_under_the_root_stops_the_batch_at_that_row`
  - `tests/test_mutation_driver.py::test_the_guard_lists_the_filesystem_root_by_default`

Old text:

```
    return tuple(sorted(found))
```

New text:

```
    return ()
```

### `r1917.D2_root_check_skipped`

check_state_guard never compares the root listing, so a child that leaves a folder at the root is not stopped

- File: `scripts/mutate.py`
- Source: `r1917.json`, row `D2_root_check_skipped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_name_added_removed_or_retyped_under_the_root_is_a_leak_and_a_deeper_write_is_not`
  - `tests/test_mutation_driver.py::test_an_entry_added_directly_under_the_root_stops_the_batch_at_that_row`

Old text:

```
    if now_top == guard.top_entries:
        return
```

New text:

```
    if True:
        return
```

### `r1917.D3_kind_not_read`

Every root entry reads as a folder, so a folder replaced by a file of the same name is not a change

- File: `scripts/mutate.py`
- Source: `r1917.json`, row `D3_kind_not_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_name_added_removed_or_retyped_under_the_root_is_a_leak_and_a_deeper_write_is_not`

Old text:

```
                found.append(f"{entry.name}\t{kind}")
```

New text:

```
                found.append(f"{entry.name}\tdir")
```

### `r1917.D4_stand_in_ignored`

take_state_guard lists the real root whatever top it is given, so a stand in is never watched

- File: `scripts/mutate.py`
- Source: `r1917.json`, row `D4_stand_in_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 3 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_name_added_removed_or_retyped_under_the_root_is_a_leak_and_a_deeper_write_is_not`
  - `tests/test_mutation_driver.py::test_a_root_that_cannot_be_listed_refuses_the_batch_rather_than_reading_as_unchanged`
  - `tests/test_mutation_driver.py::test_an_entry_added_directly_under_the_root_stops_the_batch_at_that_row`

Old text:

```
    top = FILESYSTEM_ROOT if top is None else top
```

New text:

```
    top = FILESYSTEM_ROOT
```

### `r1917.D5_unreadable_root_accepted`

A root that cannot be listed is accepted, so two unreadable listings read as unchanged after every child

- File: `scripts/mutate.py`
- Source: `r1917.json`, row `D5_unreadable_root_accepted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_root_that_cannot_be_listed_refuses_the_batch_rather_than_reading_as_unchanged`

Old text:

```
    if entries and entries[0].startswith(UNREADABLE):
```

New text:

```
    if False:
```

### `r1917.D6_removed_unnamed`

A removed root entry is left out of the stop's message, so the halt does not say what went

- File: `scripts/mutate.py`
- Source: `r1917.json`, row `D6_removed_unnamed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_name_added_removed_or_retyped_under_the_root_is_a_leak_and_a_deeper_write_is_not`

Old text:

```
        + [f"removed {name}" for name in sorted(before.keys() - after.keys())]
```

New text:

```
(empty)
```

### `r343-composites.C2_no_timestamps_no_hash`

composite for G8 in r343.md: drop mtime, ctime and the content hash together, leaving path, size and inode; a same size rewrite must now pass unseen, so the test that rewrites in place is the death

- File: `scripts/mutate.py`
- Source: `r343-composites.json`, row `C2_no_timestamps_no_hash`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_any_change_under_the_real_root_is_a_leak`

Old text:

```
                f"\t{info.st_mtime_ns}\t{info.st_ctime_ns}"
            )
            if info.st_size <= SMALL_FILE_BYTES and not os.path.islink(path):
```

New text:

```
                ""
            )
            if False:
```

### `r343-composites.C3_path_only`

composite for G3 in r343.md: drop size, inode, timestamps and the hash, leaving the path alone; only a new or removed entry is seen

- File: `scripts/mutate.py`
- Source: `r343-composites.json`, row `C3_path_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_any_change_under_the_real_root_is_a_leak`

Old text:

```
                f"{relative}\t{info.st_size}\t{info.st_ino}"
                f"\t{info.st_mtime_ns}\t{info.st_ctime_ns}"
            )
            if info.st_size <= SMALL_FILE_BYTES and not os.path.islink(path):
```

New text:

```
                f"{relative}"
            )
            if False:
```

### `r343.G10_guard_not_checked_on_timeout`

the check leaves the finally, so a child that leaks and then hangs is filed as a timeout

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G10_guard_not_checked_on_timeout`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_that_leaks_and_then_hangs_is_still_caught`

Old text:

```
        finally:
            # In a finally, so a child that leaks and then hangs past the
```

New text:

```
        except subprocess.TimeoutExpired:
            raise
        else:
            # In a finally, so a child that leaks and then hangs past the
```

### `r343.G1_guard_never_fires`

check_state_guard treats every digest as unchanged

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G1_guard_never_fires`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 4 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_that_leaks_and_then_hangs_is_still_caught`
  - `tests/test_mutation_driver.py::test_a_leak_during_the_baseline_names_the_phase`
  - `tests/test_mutation_driver.py::test_a_leak_under_a_row_names_that_row_and_stops_the_batch`
  - `tests/test_mutation_driver.py::test_any_change_under_the_real_root_is_a_leak`

Old text:

```
        if now == before:
            continue
```

New text:

```
        if True:
            continue
```

### `r343.G4_existence_not_fingerprinted`

a child that creates the real directory is not a change

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G4_existence_not_fingerprinted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_any_change_under_the_real_root_is_a_leak`

Old text:

```
    entries: list[str] = [f"exists={root.is_dir()}"]
```

New text:

```
    entries: list[str] = ["exists=True"]
```

### `r343.G5_row_loop_swallows_the_leak`

the row loop's StateLeak handler stops re-raising, so the blanket handler files it as an error row and the batch continues

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G5_row_loop_swallows_the_leak`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_leak_under_a_row_names_that_row_and_stops_the_batch`
  - `tests/test_mutation_driver.py::test_an_entry_added_directly_under_the_root_stops_the_batch_at_that_row`

Old text:

```
            # spending children against a machine it had just damaged.
            raise
```

New text:

```
            # spending children against a machine it had just damaged.
            pass
```

### `r343.G6_run_pytest_skips_the_check`

run_pytest never calls check_state_guard

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G6_run_pytest_skips_the_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 4 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_that_leaks_and_then_hangs_is_still_caught`
  - `tests/test_mutation_driver.py::test_a_leak_during_the_baseline_names_the_phase`
  - `tests/test_mutation_driver.py::test_a_leak_under_a_row_names_that_row_and_stops_the_batch`
  - `tests/test_mutation_driver.py::test_an_entry_added_directly_under_the_root_stops_the_batch_at_that_row`

Old text:

```
            if guard is not None:
                check_state_guard(guard, label=label)
```

New text:

```
            if False:
                check_state_guard(guard, label=label)
```

### `r343.G7_label_not_carried`

every leak is reported as a generic child run rather than the row or phase that caused it

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G7_label_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 4 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_that_leaks_and_then_hangs_is_still_caught`
  - `tests/test_mutation_driver.py::test_a_leak_during_the_baseline_names_the_phase`
  - `tests/test_mutation_driver.py::test_a_leak_under_a_row_names_that_row_and_stops_the_batch`
  - `tests/test_mutation_driver.py::test_an_entry_added_directly_under_the_root_stops_the_batch_at_that_row`

Old text:

```
            check_state_guard(guard, label=label)
```

New text:

```
            check_state_guard(guard, label="a child run")
```

### `r343.G9_directories_not_fingerprinted`

a directory created inside the real root is not an entry

- File: `scripts/mutate.py`
- Source: `r343.json`, row `G9_directories_not_fingerprinted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_any_change_under_the_real_root_is_a_leak`

Old text:

```
        for name in dirnames:
            entries.append(f"{(here / name).relative_to(root).as_posix()}\tdir")
```

New text:

```
        for name in ():
            entries.append(f"{(here / name).relative_to(root).as_posix()}\tdir")
```

### `r343.R1_config_override_ignored`

installation_state_roots resolves through platformdirs even when CRATEKIT_CONFIG_DIR is set, so the suite would guard the real machine's directory

- File: `scripts/mutate.py`
- Source: `r343.json`, row `R1_config_override_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_the_guarded_roots_follow_the_overrides_this_process_carries`

Old text:

```
        if config_override
        else Path(platformdirs.user_config_dir(APP_NAME)),
```

New text:

```
        if False
        else Path(platformdirs.user_config_dir(APP_NAME)),
```

### `r343.R2_roots_not_deduplicated`

a config and state directory that agree are walked twice

- File: `scripts/mutate.py`
- Source: `r343.json`, row `R2_roots_not_deduplicated`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_the_guarded_roots_follow_the_overrides_this_process_carries`

Old text:

```
    return tuple(dict.fromkeys(roots))
```

New text:

```
    return tuple(roots)
```

### `r343.S1_no_home_redirect`

the child keeps the caller's HOME, so platformdirs resolves the real config directory

- File: `scripts/mutate.py`
- Source: `r343.json`, row `S1_no_home_redirect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_the_child_starts_in_a_sandbox_and_never_writes_the_callers_config`
  - `tests/test_mutation_driver.py::test_the_sandbox_covers_every_variable_the_conftest_isolates`

Old text:

```
    "HOME": "home",
```

New text:

```
    "HOME_UNSET": "home",
```

### `r343.S2_no_config_dir_override`

the child keeps the caller's CRATEKIT_CONFIG_DIR

- File: `scripts/mutate.py`
- Source: `r343.json`, row `S2_no_config_dir_override`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_the_child_starts_in_a_sandbox_and_never_writes_the_callers_config`
  - `tests/test_mutation_driver.py::test_the_sandbox_covers_every_variable_the_conftest_isolates`

Old text:

```
    "CRATEKIT_CONFIG_DIR": f"config/{APP_NAME}",
```

New text:

```
    "CRATEKIT_CONFIG_DIR_UNSET": f"config/{APP_NAME}",
```

### `r343.S3_no_state_dir_override`

the child keeps the caller's CRATEKIT_STATE_DIR

- File: `scripts/mutate.py`
- Source: `r343.json`, row `S3_no_state_dir_override`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_the_child_starts_in_a_sandbox_and_never_writes_the_callers_config`
  - `tests/test_mutation_driver.py::test_the_sandbox_covers_every_variable_the_conftest_isolates`

Old text:

```
    "CRATEKIT_STATE_DIR": f"state/{APP_NAME}",
```

New text:

```
    "CRATEKIT_STATE_DIR_UNSET": f"state/{APP_NAME}",
```

### `r343.S4_no_xdg_config_redirect`

the child keeps the caller's XDG_CONFIG_HOME; platformdirs ignores XDG on macOS, so this row measures the Linux half of the redirect from a Mac

- File: `scripts/mutate.py`
- Source: `r343.json`, row `S4_no_xdg_config_redirect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_the_child_starts_in_a_sandbox_and_never_writes_the_callers_config`
  - `tests/test_mutation_driver.py::test_the_sandbox_covers_every_variable_the_conftest_isolates`

Old text:

```
    "XDG_CONFIG_HOME": "config",
```

New text:

```
    "XDG_CONFIG_HOME_UNSET": "config",
```

### `u200.M10_driver_unreadable_read_as_complete`

refuse_a_shallow_clone: refuse only an answer of true, so a repository git cannot read passes

- File: `scripts/mutate.py`
- Source: `u200.json`, row `M10_driver_unreadable_read_as_complete`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_known_failures_are_refused_on_a_shallow_clone`

Old text:

```
    if done.returncode != 0 or answer != "false":
```

New text:

```
    if answer == "true":
```

### `u200.M9_driver_skips_shallow_check`

main: subtract known failures without checking the clone is complete

- File: `scripts/mutate.py`
- Source: `u200.json`, row `M9_driver_skips_shallow_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_known_failures_are_refused_on_a_shallow_clone`

Old text:

```
            refuse_a_shallow_clone(args.repo_root)

```

New text:

```
            pass

```

### `u251.W5_count_summed_over_workers`

mutate plugin: add each worker's collection to the count rather than take one, so a parallel run reports every worker's copy

- File: `scripts/mutate.py`
- Source: `u251.json`, row `W5_count_summed_over_workers`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_parallel_workers_measure_what_a_serial_run_does`
  - `tests/test_mutation_driver.py::test_the_count_and_the_failure_survive_a_steal`

Old text:

```
    _STATE["collected"] = len(ids)
```

New text:

```
    _STATE["collected"] += len(ids)
```

### `u268.W10_driver_reads_cut_baseline`

read_known_failures: accept a header that ends history full, a baseline written before U268

- File: `scripts/mutate.py`
- Source: `u268.json`, row `W10_driver_reads_cut_baseline`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 37 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_baseline_red_only_by_the_machines_known_failures_is_green`
  - `tests/test_mutation_driver.py::test_a_clean_verdict_for_this_commit_stands_for_the_full_baseline_and_says_so`
  - `tests/test_mutation_driver.py::test_a_disk_the_rerun_cannot_have_is_refused_before_anything_runs`
  - `tests/test_mutation_driver.py::test_a_known_failure_whose_id_holds_a_space_is_subtracted_whole`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[before-u268]`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[before-u273]`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[no-field]`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[no-place]`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[not-a-place]`
  - `tests/test_mutation_driver.py::test_a_place_this_machine_cannot_give_is_refused_before_anything_runs`
  - `tests/test_mutation_driver.py::test_a_red_verdict_for_this_commit_refuses_the_batch`
  - `tests/test_mutation_driver.py::test_a_run_that_stopped_early_with_exit_one_is_not_read`
  - `tests/test_mutation_driver.py::test_a_status_git_cannot_read_is_never_a_clean_tree`
  - `tests/test_mutation_driver.py::test_a_verdict_for_another_commit_or_over_a_changed_tree_is_not_read`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-collection-error-read-clean]`
  - ... and 22 more, see the JSON sidecar

Old text:

```
    whole = f" {KNOWN_FAILURES_FULL_HISTORY} {KNOWN_FAILURES_WHOLE_IDS}"
```

New text:

```
    whole = f" {KNOWN_FAILURES_FULL_HISTORY}"
```

### `u271-measured.D10_empty_count_read`

read_battery_verdict: accept a record that collected nothing

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D10_empty_count_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[nothing-collected]`

Old text:

```
record["collected"] > 0,
```

New text:

```
record["collected"] >= 0,
```

### `u271-measured.D11_verdict_disagreement_read`

read_battery_verdict: drop the check that the verdict agrees with the ids it lists

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D11_verdict_disagreement_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-collection-error-read-clean]`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[a-verdict-its-ids-contradict]`

Old text:

```
    if green != (record["verdict"] == "clean"):
```

New text:

```
    if False:
```

### `u271-measured.D12_red_record_read_green`

read_battery_verdict: build the read baseline with no failures, so a red verdict reads green

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D12_red_record_read_green`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_red_verdict_for_this_commit_refuses_the_batch`

Old text:

```
        failed=tuple(beyond),
```

New text:

```
        failed=(),
```

### `u271-measured.D13_no_known_file_layer`

read_battery_verdict: drop the refusal of a run with no known failures file, the layer before the digest key

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D13_no_known_file_layer`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_an_unreadable_absent_or_unkeyed_verdict_is_not_read`

Old text:

```
    if not known_digest:
```

New text:

```
    if False:
```

### `u271-measured.D14_read_named_measured`

measure_batch: record a read baseline as measured, so the table names the wrong one

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D14_read_named_measured`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_clean_verdict_for_this_commit_stands_for_the_full_baseline_and_says_so`
  - `tests/test_mutation_driver.py::test_the_command_line_reads_the_verdict_and_measures_on_request`

Old text:

```
        header["baseline_source"] = "read"
```

New text:

```
        header["baseline_source"] = "measured"
```

### `u271-measured.D15_early_stop_read`

read_battery_verdict: drop the check that every collected test reported, so a run stopped early reads complete

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D15_early_stop_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_run_that_stopped_early_with_exit_one_is_not_read`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[fewer-ran-than-collected]`

Old text:

```
record["ran"] == record["collected"],
```

New text:

```
record["ran"] <= record["collected"],
```

### `u271-measured.D16_edited_run_read`

read_battery_verdict: drop the refusal of a run that inherited PYTEST_ADDOPTS

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D16_edited_run_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[an-edited-run]`

Old text:

```
            record.get("pytest_addopts") == "",
```

New text:

```
            True,
```

### `u271-measured.D1_commit_unchecked`

read_battery_verdict: drop the commit key, so a verdict for another commit is read

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D1_commit_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_for_another_commit_or_over_a_changed_tree_is_not_read`
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[no-commit]`

Old text:

```
            bool(commit) and recorded == commit,
```

New text:

```
            True,
```

### `u271-measured.D2_run_cleanliness_unchecked`

read_battery_verdict: drop the key saying the tree was clean throughout the battery's run

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D2_run_cleanliness_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[dirty-during-the-run]`

Old text:

```
        (record.get("clean_tree") is True, "the tree was not clean throughout the battery's run"),
```

New text:

```
        (True, "the tree was not clean throughout the battery's run"),
```

### `u271-measured.D3_tree_now_unchecked`

read_battery_verdict: drop the check that this tree is clean now

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D3_tree_now_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_for_another_commit_or_over_a_changed_tree_is_not_read`

Old text:

```
        (clean_now is True, "this tree has uncommitted or untracked changes"),
```

New text:

```
        (True, "this tree has uncommitted or untracked changes"),
```

### `u271-measured.D4_unreadable_status_read_as_clean`

tree_state in the driver: drop the None for a status git could not read, so an empty failed status reads clean

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D4_unreadable_status_read_as_clean`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_status_git_cannot_read_is_never_a_clean_tree`

Old text:

```
    if not commit or status.returncode != 0:
        return commit, None
```

New text:

```
    if not commit:
        return commit, None
```

### `u271-measured.D5_boot_unchecked`

read_battery_verdict: key the machine on the host name alone, which every cloud container shares

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D5_boot_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-boot]`

Old text:

```
            record.get("host") == socket.gethostname() and record.get("boot_id") == boot_id(),
```

New text:

```
            record.get("host") == socket.gethostname(),
```

### `u271-measured.D6_checkout_unchecked`

read_battery_verdict: drop the checkout key

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D6_checkout_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-checkout]`

Old text:

```
        (record.get("root") == str(repo_root.resolve()), "it was measured in another checkout"),
```

New text:

```
        (True, "it was measured in another checkout"),
```

### `u271-measured.D7_interpreter_unchecked`

read_battery_verdict: drop the interpreter key

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D7_interpreter_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-interpreter]`

Old text:

```
        (record.get("python") == sys.executable, "it was measured with another interpreter"),
```

New text:

```
        (True, "it was measured with another interpreter"),
```

### `u271-measured.D8_known_file_unchecked`

read_battery_verdict: drop the known failures file's digest key

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D8_known_file_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[another-known-failures-file]`

Old text:

```
            record.get("known_failures_sha256") == known_digest,
```

New text:

```
            True,
```

### `u271-measured.D9_interrupted_run_read`

read_battery_verdict: accept pytest's exit 2, an interrupted run

- File: `scripts/mutate.py`
- Source: `u271-measured.json`, row `D9_interrupted_run_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_verdict_that_differs_in_any_key_is_not_read[an-interrupted-run]`

Old text:

```
record["exit_code"] in {0, 1},
```

New text:

```
record["exit_code"] in {0, 1, 2},
```

### `u273.D1_driver_placeless_read`

read_known_failures: read a known failures file that names no place

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D1_driver_placeless_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 4 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[before-u273]`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[no-field]`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[no-place]`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[not-a-place]`

Old text:

```
    if place not in BATTERY.PLACES:
        raise DriverRefusal(
```

New text:

```
    if False:
        raise DriverRefusal(
```

### `u273.D2_driver_tmpdir_inherited`

run_pytest: do not point the child's TMPDIR at the known failures' place

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D2_driver_tmpdir_inherited`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 4 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_batch_in_memory_reads_the_listed_test_on_disk_and_says_so`
  - `tests/test_mutation_driver.py::test_a_child_runs_in_the_known_failures_place_and_the_listed_test_again_on_disk`
  - `tests/test_mutation_driver.py::test_a_listed_test_erroring_in_memory_and_passing_on_disk_is_read_passing`
  - `tests/test_mutation_driver.py::test_a_run_on_disk_runs_once_and_one_with_no_place_inherits_the_temporary_directory`

Old text:

```
            env["TMPDIR"] = str(temp)

```

New text:

```
(empty)
```

### `u273.D3_driver_no_rerun`

run_pytest: never run the listed tests again on disk after a run in memory

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D3_driver_no_rerun`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 4 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_batch_in_memory_reads_the_listed_test_on_disk_and_says_so`
  - `tests/test_mutation_driver.py::test_a_child_runs_in_the_known_failures_place_and_the_listed_test_again_on_disk`
  - `tests/test_mutation_driver.py::test_a_child_whose_place_is_gone_is_refused_rather_than_run_elsewhere`
  - `tests/test_mutation_driver.py::test_a_listed_test_erroring_in_memory_and_passing_on_disk_is_read_passing`

Old text:

```
    rerun = [one for one in on_disk if runs_node(one, paths)] if place == BATTERY.MEMORY else []
```

New text:

```
    rerun = []
```

### `u273.D4_driver_reruns_every_subset`

runs_node: read every listed test as collected by any subset

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D4_driver_reruns_every_subset`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 4 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_listed_test_is_rerun_only_by_a_run_that_collects_it[tests/a.py::t-paths7-False]`
  - `tests/test_mutation_driver.py::test_a_listed_test_is_rerun_only_by_a_run_that_collects_it[tests/a.py::tt-paths9-False]`
  - `tests/test_mutation_driver.py::test_a_listed_test_is_rerun_only_by_a_run_that_collects_it[tests/ab.py::t-paths8-False]`
  - `tests/test_mutation_driver.py::test_a_subset_that_does_not_collect_the_listed_test_runs_nothing_on_disk`

Old text:

```
    if not paths:
        return True
    for path in paths:
```

New text:

```
    if True:
        return True
    for path in paths:
```

### `u273.D5_driver_place_unchecked_upfront`

main: skip the refusal of a place this machine cannot give before the batch starts

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D5_driver_place_unchecked_upfront`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_disk_the_rerun_cannot_have_is_refused_before_anything_runs`
  - `tests/test_mutation_driver.py::test_a_place_this_machine_cannot_give_is_refused_before_anything_runs`

Old text:

```
            refuse_a_place_this_machine_cannot_give(known)
        except DriverRefusal as refusal:
```

New text:

```
            pass
        except DriverRefusal as refusal:
```

### `u273.D6_driver_errored_kept`

run_pytest: keep a listed test's memory error beside its disk outcome

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D6_driver_errored_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_listed_test_erroring_in_memory_and_passing_on_disk_is_read_passing`

Old text:

```
        errored = tuple(i for i in errored if i not in rerun) + again.errored
```

New text:

```
        errored = errored + again.errored
```

### `u273.D7_driver_lost_place_runs_elsewhere`

run_pytest: drop the refusal of a place lost after main's check, so the child runs in the inherited temporary directory

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D7_driver_lost_place_runs_elsewhere`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_child_whose_place_is_gone_is_refused_rather_than_run_elsewhere`

Old text:

```
        root, why = BATTERY.place_root(place)
        if root is None:
            raise DriverRefusal(
```

New text:

```
        root, why = BATTERY.place_root(place)
        if False:
            raise DriverRefusal(
```

### `u273.D8_driver_disk_needed_without_rerun`

refuse_a_place_this_machine_cannot_give: require the disk for every memory file, even one with nothing to run on disk

- File: `scripts/mutate.py`
- Source: `u273.json`, row `D8_driver_disk_needed_without_rerun`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_disk_the_rerun_cannot_have_is_refused_before_anything_runs`

Old text:

```
    if known.place == BATTERY.MEMORY and known.on_disk:
```

New text:

```
    if known.place == BATTERY.MEMORY:
```

### `u297.D1_replay_row_without_a_source`

load_spec: accept a replay row that names no source, so an uncapped pass takes rows no table recorded

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D1_replay_row_without_a_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_replay_row_buys_no_cap_it_cannot_name[no-source]`

Old text:

```
            if source is None:
                raise DriverRefusal(
                    f"row {row_id}: a replay row names where it came from and this one "
```

New text:

```
            if False:
                raise DriverRefusal(
                    f"row {row_id}: a replay row names where it came from and this one "
```

### `u297.D2_cap_lifted_for_every_pass`

load_spec: read the cap as the row count for every pass kind, so a light pass of 26 rows and a full pass of 46 load

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D2_cap_lifted_for_every_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 3 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_replay_row_buys_no_cap_it_cannot_name[full-cap]`
  - `tests/test_mutation_driver.py::test_a_replay_row_buys_no_cap_it_cannot_name[light-cap]`
  - `tests/test_mutation_driver.py::test_a_spec_the_driver_cannot_trust_is_refused[body1-exceeds the light pass cap]`

Old text:

```
    cap = ROW_CAPS.get(pass_kind, len(rows))
```

New text:

```
    cap = len(rows)
```

### `u297.D3_mapped_to_no_row`

load_mapped: accept a mapping whose target is no row in the batch, so a lost kill is covered by nothing

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D3_mapped_to_no_row`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_mapping_nothing_stands_behind_is_refused[entries1-it maps to 'u1.G7', which is no row in this batch]`

Old text:

```
        if target not in ids:
```

New text:

```
        if False:
```

### `u297.D4_a_measured_row_loses_its_source`

measure_row: stop carrying a replay row's source and moved reason into its result, so check has nothing to match the row by

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D4_a_measured_row_loses_its_source`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`, `tests/test_killset.py`
- Collected: 220 against a baseline of 220
- Kills: 2 (killed)
- Killed:
  - `tests/test_killset.py::test_recorded_kills_replay_through_the_driver_and_check_clean`
  - `tests/test_mutation_driver.py::test_a_replay_batch_spends_one_baseline_and_one_control_and_carries_its_sources`

Old text:

```
        head_verified=head_verify,
        **replay_fields(row),
    )
```

New text:

```
        head_verified=head_verify,
    )
```

### `u297.D5_a_replay_resumed_from_anywhere`

measure_batch: let a replay reuse rows from any sidecar, another commit's or one measured before a tracked file changed

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D5_a_replay_resumed_from_anywhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_replay_reuses_nothing_once_the_killing_test_is_gone_committed_or_not`
  - `tests/test_mutation_driver.py::test_resuming_a_replay_from_another_commits_sidecar_says_nothing_is_reused`

Old text:

```
    stale = pass_kind == REPLAY and bool(replay_resume_refusal(repo_root, prior))
```

New text:

```
    stale = False
```

### `u297.D6_sources_taken_on_trust`

main: skip the reading of each replay row's source against the table it names, so new rows ride past the caps under a table's name

- File: `scripts/mutate.py`
- Source: `u297.json`, row `D6_sources_taken_on_trust`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_the_command_checks_the_sources_and_hands_the_mappings_to_the_table`

Old text:

```
        if pass_kind == REPLAY:
            refuse_unrecorded_sources(args.repo_root, rows, mapped)
```

New text:

```
        if False:
            refuse_unrecorded_sources(args.repo_root, rows, mapped)
```

### `u313.D10_shallow_clone_measured`

refuse_a_shallow_clone: accept any answer git gives, so a shallow clone subtracts known failures unread

- File: `scripts/mutate.py`
- Source: `u313.json`, row `D10_shallow_clone_measured`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_known_failures_are_refused_on_a_shallow_clone`

Old text:

```
    if done.returncode != 0 or answer != "false":
```

New text:

```
    if done.returncode != 0:
```

### `u313.D11_red_baseline_measured`

measure_batch: measure rows against a baseline that is not green, so every row reads as a death

- File: `scripts/mutate.py`
- Source: `u313.json`, row `D11_red_baseline_measured`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 6 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_baseline_red_from_a_scrubbed_environment_is_refused_naming_the_count`
  - `tests/test_mutation_driver.py::test_a_baseline_red_only_by_the_machines_known_failures_is_green`
  - `tests/test_mutation_driver.py::test_a_batch_in_memory_reads_the_listed_test_on_disk_and_says_so`
  - `tests/test_mutation_driver.py::test_a_known_failure_whose_id_holds_a_space_is_subtracted_whole`
  - `tests/test_mutation_driver.py::test_a_red_baseline_is_refused_and_the_failures_are_named`
  - `tests/test_mutation_driver.py::test_a_red_verdict_for_this_commit_refuses_the_batch`

Old text:

```
    if not full_baseline.is_green:
```

New text:

```
    if False:
```

### `u313.D12_header_unchecked`

read_known_failures: accept any measured header, so a baseline without full history or whole ids is subtracted

- File: `scripts/mutate.py`
- Source: `u313.json`, row `D12_header_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 6 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[before-u200]`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[before-u268]`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[field-not-last]`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[shallow]`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[whole-field-not-last]`
  - `tests/test_mutation_driver.py::test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command[whole-without-history]`

Old text:

```
    if not (measured and first.endswith(whole)):
```

New text:

```
    if not measured:
```

### `u313.D13_null_control_ignored`

measure_batch: read a null control that killed tests as valid, so a broken environment's deaths are reported as kills

- File: `scripts/mutate.py`
- Source: `u313.json`, row `D13_null_control_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_null_control_that_kills_invalidates_the_whole_batch`

Old text:

```
    if control_result.deaths or control_result.status != "zero":
```

New text:

```
    if control_result.status not in ("zero", "killed"):
```

### `u313.D14_restore_failure_exit`

STOPS: exit a failed restore with the refusal's code 2 instead of 3, so a caller reads a contaminated tree as a refused batch

- File: `scripts/mutate.py`
- Source: `u313.json`, row `D14_restore_failure_exit`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_each_stop_exits_with_its_own_code[RestoreVerificationError-RESTORE FAILED-3]`

Old text:

```
    RestoreVerificationError: ("RESTORE FAILED", 3),
```

New text:

```
    RestoreVerificationError: ("RESTORE FAILED", 2),
```

### `u313.D15_invalid_batch_exit`

main: exit 0 on an invalid batch instead of 4

- File: `scripts/mutate.py`
- Source: `u313.json`, row `D15_invalid_batch_exit`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_each_stop_exits_with_its_own_code[None-INVALID BATCH-4]`

Old text:

```
        print(f"INVALID BATCH: {batch.invalid_reason}", file=sys.stderr)
        return 4
```

New text:

```
        print(f"INVALID BATCH: {batch.invalid_reason}", file=sys.stderr)
        return 0
```

### `u313.D1_quiet_flag_kept`

pytest_addopts: stop stripping -q from pyproject's addopts, so every run is -qq and loses the summary and the collect listing

- File: `scripts/mutate.py`
- Source: `u313.json`, row `D1_quiet_flag_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_addopts_is_stripped_of_quiet_and_nothing_else`
  - `tests/test_mutation_driver.py::test_parallel_workers_measure_what_a_serial_run_does`

Old text:

```
    return " ".join(token for token in tokens if token not in {"-q", "-qq", "--quiet"})
```

New text:

```
    return " ".join(token for token in tokens if token not in {"-qq", "--quiet"})
```

### `u313.D2_collect_drift_unread`

measure_row: never read a changed collected count as drift, so a file that fails to collect reads as a zero or a kill

- File: `scripts/mutate.py`
- Source: `u313.json`, row `D2_collect_drift_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_one_row_kills_is_promoted_breaks_collection_or_is_refused`
  - `tests/test_mutation_driver.py::test_parallel_workers_measure_what_a_serial_run_does`

Old text:

```
    drift = final.collected != reference.collected
```

New text:

```
    drift = False
```

### `u313.D3_subset_zero_not_promoted`

measure_row: report a zero on a subset as a zero without promoting it to the full suite

- File: `scripts/mutate.py`
- Source: `u313.json`, row `D3_subset_zero_not_promoted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 3 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_full_batch_measures_every_row_owes_its_composites_and_restores_the_tree`
  - `tests/test_mutation_driver.py::test_a_zero_row_promoted_on_a_known_red_suite_stays_a_zero`
  - `tests/test_mutation_driver.py::test_one_row_kills_is_promoted_breaks_collection_or_is_refused`

Old text:

```
            if subset is not None and result.deaths == 0 and not result.collect_errors and unbroken:
```

New text:

```
            if False:
```

### `u313.D4_bytecode_written`

run_pytest: let the child write bytecode, so two mutations of one byte length a second apart can run stale bytecode

- File: `scripts/mutate.py`
- Source: `u313.json`, row `D4_bytecode_written`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 9 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_full_batch_measures_every_row_owes_its_composites_and_restores_the_tree`
  - `tests/test_mutation_driver.py::test_a_known_failure_whose_id_holds_a_space_is_subtracted_whole`
  - `tests/test_mutation_driver.py::test_a_resumed_replay_reuses_its_rows_and_they_keep_their_sources`
  - `tests/test_mutation_driver.py::test_a_reused_replay_row_says_where_it_came_from_as_the_row_file_does_now`
  - `tests/test_mutation_driver.py::test_a_verdict_for_another_commit_or_over_a_changed_tree_is_not_read`
  - `tests/test_mutation_driver.py::test_one_row_kills_is_promoted_breaks_collection_or_is_refused`
  - `tests/test_mutation_driver.py::test_parallel_workers_measure_what_a_serial_run_does`
  - `tests/test_mutation_driver.py::test_resuming_a_replay_from_another_commits_sidecar_says_nothing_is_reused`
  - `tests/test_mutation_driver.py::test_the_command_line_reads_the_verdict_and_measures_on_request`

Old text:

```
    env["PYTHONDONTWRITEBYTECODE"] = "1"
```

New text:

```
    env["PYTHONDONTWRITEBYTECODE"] = ""
```

### `u313.D5_node_id_cut_at_space`

the report plugin: keep each failing id only up to its first space, the cut ids the battery stored until U268

- File: `scripts/mutate.py`
- Source: `u313.json`, row `D5_node_id_cut_at_space`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_known_failure_whose_id_holds_a_space_is_subtracted_whole`

Old text:

```
        bucket.append(report.nodeid)
```

New text:

```
        bucket.append(report.nodeid.split(" ")[0])
```

### `u313.D8_dirty_target_measured`

measure_batch: measure a target with uncommitted changes without --allow-dirty, so a restore certifies the wrong bytes

- File: `scripts/mutate.py`
- Source: `u313.json`, row `D8_dirty_target_measured`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_an_uncommitted_or_untracked_target_is_refused`

Old text:

```
    if dirty and not allow_dirty:
```

New text:

```
    if False:
```

### `u313.D6_restore_unverified`

verify_restore: accept any bytes on disk after a restore, so a contaminated file certifies itself

- File: `scripts/mutate_table.py`
- Source: `u313.json`, row `D6_restore_unverified`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_restore_is_verified_against_head_not_against_its_snapshot`

Old text:

```
    if on_disk != committed:
```

New text:

```
    if False:
```

### `u313.D7_file_not_restored`

mutated: leave the mutant on disk after the row instead of writing the snapshot back

- File: `scripts/mutate_table.py`
- Source: `u313.json`, row `D7_file_not_restored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 31 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_a_baseline_red_only_by_the_machines_known_failures_is_green`
  - `tests/test_mutation_driver.py::test_a_batch_in_memory_reads_the_listed_test_on_disk_and_says_so`
  - `tests/test_mutation_driver.py::test_a_capped_pass_writes_the_sidecar_and_dropped_rows_it_always_wrote`
  - `tests/test_mutation_driver.py::test_a_clean_verdict_for_this_commit_stands_for_the_full_baseline_and_says_so`
  - `tests/test_mutation_driver.py::test_a_full_batch_measures_every_row_owes_its_composites_and_restores_the_tree`
  - `tests/test_mutation_driver.py::test_a_known_failure_whose_id_holds_a_space_is_subtracted_whole`
  - `tests/test_mutation_driver.py::test_a_leak_under_a_row_names_that_row_and_stops_the_batch`
  - `tests/test_mutation_driver.py::test_a_light_pass_still_resumes_across_commits_as_it_always_did`
  - `tests/test_mutation_driver.py::test_a_null_control_that_kills_invalidates_the_whole_batch`
  - `tests/test_mutation_driver.py::test_a_replay_batch_spends_one_baseline_and_one_control_and_carries_its_sources`
  - `tests/test_mutation_driver.py::test_a_replay_resumes_over_untracked_files_but_never_over_an_unreadable_status`
  - `tests/test_mutation_driver.py::test_a_replay_reuses_nothing_once_the_killing_test_is_gone_committed_or_not`
  - `tests/test_mutation_driver.py::test_a_replay_row_that_errors_still_names_its_source`
  - `tests/test_mutation_driver.py::test_a_resumed_replay_reuses_its_rows_and_they_keep_their_sources`
  - `tests/test_mutation_driver.py::test_a_reused_replay_row_says_where_it_came_from_as_the_row_file_does_now`
  - ... and 16 more, see the JSON sidecar

Old text:

```
        path.write_bytes(snapshot)
        if head_verify:
```

New text:

```
        if head_verify:
```

### `u313.D9_dirty_status_unread`

dirty_targets: drop every line git status prints, so no target ever reads as dirty

- File: `scripts/mutate_table.py`
- Source: `u313.json`, row `D9_dirty_status_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_mutation_driver.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_an_uncommitted_or_untracked_target_is_refused`

Old text:

```
        if entry:
            found.append(entry.split(" -> ")[-1])
```

New text:

```
        if not entry:
            found.append(entry.split(" -> ")[-1])
```

### `u296.M13_own_verbs_dangle`

dangling: count the switched off toggle's own verbs, so every gated verb reads as dangling

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M13_own_verbs_dangle`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 92 against a baseline of 92
- Kills: 5 (killed)
- Killed:
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_the_toggles_own_verbs_are_off_and_so_never_dangle`
  - `tests/test_refactor_measure.py::test_imports_prints_the_seam_counts`
  - `tests/test_refactor_measure.py::test_table_fails_when_something_stands_beyond_an_allowance`
  - `tests/test_refactor_measure.py::test_table_prints_points_two_to_five_and_is_clean_on_a_full_allowance`

Old text:

```
            if verb.toggle == toggle:
                continue
```

New text:

```
            if verb.toggle == "":
                continue
```

### `u296.M16_prune_adds_lines`

pruned: keep what is found or allowed, so prune writes newly found lines into an allowance

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M16_prune_adds_lines`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`, `tests/test_refactor_measure.py`
- Collected: 66 against a baseline of 66
- Kills: 5 (killed)
- Killed:
  - `tests/test_duplication.py::test_pruning_keeps_what_is_still_found_and_can_never_add_a_line`
  - `tests/test_refactor_measure.py::test_prune_never_adds_a_line_for_something_newly_found`
  - `tests/test_refactor_measure.py::test_prune_removes_what_is_gone_keeps_the_header_and_touches_no_other_package`
  - `tests/test_refactor_measure.py::test_prune_still_lowers_the_file_of_a_package_that_left_the_tree`
  - `tests/test_refactor_measure.py::test_table_fails_when_something_stands_beyond_an_allowance`

Old text:

```
    return found & allowed
```

New text:

```
    return found | allowed
```

### `u296.M18_vendored_tree_read`

python_files: read the vendored tree, which is never refactored and never measured

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M18_vendored_tree_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`, `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 123 against a baseline of 123
- Kills: 8 (killed)
- Killed:
  - `tests/test_duplication.py::test_no_package_holds_a_copied_block_beyond_its_allowance`
  - `tests/test_refactor_measure.py::test_duplicates_prints_blocks_lines_files_and_window_places`
  - `tests/test_refactor_measure.py::test_duplicates_takes_the_block_size_and_lists_the_longest_first`
  - `tests/test_refactor_measure.py::test_in_a_checkout_the_files_are_the_ones_git_tracks_or_would`
  - `tests/test_refactor_measure.py::test_lines_prints_each_package_the_total_and_the_large_files`
  - `tests/test_refactor_measure.py::test_table_prints_points_two_to_five_and_is_clean_on_a_full_allowance`
  - `tests/test_refactor_measure.py::test_the_renamed_reading_is_printed_only_when_asked_and_matches_changed_names`
  - `tests/test_refactor_measure.py::test_the_vendored_tree_is_never_read`

Old text:

```
        and f"/{VENDOR}/" not in f"/{path}"
```

New text:

```
        and f"/{VENDOR}x/" not in f"/{path}"
```

### `u296.M1_block_size`

BLOCK_LINES: a block needs seven logical lines, so a new copy of exactly six passes the duplication check

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M1_block_size`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`, `tests/test_refactor_measure.py`
- Collected: 66 against a baseline of 66
- Kills: 15 (killed)
- Killed:
  - `tests/test_duplication.py::test_a_block_on_the_allowance_passes_and_a_new_one_beside_it_fails`
  - `tests/test_duplication.py::test_a_copy_inside_one_file_is_found`
  - `tests/test_duplication.py::test_a_copy_of_six_lines_is_found_in_both_packages`
  - `tests/test_duplication.py::test_a_copy_that_was_only_reindented_recommented_and_rewrapped_is_still_found`
  - `tests/test_duplication.py::test_a_deletion_that_brings_two_stretches_together_is_a_new_copy`
  - `tests/test_duplication.py::test_a_longer_copy_is_its_run_of_windows`
  - `tests/test_duplication.py::test_a_third_copy_of_an_allowed_block_in_the_same_package_fails`
  - `tests/test_duplication.py::test_a_window_is_described_by_where_it_stands`
  - `tests/test_duplication.py::test_an_allowance_is_its_own_packages_and_excuses_no_other`
  - `tests/test_duplication.py::test_overlapping_windows_in_one_file_are_two_places`
  - `tests/test_duplication.py::test_the_block_size_is_six_logical_lines`
  - `tests/test_refactor_measure.py::test_duplicates_prints_blocks_lines_files_and_window_places`
  - `tests/test_refactor_measure.py::test_prune_removes_what_is_gone_keeps_the_header_and_touches_no_other_package`
  - `tests/test_refactor_measure.py::test_table_prints_points_two_to_five_and_is_clean_on_a_full_allowance`
  - `tests/test_refactor_measure.py::test_the_renamed_reading_is_printed_only_when_asked_and_matches_changed_names`

Old text:

```
BLOCK_LINES = 6
```

New text:

```
BLOCK_LINES = 7
```

### `u296.M8_interface_list_ignored`

off_interface: treat every core module as off the list, so the named interface allows nothing

- File: `scripts/refactor_measure.py`
- Source: `u296.json`, row `M8_interface_list_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_refactor_measure.py`
- Collected: 92 against a baseline of 92
- Kills: 12 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_core_module_off_the_list_fails_from_a_feature_package`
  - `tests/test_import_rules.py::test_a_function_that_imports_its_module_when_called_is_not_that_module`
  - `tests/test_import_rules.py::test_a_module_handed_over_by_a_listed_one_is_a_reach_of_that_module`
  - `tests/test_import_rules.py::test_a_module_handed_over_twice_is_followed_to_the_module_it_is`
  - `tests/test_import_rules.py::test_a_module_on_the_list_passes_from_a_feature_package`
  - `tests/test_import_rules.py::test_a_module_passed_on_by_name_through_a_third_module_is_followed_to_it`
  - `tests/test_import_rules.py::test_a_name_a_listed_module_re_exports_is_reached_through_the_list`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_the_module_an_import_names_is_still_reached_when_the_name_is_a_module`
  - `tests/test_refactor_measure.py::test_imports_prints_the_seam_counts`
  - `tests/test_refactor_measure.py::test_table_fails_when_something_stands_beyond_an_allowance`
  - `tests/test_refactor_measure.py::test_table_prints_points_two_to_five_and_is_clean_on_a_full_allowance`

Old text:

```
        if module in named:
            continue
```

New text:

```
        if module in ():
            continue
```

### `u331.M01_use_as_written_dropped`

Tree._followed: drop the use as written, so a name that is a module reads only as the module it leads to, and an off interface import, a top level import of a toggleable package and a private name each read clean

- File: `scripts/refactor_measure.py`
- Source: `u331.json`, row `M01_use_as_written_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_refactor_measure.py`, `tests/test_import_rules.py`
- Collected: 92 against a baseline of 92
- Kills: 42 (killed)
- Killed:
  - `tests/test_import_rules.py::test_a_core_module_off_the_list_fails_from_a_feature_package`
  - `tests/test_import_rules.py::test_a_core_verb_whose_module_imports_a_toggled_off_package_dangles`
  - `tests/test_import_rules.py::test_a_dotted_import_under_another_name_is_followed_to_its_module`
  - `tests/test_import_rules.py::test_a_function_that_imports_its_module_when_called_is_not_that_module`
  - `tests/test_import_rules.py::test_a_home_imported_directly_in_the_builder_dangles_the_verb`
  - `tests/test_import_rules.py::test_a_lazy_private_import_across_packages_still_fails`
  - `tests/test_import_rules.py::test_a_lazy_reach_off_the_list_still_fails`
  - `tests/test_import_rules.py::test_a_local_variable_named_as_an_imported_module_is_not_a_use_of_it`
  - `tests/test_import_rules.py::test_a_module_handed_over_by_a_listed_one_is_a_reach_of_that_module`
  - `tests/test_import_rules.py::test_a_module_handed_over_twice_is_followed_to_the_module_it_is`
  - `tests/test_import_rules.py::test_a_module_that_answers_for_any_name_has_every_attribute_counted`
  - `tests/test_import_rules.py::test_a_name_a_listed_module_re_exports_is_reached_through_the_list`
  - `tests/test_import_rules.py::test_a_name_bound_in_an_except_branch_is_a_name_the_module_defines`
  - `tests/test_import_rules.py::test_a_name_imported_from_the_core_package_itself_is_a_core_name`
  - `tests/test_import_rules.py::test_a_package_initializer_is_loaded_with_any_module_inside_it`
  - ... and 27 more, see the JSON sidecar

Old text:

```
            # The use as written stands: the module it names was reached too.
            out.append(use)

```

New text:

```
            # The use as written stands: the module it names was reached too.

```

### `u159.M1_off_main_cut`

refusals: drop the refusal off main, so a release is cut from a branch

- File: `scripts/release.py`
- Source: `u159.json`, row `M1_off_main_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_cut_refuses_an_unsafe_checkout[<lambda>-{head} clean-not main]`

Old text:

```
    if branch != "main":
```

New text:

```
    if False:
```

### `u159.M2_dirty_tree_cut`

refusals: drop the clean tree refusal, so uncommitted work rides into a release

- File: `scripts/release.py`
- Source: `u159.json`, row `M2_dirty_tree_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_cut_refuses_an_unsafe_checkout[<lambda>-{head} clean-not clean]`

Old text:

```
    if git(runner, "status", "--porcelain"):
```

New text:

```
    if False:
```

### `u159.M3_behind_origin_cut`

refusals: drop the origin/main equality, so a stale or unpushed main is released

- File: `scripts/release.py`
- Source: `u159.json`, row `M3_behind_origin_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_release.py::test_cut_refuses_an_unsafe_checkout[<lambda>-{head} clean-origin/main]`
  - `tests/test_release.py::test_cut_refuses_an_unsafe_checkout[_behind-{head} clean-origin/main]`

Old text:

```
    elif remote.stdout.strip() != head:
```

New text:

```
    elif False:
```

### `u159.M4_red_battery_cut`

verdict_problem: accept a red verdict

- File: `scripts/release.py`
- Source: `u159.json`, row `M4_red_battery_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_release.py::test_cut_refuses_an_unsafe_checkout[None-{head} dirty-battery is dirty]`
  - `tests/test_release.py::test_cut_refuses_an_unsafe_checkout[None-{head} red-battery is red]`

Old text:

```
    if fields[1] != "clean":
```

New text:

```
    if False:
```

### `u159.M5_other_commit_verdict`

verdict_problem: accept a verdict measured on another commit

- File: `scripts/release.py`
- Source: `u159.json`, row `M5_other_commit_verdict`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_cut_refuses_an_unsafe_checkout[None-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa clean-another commit]`

Old text:

```
    if len(fields) < 2 or fields[0] != head:
```

New text:

```
    if len(fields) < 2:
```

### `u159.M7_unit_is_patch`

classify: a unit asks for a patch, so new behaviour ships as a repair

- File: `scripts/release.py`
- Source: `u159.json`, row `M7_unit_is_patch`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 6 (killed)
- Killed:
  - `tests/test_release.py::test_plan_reruns_a_past_range_and_prints_its_notes`
  - `tests/test_release.py::test_the_bump_a_title_asks_for[U158: a unit reaches main through a pull request-minor]`
  - `tests/test_release.py::test_the_bump_a_title_asks_for[merge(u57): the converge verb-minor]`
  - `tests/test_release.py::test_the_bump_a_title_asks_for[merge(u99-b): label registry verbs-minor]`
  - `tests/test_release.py::test_the_proposal_is_the_largest_bump_and_versions_are_read_and_bumped`
  - `tests/test_release.py::test_unit_and_residual_merges_behind_a_local_merge_of_main_are_all_listed`

Old text:

```
        return "minor", "a unit, new verbs or behaviour"
```

New text:

```
        return "patch", "a unit, new verbs or behaviour"
```

### `u215.M10_main_sync_re_bare`

MAIN_SYNC_RE: drop the bare Merge origin/main alternative

- File: `scripts/release.py`
- Source: `u215.json`, row `M10_main_sync_re_bare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_a_local_merge_of_main_is_never_a_landing[Merge origin/main]`

Old text:

```
    r"|(?:[\w.-]+/)?main)(?: into main)?$"
```

New text:

```
    r")(?: into main)?$"
```

### `u215.M11_version_at_since`

cmd_plan: read the base version from the checkout, not from --since, round one's second BLOCKING finding

- File: `scripts/release.py`
- Source: `u215.json`, row `M11_version_at_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_plan_reads_the_bump_from_the_version_the_range_starts_at`

Old text:

```
        current = version_at(runner, asked_since)

```

New text:

```
        current = read_versions(ROOT)[0]

```

### `u215.M12_crossed_tag`

cmd_plan: drop the refusal of a range crossing a version tag

- File: `scripts/release.py`
- Source: `u215.json`, row `M12_crossed_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_release.py::test_plan_reads_the_bump_from_the_version_the_range_starts_at`
  - `tests/test_release.py::test_plan_refuses_what_it_cannot_plan_or_print`

Old text:

```
        tip_tag = refuse_a_crossed_tag(runner, asked_since, tip)

```

New text:

```
        tip_tag = None

```

### `u215.M13_crossed_tag_tip_excluded`

refuse_a_crossed_tag: count the tag at the tip as crossed, so every rerun of a past release is refused

- File: `scripts/release.py`
- Source: `u215.json`, row `M13_crossed_tag_tip_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_release.py::test_plan_reads_the_bump_from_the_version_the_range_starts_at`
  - `tests/test_release.py::test_plan_reruns_a_past_range_and_prints_its_notes`

Old text:

```
        if git(runner, "rev-parse", f"{name}^{{commit}}") != tip_sha:

```

New text:

```
        if True:

```

### `u215.M14_tip_needs_since`

cmd_plan: drop the refusal of --tip without --since

- File: `scripts/release.py`
- Source: `u215.json`, row `M14_tip_needs_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_plan_refuses_what_it_cannot_plan_or_print`

Old text:

```
    if tip and not asked_since:

```

New text:

```
    if False:

```

### `u215.M15_ref_names_a_commit`

gather: drop the check that --since and --tip name commits

- File: `scripts/release.py`
- Source: `u215.json`, row `M15_ref_names_a_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_plan_refuses_what_it_cannot_plan_or_print`

Old text:

```
        if found.returncode != 0:
            raise ReleaseError(f"{ref!r} names no commit here
```

New text:

```
        if False:
            raise ReleaseError(f"{ref!r} names no commit here
```

### `u215.M16_notes_empty_range`

cmd_plan: print notes over an empty range instead of refusing

- File: `scripts/release.py`
- Source: `u215.json`, row `M16_notes_empty_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_plan_refuses_what_it_cannot_plan_or_print`

Old text:

```
    if getattr(args, "notes", False):
        if bump is None:

```

New text:

```
    if getattr(args, "notes", False):
        if False:

```

### `u215.M18_reversed_range`

refuse_a_crossed_tag: drop the refusal of a --since that is not behind --tip, so a reversed range reads as empty

- File: `scripts/release.py`
- Source: `u215.json`, row `M18_reversed_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_plan_refuses_what_it_cannot_plan_or_print`

Old text:

```
    if runner(["git", "merge-base", "--is-ancestor", since, tip]).returncode != 0:

```

New text:

```
    if False:

```

### `u215.M19_claim_filter_lands`

landings_since: claim only landing subject takers, so a second merge on the line under GitHub's default subject is listed again

- File: `scripts/release.py`
- Source: `u215.json`, row `M19_claim_filter_lands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_a_pull_request_merged_through_the_api_behind_a_local_merge_is_listed_once[Merge pull request #2 from o/cloud/2-a]`

Old text:

```
        claimed.update(sha for sha in taking if lands(sha))

```

New text:

```
        claimed.update(sha for sha in taking if LANDING_RE.match(by_sha[sha][0]))

```

### `u215.M1_whole_range`

landings_since: walk only the first parent line, the defect U215 repairs

- File: `scripts/release.py`
- Source: `u215.json`, row `M1_whole_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 7 (killed)
- Killed:
  - `tests/test_release.py::test_a_pull_request_merged_through_the_api_behind_a_local_merge_is_listed_once[Merge pull request #2 from o/cloud/2-a]`
  - `tests/test_release.py::test_a_pull_request_merged_through_the_api_behind_a_local_merge_is_listed_once[None]`
  - `tests/test_release.py::test_a_pull_request_merged_through_the_api_behind_a_local_merge_is_listed_once[merge(u2): merged locally]`
  - `tests/test_release.py::test_a_unit_reachable_through_its_head_and_its_merge_is_listed_once`
  - `tests/test_release.py::test_plan_reruns_a_past_range_and_prints_its_notes`
  - `tests/test_release.py::test_the_notes_list_exactly_the_pull_requests_since_the_last_tag`
  - `tests/test_release.py::test_unit_and_residual_merges_behind_a_local_merge_of_main_are_all_listed`

Old text:

```
    commits = range_commits(runner, since, tip)

```

New text:

```
    commits = range_commits(runner, since, tip, first_parent=True)

```

### `u215.M2_main_sync_never_lands`

lands: drop the refusal of a merge of main into a local main, so a local pull is listed as a landing

- File: `scripts/release.py`
- Source: `u215.json`, row `M2_main_sync_never_lands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 9 (killed)
- Killed:
  - `tests/test_release.py::test_a_local_merge_of_main_is_never_a_landing[Merge branch 'main' of github.com:philgutowski/cratekit]`
  - `tests/test_release.py::test_a_local_merge_of_main_is_never_a_landing[Merge branch 'main' of https://github.com/philgutowski/cratekit]`
  - `tests/test_release.py::test_a_local_merge_of_main_is_never_a_landing[Merge origin/main]`
  - `tests/test_release.py::test_a_local_merge_of_main_is_never_a_landing[Merge remote-tracking branch 'origin/main']`
  - `tests/test_release.py::test_a_pull_request_merged_through_the_api_behind_a_local_merge_is_listed_once[Merge pull request #2 from o/cloud/2-a]`
  - `tests/test_release.py::test_a_pull_request_merged_through_the_api_behind_a_local_merge_is_listed_once[None]`
  - `tests/test_release.py::test_a_pull_request_merged_through_the_api_behind_a_local_merge_is_listed_once[merge(u2): merged locally]`
  - `tests/test_release.py::test_a_unit_reachable_through_its_head_and_its_merge_is_listed_once`
  - `tests/test_release.py::test_unit_and_residual_merges_behind_a_local_merge_of_main_are_all_listed`

Old text:

```
        if MAIN_SYNC_RE.match(subject):
            return False

```

New text:

```
        if False:
            return False

```

### `u215.M3_off_line_landing_subject`

lands: list only first parent merges, so a unit merge behind a local pull is dropped

- File: `scripts/release.py`
- Source: `u215.json`, row `M3_off_line_landing_subject`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 3 (killed)
- Killed:
  - `tests/test_release.py::test_a_unit_reachable_through_its_head_and_its_merge_is_listed_once`
  - `tests/test_release.py::test_plan_reruns_a_past_range_and_prints_its_notes`
  - `tests/test_release.py::test_unit_and_residual_merges_behind_a_local_merge_of_main_are_all_listed`

Old text:

```
        return sha in first_line or bool(LANDING_RE.match(subject))

```

New text:

```
        return sha in first_line

```

### `u215.M4_off_line_any_merge`

lands: list every off line merge, so branch syncs are counted as landings

- File: `scripts/release.py`
- Source: `u215.json`, row `M4_off_line_any_merge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 3 (killed)
- Killed:
  - `tests/test_release.py::test_a_range_with_no_local_merge_lists_what_the_first_parent_line_lists`
  - `tests/test_release.py::test_a_unit_reachable_through_its_head_and_its_merge_is_listed_once`
  - `tests/test_release.py::test_a_unit_shipped_in_the_last_tag_is_not_listed_again_through_a_sibling_sync`

Old text:

```
        return sha in first_line or bool(LANDING_RE.match(subject))

```

New text:

```
        return True

```

### `u215.M5_head_in_range`

landings_since: consult the head's takers whether or not the head is in the range, round one's first BLOCKING finding

- File: `scripts/release.py`
- Source: `u215.json`, row `M5_head_in_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_a_unit_shipped_in_the_last_tag_is_not_listed_again_through_a_sibling_sync`

Old text:

```
            if head_sha in by_sha
            else []

```

New text:

```
            if True
            else []

```

### `u215.M6_landing_taker_first`

landings_since: invert the taker preference, so a branch sync is chosen over the landing merge

- File: `scripts/release.py`
- Source: `u215.json`, row `M6_landing_taker_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_a_unit_reachable_through_its_head_and_its_merge_is_listed_once`

Old text:

```
                key=lambda sha: (not lands(sha), order[sha]),

```

New text:

```
                key=lambda sha: (lands(sha), order[sha]),

```

### `u215.M7_claim_every_landing_taker`

landings_since: claim only the commit a pull request landed at, so a local merge of the same head is listed again

- File: `scripts/release.py`
- Source: `u215.json`, row `M7_claim_every_landing_taker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 2 (killed)
- Killed:
  - `tests/test_release.py::test_a_pull_request_merged_through_the_api_behind_a_local_merge_is_listed_once[Merge pull request #2 from o/cloud/2-a]`
  - `tests/test_release.py::test_a_pull_request_merged_through_the_api_behind_a_local_merge_is_listed_once[merge(u2): merged locally]`

Old text:

```
        claimed.update(sha for sha in taking if lands(sha))

```

New text:

```
        claimed.update(())

```

### `u215.M8_fast_forward_head`

landings_since: drop the fast forward fallback, so a pull request fast forwarded onto main is unlisted

- File: `scripts/release.py`
- Source: `u215.json`, row `M8_fast_forward_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_a_pull_request_fast_forwarded_onto_main_lands_at_its_head`

Old text:

```
        elif head_sha in by_sha:
            landed_at = head_sha

```

New text:

```
        elif False:
            landed_at = head_sha

```

### `u215.M9_landing_re_residual`

LANDING_RE: drop the residual alternation, so merge(r-N) behind a local pull is dropped

- File: `scripts/release.py`
- Source: `u215.json`, row `M9_landing_re_residual`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_release.py`
- Collected: 45 against a baseline of 45
- Kills: 1 (killed)
- Killed:
  - `tests/test_release.py::test_unit_and_residual_merges_behind_a_local_merge_of_main_are_all_listed`

Old text:

```
LANDING_RE = re.compile(r"^merge\((?:u\d+|r-?\d+)[a-z0-9-]*\):", re.IGNORECASE)
```

New text:

```
LANDING_RE = re.compile(r"^merge\((?:u\d+)[a-z0-9-]*\):", re.IGNORECASE)
```

### `u124.S1_head_fixed`

the scan stops comparing RESTART's head to the fixed reader's line

- File: `scripts/scan_repo.py`
- Source: `u124.json`, row `S1_head_fixed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_portability.py`
- Collected: 209 against a baseline of 209
- Kills: 2 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-head0]`
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-head1]`

Old text:

```
    if head != RESTART_HEAD:
```

New text:

```
    if head != RESTART_HEAD and False:
```

### `u124.S2_sections`

the scan accepts any section heading

- File: `scripts/scan_repo.py`
- Source: `u124.json`, row `S2_sections`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_portability.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-U999]`

Old text:

```
        if heading not in RESTART_SECTIONS:
```

New text:

```
        if heading not in RESTART_SECTIONS and False:
```

### `u124.S3_record_opener`

the record opener narrowed back to units and residuals marked built or done, so a sitting passes

- File: `scripts/scan_repo.py`
- Source: `u124.json`, row `S3_record_opener`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_portability.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-opens a unit's record1]`

Old text:

```
_UNIT_RECORD = re.compile(r"^\*\*(?:U\d+|R-\d+|A\d+|Sitting \d+)\b", re.M)
```

New text:

```
_UNIT_RECORD = re.compile(r"^\*\*(?:U\d+|R-\d+)(?: with R-\d+)? (?:built|done)\b", re.M)
```

### `u124.S4_wired`

scan_tree stops calling restart_violations

- File: `scripts/scan_repo.py`
- Source: `u124.json`, row `S4_wired`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_portability.py`
- Collected: 209 against a baseline of 209
- Kills: 5 (killed)
- Killed:
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-U999]`
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-head0]`
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-head1]`
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-opens a unit's record0]`
  - `tests/test_restart_and_residual_files.py::test_a_unit_writing_into_the_restart_state_is_refused_by_the_scan[<lambda>-opens a unit's record1]`

Old text:

```
        findings += [f"{relative}: {p}" for p in restart_violations(relative, text)]

```

New text:

```
(empty)
```

### `u124.S5_only_restart`

the restart rule judges every file, so a fragment is refused

- File: `scripts/scan_repo.py`
- Source: `u124.json`, row `S5_only_restart`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_portability.py`
- Collected: 209 against a baseline of 209
- Kills: 10 (killed)
- Killed:
  - `tests/test_portability.py::test_a_declared_word_is_not_looked_for_in_the_word_list_itself`
  - `tests/test_portability.py::test_a_relative_symlink_inside_the_repository_is_allowed`
  - `tests/test_portability.py::test_identity_off_stays_off_for_every_tier`
  - `tests/test_portability.py::test_the_archive_rule_stays_quiet_on_what_is_not_an_archive[ar-prose]`
  - `tests/test_portability.py::test_the_archive_rule_stays_quiet_on_what_is_not_an_archive[bzh-prose]`
  - `tests/test_portability.py::test_the_archive_rule_stays_quiet_on_what_is_not_an_archive[cpio-prose]`
  - `tests/test_portability.py::test_the_archive_rule_stays_quiet_on_what_is_not_an_archive[empty]`
  - `tests/test_portability.py::test_the_archive_rule_stays_quiet_on_what_is_not_an_archive[pk-prose]`
  - `tests/test_portability.py::test_the_repository_itself_is_clean`
  - `tests/test_restart_and_residual_files.py::test_the_restart_state_as_shipped_passes_its_own_scan_and_no_other_file_is_judged`

Old text:

```
    if relative_path != RESTART_FILE:
        return []
```

New text:

```
    if relative_path == "":
        return []
```

### `u257.M2_gate_never_passes`

_keyword_gate_passes: return False always, so the two alternations never scan and every keyword credential is missed

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M2_gate_never_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 175 against a baseline of 175
- Kills: 22 (killed)
- Killed:
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[CLIENTSECRET]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[accessToken]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[access_token]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[apiKey]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[api_key]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[apikey]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[client-secret]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[clientId]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[clientSecret]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[client_id]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[client_secret]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[refreshToken]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[refresh_token]`
  - `tests/test_portability.py::test_credential_shapes_are_caught[api_key = "aB3xQ7zK9mN2pR4tV6wY8cE1gJ5"-credential assignment]`
  - `tests/test_portability.py::test_credential_shapes_are_caught[{"access_token": "aB3xQ7zK9mN2pR4tV6wY8cE1gJ5"}-OAuth token field]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
    for run in _SEPARATOR_RUN.finditer(text):
        separator = run.start()
```

New text:

```
    for run in ():
        separator = run.start()
```

### `u257.M4_no_quote_landing`

_keyword_gate_passes: do not step back over a quote after the keyword, so the JSON form "key": "value" is missed

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M4_no_quote_landing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 175 against a baseline of 175
- Kills: 20 (killed)
- Killed:
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[CLIENTSECRET]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[accessToken]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[access_token]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[apiKey]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[api_key]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[apikey]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[client-secret]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[clientId]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[clientSecret]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[client_id]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[client_secret]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[refreshToken]`
  - `tests/test_portability.py::test_a_credential_key_is_caught_in_every_casing_and_separator[refresh_token]`
  - `tests/test_portability.py::test_credential_shapes_are_caught[{"access_token": "aB3xQ7zK9mN2pR4tV6wY8cE1gJ5"}-OAuth token field]`
  - `tests/test_portability.py::test_credential_shapes_are_caught[{"refresh_token": "aB3xQ7zK9mN2pR4tV6wY8cE1gJ5"}-OAuth token field]`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        ends = (end, end - 1) if end > 0 and text[end - 1] in _QUOTES else (end,)
```

New text:

```
        ends = (end,)
```

### `u257.M5_no_whitespace_walk`

_keyword_gate_passes: do not walk back over whitespace, so key = "value" with a space before the separator is missed

- File: `scripts/scan_repo.py`
- Source: `u257.json`, row `M5_no_whitespace_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_scan_secret_equality.py`, `tests/test_portability.py`
- Collected: 175 against a baseline of 175
- Kills: 3 (killed)
- Killed:
  - `tests/test_portability.py::test_credential_shapes_are_caught[api_key = "aB3xQ7zK9mN2pR4tV6wY8cE1gJ5"-credential assignment]`
  - `tests/test_scan_secret_equality.py::test_the_fast_scan_equals_the_reference_on_generated_texts`
  - `tests/test_scan_secret_equality.py::test_the_fast_scan_equals_the_reference_on_the_planted_corpus`

Old text:

```
        while end > 0 and _SPACE.match(text, end - 1):
```

New text:

```
        while False:
```

### `u28-skills-independent.X1_placeholder_exemption`

the portability scanner stops exempting a placeholder home segment, so a documented path shape is reported

- File: `scripts/scan_repo.py`
- Source: `u28-skills-independent.json`, row `X1_placeholder_exemption`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 161 against a baseline of 161
- Kills: 10 (killed)
- Killed:
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[2b7562b4e9]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[b48f8dc5c5]`
  - `tests/test_portability.py::test_any_home_directory_is_caught_not_just_one`
  - `tests/test_portability.py::test_guard_covers_every_shipped_surface[.github/workflows/other.yml-    run: ls /Users/jdoe/Documents/project\n]`
  - `tests/test_portability.py::test_guard_covers_every_shipped_surface[skills/crate-sync/SKILL.md-Work in /Users/jdoe/Documents/project when running this.\n]`
  - `tests/test_portability.py::test_guard_covers_every_shipped_surface[tests/test_something.py-PATH = "/Users/jdoe/Documents/project"\n]`
  - `tests/test_portability.py::test_placeholder_paths_are_allowed`
  - `tests/test_portability.py::test_the_login_and_home_name_are_relaxed_like_the_hostname`
  - `tests/test_portability.py::test_the_repository_is_clean_on_a_machine_named_by_a_word_it_uses`
  - `tests/test_portability.py::test_the_repository_itself_is_clean`

Old text:

```
    for match in _HOME_DIR.finditer(text):
        segment = match.group(1)
        if _is_placeholder_segment(segment):
            continue
```

New text:

```
    for match in _HOME_DIR.finditer(text):
        segment = match.group(1)
        del segment
```

### `u957.M10_host_lookbehind_hyphen`

_host_forms: let a hyphenated neighbour stand before the host name

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M10_host_lookbehind_hyphen`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[55dd574465]`

Old text:

```
rf"(?<![A-Za-z0-9_-]){name}\.{_HOST_SUFFIXES}
```

New text:

```
rf"(?<![A-Za-z0-9_]){name}\.{_HOST_SUFFIXES}
```

### `u957.M11_user_at_host_dropped`

_host_forms: drop the user@host form

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M11_user_at_host_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[56ff8e48f4]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[5875133bfd]`

Old text:

```
            rf"(?<=[A-Za-z0-9._%+-]@){name}(?![A-Za-z0-9_-])(?!\.[A-Za-z])",

```

New text:

```
(empty)
```

### `u957.M12_user_at_host_any`

_host_forms: take any @ before the name, so a decorator reads as a host

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M12_user_at_host_any`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[1b8f74dd3a]`

Old text:

```
rf"(?<=[A-Za-z0-9._%+-]@){name}
```

New text:

```
rf"(?<=@){name}
```

### `u957.M13_scp_form_loose`

_host_forms: take the name followed by any colon, so a mapping key reads as a host

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M13_scp_form_loose`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 3 (killed)
- Killed:
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[0617a05d01]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[5e2e8b2ab4]`
  - `tests/test_portability.py::test_the_repository_is_clean_on_a_machine_named_by_a_word_it_uses`

Old text:

```
{name}:(?:~|/(?!/))",
```

New text:

```
{name}:",
```

### `u957.M14_list_exemption_off`

scan_tree: look for a declared listed word in the list itself again

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M14_list_exemption_off`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_portability.py::test_a_declared_word_is_not_looked_for_in_the_word_list_itself`

Old text:

```
        if relative == ORDINARY_WORDS_PATH:

```

New text:

```
        if False:

```

### `u957.M15_list_exemption_wide`

scan_tree: skip every token in the list file, so a planted name passes

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M15_list_exemption_wide`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_portability.py::test_a_declared_word_is_not_looked_for_in_the_word_list_itself`

Old text:

```
                (token for token in identity if token.lower() not in listed),

```

New text:

```
                (),

```

### `u957.M16_cloud_relaxes_declared`

machine_identity_tokens: under the cloud exemption mark the declared tokens shape only

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M16_cloud_relaxes_declared`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_portability.py::test_a_cloud_container_relaxes_nothing`
  - `tests/test_portability.py::test_identity_off_stays_off_for_every_tier`

Old text:

```
        return IdentityTokens(declared)

```

New text:

```
        return IdentityTokens(declared, declared)

```

### `u957.M17_scheme_read_as_scp`

_host_forms: let the scp form take a URL scheme, so word:// reads as a host

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M17_scheme_read_as_scp`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[5e2e8b2ab4]`

Old text:

```
{name}:(?:~|/(?!/))",
```

New text:

```
{name}:(?:~|/)",
```

### `u957.M18_method_call_read_as_host`

_host_forms: let a method call such as word.local() read as a host

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M18_method_call_read_as_host`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[d57aa8551e]`

Old text:

```
(?![A-Za-z0-9_(-])",
```

New text:

```
(?![A-Za-z0-9_-])",
```

### `u957.M19_occurrences_case_exact`

_names_the_machine: look for the token's occurrences case exact, so a host written in another case is missed

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M19_occurrences_case_exact`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 22 (killed)
- Killed:
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[001ae12c03]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[0fcc9032b1]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[20677409b1]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[2195b937fd]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[56ff8e48f4]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[5875133bfd]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[64b2033a6b]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[77b5d775f1]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[7e4131f979]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[91df76fbbb]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[b10424d344]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[b749cc6fb5]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[bd599bb03b]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[be891c92b2]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[d93d276f9c]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
        for written in re.finditer(re.escape(token), text, re.IGNORECASE)
```

New text:

```
        for written in re.finditer(re.escape(token), text)
```

### `u957.M1_declared_wins`

machine_identity_tokens: relax a detected ordinary word even when it is also declared

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M1_declared_wins`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_portability.py::test_a_declared_ordinary_word_is_caught_bare`
  - `tests/test_portability.py::test_the_repository_is_clean_on_a_machine_named_by_a_word_it_uses`

Old text:

```
        if is_ordinary_word(token) and token.lower() not in declared_folded

```

New text:

```
        if is_ordinary_word(token)

```

### `u957.M20_file_url_read_as_host`

_host_forms: take any two slashes before the name, so a file:/// path or a path double slash reads as a host

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M20_file_url_read_as_host`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[8fa4993dfd]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[efaccc69a6]`

Old text:

```
(?:(?<=[A-Za-z]://)|(?<=[\s\"'`(<\[]//)|(?<=^//)){name}
```

New text:

```
(?<=//){name}
```

### `u957.M21_drive_path_read_as_unc`

_host_forms: take any two backslashes before the name, so an escaped drive path reads as a UNC host

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M21_drive_path_read_as_unc`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 3 (killed)
- Killed:
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[4fa2328495]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[ad419d3a5a]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[dbb6273c44]`

Old text:

```
(?:(?<=[^:A-Za-z0-9\\]\\\\)|(?<=^\\\\)){name}
```

New text:

```
(?<=\\\\){name}
```

### `u957.M22_host_end_narrow`

_HOST_END: end a share or UNC host only at a colon, slash, space or the end, so a quoted or linked host is missed

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M22_host_end_narrow`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 8 (killed)
- Killed:
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[001ae12c03]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[20677409b1]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[77b5d775f1]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[b749cc6fb5]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[bd599bb03b]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[ff10127047]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[ff13b27ef5]`
  - `tests/test_portability.py::test_a_host_form_opening_the_text_is_caught[bd599bb03b]`

Old text:

```
_HOST_END = r"(?![A-Za-z0-9_-])(?!\.[A-Za-z0-9])"
```

New text:

```
_HOST_END = r"(?=[:/]|\s|$)"
```

### `u957.M2_shape_only_ignored`

portability_violations: never take the shape only branch, so a detected word matches bare again

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M2_shape_only_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 22 (killed)
- Killed:
  - `tests/test_portability.py::test_a_detected_ordinary_word_passes_in_prose`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[0617a05d01]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[1b43b179f7]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[1b8f74dd3a]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[1bf0861883]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[42d8935682]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[4fa2328495]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[55dd574465]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[5e2e8b2ab4]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[8fa4993dfd]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[ad419d3a5a]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[aee8967d34]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[d5509746b3]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[d57aa8551e]`
  - `tests/test_portability.py::test_a_host_form_needs_the_whole_name_and_a_whole_suffix[dbb6273c44]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
        if token in shape_only:

```

New text:

```
        if False:

```

### `u957.M3_segment_check_dropped`

_names_the_machine: drop the home and mount segment check, so a path naming the machine passes

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M3_segment_check_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 5 (killed)
- Killed:
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[2b7562b4e9]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[b48f8dc5c5]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[c170c7484a]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[d10716541a]`
  - `tests/test_portability.py::test_the_login_and_home_name_are_relaxed_like_the_hostname`

Old text:

```
    if token.lower() in segments:
        return True
    host = _host_forms(token)
```

New text:

```
    host = _host_forms(token)
```

### `u957.M4_segment_case_exact`

_names_the_machine: compare the token to the segments case exact

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M4_segment_case_exact`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 4 (killed)
- Killed:
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[2b7562b4e9]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[b48f8dc5c5]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[c170c7484a]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[d10716541a]`

Old text:

```
    if token.lower() in segments:

```

New text:

```
    if token in segments:

```

### `u957.M5_home_segments_not_collected`

portability_violations: collect no home directory segment

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M5_home_segments_not_collected`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 3 (killed)
- Killed:
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[2b7562b4e9]`
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[b48f8dc5c5]`
  - `tests/test_portability.py::test_the_login_and_home_name_are_relaxed_like_the_hostname`

Old text:

```
    for match in _HOME_DIR.finditer(text):
        segment = match.group(1)
        if _is_placeholder_segment(segment):
            continue
        segments.add(segment.lower())

```

New text:

```
    for match in _HOME_DIR.finditer(text):
        segment = match.group(1)
        if _is_placeholder_segment(segment):
            continue

```

### `u957.M6_placeholder_segments_collected`

portability_violations: collect a stand in mount segment, so /Volumes/Music names a machine called Music

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M6_placeholder_segments_collected`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_portability.py::test_a_stand_in_path_segment_is_not_the_machine`

Old text:

```
    for match in _MOUNT.finditer(text):
        segment = match.group(1)
        if _is_placeholder_segment(segment):
            continue
        segments.add(segment.lower())

```

New text:

```
    for match in _MOUNT.finditer(text):
        segment = match.group(1)
        segments.add(segment.lower())
        if _is_placeholder_segment(segment):
            continue

```

### `u957.M7_inner_capital_ignored`

is_ordinary_word: treat a mixed case token like AirPort as the word

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M7_inner_capital_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_portability.py::test_a_capital_inside_a_token_marks_a_name`
  - `tests/test_portability.py::test_the_ordinary_word_list_is_well_formed`

Old text:

```
    if token[1:] != token[1:].lower() and not token.isupper():

```

New text:

```
    if False:

```

### `u957.M8_list_case_exact`

is_ordinary_word: look the token up case exact, so a capitalised hostname is never ordinary

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M8_list_case_exact`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 5 (killed)
- Killed:
  - `tests/test_portability.py::test_a_detected_ordinary_word_passes_in_prose`
  - `tests/test_portability.py::test_a_host_form_matches_under_the_regex_case_rule`
  - `tests/test_portability.py::test_a_stand_in_path_segment_is_not_the_machine`
  - `tests/test_portability.py::test_the_ordinary_word_list_is_well_formed`
  - `tests/test_portability.py::test_the_repository_is_clean_on_a_machine_named_by_a_word_it_uses`

Old text:

```
    return token.lower() in ordinary_words()

```

New text:

```
    return token in ordinary_words()

```

### `u957.M9_lan_suffix_dropped`

_HOST_SUFFIXES: drop lan

- File: `scripts/scan_repo.py`
- Source: `u957.json`, row `M9_lan_suffix_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`, `tests/test_skills_lint.py`, `tests/test_attended_orchestrator_skill.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_portability.py::test_a_detected_ordinary_word_is_caught_where_it_names_the_machine[daebd4dc53]`

Old text:

```
_HOST_SUFFIXES = r"(?:local|lan|localdomain|home\.arpa)"
```

New text:

```
_HOST_SUFFIXES = r"(?:local|localdomain|home\.arpa)"
```

### `r1313.A1_classifier_failure_alone`

classify_unavailable: read the 404 off the failure alone, as before R-1313, so a track answered with a 404 page is retried for ever

- File: `src/cratekit/acquire/adapter.py`
- Source: `r1313.json`, row `A1_classifier_failure_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_vendor_import.py`
- Collected: 370 against a baseline of 370
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-account]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_track_the_provider_answers_with_a_404_page_is_permanent_with_no_retry`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[account]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    if answered_not_found(exc):
        return TrackOutcome.UNAVAILABLE_PERMANENT
```

New text:

```
    if getattr(getattr(exc, "response", None), "status_code", None) == 404:
        return TrackOutcome.UNAVAILABLE_PERMANENT
```

### `r1313.A2_status_before_no_file_landed`

classify_unavailable: ask the nearest status before NoFileLanded, so a download whose swallowed cause was a 404 page quarantines a live track

- File: `src/cratekit/acquire/adapter.py`
- Source: `r1313.json`, row `A2_status_before_no_file_landed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_vendor_import.py`
- Collected: 370 against a baseline of 370
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_transient_marker_wins_over_a_status_code`
  - `tests/test_provider_not_found_bodies.py::test_no_file_landed_carrying_a_404_page_stays_transient`

Old text:

```
    if isinstance(exc, NoFileLanded):
        return TrackOutcome.UNAVAILABLE_TRANSIENT
    text = str(exc).lower()
```

New text:

```
    if answered_not_found(exc):
        return TrackOutcome.UNAVAILABLE_PERMANENT
    if isinstance(exc, NoFileLanded):
        return TrackOutcome.UNAVAILABLE_TRANSIENT
    text = str(exc).lower()
```

### `r1313.A3_classifier_name_on_any_link`

classify_unavailable: read a not found class name on any link the walk reaches, so a name met only as context is read as the provider's answer

- File: `src/cratekit/acquire/adapter.py`
- Source: `r1313.json`, row `A3_classifier_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_vendor_import.py`
- Collected: 370 against a baseline of 370
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_name_reached_only_as_context_is_not_a_not_found`

Old text:

```
    if "notfound" in type(exc).__name__.lower():
        return TrackOutcome.UNAVAILABLE_PERMANENT
    if answered_not_found(exc):
```

New text:

```
    from cratekit.core.cause import failure_links  # noqa: PLC0415

    if any("notfound" in type(one).__name__.lower() for one, _ in failure_links(exc)):
        return TrackOutcome.UNAVAILABLE_PERMANENT
    if answered_not_found(exc):
```

### `r705-b.S7_acquire_one_softens_the_park_at_the_lookup`

a park raised at the offer is one unavailable track and the driver claims the next

- File: `src/cratekit/acquire/adapter.py`
- Source: `r705-b.json`, row `S7_acquire_one_softens_the_park_at_the_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_acquire_one_lets_the_park_through_rather_than_failing_the_track[offer]`

Old text:

```
        offer = source.offer(request)
    except (AdapterAuthFailed, AdapterBroken, Parked):

```

New text:

```
        offer = source.offer(request)
    except (AdapterAuthFailed, AdapterBroken):

```

### `r705-b.S8_acquire_one_softens_the_park_at_the_fetch`

a park raised at the fetch is one unavailable track and the driver claims the next

- File: `src/cratekit/acquire/adapter.py`
- Source: `r705-b.json`, row `S8_acquire_one_softens_the_park_at_the_fetch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_acquire_one_lets_the_park_through_rather_than_failing_the_track[fetch]`

Old text:

```
        path = source.fetch(request, settings.download_staging)
    except (AdapterAuthFailed, AdapterBroken, Parked):

```

New text:

```
        path = source.fetch(request, settings.download_staging)
    except (AdapterAuthFailed, AdapterBroken):

```

### `u269.M3_only_import_hidden_from_the_tree`

acquire/bandcamp.py: the one import of curl_cffi becomes a computed name, so no import under src names it

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u269.json`, row `M3_only_import_hidden_from_the_tree`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_packaging.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_packaging.py::test_every_core_dependency_is_imported_by_the_package`

Old text:

```
        from curl_cffi import requests as curl_requests  # noqa: PLC0415 - the network seam

```

New text:

```
        curl_requests = __import__("".join(["curl", "_cffi.requests"])).requests

```

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

### `r668-a.M11_no_frozen_list_skip`

a job whose payload names no list is compared against an empty path and refuses any list named beside it

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M11_no_frozen_list_skip`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 23216 against a baseline of 23216
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

### `r679-b.D2_fallback_gate_on_question_alone`

fallback pass: gate the store on the needs-review state alone

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `r679-b.json`, row `D2_fallback_gate_on_question_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 834 against a baseline of 834
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_caller_of_adjudicate_gates_on_the_rows_that_touch_the_queue`

Old text:

```
    if any(match_cli.touches_the_queue(one) for one in resolved.matches):
```

New text:

```
    if any(one.state is match.MatchState.NEEDS_REVIEW for one in resolved.matches):
```

### `r1313.I1_cache_failure_alone`

said_not_found: read the 404 off the failure alone, as before R-1313, so an ISRC answered with a 404 page is never kept

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `r1313.json`, row `I1_cache_failure_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`
- Collected: 403 against a baseline of 403
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[account]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    return answered_not_found(exc)
```

New text:

```
    return getattr(getattr(exc, "response", None), "status_code", None) == 404
```

### `r1313.I2_cache_keeps_any_status`

said_not_found: keep any failure carrying a status, so an outage is remembered for a week as filed under nothing

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `r1313.json`, row `I2_cache_keeps_any_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`
- Collected: 403 against a baseline of 403
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_said_not_found_is_the_clients_own_class_or_a_404_and_nothing_else[500]`
  - `tests/test_provider_not_found_bodies.py::test_a_server_error_is_never_a_not_found_whatever_its_body[500-json-isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_server_error_is_never_a_not_found_whatever_its_body[503-empty-isrc_cache]`

Old text:

```
    return answered_not_found(exc)
```

New text:

```
    return answered_not_found(exc) or getattr(getattr(exc, "response", None), "status_code", None) is not None
```

### `u206-b.M2b_disabled_recall_composite`

Composite: drop recall's days 0 guard AND give every entry at least a day's life, so answers kept before the cache was turned off still answer

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206-b.json`, row `M2b_disabled_recall_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1131 against a baseline of 1131
- Kills: 8 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_answers_kept_before_the_cache_was_turned_off_answer_nothing`
  - `tests/test_isrc_cache.py::test_zero_days_asks_every_time_and_writes_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_lone_release_a_lone_heart_or_a_lone_album_is_never_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`

Old text:

```
        global _PROCESS_HITS
        if not self.enabled:
            return None
```

New text:

```
        global _PROCESS_HITS
        self.days = max(self.days, 1)
```

### `u206.M11_unreadable_answer_kept`

Cache.remember: keep an answer holding a track that cannot be read

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M11_unreadable_answer_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1131 against a baseline of 1131
- Kills: 4 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_answer_holding_a_track_that_cannot_be_read_is_asked_again[no-artist]`
  - `tests/test_isrc_cache.py::test_an_answer_holding_a_track_that_cannot_be_read_is_asked_again[no-identifier]`
  - `tests/test_isrc_cache.py::test_an_answer_holding_a_track_that_cannot_be_read_is_asked_again[no-title]`
  - `tests/test_organize_mirror_tie.py::test_a_tie_beside_a_release_that_cannot_be_read_is_left_out_and_asked_again`

Old text:

```
        if not all(_readable(track) for track in tracks):
            return False
```

New text:

```
        if False:
            return False
```

### `u68.D1_unlisted_on_blank_ref`

A row with no provider id is written to the document instead of being returned unlisted

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `D1_unlisted_on_blank_ref`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_with_no_provider_id_is_unlisted_and_the_document_still_reads`
  - `tests/test_listdoc.py::test_a_track_from_another_service_is_unlisted_not_written_as_a_provider_id`
  - `tests/test_listdoc.py::test_no_listable_row_writes_nothing_and_says_so`

Old text:

```
        if not ref:
            unlisted.append(row)
            continue
```

New text:

```
        if False:
            unlisted.append(row)
            continue
```

### `u68.D2_first_id_wins`

A repeated id is written again instead of being folded into its first occurrence

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `D2_first_id_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_duplicate_id_is_written_once_and_the_first_occurrence_wins`
  - `tests/test_listdoc.py::test_an_id_is_compared_stripped_because_the_reader_strips_it`

Old text:

```
        if ref in seen:
            continue
```

New text:

```
        if False:
            continue
```

### `u68.D3_ref_stripped`

An id is compared as given rather than stripped, as the reader strips it

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `D3_ref_stripped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_with_no_provider_id_is_unlisted_and_the_document_still_reads`
  - `tests/test_listdoc.py::test_an_id_is_compared_stripped_because_the_reader_strips_it`

Old text:

```
        ref = str(row.ref or "").strip()
```

New text:

```
        ref = str(row.ref or "")
```

### `u68.D4_reader_check`

Drop the read back through the reader's own row recognition, so a row the reader refuses is written

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `D4_reader_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[no-artist]`
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[no-title]`
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[only-a-version]`

Old text:

```
        track = _track(row, ref)
        _checked(track, position)
```

New text:

```
        track = _track(row, ref)
```

### `u68.F1_different_file_refused`

An existing file holding different bytes is overwritten instead of refused

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `F1_different_file_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_listdoc.py::test_an_existing_different_list_is_refused_and_left_alone`
  - `tests/test_listdoc.py::test_an_existing_different_manifest_is_refused_before_the_list_is_written`
  - `tests/test_listdoc.py::test_an_existing_different_unlisted_file_refuses_before_either_half_is_written`

Old text:

```
    if present != payload:
```

New text:

```
    if False:
```

### `u68.M1_manifest_version`

The manifest records the declared version of a row as empty

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `M1_manifest_version`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_manifest_row_reads_as_the_wanted_track_its_list_row_reads_as`
  - `tests/test_listdoc.py::test_the_manifest_records_each_ids_provenance`

Old text:

```
            "version": track.get("version", ""),
```

New text:

```
            "version": "",
```

### `u68.N1_slash`

A name holding a slash is accepted

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `N1_slash`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_name_that_is_not_one_plain_file_name_is_refused[a/b]`

Old text:

```
        or "/" in name

```

New text:

```
(empty)
```

### `u68.N2_surrounding_space`

A name with leading or trailing space is accepted

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `N2_surrounding_space`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_name_that_is_not_one_plain_file_name_is_refused[ set]`

Old text:

```
        or name != name.strip()

```

New text:

```
(empty)
```

### `u68.N3_dot_names`

A name of one or two dots is accepted

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `N3_dot_names`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_name_that_is_not_one_plain_file_name_is_refused[..]`
  - `tests/test_listdoc.py::test_a_name_that_is_not_one_plain_file_name_is_refused[.]`

Old text:

```
        or name in {".", ".."}

```

New text:

```
(empty)
```

### `u68.P1_missing_provenance`

A listed id with no provenance is not refused by name

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `P1_missing_provenance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_listed_id_with_no_provenance_refuses_and_writes_nothing`

Old text:

```
    if found is None:
        raise ListDocRefused
```

New text:

```
    if False:
        raise ListDocRefused
```

### `u68.P2_blank_source`

A provenance naming no source is accepted

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `P2_blank_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_provenance_naming_no_source_refuses`

Old text:

```
    if not isinstance(found.source, str) or not found.source.strip():
```

New text:

```
    if False:
```

### `u68.T1_version_written`

A declared version is not written to the track

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `T1_version_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 6 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_declared_version_beside_an_embedded_one_round_trips_whole[Sun Path (Extended)]`
  - `tests/test_listdoc.py::test_a_declared_version_beside_an_embedded_one_round_trips_whole[Sun Path (feat. Mira) (Extended)]`
  - `tests/test_listdoc.py::test_a_manifest_row_reads_as_the_wanted_track_its_list_row_reads_as`
  - `tests/test_listdoc.py::test_a_version_re_reads_to_the_same_token[Tide Line-Dub-dub]`
  - `tests/test_listdoc.py::test_the_list_round_trips_through_the_real_reader_and_the_download_freeze`
  - `tests/test_listdoc.py::test_the_manifest_records_each_ids_provenance`

Old text:

```
    if row.version.strip():
        track["version"]
```

New text:

```
    if False:
        track["version"]
```

### `u68.T2_isrc_written`

An isrc is not written to the track

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `T2_isrc_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 4 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_manifest_row_reads_as_the_wanted_track_its_list_row_reads_as`
  - `tests/test_listdoc.py::test_frozen_tracks_become_rows_that_freeze_back_identically`
  - `tests/test_listdoc.py::test_the_list_round_trips_through_the_real_reader_and_the_download_freeze`
  - `tests/test_listdoc.py::test_the_manifest_records_each_ids_provenance`

Old text:

```
    if row.isrc and row.isrc.strip():
```

New text:

```
    if False:
```

### `u68.T3_key_written`

A key is not written to the track

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `T3_key_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_the_list_round_trips_through_the_real_reader_and_the_download_freeze`

Old text:

```
    if row.key and row.key.strip():
```

New text:

```
    if False:
```

### `u68.W1_other_service_unlisted`

A track from another service keeps its id and is written as a provider id

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `W1_other_service_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_track_from_another_service_is_unlisted_not_written_as_a_provider_id`

Old text:

```
    ref = wanted.ref if wanted.origin == match.TIDAL else ""
```

New text:

```
    ref = wanted.ref
```

### `u68.W2_raw_title_candidate`

Drop the raw title plus declared version spelling, so the split title is the fallback

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `W2_raw_title_candidate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_declared_version_beside_an_embedded_one_round_trips_whole[Sun Path (Extended)]`
  - `tests/test_listdoc.py::test_a_declared_version_beside_an_embedded_one_round_trips_whole[Sun Path (feat. Mira) (Extended)]`

Old text:

```
        if wanted.version and wanted.spelled.endswith(suffix):
```

New text:

```
        if False:
```

### `u73-b.C1_refs_only_when_several`

Write source_refs for a single reference too, changing the bytes of a manifest an earlier build wrote

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u73-b.json`, row `C1_refs_only_when_several`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_one_reference_writes_the_bytes_a_manifest_had_before_the_field`

Old text:

```
        if len(origin.source_refs) > 1:
```

New text:

```
        if len(origin.source_refs) >= 1:
```

### `u73-b.C2_refs_written`

Never write source_refs into the manifest

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u73-b.json`, row `C2_refs_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_listdoc.py::test_every_source_that_asked_for_an_id_reads_back`
  - `tests/test_listdoc.py::test_the_manifest_keeps_every_reference_an_id_came_from`

Old text:

```
            entry["source_refs"] = list(origin.source_refs)
```

New text:

```
            pass
```

### `u77-c.C1_manifest_version`

manifest_rows: refuse only a version below this build's, so a manifest of a later version is read on the hope its keys still mean what they meant

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C1_manifest_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_manifest_that_cannot_be_read_refuses_before_any_file_moves[{"manifest": 2, "rows": {}}-version 2]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 2, "rows": {}}-version 2]`

Old text:

```
if isinstance(version, bool) or version != MANIFEST_VERSION:
```

New text:

```
if isinstance(version, bool) or version < MANIFEST_VERSION:
```

### `u77-c.C2_manifest_version_bool`

manifest_rows: drop the boolean test on the version, so true, which Python holds equal to 1, reads as version 1

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C2_manifest_version_bool`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": true, "rows": {}}-version True]`

Old text:

```
if isinstance(version, bool) or version != MANIFEST_VERSION:
```

New text:

```
if version != MANIFEST_VERSION:
```

### `u77-c.C3_not_a_manifest`

manifest_rows: stop asking whether the document names a manifest version at all, so a list document passed by mistake is not refused by name

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C3_not_a_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_that_is_not_one_is_refused[the list]`
  - `tests/test_landing_labels.py::test_a_manifest_that_cannot_be_read_refuses_before_any_file_moves[{"list": 1, "origin": "tidal", "tracks": []}-not a manifest]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"list": 1, "origin": "tidal", "tracks": []}-not a manifest]`

Old text:

```
if not isinstance(body, Mapping) or "manifest" not in body:
```

New text:

```
if not isinstance(body, Mapping):
```

