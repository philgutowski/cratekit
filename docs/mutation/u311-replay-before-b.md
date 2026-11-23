# Mutation table: u311-replay-before-b

Measured by `scripts/mutate.py` on 2026-11-23 00:38 UTC, branch `HEAD` at `48a0103d`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 21.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-22 22:38 UTC for commit `48a0103d4f0a`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 10, each measured by this driver.

Known failures: 149 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 109 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r154-c.C1_digest_the_word` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r154-c.C2_expected_volume_outside_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r154-c.C3_hand_down_the_flag` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r154-c.C4_pull_flags_dropped` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 4 | killed |
| `r154-c.C5_stated_volume_stops_at_the_verb` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r367.G10_the_report_drops_the_absent_field` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `r368-round-2.G14_the_destination_check_is_equality_only` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
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
| `r592-b.B1_step_on_every_failure` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r592-b.B2_step_on_the_wrong_half` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 5 | killed |
| `r592-b.B4_step_names_the_wrong_directory` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `r592-b.B5_step_names_no_file` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 4 | killed |
| `r592-b.B7_sample_halves_split` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 15 | killed |
| `r592-c.C1_step_on_a_rehearsal_remeasured` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u211.R1_restore_says_what_the_mirror_left` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.G3_abort_restores_anyway` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.L1_an_unusable_capture_is_filtered_out_of_the_listing` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u27-restore-cli-author.N1_the_default_takes_the_newest_unusable_capture` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u27-restore-cli-author.P1_the_report_recomputes_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.P2_a_mirror_pull_is_reported_as_nothing` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.P3_convergence_is_reported_for_a_run_that_spent_no_capture` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u27-restore-cli-author.R1_a_backup_refusal_becomes_an_internal_error` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 12 | killed |
| `u27-restore-cli-author.S6_the_named_decision_is_withdrawn` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 23 | killed |
| `u27-restore-cli-author.S8_a_rehearsal_performs_the_capture_restore` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-round-2.O2_the_discard_set_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-round-2.R2_the_reserved_remediation_is_replaced_by_the_class_default` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 3 | killed |
| `u27-restore-cli-round-2.S7_a_rehearsal_performs_the_mirror_pull` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u96-a.A12_which_half_failed` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u96-a.A13_completed_halves_recorded` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 3 | killed |
| `u96-a.A14_target_is_required` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u96-a.A15_report_names_where_the_database_is` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u96-a.A16_no_absent_companion_for_a_half_that_did_not_run` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u96-a.A1_acceptance_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 3 | killed |
| `u96-a.A2_flag_reaches_the_function` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u96-a.A4_run_inside_the_held_session` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 16 | killed |
| `u96-a.A5_the_mirror_is_pulled` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 15 | killed |
| `u96-a.A6_a_half_at_a_time` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 15 | killed |
| `u96-a.A7_rekordbox_asked_again` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u96-a.A8_database_elsewhere_is_skipped` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u96-a.A9_a_rehearsal_stays_a_rehearsal` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 2 | killed |
| `u317.Q10_token_not_struck` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 59 | 1 | killed |
| `u317.Q14_no_invalidation` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 59 | 4 | killed |
| `u317.Q15_archive_not_rechecked` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 59 | 1 | killed |
| `u317.Q16_token_not_asked` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 59 | 1 | killed |
| `u317.Q19_self_written_empty` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 59 | 6 | killed |
| `u317.Q20_resend_keeps_times` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u317.Q21_send_without_archive` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u317.Q22_flags_do_not_force_a_snapshot` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 59 | 1 | killed |
| `u317.Q24_marker_failure_kept` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 59 | 1 | killed |
| `u317.Q25_second_read_without_scan` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 59 | 1 | killed |
| `u317.Q11_line_break_carried` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 59 | 1 | killed |
| `u317.Q12_root_volume_not_rechecked` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 59 | 1 | killed |
| `u317.Q13_returned_path_archived` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u317.Q1_unlisted_folder_is_absence` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 59 | 1 | killed |
| `u317.Q2_unreadable_folder_is_absence` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 59 | 1 | killed |
| `u317.Q4_racy_file_not_hashed` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u317.Q5_rewrite_not_compared` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u317.Q6_removed_not_found` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 59 | 2 | killed |
| `u317.Q7_only_additions_count` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 59 | 2 | killed |
| `u317.Q8_settled_trusts_the_first_walk` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u317.Q9_doubt_through_plain_copy` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u27-restore-cli-independent.I_A10_an_off_machine_refusal_is_swallowed` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 6 | killed |
| `u27-restore-cli-independent.I_A3_platform_seams_never_reach_the_session` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 15 | killed |
| `u27-restore-cli-independent.I_A8_discard_set_never_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 1 | killed |
| `u27-restore-cli-independent.I_B2_the_named_session_never_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 3 | killed |
| `u27-restore-cli-independent.I_B3_the_discard_flag_is_dropped_at_the_call` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 1 | killed |
| `u27-restore-cli-independent.I_B7_the_rehearsal_flag_is_dropped_at_the_call` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 1 | killed |
| `u27-restore-cli-independent.I_C1_discard_stops_being_repeatable` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 1 | killed |
| `u27-restore-cli-independent.I_C4_the_session_identifier_becomes_required` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 31 | killed |
| `u27-restore-cli-independent.I_C6_the_listing_verb_runs_the_restore` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 4 | killed |
| `u27-restore-cli-independent.I_E4_the_reason_a_capture_cannot_be_spent_is_blanked` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 2 | killed |
| `u27-restore-cli-independent.I_F4_the_refusal_stops_naming_the_identifier` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 1 | killed |
| `u27-restore-cli-independent.X5_the_refusal_reason_is_flattened` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1254 | 11 | killed |
| `u105-b.S10_settings_to_engine` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 2 | killed |
| `u105-b.S1_parts_only_when_several` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 3 | killed |
| `u105-b.S2_lufs_frozen` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 2 | killed |
| `u105-b.S3_lufs_in_argv` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S4_parts_in_argv` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S5_queue_time_refusal` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 3 | killed |
| `u105-b.S6_join_order_notice` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S7_staged_parts` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S8_staged_target` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S9_precheck_name` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 2 | killed |
| `u28-skills-independent.K1_composite` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 11 | killed |
| `u28-skills-independent.S11_typed_cause_lost` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 2 | killed |
| `u28-skills-independent.S12_reason_slug` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 2 | killed |
| `u28-skills-independent.S14_into_ignored` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 10 | killed |
| `u28-skills-independent.S15_drift_never_warns` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `u28-skills-independent.S16_counts_miscounted` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 5 | killed |
| `u28-skills-independent.S18_detail_reworded` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `u28-skills-independent.S19_default_target_literal` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `u28-skills-independent.S5_stamp_quote_strip` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 7 | killed |
| `u28-skills-independent.S9_previous_always_none` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 5 | killed |
| `u323.I1_unread_identity_refuses` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u323.I3_raising_read_escapes` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u323.I5_provider_dropped_by_the_plan` | `src/cratekit/modules/tools/backup.py` | maintainer | 1 file(s) | 37 | 3 | killed |
| `u323.I6_provider_dropped_at_the_gate` | `src/cratekit/modules/tools/backup.py` | maintainer | 1 file(s) | 37 | 3 | killed |
| `r290-author.R2_backup_rebuild_drops_the_type` | `src/cratekit/backup/cli.py` | user | 2 file(s) | 225 | 2 | killed |
| `r290-author.S04_backup_call_removed` | `src/cratekit/backup/cli.py` | user | 2 file(s) | 225 | 12 | killed |
| `r338-c.C4_bare_metal_asks_about_the_share` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 257 | 1 | killed |
| `r338-c.C5_report_loses_the_word` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 257 | 3 | killed |
| `r592-b.B6_restore_mirror_carries_the_database` | `src/cratekit/modules/tools/backup.py` | user | 3 file(s) | 356 | 1 | killed |
| `u27-restore-cli-author.S1_plan_takes_its_own_lock` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 257 | 23 | killed |

## Zero rows and what they owe

- `r368-round-2.G14_the_destination_check_is_equality_only` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r368-round-2.G6_ancestors_not_walked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r368.G5_paths_compared_as_strings` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q20_resend_keeps_times` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q21_send_without_archive` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q13_returned_path_archived` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q4_racy_file_not_hashed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q5_rewrite_not_compared` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q8_settled_trusts_the_first_walk` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q9_doubt_through_plain_copy` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u323.I1_unread_identity_refuses` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u323.I3_raising_read_escapes` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

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
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_restore_from_a_database_only_snapshot_names_the_absent_sidecar`

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
- Collected: 22933 against a baseline of 22933
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

### `r592-b.B1_step_on_every_failure`

_half_failed: give the removal step to a mirror failure too, sending a person to delete files the mirror never lands

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-b.json`, row `B1_step_on_every_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_failed_mirror_stops_the_recovery_before_the_database`
  - `tests/test_restore_cli.py::test_a_recovery_whose_mirror_was_cut_off_reruns_with_nothing_removed`

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
- Collected: 98 against a baseline of 98
- Kills: 5 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_database_half_that_landed_part_of_the_fileset_is_refused_until_the_step`
  - `tests/test_restore_cli.py::test_a_failed_database_half_says_the_mirror_arrived_and_what_to_remove`
  - `tests/test_restore_cli.py::test_a_failed_mirror_stops_the_recovery_before_the_database`
  - `tests/test_restore_cli.py::test_a_recovery_whose_mirror_was_cut_off_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_rekordbox_opened_while_the_mirror_arrives_stops_the_database_half`

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
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_database_half_that_landed_part_of_the_fileset_is_refused_until_the_step`
  - `tests/test_restore_cli.py::test_a_failed_database_half_says_the_mirror_arrived_and_what_to_remove`

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
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_database_half_that_landed_part_of_the_fileset_is_refused_until_the_step`
  - `tests/test_restore_cli.py::test_a_failed_database_half_says_the_mirror_arrived_and_what_to_remove`
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_rekordbox_opened_while_the_mirror_arrives_stops_the_database_half`

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
- Kills: 15 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_database_half_that_landed_part_of_the_fileset_is_refused_until_the_step`
  - `tests/test_restore_cli.py::test_a_database_that_was_never_on_the_lost_volume_is_not_recovered_onto_the_new_one`
  - `tests/test_restore_cli.py::test_a_failed_database_half_says_the_mirror_arrived_and_what_to_remove`
  - `tests/test_restore_cli.py::test_a_failed_mirror_stops_the_recovery_before_the_database`
  - `tests/test_restore_cli.py::test_a_mirror_still_carrying_the_database_does_not_land_it`
  - `tests/test_restore_cli.py::test_a_recovery_lands_the_mirror_and_the_database_only_under_the_target`
  - `tests/test_restore_cli.py::test_a_recovery_whose_database_half_failed_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_a_recovery_whose_mirror_was_cut_off_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_a_rehearsal_passes_the_same_gates_and_writes_nothing`
  - `tests/test_restore_cli.py::test_a_rehearsal_whose_database_half_failed_sends_nobody_to_remove_anything`
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_both_halves_run_inside_one_holding_of_the_recovery_lock`
  - `tests/test_restore_cli.py::test_every_transfer_is_pointed_under_the_target_and_nowhere_else`
  - `tests/test_restore_cli.py::test_rekordbox_opened_while_the_mirror_arrives_stops_the_database_half`
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
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_rehearsal_whose_database_half_failed_sends_nobody_to_remove_anything`

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
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`

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
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`
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
- Kills: 12 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_failed_transfer_refuses_and_never_reports_a_restore_that_did_not_happen`
  - `tests/test_restore_cli.py::test_a_recovery_is_refused_underneath_a_running_rekordbox`
  - `tests/test_restore_cli.py::test_a_recovery_with_no_rclone_installed_refuses_by_name_and_writes_nothing`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_rehearsal_whose_preview_fails_refuses_rather_than_reading_as_a_pass`
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
- Kills: 23 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_failed_transfer_refuses_and_never_reports_a_restore_that_did_not_happen`
  - `tests/test_restore_cli.py::test_a_live_restore_in_the_outside_layout_withholds_the_share_and_closes_clean`
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_rehearsal_neutralizes_the_mirror_transfers_too`
  - `tests/test_restore_cli.py::test_a_rehearsal_whose_preview_fails_refuses_rather_than_reading_as_a_pass`
  - `tests/test_restore_cli.py::test_a_restore_from_a_database_only_snapshot_names_the_absent_sidecar`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[-pulled1-absent]`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[PIONEER/\n-pulled0-pulled]`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_a_transfer_that_succeeds_is_still_reported`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - ... and 8 more, see the JSON sidecar

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
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_failed_transfer_refuses_and_never_reports_a_restore_that_did_not_happen`
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
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_rehearsal_neutralizes_the_mirror_transfers_too`
  - `tests/test_restore_cli.py::test_a_rehearsal_whose_preview_fails_refuses_rather_than_reading_as_a_pass`

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
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_failed_database_half_says_the_mirror_arrived_and_what_to_remove`
  - `tests/test_restore_cli.py::test_a_failed_mirror_stops_the_recovery_before_the_database`

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
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_failed_database_half_says_the_mirror_arrived_and_what_to_remove`
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_rekordbox_opened_while_the_mirror_arrives_stops_the_database_half`

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
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_database_that_was_never_on_the_lost_volume_is_not_recovered_onto_the_new_one`

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
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_database_that_was_never_on_the_lost_volume_is_not_recovered_onto_the_new_one`

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
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_refusal_before_the_lock_leaves_the_disk_untouched[the replacement was not accepted]`
  - `tests/test_restore_cli.py::test_a_rehearsal_passes_the_same_gates_and_writes_nothing`
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
- Kills: 16 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_database_half_that_landed_part_of_the_fileset_is_refused_until_the_step`
  - `tests/test_restore_cli.py::test_a_database_that_was_never_on_the_lost_volume_is_not_recovered_onto_the_new_one`
  - `tests/test_restore_cli.py::test_a_failed_database_half_says_the_mirror_arrived_and_what_to_remove`
  - `tests/test_restore_cli.py::test_a_failed_mirror_stops_the_recovery_before_the_database`
  - `tests/test_restore_cli.py::test_a_failed_rehearsal_says_nothing_was_written`
  - `tests/test_restore_cli.py::test_a_mirror_still_carrying_the_database_does_not_land_it`
  - `tests/test_restore_cli.py::test_a_recovery_lands_the_mirror_and_the_database_only_under_the_target`
  - `tests/test_restore_cli.py::test_a_recovery_whose_database_half_failed_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_a_recovery_whose_mirror_was_cut_off_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_a_rehearsal_passes_the_same_gates_and_writes_nothing`
  - `tests/test_restore_cli.py::test_a_rehearsal_whose_database_half_failed_sends_nobody_to_remove_anything`
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_both_halves_run_inside_one_holding_of_the_recovery_lock`
  - `tests/test_restore_cli.py::test_every_transfer_is_pointed_under_the_target_and_nowhere_else`
  - `tests/test_restore_cli.py::test_rekordbox_opened_while_the_mirror_arrives_stops_the_database_half`
  - ... and 1 more, see the JSON sidecar

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
- Kills: 15 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_database_half_that_landed_part_of_the_fileset_is_refused_until_the_step`
  - `tests/test_restore_cli.py::test_a_database_that_was_never_on_the_lost_volume_is_not_recovered_onto_the_new_one`
  - `tests/test_restore_cli.py::test_a_failed_database_half_says_the_mirror_arrived_and_what_to_remove`
  - `tests/test_restore_cli.py::test_a_failed_mirror_stops_the_recovery_before_the_database`
  - `tests/test_restore_cli.py::test_a_failed_rehearsal_says_nothing_was_written`
  - `tests/test_restore_cli.py::test_a_mirror_still_carrying_the_database_does_not_land_it`
  - `tests/test_restore_cli.py::test_a_recovery_lands_the_mirror_and_the_database_only_under_the_target`
  - `tests/test_restore_cli.py::test_a_recovery_whose_database_half_failed_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_a_recovery_whose_mirror_was_cut_off_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_a_rehearsal_passes_the_same_gates_and_writes_nothing`
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_both_halves_run_inside_one_holding_of_the_recovery_lock`
  - `tests/test_restore_cli.py::test_every_transfer_is_pointed_under_the_target_and_nowhere_else`
  - `tests/test_restore_cli.py::test_rekordbox_opened_while_the_mirror_arrives_stops_the_database_half`
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
- Kills: 15 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_database_half_that_landed_part_of_the_fileset_is_refused_until_the_step`
  - `tests/test_restore_cli.py::test_a_database_that_was_never_on_the_lost_volume_is_not_recovered_onto_the_new_one`
  - `tests/test_restore_cli.py::test_a_failed_database_half_says_the_mirror_arrived_and_what_to_remove`
  - `tests/test_restore_cli.py::test_a_failed_mirror_stops_the_recovery_before_the_database`
  - `tests/test_restore_cli.py::test_a_mirror_still_carrying_the_database_does_not_land_it`
  - `tests/test_restore_cli.py::test_a_recovery_lands_the_mirror_and_the_database_only_under_the_target`
  - `tests/test_restore_cli.py::test_a_recovery_whose_database_half_failed_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_a_recovery_whose_mirror_was_cut_off_reruns_with_nothing_removed`
  - `tests/test_restore_cli.py::test_a_rehearsal_passes_the_same_gates_and_writes_nothing`
  - `tests/test_restore_cli.py::test_a_rehearsal_whose_database_half_failed_sends_nobody_to_remove_anything`
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_both_halves_run_inside_one_holding_of_the_recovery_lock`
  - `tests/test_restore_cli.py::test_every_transfer_is_pointed_under_the_target_and_nowhere_else`
  - `tests/test_restore_cli.py::test_rekordbox_opened_while_the_mirror_arrives_stops_the_database_half`
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
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_rekordbox_opened_while_the_mirror_arrives_stops_the_database_half`

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
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_database_that_was_never_on_the_lost_volume_is_not_recovered_onto_the_new_one`

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
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_rehearsal_passes_the_same_gates_and_writes_nothing`
  - `tests/test_restore_cli.py::test_a_rehearsal_whose_database_half_failed_sends_nobody_to_remove_anything`

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

### `u317.Q10_token_not_struck`

run_backup: the record's token stays in the library's fact while a run sends, so a failed run of another installation leaves its record trusted (round two's finding)

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q10_token_not_struck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_run_that_fails_strikes_the_token_from_the_library_fact`

Old text:

```
                    _strike_token(cfg)
```

New text:

```
                    pass
```

### `u317.Q14_no_invalidation`

run_backup: the record is not removed before a transfer, so a failed run leaves it to be trusted

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q14_no_invalidation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_full_run_that_fails_leaves_no_record_behind`
  - `tests/test_backup_quick.py::test_a_quick_run_that_fails_midway_resets_no_age_and_leaves_no_record[quick-archive]`
  - `tests/test_backup_quick.py::test_a_quick_run_that_fails_midway_resets_no_age_and_leaves_no_record[quick-send]`
  - `tests/test_backup_quick.py::test_a_record_that_cannot_be_removed_stops_the_run_before_it_sends`

Old text:

```
                backup_record.invalidate(_record_path(entry.portion))
```

New text:

```
                pass
```

### `u317.Q15_archive_not_rechecked`

run_backup: the quick archive runs without asking still_removed first

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q15_archive_not_rechecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_send_runs_only_while_the_root_is_the_volume_walked`

Old text:

```
                if stale:
                    failed = CommandResult(
```

New text:

```
                if False:
                    failed = CommandResult(
```

### `u317.Q16_token_not_asked`

_plan_files: the library's files fact is not asked for the record's token, so another writer's run is not seen (round one's B1)

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q16_token_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_fact_published_by_a_build_before_u317_makes_the_next_run_full`

Old text:

```
    if manifest is not None and not why:
        why = _record_unpublished(cfg, manifest)
```

New text:

```
    if manifest is not None and not why:
        why = ""
```

### `u317.Q19_self_written_empty`

_self_written: the fact file counts as a change, so no run after a backup is ever skipped

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q19_self_written_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_skip_carries_the_record_on_so_the_run_after_it_trusts_it`
  - `tests/test_backup_quick.py::test_an_excluded_system_folder_that_cannot_be_listed_is_never_entered`
  - `tests/test_backup_quick.py::test_doctor_names_the_last_run_and_the_next_full_check`
  - `tests/test_backup_quick.py::test_nothing_changed_is_a_skip_that_sends_nothing_and_resets_both_ages`
  - `tests/test_backup_quick.py::test_the_fact_file_alone_changed_is_still_a_skip`
  - `tests/test_backup_quick.py::test_the_last_full_check_eight_days_old_makes_a_full_run`

Old text:

```
    return frozenset({rel.as_posix()})
```

New text:

```
    return frozenset()
```

### `u317.Q20_resend_keeps_times`

_quick_commands: the resend loses --ignore-times, so a rewrite with its size and time kept is never sent

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q20_resend_keeps_times`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    rclone, "copy", root, dest, *listed, "--ignore-times",
```

New text:

```
                    rclone, "copy", root, dest, *listed,
```

### `u317.Q21_send_without_archive`

_quick_commands: the send loses --backup-dir, so an overwritten version is not archived

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q21_send_without_archive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    rclone, "copy", root, dest, *listed, "--backup-dir", archive,
```

New text:

```
                    rclone, "copy", root, dest, *listed,
```

### `u317.Q22_flags_do_not_force_a_snapshot`

plan_backup: --check and --full do not force a snapshot of an unchanged database

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q22_flags_do_not_force_a_snapshot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_the_check_flag_makes_a_full_run_and_a_snapshot_over_an_unchanged_library`

Old text:

```
                snapshot_anyway=check or full,
```

New text:

```
                snapshot_anyway=False,
```

### `u317.Q24_marker_failure_kept`

_settle_record: a snapshot whose marker failed keeps its fingerprint, so it is never retaken (round one's R2)

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q24_marker_failure_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_snapshot_whose_marker_failed_is_taken_again_next_time`

Old text:

```
            if marker_failed:
                why = "the snapshot's identity marker could not be written"
            elif _not_confirmed_gone(lister):
```

New text:

```
            if _not_confirmed_gone(lister):
```

### `u317.Q25_second_read_without_scan`

_settle_record: the database is read again with no second process scan (round one's R4)

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q25_second_read_without_scan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_the_second_reading_of_the_database_waits_on_a_second_scan`

Old text:

```
            elif _not_confirmed_gone(lister):
                why = "rekordbox was not confirmed gone after the copy"
            elif
```

New text:

```
            elif
```

### `u317.Q11_line_break_carried`

_carriable: a name holding a line break is put on rclone's list of paths

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q11_line_break_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_name_holding_a_line_break_makes_a_full_run`

Old text:

```
    if "\n" in rel or "\r" in rel:
```

New text:

```
    if False:
```

### `u317.Q12_root_volume_not_rechecked`

still_removed: a quick run's archive runs over a root that went away or changed volume (round one's B2)

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q12_root_volume_not_rechecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_send_runs_only_while_the_root_is_the_volume_walked`

Old text:

```
        if os.stat(root).st_dev != root_dev:
            return f"the library root {root} is on another volume than the one walked"
    except OSError as exc:
        return f"the library root {root} could not be read before the archive: {exc}"
```

New text:

```
        pass
    except OSError:
        pass
```

### `u317.Q13_returned_path_archived`

still_removed: a removed path that came back after the plan is archived off the mirror

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q13_returned_path_archived`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        return f"{rel} was found removed by the walk and is there again"
```

New text:

```
        continue
```

### `u317.Q1_unlisted_folder_is_absence`

walk: a listed folder that is gone is skipped as absent, so its files read as removed (round one's B2)

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q1_unlisted_folder_is_absence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_folder_gone_between_being_listed_and_being_read_makes_a_full_run`

Old text:

```
            raise WalkRefused(
                f"{directory} was listed and then was not there, so the walk did "
                f"not see the whole library"
            ) from None
```

New text:

```
            continue
```

### `u317.Q2_unreadable_folder_is_absence`

walk: a folder that cannot be listed is skipped, so its files read as removed

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q2_unreadable_folder_is_absence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_folder_that_cannot_be_listed_makes_a_full_run_and_never_an_archive`

Old text:

```
            raise WalkRefused(f"{directory} could not be listed: {exc}") from exc
```

New text:

```
            continue
```

### `u317.Q4_racy_file_not_hashed`

walk: a file inside the racy window is not hashed, so a rewrite keeping size and time is skipped

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q4_racy_file_not_hashed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            if rel in must_hash or status.st_mtime_ns >= racy_after_ns:
```

New text:

```
            if rel in must_hash:
```

### `u317.Q5_rewrite_not_compared`

difference: a hash that moved under a kept size and time is not a change

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q5_rewrite_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        elif was.sha256 is not None and was.sha256 != now.sha256:
```

New text:

```
        elif False:
```

### `u317.Q6_removed_not_found`

difference: a path in the record and not in the walk is not removed

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q6_removed_not_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_quick_run_that_fails_midway_resets_no_age_and_leaves_no_record[quick-archive]`
  - `tests/test_backup_quick.py::test_no_skip_while_anything_changed`

Old text:

```
    removed = [rel for rel in recorded if rel not in walked]
```

New text:

```
    removed = []
```

### `u317.Q7_only_additions_count`

Difference.anything: only added paths count, so a change or a removal is skipped

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q7_only_additions_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_changed_name_in_decomposed_form_makes_a_full_run`
  - `tests/test_backup_quick.py::test_no_skip_while_anything_changed`

Old text:

```
        return any(path not in self.self_written for path in self.paths)
```

New text:

```
        return any(path not in self.self_written for path in self.added)
```

### `u317.Q8_settled_trusts_the_first_walk`

settled: every entry of the walk before the transfer is trusted, so a file changed mid run is never sent again

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q8_settled_trusts_the_first_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        out[rel] = was if now is not None and was.agrees(now) else DOUBT
```

New text:

```
        out[rel] = was
```

### `u317.Q9_doubt_through_plain_copy`

difference: a present doubt is a plain change, so it is never resent with the times ignored (round one's R1)

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q9_doubt_through_plain_copy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        elif was == DOUBT:
            doubted.append(rel)
```

New text:

```
        elif was == DOUBT:
            changed.append(rel)
```

### `u27-restore-cli-independent.I_A10_an_off_machine_refusal_is_swallowed`

Continue past a refused off-machine half instead of translating it, so the capture half runs over a mirror that never landed

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_A10_an_off_machine_refusal_is_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 6 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_failed_transfer_refuses_and_never_reports_a_restore_that_did_not_happen`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_rehearsal_whose_preview_fails_refuses_rather_than_reading_as_a_pass`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_arrives_as_a_cause_and_not_as_a_bare_exception`
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_carries_the_reserved_remediation_and_not_the_class_default`

Old text:

```
            except backup.BackupRefused as exc:
                raise _refused(exc) from exc
```

New text:

```
            except backup.BackupRefused:
                pulled = None
```

### `u27-restore-cli-independent.I_A3_platform_seams_never_reach_the_session`

Drop the identity and mount seams from recovery_session, so the volume gate answers from this machine rather than from the caller

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_A3_platform_seams_never_reach_the_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 15 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_failed_transfer_refuses_and_never_reports_a_restore_that_did_not_happen`
  - `tests/test_restore_cli.py::test_a_live_restore_in_the_outside_layout_withholds_the_share_and_closes_clean`
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`
  - `tests/test_restore_cli.py::test_a_rehearsal_neutralizes_the_mirror_transfers_too`
  - `tests/test_restore_cli.py::test_a_rehearsal_whose_preview_fails_refuses_rather_than_reading_as_a_pass`
  - `tests/test_restore_cli.py::test_a_restore_from_a_database_only_snapshot_names_the_absent_sidecar`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[-pulled1-absent]`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[PIONEER/\n-pulled0-pulled]`
  - `tests/test_restore_cli.py::test_a_transfer_that_succeeds_is_still_reported`
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_carries_the_reserved_remediation_and_not_the_class_default`
  - `tests/test_restore_cli.py::test_both_halves_of_a_restore_run_inside_one_acquisition_of_the_lock`
  - `tests/test_restore_cli.py::test_include_mirror_adds_the_file_half_and_its_absence_leaves_it_out`
  - `tests/test_restore_cli.py::test_the_mirror_is_pulled_before_the_capture_is_spent`
  - `tests/test_restore_cli.py::test_the_session_watches_the_whole_library_and_not_a_folder_inside_it`
  - `tests/test_restore_cli.py::test_the_snapshot_flag_chooses_which_dated_snapshot_is_pulled`

Old text:

```
        analysis_roots=watched,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    ) as held:
```

New text:

```
        analysis_roots=watched,
    ) as held:
```

### `u27-restore-cli-independent.I_A8_discard_set_never_reaches_the_engine`

Plan with an empty discard set, so the override a person typed is dropped between the verb and the engine

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_A8_discard_set_never_reaches_the_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_discard_override_reaches_the_engine_as_identifiers`

Old text:

```
        decided = restore.plan(
            cfg,
            session_id,
            held=held,
            discarding=discarding,
            process_lister=process_lister,
        )
```

New text:

```
        decided = restore.plan(
            cfg,
            session_id,
            held=held,
            discarding=(),
            process_lister=process_lister,
        )
```

### `u27-restore-cli-independent.I_B2_the_named_session_never_reaches_the_engine`

Pass no session identifier at all, so a named restore performs only the off-machine half

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_B2_the_named_session_never_reaches_the_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_dry_run_walks_every_step_and_performs_none_of_them`
  - `tests/test_restore_cli.py::test_the_confirmation_is_two_acts_and_then_the_database_comes_back`
  - `tests/test_restore_cli.py::test_the_discard_override_reaches_the_engine_as_identifiers`

Old text:

```
        session_id=chosen.session_id if chosen is not None else None,
        discarding=tuple(ctx.args.discard),
```

New text:

```
        session_id=None,
        discarding=tuple(ctx.args.discard),
```

### `u27-restore-cli-independent.I_B3_the_discard_flag_is_dropped_at_the_call`

Hand the engine an empty discard set from the handler, the argument-side twin of I_A8

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_B3_the_discard_flag_is_dropped_at_the_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_discard_override_reaches_the_engine_as_identifiers`

Old text:

```
        session_id=chosen.session_id if chosen is not None else None,
        discarding=tuple(ctx.args.discard),
```

New text:

```
        session_id=chosen.session_id if chosen is not None else None,
        discarding=(),
```

### `u27-restore-cli-independent.I_B7_the_rehearsal_flag_is_dropped_at_the_call`

Perform for real whatever --dry-run said, the argument-side twin of the author's two in-function rehearsal rows

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_B7_the_rehearsal_flag_is_dropped_at_the_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_dry_run_walks_every_step_and_performs_none_of_them`

Old text:

```
        dry_run=ctx.args.dry_run,
        from_backup=ctx.args.from_backup,
```

New text:

```
        dry_run=False,
        from_backup=ctx.args.from_backup,
```

### `u27-restore-cli-independent.I_C1_discard_stops_being_repeatable`

Take a single discard identifier rather than an appended list, so a person discarding two sessions names one and the string is iterated character by character

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_C1_discard_stops_being_repeatable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_discard_override_reaches_the_engine_as_identifiers`

Old text:

```
        "--discard",
        action="append",
        default=[],
```

New text:

```
        "--discard",
        default="",
```

### `u27-restore-cli-independent.I_C4_the_session_identifier_becomes_required`

Make the positional mandatory, so a bare crate restore run is a usage error rather than the newest spendable capture

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_C4_the_session_identifier_becomes_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 31 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_1_structured_output_is_actually_emitted[restore.run]`
  - `tests/test_cli_contract.py::test_conformance_2_exit_codes_are_from_the_vocabulary_and_never_status_two[restore.run]`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[restore.run]`
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_backup_landing_between_the_two_acts_moves_the_digest`
  - `tests/test_restore_cli.py::test_a_database_that_is_not_on_disk_yet_is_still_the_live_database`
  - `tests/test_restore_cli.py::test_a_differently_cased_ancestor_still_puts_the_target_inside_the_library`
  - `tests/test_restore_cli.py::test_a_differently_cased_database_directory_is_still_the_live_database`
  - `tests/test_restore_cli.py::test_a_differently_cased_library_root_is_still_the_library`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_relative_target_is_compared_as_the_place_it_names`
  - `tests/test_restore_cli.py::test_a_target_beside_a_capture_rollback_is_refused[extra0]`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - ... and 16 more, see the JSON sidecar

Old text:

```
        "session_id",
        nargs="?",
        default=None,
```

New text:

```
        "session_id",
```

### `u27-restore-cli-independent.I_C6_the_listing_verb_runs_the_restore`

Bind the read-only listing to the destructive handler

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_C6_the_listing_verb_runs_the_restore`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_capture_this_product_pruned_is_refused_by_name_and_not_as_a_defect`
  - `tests/test_restore_cli.py::test_a_session_whose_capture_is_gone_is_listed_and_says_why`
  - `tests/test_restore_cli.py::test_the_listing_answers_on_a_library_that_has_never_acknowledged_a_backup`
  - `tests/test_restore_cli.py::test_the_listing_shows_a_session_with_its_timestamp_workflow_and_per_tree_counts`

Old text:

```
    parser.set_defaults(_handler=list_restorable)
```

New text:

```
    parser.set_defaults(_handler=perform_restore)
```

### `u27-restore-cli-independent.I_E4_the_reason_a_capture_cannot_be_spent_is_blanked`

List an unusable capture with no sentence saying why, which is the silence the field exists to avoid

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_E4_the_reason_a_capture_cannot_be_spent_is_blanked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_capture_this_product_pruned_is_refused_by_name_and_not_as_a_defect`
  - `tests/test_restore_cli.py::test_a_session_whose_capture_is_gone_is_listed_and_says_why`

Old text:

```
        "unusable": entry.unusable,
```

New text:

```
        "unusable": "",
```

### `u27-restore-cli-independent.I_F4_the_refusal_stops_naming_the_identifier`

Reword the refusal so it never repeats what was typed, which is what makes a typo diagnosable

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_F4_the_refusal_stops_naming_the_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_session_identifier_nothing_recorded_is_refused_by_name`

Old text:

```
                f"no write session on this library is recorded under "
                f"{session_id!r}; the listing verb shows every one that is"
```

New text:

```
                "no such write session is recorded on this library; the "
                "listing verb shows every one that is"
```

### `u27-restore-cli-independent.X5_the_refusal_reason_is_flattened`

What the refusal-message zero DOES leave held: fold the off-machine slug into an internal error, which is the half a drive does assert. Paired with I_F1, which replaced the sentence and killed nothing

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `X5_the_refusal_reason_is_flattened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1254 against a baseline of 1254
- Kills: 11 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_failed_transfer_refuses_and_never_reports_a_restore_that_did_not_happen`
  - `tests/test_restore_cli.py::test_a_recovery_is_refused_underneath_a_running_rekordbox`
  - `tests/test_restore_cli.py::test_a_recovery_with_no_rclone_installed_refuses_by_name_and_writes_nothing`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_rehearsal_whose_preview_fails_refuses_rather_than_reading_as_a_pass`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_arrives_as_a_cause_and_not_as_a_bare_exception`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_another_librarys_snapshot_is_refused_at_the_verb_and_names_both_volumes`
  - `tests/test_restore_cli.py::test_the_ledgers_traversal_value_is_refused_at_the_verb`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`

Old text:

```
            reason=slug,
            message=exc.detail,
```

New text:

```
            reason="internal-error",
            message=exc.detail,
```

### `u105-b.S10_settings_to_engine`

Call the engine without the settings built from the frozen target

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S10_settings_to_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_the_target_reaches_every_loudnorm_filter`

Old text:

```
            settings=settings,
            output_dir=Path(output_dir) if output_dir else None,
```

New text:

```
            output_dir=Path(output_dir) if output_dir else None,
```

### `u105-b.S1_parts_only_when_several`

Freeze the parts key for a single recording too

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S1_parts_only_when_several`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 3 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`
  - `tests/test_master_cli.py::test_one_input_freezes_queues_and_resumes_exactly_as_before`

Old text:

```
    if len(frozen) > 1:
```

New text:

```
    if frozen:
```

### `u105-b.S2_lufs_frozen`

Do not freeze --lufs into the payload

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S2_lufs_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_the_target_reaches_every_loudnorm_filter`

Old text:

```
        payload[TARGET_LUFS] = float(lufs)
```

New text:

```
        pass
```

### `u105-b.S3_lufs_in_argv`

Drop --lufs from the resume command line

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S3_lufs_in_argv`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`

Old text:

```
        argv.append(f"--lufs={lufs}")
```

New text:

```
        pass
```

### `u105-b.S4_parts_in_argv`

Rebuild the resume command line from the first part alone

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S4_parts_in_argv`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`

Old text:

```
    argv = ["master", *frozen_parts(payload)]
```

New text:

```
    argv = ["master", str(payload.get(SOURCE) or "")]
```

### `u105-b.S5_queue_time_refusal`

Stop validating --lufs at queue time

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S5_queue_time_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 3 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-4]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-71]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[nan]`

Old text:

```
    settings_for(ctx.args.lufs)
```

New text:

```
    pass
```

### `u105-b.S6_join_order_notice`

Queue a split recording without saying its order back

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S6_join_order_notice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_the_order_printed_is_the_order_given`

Old text:

```
        notices = (join_order_warning(frozen_parts(payload)),) if PARTS in payload else ()
```

New text:

```
        notices = ()
```

### `u105-b.S7_staged_parts`

Stage a split recording's run without its parts, mastering part one alone

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S7_staged_parts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`

Old text:

```
        staged[PARTS] = [str(p) for p in parts]
```

New text:

```
        pass
```

### `u105-b.S8_staged_target`

Stage the run without the frozen target, mastering at the default

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S8_staged_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`

Old text:

```
        staged[TARGET_LUFS] = payload[TARGET_LUFS]
```

New text:

```
        pass
```

### `u105-b.S9_precheck_name`

Pre-check the destination with part one's master name instead of the joined one

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S9_precheck_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`

Old text:

```
    final = mastering.planned_output(
        parts, output_dir=Path(str(output_dir)) if output_dir else None
    )
```

New text:

```
    final = mastering.output_path(
        parts[0], output_dir=Path(str(output_dir)) if output_dir else None
    )
```

### `u28-skills-independent.K1_composite`

What K1 does hold: break the packaged root's package name so the shipped assets cannot be resolved

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `K1_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 11 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_clean_directory_gets_every_shipped_skill_with_a_stamp`
  - `tests/test_skills_install.py::test_a_file_a_previous_install_wrote_and_this_build_withdrew_disappears`
  - `tests/test_skills_install.py::test_a_file_the_product_never_wrote_survives_a_refresh`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_an_up_to_date_install_writes_nothing_at_all`
  - `tests/test_skills_install.py::test_every_shipped_skill_is_installed_and_the_set_is_walked_not_listed`
  - `tests/test_skills_install.py::test_install_one_reports_which_of_the_three_things_happened`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`
  - `tests/test_skills_install.py::test_the_copies_are_copies_and_not_symlinks`
  - `tests/test_skills_install.py::test_the_packaged_root_resolves_through_the_package`

Old text:

```
    return resources.files("cratekit.skills") / "assets"
```

New text:

```
    return resources.files("cratekit.skills") / "skills"
```

### `u28-skills-independent.S11_typed_cause_lost`

install_skills stops converting the mkdir OSError into a typed cause, so an unwritable target arrives as an internal error

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S11_typed_cause_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 2 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_refusal_leaves_no_half_written_target`
  - `tests/test_skills_install.py::test_a_target_that_cannot_be_created_refuses_with_a_typed_cause`

Old text:

```
    try:
        into.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise CratekitError(
            Cause(
                reason="path-permission-denied",
```

New text:

```
    if True:
        into.mkdir(parents=True, exist_ok=True)
    if False:
        raise CratekitError(
            Cause(
                reason="path-permission-denied",
```

### `u28-skills-independent.S12_reason_slug`

the refusal's reason slug is changed to a neighbouring one, so the typed cause names the wrong condition

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S12_reason_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 2 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_refusal_leaves_no_half_written_target`
  - `tests/test_skills_install.py::test_a_target_that_cannot_be_created_refuses_with_a_typed_cause`

Old text:

```
                reason="path-permission-denied",
```

New text:

```
                reason="path-not-found",
```

### `u28-skills-independent.S14_into_ignored`

--into is ignored and the default target is always used, so a caller's chosen destination is silently overridden

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S14_into_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 10 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_clean_directory_gets_every_shipped_skill_with_a_stamp`
  - `tests/test_skills_install.py::test_a_file_a_previous_install_wrote_and_this_build_withdrew_disappears`
  - `tests/test_skills_install.py::test_a_file_the_product_never_wrote_survives_a_refresh`
  - `tests/test_skills_install.py::test_a_refusal_leaves_no_half_written_target`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_a_target_that_cannot_be_created_refuses_with_a_typed_cause`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_an_up_to_date_install_writes_nothing_at_all`
  - `tests/test_skills_install.py::test_every_shipped_skill_is_installed_and_the_set_is_walked_not_listed`
  - `tests/test_skills_install.py::test_the_copies_are_copies_and_not_symlinks`

Old text:

```
    into = Path(ctx.args.into).expanduser() if ctx.args.into else default_target()
```

New text:

```
    into = default_target()
```

### `u28-skills-independent.S15_drift_never_warns`

every check reports ok, so a refreshed copy no longer tells the person their agent was reading an older build

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S15_drift_never_warns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`

Old text:

```
                "status": "ok" if was in {"installed", "current"} else "info",
```

New text:

```
                "status": "ok",
```

### `u28-skills-independent.S16_counts_miscounted`

every skill is counted as installed, so the summary claims a first install on every re-run

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S16_counts_miscounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 5 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_file_the_product_never_wrote_survives_a_refresh`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_an_up_to_date_install_writes_nothing_at_all`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`

Old text:

```
        counts[was] += 1
```

New text:

```
        counts["installed"] += 1
```

### `u28-skills-independent.S18_detail_reworded`

the refreshed detail sentence is reworded, dropping the phrase the drift test reads

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S18_detail_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`

Old text:

```
        f"the copy at {where} was written by a different build and has been "
        f"replaced; anything reading it was following older instructions"
```

New text:

```
        f"the copy at {where} came from another release of this tool and was "
        f"overwritten; whatever read it was following older instructions"
```

### `u28-skills-independent.S19_default_target_literal`

default_target stops composing from home and returns a relative path, which R1 exists to forbid

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S19_default_target_literal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_install.py::test_the_default_target_is_composed_from_home_and_is_not_a_literal`

Old text:

```
    return Path.home().joinpath(*DEFAULT_TARGET)
```

New text:

```
    return Path(*DEFAULT_TARGET)
```

### `u28-skills-independent.S5_stamp_quote_strip`

installed_version stops stripping the TOML quotes, so every stamped copy reads as a different version

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S5_stamp_quote_strip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 7 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_clean_directory_gets_every_shipped_skill_with_a_stamp`
  - `tests/test_skills_install.py::test_a_file_the_product_never_wrote_survives_a_refresh`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_an_up_to_date_install_writes_nothing_at_all`
  - `tests/test_skills_install.py::test_install_one_reports_which_of_the_three_things_happened`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`

Old text:

```
            return value.strip().strip('"')
```

New text:

```
            return value.strip()
```

### `u28-skills-independent.S9_previous_always_none`

install_one never reads the existing stamp, so a copy from this same build reports as refreshed

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S9_previous_always_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 5 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_file_the_product_never_wrote_survives_a_refresh`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_up_to_date_install_writes_nothing_at_all`
  - `tests/test_skills_install.py::test_install_one_reports_which_of_the_three_things_happened`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`

Old text:

```
    previous = installed_version(destination) if destination.exists() else None
```

New text:

```
    previous = None
```

### `u323.I1_unread_identity_refuses`

_not_the_recorded_volume: an identity the platform cannot read (observed None) refuses as foreign instead of being left to the census

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u323.json`, row `I1_unread_identity_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if recorded is None or observed is None:
            return ""
```

New text:

```
        if recorded is None:
            return ""
```

### `u323.I3_raising_read_escapes`

_not_the_recorded_volume: an identity read that raises escapes the plan instead of being left to the census

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u323.json`, row `I3_raising_read_escapes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    except Exception:  # noqa: BLE001 - an unread identity is left to the census
        return ""
```

New text:

```
    except Exception:  # noqa: BLE001 - an unread identity is left to the census
        raise
```

### `u323.I5_provider_dropped_by_the_plan`

plan_backup: the caller's identity provider is not handed to the files portion, so the platform's own is read

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u323.json`, row `I5_provider_dropped_by_the_plan`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`
- Collected: 37 against a baseline of 37
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_a_root_on_another_volume_refuses_before_the_walk`
  - `tests/test_backup_unproven_root.py::test_the_identity_holds_whatever_the_flag_says`
  - `tests/test_backup_unproven_root.py::test_the_recorded_volume_at_the_root_backs_up`

Old text:

```
                emptied=emptied,
                identity_provider=identity_provider,
                mount_enumerator=mount_enumerator,
            )
        )
    if backup_facts.Portion.DATABASE in wanted:
```

New text:

```
                emptied=emptied,
                identity_provider=None,
                mount_enumerator=mount_enumerator,
            )
        )
    if backup_facts.Portion.DATABASE in wanted:
```

### `u323.I6_provider_dropped_at_the_gate`

_not_the_recorded_volume: the volume gate is asked with no provider, so the platform's own identity read answers

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u323.json`, row `I6_provider_dropped_at_the_gate`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`
- Collected: 37 against a baseline of 37
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_a_root_on_another_volume_refuses_before_the_walk`
  - `tests/test_backup_unproven_root.py::test_the_identity_holds_whatever_the_flag_says`
  - `tests/test_backup_unproven_root.py::test_the_recorded_volume_at_the_root_backs_up`

Old text:

```
        session.assert_volume_identity(
            cfg, identity_provider=identity_provider, mount_enumerator=mount_enumerator
        )
```

New text:

```
        session.assert_volume_identity(
            cfg, identity_provider=None, mount_enumerator=mount_enumerator
        )
```

### `r290-author.R2_backup_rebuild_drops_the_type`

Rebuild the backup rehearsal refusal as a plain CratekitError again, so a rehearsal the worker parked says failed

- File: `src/cratekit/backup/cli.py`
- Source: `r290-author.json`, row `R2_backup_rebuild_drops_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_backup_cli.py`
- Collected: 225 against a baseline of 225
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
- Collected: 225 against a baseline of 225
- Kills: 12 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
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

### `r338-c.C4_bare_metal_asks_about_the_share`

recover_under_bare_metal_session: let the plan ask the remote about a share the skipped database half will never pull

- File: `src/cratekit/session/restore_cli.py`
- Source: `r338-c.json`, row `C4_bare_metal_asks_about_the_share`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_database_that_was_never_on_the_lost_volume_is_not_recovered_onto_the_new_one`

Old text:

```
                pull_share=False,
```

New text:

```
                pull_share=True,
```

### `r338-c.C5_report_loses_the_word`

restore_under_one_session: stop carrying the plan's share word onto the report, so the totals say null whatever happened to the grids

- File: `src/cratekit/session/restore_cli.py`
- Source: `r338-c.json`, row `C5_report_loses_the_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_live_restore_in_the_outside_layout_withholds_the_share_and_closes_clean`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[-pulled1-absent]`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[PIONEER/\n-pulled0-pulled]`

Old text:

```
                "share": str(pulled.share),

```

New text:

```
(empty)
```

### `r592-b.B6_restore_mirror_carries_the_database`

_plan_restore_inside_the_gates: exclude volume clutter only from the restore mirror, so a mirror still holding the database lands it where the database half writes

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r592-b.json`, row `B6_restore_mirror_carries_the_database`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_backup_cli.py`, `tests/test_restore.py`
- Collected: 356 against a baseline of 356
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_mirror_still_carrying_the_database_does_not_land_it`

Old text:

```
                    rclone, "copy", str(cfg.backup.dest), str(target),
                    *_exclude_args(_mirror_excludes(cfg)),
```

New text:

```
                    rclone, "copy", str(cfg.backup.dest), str(target),
                    *_exclude_args(VOLUME_EXCLUDES),
```

### `u27-restore-cli-author.S1_plan_takes_its_own_lock`

Let the off-machine PLAN acquire the library lock itself instead of taking the open guard

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `S1_plan_takes_its_own_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 23 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_failed_transfer_refuses_and_never_reports_a_restore_that_did_not_happen`
  - `tests/test_restore_cli.py::test_a_live_restore_in_the_outside_layout_withholds_the_share_and_closes_clean`
  - `tests/test_restore_cli.py::test_a_mirror_pull_with_no_session_named_is_reported_as_work_that_happened`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_rehearsal_neutralizes_the_mirror_transfers_too`
  - `tests/test_restore_cli.py::test_a_rehearsal_whose_preview_fails_refuses_rather_than_reading_as_a_pass`
  - `tests/test_restore_cli.py::test_a_restore_from_a_database_only_snapshot_names_the_absent_sidecar`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[-pulled1-absent]`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[PIONEER/\n-pulled0-pulled]`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_a_transfer_that_succeeds_is_still_reported`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - ... and 8 more, see the JSON sidecar

Old text:

```
                    include_mirror=include_mirror,
                    gates=held.guard,
```

New text:

```
                    include_mirror=include_mirror,
```

