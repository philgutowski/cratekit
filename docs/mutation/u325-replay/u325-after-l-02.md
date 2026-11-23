# Mutation table: u325-after-l-02

Measured by `scripts/mutate.py` on 2026-11-23 00:22 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 76.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:19 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 3, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 62 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r222-b.B12_warnings_from_the_live_configuration` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B14_destination_claimed_unread` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B1_always_enqueue` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 9 | killed |
| `r222-b.B2_any_verb_is_a_twin` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B3_any_library_is_a_twin` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B4_rehearsal_is_a_twin` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `r222-b.B5_whole_payload_compared` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 10 | killed |
| `r222-b.B6_itemless_job_is_a_twin` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B7_unreadable_is_elsewhere` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B8_every_exception_is_unreadable` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B9_mirror_not_compared` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r349-a.A1_failure_write` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `r349-a.A2_success_produced` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 6 | killed |
| `r349-a.A4_envelope_field` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r390-a.A6_backup_transfer_exit_is_permanent` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 4 | killed |
| `u45-round-1.A1_unreadable_reported_as_absent` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `u45-round-1.A4_state_collapsed_to_known` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u45-round-1.C2_refusal_read_as_failure` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 6 | killed |
| `u45-round-1.C3_nothing_ran_accepted` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 8 | killed |
| `u45-round-1.C4_uniform_refusal_flattened` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `u45-round-1.C5_first_refusal_taken` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u45-round-1.C6_partial_run_refused` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `u45-round-1.Q1_resume_drops_the_rehearsal` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u45-round-1.Q2_resume_always_rehearses` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u45-round-1.Q3_resume_loses_the_job` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u45-round-1.Q4_payload_key_not_read` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u45-round-1.R1_reserved_remediation_discarded` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 4 | killed |
| `u45-round-1.R2_slug_flattened` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `u45-round-1.W2_report_from_the_plan` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 11 | killed |
| `u45-round-1.W3_ages_not_read_back` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `u45-round-1.W4_ages_derived_from_the_outcome` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `u45-round-1.W5_publishing_switched_off` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 9 | killed |
| `u45-round-1.W6_rehearsal_becomes_a_real_run` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 6 | killed |
| `u45-round-1.W8_engine_refusal_escapes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u45-round-2.A3_age_seconds_always_none` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u45-round-2.C7_failed_detail_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u50-author.B1_no_items_enqueued` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 38 | killed |
| `u50-author.B3_items_one_portion_only` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 16 | killed |
| `u50-author.W1_no_narrowing` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u50-author.W5_unknown_portion_unchecked` | `src/cratekit/backup/cli.py` | maintainer | 1 file(s) | 99 | 1 | killed |
| `u50-author.W6_fresh_config_in_the_handler` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 26 | killed |
| `u50-review-fixes.R2_empty_job_guard_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u50-zero-rows.B2_items_hardcoded_pair` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `u50-zero-rows.W4b_item_ignored_entirely` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 14 | killed |
| `r154-c.C1_digest_the_word` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r154-c.C2_expected_volume_outside_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r154-c.C3_hand_down_the_flag` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r154-c.C4_pull_flags_dropped` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 4 | killed |
| `r154-c.C5_stated_volume_stops_at_the_verb` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r368-round-2.G6_ancestors_not_walked` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
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
| `r368.G5_paths_compared_as_strings` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r368.G8_target_without_the_off_machine_pull_is_allowed` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r368.G9_target_beside_a_capture_rollback_is_allowed` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r592-b.B7_sample_halves_split` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u211.R1_restore_says_what_the_mirror_left` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.G3_abort_restores_anyway` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.L1_an_unusable_capture_is_filtered_out_of_the_listing` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u27-restore-cli-author.N1_the_default_takes_the_newest_unusable_capture` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u27-restore-cli-author.P1_the_report_recomputes_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.R1_a_backup_refusal_becomes_an_internal_error` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 10 | killed |
| `u27-restore-cli-author.S8_a_rehearsal_performs_the_capture_restore` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-round-2.O2_the_discard_set_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-round-2.R2_the_reserved_remediation_is_replaced_by_the_class_default` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u96-a.A14_target_is_required` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u96-a.A1_acceptance_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u96-a.A2_flag_reaches_the_function` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u96-a.A4_run_inside_the_held_session` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u96-a.A5_the_mirror_is_pulled` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u96-a.A6_a_half_at_a_time` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
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

## Zero rows and what they owe

- `u50-author.W1_no_narrowing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r368-round-2.G6_ancestors_not_walked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r368.G5_paths_compared_as_strings` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r222-b.B12_warnings_from_the_live_configuration`

Describe the reported job from the configuration on disk rather than the one it was frozen against

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B12_warnings_from_the_live_configuration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_warnings_beside_a_reported_job_describe_that_job`

Old text:

```
            described = cfg if frozen is None else frozen
```

New text:

```
            described = cfg
```

### `r222-b.B14_destination_claimed_unread`

Reword the unreadable case to the ordinary sentence's opening, so the warning no longer says the configuration was not rebuilt

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B14_destination_claimed_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`

Old text:

```
        "its frozen configuration could not be rebuilt, so where it writes is "
```

New text:

```
        "its frozen configuration was not consulted, so where it writes is "
```

### `r222-b.B1_always_enqueue`

Never report a twin, which is the finding itself: every ask files another job

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B1_always_enqueue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 9 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_payload_key_this_build_does_not_read_does_not_make_a_stranger`
  - `tests/test_backup_cli.py::test_a_second_ask_for_a_real_backup_is_not_told_the_open_job_copies_nothing`
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`
  - `tests/test_backup_cli.py::test_asking_for_a_backup_twice_reports_the_open_job_rather_than_a_second`
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[archive_root]`
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[dest]`
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`
  - `tests/test_backup_cli.py::test_the_warnings_beside_a_reported_job_describe_that_job`

Old text:

```
        if found is not None:
            twin, frozen = found
```

New text:

```
        if False:
            twin, frozen = found
```

### `r222-b.B2_any_verb_is_a_twin`

Drop the handler key comparison, so another verb's open job is reported as the backup

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B2_any_verb_is_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_another_verb_s_open_job_is_not_a_backup`

Old text:

```
        if job.handler_key != handler_key or job.library_id != cfg.library.volume_id:
```

New text:

```
        if job.library_id != cfg.library.volume_id:
```

### `r222-b.B3_any_library_is_a_twin`

Drop the library comparison, so a job copying another library is reported as this one's backup

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B3_any_library_is_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_another_library_s_open_backup_is_not_this_library_s`

Old text:

```
        if job.handler_key != handler_key or job.library_id != cfg.library.volume_id:
```

New text:

```
        if job.handler_key != handler_key:
```

### `r222-b.B4_rehearsal_is_a_twin`

Drop the rehearsal flag comparison, so an open rehearsal answers a request for a real backup

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B4_rehearsal_is_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_and_a_real_run_are_two_jobs`
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_frozen_payload_and_the_parser_agree_about_the_flag`

Old text:

```
        if bool((job.payload or {}).get(DRY_RUN)) != dry_run:
            continue
```

New text:

```
        if False:
            continue
```

### `r222-b.B5_whole_payload_compared`

Compare the whole payload, so a job frozen with one more key is a stranger and a second backup is filed beside it

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B5_whole_payload_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 10 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_payload_key_this_build_does_not_read_does_not_make_a_stranger`
  - `tests/test_backup_cli.py::test_a_second_ask_for_a_real_backup_is_not_told_the_open_job_copies_nothing`
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`
  - `tests/test_backup_cli.py::test_asking_for_a_backup_twice_reports_the_open_job_rather_than_a_second`
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[archive_root]`
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[dest]`
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`
  - `tests/test_backup_cli.py::test_the_warnings_beside_a_reported_job_describe_that_job`

Old text:

```
        if bool((job.payload or {}).get(DRY_RUN)) != dry_run:
```

New text:

```
        if dict(job.payload or {}) != {DRY_RUN: dry_run}:
```

### `r222-b.B6_itemless_job_is_a_twin`

Report a job with no items, which refuses when driven, as the backup asked for

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B6_itemless_job_is_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_that_can_never_run_does_not_stand_in_for_a_backup`

Old text:

```
        if not jobs.items(store, job.job_id):
            continue
        try:
```

New text:

```
        if False:
            continue
        try:
```

### `r222-b.B7_unreadable_is_elsewhere`

Read a frozen configuration that cannot be rebuilt as somewhere else, and file a second job beside it

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B7_unreadable_is_elsewhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`

Old text:

```
        except (config.ConfigError, ValueError):
            return job, None
```

New text:

```
        except (config.ConfigError, ValueError):
            continue
```

### `r222-b.B8_every_exception_is_unreadable`

Catch every exception from the rebuild, so a defect in it is reported as an open backup with exit zero

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B8_every_exception_is_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`

Old text:

```
        except (config.ConfigError, ValueError):
            return job, None
```

New text:

```
        except Exception:
            return job, None
```

### `r222-b.B9_mirror_not_compared`

Compare only the archive root, so two jobs syncing into one mirror with different archives are strangers

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B9_mirror_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[dest]`

Old text:

```
            frozen.backup.dest == cfg.backup.dest
            or frozen.backup.archive_root == cfg.backup.archive_root
```

New text:

```
            frozen.backup.archive_root == cfg.backup.archive_root
```

### `r349-a.A1_failure_write`

Drop the failure path JSON write: raise the refusal without writing the outcome

- File: `src/cratekit/backup/cli.py`
- Source: `r349-a.json`, row `A1_failure_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
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
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`

Old text:

```
        progress[OUTCOMES] = outcomes
```

New text:

```
        pass
```

### `r390-a.A6_backup_transfer_exit_is_permanent`

the flag the review round added: a transfer exit recorded with no retryable flag

- File: `src/cratekit/backup/cli.py`
- Source: `r390-a.json`, row `A6_backup_transfer_exit_is_permanent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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

### `u45-round-1.Q1_resume_drops_the_rehearsal`

Drop --dry-run from the resume argv, so a queued rehearsal respawns as a real transfer that publishes an age

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `Q1_resume_drops_the_rehearsal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    if payload.get(DRY_RUN):
        argv.append("--dry-run")
```

New text:

```
    pass
```

### `u45-round-1.Q2_resume_always_rehearses`

Always emit --dry-run, the other direction, so a real backup respawns as a rehearsal that copies nothing

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `Q2_resume_always_rehearses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    if payload.get(DRY_RUN):
        argv.append("--dry-run")
```

New text:

```
    argv.append("--dry-run")
```

### `u45-round-1.Q3_resume_loses_the_job`

Drop --job from the resume argv, so the child queues a second backup instead of continuing the first

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `Q3_resume_loses_the_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    return [*argv, "--job", job.job_id]
```

New text:

```
    return list(argv)
```

### `u45-round-1.Q4_payload_key_not_read`

Read a key the handler does not freeze, which is the drift the named constant exists to prevent

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `Q4_payload_key_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    if payload.get(DRY_RUN):
```

New text:

```
    if payload.get("dryrun"):
```

### `u45-round-1.R1_reserved_remediation_discarded`

Replace the reservation table's per-slug remediation with the class default, which is what the first draft did

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `R1_reserved_remediation_discarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
- Kills: 11 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_completed_warns_about_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
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
- Collected: 99 against a baseline of 99
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_completed_warns_about_nothing`
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
- Kills: 9 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_completed_warns_about_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_a_supplied_configuration_is_used_rather_than_the_one_on_disk`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`
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
- Collected: 99 against a baseline of 99
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
- Kills: 38 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion`
  - `tests/test_backup_cli.py::test_a_contained_analysis_share_draws_no_warning_from_the_verb`
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_library_with_an_identity_draws_no_such_warning`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_carries_no_rehearsal_word`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - ... and 23 more, see the JSON sidecar

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
- Collected: 99 against a baseline of 99
- Kills: 16 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_backup_cli.py::test_queueing_still_needs_nothing_from_the_machine`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - `tests/test_backup_cli.py::test_the_item_list_is_derived_from_the_portions_rather_than_written_out`
  - ... and 1 more, see the JSON sidecar

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
- Collected: 22933 against a baseline of 22933
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
- Kills: 26 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_contained_analysis_share_draws_no_warning_from_the_verb`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_library_with_an_identity_draws_no_such_warning`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_carries_no_rehearsal_word`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - `tests/test_backup_cli.py::test_a_resume_reports_the_queued_job_rather_than_filing_a_second`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_that_is_absent_is_warned_at_queue_and_at_resume`
  - ... and 11 more, see the JSON sidecar

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
- Collected: 99 against a baseline of 99
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

### `u50-zero-rows.B2_items_hardcoded_pair`

Name the two portions instead of deriving them, so a third portion is queued by nobody

- File: `src/cratekit/backup/cli.py`
- Source: `u50-zero-rows.json`, row `B2_items_hardcoded_pair`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_item_list_is_derived_from_the_portions_rather_than_written_out`

Old text:

```
    return tuple(str(portion) for portion in backup_facts.Portion)
```

New text:

```
    return ("files", "database")
```

### `u50-zero-rows.W4b_item_ignored_entirely`

Back up the mirror whatever the item says, so every item of the job does the same half

- File: `src/cratekit/backup/cli.py`
- Source: `u50-zero-rows.json`, row `W4b_item_ignored_entirely`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 14 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_queued_backup_runs_every_portion_through_the_real_resume`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_backup_cli.py::test_the_age_a_driven_run_publishes_is_the_engine_s_and_reaches_the_envelope`
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

### `r368-round-2.G6_ancestors_not_walked`

re-measured: ask samefile of the candidate alone, so a differently cased ancestor is missed

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368-round-2.json`, row `G6_ancestors_not_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22933 against a baseline of 22933
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
- Collected: 22933 against a baseline of 22933
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

