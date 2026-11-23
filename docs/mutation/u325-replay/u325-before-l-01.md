# Mutation table: u325-before-l-01

Measured by `scripts/mutate.py` on 2026-11-23 01:21 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 96.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 19:20 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 4, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 46 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u188.M5_repeat_kept` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r154-c.C1_digest_the_word` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r154-c.C2_expected_volume_outside_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r154-c.C3_hand_down_the_flag` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r154-c.C4_pull_flags_dropped` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 4 | killed |
| `r154-c.C5_stated_volume_stops_at_the_verb` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r367.G10_the_report_drops_the_absent_field` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r368-round-2.G14_the_destination_check_is_equality_only` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r368-round-2.G6_ancestors_not_walked` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r368-round-2.G7_composite` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r368-round-2.G7_target_not_resolved` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r368-round-2.R1_the_live_root_refusal_is_reworded` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r368.A1_the_detail_check_is_one_value` | `src/cratekit/session/restore_cli.py` | maintainer | 1 file(s) | 98 | 1 | killed |
| `r368.G10_the_default_capture_survives_a_target` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r368.G11_the_target_is_dropped_before_the_engine` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r368.G12_the_target_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r368.G13_the_rehearsal_flag_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r368.G1_no_live_database_destination_check` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r368.G2_no_containment_check` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r368.G3_containment_one_direction_only` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r368.G4_containment_is_equality_only` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r368.G5_paths_compared_as_strings` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r368.G8_target_without_the_off_machine_pull_is_allowed` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r368.G9_target_beside_a_capture_rollback_is_allowed` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r592-b.B1_step_on_every_failure` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r592-b.B2_step_on_the_wrong_half` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r592-b.B4_step_names_the_wrong_directory` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r592-b.B5_step_names_no_file` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r592-b.B7_sample_halves_split` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r592-c.C1_step_on_a_rehearsal_remeasured` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u211.R1_restore_says_what_the_mirror_left` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.G3_abort_restores_anyway` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.L1_an_unusable_capture_is_filtered_out_of_the_listing` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u27-restore-cli-author.N1_the_default_takes_the_newest_unusable_capture` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u27-restore-cli-author.P1_the_report_recomputes_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.P2_a_mirror_pull_is_reported_as_nothing` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u27-restore-cli-author.P3_convergence_is_reported_for_a_run_that_spent_no_capture` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.R1_a_backup_refusal_becomes_an_internal_error` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 10 | killed |
| `u27-restore-cli-author.S6_the_named_decision_is_withdrawn` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 10 | killed |
| `u27-restore-cli-author.S8_a_rehearsal_performs_the_capture_restore` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-round-2.O2_the_discard_set_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-round-2.R2_the_reserved_remediation_is_replaced_by_the_class_default` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u27-restore-cli-round-2.S7_a_rehearsal_performs_the_mirror_pull` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u96-a.A12_which_half_failed` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u96-a.A13_completed_halves_recorded` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u96-a.A14_target_is_required` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u96-a.A15_report_names_where_the_database_is` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u96-a.A16_no_absent_companion_for_a_half_that_did_not_run` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u96-a.A1_acceptance_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u96-a.A2_flag_reaches_the_function` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u96-a.A4_run_inside_the_held_session` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u96-a.A5_the_mirror_is_pulled` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u96-a.A6_a_half_at_a_time` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u96-a.A7_rekordbox_asked_again` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u96-a.A8_database_elsewhere_is_skipped` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u96-a.A9_a_rehearsal_stays_a_rehearsal` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r172-a.A1_nothing_collides` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `r172-a.A2_one_round_only` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-a.A3_shared_target_ignored` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 4 | killed |
| `r172-a.A4_occupied_target_ignored` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r172-a.A5_chain_held_too` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-a.A7_targets_compared_exactly` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-a.A9_collides_reported_as_a_rename` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `r172-b.B11_collision_step_always` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B12_the_first_file_is_not_named` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B13_detail_carries_nothing` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 10 | killed |
| `r172-b.B14_diagnostic_surface` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 6 | killed |
| `r172-b.B16_referenced_recheck_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B17_claim_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B1_ok_whatever_happened` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 15 | killed |
| `r172-b.B2_missing_file_unreported` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B3_new_row_unreported` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B5_os_error_unreported` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B6_tag_write_answer_ignored` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r172-b.B8_tag_failure_named_where_it_was` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r172-b.B9_renamed_count_is_the_promise` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-a.G1_no_refusal` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 13 | killed |
| `r500-a.G2_existence_half_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-a.G3_unmapped_half_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-a.G4_lexists` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-a.G5_recorded_key_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r500-b.G9_plural_always` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-c.G11_prefix_cap_halved` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-c.G12_remedy_run_doctor` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r500-c.G15_other_host_refuses` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u39-author-full.R1_filename_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `u39-author-full.R2_title_fallback_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u39-author-full.R3_bpm_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 29 | killed |
| `u39-author-full.R4_head_key_overrules_tag` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u39-author-full.R5_junk_tag_admitted` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u39-author-full.R6_lossy_flag_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `u39-naming-independent.R5_bpm_wrong_type` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 71 | killed |
| `u41-author-full.R1_filename_head_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `u41-author-full.R6_head_key_overrules_tag` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u41-author-full.T1_title_tag_fed_the_filename_body` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u41-author-full.T2_title_field_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u41-naming-independent.B1_head_precedence_swapped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u41-naming-independent.B2_filename_head_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `u41-naming-independent.B3_title_head_source_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u41-naming-independent.B7_lossy_filename_operand_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u41-naming-independent.B8_lossy_title_operand_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 3 | killed |
| `u41-naming-independent.C1_plan_no_op_filter_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 10 | killed |
| `u67-round-2.C1_action_filter_and_recheck` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 19 | killed |
| `u67.M2_nfc` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.M3_prefix_resolution` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.M6_remote_host_skip` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.M7_absolute_spelling` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.M8_resolved_spelling` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.R1_refusal_to_empty` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 3 | killed |
| `u67.R2_generic_to_empty` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u67.R3_remedy_passthrough` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u95-a.A1_never_rerooted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 7 | killed |
| `u95-a.A2_library_sessions_rerooted_too` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-a.A3_database_not_carried` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 4 | killed |
| `u95-a.A4_outside_database_refusal_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-a.A5_capture_path_not_rebased` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-a.A6_manifest_not_rebased_in_plan` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 3 | killed |
| `u95-a.A7_manifest_not_rebased_in_preflight` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-a.A8_run_not_rooted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-b.B2_manifest_database_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-b.B3_sources_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 3 | killed |
| `u95-b.B4_captured_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-b.B5_not_idempotent` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 498 | 1 | killed |
| `u95-b.B6_recorded_path_not_normalised` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 498 | 1 | killed |
| `u95-b.B8_outside_path_moved_anyway` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 498 | 2 | killed |
| `u95-b1.B1_manifest_root_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-c.C1_plan_side_guard_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-c.C2_run_side_guard_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 7 | killed |
| `u95-c.C3_step_authorisation_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u95-c.C4_restorable_membership_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 1 | killed |
| `u95-c.C5_staging_authorisation_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 498 | 2 | killed |
| `u144-c.C8_question_named` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 39 | 1 | killed |

## Zero rows and what they owe

- `u188.M5_repeat_kept` (maintainer facing): maintainer facing, composite not required
- `r367.G10_the_report_drops_the_absent_field` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r368-round-2.G14_the_destination_check_is_equality_only` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r368-round-2.G6_ancestors_not_walked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r368.G5_paths_compared_as_strings` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r592-b.B1_step_on_every_failure` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r592-b.B2_step_on_the_wrong_half` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r592-b.B4_step_names_the_wrong_directory` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r592-c.C1_step_on_a_rehearsal_remeasured` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-restore-cli-author.P2_a_mirror_pull_is_reported_as_nothing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-restore-cli-round-2.S7_a_rehearsal_performs_the_mirror_pull` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u96-a.A12_which_half_failed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u96-a.A15_report_names_where_the_database_is` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u96-a.A16_no_absent_companion_for_a_half_that_did_not_run` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u96-a.A7_rekordbox_asked_again` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u96-a.A8_database_elsewhere_is_skipped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u96-a.A9_a_rehearsal_stays_a_rehearsal` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u188.M5_repeat_kept`

_mapped_back: keep a repeated pair instead of dropping it, so the refusal names the folder pair twice on a drive that never moved

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M5_repeat_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
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

### `r154-c.C1_digest_the_word`

Digest a constant where the resolved stamp goes, which is R-153 itself: a backup landing between the two acts leaves the digest where it was

- File: `src/cratekit/session/restore_cli.py`
- Source: `r154-c.json`, row `C1_digest_the_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_backup_landing_between_the_two_acts_moves_the_digest`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled`

Old text:

```
                "snapshot": snapshot.stamp,
```

New text:

```
                "snapshot": "newest",
```

### `r154-c.C2_expected_volume_outside_the_digest`

Leave the stated volume out of the offer, so an answer given without the flag is honoured against a run carrying it

- File: `src/cratekit/session/restore_cli.py`
- Source: `r154-c.json`, row `C2_expected_volume_outside_the_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_expected_volume_is_stated`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`

Old text:

```
                "expected_volume": snapshot_volume,
```

New text:

```
                "expected_volume": None,
```

### `r154-c.C3_hand_down_the_flag`

Hand the engine the flag instead of the stamp that was offered, so it resolves the newest snapshot again after the approval

- File: `src/cratekit/session/restore_cli.py`
- Source: `r154-c.json`, row `C3_hand_down_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`

Old text:

```
        snapshot=pulling.stamp if pulling is not None else None,
```

New text:

```
        snapshot=ctx.args.snapshot,
```

### `r154-c.C4_pull_flags_dropped`

Never refuse a flag about the pull typed without the pull, so it is dropped in silence ahead of a capture rollback

- File: `src/cratekit/session/restore_cli.py`
- Source: `r154-c.json`, row `C4_pull_flags_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_flag_about_the_pull_is_refused_when_no_pull_was_asked_for[flags0]`
  - `tests/test_restore_cli.py::test_a_flag_about_the_pull_is_refused_when_no_pull_was_asked_for[flags1]`
  - `tests/test_restore_cli.py::test_a_flag_about_the_pull_is_refused_when_no_pull_was_asked_for[flags2]`
  - `tests/test_restore_cli.py::test_a_flag_about_the_pull_is_refused_when_no_pull_was_asked_for[flags3]`

Old text:

```
    _refuse_pull_flags_without_the_pull(ctx.args)
    requested = ctx.args.session_id
```

New text:

```
    requested = ctx.args.session_id
```

### `r154-c.C5_stated_volume_stops_at_the_verb`

Show and digest the stated volume and never pass it to the engine, so the replaced drive restore is approved and then refused under the gates

- File: `src/cratekit/session/restore_cli.py`
- Source: `r154-c.json`, row `C5_stated_volume_stops_at_the_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`

Old text:

```
        snapshot_volume=ctx.args.snapshot_volume,
        accept_unrecorded=pulling.named if pulling is not None else None,
```

New text:

```
        snapshot_volume=None,
        accept_unrecorded=pulling.named if pulling is not None else None,
```

### `r367.G10_the_report_drops_the_absent_field`

the off machine half ran and the person is not told the sidecar was missing

- File: `src/cratekit/session/restore_cli.py`
- Source: `r367.json`, row `G10_the_report_drops_the_absent_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            missing = pulled.absent_sidecars
```

New text:

```
            missing = ()
```

### `r368-round-2.G14_the_destination_check_is_equality_only`

re-measured: drop the name-plus-parent half, so a landing path that is not on disk yet passes

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368-round-2.json`, row `G14_the_destination_check_is_equality_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if _same_place(landing, live) or (
        landing.name == live.name and _same_place(landing.parent, live.parent)
    ):

```

New text:

```
    if _same_place(landing, live):

```

### `r368-round-2.G6_ancestors_not_walked`

re-measured: ask samefile of the candidate alone, so a differently cased ancestor is missed

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368-round-2.json`, row `G6_ancestors_not_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return any(_same_place(ancestor, root) for ancestor in (place, *place.parents))

```

New text:

```
    return _same_place(place, root)

```

### `r368-round-2.G7_composite`

what the resolution does hold now that samefile answers the comparison: report the word somebody typed rather than the directory it named

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368-round-2.json`, row `G7_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_relative_target_is_compared_as_the_place_it_names`

Old text:

```
            target=str(resolved),
            library_root=str(root),

```

New text:

```
            target=str(raw),
            library_root=str(root),

```

### `r368-round-2.G7_target_not_resolved`

re-measured: compare the raw argument, leaving samefile to answer for a relative spelling

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368-round-2.json`, row `G7_target_not_resolved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_relative_target_is_compared_as_the_place_it_names`

Old text:

```
    resolved = Path(raw).expanduser().resolve()

```

New text:

```
    resolved = Path(raw).expanduser()

```

### `r368-round-2.R1_the_live_root_refusal_is_reworded`

re-measured: reword the destination refusal rather than appending to it

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368-round-2.json`, row `R1_the_live_root_refusal_is_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_whose_database_lands_on_the_live_one_is_refused`

Old text:

```
            f"the database would land on {landing}, which is this library's live "
            f"database; the target is outside the library root and the database "
            f"is too, so naming its directory restores over it in place",

```

New text:

```
            f"the chosen folder resolves to somewhere this installation already "
            f"reads from, so the copy would replace what is there",

```

### `r368.A1_the_detail_check_is_one_value`

an existing guard in the sample: report both destination refusals under one detail, so the two cannot be told apart

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `A1_the_detail_check_is_one_value`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_whose_database_lands_on_the_live_one_is_refused`

Old text:

```
            check="destination",

```

New text:

```
            check="containment",

```

### `r368.G10_the_default_capture_survives_a_target`

let a rehearsal roll the newest spendable session back on the live library

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G10_the_default_capture_survives_a_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`

Old text:

```
    if target is not None:
        chosen = None
    elif requested is None:

```

New text:

```
    if requested is None:

```

### `r368.G11_the_target_is_dropped_before_the_engine`

read the flag, refuse on it, and then restore to the live root anyway

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G11_the_target_is_dropped_before_the_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`

Old text:

```
        include_mirror=ctx.args.include_mirror,
        target=target,
    )
    return ctx.envelope(data=_performed(report, offered))

```

New text:

```
        include_mirror=ctx.args.include_mirror,
    )
    return ctx.envelope(data=_performed(report, offered))

```

### `r368.G12_the_target_leaves_the_digest`

a decision recorded against a rehearsal is honoured against the live restore

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G12_the_target_leaves_the_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_restore_is_pointed_somewhere_else`

Old text:

```
                "target": str(target) if target is not None else "library",

```

New text:

```
(empty)
```

### `r368.G13_the_rehearsal_flag_leaves_the_digest`

the review's second finding, restored: an approved preview authorises the real run

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G13_the_rehearsal_flag_leaves_the_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_rehearsal_flag_does`

Old text:

```
        "digest": digest_of(
            {"kind": "restore.run", "items": items, "dry_run": dry_run}
        ),

```

New text:

```
        "digest": digest_of({"kind": "restore.run", "items": items}),

```

### `r368.G1_no_live_database_destination_check`

the row the brief names: drop the check that the database would land on the live one

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G1_no_live_database_destination_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_whose_database_lands_on_the_live_one_is_refused`

Old text:

```
    if _same_place(landing, live) or (
        landing.name == live.name and _same_place(landing.parent, live.parent)
    ):

```

New text:

```
    if False:

```

### `r368.G2_no_containment_check`

drop the check that the target is the library root, holds it, or sits inside it

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G2_no_containment_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_that_holds_the_library_or_sits_in_it_is_refused[above-the directory the library root sits in]`
  - `tests/test_restore_cli.py::test_a_target_that_holds_the_library_or_sits_in_it_is_refused[inside-a directory underneath the library root]`

Old text:

```
    if _holds_or_is(root, resolved) or _holds_or_is(resolved, root):

```

New text:

```
    if False:

```

### `r368.G3_containment_one_direction_only`

keep the target inside the root and drop the root inside the target, the mirror over the library's parent

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G3_containment_one_direction_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_that_holds_the_library_or_sits_in_it_is_refused[above-the directory the library root sits in]`

Old text:

```
    if _holds_or_is(root, resolved) or _holds_or_is(resolved, root):

```

New text:

```
    if _holds_or_is(root, resolved):

```

### `r368.G4_containment_is_equality_only`

refuse only the root itself, so a directory underneath it passes

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G4_containment_is_equality_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_that_holds_the_library_or_sits_in_it_is_refused[above-the directory the library root sits in]`
  - `tests/test_restore_cli.py::test_a_target_that_holds_the_library_or_sits_in_it_is_refused[inside-a directory underneath the library root]`

Old text:

```
    if place == root or place.is_relative_to(root):
        return True
    return any(_same_place(ancestor, root) for ancestor in (place, *place.parents))

```

New text:

```
    if place == root:
        return True
    return _same_place(place, root)

```

### `r368.G5_paths_compared_as_strings`

the review's finding, restored: compare spellings rather than places

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G5_paths_compared_as_strings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        return one.samefile(other)
    except OSError:
        return one == other

```

New text:

```
    return one == other

```

### `r368.G8_target_without_the_off_machine_pull_is_allowed`

accept a target with no mirror pull to fill it, which silently becomes a live rollback

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G8_target_without_the_off_machine_pull_is_allowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_with_no_off_machine_pull_is_refused`

Old text:

```
    if not args.from_backup:
        raise _target_invalid(

```

New text:

```
    if False:
        raise _target_invalid(

```

### `r368.G9_target_beside_a_capture_rollback_is_allowed`

accept a target next to a named session or a discard, which puts two halves on two volumes

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G9_target_beside_a_capture_rollback_is_allowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_beside_a_capture_rollback_is_refused[extra0]`
  - `tests/test_restore_cli.py::test_a_target_beside_a_capture_rollback_is_refused[extra1]`

Old text:

```
    if args.session_id is not None or args.discard:
        raise _target_invalid(

```

New text:

```
    if False:
        raise _target_invalid(

```

### `r592-b.B1_step_on_every_failure`

_half_failed: give the removal step to a mirror failure too, sending a person to delete files the mirror never lands

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-b.json`, row `B1_step_on_every_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not dry_run and half == DATABASE_HALF:
```

New text:

```
    if not dry_run:
```

### `r592-b.B2_step_on_the_wrong_half`

_half_failed: give the removal step to the mirror half and not the database half, so a database half that landed part of the fileset says nothing about it

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-b.json`, row `B2_step_on_the_wrong_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not dry_run and half == DATABASE_HALF:
```

New text:

```
    if not dry_run and half == MIRROR_HALF:
```

### `r592-b.B4_step_names_the_wrong_directory`

rerun_step: name the target rather than the directory the database lands in, so the person looks for it in the wrong place

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-b.json`, row `B4_step_names_the_wrong_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        f"companion of it in {database_target.parent} if one is there, because a "
```

New text:

```
        f"companion of it in {database_target.parent.parent} if one is there, because a "
```

### `r592-b.B5_step_names_no_file`

rerun_step: say the database rather than its file name, so the step does not say which file to remove

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-b.json`, row `B5_step_names_no_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`

Old text:

```
        f"before running the recovery again, remove {database_target.name} and any "
```

New text:

```
        f"before running the recovery again, remove the database and any "
```

### `r592-b.B7_sample_halves_split`

SAMPLE, existing guard: _halves hands the whole plan to the mirror half, so a failed mirror lands the database behind it

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-b.json`, row `B7_sample_halves_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
    mirror = tuple(c for c in decided.commands if c.label == backup.RESTORE_MIRROR)
```

New text:

```
    mirror = tuple(decided.commands)
```

### `r592-c.C1_step_on_a_rehearsal_remeasured`

_half_failed: give the removal step to a rehearsal whose database half failed, though a rehearsal landed nothing (B3 of r592-b, re-measured)

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-c.json`, row `C1_step_on_a_rehearsal_remeasured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not dry_run and half == DATABASE_HALF:
```

New text:

```
    if half == DATABASE_HALF:
```

### `u211.R1_restore_says_what_the_mirror_left`

restore session database half: raise the scan's refusal as it came, without the half, the completed mirror or the rerun step

- File: `src/cratekit/session/restore_cli.py`
- Source: `u211.json`, row `R1_restore_says_what_the_mirror_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`

Old text:

```
                        raise _absence_unconfirmed(
                            exc, completed, decided, dry_run=dry_run
                        ) from exc
```

New text:

```
                        raise
```

### `u27-restore-cli-author.G3_abort_restores_anyway`

Treat an aborted confirmation as an approval

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `G3_abort_restores_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_aborted_confirmation_restores_nothing`

Old text:

```
    if option == "abort":
        return ctx.envelope(data=offered, outcome=Outcome.NO_OP)
    if chosen is None and not ctx.args.from_backup:
```

New text:

```
    if option == "never-an-option":
        return ctx.envelope(data=offered, outcome=Outcome.NO_OP)
    if chosen is None and not ctx.args.from_backup:
```

### `u27-restore-cli-author.L1_an_unusable_capture_is_filtered_out_of_the_listing`

Drop the sessions a person is most likely to be looking for

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `L1_an_unusable_capture_is_filtered_out_of_the_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_capture_this_product_pruned_is_refused_by_name_and_not_as_a_defect`
  - `tests/test_restore_cli.py::test_a_session_whose_capture_is_gone_is_listed_and_says_why`

Old text:

```
            "items": [_listed(entry) for entry in listed],
```

New text:

```
            "items": [_listed(e) for e in listed if e.restorable],
```

### `u27-restore-cli-author.N1_the_default_takes_the_newest_unusable_capture`

Choose the newest session regardless of whether its capture can be spent

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `N1_the_default_takes_the_newest_unusable_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_bare_run_takes_the_newest_spendable_capture_and_not_merely_the_newest`
  - `tests/test_restore_cli.py::test_a_capture_that_exists_but_is_unverified_is_not_spendable`

Old text:

```
    for entry in restore.list_sessions(cfg):
        if entry.restorable:
            return entry
    return None
```

New text:

```
    for entry in restore.list_sessions(cfg):
        return entry
    return None
```

### `u27-restore-cli-author.P1_the_report_recomputes_the_digest`

Report a digest computed here rather than the one the decision was recorded against

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `P1_the_report_recomputes_the_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_report_keeps_the_digest_the_decision_was_recorded_against`

Old text:

```
    return {"digest": offered["digest"], "items": items, "totals": totals, "chunk": None}
```

New text:

```
    return {"digest": digest_of(items), "items": items, "totals": totals, "chunk": None}
```

### `u27-restore-cli-author.P2_a_mirror_pull_is_reported_as_nothing`

Leave the off-machine transfers out of the report, which is the defect this shape fixed

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `P2_a_mirror_pull_is_reported_as_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    items: list[dict[str, Any]] = [
        {"half": "off-machine", "transfer": label} for label in report.pulled
    ]
```

New text:

```
    items: list[dict[str, Any]] = []
```

### `u27-restore-cli-author.P3_convergence_is_reported_for_a_run_that_spent_no_capture`

Answer the capture restore's own question when no capture restore happened

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `P3_convergence_is_reported_for_a_run_that_spent_no_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`

Old text:

```
    if outcome is not None:
        totals["converged"] = outcome.converged
        totals["outstanding"] = len(outcome.outstanding)
```

New text:

```
    totals["converged"] = outcome.converged if outcome is not None else True
    if outcome is not None:
        totals["outstanding"] = len(outcome.outstanding)
```

### `u27-restore-cli-author.R1_a_backup_refusal_becomes_an_internal_error`

Flatten every off-machine diagnosis into report-a-defect

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `R1_a_backup_refusal_becomes_an_internal_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 10 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_recovery_is_refused_underneath_a_running_rekordbox`
  - `tests/test_restore_cli.py::test_a_recovery_with_no_rclone_installed_refuses_by_name_and_writes_nothing`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_arrives_as_a_cause_and_not_as_a_bare_exception`
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_carries_the_reserved_remediation_and_not_the_class_default`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_another_librarys_snapshot_is_refused_at_the_verb_and_names_both_volumes`
  - `tests/test_restore_cli.py::test_the_ledgers_traversal_value_is_refused_at_the_verb`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`

Old text:

```
            reason=slug,
            message=exc.detail,
            remediation=reservations.remediation_for(slug),
```

New text:

```
            reason="internal-error",
            message=exc.detail,
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
```

### `u27-restore-cli-author.S6_the_named_decision_is_withdrawn`

Tell the off-machine restore no decision exists, which R33 makes it refuse on

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `S6_the_named_decision_is_withdrawn`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 10 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`
  - `tests/test_restore_cli.py::test_the_report_names_the_snapshot_that_arrived`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled`

Old text:

```
                    confirmed=True,
```

New text:

```
                    confirmed=False,
```

### `u27-restore-cli-author.S8_a_rehearsal_performs_the_capture_restore`

Ignore dry_run on the capture half, so a preview replaces the live database

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `S8_a_rehearsal_performs_the_capture_restore`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_dry_run_walks_every_step_and_performs_none_of_them`

Old text:

```
            outcome=restore.run(
                decided,
                cfg,
                held=held,
                dry_run=dry_run,
```

New text:

```
            outcome=restore.run(
                decided,
                cfg,
                held=held,
                dry_run=False,
```

### `u27-restore-cli-round-2.O2_the_discard_set_leaves_the_digest`

Digest without the sessions being discarded, so an approval covers a wider destruction

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-round-2.json`, row `O2_the_discard_set_leaves_the_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_discard_set_moves`

Old text:

```
                "discarding": list(discarding),
            }
```

New text:

```
            }
```

### `u27-restore-cli-round-2.R2_the_reserved_remediation_is_replaced_by_the_class_default`

Discard the per-slug remediation the reservation table holds

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-round-2.json`, row `R2_the_reserved_remediation_is_replaced_by_the_class_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_carries_the_reserved_remediation_and_not_the_class_default`
  - `tests/test_restore_cli.py::test_the_ledgers_traversal_value_is_refused_at_the_verb`

Old text:

```
            remediation=reservations.remediation_for(slug),
```

New text:

```
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
```

### `u27-restore-cli-round-2.S7_a_rehearsal_performs_the_mirror_pull`

Ignore dry_run on the off-machine half, so a preview transfers for real

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-round-2.json`, row `S7_a_rehearsal_performs_the_mirror_pull`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    pulled,
                    cfg,
                    dry_run=dry_run,
```

New text:

```
                    pulled,
                    cfg,
                    dry_run=False,
```

### `u96-a.A12_which_half_failed`

_half_failed: swap the two failure sentences, so a failed mirror is reported as a failed database half

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A12_which_half_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    elif half == MIRROR_HALF:
        message = (
```

New text:

```
    elif half == DATABASE_HALF:
        message = (
```

### `u96-a.A13_completed_halves_recorded`

Never record a completed half, so a database failure does not say the mirror arrived

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A13_completed_halves_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`

Old text:

```
            completed.append(half)
```

New text:

```
            pass
```

### `u96-a.A14_target_is_required`

build_bare_metal: make --target optional, so the verb can be typed with no destination

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A14_target_is_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_verb_cannot_be_typed_without_naming_a_target`

Old text:

```
        "--target",
        required=True,
        metavar="DIRECTORY",
```

New text:

```
        "--target",
        metavar="DIRECTORY",
```

### `u96-a.A15_report_names_where_the_database_is`

_recovered: always report the rebased database path, so a database that was never recovered is reported at the top of the target

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A15_report_names_where_the_database_is`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            "database_target": str(report.database_elsewhere or report.database_target),
```

New text:

```
            "database_target": str(report.database_target),
```

### `u96-a.A16_no_absent_companion_for_a_half_that_did_not_run`

Report the plan's absent companions even when the database half was skipped

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A16_no_absent_companion_for_a_half_that_did_not_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            absent=decided.absent_sidecars if elsewhere is None else (),
```

New text:

```
            absent=decided.absent_sidecars,
```

### `u96-a.A1_acceptance_reaches_the_engine`

recover_under_bare_metal_session: hand the engine acknowledged=True whatever the caller accepted, so the replacement is never a person's decision

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A1_acceptance_reaches_the_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[the replacement was not accepted]`
  - `tests/test_restore_cli.py::test_the_verb_refuses_without_the_acceptance_flag`

Old text:

```
        acknowledged=accepted,
```

New text:

```
        acknowledged=True,
```

### `u96-a.A2_flag_reaches_the_function`

perform_bare_metal: pass accepted=True instead of the flag, so the verb recovers without --accept-replacement

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A2_flag_reaches_the_function`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_verb_refuses_without_the_acceptance_flag`

Old text:

```
        accepted=ctx.args.accept_replacement,
```

New text:

```
        accepted=True,
```

### `u96-a.A4_run_inside_the_held_session`

Drop gates=held.guard from the run_restore call of each half

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A4_run_inside_the_held_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
                    portion,
                    cfg,
                    dry_run=dry_run,
                    gates=held.guard,
```

New text:

```
                    portion,
                    cfg,
                    dry_run=dry_run,
```

### `u96-a.A5_the_mirror_is_pulled`

Plan with include_mirror=False, so a recovery onto an empty drive brings a database and no music

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A5_the_mirror_is_pulled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
                include_mirror=True,
```

New text:

```
                include_mirror=False,
```

### `u96-a.A6_a_half_at_a_time`

_halves: put every command in the mirror half, which is spending the plan whole, so a failed mirror still lands the database

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A6_a_half_at_a_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
    mirror = tuple(c for c in decided.commands if c.label == backup.RESTORE_MIRROR)
```

New text:

```
    mirror = decided.commands
```

### `u96-a.A7_rekordbox_asked_again`

Disarm the second rekordbox check, the one before the database half

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A7_rekordbox_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    if running:
                        raise backup.BackupRefused(
```

New text:

```
                    if False:
                        raise backup.BackupRefused(
```

### `u96-a.A8_database_elsewhere_is_skipped`

Run the database half even when the configured database was never on the lost volume

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A8_database_elsewhere_is_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            if half == DATABASE_HALF and elsewhere is not None:
```

New text:

```
            if False:
```

### `u96-a.A9_a_rehearsal_stays_a_rehearsal`

Pass dry_run=False to run_restore whatever was asked, so a rehearsal transfers

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A9_a_rehearsal_stays_a_rehearsal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    portion,
                    cfg,
                    dry_run=dry_run,
```

New text:

```
                    portion,
                    cfg,
                    dry_run=False,
```

### `r172-a.A1_nothing_collides`

Hold nothing, which is the finding itself: two files rendering to one name are promised two renames and the apply performs one

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A1_nothing_collides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_two_files_rendering_to_one_name_are_not_promised_two_renames`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
        if not found:
            return held
        held.update(found)
```

New text:

```
        return held
```

### `r172-a.A2_one_round_only`

Ask once rather than to a fixpoint, so a file whose target a collider still holds reads as a chain sort order would resolve. This is the review's first finding, reintroduced

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A2_one_round_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`

Old text:

```
        if not found:
            return held
        held.update(found)
```

New text:

```
        held.update(found)
        return held
```

### `r172-a.A3_shared_target_ignored`

Stop holding several movers that render to one target, keeping only the occupied target half, so an arbitrary winner in sort order takes the name again

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A3_shared_target_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_two_files_rendering_to_one_name_are_not_promised_two_renames`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
            sharing = sorted(
                other.name for other in holders[_key(str(target))] if other != path
            )
```

New text:

```
            sharing = []
```

### `r172-a.A4_occupied_target_ignored`

Stop holding a mover whose rendered name a file on disk already carries, which is the collision the U67 table drove

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A4_occupied_target_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`

Old text:

```
            elif _key(str(target)) not in sources and target.exists():
```

New text:

```
            elif False:
```

### `r172-a.A5_chain_held_too`

Hold a target another mover still holds, which loses a rename that succeeds whenever sort order reaches the occupant first

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A5_chain_held_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`

Old text:

```
            elif _key(str(target)) not in sources and target.exists():
```

New text:

```
            elif target.exists():
```

### `r172-a.A7_targets_compared_exactly`

Compare targets as written instead of through _key, so two names differing only in case are two names on a volume that treats them as one

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A7_targets_compared_exactly`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
        for path, target in moving:
            holders.setdefault(_key(str(target)), []).append(path)
        sources = {_key(str(path)) for path, _ in moving}
        found: dict[str, str] = {}
        for path, target in moving:
            sharing = sorted(
                other.name for other in holders[_key(str(target))] if other != path
            )
            if len(sharing) == 1:
                found[str(path)] = (
                    f"{sharing[0]} renders to the same name, and neither is renamed"
                )
            elif sharing:
                found[str(path)] = (
                    f"{', '.join(sharing)} render to the same name, and none of them "
                    f"is renamed"
                )
            elif _key(str(target)) not in sources and target.exists():
```

New text:

```
        for path, target in moving:
            holders.setdefault(str(target), []).append(path)
        sources = {str(path) for path, _ in moving}
        found: dict[str, str] = {}
        for path, target in moving:
            sharing = sorted(
                other.name for other in holders[str(target)] if other != path
            )
            if len(sharing) == 1:
                found[str(path)] = (
                    f"{sharing[0]} renders to the same name, and neither is renamed"
                )
            elif sharing:
                found[str(path)] = (
                    f"{', '.join(sharing)} render to the same name, and none of them "
                    f"is renamed"
                )
            elif str(target) not in sources and target.exists():
```

### `r172-a.A9_collides_reported_as_a_rename`

Mark a collision as an ordinary rename in the plan, so nothing in the report says which file is held and the apply attempts it

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A9_collides_reported_as_a_rename`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_two_files_rendering_to_one_name_are_not_promised_two_renames`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
        elif str(path) in collides:
```

New text:

```
        elif False:
```

### `r172-b.B11_collision_step_always`

Tell a person to name a file by hand whatever the reason was, which is the review's second finding reintroduced

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B11_collision_step_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_remediation_only_names_a_hand_rename_over_a_real_collision`

Old text:

```
    if collides:
        steps.append(
```

New text:

```
    if True:
        steps.append(
```

### `r172-b.B12_the_first_file_is_not_named`

Report the counts without naming the first outstanding file, which is the half of the recorded cost about nothing naming which file stayed put

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B12_the_first_file_is_not_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`

Old text:

```
        f"not, the first of them {incomplete[0]['from']}, {incomplete[0]['why']}",
```

New text:

```
        f"not",
```

### `r172-b.B13_detail_carries_nothing`

Drop the outstanding items from the cause detail, so a machine consumer reads a count and no names

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B13_detail_carries_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 10 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_rename_the_filesystem_refuses_is_named_and_leaves_no_claim`
  - `tests/test_naming_apply_cli.py::test_a_row_that_appears_after_the_gate_still_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_a_title_tag_that_could_not_be_written_is_named`
  - `tests/test_naming_apply_cli.py::test_an_artist_tag_removed_while_the_gate_waits_holds_the_file`

Old text:

```
            "incomplete": incomplete[:INCOMPLETE_SHOWN],
```

New text:

```
            "incomplete": [],
```

### `r172-b.B14_diagnostic_surface`

Answer on the default surface, which drops the plan and with it every rename that DID land

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B14_diagnostic_surface`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 6 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_a_title_tag_that_could_not_be_written_is_named`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
        schema=ctx.entry.output_schema or output.current_schema("plan"),
        data=plan,
    )
```

New text:

```
    )
```

### `r172-b.B16_referenced_recheck_dropped`

A sample of an EXISTING guard: trust the plan's own referenced set instead of reading the collection again after the gate, so a file rekordbox imported while a person decided is renamed out from under its row

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B16_referenced_recheck_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_that_appears_after_the_gate_still_protects_its_file`

Old text:

```
        if _is_referenced(path, referenced):
            _owed(
```

New text:

```
        if False:
            _owed(
```

### `r172-b.B17_claim_dropped`

A sample of an EXISTING guard: rename without claiming the target first, which on this platform replaces the file that holds the name

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B17_claim_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`

Old text:

```
            if not naming.claim_target(target):
                collided += 1
```

New text:

```
            if False:
                collided += 1
```

### `r172-b.B1_ok_whatever_happened`

Answer ok however the sweep went, which is the finding itself: a plan carried out in part is reported as one carried out in full

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B1_ok_whatever_happened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 15 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rename_the_filesystem_refuses_is_named_and_leaves_no_claim`
  - `tests/test_naming_apply_cli.py::test_a_row_that_appears_after_the_gate_still_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_a_title_tag_that_could_not_be_written_is_named`
  - `tests/test_naming_apply_cli.py::test_an_artist_tag_removed_while_the_gate_waits_holds_the_file`
  - `tests/test_naming_apply_cli.py::test_the_remediation_only_names_a_hand_rename_over_a_real_collision`
  - `tests/test_naming_apply_cli.py::test_the_report_over_a_held_identifier_says_to_tag_it`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
    if not incomplete:
        return ctx.envelope(data=plan, outcome=Outcome.OK)
```

New text:

```
    return ctx.envelope(data=plan, outcome=Outcome.OK)
```

### `r172-b.B2_missing_file_unreported`

Skip a file that left while the gate waited in silence, as the shipped verb did

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B2_missing_file_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`

Old text:

```
        if not path.is_file():
            _owed(item, "the file is no longer there")
            continue
```

New text:

```
        if not path.is_file():
            continue
```

### `r172-b.B3_new_row_unreported`

Hold back a file the collection began referencing after the gate without saying the approved rename did not happen

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B3_new_row_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_that_appears_after_the_gate_still_protects_its_file`

Old text:

```
            _owed(
                item,
                "the rekordbox collection began referencing it after the plan was "
                "approved, and renaming it would strand that row",
            )
            continue
```

New text:

```
            continue
```

### `r172-b.B5_os_error_unreported`

Swallow a rename the filesystem refused, leaving a person a clean report over a file that did not move

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B5_os_error_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_rename_the_filesystem_refuses_is_named_and_leaves_no_claim`

Old text:

```
                _owed(item, f"the filesystem refused the rename: {exc.strerror or exc}")
                continue
```

New text:

```
                continue
```

### `r172-b.B6_tag_write_answer_ignored`

Stop reading the answer write_tags returns, so a renamed file whose title never took the head is reported as a rename that happened in full

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B6_tag_write_answer_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_title_tag_that_could_not_be_written_is_named`
  - `tests/test_naming_apply_cli.py::test_the_remediation_only_names_a_hand_rename_over_a_real_collision`

Old text:

```
        if not tags.write_tags(path, {"title": rendered.title_tag}):
            _owed(item, "it was renamed and its title tag could not be written", at=path)
```

New text:

```
        tags.write_tags(path, {"title": rendered.title_tag})
```

### `r172-b.B8_tag_failure_named_where_it_was`

Name the tag write failure at the plan's own path, which is the file's name before the rename and a file nobody can go and look at

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B8_tag_failure_named_where_it_was`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_title_tag_that_could_not_be_written_is_named`

Old text:

```
            _owed(item, "it was renamed and its title tag could not be written", at=path)
```

New text:

```
            _owed(item, "it was renamed and its title tag could not be written")
```

### `r172-b.B9_renamed_count_is_the_promise`

Count every promised rename as performed rather than counting the ones that were, so totals.renamed is the plan's wish

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-b.json`, row `B9_renamed_count_is_the_promise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`

Old text:

```
        "renamed": renamed,
        "incomplete": len(incomplete),
```

New text:

```
        "renamed": len(renames),
        "incomplete": len(incomplete),
```

### `r500-a.G1_no_refusal`

Drop the refusal over dark rows in _referenced, so an unmapped row contributes only a key nothing matches and the file it names is renamed (R-500 as filed)

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G1_no_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 13 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`
  - `tests/test_naming_apply_cli.py::test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename`
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_an_unmapped_row_refuses_the_plan_too`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`
  - `tests/test_naming_apply_cli.py::test_the_refusal_names_the_decoded_location_a_rule_is_matched_against`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
    if dark:
        raise _unmapped_refusal(dark)

```

New text:

```
(empty)
```

### `r500-a.G2_existence_half_dropped`

Drop the existence half of dark, so every unmapped row refuses, including a row whose recorded file is on this machine (the first cut the review rejected)

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G2_existence_half_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_whose_file_exists_elsewhere_does_not_hold_a_namesake_in_the_library`

Old text:

```
        elif resolved.resolution is locations.Resolution.UNMAPPED and not os.path.exists(decoded):
```

New text:

```
        elif resolved.resolution is locations.Resolution.UNMAPPED:
```

### `r500-a.G3_unmapped_half_dropped`

Drop the UNMAPPED half of dark, so any unresolved row whose text is not a file here refuses, a streaming pseudo-location included

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G3_unmapped_half_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_device_relative_row_neither_blocks_nor_protects`

Old text:

```
        elif resolved.resolution is locations.Resolution.UNMAPPED and not os.path.exists(decoded):
```

New text:

```
        elif not os.path.exists(decoded):
```

### `r500-a.G4_lexists`

Ask whether the recorded NAME exists rather than whether it reaches a file, so a link to nothing reads as a row that answered

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G4_lexists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`

Old text:

```
not os.path.exists(decoded):
```

New text:

```
not os.path.lexists(decoded):
```

### `r500-a.G5_recorded_key_dropped`

Drop the as recorded key. The existence rule rests on it: an unmapped row whose file exists is excused BECAUSE this key protects the file

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-a.json`, row `G5_recorded_key_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_recorded_through_a_link_is_protected_through_that_link`
  - `tests/test_naming_apply_cli.py::test_a_root_outside_the_library_is_still_checked`

Old text:

```
        keys.add(_key(decoded))

```

New text:

```
(empty)
```

### `r500-b.G9_plural_always`

Move the singular wording's bound, so one row reads as rows

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-b.json`, row `G9_plural_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`

Old text:

```
"collection row records" if count == 1 else
```

New text:

```
"collection row records" if count == 0 else
```

### `r500-c.G11_prefix_cap_halved`

Halve the cap on the detail's prefix list, a coefficient

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-c.json`, row `G11_prefix_cap_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`

Old text:

```
            "unmapped_prefixes": prefixes[:20],
```

New text:

```
            "unmapped_prefixes": prefixes[:10],
```

### `r500-c.G12_remedy_run_doctor`

Carry the deletion pass's run-doctor token, which sends a caller to a report no check of which reads the prefix map

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-c.json`, row `G12_remedy_run_doctor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`

Old text:

```
        remedy=Remedy.FIX_CONFIG_VALUES,
```

New text:

```
        remedy=Remedy.RUN_DOCTOR,
```

### `r500-c.G15_other_host_refuses`

Existing U67 guard, sampled: a row naming another host raises out of the verb rather than being passed over

- File: `src/cratekit/write/naming_cli.py`
- Source: `r500-c.json`, row `G15_other_host_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_naming_another_host_neither_blocks_nor_protects`

Old text:

```
        except locations.LocationDecodeError:
            continue
```

New text:

```
        except locations.LocationDecodeError:
            raise
```

### `u39-author-full.R1_filename_source_dropped`

Head recovery loses the filename source and keeps only the title fallback

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R1_filename_source_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_alone_is_enough_when_the_title_tag_lacks_it`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_wins_when_both_heads_parse_and_disagree`

Old text:

```
    head = (
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)
        or {}
    )

```

New text:

```
    head = (
        naming.parse_head(title, template=template)
        or {}
    )

```

### `u39-author-full.R2_title_fallback_dropped`

Head recovery loses the title fallback that heals the tag then rename crash window

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R2_title_fallback_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_head_inside_the_title_tag_is_not_composed_into_the_body`
  - `tests/test_naming_apply_cli.py::test_the_head_is_recovered_from_the_title_when_the_filename_lost_it`

Old text:

```
    head = (
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)
        or {}
    )

```

New text:

```
    head = (
        naming.parse_head(path.name, template=template)
        or {}
    )

```

### `u39-author-full.R3_bpm_dropped`

The recovered tempo is discarded, reproducing the head destroying defect

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R3_bpm_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 29 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_deduping_rename_converges_on_one_pass`
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`
  - `tests/test_naming_apply_cli.py::test_a_file_with_no_title_tag_takes_its_body_from_the_filename`
  - `tests/test_naming_apply_cli.py::test_a_folder_already_in_convention_proposes_no_rename`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_another_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_head_inside_the_title_tag_is_not_composed_into_the_body`
  - `tests/test_naming_apply_cli.py::test_a_key_tag_that_is_not_camelot_does_not_poison_the_pass`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_does_not_hold_a_name_it_will_never_take`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_is_untouched_and_its_sibling_is_renamed`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_a_row_whose_file_exists_elsewhere_does_not_hold_a_namesake_in_the_library`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - ... and 14 more, see the JSON sidecar

Old text:

```
        bpm=int(head["bpm"]) if "bpm" in head else None,

```

New text:

```
        bpm=None,

```

### `u39-author-full.R4_head_key_overrules_tag`

The stale head key wins over a corrected initialkey tag

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R4_head_key_overrules_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_tag_key_wins_over_a_stale_head_and_the_pass_converges`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")

```

New text:

```
    key = head.get("key") or tag_key

```

### `u39-author-full.R5_junk_tag_admitted`

A non Camelot initialkey tag reaches the renderer instead of being ignored

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R5_junk_tag_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_key_tag_that_is_not_camelot_does_not_poison_the_pass`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")

```

New text:

```
    key = tag_key if tag_key else head.get("key")

```

### `u39-author-full.R6_lossy_flag_dropped`

The shared spec loses the lossy flag, recreating the plan and apply disagreement

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-author-full.json`, row `R6_lossy_flag_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_marker_in_the_filename_alone_is_not_stripped_off`
  - `tests/test_naming_apply_cli.py::test_a_marker_in_the_title_alone_is_still_recovered`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_the_plan_and_the_apply_agree_on_a_marked_file`

Old text:

```
        lossy=marker in path.stem or marker in title,

```

New text:

```
        lossy=False,

```

### `u39-naming-independent.R5_bpm_wrong_type`

The recovered tempo is coerced to float instead of int

- File: `src/cratekit/write/naming_cli.py`
- Source: `u39-naming-independent.json`, row `R5_bpm_wrong_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 71 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_case_variant_of_the_name_still_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFC]`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFD]`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_another_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_database_with_no_matching_row_proceeds`
  - `tests/test_naming_apply_cli.py::test_a_deduping_rename_converges_on_one_pass`
  - `tests/test_naming_apply_cli.py::test_a_device_relative_row_neither_blocks_nor_protects`
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`
  - `tests/test_naming_apply_cli.py::test_a_file_recorded_by_its_real_path_is_protected_through_a_linked_root`
  - ... and 56 more, see the JSON sidecar

Old text:

```
        bpm=int(head["bpm"]) if "bpm" in head else None,

```

New text:

```
        bpm=float(head["bpm"]) if "bpm" in head else None,

```

### `u41-author-full.R1_filename_head_source_dropped`

The filename is no longer a head source, leaving the title as the only one

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-author-full.json`, row `R1_filename_head_source_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_alone_is_enough_when_the_title_tag_lacks_it`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_wins_when_both_heads_parse_and_disagree`

Old text:

```
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)

```

New text:

```
        naming.parse_head(title, template=template)

```

### `u41-author-full.R6_head_key_overrules_tag`

Key precedence reversed, so a corrected key tag can no longer move a file

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-author-full.json`, row `R6_head_key_overrules_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_tag_key_wins_over_a_stale_head_and_the_pass_converges`

Old text:

```
    key = tag_key if tag_key and naming.is_camelot(tag_key) else head.get("key")

```

New text:

```
    key = head.get("key") or (tag_key if tag_key and naming.is_camelot(tag_key) else None)

```

### `u41-author-full.T1_title_tag_fed_the_filename_body`

The title tag is rebuilt from the filename body, which stuffs the artist and the album into every tag the apply pass rewrites

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-author-full.json`, row `T1_title_tag_fed_the_filename_body`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_the_title_tag_is_not_given_the_filename_body`

Old text:

```
        title=naming.strip_head(title, template=template),

```

New text:

```
        title=naming.strip_head(path.stem, template=template),

```

### `u41-author-full.T2_title_field_dropped`

The spec stops carrying a title at all, so render_all falls back to the stem for the tag surface

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-author-full.json`, row `T2_title_field_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_the_title_tag_is_not_given_the_filename_body`

Old text:

```
        title=naming.strip_head(title, template=template),

```

New text:

```
        title=None,

```

### `u41-naming-independent.B1_head_precedence_swapped`

The title's head is parsed before the filename's, so a stale tag head drags a correct filename backwards

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B1_head_precedence_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_the_filename_head_wins_when_both_heads_parse_and_disagree`

Old text:

```
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)

```

New text:

```
        naming.parse_head(title, template=template)
        or naming.parse_head(path.name, template=template)

```

### `u41-naming-independent.B2_filename_head_source_dropped`

The filename is no longer a head source, so only a tag-carried head is recovered

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B2_filename_head_source_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_stem_carrying_text_is_not_recomposed_from_its_tags`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_alone_is_enough_when_the_title_tag_lacks_it`
  - `tests/test_naming_apply_cli.py::test_the_filename_head_wins_when_both_heads_parse_and_disagree`

Old text:

```
        naming.parse_head(path.name, template=template)

```

New text:

```
        None

```

### `u41-naming-independent.B3_title_head_source_dropped`

The title is no longer a head source, so the tag-then-rename crash window stops healing

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B3_title_head_source_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_head_inside_the_title_tag_is_not_composed_into_the_body`
  - `tests/test_naming_apply_cli.py::test_the_head_is_recovered_from_the_title_when_the_filename_lost_it`

Old text:

```
        or naming.parse_head(title, template=template)

```

New text:

```
        or None

```

### `u41-naming-independent.B7_lossy_filename_operand_dropped`

U39's K2: the lossy OR loses its filename operand, so a file marked only in its name is renamed to its unmarked form

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B7_lossy_filename_operand_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_marker_in_the_filename_alone_is_not_stripped_off`

Old text:

```
        lossy=marker in path.stem or marker in title,

```

New text:

```
        lossy=marker in title,

```

### `u41-naming-independent.B8_lossy_title_operand_dropped`

U39's K1: the lossy OR loses its title operand, so a marker surviving only in the tag stops being restored

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `B8_lossy_title_operand_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_marker_in_the_title_alone_is_still_recovered`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`

Old text:

```
        lossy=marker in path.stem or marker in title,

```

New text:

```
        lossy=marker in path.stem,

```

### `u41-naming-independent.C1_plan_no_op_filter_dropped`

Every audio file enters the plan, including the ones already in convention

- File: `src/cratekit/write/naming_cli.py`
- Source: `u41-naming-independent.json`, row `C1_plan_no_op_filter_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 10 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_deduping_rename_converges_on_one_pass`
  - `tests/test_naming_apply_cli.py::test_a_folder_already_in_convention_proposes_no_rename`
  - `tests/test_naming_apply_cli.py::test_a_letterless_stem_that_is_not_a_number_is_carried_as_it_is`
  - `tests/test_naming_apply_cli.py::test_a_marker_in_the_filename_alone_is_not_stripped_off`
  - `tests/test_naming_apply_cli.py::test_a_name_with_no_parseable_head_is_left_as_it_arrives`
  - `tests/test_naming_apply_cli.py::test_a_padded_text_stem_with_tags_plans_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_an_unpadded_head_is_carried_and_padded_with_the_tempo_intact`
  - `tests/test_naming_apply_cli.py::test_the_plan_and_the_apply_agree_on_a_marked_file`
  - `tests/test_naming_apply_cli.py::test_the_tag_key_wins_over_a_stale_head_and_the_pass_converges`

Old text:

```
            if rendered.filename != path.name:

```

New text:

```
            if True:

```

### `u67-round-2.C1_action_filter_and_recheck`

Composite: apply every plan item AND drop the re-check before the rename

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67-round-2.json`, row `C1_action_filter_and_recheck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 19 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_case_variant_of_the_name_still_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFC]`
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFD]`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_file_recorded_by_its_real_path_is_protected_through_a_linked_root`
  - `tests/test_naming_apply_cli.py::test_a_file_recorded_through_a_link_is_protected_through_that_link`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_does_not_hold_a_name_it_will_never_take`
  - `tests/test_naming_apply_cli.py::test_a_referenced_file_is_untouched_and_its_sibling_is_renamed`
  - `tests/test_naming_apply_cli.py::test_a_referenced_identifier_file_is_held_as_referenced_and_never_owed`
  - `tests/test_naming_apply_cli.py::test_a_root_outside_the_library_is_still_checked`
  - `tests/test_naming_apply_cli.py::test_a_row_recorded_as_a_location_url_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_a_row_that_appears_after_the_gate_still_protects_its_file`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    renames = [item for item in plan["items"] if item["action"] == RENAME]
```

New text:

```
    renames = list(plan["items"])
    _is_referenced = lambda path, referenced: False  # noqa: E731
```

### `u67.M2_nfc`

Skip NFC normalisation of the compared path

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M2_nfc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_composition_variant_of_the_name_still_protects_its_file[NFD]`

Old text:

```
    return locations.norm_for_compare(path).casefold()
```

New text:

```
    return path.casefold()
```

### `u67.M3_prefix_resolution`

Drop the prefix mapped spelling of a row

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M3_prefix_resolution`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_a_remapped_volume_still_protects_its_file[prefix_map0]`

Old text:

```
        if resolved.path is not None:
            keys.add(_key(resolved.path))
```

New text:

```
        if False:
            keys.add(_key(resolved.path))
```

### `u67.M6_remote_host_skip`

Let a row naming another host raise instead of being skipped

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M6_remote_host_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_naming_another_host_neither_blocks_nor_protects`

Old text:

```
        except locations.LocationDecodeError:
            continue
```

New text:

```
        except ZeroDivisionError:
            continue
```

### `u67.M7_absolute_spelling`

Ask only the resolved spelling of a candidate

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M7_absolute_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_recorded_through_a_link_is_protected_through_that_link`

Old text:

```
    return _key(str(path.absolute())) in referenced or _key(str(path.resolve())) in referenced
```

New text:

```
    return _key(str(path.resolve())) in referenced
```

### `u67.M8_resolved_spelling`

Ask only the absolute spelling of a candidate

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `M8_resolved_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_recorded_by_its_real_path_is_protected_through_a_linked_root`

Old text:

```
    return _key(str(path.absolute())) in referenced or _key(str(path.resolve())) in referenced
```

New text:

```
    return _key(str(path.absolute())) in referenced
```

### `u67.R1_refusal_to_empty`

A classified open failure reads as an empty collection instead of refusing

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `R1_refusal_to_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_library_with_cloud_sync_on_refuses_and_names_the_real_cause`
  - `tests/test_naming_apply_cli.py::test_a_missing_database_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_an_unopenable_database_refuses_and_renames_nothing`

Old text:

```
    except CratekitError as exc:
        inner = exc.cause
```

New text:

```
    except CratekitError as exc:
        return ()
        inner = exc.cause
```

### `u67.R2_generic_to_empty`

A read that fails after the open reads as an empty collection instead of refusing

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `R2_generic_to_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_read_that_fails_after_the_open_refuses_and_renames_nothing`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - every failed read is one refusal
        raise refuse(
```

New text:

```
    except Exception as exc:  # noqa: BLE001 - every failed read is one refusal
        return ()
        raise refuse(
```

### `u67.R3_remedy_passthrough`

Drop the inner remedy, so the refusal defaults to restore-from-snapshot

- File: `src/cratekit/write/naming_cli.py`
- Source: `u67.json`, row `R3_remedy_passthrough`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_library_with_cloud_sync_on_refuses_and_names_the_real_cause`
  - `tests/test_naming_apply_cli.py::test_a_missing_database_refuses_and_renames_nothing`

Old text:

```
            remedy=inner.remediation.remedy or (None if steps else Remedy.REPORT_DEFECT),
            steps=steps,
```

New text:

```
            remedy=None,
            steps=(),
```

### `u95-a.A1_never_rerooted`

_rooted hands every session its configuration back unchanged, which is main's state: a bare-metal session resolves from the configured root again

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A1_never_rerooted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 7 (killed)
- Killed:
  - `tests/test_restore.py::test_blocking_1_a_bare_metal_session_cannot_be_spent_on_the_library_it_refused`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_never_reads_the_capture_the_refused_library_holds`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_roots_the_configuration_at_its_target`
  - `tests/test_restore.py::test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
    if held.issued_by is not Guard.BARE_METAL:
        return cfg
    target = Path(held.authorises)
```

New text:

```
    if held.issued_by is not None:
        return cfg
    target = Path(held.authorises)
```

### `u95-a.A2_library_sessions_rerooted_too`

Drop the guard test in _rooted, so a library session handed a configuration for ANOTHER library is quietly re-aimed at what it authorises instead of refused

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A2_library_sessions_rerooted_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_library_session_still_refuses_a_configuration_for_another_library`
  - `tests/test_restore.py::test_u95_a_live_recovery_session_plan_is_unchanged_by_golden`

Old text:

```
    if held.issued_by is not Guard.BARE_METAL:
        return cfg
    target = Path(held.authorises)
```

New text:

```
    target = Path(held.authorises)
```

### `u95-a.A3_database_not_carried`

The relocated root no longer carries its database: db_path stays at the configured root while the root moves to the target

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A3_database_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_roots_the_configuration_at_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
    return replace(cfg, library=replace(cfg.library, root=target, db_path=database))
```

New text:

```
    return replace(cfg, library=replace(cfg.library, root=target))
```

### `u95-a.A4_outside_database_refusal_removed`

Delete the by-name refusal for a database kept outside the library, leaving the defect-flavoured authorisation refusal to catch it later

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A4_outside_database_refusal_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name`

Old text:

```
    if not held.authorises_path(database):
        raise _refuse_target(
```

New text:

```
    if False:
        raise _refuse_target(
```

### `u95-a.A5_capture_path_not_rebased`

plan reads the session record's capture path as written, so the capture is taken from the configured root, the volume the identity gate refused

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A5_capture_path_not_rebased`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
    root = capture_root_of(_rebased(record.snapshot_path, recorded_root, rooted_at))
```

New text:

```
    root = capture_root_of(record.snapshot_path)
```

### `u95-a.A6_manifest_not_rebased_in_plan`

plan uses the manifest as read from disk, every path in it still naming the dead root

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A6_manifest_not_rebased_in_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
    captured = _rebased_capture(snapshot.read_manifest(root), recorded_root, rooted_at)
```

New text:

```
    captured = snapshot.read_manifest(root)
```

### `u95-a.A7_manifest_not_rebased_in_preflight`

The run's preflight re-reads the manifest and checks it un-rebased, so it asks the DEAD volume whether the capture is still whole

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A7_manifest_not_rebased_in_preflight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
    captured = _rebased_capture(
        snapshot.read_manifest(decided.capture_root),
        recorded_root,
        Path(cfg.library.root),
    )
```

New text:

```
    captured = snapshot.read_manifest(decided.capture_root)
```

### `u95-a.A8_run_not_rooted`

run resolves from the caller's configuration while plan resolves from the session, the two sources for one answer R-20 forbids

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A8_run_not_rooted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
    cfg = _rooted(configured, held)
    assert_gates_are_open(held, writing=cfg.library.root)
    _assert_rekordbox_closed(process_lister)
    _preflight(
```

New text:

```
    cfg = configured
    assert_gates_are_open(held, writing=cfg.library.root)
    _assert_rekordbox_closed(process_lister)
    _preflight(
```

### `u95-b.B2_manifest_database_not_moved`

_rebased_capture leaves Capture.database at the dead root, the file assert_verified asks the disk about

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B2_manifest_database_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
        database=moved(captured.database),
```

New text:

```
        database=captured.database,
```

### `u95-b.B3_sources_not_moved`

The WRITE side is not re-based: every manifest source still names the configured root

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B3_sources_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
                source=_rebased(entry.source, recorded_root, root),
```

New text:

```
                source=entry.source,
```

### `u95-b.B4_captured_not_moved`

The READ side is not re-based: writes aim at the target while the bytes come from the dead volume, the bypass run the other way

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B4_captured_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
                captured=moved(entry.captured),
```

New text:

```
                captured=entry.captured,
```

### `u95-b.B5_not_idempotent`

Drop the already-under-the-new-root clause, so a path naming a target mounted inside the configured root is moved twice

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B5_not_idempotent`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_recorded_path_is_moved_by_the_rule_config_uses_and_only_once`

Old text:

```
    if parts[: len(here)] == here or parts[: len(there)] != there:
```

New text:

```
    if parts[: len(there)] != there:
```

### `u95-b.B6_recorded_path_not_normalised`

Compare the recorded path's raw parts, so a dotted spelling config calls inside is left unmoved and one it calls outside is moved

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B6_recorded_path_not_normalised`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_recorded_path_is_moved_by_the_rule_config_uses_and_only_once`

Old text:

```
    parts = Path(os.path.normpath(str(recorded))).parts
```

New text:

```
    parts = recorded.parts
```

### `u95-b.B8_outside_path_moved_anyway`

A path under NEITHER root is joined onto the target instead of left where it says it is

- File: `src/cratekit/core/restore.py`
- Source: `u95-b.json`, row `B8_outside_path_moved_anyway`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name`
  - `tests/test_restore.py::test_u95_a_recorded_path_is_moved_by_the_rule_config_uses_and_only_once`

Old text:

```
    if parts[: len(here)] == here or parts[: len(there)] != there:
        return recorded
    return Path(root).joinpath(*parts[len(there) :])
```

New text:

```
    if parts[: len(here)] == here:
        return recorded
    return Path(root).joinpath(*parts[len(there) :])
```

### `u95-b1.B1_manifest_root_not_moved`

RE-MEASURED after test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else learned to compare decisions. _rebased_capture leaves Capture.root at the dead root, which is what _captured_by_key composes coupled entries from

- File: `src/cratekit/core/restore.py`
- Source: `u95-b1.json`, row `B1_manifest_root_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`

Old text:

```
        root=_rebased(captured.root, recorded_root, root),
```

New text:

```
        root=captured.root,
```

### `u95-c.C1_plan_side_guard_removed`

plan no longer checks its own answer, so only a run would find a plan naming an outside path

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C1_plan_side_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_plan_checks_its_own_answer_rather_than_trusting_the_derivation`

Old text:

```
    _assert_plan_is_authorised(steps, pre_restore_root, cfg, held)

```

New text:

```
(empty)
```

### `u95-c.C2_run_side_guard_removed`

The preflight no longer asks the session about a plan value, so a plan built for one directory runs under a session for another

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C2_run_side_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 7 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`
  - `tests/test_restore.py::test_u95_a_step_aimed_at_the_authorised_directory_itself_is_refused`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[a-directory-in-the-library]`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-library-root]`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-staging-store-itself]`
  - `tests/test_restore.py::test_u95_the_staging_directory_is_a_write_location_and_is_authorised_too`

Old text:

```
    _assert_plan_is_authorised(decided.steps, decided.pre_restore_root, cfg, held)

```

New text:

```
(empty)
```

### `u95-c.C3_step_authorisation_removed`

Inside the guard, drop the per step authorisation and leave only the membership test

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C3_step_authorisation_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`

Old text:

```
        assert_gates_are_open(held, writing=step.target)
        if step.target not in allowed:
```

New text:

```
        if step.target not in allowed:
```

### `u95-c.C4_restorable_membership_removed`

Inside the guard, drop the re-derived membership test, so a step aimed at the authorised directory itself is admitted

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C4_restorable_membership_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_step_aimed_at_the_authorised_directory_itself_is_refused`

Old text:

```
        if step.target not in allowed:
            raise refuse(
```

New text:

```
        if False:
            raise refuse(
```

### `u95-c.C5_staging_authorisation_removed`

Inside the guard, drop the authorisation of the staging directory and leave only the store rule

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C5_staging_authorisation_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 498 against a baseline of 498
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_plan_checks_its_own_answer_rather_than_trusting_the_derivation`
  - `tests/test_restore.py::test_u95_the_staging_directory_is_a_write_location_and_is_authorised_too`

Old text:

```
    assert_gates_are_open(held, writing=pre_restore_root)
    store = _pre_restore_root(cfg).parent
```

New text:

```
    store = _pre_restore_root(cfg).parent
```

### `u144-c.C8_question_named`

Library rows: name an unanswered question as a track the library lacks

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u144-c.json`, row `C8_question_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_near_match_is_a_question_named_as_a_miss_and_never_written`

Old text:

```
            return "", UNANSWERED
```

New text:

```
            return "", NOT_HELD
```

