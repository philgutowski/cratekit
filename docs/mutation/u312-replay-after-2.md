# Mutation table: u312-replay-after-2

Measured by `scripts/mutate.py` on 2026-11-23 12:41 UTC, branch `HEAD` at `55e2f3b6`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22479 collected. pytest invocations for this batch: 84.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 45, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `known/scratch.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 188 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22479 against 22479. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u23-round-8-independent.E1_vacancy_is_mere_absence` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.E2_vacancy_parent_check_inverted` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.E4_vacancy_always_true` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 3 | killed |
| `u23-round-8-independent.F1_byte_search_drops_the_vacancy_filter` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 3 | killed |
| `u23-round-8-independent.F4_byte_search_reads_before_it_filters` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.G1_locked_passes_no_size` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 2 | killed |
| `r658-c.S4c_dataless_skip_returns` | `src/cratekit/adopt/revert_changed.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.S1_size_of_always_none` | `src/cratekit/adopt/revert_changed.py` | maintainer | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.X12_look_at_drops_the_regular_file_test` | `src/cratekit/adopt/revert_changed.py` | user | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.X13_look_at_drops_the_recorded_size_shortcut` | `src/cratekit/adopt/revert_changed.py` | maintainer | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.X14_probe_drops_the_dataless_test` | `src/cratekit/adopt/scan.py` | user | 1 file(s) | 615 | 1 | killed |
| `r658-b.S3_adoption_failing_stat` | `tests/test_adoption.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent-composites.X6_composite_excluded_becomes_routed` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 619 | 5 | killed |
| `u92-author.G1_guard_deleted` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 4 | killed |
| `u92-author.G8_refused_file_tagged_zero` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 2 | killed |
| `u92-author.G9_warning_counts_the_wrong_reason` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 223 | 5 | killed |
| `u223.M1_keep_intent` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 3 | killed |
| `u223.M22_discard_unlinks_directory` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M4_subdir_unlinked` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 172 | 2 | killed |
| `u223.M5_discard_keeps_report` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M6_discard_keeps_intent` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 4 | killed |
| `r395.M9_worker_literal` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u192.A2_restamp_queue_only_ignored` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 3 | killed |
| `u223.M17_claim_failure_keeps_evidence` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M18_refused_rename_keeps_evidence` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M19_attempt_start_keeps_evidence` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.R2_extra_not_required` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.R4_keyless_finalized` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.R5_tag_write_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.R7_absent_energy_stamped` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.R8_title_without_head` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.R9_missing_file_analysed` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.S2_unchanged_rewritten` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.S3_queue_without_calibration` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 3 | killed |
| `u58-workers-and-wav.W1_voxlevel_zero` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 172 | 4 | killed |
| `u58-workers-and-wav.W2_decoder_seam_ignored` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 172 | 7 | killed |
| `u58-workers-and-wav.W4_model_guard` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-zero-row-remeasured.W6_gender_constant` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 172 | 2 | killed |
| `u212.T5_name_wraps` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1608 | 2 | killed |
| `u212.S1_missing_ends` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 318 | 1 | killed |
| `u212.S4_staged_said` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 318 | 1 | killed |
| `u223.M3_no_clear` | `src/cratekit/analysis/artifacts.py` | user | 2 file(s) | 274 | 3 | killed |
| `u192.A1_run_queue_only_ignored` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 11 | killed |
| `u306.A3_walk_recursive` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 18 | killed |
| `u93-recursive-analysis.D21_restamp_flag` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 18 | killed |
| `r221-a.S3_flag_reads_a_key_nothing_freezes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 7 | killed |
| `r221-a.W1_rehearsal_never_said` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 3 | killed |
| `r221-a.W2_rehearsal_said_unconditionally` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 3 | killed |
| `r221-b.M1_refusal_step_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 4 | killed |
| `r221-b.M2_refusal_step_unconditional` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 4 | killed |
| `r349-a.A1_failure_write` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 2 | killed |
| `r349-a.A2_success_produced` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 6 | killed |
| `r349-a.A4_envelope_field` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r349-b.B3_clear_before_attempt` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `r349-b.B4_stage_error_completes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `r390-a.A6_backup_transfer_exit_is_permanent` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 4 | killed |
| `u45-round-1.A1_unreadable_reported_as_absent` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 5 | killed |
| `u45-round-1.A4_state_collapsed_to_known` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 2 | killed |
| `u45-round-1.C2_refusal_read_as_failure` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 6 | killed |
| `u45-round-1.C3_nothing_ran_accepted` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 8 | killed |
| `u45-round-1.C4_uniform_refusal_flattened` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 3 | killed |
| `u45-round-1.C5_first_refusal_taken` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u45-round-1.C6_partial_run_refused` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 3 | killed |
| `u45-round-1.H2_queueing_plans_first` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u45-round-1.R1_reserved_remediation_discarded` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 4 | killed |
| `u45-round-1.R2_slug_flattened` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 2 | killed |
| `u45-round-1.W2_report_from_the_plan` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 10 | killed |
| `u45-round-1.W3_ages_not_read_back` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 4 | killed |
| `u45-round-1.W4_ages_derived_from_the_outcome` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 3 | killed |
| `u45-round-1.W5_publishing_switched_off` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 8 | killed |
| `u45-round-1.W6_rehearsal_becomes_a_real_run` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 6 | killed |
| `u45-round-1.W8_engine_refusal_escapes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u45-round-2.A3_age_seconds_always_none` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u45-round-2.C7_failed_detail_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u50-author.B1_no_items_enqueued` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 30 | killed |
| `u50-author.B3_items_one_portion_only` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 14 | killed |
| `u50-author.W1_no_narrowing` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `u50-author.W5_unknown_portion_unchecked` | `src/cratekit/backup/cli.py` | maintainer | 1 file(s) | 89 | 1 | killed |
| `u50-author.W6_fresh_config_in_the_handler` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 19 | killed |
| `u50-review-fixes.R2_empty_job_guard_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u50-zero-rows.W4b_item_ignored_entirely` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 12 | killed |
| `r349-a.A3_job_show_field` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 89 | 4 | killed |
| `r349-c.C1_prune_recorded` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 29 | killed |
| `r349-c.C4_argv_rendered` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 4 | killed |
| `u311.B3_iso_drops_a_present_moment` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 218 | 1 | killed |
| `u132.D1_doctor_behind` | `src/cratekit/cli/doctor_library.py` | user | 12 file(s) | 2220 | 2 | killed |
| `u132.D2_doctor_defect` | `src/cratekit/cli/doctor_library.py` | user | 12 file(s) | 2220 | 1 | killed |
| `r1761.P13_history_record_ignored` | `src/cratekit/modules/tools/backup_proof.py` | user | 5 file(s) | 406 | 77 | killed |
| `u281.S1_beatport_reads_no_refusal` | `src/cratekit/tagging/shops.py` | user | 5 file(s) | 447 | 22 | killed |
| `u281.R1_stop_after_four` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 11 | killed |
| `u281.R2_limit_two` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 12 | killed |
| `u281.W2_searcher_ignores_the_handed_count` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 10 | killed |
| `u281.W5_run_never_changes` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 4 | killed |
| `u306.S1_shop_query` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 205 | 14 | killed |
| `u56-catalogue-searcher-and-tag-workers.R5_bare_alias_lookup` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 189 | 29 | killed |
| `r791-a.S1_403_blocks` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 239 | 11 | killed |
| `u322.M13_beside_any_said_dropped` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 2 | killed |
| `u322.M14_token_rows_said_no_token` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 4 | killed |
| `u27-reports-round-1.D2_required_gate` | `src/cratekit/cli/doctor_library.py` | user | 4 file(s) | 1685 | 1 | killed |
| `u27-reports-round-3-fixes.F3_trash_absent_is_a_failure` | `src/cratekit/cli/doctor_library.py` | user | 4 file(s) | 1685 | 1 | killed |
| `u27-round-8-independent.E1_mount_detail_swapped` | `src/cratekit/cli/doctor_library.py` | user | 4 file(s) | 1685 | 1 | killed |
| `u27-round-8-independent.E2_identity_verdict_green` | `src/cratekit/cli/doctor_library.py` | user | 4 file(s) | 1685 | 3 | killed |
| `u27-round-8-independent.E3_found_at_dropped` | `src/cratekit/cli/doctor_library.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.E1_dispatch_impl` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.E2_config_inside_checkout` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T10_no_yaml_falls_back` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T12_caller_ignores_unknown` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 2 | killed |
| `r-1.T13_missing_other_hook` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 2 | killed |
| `r-1.T15_other_dispatch` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T16_same_configuration` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T17_install_config_flag` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T18_remedy_floor` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T19_remedy_reads_config` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T20_stage_parameter` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 3 | killed |
| `r-1.T21_ok_names_others` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `r-1.T22_pre_commit_floor` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 13 | killed |
| `r-1.T5_hook_stages` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 12 | killed |
| `r-1.T9_yaml_error_falls_back` | `src/cratekit/cli/doctor_state.py` | user | 4 file(s) | 1685 | 1 | killed |
| `u27-round-8-independent.C8_two_path_precondition` | `src/cratekit/core/cause.py` | maintainer | 11 file(s) | 22479 | 0 (promoted) | zero |
| `u212.M10_left_out` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u212.M1_staged_match` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 5 | killed |
| `u212.M2_own_rows_both` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 3 | killed |
| `u212.M3_own_rows_by_id` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u212.M4_own_rows_by_isrc` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u212.M5_unread_is_empty` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u212.M6_absent_folder` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u212.M7_outcome_staged` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u212.M8_summary_count` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 4 | killed |
| `u212.M9_unread_status` | `src/cratekit/intake/missing_cli.py` | user | 14 file(s) | 1364 | 1 | killed |
| `u234.O18_snapshot_keeps_the_reading` | `src/cratekit/modules/outbound/pairs.py` | maintainer | 23 file(s) | 1764 | 4 | killed |
| `u234.O19_reading_not_written` | `src/cratekit/modules/outbound/pairs.py` | user | 23 file(s) | 1764 | 14 | killed |
| `u248.L2_chosen_never_built` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1156 | 306 | killed |
| `u197.M2_retired_mapping_empty` | `src/cratekit/core/config_schema.py` | user | 3 file(s) | 826 | 4 | killed |
| `u197.M1_config_fold` | `src/cratekit/core/config_validate.py` | user | 3 file(s) | 826 | 2 | killed |
| `u326.R3_library_root_redirected` | `tests/conftest.py` | maintainer | 4 file(s) | 460 | 1 | killed |
| `u299.U7_library_extras_passed` | `src/cratekit/core/state_files.py` | user | 4 file(s) | 462 | 34 | killed |
| `r926.C1_root_is_state_roots_only` | `tests/conftest.py` | maintainer | 4 file(s) | 310 | 11 | killed |
| `r926.C2_root_never_registered` | `tests/conftest.py` | maintainer | 4 file(s) | 310 | 30 | killed |
| `r235-a.M13_snapshot_check_dropped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 11 | killed |
| `r235-a.M1_unreadable_log_skipped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `u326.R6_cyanite_refused` | `tests/conftest.py` | maintainer | 1 file(s) | 78 | 1 | killed |
| `u40-author-full.F4_tombstone_indexed` | `src/cratekit/write/trees.py` | user | 7 file(s) | 755 | 3 | killed |
| `u27-round-8-independent.E4_path_missing_reads_ok` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 738 | 4 | killed |
| `u27-round-8-independent.E5_unmounted_reads_foreign` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 738 | 5 | killed |
| `r318.P1_withdrawn_branch_removed` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 423 | 5 | killed |
| `r318.P4_ambiguous_reads_not_imported` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 423 | 3 | killed |
| `r1844.N17_screen_silent` | `src/cratekit/deletion/cli.py` | user | 2 file(s) | 373 | 6 | killed |
| `r1037.M1_identity_unchecked` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1037.M8_playlist_ids_live_only` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 9 | killed |
| `r1844.N10_numbered_ignored` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1844.N11_marked_uuid_unread` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1844.N12_record_uuid_unread` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 5 | killed |
| `r1844.N1_uuid_proof_dropped` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 5 | killed |
| `r1844.N2_id_alone_proves` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 3 | killed |
| `r1844.N4_playlist_proof_dropped` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 11 | killed |
| `r1844.N5_any_playlist_proves` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 1 | killed |
| `r1844.N6_no_playlist_proves` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 5 | killed |
| `r1844.N7_held_rows_read_absent` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 35 | killed |
| `r1844.N9_rolled_back_unlisted` | `src/cratekit/deletion/library.py` | user | 3 file(s) | 447 | 7 | killed |
| `r1037.M10_landed_not_joined` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 14 | killed |
| `r1037.M11_sightings_never_forgotten` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 1 | killed |
| `r1037.M12_playlists_always_held` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 8 | killed |
| `r1037.M9_recorded_not_excluded` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1844.N14_uuids_not_passed` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 4 | killed |
| `r1844.N16_review_count_lost` | `src/cratekit/deletion/run.py` | user | 3 file(s) | 447 | 5 | killed |
| `r1037.M13_sight_renumbers` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 447 | 3 | killed |
| `r1037.M14_sight_at_the_watermark` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 447 | 15 | killed |
| `r1037.M15_sight_keeps_held` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1037.M16_advance_drops_sightings` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 447 | 2 | killed |
| `r1037.M19_version_two_refused` | `src/cratekit/deletion/watermark.py` | user | 3 file(s) | 447 | 114 | killed |
| `r1844.N13_landing_writes_no_uuid` | `src/cratekit/intake/native.py` | user | 2 file(s) | 86 | 5 | killed |
| `r1037.N1_landed_not_recorded` | `src/cratekit/intake/native.py` | user | 3 file(s) | 119 | 33 | killed |
| `r1037.N2_joined_not_made` | `src/cratekit/intake/native.py` | user | 3 file(s) | 119 | 5 | killed |
| `r1037.N3_identity_wrong` | `src/cratekit/intake/native.py` | user | 3 file(s) | 119 | 21 | killed |
| `r1037.N4_size_not_read` | `src/cratekit/intake/native.py` | user | 3 file(s) | 119 | 12 | killed |
| `r1037.N6_before_empty` | `src/cratekit/intake/native.py` | user | 3 file(s) | 119 | 5 | killed |
| `u282.W1_walk_beatport_first` | `src/cratekit/tagging/catalogues.py` | user | 9 file(s) | 1470 | 43 | killed |
| `u282.W2_sources_beatport_first` | `src/cratekit/tagging/catalogues.py` | user | 9 file(s) | 1470 | 2 | killed |
| `u282.L2_nobody_named_is_the_source` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 4 | killed |
| `u282.P1_no_picture_question` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 8 | killed |
| `u282.P3_answer_not_folded` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 5 | killed |
| `u282.P5_match_names_no_picture` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 4 | killed |
| `u282.P6_waiting_note_dropped` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 1 | killed |
| `u282.R1_rejection_raised_at_once` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 5 | killed |
| `u282.R4_rejection_reads_as_no_token` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 3 | killed |
| `u282.T1_question_asked_with_a_picture` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1470 | 2 | killed |
| `u282.T2_question_never_asked` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1470 | 5 | killed |
| `u282.C2_refused_token_not_warned` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 443 | 1 | killed |
| `u282.C1_refused_token_not_counted` | `src/cratekit/tagging/summary.py` | user | 5 file(s) | 443 | 1 | killed |
| `u244.M02_rejection_remembered` | `src/cratekit/tagging/discogs.py` | user | 3 file(s) | 262 | 2 | killed |
| `u244.M01_no_token_not_asked` | `src/cratekit/tagging/discogs.py` | user | 5 file(s) | 470 | 11 | killed |
| `u184.D8_check_unlisted` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 6 | killed |
| `u184.D1_volume_not_established` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D2_unreadable_is_a_note` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D3_remedy_chosen_here` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D4_expired_read_as_valid` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D5_wall_clock` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D6_hours_coefficient` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D7_rule_not_named` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u185.D1_push_newer_warns` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 2 | killed |
| `u185.D2_hidden_entries` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 4 | killed |
| `u185.D3_unread_folder` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 2 | killed |
| `u224.M10_refused_backups_read_no_push` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M1_found_ignored` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 7 | killed |
| `u224.M2_unread_place_dropped` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M3_broken_installed_probe_silent` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M4_unread_support_read_absent` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M5_refused_stat_read_absent` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 4 | killed |
| `u224.M6_unread_folded_into_not_installed` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 4 | killed |
| `u224.M7_install_signals_always_asked` | `src/cratekit/cli/doctor_backup.py` | maintainer | 1 file(s) | 417 | 1 | killed |
| `u224.M9_path_through_a_file_unread` | `src/cratekit/cli/doctor_backup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u263.D21_doctor_names_verbs` | `src/cratekit/cli/doctor_keys.py` | user | 1 file(s) | 417 | 1 | killed |
| `r598-b.B6_doctor_clause_dropped` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `u159.M8_behind_reads_current` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 4 | killed |
| `u181.D5_upgrade_never_adds_vocals` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 1 | killed |
| `u181.D6_upgrade_always_adds_vocals` | `src/cratekit/cli/doctor_state.py` | user | 1 file(s) | 417 | 2 | killed |
| `r83.P2_nothing_entered_raise` | `src/cratekit/cli/prompt.py` | user | 1 file(s) | 417 | 2 | killed |
| `r83.P3_empty_secret_note_status` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r83.P4_empty_secret_branch` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `u299.U2_installation_area_passed` | `src/cratekit/core/state_files.py` | user | 1 file(s) | 417 | 3 | killed |
| `u303.D4_run_ignores_probes` | `src/cratekit/cli/doctor.py` | user | 2 file(s) | 1415 | 78 | killed |
| `u263.D22_restamp_declares` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1415 | 1 | killed |
| `r662-b.M16_flag_not_declared` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 1415 | 14 | killed |
| `r345.B2_module_off` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 1466 | 3 | killed |
| `r1255.D1_doctor_branches_on_the_scan` | `src/cratekit/cli/doctor_state.py` | user | 2 file(s) | 432 | 1 | killed |

## Zero rows and what they owe

- `r349-b.B3_clear_before_attempt` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r349-b.B4_stage_error_completes` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u50-author.W1_no_narrowing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.C8_two_path_precondition` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `u23-round-8-independent.E1_vacancy_is_mere_absence`

Round 7 restored: an unmounted volume reads as a deleted file

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `E1_vacancy_is_mere_absence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`

Old text:

```
    recorded = Path(record.path)
    try:
        if not recorded.parent.is_dir():
            return False
        return not recorded.exists()
    except OSError:
        return False

```

New text:

```
    recorded = Path(record.path)
    try:
        return not recorded.exists()
    except OSError:
        return False

```

### `u23-round-8-independent.E2_vacancy_parent_check_inverted`

Vacancy requires the containing directory to be ABSENT

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `E2_vacancy_parent_check_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`

Old text:

```
        if not recorded.parent.is_dir():
            return False
        return not recorded.exists()
```

New text:

```
        if recorded.parent.is_dir():
            return False
        return not recorded.exists()
```

### `u23-round-8-independent.E4_vacancy_always_true`

Every record is stranded, so every record is a byte-search candidate

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `E4_vacancy_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 3 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_first_adoption_of_EIGHT_files_reads_EIGHT_times_and_not_FIFTEEN`
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`
  - `tests/test_adoption.py::test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING`

Old text:

```
    recorded = Path(record.path)
    try:
        if not recorded.parent.is_dir():
            return False
        return not recorded.exists()
    except OSError:
        return False

```

New text:

```
    return True

```

### `u23-round-8-independent.F1_byte_search_drops_the_vacancy_filter`

A record whose path still holds its file is a byte-search candidate

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `F1_byte_search_drops_the_vacancy_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 3 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_first_adoption_of_EIGHT_files_reads_EIGHT_times_and_not_FIFTEEN`
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`
  - `tests/test_adoption.py::test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING`

Old text:

```
    vacant = [record for record in possible if _the_recorded_path_is_vacant(record)]
```

New text:

```
    vacant = list(possible)
```

### `u23-round-8-independent.F4_byte_search_reads_before_it_filters`

Round 7 order restored: the whole-file read runs before the filters that empty the list

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `F4_byte_search_reads_before_it_filters`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_first_adoption_of_EIGHT_files_reads_EIGHT_times_and_not_FIFTEEN`
  - `tests/test_adoption.py::test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING`

Old text:

```
    vacant = [record for record in possible if _the_recorded_path_is_vacant(record)]
    if not vacant or size_here is None:
        return None
    same_size = [record for record in vacant if record.size == size_here]
    if not same_size:
        return None
    looked = look()
    if looked.outcome is not ByteRead.ANSWERED:
        return None

```

New text:

```
    looked = look()
    if looked.outcome is not ByteRead.ANSWERED:
        return None
    vacant = [record for record in possible if _the_recorded_path_is_vacant(record)]
    if not vacant or size_here is None:
        return None
    same_size = [record for record in vacant if record.size == size_here]
    if not same_size:
        return None

```

### `u23-round-8-independent.G1_locked_passes_no_size`

_record_locked hands size_here=None, disabling every size gate below it

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `G1_locked_passes_no_size`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`
  - `tests/test_adoption.py::test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`

Old text:

```
        size_here=_size_of(resolved),
```

New text:

```
        size_here=None,
```

### `r658-c.S4c_dataless_skip_returns`

Composite for S4, run as its own table: put back a skip that refuses to read a dataless file, which only the scoped evicted stat can reach

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `r658-c.json`, row `S4c_dataless_skip_returns`
- Moved: Anchored where u310-replay-after-b.json replayed it: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_cloud_EVICTED_file_IS_read_because_the_restore_fetches_it_anyway`

Old text:

```
    if recorded_size is not None and info.st_size != recorded_size:
        return _Looked(ByteRead.A_DIFFERENT_SIZE)
    try:
        found = digest_of(target)

```

New text:

```
    if recorded_size is not None and info.st_size != recorded_size:
        return _Looked(ByteRead.A_DIFFERENT_SIZE)
    if getattr(info, "st_flags", 0) & 0x40000000:
        return _Looked(ByteRead.UNREADABLE)
    try:
        found = digest_of(target)

```

### `u23-round-8-independent.S1_size_of_always_none`

_size_of never answers, so every size shortcut on every path is disabled

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `u23-round-8-independent.json`, row `S1_size_of_always_none`
- Moved: Anchored where u310-replay-after-b.json replayed it: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`
  - `tests/test_adoption.py::test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`

Old text:

```
    try:
        return target.stat().st_size
    except OSError:
        return None

```

New text:

```
    return None

```

### `u23-round-8-independent.X12_look_at_drops_the_regular_file_test`

A directory or a fifo at the recorded path reaches the hash

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `u23-round-8-independent.json`, row `X12_look_at_drops_the_regular_file_test`
- Moved: Anchored where u310-replay-after-b.json replayed it: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIRECTORY_at_the_recorded_path_refuses_as_ITS_OWN_reason`
  - `tests/test_adoption.py::test_a_FIFO_at_the_recorded_path_refuses_instead_of_blocking_forever`

Old text:

```
    if not stat_module.S_ISREG(info.st_mode):
        return _Looked(ByteRead.NOT_A_REGULAR_FILE)

```

New text:

```
(empty)
```

### `u23-round-8-independent.X13_look_at_drops_the_recorded_size_shortcut`

The prefetch reads a file whose size already rules the record out

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `u23-round-8-independent.json`, row `X13_look_at_drops_the_recorded_size_shortcut`
- Moved: Anchored where u310-replay-after-b.json replayed it: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_file_of_a_DIFFERENT_SIZE_is_refused_without_reading_it`

Old text:

```
    if recorded_size is not None and info.st_size != recorded_size:
        return _Looked(ByteRead.A_DIFFERENT_SIZE)

```

New text:

```
(empty)
```

### `u23-round-8-independent.X14_probe_drops_the_dataless_test`

A cloud-evicted file is probed by reading it, so the census downloads

- File: `src/cratekit/adopt/scan.py`
- Source: `u23-round-8-independent.json`, row `X14_probe_drops_the_dataless_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_online_only_file_is_never_opened_by_the_probe`

Old text:

```
    if _is_dataless(info):
        return Readability.ONLINE_ONLY

```

New text:

```
(empty)
```

### `r658-b.S3_adoption_failing_stat`

Drop the scoped failing stat around the stamping write

- File: `tests/test_adoption.py`
- Source: `r658-b.json`, row `S3_adoption_failing_stat`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_stamping_STAT_that_fails_records_the_state_rather_than_asserting_it_cannot`

Old text:

```
        failing.setattr(Path, "stat", stat_fails_after_the_write)

```

New text:

```
(empty)
```

### `u23-round-8-independent-composites.X6_composite_excluded_becomes_routed`

What X6 holds: the EXCLUDED disposition itself, forced to ROUTE

- File: `src/cratekit/adopt/scan.py`
- Source: `u23-round-8-independent-composites.json`, row `X6_composite_excluded_becomes_routed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 619 against a baseline of 619
- Kills: 5 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_location_naming_another_host_is_reported_rather_than_guessed`
  - `tests/test_adoption.py::test_a_row_whose_location_column_is_NULL_does_not_end_the_census`
  - `tests/test_adoption.py::test_an_excluded_track_is_carried_in_the_plan_rather_than_dropped`
  - `tests/test_adoption.py::test_every_plan_entry_identifier_is_derivable_from_the_record_it_names`
  - `tests/test_adoption.py::test_the_plan_carries_every_scanned_row_whatever_happened_to_it`

Old text:

```
        if readability not in ADOPTABLE:
            yield ScannedTrack(
                content_id=row.content_id,
                recorded=row.recorded,
                path=path,
                readability=readability,
                disposition=Disposition.EXCLUDED,
                genre=row.genre,
            )
            continue

```

New text:

```
        if readability not in ADOPTABLE:
            yield ScannedTrack(
                content_id=row.content_id,
                recorded=row.recorded,
                path=path,
                readability=readability,
                disposition=Disposition.ROUTE,
                genre=row.genre,
            )
            continue

```

### `u92-author.G1_guard_deleted`

Delete the oversize guard from analyse entirely, which is main's state

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G1_guard_deleted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 223 against a baseline of 223
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

### `u92-author.G8_refused_file_tagged_zero`

Tag the refused file voxlevel 0 the way the source system did, instead of leaving an absence

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G8_refused_file_tagged_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 223 against a baseline of 223
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
- Collected: 223 against a baseline of 223
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

### `u223.M1_keep_intent`

staged_path: clear the rename intent with everything else, the shipped behaviour

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M1_keep_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`

Old text:

```
                entry.name == RENAME_INTENT_FILENAME
                and entry.is_file()
```

New text:

```
                entry.name == "never-kept.json"
                and entry.is_file()
```

### `u223.M22_discard_unlinks_directory`

discard_rename_evidence: unlink a directory at the report name, failing the item for good

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M22_discard_unlinks_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`

Old text:

```
        if entry.is_symlink() or not entry.is_dir():
            entry.unlink(missing_ok=True)
```

New text:

```
        if True:
            entry.unlink(missing_ok=True)
```

### `u223.M4_subdir_unlinked`

staged_path: unlink a subdirectory entry instead of removing its tree

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M4_subdir_unlinked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`

Old text:

```
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
```

New text:

```
            if False:
                shutil.rmtree(entry)
```

### `u223.M5_discard_keeps_report`

discard_rename_evidence: drop the intent only, round one's residual

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M5_discard_keeps_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`

Old text:

```
    for name in (RENAME_INTENT_FILENAME, _report_name(item.ordinal)):
```

New text:

```
    for name in (RENAME_INTENT_FILENAME,):
```

### `u223.M6_discard_keeps_intent`

discard_rename_evidence: drop the report only, keeping the intent

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M6_discard_keeps_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`
  - `tests/test_analysis_workers.py::test_a_taken_target_name_leaves_no_intent_behind`

Old text:

```
    for name in (RENAME_INTENT_FILENAME, _report_name(item.ordinal)):
```

New text:

```
    for name in (_report_name(item.ordinal),):
```

### `r395.M9_worker_literal`

Put the old bare pip literal back in the analysis worker refusal

- File: `src/cratekit/analysis/cli.py`
- Source: `r395.json`, row `M9_worker_literal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_missing_extra_refuses_the_item_rather_than_skipping_it_as_keyless`

Old text:

```
"install": extras.install_command("analysis")
```

New text:

```
"install": "pip install 'cratekit[analysis]'"
```

### `u192.A2_restamp_queue_only_ignored`

analyze_restamp: ignore --queue-only and drive the job

- File: `src/cratekit/analysis/cli.py`
- Source: `u192.json`, row `A2_restamp_queue_only_ignored`
- Moved: Anchored where u325-replay-after.json replayed it: Same branch in analyze_restamp; U298 replaced the local _reported with core.jobs.reported
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[restamp]`

Old text:

```
        if foreground.queue_only(ctx.args):
            return ctx.envelope(
                data=jobs.reported(store, job), warnings=(DB_NOT_WRITTEN, *extra)
```

New text:

```
        if False:
            return ctx.envelope(
                data=jobs.reported(store, job), warnings=(DB_NOT_WRITTEN, *extra)
```

### `u223.M17_claim_failure_keeps_evidence`

_finalize: keep the intent when the target name is taken

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M17_claim_failure_keeps_evidence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_taken_target_name_leaves_no_intent_behind`

Old text:

```
        # read that unrelated file as this item's twin (U223).
        artifacts.discard_rename_evidence(cfg, job, item)
```

New text:

```
        # read that unrelated file as this item's twin (U223).
```

### `u223.M18_refused_rename_keeps_evidence`

_finalize: keep the intent when the rename is refused

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M18_refused_rename_keeps_evidence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`

Old text:

```
        target.unlink(missing_ok=True)
        artifacts.discard_rename_evidence(cfg, job, item)
```

New text:

```
        target.unlink(missing_ok=True)
```

### `u223.M19_attempt_start_keeps_evidence`

handle_run: keep stale evidence when the source is still a file

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M19_attempt_start_keeps_evidence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`

Old text:

```
    # it renames (U223).
    artifacts.discard_rename_evidence(cfg, job, item)
```

New text:

```
    # it renames (U223).
```

### `u58-workers-and-wav.R2_extra_not_required`

Drop the missing extra refusal in the run worker

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R2_extra_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_missing_extra_refuses_the_item_rather_than_skipping_it_as_keyless`

Old text:

```
    _require_heavy(_fake_detect_bound(), "analysing a track")

```

New text:

```
(empty)
```

### `u58-workers-and-wav.R4_keyless_finalized`

Finalize a track whose head found no key

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R4_keyless_finalized`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_keyless_track_is_a_terminal_skip_with_nothing_written`
  - `tests/test_analysis_workers.py::test_an_undecodable_file_is_its_own_terminal_and_not_a_keyless_track`

Old text:

```
    if partial.get("terminal") is not None:
        return artifacts.produced(
            cfg, job, item, {"item": item.item_id, "path": str(path), "status": partial["terminal"]}
        )

```

New text:

```
(empty)
```

### `u58-workers-and-wav.R5_tag_write_unchecked`

Ignore a failed tag write and rename anyway

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R5_tag_write_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug`
  - `tests/test_analysis_workers.py::test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone`

Old text:

```
    _write_or_refuse(path, fields, untouched="The file is untouched and was not renamed")
```

New text:

```
    tags.write_tags(path, fields)
```

### `u58-workers-and-wav.R7_absent_energy_stamped`

Write a level for an absent energy

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R7_absent_energy_stamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_uncalibrated_library_writes_no_energy_tag_and_routes_to_the_sink`

Old text:

```
        "energylevel": scored.get("energy"),
```

New text:

```
        "energylevel": scored.get("energy") or 5,
```

### `u58-workers-and-wav.R8_title_without_head`

Write the bare stem as the title tag

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R8_title_without_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_taken_target_name_fails_the_item_and_keeps_the_written_head_in_the_title`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`

Old text:

```
        "title": rendered.title_tag,
```

New text:

```
        "title": path.stem,
```

### `u58-workers-and-wav.R9_missing_file_analysed`

Drop the source-missing refusal for a file that vanished

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R9_missing_file_analysed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`

Old text:

```
        if twin is None:
            raise _refuse_missing(item, folder, path, "analyse")

```

New text:

```
(empty)
```

### `u58-workers-and-wav.S2_unchanged_rewritten`

Rewrite a file whose level did not move

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `S2_unchanged_rewritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_whose_level_did_not_move_is_reported_unchanged_and_not_rewritten`

Old text:

```
    if previous != level:
```

New text:

```
    if True:
```

### `u58-workers-and-wav.S3_queue_without_calibration`

Queue a restamp over a library that has no calibration

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `S3_queue_without_calibration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_restamp_with_no_calibration_refuses_at_the_queue`
  - `tests/test_analysis_workers.py::test_the_restamp_refusal_names_the_library_wide_calibrate`

Old text:

```
    # REFUSED AT THE QUEUE, not only in the worker: a job whose every item
    # would fail on the same absence is a report over work nothing could do.
    _calibration_or_refuse(cfg)

```

New text:

```
(empty)
```

### `u58-workers-and-wav.W1_voxlevel_zero`

The original defect: score every track voxlevel 0 with a model loaded

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W1_voxlevel_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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

### `u58-workers-and-wav.W4_model_guard`

Drop the guard for a model that did not load

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W4_model_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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

### `u58-zero-row-remeasured.W6_gender_constant`

Report every scored track's gender as U

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-zero-row-remeasured.json`, row `W6_gender_constant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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

### `u212.T5_name_wraps`

tail.name: the name step's stop passed on without the passes that downloaded the copy

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T5_name_wraps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1608 against a baseline of 1608
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_name_stop_over_a_second_copy_names_the_pass_that_downloaded_it`
  - `tests/test_sync_land_staged.py::test_a_second_copy_no_download_job_records_is_said_so`

Old text:

```
        raise second_copies(stop, cfg) from None
```

New text:

```
        raise stop from None
```

### `u212.S1_missing_ends`

sync_land._missing: nothing listed ends the pass whatever is staged

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S1_missing_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 318 against a baseline of 318
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`

Old text:

```
    if (envelope.get("outcome") == str(Outcome.NO_OP) or not listed) and not staged:
```

New text:

```
    if envelope.get("outcome") == str(Outcome.NO_OP) or not listed:
```

### `u212.S4_staged_said`

sync_land._missing: the missing row drops the staged clause, so the pass does not say how many it skipped

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S4_staged_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 318 against a baseline of 318
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses`

Old text:

```
        + (f"; {staged} more {held}" if staged else ""),
```

New text:

```
        + "",
```

### `u223.M3_no_clear`

staged_path: clear nothing, so a stale report and scratch leak into the next attempt

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M3_no_clear`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_tag_workers.py`
- Collected: 274 against a baseline of 274
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_linked_intent_is_cleared_rather_than_kept_and_followed`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`

Old text:

```
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()
```

New text:

```
            continue
```

### `u192.A1_run_queue_only_ignored`

analyze_run: ignore --queue-only and drive the job

- File: `src/cratekit/analysis/cli.py`
- Source: `u192.json`, row `A1_run_queue_only_ignored`
- Moved: Anchored where u325-replay-after.json replayed it: Same branch in analyze_run; U298 replaced the local _reported with core.jobs.reported
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 11 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`
  - `tests/test_analysis_workers.py::test_an_item_renamed_before_its_row_moved_resumes_as_finished`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[run]`
  - `tests/test_analysis_workers.py::test_the_shared_tail_step_queues_only_and_drives_its_job_once`

Old text:

```
        if foreground.queue_only(ctx.args):
            return ctx.envelope(data=jobs.reported(store, job))
```

New text:

```
        if False:
            return ctx.envelope(data=jobs.reported(store, job))
```

### `u306.A3_walk_recursive`

analysis.cli.walk_folder: ignore --recursive, so a nested file is never queued by restamp or vocals

- File: `src/cratekit/analysis/cli.py`
- Source: `u306.json`, row `A3_walk_recursive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 18 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_nested_appledouble_sidecar_and_a_dot_directory_are_not_items`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_freezes_the_flag_in_the_payload`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_queues_every_nested_file_once_in_sorted_order`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_runs_every_nested_item_to_done_and_writes_the_right_file`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_says_which_linked_folders_it_did_not_walk`
  - `tests/test_analysis_workers.py::test_a_restamp_driven_at_its_queue_names_a_linked_folder_once`
  - `tests/test_analysis_workers.py::test_a_tree_whose_only_folders_are_links_says_so_on_the_zero`
  - `tests/test_analysis_workers.py::test_the_resume_repeats_what_the_walk_left_out_rather_than_only_the_queue`
  - `tests/test_analysis_workers.py::test_two_nested_folders_holding_the_same_filename_are_two_items`
  - `tests/test_vocals_cli.py::test_a_nested_file_deleted_after_the_vocals_queue_refuses_that_item_only`
  - `tests/test_vocals_cli.py::test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_queues_every_nested_file_once_in_sorted_order`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_says_which_linked_folders_it_did_not_walk`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    recursive = bool(getattr(ctx.args, "recursive", False))
```

New text:

```
    recursive = False
```

### `u93-recursive-analysis.D21_restamp_flag`

The restamp queue ignores the flag and always scans one level

- File: `src/cratekit/analysis/cli.py`
- Source: `u93-recursive-analysis.json`, row `D21_restamp_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 18 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_nested_appledouble_sidecar_and_a_dot_directory_are_not_items`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_freezes_the_flag_in_the_payload`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_queues_every_nested_file_once_in_sorted_order`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_runs_every_nested_item_to_done_and_writes_the_right_file`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_says_which_linked_folders_it_did_not_walk`
  - `tests/test_analysis_workers.py::test_a_restamp_driven_at_its_queue_names_a_linked_folder_once`
  - `tests/test_analysis_workers.py::test_a_tree_whose_only_folders_are_links_says_so_on_the_zero`
  - `tests/test_analysis_workers.py::test_the_resume_repeats_what_the_walk_left_out_rather_than_only_the_queue`
  - `tests/test_analysis_workers.py::test_two_nested_folders_holding_the_same_filename_are_two_items`
  - `tests/test_vocals_cli.py::test_a_nested_file_deleted_after_the_vocals_queue_refuses_that_item_only`
  - `tests/test_vocals_cli.py::test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_queues_every_nested_file_once_in_sorted_order`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_says_which_linked_folders_it_did_not_walk`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    recursive = bool(getattr(ctx.args, "recursive", False))
    scan = discovery.scan_audio(folder, recursive=recursive)
```

New text:

```
    recursive = bool(getattr(ctx.args, "recursive", False))
    scan = discovery.scan_audio(folder, recursive=False)
```

### `r221-a.S3_flag_reads_a_key_nothing_freezes`

Read the rehearsal flag under a name the build does not freeze, so every job reads as a real backup

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `S3_flag_reads_a_key_nothing_freezes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 7 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_rehearsal_says_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
    return bool((job.payload or {}).get(DRY_RUN))
```

New text:

```
    return bool((job.payload or {}).get("rehearsal"))
```

### `r221-a.W1_rehearsal_never_said`

The warning is never carried, which is the exact state the ledger entry describes

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W1_rehearsal_never_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
    return (rehearsal_warning(),) if _is_rehearsal(job) else ()
```

New text:

```
    return ()
```

### `r221-a.W2_rehearsal_said_unconditionally`

Every run is told it copied nothing, including the real one that copied and published, which is the same defect pointing the other way

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W2_rehearsal_said_unconditionally`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_asking_for_a_backup_twice_reports_the_open_job_rather_than_a_second`
  - `tests/test_backup_cli.py::test_the_flag_on_the_envelope_is_the_jobs_own_and_not_the_command_lines`

Old text:

```
    return (rehearsal_warning(),) if _is_rehearsal(job) else ()
```

New text:

```
    return (rehearsal_warning(),)
```

### `r221-b.M1_refusal_step_dropped`

No refusal carries the sentence, so a rehearsal that failed reads as a real backup attempt that fell over

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `M1_refusal_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_rehearsal_says_which_kind_of_run_it_was`

Old text:

```
    if not _is_rehearsal(job):
        return error
    cause = error.cause
```

New text:

```
    return error
    cause = error.cause
```

### `r221-b.M2_refusal_step_unconditional`

Every refusal gains the sentence, so a person whose REAL backup failed is told nothing was copied and stops looking for the half that was

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `M2_refusal_step_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_real_backup_that_ended_badly_gains_no_rehearsal_step`
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_real_run_gains_no_rehearsal_step`

Old text:

```
    if not _is_rehearsal(job):
        return error
    cause = error.cause
```

New text:

```
    cause = error.cause
```

### `r349-a.A1_failure_write`

Drop the failure path JSON write: raise the refusal without writing the outcome

- File: `src/cratekit/backup/cli.py`
- Source: `r349-a.json`, row `A1_failure_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_the_outcome_record_is_private_under_a_permissive_umask`

Old text:

```
            raise _with_outcome_recorded(refusal, outcome, outcome_to)
```

New text:

```
            raise refusal
```

### `r349-a.A2_success_produced`

The handler returns nothing on success instead of the staged record

- File: `src/cratekit/backup/cli.py`
- Source: `r349-a.json`, row `A2_success_produced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_handler_uses_the_configuration_it_was_handed`
  - `tests/test_backup_cli.py::test_the_outcome_record_is_private_under_a_permissive_umask`

Old text:

```
    return jobs.Produced(staged=staged, final=final)
```

New text:

```
    return None
```

### `r349-a.A4_envelope_field`

The backup run --job envelope stops attaching the outcomes field

- File: `src/cratekit/backup/cli.py`
- Source: `r349-a.json`, row `A4_envelope_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`

Old text:

```
        progress[OUTCOMES] = outcomes
```

New text:

```
        pass
```

### `r349-b.B3_clear_before_attempt`

The handler no longer clears the previous attempt's record

- File: `src/cratekit/backup/cli.py`
- Source: `r349-b.json`, row `B3_clear_before_attempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    backup_facts.clear_outcome(job.job_id, named)
    report = perform_backup(
```

New text:

```
    report = perform_backup(
```

### `r349-b.B4_stage_error_completes`

A staging write error escapes the handler instead of completing the item

- File: `src/cratekit/backup/cli.py`
- Source: `r349-b.json`, row `B4_stage_error_completes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    except OSError:
        return None
    return jobs.Produced
```

New text:

```
    except KeyError:
        return None
    return jobs.Produced
```

### `r390-a.A6_backup_transfer_exit_is_permanent`

the flag the review round added: a transfer exit recorded with no retryable flag

- File: `src/cratekit/backup/cli.py`
- Source: `r390-a.json`, row `A6_backup_transfer_exit_is_permanent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_decides_the_run_even_when_the_other_completed`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`

Old text:

```
            retryable=True,
            origin=("backup", "cli"),
            detail={"portions": [entry.portion.value for entry in failed]},
```

New text:

```
            origin=("backup", "cli"),
            detail={"portions": [entry.portion.value for entry in failed]},
```

### `u45-round-1.A1_unreadable_reported_as_absent`

Return an empty list for an unreadable fact file, so a library with a good backup reads as never backed up

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `A1_unreadable_reported_as_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_fact_file_that_cannot_be_read_refuses_rather_than_reporting_nothing`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_real_run_gains_no_rehearsal_step`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_rehearsal_says_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`
  - `tests/test_backup_cli.py::test_the_remedy_for_an_unreadable_fact_file_travels_from_the_exception`

Old text:

```
    except backup_facts.BackupFactsUnreadable as exc:
        raise refuse(
            "backup-facts-unreadable",
```

New text:

```
    except backup_facts.BackupFactsUnreadable as exc:
        del exc
        return []
        raise refuse(
            "backup-facts-unreadable",
```

### `u45-round-1.A4_state_collapsed_to_known`

Report every portion as known, so never-recorded and recorded-in-the-future both read as a current backup

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `A4_state_collapsed_to_known`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
            "state": str(entry.state),
            "age_seconds"
```

New text:

```
            "state": "known",
            "age_seconds"
```

### `u45-round-1.C2_refusal_read_as_failure`

Widen the failed predicate to any portion that did not run, so a refused database portion reads as a failed transfer

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C2_refusal_read_as_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_nothing_that_ran_is_never_reported_as_a_refusal`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
        entry for entry in outcome.portions if not entry.ran and entry.refusal is None
```

New text:

```
        entry for entry in outcome.portions if not entry.ran
```

### `u45-round-1.C3_nothing_ran_accepted`

Return None when no portion ran, so a machine with no rclone exits OK over a backup that did not happen

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C3_nothing_ran_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 8 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_a_real_backup_that_ended_badly_gains_no_rehearsal_step`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_outcome_with_no_portions_refuses_rather_than_raising`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
    if any(entry.ran for entry in outcome.portions):
        return None
    refusals
```

New text:

```
    return None
    refusals
```

### `u45-round-1.C4_uniform_refusal_flattened`

Drop the uniform pass-through so every no-run refusal becomes the summary slug and rclone-missing loses install-binary

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C4_uniform_refusal_flattened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`

Old text:

```
    if len(refusals) == 1:
        only = next(iter(refusals))
```

New text:

```
    if False:
        only = next(iter(refusals))
```

### `u45-round-1.C5_first_refusal_taken`

Take the first portion's refusal when the reasons differ, rather than naming all of them

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C5_first_refusal_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
    if len(refusals) == 1:
```

New text:

```
    if refusals:
```

### `u45-round-1.C6_partial_run_refused`

Refuse whenever any portion did not run, so a mirror that completed while the database was skipped is reported as a failure

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C6_partial_run_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_an_outcome_with_no_portions_refuses_rather_than_raising`
  - `tests/test_backup_cli.py::test_nothing_that_ran_is_never_reported_as_a_refusal`

Old text:

```
    if any(entry.ran for entry in outcome.portions):
        return None
```

New text:

```
    if all(entry.ran for entry in outcome.portions):
        return None
```

### `u45-round-1.H2_queueing_plans_first`

Plan inside the handler, so queueing refuses on a machine with no rclone where the work would have run fine

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `H2_queueing_plans_first`
- Moved: Anchored where u325-replay-after.json replayed it: Same handler, backup_library; U298 replaced its private _load with cli.output.load_config, so the line the plan is inserted after is reworded and the insertion point is the same
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_queueing_needs_no_rclone_no_remote_and_no_volume`

Old text:

```
    cfg = load_config(("backup.cli",))
    with jobs.open_store() as store:
        if ctx.args.job:
```

New text:

```
    cfg = load_config(("backup.cli",))
    backup.plan_backup(cfg)
    with jobs.open_store() as store:
        if ctx.args.job:
```

### `u45-round-1.R1_reserved_remediation_discarded`

Replace the reservation table's per-slug remediation with the class default, which is what the first draft did

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `R1_reserved_remediation_discarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_an_unconfigured_remote_refuses_in_the_backup_vocabulary`

Old text:

```
            remediation=reservations.remediation_for(slug),
```

New text:

```
            remediation=Remediation(),
```

### `u45-round-1.R2_slug_flattened`

Fold every engine refusal into one slug, so nine diagnoses arrive as one and each loses its own fix

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `R2_slug_flattened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_an_unconfigured_remote_refuses_in_the_backup_vocabulary`

Old text:

```
    slug = str(refusal)
    return CratekitError(
```

New text:

```
    slug = str(backup.Refusal.RCLONE_MISSING)
    return CratekitError(
```

### `u45-round-1.W2_report_from_the_plan`

Report the PLAN rather than the OUTCOME, which is the shell half of the first-caller defect

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W2_report_from_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 10 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_every_command_the_engine_ran_is_paired_with_its_own_return_code`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    report = backup.outcome_payload(outcome)
```

New text:

```
    report = backup.plan_payload(plan)
```

### `u45-round-1.W3_ages_not_read_back`

Drop the age read-back, so the verb never reports what a destructive session would see

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W3_ages_not_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    report["ages"] = published_ages(cfg, now=now)
```

New text:

```
    report["ages"] = []
```

### `u45-round-1.W4_ages_derived_from_the_outcome`

Derive the published ages from the outcome instead of reading the fact file, the duplicate rule the module argues against

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W4_ages_derived_from_the_outcome`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    report["ages"] = published_ages(cfg, now=now)
```

New text:

```
    report["ages"] = [
        {"portion": p.portion.value, "state": "known" if p.ran else "never-recorded"}
        for p in outcome.portions
    ]
```

### `u45-round-1.W5_publishing_switched_off`

Pass publish=False, so a successful backup records no age and the write session still sees never-recorded

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W5_publishing_switched_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 8 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_a_supplied_configuration_is_used_rather_than_the_one_on_disk`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - `tests/test_backup_cli.py::test_the_report_carries_the_age_number_and_not_only_the_state`

Old text:

```
    outcome = backup.run_backup(cfg, plan, runner=runner, now=now, dry_run=dry_run)
```

New text:

```
    outcome = backup.run_backup(
        cfg, plan, runner=runner, now=now, dry_run=dry_run, publish=False
    )
```

### `u45-round-1.W6_rehearsal_becomes_a_real_run`

Ignore the frozen dry-run key, so a rehearsal transfers for real and publishes an age

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W6_rehearsal_becomes_a_real_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    dry_run = bool(payload.get(DRY_RUN))
```

New text:

```
    dry_run = False
```

### `u45-round-1.W8_engine_refusal_escapes`

Let BackupRefused escape, so an unconfigured remote reaches the dispatcher as internal-error with report-defect

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W8_engine_refusal_escapes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_unconfigured_remote_refuses_in_the_backup_vocabulary`

Old text:

```
    except backup.BackupRefused as exc:
        raise _engine_refusal(
            exc.refusal, exc.detail, library=str(cfg.library.root)
        ) from exc
```

New text:

```
    except backup.BackupRefused:
        raise
```

### `u45-round-2.A3_age_seconds_always_none`

Report no age number even for a known portion, so the value R15's warning quotes never reaches the report

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-2.json`, row `A3_age_seconds_always_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_report_carries_the_age_number_and_not_only_the_state`

Old text:

```
            "age_seconds": entry.age.total_seconds() if entry.age is not None else None,
```

New text:

```
            "age_seconds": None,
```

### `u45-round-2.C7_failed_detail_dropped`

Reword the transfer-failed message so it no longer says a destructive session still sees the previous age

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-2.json`, row `C7_failed_detail_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_transfer_failure_says_no_age_was_published`

Old text:

```
            + ". No backup age was published for that portion, so a destructive "
            "session still sees whatever the last successful run left",
```

New text:

```
            + ". The run stopped there.",
```

### `u50-author.B1_no_items_enqueued`

Queue the backup with no items, so the driver has nothing to claim and reports an empty success

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `B1_no_items_enqueued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 30 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion_and_a_bound_worker`
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_a_resume_reports_the_queued_job_rather_than_filing_a_second`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - ... and 15 more, see the JSON sidecar

Old text:

```
            item_ids=backup_items(),
```

New text:

```
(empty)
```

### `u50-author.B3_items_one_portion_only`

Queue only the mirror, so the database half of every backup is never claimed

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `B3_items_one_portion_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 14 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion_and_a_bound_worker`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_backup_cli.py::test_queueing_still_needs_nothing_from_the_machine`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - `tests/test_backup_cli.py::test_the_item_list_is_derived_from_the_portions_rather_than_written_out`
  - `tests/test_backup_cli.py::test_the_outcome_record_is_private_under_a_permissive_umask`

Old text:

```
    return tuple(str(portion) for portion in backup_facts.Portion)
```

New text:

```
    return (str(backup_facts.Portion.FILES),)
```

### `u50-author.W1_no_narrowing`

Ignore the portion and run the whole plan for every item, so each item does the whole backup

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `W1_no_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if portion is not None:
```

New text:

```
    if False:
```

### `u50-author.W5_unknown_portion_unchecked`

Let an undeclared item name raise out of the coercion rather than refusing by name

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `W5_unknown_portion_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`

Old text:

```
        raise refuse(
            "internal-error",
            f"this job's item is {named!r}, which is not a backup portion this "
            f"build declares. The portions are {', '.join(declared)}",
```

New text:

```
        raise refuse(
            "internal-error",
            "the item could not be read",
```

### `u50-author.W6_fresh_config_in_the_handler`

Load the configuration in the handler rather than using the one frozen on the job (KTD9)

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `W6_fresh_config_in_the_handler`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 19 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_resume_reports_the_queued_job_rather_than_filing_a_second`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_that_is_absent_is_warned_at_queue_and_at_resume`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_real_run_gains_no_rehearsal_step`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_rehearsal_says_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - `tests/test_backup_cli.py::test_the_configuration_the_worker_runs_against_is_the_frozen_one`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        cfg=cfg,
        # RESOLVED AT CALL TIME, not left to the default, so a test can put a
        # stand-in in front of it. ``perform_backup``'s own default is bound when
        # this module is imported and cannot be reached any other way.
        runner=backup.subprocess_runner,
```

New text:

```
        cfg=_load(),
        runner=backup.subprocess_runner,
```

### `u50-review-fixes.R2_empty_job_guard_dropped`

Drive a job with no items, so a job queued by the previous build reports SUCCEEDED over a library nothing copied

- File: `src/cratekit/backup/cli.py`
- Source: `u50-review-fixes.json`, row `R2_empty_job_guard_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_queued_before_the_worker_existed_refuses_rather_than_succeeding`

Old text:

```
                _refuse_an_empty_job(store, job)
```

New text:

```
(empty)
```

### `u50-zero-rows.W4b_item_ignored_entirely`

Back up the mirror whatever the item says, so every item of the job does the same half

- File: `src/cratekit/backup/cli.py`
- Source: `u50-zero-rows.json`, row `W4b_item_ignored_entirely`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 12 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - `tests/test_backup_cli.py::test_the_outcome_record_is_private_under_a_permissive_umask`

Old text:

```
    named = str(item.item_id or "")
```

New text:

```
    named = str(backup_facts.Portion.FILES)
```

### `r349-a.A3_job_show_field`

job show stops attaching the outcomes field

- File: `src/cratekit/cli/jobs.py`
- Source: `r349-a.json`, row `A3_job_show_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`

Old text:

```
        summary[backup_facts.OUTCOMES_FIELD] = outcomes
```

New text:

```
        pass
```

### `r349-c.C1_prune_recorded`

The prune calls the bare runner, so its commands are not recorded beside its results

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r349-c.json`, row `C1_prune_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`, `tests/modules/test_tools.py`
- Collected: 277 against a baseline of 277
- Kills: 29 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_backup_payload_carries_a_version`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_resume_reports_the_queued_job_rather_than_filing_a_second`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_a_supplied_configuration_is_used_rather_than_the_one_on_disk`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - ... and 14 more, see the JSON sidecar

Old text:

```
                    runner=recorded,
```

New text:

```
                    runner=runner,
```

### `r349-c.C4_argv_rendered`

outcome_payload renders the label where the argv belongs

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r349-c.json`, row `C4_argv_rendered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`, `tests/modules/test_tools.py`
- Collected: 277 against a baseline of 277
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_every_command_the_engine_ran_is_paired_with_its_own_return_code`

Old text:

```
                        "argv": list(command.argv),
```

New text:

```
                        "argv": [command.label],
```

### `u311.B3_iso_drops_a_present_moment`

The backup ages report a recorded moment as none

- File: `src/cratekit/backup/cli.py`
- Source: `u311.json`, row `B3_iso_drops_a_present_moment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`
- Collected: 218 against a baseline of 218
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_report_carries_the_age_number_and_not_only_the_state`

Old text:

```
    return moment.isoformat() if moment is not None else None
```

New text:

```
    return None
```

### `u132.D1_doctor_behind`

Doctor reads a copy behind the shipped schema as OK

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u132.json`, row `D1_doctor_behind`
- Moved: Anchored where u303-replay-merged6.json replayed it: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2220 against a baseline of 2220
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_current_copy_with_every_entry_is_ok`
  - `tests/test_doctor.py::test_a_version_2_copy_without_favorites_is_named_with_both_versions`

Old text:

```
    if not found.behind:

```

New text:

```
    if found.behind:

```

### `u132.D2_doctor_defect`

Doctor reports a shipped template defect as the copy not compared

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u132.json`, row `D2_doctor_defect`
- Moved: Anchored where u303-replay-merged6.json replayed it: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2220 against a baseline of 2220
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_shipped_template_that_does_not_load_is_a_defect_and_not_the_copy`

Old text:

```
        if exc.cause.reason == "internal-error":

```

New text:

```
        if False:

```

### `r1761.P13_history_record_ignored`

_history: the record is not read, so an upgrade from a record with no census has no history

- File: `src/cratekit/modules/tools/backup_proof.py`
- Source: `r1761.json`, row `P13_history_record_ignored`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_proof.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 406 against a baseline of 406
- Kills: 77 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`
  - `tests/modules/test_tools.py::test_a_dry_run_publishes_no_backup_age`
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_failed_portion_publishes_no_age`
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_keep_of_zero_is_still_a_keep_of_zero`
  - `tests/modules/test_tools.py::test_a_marker_that_cannot_be_written_warns_and_does_not_fail_the_backup`
  - `tests/modules/test_tools.py::test_a_record_that_cannot_be_read_purges_nothing`
  - `tests/modules/test_tools.py::test_a_refused_portion_leaves_its_previous_age_untouched`
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/modules/test_tools.py::test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_run_that_overwrote_nothing_still_keeps_the_newest_settled_archive`
  - ... and 62 more, see the JSON sidecar

Old text:

```
        manifest is not None
        and manifest.library_root == str(cfg.library.root)
```

New text:

```
        manifest is None
        and manifest.library_root == str(cfg.library.root)
```

### `u281.S1_beatport_reads_no_refusal`

_search_beatport: drop the shared refusal check, so a 403 is unreachable and a 200 challenge a parse break, as before the card

- File: `src/cratekit/tagging/shops.py`
- Source: `u281.json`, row `S1_beatport_reads_no_refusal`
- Moved: Anchored where u306-replay-after-a.json replayed it: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`
- Collected: 447 against a baseline of 447
- Kills: 22 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_200_challenge_beside_an_unread_discogs_refuses_as_unreachable_not_parse_broken`
  - `tests/test_beatport_refusal.py::test_a_200_just_a_moment_page_is_blocked_not_a_parse_break`
  - `tests/test_beatport_refusal.py::test_a_200_page_carrying_only_cloudflares_script_is_blocked`
  - `tests/test_beatport_refusal.py::test_a_403_carrying_cloudflares_challenge_header_is_blocked_and_named`
  - `tests/test_beatport_refusal.py::test_a_403_without_the_header_is_blocked_and_says_only_the_status`
  - `tests/test_beatport_refusal.py::test_a_429_that_outlasts_the_backoff_is_blocked_as_the_fallbacks_read_it`
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_a_new_run_asks_again_from_its_first_file`
  - `tests/test_beatport_refusal.py::test_a_searcher_given_no_count_keeps_its_own_for_its_life`
  - `tests/test_beatport_refusal.py::test_a_stopped_beatport_and_a_discogs_with_no_token_refuse_rather_than_decline`
  - `tests/test_beatport_refusal.py::test_a_stopped_catalogue_is_answered_without_a_wait`
  - `tests/test_beatport_refusal.py::test_another_mitigation_is_not_called_a_challenge`
  - `tests/test_beatport_refusal.py::test_blocked_miss_blocked_blocked_does_not_stop_the_run`
  - `tests/test_beatport_refusal.py::test_deezer_is_still_not_asked_beside_a_blocked_beatport[not-sent]`
  - `tests/test_beatport_refusal.py::test_deezer_is_still_not_asked_beside_a_blocked_beatport[refused]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
    tracks = None if page.text is None else _beatport_tracks(page.text)
    if tracks is None:
        refused = unread_outcome(BEATPORT, page)
        if refused is not None:
            return refused
        return SourceOutcome(
```

New text:

```
    if page.text is None:
        return SourceOutcome(BEATPORT, Answer.UNREACHABLE, note=page.note)
    tracks = _beatport_tracks(page.text)
    if tracks is None:
        return SourceOutcome(
```

### `u281.R1_stop_after_four`

Refusals.stopped: stop only once the count passes the limit, so four refusals are sent, not three

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R1_stop_after_four`
- Moved: Anchored where u306-replay-after-a.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 11 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_a_new_run_asks_again_from_its_first_file`
  - `tests/test_beatport_refusal.py::test_a_searcher_given_no_count_keeps_its_own_for_its_life`
  - `tests/test_beatport_refusal.py::test_a_stopped_beatport_and_a_discogs_with_no_token_refuse_rather_than_decline`
  - `tests/test_beatport_refusal.py::test_a_stopped_catalogue_is_answered_without_a_wait`
  - `tests/test_beatport_refusal.py::test_the_binder_hands_the_run_count_to_the_searcher`
  - `tests/test_beatport_refusal.py::test_the_count_is_per_catalogue_so_a_refusing_one_never_stops_an_answering_one`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
        if self.running.get(source, 0) < self.limit:
```

New text:

```
        if self.running.get(source, 0) <= self.limit:
```

### `u281.R2_limit_two`

REFUSALS_BEFORE_STOP: two rather than three, a moment's challenge stops the run

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R2_limit_two`
- Moved: Anchored where u306-replay-after-a.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 12 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_match_resets_the_count_as_a_miss_does`
  - `tests/test_beatport_refusal.py::test_a_new_run_asks_again_from_its_first_file`
  - `tests/test_beatport_refusal.py::test_a_searcher_given_no_count_keeps_its_own_for_its_life`
  - `tests/test_beatport_refusal.py::test_an_outage_between_refusals_ends_the_run_of_them`
  - `tests/test_beatport_refusal.py::test_blocked_miss_blocked_blocked_does_not_stop_the_run`
  - `tests/test_beatport_refusal.py::test_the_binder_hands_the_run_count_to_the_searcher`
  - `tests/test_beatport_refusal.py::test_the_count_is_per_catalogue_so_a_refusing_one_never_stops_an_answering_one`
  - `tests/test_beatport_refusal.py::test_the_limit_is_three`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
REFUSALS_BEFORE_STOP = 3
```

New text:

```
REFUSALS_BEFORE_STOP = 2
```

### `u281.W2_searcher_ignores_the_handed_count`

catalogue_searcher: build its own count whatever it is handed, so a worker's per file searcher starts again every file

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `W2_searcher_ignores_the_handed_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 10 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_a_new_run_asks_again_from_its_first_file`
  - `tests/test_beatport_refusal.py::test_a_stopped_beatport_and_a_discogs_with_no_token_refuse_rather_than_decline`
  - `tests/test_beatport_refusal.py::test_a_stopped_catalogue_is_answered_without_a_wait`
  - `tests/test_beatport_refusal.py::test_the_binder_hands_the_run_count_to_the_searcher`
  - `tests/test_beatport_refusal.py::test_the_count_is_per_catalogue_so_a_refusing_one_never_stops_an_answering_one`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
    counted = Refusals() if refusals is None else refusals
```

New text:

```
    counted = Refusals()
```

### `u281.W5_run_never_changes`

for_run: keep the first run's count for every later run, so the next sweep never asks a stopped catalogue

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `W5_run_never_changes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 4 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_run_met_again_after_another_starts_afresh`
  - `tests/test_beatport_refusal.py::test_one_run_name_is_one_count_and_another_name_a_fresh_one`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
    if not _run_refusals or _run_refusals[0][0] != run:
```

New text:

```
    if not _run_refusals:
```

### `u306.S1_shop_query`

searchers.catalogue_searcher: hand the shops a query builder that does not escape, so every Beatport, Traxsource and Bandcamp URL carries raw spaces and ampersands

- File: `src/cratekit/tagging/searchers.py`
- Source: `u306.json`, row `S1_shop_query`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 205 against a baseline of 205
- Kills: 14 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_an_artist_and_title_that_need_escaping_reach_the_seam_as_a_quoted_url`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_four_real_misses_are_no_hit_and_carry_no_unread_warning`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
            artist, title, fetch=touch, pacer=pacer, declared=declared, track=track, query=_query
```

New text:

```
            artist, title, fetch=touch, pacer=pacer, declared=declared, track=track, query=lambda *parts: " ".join(parts)
```

### `u56-catalogue-searcher-and-tag-workers.R5_bare_alias_lookup`

The defect the document review found: hand roll the resolution out of tagging_alias instead of routing.suggest_tag, which loses the sub display and every declared refusal

- File: `src/cratekit/tagging/searchers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R5_bare_alias_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 29 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_genre_costs_one_fetch_and_its_picture_is_the_original`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_no_genre_spends_a_second_fetch_on_the_track_page`
  - `tests/test_catalogue_searcher.py::test_a_beatport_hit_carries_its_release_picture_resized_to_the_source_edge`
  - `tests/test_catalogue_searcher.py::test_a_beatport_match_carries_the_tag_the_source_name_and_the_raw_genre`
  - `tests/test_catalogue_searcher.py::test_a_beatport_miss_or_silence_falls_through_to_traxsource_which_names_itself[miss]`
  - `tests/test_catalogue_searcher.py::test_a_beatport_miss_or_silence_falls_through_to_traxsource_which_names_itself[unreachable]`
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[acapella]`
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[electronic]`
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[electronica]`
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[techno]`
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[declared tag with no bucket]`
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[padded genre]`
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[unknown word]`
  - `tests/test_catalogue_searcher.py::test_a_match_after_an_unreachable_source_names_it_in_unread_too`
  - ... and 14 more, see the JSON sidecar

Old text:

```
    suggestion = routing.suggest_tag(declared, outcome.source_genre)
    tag = suggestion.tag
    if suggestion.declined or not tag or declared.is_too_coarse_as_source(tag):
        tag = None
```

New text:

```
    hit = declared.tagging_alias(outcome.source_genre.casefold())
    tag = declared.bucket(hit[0]).display if hit is not None else None
```

### `r791-a.S1_403_blocks`

_BLOCK_STATUSES: drop 403, so Traxsource's Cloudflare 403 reads as unreachable again

- File: `src/cratekit/tagging/catalogues.py`
- Source: `r791-a.json`, row `S1_403_blocks`
- Moved: Anchored where u306-replay-after-d.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 239 against a baseline of 239
- Kills: 11 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_beatport_miss_beside_two_blocked_fallbacks_is_not_a_no_hit`
  - `tests/test_catalogue_searcher.py::test_a_fallbacks_refusal_is_blocked_and_its_outage_unreachable[403 interstitial]`
  - `tests/test_catalogue_searcher.py::test_beatport_answering_403_is_blocked_like_the_fallbacks`
  - `tests/test_catalogue_searcher.py::test_three_refusals_raise_unreachable_and_say_the_fallbacks_were_blocked`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
_BLOCK_STATUSES = frozenset({403, 429})
```

New text:

```
_BLOCK_STATUSES = frozenset({429})
```

### `u322.M13_beside_any_said_dropped`

Asked.unread_beside_an_answer: only an unread row is named, so a row written from Deezer while Beatport refused is silent

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M13_beside_any_said_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_row_written_from_deezer_while_beatport_refused_is_named_in_the_warning`
  - `tests/test_catalogue_walk_refusal.py::test_rows_are_sorted_by_why_they_were_not_read_whole`

Old text:

```
        if not any(word in _ANSWERED for _source, word in self.answers):
            return ()
        return self.unread_by
```

New text:

```
        if self.said != UNREAD or not any(word in _ANSWERED for _source, word in self.answers):
            return ()
        return self.unread_by
```

### `u322.M14_token_rows_said_no_token`

sort_unread: a row passed over for a refused token is said as no token recorded

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M14_token_rows_said_no_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 4 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_rejected_discogs_token_beside_a_beatport_that_answers_does_not_stop_the_walk`
  - `tests/test_catalogue_walk_refusal.py::test_rows_are_sorted_by_why_they_were_not_read_whole`
  - `tests/test_catalogue_walk_refusal.py::test_the_suggest_verb_says_a_token_that_could_not_be_used`
  - `tests/test_tag_backlog.py::test_a_token_discogs_refused_is_said_and_beatport_is_asked_on_every_row`

Old text:

```
        elif TOKEN_UNUSABLE in asked.note:
```

New text:

```
        elif False:
```

### `u27-reports-round-1.D2_required_gate`

Report a broken Trash as a failure even where no verb needs it

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-reports-round-1.json`, row `D2_required_gate`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_broken_trash_is_informational_when_no_verb_this_profile_needs_it`

Old text:

```
    if not inputs.required(key):
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{status.problem}, and no verb this profile switches on moves a "
                f"file to the Trash, so nothing depends on it today"
            ),
        )

```

New text:

```
(empty)
```

### `u27-reports-round-3-fixes.F3_trash_absent_is_a_failure`

Report a volume whose Trash has not been created yet as a failure again

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-reports-round-3-fixes.json`, row `F3_trash_absent_is_a_failure`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_with_no_trash_directory_yet_is_not_a_failure`

Old text:

```
    if status.absent:
```

New text:

```
    if False:
```

### `u27-round-8-independent.E1_mount_detail_swapped`

Swap the NOT_MOUNTED and MOUNTED_ELSEWHERE sentences, conflating unmounted with moved

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-round-8-independent.json`, row `E1_mount_detail_swapped`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`

Old text:

```
        preflight.MountState.NOT_MOUNTED: (
            "the recorded volume is not mounted anywhere and the configured root "
            "does not exist. Attach it"
        ),
        preflight.MountState.MOUNTED_ELSEWHERE: (
            "the recorded volume IS attached, at a different mount point than the "
            "configured root. Nothing needs plugging in; the configured root is "
            "pointing at the wrong place"
        ),
```

New text:

```
        preflight.MountState.NOT_MOUNTED: (
            "the recorded volume IS attached, at a different mount point than the "
            "configured root. Nothing needs plugging in; the configured root is "
            "pointing at the wrong place"
        ),
        preflight.MountState.MOUNTED_ELSEWHERE: (
            "the recorded volume is not mounted anywhere and the configured root "
            "does not exist. Attach it"
        ),
```

### `u27-round-8-independent.E2_identity_verdict_green`

Report the identity check GREEN for an absent and for a relocated volume

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-round-8-independent.json`, row `E2_identity_verdict_green`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_mounted_elsewhere_is_one_problem_reported_once`
  - `tests/test_doctor.py::test_an_unmounted_volume_never_reports_a_matching_identity`
  - `tests/test_doctor.py::test_the_identity_check_never_reports_green_over_an_identity_that_did_not_match`

Old text:

```
            preflight.MountState.NOT_MOUNTED: (Status.INFO, None),
            preflight.MountState.MOUNTED_ELSEWHERE: (Status.INFO, None),
```

New text:

```
            preflight.MountState.NOT_MOUNTED: (Status.OK, None),
            preflight.MountState.MOUNTED_ELSEWHERE: (Status.OK, None),
```

### `u27-round-8-independent.E3_found_at_dropped`

Stop telling the user where a relocated volume actually is

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u27-round-8-independent.json`, row `E3_found_at_dropped`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`

Old text:

```
    if status.state is preflight.MountState.MOUNTED_ELSEWHERE:
        where = f" (configured root {status.configured_root}, found at {status.found_at})"
```

New text:

```
(empty)
```

### `r-1.E1_dispatch_impl`

Existing guard, sample: drop the requirement that the hook invokes hook-impl

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `E1_dispatch_impl`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_hook_that_does_not_dispatch_to_this_repository_is_refused[#!/bin/sh\n# pre-commit\nexit 0\n-True-hook-impl]`

Old text:

```
    if _HOOK_DISPATCH not in body:
        return f"it never invokes pre-commit's {_HOOK_DISPATCH}"

```

New text:

```
(empty)
```

### `r-1.E2_config_inside_checkout`

Existing guard, sample: drop the requirement that the named configuration is inside the checkout

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `E2_config_inside_checkout`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_hook_that_does_not_dispatch_to_this_repository_is_refused[ARGS=(hook-impl --config=/elsewhere/.pre-commit-config.yaml --hook-type=pre-commit)\n-True-outside]`

Old text:

```
    if root.resolve() not in resolved.parents and resolved != root.resolve():
```

New text:

```
    if False:
```

### `r-1.T10_no_yaml_falls_back`

PyYAML missing falls back to the pre-commit floor instead of a sentence

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T10_no_yaml_falls_back`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_no_yaml_reader_is_unknown_rather_than_one_hook_type`

Old text:

```
    except ImportError:
        return (
            (),
            (
                f"PyYAML is not importable from this interpreter, so the hook types "
                f"{config_file.name} configures could not be read. Install the dev "
                f"extra, `pip install -e '.[dev]'`"
            ),
            None,
        )

```

New text:

```
    except ImportError:
        return ("pre-commit",), None, None

```

### `r-1.T12_caller_ignores_unknown`

The check ignores an unknown configuration and reports on no extra types

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T12_caller_ignores_unknown`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_that_does_not_parse_is_not_read_as_one_hook_type`
  - `tests/test_doctor.py::test_no_yaml_reader_is_unknown_rather_than_one_hook_type`

Old text:

```
    if unknown is not None:
```

New text:

```
    if False:
```

### `r-1.T13_missing_other_hook`

A configured hook type with no hook file is not reported

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T13_missing_other_hook`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configured_commit_msg_stage_with_no_hook_is_refused`
  - `tests/test_doctor.py::test_the_install_line_names_a_configuration_that_is_not_the_default`

Old text:

```
            absent.append(f"no {hook_type} hook at {other}")
            continue

```

New text:

```
            continue

```

### `r-1.T15_other_dispatch`

A configured hook that does not dispatch for its own stage is not reported

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T15_other_dispatch`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`

Old text:

```
        if other_problem is not None:
            absent.append(

```

New text:

```
        if other_problem is not None:
            continue
            absent.append(

```

### `r-1.T16_same_configuration`

Drop the requirement that every other hook dispatches to the pre-commit hook's configuration

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T16_same_configuration`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`

Old text:

```
        if _config_path(other_name, root).resolve() != config_file.resolve():
```

New text:

```
        if False:
```

### `r-1.T17_install_config_flag`

The install line never names a non-default configuration

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T17_install_config_flag`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_install_line_names_a_configuration_that_is_not_the_default`

Old text:

```
    if config_name != _HOOK_CONFIG_DEFAULT:
```

New text:

```
    if False:
```

### `r-1.T18_remedy_floor`

With no readable configuration the install line names no type at all

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T18_remedy_floor`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_clone_with_no_configuration_is_told_the_floor`

Old text:

```
    return _install_command(types if problem is None else ("pre-commit",))
```

New text:

```
    return _install_command(types)
```

### `r-1.T19_remedy_reads_config`

The fresh clone install line stops reading the configuration and names only pre-commit

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T19_remedy_reads_config`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_fresh_clone_is_told_the_whole_install_line`

Old text:

```
    types, problem, _remedy = _configured_hook_types(root / _HOOK_CONFIG_DEFAULT)
```

New text:

```
    types, problem, _remedy = ("pre-commit",), None, None
```

### `r-1.T20_stage_parameter`

The dispatch check ignores the hook type it was asked about and always wants pre-commit

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T20_stage_parameter`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`
  - `tests/test_doctor.py::test_every_configured_hook_type_installed_passes_the_check`

Old text:

```
    stage = f"--hook-type={hook_type}"
```

New text:

```
    stage = "--hook-type=pre-commit"
```

### `r-1.T21_ok_names_others`

The OK detail stops naming the other stages it verified

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T21_ok_names_others`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_every_configured_hook_type_installed_passes_the_check`

Old text:

```
        if len(types) > 1

```

New text:

```
        if False

```

### `r-1.T22_pre_commit_floor`

Pre-commit is no longer the floor of the needed types

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T22_pre_commit_floor`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 13 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`
  - `tests/test_doctor.py::test_a_configured_commit_msg_stage_with_no_hook_is_refused`
  - `tests/test_doctor.py::test_a_fresh_clone_is_told_the_whole_install_line`
  - `tests/test_doctor.py::test_every_configured_hook_type_installed_passes_the_check`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_install_hook_types: [pre-push]\nrepos: []\n-expected2]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_stages: [push]\nrepos: []\n-expected3]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[repos: []\n-expected0]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text1-expected1]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text5-expected5]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text6-expected6]`
  - `tests/test_doctor.py::test_the_install_line_names_a_configuration_that_is_not_the_default`
  - `tests/test_doctor.py::test_this_repositorys_own_configuration_needs_both_hook_types`

Old text:

```
    types = ["pre-commit"]
    for stage in named:

```

New text:

```
    types = []
    for stage in named:

```

### `r-1.T5_hook_stages`

Ignore every hook's own stages, the reading that finds this repository's commit-msg stage

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T5_hook_stages`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 12 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[text0-'on-commit']`
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[text1-installs no hook for]`
  - `tests/test_doctor.py::test_a_configured_commit_msg_stage_with_no_hook_is_refused`
  - `tests/test_doctor.py::test_a_fresh_clone_is_told_the_whole_install_line`
  - `tests/test_doctor.py::test_every_configured_hook_type_installed_passes_the_check`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text1-expected1]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text4-expected4]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text6-expected6]`
  - `tests/test_doctor.py::test_the_install_line_names_a_configuration_that_is_not_the_default`
  - `tests/test_doctor.py::test_this_repositorys_own_configuration_needs_both_hook_types`

Old text:

```
                named.extend(hook.get("stages") or [])
```

New text:

```
                pass
```

### `r-1.T9_yaml_error_falls_back`

A configuration that does not parse falls back to the pre-commit floor instead of a sentence

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r-1.json`, row `T9_yaml_error_falls_back`
- Moved: Anchored where u303-replay-merged4.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1685 against a baseline of 1685
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_that_does_not_parse_is_not_read_as_one_hook_type`

Old text:

```
    except yaml.YAMLError as exc:
        return (), f"{config_file} is not valid YAML ({exc})", None

```

New text:

```
    except yaml.YAMLError:
        return ("pre-commit",), None, None

```

### `u27-round-8-independent.C8_two_path_precondition`

Drop the both-paths-present precondition, so a one-path permission error is re-measured

- File: `src/cratekit/core/cause.py`
- Source: `u27-round-8-independent.json`, row `C8_two_path_precondition`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if exc.filename2 is not None and exc.filename is not None:
            path = _refused_of_two(exc, path)
```

New text:

```
        path = _refused_of_two(exc, path)
```

### `u212.M10_left_out`

missing_cli._listed: drop the staged clause of the left out refusal, so a run with a failed job and every finished row staged refuses

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M10_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok`

Old text:

```
    if left_out and not listed and not unlisted and not staged_rows:
```

New text:

```
    if left_out and not listed and not unlisted:
```

### `u212.M1_staged_match`

missing_cli._staged: never record a staged row, so a track a staged file carries is listed and downloaded again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M1_staged_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[204.flac]`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[Lumen Drift - Salt Road.flac]`
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[neither]`

Old text:

```
        if held:
            found.append((n, held[0].path))
```

New text:

```
        if held and False:
            found.append((n, held[0].path))
```

### `u212.M2_own_rows_both`

missing_cli._staged: drop the own rows rule, so a continued pass subtracts its own staged downloads and its list is refused over its earlier copy

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M2_own_rows_both`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-isrc]`
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-provider-id]`

Old text:

```
        if (ref and ref in ids) or token in isrcs:
            continue
```

New text:

```
        if False:
            continue
```

### `u212.M3_own_rows_by_id`

missing_cli._staged: the own rows rule by ISRC alone, the provider id half removed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M3_own_rows_by_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-provider-id]`

Old text:

```
        if (ref and ref in ids) or token in isrcs:
```

New text:

```
        if token in isrcs:
```

### `u212.M4_own_rows_by_isrc`

missing_cli._staged: the own rows rule by provider id alone, the ISRC half removed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M4_own_rows_by_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-isrc]`

Old text:

```
        if (ref and ref in ids) or token in isrcs:
```

New text:

```
        if ref and ref in ids:
```

### `u212.M5_unread_is_empty`

missing_cli._staged: an unreadable staging folder read as one holding nothing, so the staged row says nothing failed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M5_unread_is_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`

Old text:

```
        return _Staged(folder, unread=str(exc.strerror or exc))
```

New text:

```
        return _Staged(folder)
```

### `u212.M6_absent_folder`

missing_cli._staged: drop the absent folder guard, so a machine with no staging folder yet reports the folder unreadable

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M6_absent_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`

Old text:

```
        if not folder.exists():
```

New text:

```
        if False:
```

### `u212.M7_outcome_staged`

missing_cli._listed: every row staged answers no_op, so a pass ends before the landing that takes them

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M7_outcome_staged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`

Old text:

```
        outcome=Outcome.OK if listed or unlisted or staged_rows else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if listed or unlisted else Outcome.NO_OP,
```

### `u212.M8_summary_count`

missing_cli._listed: the summary's staged count read as zero, the number the pass reads

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M8_summary_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[204.flac]`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[Lumen Drift - Salt Road.flac]`

Old text:

```
        "staged": len(staged_rows),
```

New text:

```
        "staged": 0,
```

### `u212.M9_unread_status`

missing_cli._staged_check: an unreadable staging folder said on an info row rather than a failing one

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M9_unread_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_favorites_split.py`, `tests/test_inbox_refill.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_sync_mark.py`
- Collected: 1364 against a baseline of 1364
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`

Old text:

```
            "staged",
            "fail",
```

New text:

```
            "staged",
            "info",
```

### `u234.O18_snapshot_keeps_the_reading`

a snapshot that moved keeps the reading after the stop, so it outlives the stop it was read after

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u234.json`, row `O18_snapshot_keeps_the_reading`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_intake_land_twins.py`, `tests/test_outbound_order.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 1764 against a baseline of 1764
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_stopped.py::test_a_reading_after_a_stop_round_trips_and_goes_when_the_snapshot_moves`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
                stop_seen=None if moved else held.stop_seen,
```

New text:

```
                stop_seen=held.stop_seen,
```

### `u234.O19_reading_not_written`

the pair's document never writes the reading after the stop, so a later sync never finds it

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u234.json`, row `O19_reading_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_intake_land_twins.py`, `tests/test_outbound_order.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 1764 against a baseline of 1764
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped.py::test_a_reading_after_a_stop_round_trips_and_goes_when_the_snapshot_moves`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`

Old text:

```
        if self.stop_seen is not None:
            record["stop_seen"] = self.stop_seen.to_json()
```

New text:

```
        if False:
            record["stop_seen"] = self.stop_seen.to_json()
```

### `u248.L2_chosen_never_built`

_LazyChoices.__call__: never build the chosen verb, so it parses as an empty subparser with no handler

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L2_chosen_never_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`
- Collected: 1156 against a baseline of 1156
- Kills: 306 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale`
  - `tests/test_cli_contract.py::test_a_decision_naming_a_gate_the_verb_does_not_declare_is_refused`
  - `tests/test_cli_contract.py::test_a_defect_in_our_own_module_does_not_masquerade_as_a_missing_extra`
  - `tests/test_cli_contract.py::test_a_gate_is_answerable_from_a_different_process_in_a_later_session`
  - `tests/test_cli_contract.py::test_a_malformed_decision_is_refused_rather_than_ignored`
  - `tests/test_cli_contract.py::test_a_profile_that_switches_a_module_off_removes_its_verbs`
  - `tests/test_cli_contract.py::test_a_run_carrying_a_pending_action_reports_it_as_pending`
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_a_run_record_belongs_to_the_verb_that_created_it`
  - `tests/test_cli_contract.py::test_a_run_that_reached_a_gate_reports_it`
  - `tests/test_cli_contract.py::test_a_scripted_run_with_no_terminal_reaches_a_gate_and_exits_with_its_code`
  - `tests/test_cli_contract.py::test_a_verb_blocked_by_an_unverified_pending_action_refuses_before_doing_anything`
  - `tests/test_cli_contract.py::test_a_verb_that_exits_the_process_directly_is_converted_rather_than_obeyed`
  - `tests/test_cli_contract.py::test_a_verb_that_raises_something_unexpected_becomes_an_internal_cause`
  - `tests/test_cli_contract.py::test_an_unanswered_gate_exits_with_the_documented_code_and_leaves_the_run_resumable`
  - ... and 291 more, see the JSON sidecar

Old text:

```
        if waiting is not None:
            waiting.build()
```

New text:

```
        if waiting is not None:
            pass
```

### `u197.M2_retired_mapping_empty`

RETIRED_ADAPTER_NAMES: forget the vendored downloader's old key, so an older configuration names an unknown adapter

- File: `src/cratekit/core/config_schema.py`
- Source: `u197.json`, row `M2_retired_mapping_empty`
- Moved: Anchored where u299-replay-after-10.json replayed it: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_adapter_contract.py`
- Collected: 826 against a baseline of 826
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_retired_vendored_key_resolves_to_the_same_adapter`
  - `tests/test_config.py::test_a_file_naming_the_retired_adapter_key_reads_back_as_the_current_one`
  - `tests/test_config.py::test_only_a_retired_adapter_key_is_folded`
  - `tests/test_doctor.py::test_a_configuration_naming_the_retired_vendored_key_passes_the_adapter_check`

Old text:

```
RETIRED_ADAPTER_NAMES: Mapping[str, str] = MappingProxyType({"tidal_dl_ng": "vendored"})
```

New text:

```
RETIRED_ADAPTER_NAMES: Mapping[str, str] = MappingProxyType({})
```

### `u197.M1_config_fold`

_acquisition: return the section as written, so a file naming the retired key reaches doctor and every report under it

- File: `src/cratekit/core/config_validate.py`
- Source: `u197.json`, row `M1_config_fold`
- Moved: Anchored where u299-replay-after-4.json replayed it: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_adapter_contract.py`
- Collected: 826 against a baseline of 826
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_file_naming_the_retired_adapter_key_reads_back_as_the_current_one`
  - `tests/test_doctor.py::test_a_configuration_naming_the_retired_vendored_key_passes_the_adapter_check`

Old text:

```
    current = current_adapter_name(built.adapter)
    if current == built.adapter:
        return built
```

New text:

```
    current = current_adapter_name(built.adapter)
    if True:
        return built
```

### `u326.R3_library_root_redirected`

_block_real_library_paths: leave CRATEKIT_LIBRARY_ROOT as the process found it, the no real library path detonator

- File: `tests/conftest.py`
- Source: `u326.json`, row `R3_library_root_redirected`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_isolation_survives_undo.py`, `tests/test_outbound_workers.py`, `tests/test_label_workers.py`
- Collected: 460 against a baseline of 460
- Kills: 1 (killed)
- Killed:
  - `tests/test_isolation_survives_undo.py::test_every_redirect_survives_an_undo_of_the_body_s_own_patch`

Old text:

```
        monkeypatch.setenv("CRATEKIT_LIBRARY_ROOT", str(library))
```

New text:

```
        pass
```

### `u299.U7_library_extras_passed`

_library: the rollback effects, decision stores and sidecars an entry declares are dropped

- File: `src/cratekit/core/state_files.py`
- Source: `u299.json`, row `U7_library_extras_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_snapshot.py`, `tests/test_review_queue.py`, `tests/test_tombstones.py`
- Collected: 462 against a baseline of 462
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

### `r926.C1_root_is_state_roots_only`

The conftest registers its own state_roots folder rather than the base temp, so a save to a test's tmp_path is refused

- File: `tests/conftest.py`
- Source: `r926.json`, row `C1_root_is_state_roots_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 11 (killed)
- Killed:
  - `tests/test_config.py::test_a_failed_write_leaves_no_temporary_file_behind`
  - `tests/test_config.py::test_a_migration_backup_gets_the_same_mode_as_the_file_it_copies`
  - `tests/test_config.py::test_a_rewritten_config_is_not_served_from_the_memo`
  - `tests/test_config.py::test_a_save_under_a_relocation_writes_a_file_that_loads_again`
  - `tests/test_config.py::test_saving_creates_the_directory_only_when_it_writes`
  - `tests/test_config.py::test_the_fingerprint_survives_a_round_trip_through_disk`
  - `tests/test_config_migration.py::test_a_migration_that_cannot_take_the_lock_refuses`
  - `tests/test_config_migration.py::test_a_second_process_that_migrated_first_does_not_get_its_backup_clobbered`
  - `tests/test_config_migration.py::test_a_successful_migration_rewrites_the_file_and_keeps_a_backup`
  - `tests/test_config_test_root.py::test_a_write_to_a_tmp_path_lands_as_it_always_has`
  - `tests/test_config_test_root.py::test_with_the_isolation_a_save_lands_in_the_temporary_root`

Old text:

```
                config, "_TEST_WRITE_ROOT", tmp_path_factory.getbasetemp()
```

New text:

```
                config, "_TEST_WRITE_ROOT", root
```

### `r926.C2_root_never_registered`

The conftest never registers a root, the state a probe outside tests/ is in, for every test

- File: `tests/conftest.py`
- Source: `r926.json`, row `C2_root_never_registered`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 310 against a baseline of 310
- Kills: 30 (killed)
- Killed:
  - `tests/test_config.py::test_a_failed_write_leaves_no_temporary_file_behind`
  - `tests/test_config.py::test_a_migration_backup_gets_the_same_mode_as_the_file_it_copies`
  - `tests/test_config.py::test_a_rewritten_config_is_not_served_from_the_memo`
  - `tests/test_config.py::test_a_save_under_a_relocation_writes_a_file_that_loads_again`
  - `tests/test_config.py::test_every_file_and_directory_this_unit_creates_is_private_under_any_umask`
  - `tests/test_config.py::test_saving_creates_the_directory_only_when_it_writes`
  - `tests/test_config.py::test_the_default_location_round_trips_end_to_end`
  - `tests/test_config.py::test_the_fingerprint_survives_a_round_trip_through_disk`
  - `tests/test_config_migration.py::test_a_migration_that_cannot_take_the_lock_refuses`
  - `tests/test_config_migration.py::test_a_second_process_that_migrated_first_does_not_get_its_backup_clobbered`
  - `tests/test_config_migration.py::test_a_successful_migration_rewrites_the_file_and_keeps_a_backup`
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[durable-append]`
  - `tests/test_config_test_root.py::test_a_write_to_a_tmp_path_lands_as_it_always_has`
  - ... and 15 more, see the JSON sidecar

Old text:

```
                config, "_TEST_WRITE_ROOT", tmp_path_factory.getbasetemp()
```

New text:

```
                config, "_TEST_WRITE_ROOT", None
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

### `u326.R6_cyanite_refused`

_no_live_cyanite: leave the shipped Cyanite send in place, so a forgotten fake uploads to the paid service

- File: `tests/conftest.py`
- Source: `u326.json`, row `R6_cyanite_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_the_shipped_send_is_detonated_for_every_test`

Old text:

```
        monkeypatch.setattr(cyanite, "_requests_send", refused)
```

New text:

```
        pass
```

### `u40-author-full.F4_tombstone_indexed`

First caller sample: stop dropping tombstones from the active row index, so a removed track claims its location

- File: `src/cratekit/write/trees.py`
- Source: `u40-author-full.json`, row `F4_tombstone_indexed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_rebuild.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_splice_golden.py`
- Collected: 755 against a baseline of 755
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_soft_deleted_row_is_never_retagged`
  - `tests/test_rebuild.py::test_a_membership_pointing_at_a_soft_deleted_row_is_not_a_difference_either`
  - `tests/test_tree_writer.py::test_normalization_resolves_each_spelling_to_the_right_row[a-tombstone-beside-an-active-row]`

Old text:

```
    for row in rows:
        if row.deleted:
            continue
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
```

New text:

```
    for row in rows:
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
```

### `u27-round-8-independent.E4_path_missing_reads_ok`

A matching identity with an absent root resolves to OK instead of LIBRARY_PATH_MISSING

- File: `src/cratekit/core/preflight.py`
- Source: `u27-round-8-independent.json`, row `E4_path_missing_reads_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 738 against a baseline of 738
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unresolved_session_is_never_reported_clean_because_its_disk_is_gone`
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`
  - `tests/test_preflight.py::test_the_right_volume_with_a_missing_library_subdirectory_is_its_own_cause`
  - `tests/test_write_session.py::test_a_matched_volume_with_the_directory_absent_is_left_to_the_pass_that_follows_the_rule`

Old text:

```
            MountState.OK if root_exists else MountState.LIBRARY_PATH_MISSING,
```

New text:

```
            MountState.OK,
```

### `u27-round-8-independent.E5_unmounted_reads_foreign`

An absent volume resolves to FOREIGN_VOLUME instead of NOT_MOUNTED

- File: `src/cratekit/core/preflight.py`
- Source: `u27-round-8-independent.json`, row `E5_unmounted_reads_foreign`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_preflight.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 738 against a baseline of 738
- Kills: 5 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`
  - `tests/test_doctor.py::test_the_wizard_refuses_to_write_when_the_volume_is_not_mounted_at_all`
  - `tests/test_preflight.py::test_a_volume_that_is_not_mounted_refuses_with_its_own_cause`
  - `tests/test_preflight.py::test_the_three_refusals_are_distinguishable_from_each_other`
  - `tests/test_write_session.py::test_a_recorded_volume_that_is_not_mounted_anywhere_has_its_own_slug`

Old text:

```
        MountState.NOT_MOUNTED if not root_exists else MountState.FOREIGN_VOLUME,
```

New text:

```
        MountState.FOREIGN_VOLUME,
```

### `r318.P1_withdrawn_branch_removed`

row_placement: never answer withdrawn, so a track imported then removed in rekordbox is reported as never imported and the person is sent to import it again

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P1_withdrawn_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 423 against a baseline of 423
- Kills: 5 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_location_reaching_only_soft_deleted_rows_is_withdrawn`
  - `tests/test_deferred_routing.py::test_a_track_deleted_after_import_is_surfaced`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn-twice]`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn]`

Old text:

```
    if removed.outcome in (trees.MatchOutcome.MATCHED, trees.MatchOutcome.AMBIGUOUS):
        # A row exists and every one of them is a tombstone: imported once, then
```

New text:

```
    if False:
        # A row exists and every one of them is a tombstone: imported once, then
```

### `r318.P4_ambiguous_reads_not_imported`

row_placement: two live rows claiming a location answer not imported instead of ambiguous

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P4_ambiguous_reads_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 423 against a baseline of 423
- Kills: 3 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_two_active_rows_on_one_location_are_ambiguous_and_never_written`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[ambiguous]`

Old text:

```
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.AMBIGUOUS
```

New text:

```
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.NOT_IMPORTED
```

### `r1844.N17_screen_silent`

the gate's screen never shows the landings read as rolled back

- File: `src/cratekit/deletion/cli.py`
- Source: `r1844.json`, row `N17_screen_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`
- Collected: 373 against a baseline of 373
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

### `r1037.M1_identity_unchecked`

landed_absences: read a landing record of any database, so another library's landed rows are offered here

- File: `src/cratekit/deletion/library.py`
- Source: `r1037.json`, row `M1_identity_unchecked`
- Moved: Anchored where u310-replay-after-c.json replayed it: the record preamble of landed_absences and recorded_removals is now one generator, _records, whose record is named recorded; the identity check is dropped from it, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
- Kills: 2 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_of_another_database_offers_nothing`
  - `tests/test_sync_removed.py::test_a_recorded_removal_is_read_only_for_its_own_database_and_a_row_still_absent`

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

### `r1037.M8_playlist_ids_live_only`

playlist_ids: count no playlist at all, so every landing reads as rolled back

- File: `src/cratekit/deletion/library.py`
- Source: `r1037.json`, row `M8_playlist_ids_live_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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

### `r1844.N4_playlist_proof_dropped`

_landing_stands: every playlist held no longer proves the landing, so a lone landed track removed while its playlist stays is never offered

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N4_playlist_proof_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Moved: Anchored where u310-replay-after-c.json replayed it: the formatter split the over long comprehension; the held filter is dropped, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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

### `r1844.N9_rolled_back_unlisted`

landed_absences: a landing read as rolled back is not listed, so the gate never counts it

- File: `src/cratekit/deletion/library.py`
- Source: `r1844.json`, row `N9_rolled_back_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Moved: Anchored where u310-replay-after-c.json replayed it: the replace call collapsed onto one argument line; the landed absences are not joined, as before
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
- Moved: Anchored where u310-replay-after-c.json replayed it: the sight call collapsed onto one line; nothing is held present, as before
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
- Moved: Anchored where u310-replay-after-c.json replayed it: the once only playlist read is now functools.cache over the ids; every playlist reads as held, as before
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

### `r1037.M13_sight_renumbers`

sight: number a row again at every run, so it moves past every advance and is offered again

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M13_sight_renumbers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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

### `r1037.M19_version_two_refused`

_recognize: read only version 1, so this build refuses its own document

- File: `src/cratekit/deletion/watermark.py`
- Source: `r1037.json`, row `M19_version_two_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_deletion.py`, `tests/test_sync_removed.py`
- Collected: 447 against a baseline of 447
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

### `u282.W1_walk_beatport_first`

WALK: Beatport first again, the order before the card

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u282.json`, row `W1_walk_beatport_first`
- Moved: Anchored where u306-replay-after-d.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 43 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_200_challenge_beside_an_unread_discogs_refuses_as_unreachable_not_parse_broken`
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_discogs_first.py::test_a_401_is_sent_once_and_beatport_decides_every_file`
  - `tests/test_discogs_first.py::test_a_beatport_decline_beside_a_refused_token_is_a_decline_and_never_raises`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_a_beatport_miss_keeps_discogs_word_and_is_not_no_hit`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[outage]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[refused]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[reshaped]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[both]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[fallback-only]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[styleless]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[unmapped]`
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_discogs_match_decides_and_beatport_is_not_asked`
  - `tests/test_discogs_first.py::test_a_discogs_miss_asks_beatport_and_beatport_decides`
  - ... and 28 more, see the JSON sidecar

Old text:

```
WALK: tuple[str, ...] = (DISCOGS, BEATPORT)
```

New text:

```
WALK: tuple[str, ...] = (BEATPORT, DISCOGS)
```

### `u282.W2_sources_beatport_first`

SOURCES: Beatport first again, so the summary and its sentences count Beatport first

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u282.json`, row `W2_sources_beatport_first`
- Moved: Anchored where u306-replay-after-d.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_record_and_a_summary_list_discogs_first`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
SOURCES: tuple[str, ...] = (DISCOGS, BEATPORT, TRAXSOURCE, BANDCAMP)
```

New text:

```
SOURCES: tuple[str, ...] = (BEATPORT, DISCOGS, TRAXSOURCE, BANDCAMP)
```

### `u282.L2_nobody_named_is_the_source`

_lent: with no shop's row, art_source stays None, so the picture's report is written about Discogs

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `L2_nobody_named_is_the_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_a_beatport_miss_keeps_discogs_word_and_is_not_no_hit`
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_misses_names_no_picture_and_no_unread`
  - `tests/test_discogs_first.py::test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread`

Old text:

```
        return replace(hit, art_url="", art_source="")
```

New text:

```
        return replace(hit, art_url="")
```

### `u282.P1_no_picture_question`

_pictured: no picture question is carried, so a file Discogs tagged gets no cover (merge blocker 5)

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `P1_no_picture_question`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 8 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_misses_names_no_picture_and_no_unread`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_refuses_is_unread_and_counts_toward_the_stop`
  - `tests/test_discogs_first.py::test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread`
  - `tests/test_discogs_first.py::test_a_tagged_file_with_no_picture_keeps_its_genre_and_gets_the_cover`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
    if not later:
        return lent
```

New text:

```
    if True:
        return lent
```

### `u282.P3_answer_not_folded`

_pictured: the picture's answer is not folded into the record, so Beatport stays not-asked after it was asked

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `P3_answer_not_folded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_misses_names_no_picture_and_no_unread`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_refuses_is_unread_and_counts_toward_the_stop`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
            answers = [entry if said.source == source else said for said in answers]
```

New text:

```
            answers = [said for said in answers]
```

### `u282.P5_match_names_no_picture`

_pictured: a matched row's cover is not taken

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `P5_match_names_no_picture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_tagged_file_with_no_picture_keeps_its_genre_and_gets_the_cover`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
                    art_url=outcome.art_url,
                    art_source=source,
```

New text:

```
                    art_url="",
                    art_source="",
```

### `u282.P6_waiting_note_dropped`

_pictured: the not-asked entry carries no note saying Beatport waits for a picture

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `P6_waiting_note_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`

Old text:

```
        replace(said, note=note) if said.source in later else said for said in lent.answers
```

New text:

```
        said for said in lent.answers
```

### `u282.R1_rejection_raised_at_once`

search: a rejected token is raised at once, so Beatport is never asked (round one's BLOCKING)

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `R1_rejection_raised_at_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_401_is_sent_once_and_beatport_decides_every_file`
  - `tests/test_discogs_first.py::test_a_beatport_decline_beside_a_refused_token_is_a_decline_and_never_raises`
  - `tests/test_discogs_first.py::test_a_tagged_file_still_gets_its_cover_when_the_token_is_refused`
  - `tests/test_discogs_first.py::test_a_token_refused_on_its_shape_still_lets_beatport_decide_and_lend_its_cover`
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
                    rejected = refusal
                    passed.append
```

New text:

```
                    raise refusal
                    passed.append
```

### `u282.R4_rejection_reads_as_no_token`

search: a rejected token is recorded with the no token note, so the sweep counts it as never recorded

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `R4_rejection_reads_as_no_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_beatport_decline_beside_a_refused_token_is_a_decline_and_never_raises`
  - `tests/test_discogs_first.py::test_a_token_refused_on_its_shape_still_lets_beatport_decide_and_lend_its_cover`
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
                        NotAsked(DISCOGS, f"{DISCOGS_TOKEN_REFUSED}{refusal.cause.message}")
```

New text:

```
                        NotAsked(DISCOGS, DISCOGS_NO_TOKEN)
```

### `u282.T1_question_asked_with_a_picture`

tag_one: the picture's question is asked whatever the file holds, so a file with a picture spends a Beatport request

- File: `src/cratekit/tagging/tag.py`
- Source: `u282.json`, row `T1_question_asked_with_a_picture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_that_has_a_picture_sends_beatport_nothing`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
    if settled is None and hit is not None and hit.ask_picture is not None:
```

New text:

```
    if hit is not None and hit.ask_picture is not None:
```

### `u282.T2_question_never_asked`

tag_one: the picture's question is never asked (merge blocker 5)

- File: `src/cratekit/tagging/tag.py`
- Source: `u282.json`, row `T2_question_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_picture_ask_that_raises_never_fails_the_file`
  - `tests/test_discogs_first.py::test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread`
  - `tests/test_discogs_first.py::test_a_tagged_file_with_no_picture_keeps_its_genre_and_gets_the_cover`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
    if settled is None and hit is not None and hit.ask_picture is not None:
```

New text:

```
    if False:
```

### `u282.C2_refused_token_not_warned`

_discogs_warnings: the refused token's warning is never raised

- File: `src/cratekit/tagging/cli.py`
- Source: `u282.json`, row `C2_refused_token_not_warned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tag_suggest.py`
- Collected: 443 against a baseline of 443
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
    if refused:
        warnings.append(
```

New text:

```
    if False:
        warnings.append(
```

### `u282.C1_refused_token_not_counted`

_summary: a refused token's not-asked is never counted, so the sweep says nothing about it (round two's BLOCKING)

- File: `src/cratekit/tagging/summary.py`
- Source: `u282.json`, row `C1_refused_token_not_counted`
- Moved: Anchored where u306-replay-after-c2.json replayed it: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tag_suggest.py`
- Collected: 443 against a baseline of 443
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
                discogs_refused += 1
```

New text:

```
                discogs_refused += 0
```

### `u244.M02_rejection_remembered`

DiscogsAsker.ask: forget a rejected token, so it is resent on every later file

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M02_rejection_remembered`
- Moved: Anchored where u306-replay-after-d.json replayed it: DiscogsAsker moved verbatim from tagging/searchers.py to tagging/discogs.py, where the text occurs once, in DiscogsAsker.ask; the identical line in tagging/cyanite.py is Cyanite's own guard and not this one
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tag_suggest.py`
- Collected: 262 against a baseline of 262
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_rejected_token_is_not_sent_again_in_the_run`
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
        if self.rejected is not None:
```

New text:

```
        if False:
```

### `u244.M01_no_token_not_asked`

DiscogsAsker.ask: answer MISS for a searcher with no token instead of not-asked, so a sweep with no token records no-hit

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M01_no_token_not_asked`
- Moved: Anchored where u306-replay-after-c2.json replayed it: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tag_suggest.py`, `tests/test_catalogue_searcher.py`, `tests/test_published_genre.py`
- Collected: 470 against a baseline of 470
- Kills: 11 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_file_swept_without_a_token_is_sources_unread_not_no_hit`
  - `tests/test_discogs_searcher.py::test_a_recorded_token_the_keychain_lost_is_not_asked_and_says_so`
  - `tests/test_discogs_searcher.py::test_a_searcher_built_with_no_asker_has_no_token_and_reads_no_keychain`
  - `tests/test_discogs_searcher.py::test_a_walk_that_asked_nothing_is_a_decline_naming_what_it_passed_over`
  - `tests/test_discogs_searcher.py::test_beatport_unreachable_and_discogs_unasked_refuse_as_an_outage_naming_the_token`
  - `tests/test_discogs_searcher.py::test_no_recorded_token_reads_no_keychain_and_is_not_asked`
  - `tests/test_discogs_searcher.py::test_no_token_is_not_asked_with_how_to_record_one_and_never_no_hit`
  - `tests/test_discogs_searcher.py::test_the_general_catalogue_is_still_asked_beside_an_unasked_discogs`
  - `tests/test_tag_suggest.py::test_rows_unread_only_by_a_catalogue_nobody_asked_do_not_stop_the_walk`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`

Old text:

```
        if self.token is None:
            return NotAsked(DISCOGS, self.unasked)
```

New text:

```
        if self.token is None:
            return SourceOutcome(DISCOGS, Answer.MISS)
```

### `u184.D8_check_unlisted`

CHECKS: drop the new check, so doctor never shows the acknowledgment

- File: `src/cratekit/cli/doctor.py`
- Source: `u184.json`, row `D8_check_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 6 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_acknowledgment_that_cannot_be_understood_is_a_failure`
  - `tests/test_doctor.py::test_doctor_names_when_an_acknowledgment_lapsed`
  - `tests/test_doctor.py::test_doctor_says_when_no_acknowledgment_is_on_record`
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_doctor.py::test_every_check_key_and_its_place_in_the_run_order_is_written_out`
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`

Old text:

```
    Check("backup.acknowledgment", _check_backup_acknowledgment),
```

New text:

```
(empty)
```

### `u184.D1_volume_not_established`

_check_backup_acknowledgment: read the record off a volume nobody established, so a missing disk reads as none on record

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D1_volume_not_established`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`

Old text:

```
    unreadable = _library_state_unreadable(inputs, "the backup acknowledgment")
```

New text:

```
    unreadable = None
```

### `u184.D2_unreadable_is_a_note`

_check_backup_acknowledgment: report a record that cannot be understood as a note rather than a failure

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D2_unreadable_is_a_note`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_acknowledgment_that_cannot_be_understood_is_a_failure`

Old text:

```
            status=Status.FAIL,
            detail=(
                f"{exc.cause.message}. Every destructive verb refuses while the "
```

New text:

```
            status=Status.INFO,
            detail=(
                f"{exc.cause.message}. Every destructive verb refuses while the "
```

### `u184.D3_remedy_chosen_here`

_check_backup_acknowledgment: name a remedy chosen here instead of the reader's own

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D3_remedy_chosen_here`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_acknowledgment_that_cannot_be_understood_is_a_failure`

Old text:

```
            remedy=exc.cause.remediation.remedy,
        )
    if recorded is None:
```

New text:

```
            remedy=Remedy.ACKNOWLEDGE_BACKUP,
        )
    if recorded is None:
```

### `u184.D4_expired_read_as_valid`

_check_backup_acknowledgment: drop the expired branch, so a lapsed record reads as valid with time left

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D4_expired_read_as_valid`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_names_when_an_acknowledgment_lapsed`

Old text:

```
    if not recorded.valid_at(now):
```

New text:

```
    if False:
```

### `u184.D5_wall_clock`

_check_backup_acknowledgment: read the wall clock rather than the run's own instant

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D5_wall_clock`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`

Old text:

```
    now = inputs.probes.now
    expires = recorded.expires_at.replace(microsecond=0).isoformat()
```

New text:

```
    now = datetime.now(timezone.utc)
    expires = recorded.expires_at.replace(microsecond=0).isoformat()
```

### `u184.D6_hours_coefficient`

_check_backup_acknowledgment: halve the minutes per hour, so the time left is misstated

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D6_hours_coefficient`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`

Old text:

```
    hours, minutes = divmod(int(left.total_seconds()) // 60, 60)
```

New text:

```
    hours, minutes = divmod(int(left.total_seconds()) // 60, 30)
```

### `u184.D7_rule_not_named`

_check_backup_acknowledgment: name the terminal rule whatever minted the record

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u184.json`, row `D7_rule_not_named`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`

Old text:

```
            f"the {recorded.rule} rule"
```

New text:

```
            f"the terminal rule"
```

### `u185.D1_push_newer_warns`

deadca7.push: invert the comparison, so a push after the last backup reads as held by it

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u185.json`, row `D1_push_newer_warns`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_push_newer_than_the_last_database_backup_warns_and_names_the_backup`
  - `tests/test_doctor.py::test_a_push_older_than_the_last_database_backup_is_held_by_it`

Old text:

```
    if completed is not None and pushed > completed:
```

New text:

```
    if completed is not None and pushed < completed:
```

### `u185.D2_hidden_entries`

deadca7.push: count hidden entries, so a .DS_Store reads as a push

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u185.json`, row `D2_hidden_entries`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_push_older_than_the_last_database_backup_is_held_by_it`
  - `tests/test_doctor.py::test_installed_with_an_empty_backup_folder_says_the_location_is_unconfirmed`
  - `tests/test_doctor.py::test_installed_with_no_push_says_so`
  - `tests/test_doctor.py::test_with_its_support_folder_here_the_install_signals_are_not_asked`

Old text:

```
        entry.stat().st_mtime for entry in folder.iterdir() if not entry.name.startswith(".")
```

New text:

```
        entry.stat().st_mtime for entry in folder.iterdir()
```

### `u185.D3_unread_folder`

deadca7.push: let an unreadable backup folder escape, so the check fails the report

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u185.json`, row `D3_unread_folder`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_backup_folder_that_cannot_be_read_is_said_as_unread_and_does_not_fail`
  - `tests/test_doctor.py::test_a_backup_folder_whose_stat_is_refused_is_unread_never_no_push`

Old text:

```
    except OSError as exc:
        # Unread is not none
```

New text:

```
    except ZeroDivisionError as exc:
        # Unread is not none
```

### `u224.M10_refused_backups_read_no_push`

_check_deadca7_push: a backup folder whose stat is refused reads as absent, so no push

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M10_refused_backups_read_no_push`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_backup_folder_whose_stat_is_refused_is_unread_never_no_push`

Old text:

```
        if isinstance(presence, OSError):
            raise presence
```

New text:

```
        if isinstance(presence, OSError):
            presence = False
```

### `u224.M1_found_ignored`

_deadca7_presence: never count a present install place as found, so a bundle reads not installed again

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M1_found_ignored`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 7 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_probe_that_raises_beside_a_present_bundle_still_reads_installed`
  - `tests/test_doctor.py::test_a_real_probes_value_asks_the_installed_probe`
  - `tests/test_doctor.py::test_installed_with_its_support_folder_unread_says_its_push_cannot_be_said`
  - `tests/test_doctor.py::test_installed_with_no_home_to_resolve_says_where_its_backups_land_is_unconfirmed`
  - `tests/test_doctor.py::test_one_installed_place_alone_reads_installed_with_no_push[the-accounts-own-applications-folder]`
  - `tests/test_doctor.py::test_one_installed_place_alone_reads_installed_with_no_push[the-state-folder-alone]`
  - `tests/test_doctor.py::test_sitting_68s_mac_the_bundle_and_no_support_folder_reads_installed_with_no_push`

Old text:

```
            elif state:
                found.append(place)
```

New text:

```
            elif False:
                found.append(place)
```

### `u224.M2_unread_place_dropped`

_deadca7_presence: drop an install place the account cannot stat, so it reads absent

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M2_unread_place_dropped`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_install_signal_that_cannot_be_read_is_unread_never_not_installed`

Old text:

```
                unread.append(f"{place} could not be read ({_said(state)})")
```

New text:

```
                pass
```

### `u224.M3_broken_installed_probe_silent`

_deadca7_presence: an install probe that raises adds nothing, so it reads not installed

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M3_broken_installed_probe_silent`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_probe_that_raises_reads_unread_rather_than_not_installed[deadca7_installed]`

Old text:

```
            unread.append(f"where its app is installed could not be located ({_said(exc)})")
```

New text:

```
            pass
```

### `u224.M4_unread_support_read_absent`

_deadca7_presence: a support folder whose stat is refused answers absent, so an installed app reads no push

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M4_unread_support_read_absent`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_installed_with_its_support_folder_unread_says_its_push_cannot_be_said`

Old text:

```
            support = None
            unread.append(f"{home} could not be read
```

New text:

```
            support = False
            unread.append(f"{home} could not be read
```

### `u224.M5_refused_stat_read_absent`

_folder_presence: any refused stat answers absent, the Path.is_dir shape on later Pythons

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M5_refused_stat_read_absent`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_backup_folder_whose_stat_is_refused_is_unread_never_no_push`
  - `tests/test_doctor.py::test_a_support_folder_that_cannot_be_read_is_unread_never_not_installed`
  - `tests/test_doctor.py::test_an_install_signal_that_cannot_be_read_is_unread_never_not_installed`
  - `tests/test_doctor.py::test_installed_with_its_support_folder_unread_says_its_push_cannot_be_said`

Old text:

```
    except OSError as exc:
        return exc
    return stat.S_ISDIR(mode)
```

New text:

```
    except OSError as exc:
        return False
    return stat.S_ISDIR(mode)
```

### `u224.M6_unread_folded_into_not_installed`

_check_deadca7_push: nothing found and something unread reads not installed

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M6_unread_folded_into_not_installed`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_probe_that_raises_reads_unread_rather_than_not_installed[deadca7_home]`
  - `tests/test_doctor.py::test_a_probe_that_raises_reads_unread_rather_than_not_installed[deadca7_installed]`
  - `tests/test_doctor.py::test_a_support_folder_that_cannot_be_read_is_unread_never_not_installed`
  - `tests/test_doctor.py::test_an_install_signal_that_cannot_be_read_is_unread_never_not_installed`

Old text:

```
        if unread:
            return said("whether DEADCA7 is installed here cannot be said: "
```

New text:

```
        if False:
            return said("whether DEADCA7 is installed here cannot be said: "
```

### `u224.M7_install_signals_always_asked`

_deadca7_presence: ask the install signals even with the support folder here

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M7_install_signals_always_asked`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_with_its_support_folder_here_the_install_signals_are_not_asked`

Old text:

```
    if not support:
        try:
            places = tuple(probes.deadca7_installed())
```

New text:

```
    if True:
        try:
            places = tuple(probes.deadca7_installed())
```

### `u224.M9_path_through_a_file_unread`

_folder_presence: a stat through a file reads unread rather than absent

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `u224.json`, row `M9_path_through_a_file_unread`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_install_place_reached_through_a_file_is_absent_not_unread`

Old text:

```
    except (FileNotFoundError, NotADirectoryError):
        return False
    except OSError as exc:
        return exc
```

New text:

```
    except FileNotFoundError:
        return False
    except OSError as exc:
        return exc
```

### `u263.D21_doctor_names_verbs`

doctor: drop the verbs from a failing binary row

- File: `src/cratekit/cli/doctor_keys.py`
- Source: `u263.json`, row `D21_doctor_names_verbs`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_keys.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_missing_ffmpeg_names_the_analysis_whose_decoder_it_is`

Old text:

```
            f"{', '.join(inputs.requiring(key))} ({source}; override with {override})"
```

New text:

```
            f"({source}; override with {override})"
```

### `r598-b.B6_doctor_clause_dropped`

_open_state: list an orphaned record bare, so it reads as a run in progress with no verb named

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r598-b.json`, row `B6_doctor_clause_dropped`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`

Old text:

```
    if session.orphaned(record):
        return f"{record.state}, its process is gone, crate session release abandons it"
```

New text:

```
    if False:
        return f"{record.state}, its process is gone, crate session release abandons it"
```

### `u159.M8_behind_reads_current`

_check_release: any parseable installed version passes, so a copy behind reads as current

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u159.json`, row `M8_behind_reads_current`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_newer_release_warns_with_the_one_pipx_command_keeping_the_extras`
  - `tests/test_doctor.py::test_a_newer_release_without_extras_names_plain_cratekit`
  - `tests/test_doctor.py::test_an_upgrade_keeps_the_extras_and_adds_vocals_only_for_a_scored_library[never-scored-adds-nothing]`
  - `tests/test_doctor.py::test_an_upgrade_keeps_the_extras_and_adds_vocals_only_for_a_scored_library[scored-adds-vocals]`

Old text:

```
    if installed >= newest:
```

New text:

```
    if True:
```

### `u181.D5_upgrade_never_adds_vocals`

doctor _kept: the upgrade command never adds vocals, so a scored library upgrades without it

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u181.json`, row `D5_upgrade_never_adds_vocals`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_upgrade_keeps_the_extras_and_adds_vocals_only_for_a_scored_library[scored-adds-vocals]`

Old text:

```
    if VOCALS_EXTRA in origin.extras or not inputs.probes.vocals_scored(inputs.cfg):
```

New text:

```
    if True:
```

### `u181.D6_upgrade_always_adds_vocals`

doctor _kept: the upgrade command adds vocals for a library never scored

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u181.json`, row `D6_upgrade_always_adds_vocals`
- Moved: Anchored where u303-replay-after-a.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_newer_release_without_extras_names_plain_cratekit`
  - `tests/test_doctor.py::test_an_upgrade_keeps_the_extras_and_adds_vocals_only_for_a_scored_library[never-scored-adds-nothing]`

Old text:

```
    if VOCALS_EXTRA in origin.extras or not inputs.probes.vocals_scored(inputs.cfg):
```

New text:

```
    if VOCALS_EXTRA in origin.extras:
```

### `r83.P2_nothing_entered_raise`

R-347: an empty secret raises the plain PromptUnavailable again

- File: `src/cratekit/cli/prompt.py`
- Source: `r83.json`, row `P2_nothing_entered_raise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_credential_offer_accepted_and_left_empty_is_the_same_note_as_a_no`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`

Old text:

```
            raise NothingEntered(f"nothing entered for {question!r}")
```

New text:

```
            raise PromptUnavailable(f"nothing entered for {question!r}")
```

### `r83.P3_empty_secret_note_status`

R-347: the wizard's empty credential note is FAIL instead of INFO

- File: `src/cratekit/cli/setup.py`
- Source: `r83.json`, row `P3_empty_secret_note_status`
- Moved: Anchored where u303-replay-after-c.json replayed it: U303 shortened the comment above the note to its rule; the INFO status of the empty credential note, the guard this row flips, is unchanged in the same place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_credential_offer_accepted_and_left_empty_is_the_same_note_as_a_no`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`

Old text:

```
                # Accepted then left empty is the same as a no (R-347).
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.INFO,
```

New text:

```
                # Accepted then left empty is the same as a no (R-347).
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.FAIL,
```

### `r83.P4_empty_secret_branch`

R-347: remove the NothingEntered branch so the unreadable branch catches it

- File: `src/cratekit/cli/setup.py`
- Source: `r83.json`, row `P4_empty_secret_branch`
- Moved: Anchored where u303-replay-after-c.json replayed it: U303 shortened the comment inside the branch to one line; the NothingEntered branch, the guard this row removes, is unchanged in the same place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_credential_offer_accepted_and_left_empty_is_the_same_note_as_a_no`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`

Old text:

```
            except prompt.NothingEntered:
                # Accepted then left empty is the same as a no (R-347).
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.INFO,
                    f"{name} is not recorded and was not entered; doctor reports it",
                )
                continue

```

New text:

```
(empty)
```

### `u299.U2_installation_area_passed`

_installation: the area an entry names is dropped, so config.toml resolves under the state directory

- File: `src/cratekit/core/state_files.py`
- Source: `u299.json`, row `U2_installation_area_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_from_a_newer_build_keeps_its_own_remedy`
  - `tests/test_doctor.py::test_the_wizard_completes_an_incomplete_configuration_rather_than_refusing`
  - `tests/test_doctor.py::test_the_wizard_refuses_to_overwrite_a_configuration_it_cannot_understand`

Old text:

```
        installation_area=area,
    )
```

New text:

```
        installation_area=InstallationArea.STATE,
    )
```

### `u303.D4_run_ignores_probes`

doctor.run: a caller's probes are dropped for the real machine's

- File: `src/cratekit/cli/doctor.py`
- Source: `u303.json`, row `D4_run_ignores_probes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_cli_contract.py`
- Collected: 1415 against a baseline of 1415
- Kills: 78 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_8_every_declared_precondition_can_pass_and_can_refuse`
  - `tests/test_doctor.py::test_a_backup_folder_that_cannot_be_read_is_said_as_unread_and_does_not_fail`
  - `tests/test_doctor.py::test_a_backup_folder_whose_stat_is_refused_is_unread_never_no_push`
  - `tests/test_doctor.py::test_a_backup_recorded_in_the_future_is_refused_rather_than_treated_as_fresh`
  - `tests/test_doctor.py::test_a_binary_that_is_simply_absent_still_says_install_it`
  - `tests/test_doctor.py::test_a_broken_trash_is_informational_when_no_verb_this_profile_needs_it`
  - `tests/test_doctor.py::test_a_clone_with_no_configuration_is_told_the_floor`
  - `tests/test_doctor.py::test_a_commit_hook_that_is_present_and_is_not_text_is_reported`
  - `tests/test_doctor.py::test_a_commit_msg_hook_installed_for_another_stage_is_refused`
  - `tests/test_doctor.py::test_a_commit_msg_hook_on_another_configuration_is_refused`
  - `tests/test_doctor.py::test_a_commondir_that_is_present_and_is_not_text_is_reported_too`
  - `tests/test_doctor.py::test_a_configuration_that_does_not_parse_is_not_read_as_one_hook_type`
  - `tests/test_doctor.py::test_a_configured_commit_msg_stage_with_no_hook_is_refused`
  - `tests/test_doctor.py::test_a_drifted_application_pin_is_a_different_answer_from_an_unset_one`
  - `tests/test_doctor.py::test_a_foreign_volume_at_the_configured_root_is_its_own_answer`
  - ... and 63 more, see the JSON sidecar

Old text:

```
    inputs = _Inputs(cfg, error, probes or Probes())
```

New text:

```
    inputs = _Inputs(cfg, error, Probes())
```

### `u263.D22_restamp_declares`

registry: analyze restamp no longer declares binary.ffmpeg

- File: `src/cratekit/cli/registry.py`
- Source: `u263.json`, row `D22_restamp_declares`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_cli_contract.py`
- Collected: 1415 against a baseline of 1415
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_missing_ffmpeg_names_the_analysis_whose_decoder_it_is`

Old text:

```
        doctor_checks=("library.mounted", "rekordbox.pins", "binary.ffmpeg"),
```

New text:

```
        doctor_checks=("library.mounted", "rekordbox.pins"),
```

### `r662-b.M16_flag_not_declared`

the parser no longer declares --backup-remote

- File: `src/cratekit/cli/setup.py`
- Source: `r662-b.json`, row `M16_flag_not_declared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_cli_contract.py`
- Collected: 1415 against a baseline of 1415
- Kills: 14 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_bare_folder_name_is_refused_by_the_wizard_however_it_arrives[flag]`
  - `tests/test_doctor.py::test_a_bare_folder_name_is_refused_by_the_wizard_however_it_arrives[prompt]`
  - `tests/test_doctor.py::test_a_mistyped_module_name_is_still_a_named_problem_not_a_traceback`
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_doctor.py::test_an_install_with_no_templates_offers_no_closed_set_rather_than_an_empty_one`
  - `tests/test_doctor.py::test_setup_leaves_under_the_code_a_refusing_check_reserved`
  - `tests/test_doctor.py::test_setup_writes_nothing_beside_the_library_until_the_volume_is_asserted`
  - `tests/test_doctor.py::test_the_backup_flags_are_recorded_without_a_question`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_wizard_on_a_clean_machine_produces_a_valid_config_and_a_green_doctor`
  - `tests/test_doctor.py::test_the_wizard_writes_the_active_template_on_a_linux_style_ordinary_directory`
  - `tests/test_doctor.py::test_the_wizard_writes_the_active_template_once_the_volume_is_the_recorded_one`

Old text:

```
    parser.add_argument(
        "--backup-remote",
        help="the rclone remote the three destinations name, replacing a recorded one",
    )
```

New text:

```
(empty)
```

### `r345.B2_module_off`

_resolve_backup: offer the destinations whatever the profile says, so slim is asked about a module it does not have

- File: `src/cratekit/cli/setup.py`
- Source: `r345.json`, row `B2_module_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_paths_resolved.py`, `tests/test_cli_contract.py`
- Collected: 1466 against a baseline of 1466
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_doctor.py::test_backup_flags_are_recorded_even_when_the_module_is_off`
  - `tests/test_doctor.py::test_the_wizard_asks_nothing_about_backup_when_the_module_is_off`

Old text:

```
    if "backup" not in membership.modules:
```

New text:

```
    if False:
```

### `r1255.D1_doctor_branches_on_the_scan`

doctor _check_unresolved_session: never branch on the listing, so the log directory is named as an unreadable record

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r1255.json`, row `D1_doctor_branches_on_the_scan`
- Moved: Anchored where u303-replay-merged.json replayed it: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_session_log_unlisted.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_session_log_this_account_cannot_list_is_failed_by_its_own_check`

Old text:

```
    if session.log_unlisted(unreadable, inputs.cfg):
        unreadable_directory = session.log_dir(inputs.cfg)
```

New text:

```
    if False:
        unreadable_directory = session.log_dir(inputs.cfg)
```

