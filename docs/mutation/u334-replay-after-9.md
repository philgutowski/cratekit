# Mutation table: u334-replay-after-9

Measured by `scripts/mutate.py` on 2026-11-24 06:57 UTC, branch `HEAD` at `90c0cc08`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23214 collected. pytest invocations for this batch: 199.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:57 UTC for commit `90c0cc0829da`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 43, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 114 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 23214 against 23214. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u150.Z1_frozen_retire` | `src/cratekit/organize/mirror_frozen.py` | user | 2 file(s) | 69 | 2 | killed |
| `u150.Z2_frozen_flag_checked` | `src/cratekit/organize/mirror_frozen.py` | maintainer | 2 file(s) | 69 | 1 | killed |
| `u222-zeros.M18_label_no_folder` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222-zeros.M5_agreed_none_lost` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M10_shown_flag_check` | `src/cratekit/organize/mirror_frozen.py` | maintainer | 6 file(s) | 255 | 1 | killed |
| `u222.M13_moved_equal_named` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 5 | killed |
| `u222.M14_moved_new_step_silent` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M15_moved_gone_step_silent` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M16_lines_inverted` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 4 | killed |
| `u222.M17_refused_named_by_every_line` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M2_overlay_never_replaces` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 4 | killed |
| `u222.M3_overlay_any_remote_id` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M6_load_drops_agreed` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 6 | killed |
| `u222.M8_agreed_list_check` | `src/cratekit/organize/mirror_frozen.py` | maintainer | 6 file(s) | 255 | 1 | killed |
| `u222.M9_text_check` | `src/cratekit/organize/mirror_frozen.py` | maintainer | 6 file(s) | 255 | 1 | killed |
| `u236.M21_frozen_not_overlaid` | `src/cratekit/organize/mirror_frozen.py` | user | 8 file(s) | 225 | 2 | killed |
| `u236.M22_frozen_not_written` | `src/cratekit/organize/mirror_frozen.py` | user | 8 file(s) | 225 | 1 | killed |
| `u236.M23_frozen_reads_malformed` | `src/cratekit/organize/mirror_frozen.py` | user | 8 file(s) | 225 | 1 | killed |
| `u112.O1_year_before_label` | `src/cratekit/organize/own.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.R1_no_ack_planned` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 6 | killed |
| `u112.R2_applied_entries_outstanding` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.R3_bridge_tree_planned` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.R4_job_without_gate_run` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.R5_actor_invented` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.R7_every_batch_suggested` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.R8_inbox_mine_unlisted` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 2 | killed |
| `u137.R1_adopt_gate` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 3 | killed |
| `u137.R2_rotation_for_yours` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 2 | killed |
| `u137.R3_refused_rotation_shown` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u137.R4_rotation_shown_unselected` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 1 | killed |
| `u137.R5_record_labels_gate` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 4 | killed |
| `u144-c.C5_export_module` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-c.C6_native_only` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-c.C7_folder_warning` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 38 | 1 | killed |
| `u185.R1_organize_not_yours` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 2 | killed |
| `u185.R2_organize_fact` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 97 | 2 | killed |
| `u143-a.R1_missing_tracks` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u143-a.R2_short_read` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u143-a.R3_no_count` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u143-a.R6_one_named_folder` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u143-b.L1_nested_stays` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u143-e.P1_still_at_root` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u143-e.P2_tracks_unchanged` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u143-e.P3_kept_problems` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u242.M24_root_reads_the_title_alone` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u112.S1_digest_drops_step_plans` | `src/cratekit/organize/steps.py` | user | 1 file(s) | 97 | 24 | killed |
| `u137.S1_identity_names_only` | `src/cratekit/organize/steps.py` | user | 1 file(s) | 97 | 1 | killed |
| `u137.S2_only_fact` | `src/cratekit/organize/steps.py` | user | 1 file(s) | 97 | 2 | killed |
| `u137.S3_wants_everything` | `src/cratekit/organize/steps.py` | user | 1 file(s) | 97 | 13 | killed |
| `u137.S4_selection_ignores_only` | `src/cratekit/organize/steps.py` | user | 1 file(s) | 97 | 21 | killed |
| `u309.U24_planned_step_apply_bound` | `src/cratekit/organize/steps.py` | user | 3 file(s) | 176 | 33 | killed |
| `r154-c.C1_digest_the_word` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `r154-c.C2_expected_volume_outside_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `r154-c.C3_hand_down_the_flag` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r154-c.C4_pull_flags_dropped` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 4 | killed |
| `r154-c.C5_stated_volume_stops_at_the_verb` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r338-c.C4_bare_metal_asks_about_the_share` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 23214 | 0 (promoted) | zero |
| `r338-c.C5_report_loses_the_word` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 23214 | 0 (promoted) | zero |
| `r367.G10_the_report_drops_the_absent_field` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `r368-round-2.G14_the_destination_check_is_equality_only` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `r368-round-2.G6_ancestors_not_walked` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `r368-round-2.G7_composite` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r368-round-2.G7_target_not_resolved` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r368-round-2.R1_the_live_root_refusal_is_reworded` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r368.A1_the_detail_check_is_one_value` | `src/cratekit/session/restore_cli.py` | maintainer | 1 file(s) | 94 | 1 | killed |
| `r368.G10_the_default_capture_survives_a_target` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r368.G12_the_target_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r368.G13_the_rehearsal_flag_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r368.G1_no_live_database_destination_check` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r368.G2_no_containment_check` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 3 | killed |
| `r368.G3_containment_one_direction_only` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r368.G4_containment_is_equality_only` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `r368.G5_paths_compared_as_strings` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `r368.G8_target_without_the_off_machine_pull_is_allowed` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r368.G9_target_beside_a_capture_rollback_is_allowed` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `r592-b.B1_step_on_every_failure` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `r592-b.B2_step_on_the_wrong_half` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `r592-b.B4_step_names_the_wrong_directory` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `r592-b.B5_step_names_no_file` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r592-b.B7_sample_halves_split` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `r592-c.C1_step_on_a_rehearsal_remeasured` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u211.R1_restore_says_what_the_mirror_left` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u27-restore-cli-author.G3_abort_restores_anyway` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u27-restore-cli-author.L1_an_unusable_capture_is_filtered_out_of_the_listing` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u27-restore-cli-author.N1_the_default_takes_the_newest_unusable_capture` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u27-restore-cli-author.P1_the_report_recomputes_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u27-restore-cli-author.P2_a_mirror_pull_is_reported_as_nothing` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u27-restore-cli-author.P3_convergence_is_reported_for_a_run_that_spent_no_capture` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u27-restore-cli-author.R1_a_backup_refusal_becomes_an_internal_error` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 10 | killed |
| `u27-restore-cli-author.S1_plan_takes_its_own_lock` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 253 | 9 | killed |
| `u27-restore-cli-author.S6_the_named_decision_is_withdrawn` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 9 | killed |
| `u27-restore-cli-author.S8_a_rehearsal_performs_the_capture_restore` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u27-restore-cli-independent.I_A10_an_off_machine_refusal_is_swallowed` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 4 | killed |
| `u27-restore-cli-independent.I_A3_platform_seams_never_reach_the_session` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 2 | killed |
| `u27-restore-cli-independent.I_A8_discard_set_never_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 1 | killed |
| `u27-restore-cli-independent.I_B2_the_named_session_never_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 3 | killed |
| `u27-restore-cli-independent.I_B3_the_discard_flag_is_dropped_at_the_call` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 1 | killed |
| `u27-restore-cli-independent.I_B7_the_rehearsal_flag_is_dropped_at_the_call` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 1 | killed |
| `u27-restore-cli-independent.I_C1_discard_stops_being_repeatable` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 1 | killed |
| `u27-restore-cli-independent.I_C4_the_session_identifier_becomes_required` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 30 | killed |
| `u27-restore-cli-independent.I_C6_the_listing_verb_runs_the_restore` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 3 | killed |
| `u27-restore-cli-independent.I_E4_the_reason_a_capture_cannot_be_spent_is_blanked` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 2 | killed |
| `u27-restore-cli-independent.I_F3_an_unknown_identifier_becomes_a_defect_report` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 1 | killed |
| `u27-restore-cli-independent.I_F4_the_refusal_stops_naming_the_identifier` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 1 | killed |
| `u27-restore-cli-independent.X5_the_refusal_reason_is_flattened` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1273 | 9 | killed |
| `u27-restore-cli-round-2.G1_gate_found_by_position` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 1114 | 1 | killed |
| `u27-restore-cli-round-2.O2_the_discard_set_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u27-restore-cli-round-2.R2_the_reserved_remediation_is_replaced_by_the_class_default` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u27-restore-cli-round-2.S3_analysis_watch_watches_nothing` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 242 | 1 | killed |
| `u27-restore-cli-round-2.S7_a_rehearsal_performs_the_mirror_pull` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u311.B1_verb_refusal_origin` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 336 | 14 | killed |
| `u96-a.A12_which_half_failed` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u96-a.A13_completed_halves_recorded` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u96-a.A14_target_is_required` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u96-a.A15_report_names_where_the_database_is` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u96-a.A16_no_absent_companion_for_a_half_that_did_not_run` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u96-a.A1_acceptance_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u96-a.A2_flag_reaches_the_function` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u96-a.A4_run_inside_the_held_session` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u96-a.A5_the_mirror_is_pulled` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u96-a.A6_a_half_at_a_time` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u96-a.A7_rekordbox_asked_again` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u96-a.A8_database_elsewhere_is_skipped` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u96-a.A9_a_rehearsal_stays_a_rehearsal` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u28-skills-independent.S10_stamp_skill_name` | `src/cratekit/skills/cli.py` | maintainer | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u28-skills-independent.S13_expanduser` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u28-skills-independent.S17_outcome_always_ok` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u28-skills-independent.S20_packaged_root_via_file` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u147-c.M19_sweep_handoff` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `u304.S12_pair_cli_offers_file_identity` | `src/cratekit/sync/pair_cli.py` | maintainer | 2 file(s) | 71 | 2 | killed |
| `u304.S13_pair_cli_offers_scope_account` | `src/cratekit/sync/pair_cli.py` | maintainer | 1 file(s) | 34 | 1 | killed |
| `u147-c.M20_pair_scope` | `src/cratekit/sync/pair_model.py` | user | 1 file(s) | 34 | 1 | killed |
| `r1376.F5_first_sync_marked_only` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 318 | killed |
| `u220.A3_keep_head` | `src/cratekit/sync/pair_stopped.py` | user | 6 file(s) | 283 | 26 | killed |
| `u220.A4_first_first` | `src/cratekit/sync/pair_stopped.py` | user | 6 file(s) | 283 | 14 | killed |
| `u147-c.M18_sweep_exclusion` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 34 | 1 | killed |
| `u242.M2_is_taken_drops_the_id` | `src/cratekit/sync/playlists.py` | user | 4 file(s) | 286 | 14 | killed |
| `u242.M3_is_taken_drops_the_prefix` | `src/cratekit/sync/playlists.py` | user | 5 file(s) | 383 | 21 | killed |
| `u304.S14_playlists_still_answers_account_playlist` | `src/cratekit/sync/playlists.py` | maintainer | 1 file(s) | 32 | 1 | killed |
| `u109-b.B1_labels_not_guided` | `src/cratekit/sync/sources.py` | user | 3 file(s) | 229 | 14 | killed |
| `u109-b.B2_command_spelling` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 198 | 10 | killed |
| `u192.T4_tag_queue_only_ignored` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 221 | 7 | killed |
| `r796-a.L1_no_data_is_a_miss` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 6 | killed |
| `r796-a.L2_quota_is_blocked` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 5 | killed |
| `r796-a.L3_unknown_error_is_not_a_miss` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 2 | killed |
| `r796-a.L4_refusal_check_on_a_200` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 1 | killed |
| `r796-a.L5_answer_is_about_the_isrc_asked` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 3 | killed |
| `r796-a.L6_album_id_is_a_positive_integer` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 6 | killed |
| `r796-a.L7_a_refusal_is_remembered` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 4 | killed |
| `r796-a.L8_only_a_refusal_is_remembered` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 4 | killed |
| `r796-b.O3_a_usable_answer_is_never_replaced` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 2 | killed |
| `r796-b.O5_a_declined_beatport_match_is_asked_about` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 5 | killed |
| `r796-b.O6_unread_joins_the_unread_names` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 7 | killed |
| `r796-c.V6_one_lookup_per_process` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 3 | killed |
| `r796-c.V7_the_request_names_this_tool` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 1 | killed |
| `r796-d.L9_first_isrc_of_several_again` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 9 | killed |
| `r796-d.O7_a_decline_keeps_the_shops_word_again` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 3 | killed |
| `r1724.N13_retag_raw_stem` | `src/cratekit/tagging/retag.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1724.N14_retag_tag_read` | `src/cratekit/tagging/retag.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1103.H2_refusal_slug` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 331 | 4 | killed |
| `u40-author-full.C3_resume_without_run` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 70 | 3 | killed |
| `u40-author-full.C4_resume_always_runs` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 70 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R26_retag_queues_no_items` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 122 | 20 | killed |
| `u282.D2_shop_decline_gives_way` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 3 | killed |
| `r1724.N11_tag_one_raw_stem` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1679 | 5 | killed |
| `r1724.N12_tag_one_tag_read` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r796-b.O9_no_isrc_is_not_no_hit` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 380 | 3 | killed |
| `u85-a.A5_no_url_guard` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 141 | 1 | killed |
| `r1724.N10_by_name_unsplit_stem` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 2 | killed |
| `r1724.N1_tail_any_case` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1724.N2_no_trailing_space_read` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1724.N3_space_before_tail_kept` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1724.N4_tail_alone_guard` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 9 | killed |
| `r1724.N5_tail_alone_empty` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 9 | killed |
| `r1724.N6_tail_never_dropped` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 81 | killed |
| `r1724.N7_tail_word` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 82 | killed |
| `r1724.N8_by_name_raw_stem` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 6 | killed |
| `r1724.N9_by_name_headless_stem` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1949.E1_missing_never` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 25 | killed |
| `r1949.E2_inactive_counted` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 1 | killed |
| `r1949.E3_doubled_ignored` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 1 | killed |
| `r1949.E5_addressable_dropped` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 1 | killed |
| `r1949.E7_record_union_dropped` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 2 | killed |
| `r1949.E8_favorites_gap_unread` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 3 | killed |
| `r1949.N12_undeclared_pair_raises` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 110 | killed |
| `r1949.N15_vocal_half_dropped` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 2 | killed |
| `r312.E12_check_names_no_file` | `src/cratekit/write/convergence_check.py` | user | 2 file(s) | 309 | 6 | killed |
| `u302.W8_display_pair_keyed_on_the_folder_twice` | `src/cratekit/write/convergence_check.py` | user | 3 file(s) | 240 | 30 | killed |
| `r414.M10_skip_reason_reworded` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 1 | killed |
| `r414.M11_byte_table_off_by_one` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 3 | killed |
| `r414.M12_detail_key_renamed` | `src/cratekit/write/metadata.py` | maintainer | 3 file(s) | 116 | 5 | killed |
| `r414.M13_remedy_swapped` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 5 | killed |
| `r414.M1_planner_writes_the_byte` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 3 | killed |
| `r414.M2_fold_returns_the_byte` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 4 | killed |
| `r414.M3_unknown_value_not_refused` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 5 | killed |
| `r414.M4_star_passthrough_dropped` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 2 | killed |
| `r414.M5_zero_passthrough_dropped` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 1 | killed |
| `r414.M6_mixed_scale_not_refused` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 1 | killed |
| `r414.M7_mixed_scale_needs_two_stars` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 1 | killed |
| `r414.M8_curve_checked_lazily` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 5 | killed |
| `r414.M9_zero_band_planned` | `src/cratekit/write/metadata.py` | user | 3 file(s) | 116 | 1 | killed |
| `u40-author-full.F2_genre_unknown_silent` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 4 | killed |
| `u59.M1_permissive_default` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 3 | killed |
| `u59.M2_refusal_removed` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 4 | killed |
| `u59.M3_none_admitted` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 1 | killed |
| `u59.M4_tombstone_resolves` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 10 | killed |
| `u59.M5_first_row_wins` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 6 | killed |
| `u59.M6_reason_reworded` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 4 | killed |
| `r239-b.S7_metadata_key_off` | `src/cratekit/write/metadata_cli.py` | user | 7 file(s) | 724 | 1 | killed |
| `r342.E1_cut_inclusive` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V13_detail_key` | `src/cratekit/write/metadata_cli.py` | maintainer | 1 file(s) | 26 | 10 | killed |
| `r342.V1_default_on_corrupt` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 12 | killed |
| `r342.V2_no_finite_check` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `r342.V3_isnan_for_isfinite` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V4_no_bool_check` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V5_tuple_drops_overflow` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V6_tuple_drops_keyerror` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V7_tuple_drops_typeerror` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 3 | killed |
| `r342.V8_tuple_drops_valueerror` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 6 | killed |
| `r342.V9_tuple_drops_oserror` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r372-a.A1_majority_boundary` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A2_majority_coefficient` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A3_pathless_rows_count_as_unmapped` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 17 | killed |
| `r372-a.A4_verb_never_refuses` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 2 | killed |
| `r372-a.A5_apply_proceeds` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A6_decode_error_escapes` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-a.A7_remedy_run_doctor` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 3 | killed |
| `r372-a.A8_refused_plan_reports_ok` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 494 | 2 | killed |
| `r375-b.M2_a_noop_claims_a_commit` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r375-b.M3_witnessed_commit_not_recorded` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r375-b.M4_summary_keyed_on_the_display_name` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u25.G10_ignore_cut` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u25.G11_gender_without_vox` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u25.G12_apply_by_default` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u25.G13_skip_apply_gate` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 8 | killed |
| `u25.G24_content_column` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 6 | killed |
| `u89.L1_absent_is_default` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 223 | 126 | killed |
| `u89.L2_tagging_default` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 223 | 12 | killed |
| `u90-c.C6_wrapper_reads_nothing` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 203 | 8 | killed |
| `r172-a.A1_nothing_collides` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `r172-a.A2_one_round_only` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r172-a.A3_shared_target_ignored` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 4 | killed |
| `r172-a.A4_occupied_target_ignored` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `r172-a.A5_chain_held_too` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r172-a.A7_targets_compared_exactly` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r172-a.A9_collides_reported_as_a_rename` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 5 | killed |
| `r172-b.B11_collision_step_always` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r172-b.B12_the_first_file_is_not_named` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r172-b.B13_detail_carries_nothing` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 10 | killed |
| `r172-b.B14_diagnostic_surface` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 6 | killed |
| `r172-b.B16_referenced_recheck_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r172-b.B17_claim_dropped` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r172-b.B1_ok_whatever_happened` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 15 | killed |
| `r172-b.B2_missing_file_unreported` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r172-b.B3_new_row_unreported` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r172-b.B5_os_error_unreported` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r172-b.B6_tag_write_answer_ignored` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 2 | killed |
| `r172-b.B8_tag_failure_named_where_it_was` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r172-b.B9_renamed_count_is_the_promise` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r239-b.S8_naming_key_off` | `src/cratekit/write/naming_cli.py` | user | 7 file(s) | 724 | 1 | killed |

## Zero rows and what they owe

- `r338-c.C4_bare_metal_asks_about_the_share` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r338-c.C5_report_loses_the_word` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
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
- `u28-skills-independent.S10_stamp_skill_name` (maintainer facing): maintainer facing, composite not required
- `u28-skills-independent.S13_expanduser` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u28-skills-independent.S17_outcome_always_ok` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u28-skills-independent.S20_packaged_root_via_file` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u150.Z1_frozen_retire`

mirror_frozen: rebuild every frozen folder as not retiring, so the apply after a gate removes nothing the gate named

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u150.json`, row `Z1_frozen_retire`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_frozen_folder_whose_retire_is_not_a_boolean_is_not_read[retire-yes]`
  - `tests/test_organize_mirror_inbox.py::test_the_frozen_plan_carries_inbox_its_retirement_and_its_titles`

Old text:

```
                retire=_flag(folder["retire"]),
```

New text:

```
                retire=False,
```

### `u150.Z2_frozen_flag_checked`

mirror_frozen._flag: accept any value as a retire flag, so a damaged record retires on a string

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u150.json`, row `Z2_frozen_flag_checked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_frozen_folder_whose_retire_is_not_a_boolean_is_not_read[retire-yes]`

Old text:

```
    if not isinstance(value, bool):
```

New text:

```
    if False:
```

### `u222-zeros.M18_label_no_folder`

_label: read no folder line, so a folder that moved is never named

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222-zeros.json`, row `M18_label_no_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_label_step_that_moved_is_named_by_its_folder_line`

Old text:

```
    for key in ("playlist", "folder"):
```

New text:

```
    for key in ("playlist",):
```

### `u222-zeros.M5_agreed_none_lost`

_agreed_json: freeze a never agreed snapshot as an empty one

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222-zeros.json`, row `M5_agreed_none_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_never_agreed_snapshot_is_frozen_and_read_back_as_never_agreed`

Old text:

```
            title: [one.remote_id, None if one.agreed is None else sorted(one.agreed)]
```

New text:

```
            title: [one.remote_id, sorted(one.agreed or ())]
```

### `u222.M10_shown_flag_check`

load: accept a shown flag that is not true or false

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M10_shown_flag_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`

Old text:

```
        if not isinstance(shown, bool):
```

New text:

```
        if False:
```

### `u222.M13_moved_equal_named`

moved: name every step, moved or not

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M13_moved_equal_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_write_outside_any_mirrored_playlist_between_the_acts_is_not_stale`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_account_change_between_the_acts_is_stale_and_names_its_folder_and_playlist`
  - `tests/test_organize_mirror_frozen_u222.py::test_with_nothing_between_the_acts_the_apply_rebuilds_the_frozen_plan`

Old text:

```
        if digest_of(step.identity()) == then.digest:
            continue

```

New text:

```
(empty)
```

### `u222.M14_moved_new_step_silent`

moved: say nothing of a step the gate did not show

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M14_moved_new_step_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`

Old text:

```
            said.append(f"{step.title}, which the gate did not show")
            continue
```

New text:

```
            continue
```

### `u222.M15_moved_gone_step_silent`

moved: say nothing of a step the gate showed and this run did not plan

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M15_moved_gone_step_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`

Old text:

```
            said.append(f"{then.title}, which the gate showed and this run did not plan")
```

New text:

```
            pass
```

### `u222.M16_lines_inverted`

moved: name the lines that did NOT move

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M16_lines_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_label_step_that_moved_is_named_by_its_folder_line`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_account_change_between_the_acts_is_stale_and_names_its_folder_and_playlist`

Old text:

```
                if lines.get(label) != then.lines.get(label)
```

New text:

```
                if lines.get(label) == then.lines.get(label)
```

### `u222.M17_refused_named_by_every_line`

moved: name a refused step by every line the gate showed (review round one)

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M17_refused_named_by_every_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`

Old text:

```
            if lines and then.lines
            else []
```

New text:

```
            if lines or then.lines
            else []
```

### `u222.M2_overlay_never_replaces`

overlay: keep the live snapshot of every playlist, the frozen one never taken

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M2_overlay_never_replaces`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_genre_edit_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_playlist_made_again_between_the_acts_reads_its_snapshot_now`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_join_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_leave_the_library_took_between_the_acts_applies_the_approved_plan`

Old text:

```
                one = replace(one, agreed=held[1])
```

New text:

```
                one = one
```

### `u222.M3_overlay_any_remote_id`

overlay: take the frozen snapshot for a playlist made again under another remote id

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M3_overlay_any_remote_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_playlist_made_again_between_the_acts_reads_its_snapshot_now`

Old text:

```
            if held is not None and held[0] == one.remote_id:
```

New text:

```
            if held is not None:
```

### `u222.M6_load_drops_agreed`

load: read no frozen snapshot, so the overlay has nothing to take

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M6_load_drops_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_genre_edit_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_never_agreed_snapshot_is_frozen_and_read_back_as_never_agreed`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_join_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_leave_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`
  - `tests/test_organize_mirror_frozen_u222.py::test_the_frozen_snapshot_is_the_one_the_gates_plan_read_not_the_one_it_recorded`

Old text:

```
        agreed = _agreed_of(data["agreed"])
```

New text:

```
        agreed = {}
```

### `u222.M8_agreed_list_check`

_agreed_of: accept a snapshot that is not a list of text

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M8_agreed_list_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`

Old text:

```
            if agreed is not None and (
```

New text:

```
            if False and (
```

### `u222.M9_text_check`

_text: accept anything as text

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M9_text_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`

Old text:

```
    if not isinstance(value, str):
        raise ValueError(f"{what} is {value!r}, not text")
```

New text:

```
    if False:
        raise ValueError(f"{what} is {value!r}, not text")
```

### `u236.M21_frozen_not_overlaid`

overlay: read the ledger's placements now beside the gate's snapshot

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u236.json`, row `M21_frozen_not_overlaid`
- Moved: the overlay of the gate's placements is still in mirror_frozen.overlay, the replace call now written on one line instead of two; same snapshot read dropped for the ledger's own
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_frozen_folder_with_no_placements_reads_none_and_one_unread_reads_the_ledgers`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`

Old text:

```
placed=frozen.placed.get(name, folder.placed))
```

New text:

```
placed=folder.placed)
```

### `u236.M22_frozen_not_written`

freeze: freeze no placements

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u236.json`, row `M22_frozen_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`

Old text:

```
            name: {title: dict(sorted(tracks.items())) for title, tracks in sorted(folder.placed.items())}
```

New text:

```
            name: {}
```

### `u236.M23_frozen_reads_malformed`

load: accept placements that are not tracks to times

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u236.json`, row `M23_frozen_reads_malformed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`

Old text:

```
            if not isinstance(tracks, dict) or not all(
                isinstance(track, str) and isinstance(at, str) for track, at in tracks.items()
            ):
```

New text:

```
            if False:
```

### `u112.O1_year_before_label`

A year in an account playlist's name wins over the followed label it starts with

- File: `src/cratekit/organize/own.py`
- Source: `u112.json`, row `O1_year_before_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_home_is_a_label_then_a_year_and_otherwise_none[kompakt  2021 picks-the Kompakt label folder]`

Old text:

```
    label = label_of(name, labels)
    if label is not None:
        return f"the {label} label folder"
    year = year_of(name)
    if year is not None:
        return f"the {year} year folder"
```

New text:

```
    year = year_of(name)
    if year is not None:
        return f"the {year} year folder"
    label = label_of(name, labels)
    if label is not None:
        return f"the {label} label folder"
```

### `u112.R1_no_ack_planned`

With no backup acknowledgment the database area is planned and asked anyway

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R1_no_ack_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize.py::test_a_playlist_marked_twice_is_filed_by_its_latest_mark`
  - `tests/test_organize.py::test_a_year_folder_already_on_the_account_is_adopted_with_no_set_to_make_it`
  - `tests/test_organize.py::test_an_answer_ahead_of_a_gate_the_continue_may_not_reach_promises_no_stop_there`
  - `tests/test_organize.py::test_only_files_digest_is_not_the_full_areas_and_an_answer_over_one_is_stale_for_the_other`
  - `tests/test_organize.py::test_the_plan_is_empty_and_still_asks_when_the_root_is_clean`
  - `tests/test_organize.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
        if not report:
            area.cause = unacknowledged.cause
            return area
```

New text:

```
        if False:
            area.cause = unacknowledged.cause
            return area
```

### `u112.R2_applied_entries_outstanding`

Adoption plans every placeable entry, the ones a finished apply already filed included

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R2_applied_entries_outstanding`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`

Old text:

```
        pending = apply_engine.outstanding(plan, apply_engine.read(cfg))
```

New text:

```
        pending = plan.applicable()
```

### `u112.R3_bridge_tree_planned`

Adoption over a routing tree still on the bridge is planned rather than refused

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R3_bridge_tree_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_an_area_with_nothing_to_do_still_asks`

Old text:

```
    if not registry.is_database_native(declared.tree.id):
```

New text:

```
    if False:
```

### `u112.R4_job_without_gate_run`

The adoption job is queued with no gate run, so its resume can never be answered

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R4_job_without_gate_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_adoption_job_carries_a_run_its_own_resume_can_answer`

Old text:

```
                    jobs.GATE_RUN_KEY: gate_run,

```

New text:

```
(empty)
```

### `u112.R5_actor_invented`

The adoption job's approving actor is the process rather than the person who answered

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R5_actor_invented`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_adoption_job_carries_a_run_its_own_resume_can_answer`

Old text:

```
                    apply_cli.ACTOR_KEY: decision.actor if decision is not None else "",
```

New text:

```
                    apply_cli.ACTOR_KEY: "cli",
```

### `u112.R7_every_batch_suggested`

Every batch is suggested a rename, a readably named one included

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R7_every_batch_suggested`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_what_the_author_made_is_listed_with_a_home_and_never_a_write`

Old text:

```
        if batch.recognised_by == rotate.BY_SUFFIX:
```

New text:

```
        if True:
```

### `u112.R8_inbox_mine_unlisted`

A playlist of the author's that the rotation leaves alone under INBOX is not listed

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R8_inbox_mine_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_what_the_author_made_is_listed_with_a_home_and_never_a_write`

Old text:

```
    for node in plan.left:
```

New text:

```
    for node in ():
```

### `u137.R1_adopt_gate`

Plan the adoption whatever the selection

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R1_adopt_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
    if area.wants(ADOPT):
```

New text:

```
    if True:
```

### `u137.R2_rotation_for_yours`

Skip the rotation plan when yours is selected without rotate

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R2_rotation_for_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
    if area.wants(ROTATE) or area.wants(YOURS):
```

New text:

```
    if area.wants(ROTATE):
```

### `u137.R3_refused_rotation_shown`

Hide a rotation that refused when it was planned only for yours

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R3_refused_rotation_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
        if area.wants(ROTATE) or rotation.cause is not None:
```

New text:

```
        if area.wants(ROTATE):
```

### `u137.R4_rotation_shown_unselected`

Show a planned rotation that was planned only for yours

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R4_rotation_shown_unselected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`

Old text:

```
        if area.wants(ROTATE) or rotation.cause is not None:
```

New text:

```
        if True:
```

### `u137.R5_record_labels_gate`

Plan the record labels listing whatever the selection

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R5_record_labels_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_only_a_database_kind_asks_the_database_alone`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
    if area.wants(RECORD_LABELS):
```

New text:

```
    if True:
```

### `u144-c.C5_export_module`

Area: plan the step with the export module off

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u144-c.json`, row `C5_export_module`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_profile_without_the_export_module_lists_the_step`

Old text:

```
    if available is not None and EXPORT_MODULE not in available:
```

New text:

```
    if False:
```

### `u144-c.C6_native_only`

Area: drop the refusal of an intake tree still on the xml bridge

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u144-c.json`, row `C6_native_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_an_intake_tree_on_the_bridge_refuses_the_step`

Old text:

```
        set_playlist.assert_native(ingest.intake_medium(cfg), landing=False)
```

New text:

```
        pass
```

### `u144-c.C7_folder_warning`

Area: warn only for an unread set, not for an unread sets folder

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u144-c.json`, row `C7_folder_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_sets_folder_that_cannot_be_listed_is_named_and_the_rest_still_plan`

Old text:

```
        if row.action in (inspiration.UNREAD, inspiration.FOLDER_UNREAD)
```

New text:

```
        if row.action == inspiration.UNREAD
```

### `u185.R1_organize_not_yours`

organize: list the DEADCA7 folder among the author's own with a home

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u185.json`, row `R1_organize_not_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_deadca7s_folder_is_named_once_as_foreign_and_a_full_apply_leaves_it_as_it_was`

Old text:

```
        if name in declared_roots or str(row.ID) in foreign:
```

New text:

```
        if name in declared_roots:
```

### `u185.R2_organize_fact`

organize: name the folder nowhere, so the report is silent about it

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u185.json`, row `R2_organize_fact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_deadca7s_folder_is_named_once_as_foreign_and_a_full_apply_leaves_it_as_it_was`

Old text:

```
    if foreign:
        area.facts[FOREIGN_FACT]
```

New text:

```
    if foreign and False:
        area.facts[FOREIGN_FACT]
```

### `u143-a.R1_missing_tracks`

Debris: read no track as missing, so a copy holding a track the label folder lacks is planned for removal

- File: `src/cratekit/organize/root.py`
- Source: `u143-a.json`, row `R1_missing_tracks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_debris_copy_with_a_track_the_label_folder_lacks_is_left_naming_it`

Old text:

```
        missing = [one for one in dict.fromkeys(tracks) if one not in held]
```

New text:

```
        missing = []
```

### `u143-a.R2_short_read`

Debris: drop the read short of the declared count check

- File: `src/cratekit/organize/root.py`
- Source: `u143-a.json`, row `R2_short_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_debris_copy_whose_tracks_could_not_all_be_read_is_left`

Old text:

```
        if len(tracks) != declared:
```

New text:

```
        if False:
```

### `u143-a.R3_no_count`

Debris: drop the no listed count check that comes before any read

- File: `src/cratekit/organize/root.py`
- Source: `u143-a.json`, row `R3_no_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_debris_copy_with_no_listed_count_is_left_before_any_read`

Old text:

```
    if not isinstance(declared, int) or isinstance(declared, bool):
```

New text:

```
    if False:
```

### `u143-a.R6_one_named_folder`

Label folder: take the first of several root folders of the label's name

- File: `src/cratekit/organize/root.py`
- Source: `u143-a.json`, row `R6_one_named_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_debris_with_no_label_folder_or_two_of_them_is_left_with_why`

Old text:

```
        if len(named) == 1:
            return named[0], ""
```

New text:

```
        if named:
            return named[0], ""
```

### `u143-b.L1_nested_stays`

Legacy: plan a folder's removal when it holds a folder but no playlist

- File: `src/cratekit/organize/root.py`
- Source: `u143-b.json`, row `L1_nested_stays`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_legacy_folder_holding_a_folder_stays_and_its_folder_is_not_moved`

Old text:

```
    if not held and not nested:
```

New text:

```
    if not held:
```

### `u143-e.P1_still_at_root`

Apply: remove a playlist moved into a folder since the gate was answered

- File: `src/cratekit/organize/root.py`
- Source: `u143-e.json`, row `P1_still_at_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_playlist_moved_into_a_folder_since_the_plan_is_kept`

Old text:

```
    if row.target in in_folders:
```

New text:

```
    if False:
```

### `u143-e.P2_tracks_unchanged`

Apply: remove a debris playlist given a track since the gate was answered

- File: `src/cratekit/organize/root.py`
- Source: `u143-e.json`, row `P2_tracks_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_debris_copy_given_a_track_since_the_plan_is_kept_and_the_rest_removed`

Old text:

```
        if not now <= set(row.tracks):
```

New text:

```
        if False:
```

### `u143-e.P3_kept_problems`

Apply: stop on every refusal, so a refusal before sending stops the rest

- File: `src/cratekit/organize/root.py`
- Source: `u143-e.json`, row `P3_kept_problems`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_removal_the_account_refuses_before_sending_is_kept_and_the_apply_goes_on`

Old text:

```
                if exc.cause.detail.get("problem") not in KEPT_PROBLEMS:
```

New text:

```
                if True:
```

### `u242.M24_root_reads_the_title_alone`

root step: count a label folder's downloaded playlists by the title alone

- File: `src/cratekit/organize/root.py`
- Source: `u242.json`, row `M24_root_reads_the_title_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_year_playlist_held_as_taken_with_no_prefix_proves_its_tracks_downloaded`

Old text:

```
                if is_taken(playlist_id, name, self._taken)
```

New text:

```
                if name.startswith("DOWNLOADED ")
```

### `u112.S1_digest_drops_step_plans`

The area digest covers each step's key and state and not its own plan's digest

- File: `src/cratekit/organize/steps.py`
- Source: `u112.json`, row `S1_digest_drops_step_plans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 24 (killed)
- Killed:
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[False]`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[True]`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_plan_that_moves_after_the_answer_is_stale_rather_than_applied`
  - `tests/test_organize.py::test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine`
  - `tests/test_organize.py::test_a_provider_refusal_mid_pass_stops_and_names_what_moved[False]`
  - `tests/test_organize.py::test_a_provider_refusal_mid_pass_stops_and_names_what_moved[True]`
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_a_run_resumed_with_no_account_answer_plans_the_mirror_afresh`
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_a_stale_rekordbox_refusal_shows_the_moved_plan_and_the_decide_after_it_files_it`
  - ... and 9 more, see the JSON sidecar

Old text:

```
        said = self.digest if self.cause is None else f"refused:{self.cause.reason}"
```

New text:

```
        said = None if self.cause is None else f"refused:{self.cause.reason}"
```

### `u137.S1_identity_names_only`

Leave the selection out of the area's digest document

- File: `src/cratekit/organize/steps.py`
- Source: `u137.json`, row `S1_identity_names_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_selection_alone_moves_the_digest_when_it_names_every_step`

Old text:

```
        if self.only is not None:
            identity["only"] = list(self.only)
```

New text:

```
        pass
```

### `u137.S2_only_fact`

Stop naming the selection in the area's facts

- File: `src/cratekit/organize/steps.py`
- Source: `u137.json`, row `S2_only_fact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_only_file_plans_the_filing_alone_and_the_database_is_not_asked`

Old text:

```
            self.facts[ONLY_FACT] = ", ".join(self.only)
```

New text:

```
            pass
```

### `u137.S3_wants_everything`

Let every kind through whatever the selection

- File: `src/cratekit/organize/steps.py`
- Source: `u137.json`, row `S3_wants_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 13 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_an_unread_label_registry_refuses_the_filing_rather_than_plan_it_over_no_label`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`
  - `tests/test_organize.py::test_only_a_database_kind_asks_the_database_alone`
  - `tests/test_organize.py::test_only_file_plans_the_filing_alone_and_the_database_is_not_asked`
  - `tests/test_organize.py::test_only_mirror_plans_and_writes_the_mirror_alone_and_a_rerun_plans_nothing`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
        return self.only is None or kind in self.only
```

New text:

```
        return True
```

### `u137.S4_selection_ignores_only`

Take every kind of the area as selected when --only names any

- File: `src/cratekit/organize/steps.py`
- Source: `u137.json`, row `S4_selection_ignores_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 21 (killed)
- Killed:
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_a_run_resumed_with_no_account_answer_plans_the_mirror_afresh`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_an_unread_label_registry_refuses_the_filing_rather_than_plan_it_over_no_label`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`
  - `tests/test_organize.py::test_only_a_database_kind_asks_the_database_alone`
  - `tests/test_organize.py::test_only_file_moves_a_marked_playlist_as_the_full_verb_does_and_then_plans_nothing`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return tuple(kind for kind in kinds if kind in only)
```

New text:

```
    return tuple(kinds)
```

### `u309.U24_planned_step_apply_bound`

A planned step that writes is given no apply

- File: `src/cratekit/organize/steps.py`
- Source: `u309.json`, row `U24_planned_step_apply_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_organize_root.py`, `tests/test_label_dated.py`
- Collected: 176 against a baseline of 176
- Kills: 33 (killed)
- Killed:
  - `tests/test_label_dated.py::test_organize_plans_the_dated_playlist_after_the_label_folder_and_applies_in_order`
  - `tests/test_organize.py::test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year`
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_playlist_marked_twice_is_filed_by_its_latest_mark`
  - `tests/test_organize.py::test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine`
  - `tests/test_organize.py::test_a_provider_refusal_mid_pass_stops_and_names_what_moved[False]`
  - `tests/test_organize.py::test_a_provider_refusal_mid_pass_stops_and_names_what_moved[True]`
  - `tests/test_organize.py::test_a_run_resumed_with_no_account_answer_plans_the_mirror_afresh`
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`
  - `tests/test_organize.py::test_a_set_archived_by_its_inspiration_proof_stays_archived_once_that_playlist_goes`
  - `tests/test_organize.py::test_a_set_in_its_folder_with_its_built_title_is_taken_and_not_moved`
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    if writes and apply is not None:
        step.apply = partial(apply, step)
```

New text:

```
    if False:
        step.apply = partial(apply, step)
```

### `r154-c.C1_digest_the_word`

Digest a constant where the resolved stamp goes, which is R-153 itself: a backup landing between the two acts leaves the digest where it was

- File: `src/cratekit/session/restore_cli.py`
- Source: `r154-c.json`, row `C1_digest_the_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_backup_landing_between_the_two_acts_moves_the_digest`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled_and_reported`

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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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

### `r338-c.C4_bare_metal_asks_about_the_share`

recover_under_bare_metal_session: let the plan ask the remote about a share the skipped database half will never pull

- File: `src/cratekit/session/restore_cli.py`
- Source: `r338-c.json`, row `C4_bare_metal_asks_about_the_share`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                "share": str(pulled.share),

```

New text:

```
(empty)
```

### `r367.G10_the_report_drops_the_absent_field`

the off machine half ran and the person is not told the sidecar was missing

- File: `src/cratekit/session/restore_cli.py`
- Source: `r367.json`, row `G10_the_report_drops_the_absent_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 23214 against a baseline of 23214
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
- Collected: 23214 against a baseline of 23214
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
- Collected: 23214 against a baseline of 23214
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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

### `r368.G12_the_target_leaves_the_digest`

a decision recorded against a rehearsal is honoured against the live restore

- File: `src/cratekit/session/restore_cli.py`
- Source: `r368.json`, row `G12_the_target_leaves_the_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_mirror_half_or_the_rehearsal_flag_is_added`

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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_that_is_holds_or_sits_in_the_library_is_refused[above-the directory the library root sits in]`
  - `tests/test_restore_cli.py::test_a_target_that_is_holds_or_sits_in_the_library_is_refused[inside-a directory underneath the library root]`
  - `tests/test_restore_cli.py::test_a_target_that_is_holds_or_sits_in_the_library_is_refused[root-the library root itself]`

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
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_that_is_holds_or_sits_in_the_library_is_refused[above-the directory the library root sits in]`

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
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_that_is_holds_or_sits_in_the_library_is_refused[above-the directory the library root sits in]`
  - `tests/test_restore_cli.py::test_a_target_that_is_holds_or_sits_in_the_library_is_refused[inside-a directory underneath the library root]`

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
- Collected: 23214 against a baseline of 23214
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
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_without_the_pull_or_beside_a_capture_rollback_is_refused[no-pull]`

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
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_without_the_pull_or_beside_a_capture_rollback_is_refused[beside-a-discard]`
  - `tests/test_restore_cli.py::test_a_target_without_the_pull_or_beside_a_capture_rollback_is_refused[beside-a-named-session]`

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
- Collected: 23214 against a baseline of 23214
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
- Collected: 23214 against a baseline of 23214
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
- Collected: 23214 against a baseline of 23214
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 23214 against a baseline of 23214
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 23214 against a baseline of 23214
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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

### `u27-restore-cli-author.S1_plan_takes_its_own_lock`

Let the off-machine PLAN acquire the library lock itself instead of taking the open guard

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `S1_plan_takes_its_own_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 253 against a baseline of 253
- Kills: 9 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled_and_reported`

Old text:

```
                    include_mirror=include_mirror,
                    gates=held.guard,
```

New text:

```
                    include_mirror=include_mirror,
```

### `u27-restore-cli-author.S6_the_named_decision_is_withdrawn`

Tell the off-machine restore no decision exists, which R33 makes it refuse on

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `S6_the_named_decision_is_withdrawn`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 94 against a baseline of 94
- Kills: 9 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled_and_reported`

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
- Collected: 94 against a baseline of 94
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

### `u27-restore-cli-independent.I_A10_an_off_machine_refusal_is_swallowed`

Continue past a refused off-machine half instead of translating it, so the capture half runs over a mirror that never landed

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_A10_an_off_machine_refusal_is_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1273 against a baseline of 1273
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
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
- Collected: 1273 against a baseline of 1273
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_carries_the_reserved_remediation_and_not_the_class_default`
  - `tests/test_restore_cli.py::test_the_session_watches_the_whole_library_and_not_a_folder_inside_it`

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
- Collected: 1273 against a baseline of 1273
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
- Collected: 1273 against a baseline of 1273
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
- Collected: 1273 against a baseline of 1273
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
- Collected: 1273 against a baseline of 1273
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
- Collected: 1273 against a baseline of 1273
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
- Collected: 1273 against a baseline of 1273
- Kills: 30 (killed)
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
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_a_target_that_is_holds_or_sits_in_the_library_is_refused[above-the directory the library root sits in]`
  - ... and 15 more, see the JSON sidecar

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
- Collected: 1273 against a baseline of 1273
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_capture_this_product_pruned_is_refused_by_name_and_not_as_a_defect`
  - `tests/test_restore_cli.py::test_a_session_whose_capture_is_gone_is_listed_and_says_why`
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
- Collected: 1273 against a baseline of 1273
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

### `u27-restore-cli-independent.I_F3_an_unknown_identifier_becomes_a_defect_report`

Refuse a typo as an internal error, so a person who mistyped a session is told to report a defect

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_F3_an_unknown_identifier_becomes_a_defect_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1273 against a baseline of 1273
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_session_identifier_nothing_recorded_is_refused_by_name`

Old text:

```
            reason="restore-record-unusable",
```

New text:

```
            reason="internal-error",
```

### `u27-restore-cli-independent.I_F4_the_refusal_stops_naming_the_identifier`

Reword the refusal so it never repeats what was typed, which is what makes a typo diagnosable

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-independent.json`, row `I_F4_the_refusal_stops_naming_the_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`, `tests/test_cli_contract.py`
- Collected: 1273 against a baseline of 1273
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
- Collected: 1273 against a baseline of 1273
- Kills: 9 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_recovery_is_refused_underneath_a_running_rekordbox`
  - `tests/test_restore_cli.py::test_a_recovery_with_no_rclone_installed_refuses_by_name_and_writes_nothing`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
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

### `u27-restore-cli-round-2.G1_gate_found_by_position`

Take gates[0] rather than the gate digested against the plan

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-round-2.json`, row `G1_gate_found_by_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_cli_contract.py`
- Collected: 1114 against a baseline of 1114
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_confirmation_gate_is_found_by_digest_source_and_not_by_position`

Old text:

```
    for spec in entry.gates:
        if spec.digest_source == "plan":
            return spec
```

New text:

```
    for spec in entry.gates:
        return spec
```

### `u27-restore-cli-round-2.O2_the_discard_set_leaves_the_digest`

Digest without the sessions being discarded, so an approval covers a wider destruction

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-round-2.json`, row `O2_the_discard_set_leaves_the_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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

### `u27-restore-cli-round-2.S3_analysis_watch_watches_nothing`

Arm the analysis watch on no roots, so it reports a clean session either way

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-round-2.json`, row `S3_analysis_watch_watches_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_session_watches_the_whole_library_and_not_a_folder_inside_it`

Old text:

```
        analysis_roots=watched,
```

New text:

```
        analysis_roots=(),
```

### `u27-restore-cli-round-2.S7_a_rehearsal_performs_the_mirror_pull`

Ignore dry_run on the off-machine half, so a preview transfers for real

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-round-2.json`, row `S7_a_rehearsal_performs_the_mirror_pull`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 23214 against a baseline of 23214
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

### `u311.B1_verb_refusal_origin`

The restore verb's own refusals carry no step beside their condition

- File: `src/cratekit/session/restore_cli.py`
- Source: `u311.json`, row `B1_verb_refusal_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_sync_removed.py`
- Collected: 336 against a baseline of 336
- Kills: 14 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_capture_this_product_pruned_is_refused_by_name_and_not_as_a_defect`
  - `tests/test_restore_cli.py::test_a_flag_about_the_pull_is_refused_when_no_pull_was_asked_for[flags0]`
  - `tests/test_restore_cli.py::test_a_flag_about_the_pull_is_refused_when_no_pull_was_asked_for[flags1]`
  - `tests/test_restore_cli.py::test_a_flag_about_the_pull_is_refused_when_no_pull_was_asked_for[flags2]`
  - `tests/test_restore_cli.py::test_a_flag_about_the_pull_is_refused_when_no_pull_was_asked_for[flags3]`
  - `tests/test_restore_cli.py::test_a_relative_target_is_compared_as_the_place_it_names`
  - `tests/test_restore_cli.py::test_a_target_that_is_holds_or_sits_in_the_library_is_refused[above-the directory the library root sits in]`
  - `tests/test_restore_cli.py::test_a_target_that_is_holds_or_sits_in_the_library_is_refused[inside-a directory underneath the library root]`
  - `tests/test_restore_cli.py::test_a_target_that_is_holds_or_sits_in_the_library_is_refused[root-the library root itself]`
  - `tests/test_restore_cli.py::test_a_target_whose_database_lands_on_the_live_one_is_refused`
  - `tests/test_restore_cli.py::test_a_target_without_the_pull_or_beside_a_capture_rollback_is_refused[beside-a-discard]`
  - `tests/test_restore_cli.py::test_a_target_without_the_pull_or_beside_a_capture_rollback_is_refused[beside-a-named-session]`
  - `tests/test_restore_cli.py::test_a_target_without_the_pull_or_beside_a_capture_rollback_is_refused[no-pull]`
  - `tests/test_restore_cli.py::test_an_unusable_capture_is_refused_before_the_mirror_moves_a_byte`

Old text:

```
            remediation=Remediation(steps=(step,)),
```

New text:

```
            remediation=Remediation(steps=()),
```

### `u96-a.A12_which_half_failed`

_half_failed: swap the two failure sentences, so a failed mirror is reported as a failed database half

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A12_which_half_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 23214 against a baseline of 23214
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 23214 against a baseline of 23214
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
- Collected: 23214 against a baseline of 23214
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 94 against a baseline of 94
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
- Collected: 23214 against a baseline of 23214
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
- Collected: 23214 against a baseline of 23214
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
- Collected: 23214 against a baseline of 23214
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

### `u28-skills-independent.S10_stamp_skill_name`

the stamp stops recording which skill it belongs to, so a copied stamp cannot be told from its own

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S10_stamp_skill_name`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
\nskill = "{name}"
```

New text:

```
(empty)
```

### `u28-skills-independent.S13_expanduser`

--into stops expanding a tilde, so a target given as ~/skills is created as a literal directory named ~

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S13_expanduser`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    into = Path(ctx.args.into).expanduser() if ctx.args.into else default_target()
```

New text:

```
    into = Path(ctx.args.into) if ctx.args.into else default_target()
```

### `u28-skills-independent.S17_outcome_always_ok`

the envelope reports OK even when nothing was installed, so an empty package reads as a successful install

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S17_outcome_always_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        outcome=Outcome.OK if checks else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u28-skills-independent.S20_packaged_root_via_file`

packaged_root resolves by path arithmetic from __file__ rather than through importlib.resources

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S20_packaged_root_via_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_portability.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return resources.files("cratekit.skills") / "assets"
```

New text:

```
    return Path(__file__).resolve().parent / "assets"
```

### `u147-c.M19_sweep_handoff`

sync.cli: the sync source hands the sweep no mirrored playlist

- File: `src/cratekit/sync/cli.py`
- Source: `u147-c.json`, row `M19_sweep_handoff`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_the_sync_pass_hands_the_sweep_every_mirrored_playlist`

Old text:

```
            mirrored=mirrored,
```

New text:

```
(empty)
```

### `u304.S12_pair_cli_offers_file_identity`

pair_cli: file_identity, which organize reads there, is no longer offered

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u304.json`, row `S12_pair_cli_offers_file_identity`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_code_read_off_the_file_asks_the_one_track_to_agree_and_a_database_code_does_not`
  - `tests/test_organize_mirror_frozen.py::test_a_file_that_gains_a_code_is_asked_again_and_an_unchanged_one_is_not`

Old text:

```
from cratekit.sync.pair_read import (
    file_identity,

```

New text:

```
from cratekit.sync.pair_read import (

```

### `u304.S13_pair_cli_offers_scope_account`

pair_cli: _scope_account, which the organize suite reads there, is no longer offered

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u304.json`, row `S13_pair_cli_offers_scope_account`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_sync_pair_refuses_to_pair_a_mirrored_playlist`

Old text:

```
from cratekit.sync.pair_model import _scope_account as _scope_account  # noqa: PLC0414

```

New text:

```
(empty)
```

### `u147-c.M20_pair_scope`

sync.pair_cli._scope_account: a mirrored playlist may be paired

- File: `src/cratekit/sync/pair_model.py`
- Source: `u147-c.json`, row `M20_pair_scope`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_sync_pair_refuses_to_pair_a_mirrored_playlist`

Old text:

```
    if account_id in mirrored:
```

New text:

```
    if False:
```

### `r1376.F5_first_sync_marked_only`

plan_pair: a pair with no record at all, a hand pairing before its mark, is not read as a first sync

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F5_first_sync_marked_only`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 318 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_rekordbox_running_refusal_still_ends_the_run_as_failed`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - `tests/test_sync_pair.py::test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale`
  - `tests/test_sync_pair.py::test_a_rekordbox_row_with_no_isrc_column_is_matched_on_its_files_isrc`
  - `tests/test_sync_pair.py::test_a_row_with_no_isrc_anywhere_is_named_and_the_provider_is_not_asked`
  - `tests/test_sync_pair.py::test_a_second_rekordbox_playlist_for_a_paired_account_playlist_is_refused`
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - ... and 303 more, see the JSON sidecar

Old text:

```
    first_sync = held is None or held.first
```

New text:

```
    first_sync = held is not None and held.first
```

### `u220.A3_keep_head`

_to_the_front: match the asked order's head rather than its tail, the old to the end rule

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u220.json`, row `A3_keep_head`
- Moved: U298 replaced tidal_account._to_the_front's body with sync.pair_stopped.front_moves, its copy until then, which the adapter now returns; the same tail match
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 26 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_move_that_lands_anywhere_else_is_not_read_back_and_the_settle_reading_shows_it`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_recorder_that_cannot_record_has_no_further_move_sent`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_every_move_is_to_the_front_where_both_ways_of_counting_agree`
  - `tests/test_outbound_order.py::test_nothing_to_move_tells_the_caller_nothing`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before1-order1]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before2-order2]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before3-order3]`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - ... and 11 more, see the JSON sidecar

Old text:

```
one == wanted[len(wanted) - 1 - keep]
```

New text:

```
one == wanted[keep]
```

### `u220.A4_first_first`

_to_the_front: move the tracks first first rather than last first, so the moved ones land reversed

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u220.json`, row `A4_first_first`
- Moved: U298 replaced tidal_account._to_the_front's body with sync.pair_stopped.front_moves, its copy until then, which the adapter now returns; the same reversal of the moves
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 14 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_holding_what_the_adds_left_in_another_order_is_not_stale`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before2-order2]`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`
  - `tests/test_outbound_order.py::test_the_tracks_before_the_kept_tail_are_moved_last_first`
  - `tests/test_sync_pair_account.py::test_a_move_that_landed_elsewhere_is_left_to_the_settle_reading_with_every_track_kept`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`

Old text:

```
    return list(reversed(wanted[: len(wanted) - keep]))
```

New text:

```
    return wanted[: len(wanted) - keep]
```

### `u147-c.M18_sweep_exclusion`

sync.playlists.exclusion: a mirrored playlist is swept as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `u147-c.json`, row `M18_sweep_exclusion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_the_intake_sweep_leaves_a_mirrored_playlist_alone`

Old text:

```
    if playlist.playlist_id in mirrored:
        return Excluded.MIRROR

```

New text:

```
(empty)
```

### `u242.M2_is_taken_drops_the_id`

is_taken: read the title alone, the ledger ignored by every reader

- File: `src/cratekit/sync/playlists.py`
- Source: `u242.json`, row `M2_is_taken_drops_the_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_organize_root.py`
- Collected: 286 against a baseline of 286
- Kills: 14 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_year_playlist_held_as_taken_with_no_prefix_proves_its_tracks_downloaded`
  - `tests/test_organize_root.py::test_filing_reads_a_stripped_hand_mark_as_it_read_the_prefixed_one`
  - `tests/test_sync_all.py::test_a_mark_that_landed_is_not_owed_a_second_time`
  - `tests/test_sync_mark.py::test_a_partial_failure_names_what_was_marked`
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_mark_since_u242_writes_no_title_and_the_playlist_is_never_offered`
  - `tests/test_u242_taken.py::test_a_stripped_playlist_named_like_a_followed_label_is_still_filed_by_its_mark`
  - `tests/test_u242_taken.py::test_exclusion_answers_swept_for_a_taken_playlist_with_no_prefix`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_is_taken_holds_a_recorded_id_whatever_its_title_and_a_legacy_prefix`
  - `tests/test_u242_taken.py::test_the_inspiration_set_rule_reads_a_stripped_set_as_the_prefixed_one`
  - `tests/test_u242_taken.py::test_twins_reads_a_stripped_custom_playlist_as_downloaded`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    return str(playlist_id or "") in taken or is_swept_name(name)
```

New text:

```
    return is_swept_name(name)
```

### `u242.M3_is_taken_drops_the_prefix`

is_taken: read the ledger alone, so a legacy prefixed title the migration has not recorded reads as new

- File: `src/cratekit/sync/playlists.py`
- Source: `u242.json`, row `M3_is_taken_drops_the_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_organize_root.py`, `tests/test_organize.py`
- Collected: 383 against a baseline of 383
- Kills: 21 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mark_put_back_is_no_mark_and_the_playlist_stays`
  - `tests/test_organize.py::test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine`
  - `tests/test_organize.py::test_only_root_removes_debris_and_empties_on_the_gate_and_files_the_legacy_folder`
  - `tests/test_organize_root.py::test_a_debris_copy_given_a_track_since_the_plan_is_kept_and_the_rest_removed`
  - `tests/test_organize_root.py::test_a_debris_copy_whose_tracks_could_not_all_be_read_is_left`
  - `tests/test_organize_root.py::test_a_debris_copy_with_a_track_the_label_folder_lacks_is_left_naming_it`
  - `tests/test_organize_root.py::test_a_followed_labels_recorded_folder_is_read_whatever_it_is_called_now`
  - `tests/test_organize_root.py::test_a_refusal_part_way_stops_and_names_what_was_removed`
  - `tests/test_organize_root.py::test_a_second_run_on_a_clean_root_plans_nothing`
  - `tests/test_organize_root.py::test_filing_reads_a_stripped_hand_mark_as_it_read_the_prefixed_one`
  - `tests/test_organize_root.py::test_four_identical_debris_copies_with_every_track_filed_plan_four_removals`
  - `tests/test_organize_root.py::test_the_plans_digest_moves_when_a_row_changes`
  - `tests/test_sync_all.py::test_a_playlist_the_source_system_already_prefixed_is_not_prefixed_twice`
  - `tests/test_sync_all.py::test_a_slim_pass_queues_each_new_account_playlist_under_the_shared_run`
  - `tests/test_sync_all.py::test_the_label_batch_debris_is_not_queued_as_intake`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return str(playlist_id or "") in taken or is_swept_name(name)
```

New text:

```
    return str(playlist_id or "") in taken
```

### `u304.S14_playlists_still_answers_account_playlist`

sync.playlists.__getattr__: AccountPlaylist, which organize's suite reads there, is no longer answered (round one's finding)

- File: `src/cratekit/sync/playlists.py`
- Source: `u304.json`, row `S14_playlists_still_answers_account_playlist`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_the_sweep_still_excludes_every_mirrored_inbox_playlist`

Old text:

```
    if name == "AccountPlaylist":
        from cratekit.label.catalogue import AccountPlaylist

        return AccountPlaylist
    raise
```

New text:

```
    raise
```

### `u109-b.B1_labels_not_guided`

Drop guided_by from the labels spec, so labels is an ordinary source with no worker

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B1_labels_not_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 229 against a baseline of 229
- Kills: 14 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_explicit_toggle_puts_back_the_source_its_profile_leaves_out`
  - `tests/test_sync_all.py::test_every_guided_source_names_a_verb_the_registry_declares_and_queues_nothing`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
        guided_by="label.sync",
```

New text:

```
(empty)
```

### `u109-b.B2_command_spelling`

Spell the guided command with the registry's dotted name, crate label.sync

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B2_command_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_label_workers.py`
- Collected: 198 against a baseline of 198
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_an_explicit_toggle_puts_back_the_source_its_profile_leaves_out`
  - `tests/test_sync_all.py::test_every_guided_source_names_a_verb_the_registry_declares_and_queues_nothing`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
        return "crate " + self.guided_by.replace(".", " ")
```

New text:

```
        return "crate " + self.guided_by
```

### `u192.T4_tag_queue_only_ignored`

tag_folder: ignore --queue-only and drive the sweep

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T4_tag_queue_only_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_label_genre.py`, `tests/test_render_payloads.py`
- Collected: 221 against a baseline of 221
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_genre.py::test_an_unreadable_registry_warns_and_refuses_only_a_sweep_that_named_a_label`
  - `tests/test_label_genre.py::test_the_remedy_names_the_label_by_its_identifier`
  - `tests/test_render_payloads.py::test_a_builder_that_raises_leaves_the_queued_verb_a_success`
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`
  - `tests/test_tag_workers.py::test_a_real_track_beside_the_staging_tree_is_still_queued`
  - `tests/test_tag_workers.py::test_queueing_a_folder_names_the_job_and_the_command_that_drives_it`
  - `tests/test_tag_workers.py::test_tag_folder_queue_only_returns_the_sweep_queued_with_nothing_asked`

Old text:

```
        if foreground.queue_only(ctx.args):
```

New text:

```
        if False:
```

### `r796-a.L1_no_data_is_a_miss`

_error: stop reading the catalogue's 'no data' as a miss, so an ISRC it does not know is an error nobody recognises

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L1_no_data_is_a_miss`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 6 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_known_track_whose_album_names_no_genre_is_a_match_with_none[a-track-whose-album-the-catalogue-does-not-list-is-not-a-miss]`
  - `tests/test_published_genre.py::test_a_track_no_catalogue_knows_with_every_source_read_is_still_no_hit`
  - `tests/test_published_genre.py::test_an_isrc_the_catalogue_does_not_know_is_a_miss_and_asks_for_no_album`
  - `tests/test_published_genre.py::test_the_request_names_this_tool_and_not_a_browser`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_four_real_misses_are_no_hit_and_carry_no_unread_warning`

Old text:

```
    if code == _NO_DATA:
```

New text:

```
    if False:
```

### `r796-a.L2_quota_is_blocked`

_error: stop reading the quota error as a refusal, so a rate limit in a 200 body is a parse break

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L2_quota_is_blocked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 5 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_known_track_whose_album_could_not_be_read_is_unread_and_not_a_match[{"error": {"type": "Exception", "message": "Quota limit exceeded", "code": 4}}-blocked]`
  - `tests/test_published_genre.py::test_a_refusal_is_remembered_and_nothing_more_is_asked_in_the_run`
  - `tests/test_published_genre.py::test_a_refusal_on_one_file_reaches_the_next_files_seam`
  - `tests/test_published_genre.py::test_a_track_answer_nobody_can_read_a_genre_off_is_never_a_miss[{"error": {"type": "Exception", "message": "Quota limit exceeded", "code": 4}}-blocked-Quota limit exceeded]`
  - `tests/test_published_genre.py::test_the_quota_error_is_not_retried_at_all`

Old text:

```
    if code == _QUOTA:
```

New text:

```
    if False:
```

### `r796-a.L3_unknown_error_is_not_a_miss`

_error: answer MISS for an error this reader does not know, the guess the module forbids

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L3_unknown_error_is_not_a_miss`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 2 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_track_answer_nobody_can_read_a_genre_off_is_never_a_miss[{"error": "a string"}-parse-break-does not know]`
  - `tests/test_published_genre.py::test_a_track_answer_nobody_can_read_a_genre_off_is_never_a_miss[{"error": {"type": "InvalidQueryException", "message": "bad", "code": 600}}-parse-break-code 600]`

Old text:

```
    return _said(
        Answer.PARSE_BREAK,
        f"the catalogue answered with an error this reader does not know, {described}",
```

New text:

```
    return _said(
        Answer.MISS,
        f"the catalogue answered with an error this reader does not know, {described}",
```

### `r796-a.L4_refusal_check_on_a_200`

_read: run the refusal check only on a page with no text, so a challenge page served with 200 is parsed as JSON

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L4_refusal_check_on_a_200`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 1 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_track_answer_nobody_can_read_a_genre_off_is_never_a_miss[page2-blocked-bot check]`

Old text:

```
    refused = searchers.unread_outcome(SOURCE, page)
```

New text:

```
    refused = None if page.text is not None else searchers.unread_outcome(SOURCE, page)
```

### `r796-a.L5_answer_is_about_the_isrc_asked`

_ask: accept a track answer naming another ISRC, or none, as this track's

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L5_answer_is_about_the_isrc_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 3 (killed)
- Killed:
  - `tests/test_published_genre.py::test_an_answer_about_another_recording_is_not_read_as_this_tracks[track0]`
  - `tests/test_published_genre.py::test_an_answer_about_another_recording_is_not_read_as_this_tracks[track1]`
  - `tests/test_published_genre.py::test_an_answer_about_another_recording_is_not_read_as_this_tracks[track2]`

Old text:

```
    if isrc_token(track.get("isrc")) != isrc:
```

New text:

```
    if False:
```

### `r796-a.L6_album_id_is_a_positive_integer`

_ask: let any album identifier that is not None become a URL

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L6_album_id_is_a_positive_integer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 6 (killed)
- Killed:
  - `tests/test_published_genre.py::test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url[-4]`
  - `tests/test_published_genre.py::test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url[0]`
  - `tests/test_published_genre.py::test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url[1/../../track/9]`
  - `tests/test_published_genre.py::test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url[3.5]`
  - `tests/test_published_genre.py::test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url[302127]`
  - `tests/test_published_genre.py::test_an_album_identifier_that_is_not_a_positive_integer_is_never_a_url[True]`

Old text:

```
    if not isinstance(album_id, int) or isinstance(album_id, bool) or album_id <= 0:
```

New text:

```
    if album_id is None:
```

### `r796-a.L7_a_refusal_is_remembered`

genre_lookup: forget a BLOCKED answer, so the next file asks a catalogue that said stop

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L7_a_refusal_is_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 4 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_block_on_the_album_is_remembered_too`
  - `tests/test_published_genre.py::test_a_refusal_is_remembered_and_nothing_more_is_asked_in_the_run`
  - `tests/test_published_genre.py::test_a_refusal_on_one_file_reaches_the_next_files_seam`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`

Old text:

```
        if said.answer == Answer.BLOCKED.value:
            refusals.append(said)
```

New text:

```
        if False:
            refusals.append(said)
```

### `r796-a.L8_only_a_refusal_is_remembered`

genre_lookup: remember every unread answer, so one outage or parse break ends the catalogue's part in the run

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L8_only_a_refusal_is_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 4 (killed)
- Killed:
  - `tests/test_published_genre.py::test_an_album_that_could_not_be_read_is_asked_for_again`
  - `tests/test_published_genre.py::test_only_a_refusal_is_remembered[<html>not json</html>]`
  - `tests/test_published_genre.py::test_only_a_refusal_is_remembered[page0]`
  - `tests/test_published_genre.py::test_only_a_refusal_is_remembered[{"error": {"type": "Exception", "message": "Service busy", "code": 700}}]`

Old text:

```
        if said.answer == Answer.BLOCKED.value:
            refusals.append(said)
```

New text:

```
        if said.answer in UNREAD:
            refusals.append(said)
```

### `r796-b.O3_a_usable_answer_is_never_replaced`

second_opinion: ask the general catalogue about a hit that already has a genre (R4)

- File: `src/cratekit/tagging/published.py`
- Source: `r796-b.json`, row `O3_a_usable_answer_is_never_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 2 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_hit_beatport_did_not_leave_unsettled_is_not_asked_about[a-file-with-no-isrc-whose-genre-a-shop-settled-is-still-not-asked]`
  - `tests/test_published_genre.py::test_a_usable_answer_is_never_replaced_and_the_record_says_not_asked`

Old text:

```
        if hit.genre or isrc is None:
```

New text:

```
        if isrc is None:
```

### `r796-b.O5_a_declined_beatport_match_is_asked_about`

_BEATPORT_ANSWERED: count only a miss, so a track Beatport calls by a catch-all is never asked about (R1, AE2)

- File: `src/cratekit/tagging/published.py`
- Source: `r796-b.json`, row `O5_a_declined_beatport_match_is_asked_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 5 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_declined_answer_beside_beatports_own_declined_word_keeps_beatports`
  - `tests/test_published_genre.py::test_a_published_genre_over_beatports_declined_word_is_written_and_keeps_beatports_picture`
  - `tests/test_published_genre.py::test_ae2_two_coarse_answers_write_nothing_and_the_record_shows_both`
  - `tests/test_published_genre.py::test_beatports_picture_is_embedded_under_a_published_genre_and_says_whose_it_is`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`

Old text:

```
_BEATPORT_ANSWERED = (Answer.MATCHED.value, Answer.MISS.value)
```

New text:

```
_BEATPORT_ANSWERED = (Answer.MISS.value,)
```

### `r796-b.O6_unread_joins_the_unread_names`

second_opinion: leave the general catalogue out of the hit's unread names when it could not be read

- File: `src/cratekit/tagging/published.py`
- Source: `r796-b.json`, row `O6_unread_joins_the_unread_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 7 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_blocked_general_catalogue_leaves_the_file_untagged_and_askable`
  - `tests/test_published_genre.py::test_an_unread_general_catalogue_joins_the_unread_names[blocked]`
  - `tests/test_published_genre.py::test_an_unread_general_catalogue_joins_the_unread_names[parse-break]`
  - `tests/test_published_genre.py::test_an_unread_general_catalogue_joins_the_unread_names[unreachable]`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`

Old text:

```
            unread = (*hit.unread, SOURCE) if said.answer in UNREAD else hit.unread
```

New text:

```
            unread = hit.unread
```

### `r796-c.V6_one_lookup_per_process`

for_lookup: build a fresh lookup per call, so a refusal on one file is forgotten by the next file's seam

- File: `src/cratekit/tagging/published.py`
- Source: `r796-c.json`, row `V6_one_lookup_per_process`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 3 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_refusal_on_one_file_reaches_the_next_files_seam`
  - `tests/test_published_genre.py::test_the_lookup_binder_hands_back_one_lookup_per_process`
  - `tests/test_published_genre.py::test_the_suite_cannot_reach_the_live_catalogue_through_the_shared_lookup`

Old text:

```
    if not _shared:
        _shared.append(genre_lookup())
    return _shared[0]
```

New text:

```
    return genre_lookup()
```

### `r796-c.V7_the_request_names_this_tool`

genre_lookup: build the default fetch without this module's headers, so the API is asked under the browser identity

- File: `src/cratekit/tagging/published.py`
- Source: `r796-c.json`, row `V7_the_request_names_this_tool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 1 (killed)
- Killed:
  - `tests/test_published_genre.py::test_the_request_names_this_tool_and_not_a_browser`

Old text:

```
    touch = searchers.default_fetch(sleep=naps, headers=HEADERS) if fetch is None else fetch
```

New text:

```
    touch = searchers.default_fetch(sleep=naps) if fetch is None else fetch
```

### `r796-d.L9_first_isrc_of_several_again`

re-measure of r796-a L9 after the second review round rewrote the line: _first_isrc never looks inside a value, so two ISRCs in one field read as no ISRC

- File: `src/cratekit/tagging/published.py`
- Source: `r796-d.json`, row `L9_first_isrc_of_several_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 9 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[CAT-0042,USRC17607839]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[ISRC: USRC17607839]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[USRC17607839 / GBAYE0601498]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[USRC17607839 GBAYE0601498]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[USRC17607839; GBAYE0601498]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[USRC17607839\nGBAYE0601498]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[USRC17607839\x00GBAYE0601498]`
  - `tests/test_published_genre.py::test_a_field_holding_several_values_is_read_as_its_first_isrc[isrc US-RC1-76-07839 (remaster)]`
  - `tests/test_published_genre.py::test_the_two_value_id3_frame_is_the_shape_the_reader_really_hands_back`

Old text:

```
    for found in _ISRC_WITHIN.finditer(str(value or "")):
```

New text:

```
    for found in ():
```

### `r796-d.O7_a_decline_keeps_the_shops_word_again`

re-measure of r796-b O7 after the second review round rewrote the line: a declined answer always takes over the file's source, over Beatport's word and when it published no word at all

- File: `src/cratekit/tagging/published.py`
- Source: `r796-d.json`, row `O7_a_decline_keeps_the_shops_word_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 3 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_declined_answer_beside_beatports_own_declined_word_keeps_beatports`
  - `tests/test_published_genre.py::test_a_match_that_publishes_no_genre_is_a_decline_with_no_word`
  - `tests/test_published_genre.py::test_a_match_with_no_genre_leaves_the_file_as_the_shops_left_it`

Old text:

```
        if picked is None and (hit.source_genre or not word):
```

New text:

```
        if False:
```

### `r1724.N13_retag_raw_stem`

retag_one: ask the raw stem, so tag retag asks Sunshine Hotel_PN

- File: `src/cratekit/tagging/retag.py`
- Source: `r1724.json`, row `N13_retag_raw_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_retag_asks_a_file_with_no_title_tag_its_name_past_the_tail`

Old text:

```
        title = tags.read_tag(candidate.path, "title") or titles.name_title(candidate.path.stem)
```

New text:

```
        title = tags.read_tag(candidate.path, "title") or candidate.path.stem
```

### `r1724.N14_retag_tag_read`

retag_one: read the tail off a title tag too

- File: `src/cratekit/tagging/retag.py`
- Source: `r1724.json`, row `N14_retag_tag_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_retag_asks_a_title_tag_ending_in_the_tail_as_written`

Old text:

```
        title = tags.read_tag(candidate.path, "title") or titles.name_title(candidate.path.stem)
```

New text:

```
        title = titles.name_title(tags.read_tag(candidate.path, "title") or candidate.path.stem)
```

### `r1103.H2_refusal_slug`

handle: the item fails under the general analysis-write-failed slug instead of retag's own

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H2_refusal_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_reserved_causes.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
        raise refuse(
            retag.UNWRITTEN_REASON,
```

New text:

```
        raise refuse(
            "analysis-write-failed",
```

### `u40-author-full.C3_resume_without_run`

Drop --run from the resume argv, so the job driver's child meets the explicit gate with nothing recorded and stalls for ever

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u40-author-full.json`, row `C3_resume_without_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`
- Collected: 70 against a baseline of 70
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_resume_argv_carries_the_folder_the_job_and_the_gate_run`
  - `tests/test_queued_resume_contract.py::test_a_queued_gated_verb_emits_the_run_its_decision_was_recorded_against[tag.retag]`
  - `tests/test_queued_resume_contract.py::test_the_resume_the_job_driver_spawns_can_actually_proceed[tag.retag]`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
```

New text:

```
    resume = []
```

### `u40-author-full.C4_resume_always_runs`

Emit --run even when no gate run is frozen, so a job from an older build hands its child an empty run identifier

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u40-author-full.json`, row `C4_resume_always_runs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_queued_resume_contract.py::test_a_payload_from_an_older_build_still_builds_a_valid_command_line[tag.retag]`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "tag", "retag", folder, "--job", job.job_id]
```

New text:

```
    return ["--run", str(gate_run), "tag", "retag", folder, "--job", job.job_id]
```

### `u56-catalogue-searcher-and-tag-workers.R26_retag_queues_no_items`

The zero item rule broken on the second verb, over work somebody explicitly confirmed

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R26_retag_queues_no_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 20 (killed)
- Killed:
  - `tests/test_queued_resume_contract.py::test_the_resume_the_job_driver_spawns_can_actually_proceed[tag.retag]`
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_rather_than_reported_done`
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[-read_back1-no-genre]`
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[Ambient-read_back0-genre-specific]`
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_parses_the_active_taxonomy_once_however_many_files_it_corrects`
  - `tests/test_tag_workers.py::test_a_retag_that_corrected_nothing_does_not_send_a_person_to_rekordbox`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`
  - `tests/test_tag_workers.py::test_a_retried_retag_drives_only_the_item_that_failed`
  - ... and 5 more, see the JSON sidecar

Old text:

```
            item_ids=tuple(str(row["path"]) for row in plan["items"]),
```

New text:

```
            item_ids=(),
```

### `u282.D2_shop_decline_gives_way`

search: a record shop's decline gives way too, so an explicit Beatport first walk asks Discogs after Beatport's unmapped genre

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `D2_shop_decline_gives_way`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_record_shop_decline_still_ends_an_explicit_walk`
  - `tests/test_published_genre.py::test_ae2_two_coarse_answers_write_nothing_and_the_record_shows_both`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`

Old text:

```
            if resolved.genre is None and source not in _SEARCHES:
```

New text:

```
            if resolved.genre is None:
```

### `r1724.N11_tag_one_raw_stem`

tag_one: hand the searcher the raw stem, so the match reads mix)_pn and the Obiman release is missed

- File: `src/cratekit/tagging/tag.py`
- Source: `r1724.json`, row `N11_tag_one_raw_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_name_tail.py::test_a_file_with_an_artist_tag_and_no_title_tag_is_asked_its_name_past_the_tail`
  - `tests/test_name_tail.py::test_sunshine_hotel_is_asked_by_its_artist_and_title_and_no_source_sees_the_tail`
  - `tests/test_name_tail.py::test_the_obiman_name_is_asked_its_title_and_takes_the_release_a_person_would_type`
  - `tests/test_name_tail.py::test_the_obiman_name_matches_its_release_whatever_discogs_is_asked`

Old text:

```
    title = title_tag or titles.name_title(path.stem)
```

New text:

```
    title = title_tag or path.stem
```

### `r1724.N12_tag_one_tag_read`

tag_one: read the tail off a title tag too, so a tag ending _PN is not asked as written

- File: `src/cratekit/tagging/tag.py`
- Source: `r1724.json`, row `N12_tag_one_tag_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_title_tag_ending_in_the_tail_is_asked_and_matched_as_written`

Old text:

```
    title = title_tag or titles.name_title(path.stem)
```

New text:

```
    title = titles.name_title(title_tag or path.stem)
```

### `r796-b.O9_no_isrc_is_not_no_hit`

tag_one: drop the no-isrc skip reason, so a file the general catalogue could not be asked about is no-hit (AE4)

- File: `src/cratekit/tagging/tag.py`
- Source: `r796-b.json`, row `O9_no_isrc_is_not_no_hit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 3 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_malformed_isrc_tag_is_reported_with_what_it_held`
  - `tests/test_published_genre.py::test_ae4_a_file_with_no_isrc_is_reported_as_that_and_not_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`

Old text:

```
        elif any(said.answer == NO_ISRC for said in hit.answers):
```

New text:

```
        elif False:
```

### `u85-a.A5_no_url_guard`

A hit naming no picture is still fetched, with an empty URL

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A5_no_url_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_picture_from_beatports_row_is_reported_as_beatports`

Old text:

```
    if not hit.art_url:
```

New text:

```
    if False:
```

### `r1724.N10_by_name_unsplit_stem`

by_name: the unsplit question reads the raw stem, so an ambiguous name is asked with its tail

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N10_by_name_unsplit_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 2 (killed)
- Killed:
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[8A - 124 - Make Luv - Room 5 - Album_PN-asked3]`
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[8A - 124_PN-asked5]`

Old text:

```
    unsplit = question(name, "")
```

New text:

```
    unsplit = question(stem, "")
```

### `r1724.N1_tail_any_case`

name_title: read the tail in any letter case, so a name ending _pn loses it too

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N1_tail_any_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_name_with_no_tail_is_read_byte_for_byte[Sunrise Mood_pn]`

Old text:

```
    if not text.endswith(NAME_TAIL):
        return stem
    parts =
```

New text:

```
    if not text.lower().endswith(NAME_TAIL.lower()):
        return stem
    parts =
```

### `r1724.N2_no_trailing_space_read`

name_title: read the stem with its trailing space, so a tail before a space is kept

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N2_no_trailing_space_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood_PN  -Sunrise Mood]`

Old text:

```
    text = stem.rstrip()
    if not text.endswith(NAME_TAIL):
```

New text:

```
    text = stem
    if not text.endswith(NAME_TAIL):
```

### `r1724.N3_space_before_tail_kept`

name_title: keep the space before the tail, so Sunrise Mood _PN is asked with a trailing space

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N3_space_before_tail_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood _PN-Sunrise Mood]`

Old text:

```
    parts[-1] = parts[-1].rstrip()

```

New text:

```
(empty)
```

### `r1724.N4_tail_alone_guard`

name_title: drop the tail alone guard, so 8A - 124 - Artist - _PN reads to a name ending in a dash and loses its ISRC genre

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N4_tail_alone_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 9 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_asked_as_before`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[ _PN-asked1]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - Artist - ?_PN-asked6]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - Artist - Title - _PN-asked5]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - Sean Doron - _PN-asked3]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - _PN-asked4]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[Sean Doron - _PN-asked2]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[_PN-asked0]`
  - `tests/test_name_tail.py::test_retag_asks_a_name_whose_last_part_is_the_tail_alone_as_written`

Old text:

```
    if not identifies(parts[-1]):
        return stem
    return DASH.join(parts)
```

New text:

```
    return DASH.join(parts)
```

### `r1724.N5_tail_alone_empty`

name_title: a tail alone name reads to nothing, round one's code, so it asks nothing and misses its ISRC

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N5_tail_alone_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 9 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_asked_as_before`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[ _PN-asked1]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - Artist - ?_PN-asked6]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - Artist - Title - _PN-asked5]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - Sean Doron - _PN-asked3]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - _PN-asked4]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[Sean Doron - _PN-asked2]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[_PN-asked0]`
  - `tests/test_name_tail.py::test_retag_asks_a_name_whose_last_part_is_the_tail_alone_as_written`

Old text:

```
    if not identifies(parts[-1]):
        return stem
    return DASH.join(parts)
```

New text:

```
    if not identifies(parts[-1]):
        return ""
    return DASH.join(parts)
```

### `r1724.N6_tail_never_dropped`

name_title: return the stem whatever it ends with, main's reading

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N6_tail_never_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 81 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_name_tail.py::test_a_file_with_an_artist_tag_and_no_title_tag_is_asked_its_name_past_the_tail`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[06A - 126 - Sean Doron - Sunshine Hotel_PN-06A - 126 - Sean Doron - Sunshine Hotel]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[8A - 124 - [MP3] Lane 8 - Aba_PN-8A - 124 - [MP3] Lane 8 - Aba]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)_PN-9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Attention_PN-Attention]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Promise to Stay Here_PN-Promise to Stay Here]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood [Nightwave Remix]_PN-Sunrise Mood [Nightwave Remix]]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood _PN-Sunrise Mood]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood_PN  -Sunrise Mood]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Foo) Bar (feat. X) (Extended Mix)-(Foo) Bar]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro) (Extended Mix)-(Intro)]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro)-(Intro)]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro)-Intro (Original Mix)]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro)-Intro]`
  - ... and 66 more, see the JSON sidecar

Old text:

```
        return stem
    return DASH.join(parts)
```

New text:

```
        return stem
    return stem
```

### `r1724.N7_tail_word`

NAME_TAIL: the tail without its underscore, so Sunrise Mood PN loses a word

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N7_tail_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 82 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_name_tail.py::test_a_file_with_an_artist_tag_and_no_title_tag_is_asked_its_name_past_the_tail`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[06A - 126 - Sean Doron - Sunshine Hotel_PN-06A - 126 - Sean Doron - Sunshine Hotel]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[8A - 124 - [MP3] Lane 8 - Aba_PN-8A - 124 - [MP3] Lane 8 - Aba]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)_PN-9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Attention_PN-Attention]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Promise to Stay Here_PN-Promise to Stay Here]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood [Nightwave Remix]_PN-Sunrise Mood [Nightwave Remix]]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood _PN-Sunrise Mood]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood_PN  -Sunrise Mood]`
  - `tests/test_name_tail.py::test_a_name_with_no_tail_is_read_byte_for_byte[Sunrise Mood PN]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Foo) Bar (feat. X) (Extended Mix)-(Foo) Bar]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro) (Extended Mix)-(Intro)]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro)-(Intro)]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro)-Intro (Original Mix)]`
  - ... and 67 more, see the JSON sidecar

Old text:

```
NAME_TAIL = "_PN"
```

New text:

```
NAME_TAIL = "PN"
```

### `r1724.N8_by_name_raw_stem`

by_name: read the raw stem, so Sunshine Hotel_PN splits with its tail

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N8_by_name_raw_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 6 (killed)
- Killed:
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[06A - 126 - Sean Doron - Sunshine Hotel_PN-asked0]`
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[8A - 124 - Make Luv - Room 5 - Album_PN-asked3]`
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[8A - 124 - [MP3] Lane 8 - Aba_PN-asked2]`
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[8A - 124_PN-asked5]`
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)_PN-asked1]`
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[Sunshine Hotel_PN-asked4]`

Old text:

```
    name = name_title(stem)
    rest = _past_head(name)
```

New text:

```
    name = stem
    rest = _past_head(name)
```

### `r1724.N9_by_name_headless_stem`

by_name: a headless name is asked as its raw stem, tail and all

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N9_by_name_headless_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[Sunshine Hotel_PN-asked4]`

Old text:

```
        return Question("", name, Read.AS_WRITTEN)
```

New text:

```
        return Question("", stem, Read.AS_WRITTEN)
```

### `r1949.E1_missing_never`

check: never report a declared track the playlist lacks, so a short tree reads matching

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `E1_missing_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 25 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`
  - `tests/test_rebuild.py::test_a_tree_stripped_of_its_membership_rebuilds_to_match_the_control`
  - `tests/test_rebuild.py::test_the_check_reports_a_difference_in_both_directions`
  - `tests/test_rebuild.py::test_the_check_walks_down_from_the_adopted_root_and_ignores_a_namesake`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[the library moved]`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[two files swapped]`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`
  - `tests/test_resort_scope.py::test_the_gate_shows_every_add_and_only_the_routing_trees`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_refuses_the_resume_before_any_item_runs[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[resort]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
        if content_id not in held:
```

New text:

```
        if False:
```

### `r1949.E2_inactive_counted`

check: count a membership on a soft deleted row as unexpected

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `E2_inactive_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild.py::test_a_membership_pointing_at_a_soft_deleted_row_is_not_a_difference_either`

Old text:

```
        for content_id in sorted((node.content_ids & active) - declared_here):
```

New text:

```
        for content_id in sorted(node.content_ids - declared_here):
```

### `r1949.E3_doubled_ignored`

check: never report a playlist holding a track twice

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `E3_doubled_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild.py::test_a_track_held_twice_in_one_playlist_is_a_difference_the_flag_stays_shut_on`

Old text:

```
        for content_id in sorted(node.doubled & active):
```

New text:

```
        for content_id in sorted(frozenset()):
```

### `r1949.E5_addressable_dropped`

check: drop the refusal of two nodes on one destination, so the check picks one silently

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `E5_addressable_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild.py::test_two_declared_destinations_on_one_display_pair_refuse`

Old text:

```
    assert_addressable(tree_id, destinations, nodes)
    by_key
```

New text:

```
    by_key
```

### `r1949.E7_record_union_dropped`

resolve_destinations: drop the recorded destinations from the set, so one that lost every track falls into foreign

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `E7_record_union_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_check_with_no_source_leaves_the_recorded_favorites_out_and_names_the_gap`
  - `tests/test_rebuild.py::test_a_vocal_playlist_nothing_compared_is_not_named_as_left_behind`

Old text:

```
        wanted |= {(entry.bucket, entry.sub) for entry in record.nodes}
```

New text:

```
        pass
```

### `r1949.E8_favorites_gap_unread`

_uncompared_playlist_subs: answer the playlist classes whether or not the favourites source was read

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `E8_favorites_gap_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`

Old text:

```
    if genre_favorites.FAVORITES_DIMENSION not in tuple(not_compared):
        return set()
```

New text:

```
    if False:
        return set()
```

### `r1949.N12_undeclared_pair_raises`

declared_names: let a former or split place's KeyError escape, so every check refuses

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N12_undeclared_pair_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 110 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_check_with_no_source_leaves_the_recorded_favorites_out_and_names_the_gap`
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`
  - `tests/test_genre_favorites.py::test_the_rebuild_files_a_favourite_into_the_folder_it_moves_it_to`
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`
  - `tests/test_rebuild.py::test_a_declared_file_the_library_has_no_row_for_is_surfaced_and_is_not_a_difference`
  - `tests/test_rebuild.py::test_a_destination_that_lost_every_track_is_still_compared`
  - `tests/test_rebuild.py::test_a_destination_with_no_recorded_node_falls_back_to_the_declared_name`
  - `tests/test_rebuild.py::test_a_genre_sub_is_created_once_beside_the_band_and_a_second_rebuild_plans_nothing`
  - `tests/test_rebuild.py::test_a_governed_write_records_the_fingerprint_at_its_close`
  - `tests/test_rebuild.py::test_a_library_with_no_vocal_calibration_reports_what_it_did_not_compare`
  - `tests/test_rebuild.py::test_a_membership_pointing_at_a_soft_deleted_row_is_not_a_difference_either`
  - `tests/test_rebuild.py::test_a_playlist_nobody_declared_is_reported_and_is_not_a_difference`
  - `tests/test_rebuild.py::test_a_rebuild_after_a_rename_converges_rather_than_doubling_the_tree`
  - `tests/test_rebuild.py::test_a_rebuild_and_its_check_beside_deadca7s_folder_leave_it_and_report_no_drift[ordinary]`
  - `tests/test_rebuild.py::test_a_rebuild_and_its_check_beside_deadca7s_folder_leave_it_and_report_no_drift[zero-date-west-of-utc]`
  - ... and 95 more, see the JSON sidecar

Old text:

```
            except KeyError:
                continue
            found.setdefault
```

New text:

```
            except ValueError:
                continue
            found.setdefault
```

### `r1949.N15_vocal_half_dropped`

_uncompared_subs: drop the vocal half, so with vox reads left behind and differing on an uncalibrated run

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N15_vocal_half_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 2 (killed)
- Killed:
  - `tests/test_rebuild.py::test_a_vocal_playlist_nothing_compared_is_not_named_as_left_behind`
  - `tests/test_second_genre.py::test_a_vocal_playlist_the_run_did_not_compare_is_not_named_through_its_names`

Old text:

```
    if VOCAL_DIMENSION in tuple(not_compared):
        skipped |=
```

New text:

```
    if False:
        skipped |=
```

### `r312.E12_check_names_no_file`

check: an unexpected difference carries no file location, the state before this unit

- File: `src/cratekit/write/convergence_check.py`
- Source: `r312.json`, row `E12_check_names_no_file`
- Moved: Anchored where u302-replay-after-c.json replayed it: the same text, now in src/cratekit/write/convergence_check.py, was in src/cratekit/write/rebuild.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 6 (killed)
- Killed:
  - `tests/test_rebuild.py::test_the_check_reports_a_difference_in_both_directions`
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
            replace(entry, location=located_at.get(entry.content_id or ""))
```

New text:

```
            replace(entry, location=None)
```

### `u302.W8_display_pair_keyed_on_the_folder_twice`

by_display_pair: the key forgets the playlist name

- File: `src/cratekit/write/convergence_check.py`
- Source: `u302.json`, row `W8_display_pair_keyed_on_the_folder_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_deferred_routing.py`, `tests/test_genre_favorites.py`
- Collected: 240 against a baseline of 240
- Kills: 30 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_recovery_run_after_a_rename_converges_once_the_tree_layer_can`
  - `tests/test_deferred_routing.py::test_a_recovery_run_after_a_taxonomy_rename_converges_rather_than_duplicating`
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`
  - `tests/test_genre_favorites.py::test_the_rebuild_files_a_favourite_into_the_folder_it_moves_it_to`
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`
  - `tests/test_rebuild.py::test_a_destination_that_lost_every_track_is_still_compared`
  - `tests/test_rebuild.py::test_a_destination_with_no_recorded_node_falls_back_to_the_declared_name`
  - `tests/test_rebuild.py::test_a_genre_sub_is_created_once_beside_the_band_and_a_second_rebuild_plans_nothing`
  - `tests/test_rebuild.py::test_a_library_with_no_vocal_calibration_reports_what_it_did_not_compare`
  - `tests/test_rebuild.py::test_a_membership_pointing_at_a_soft_deleted_row_is_not_a_difference_either`
  - `tests/test_rebuild.py::test_a_rebuild_after_a_rename_converges_rather_than_doubling_the_tree`
  - `tests/test_rebuild.py::test_a_rebuild_and_its_check_beside_deadca7s_folder_leave_it_and_report_no_drift[ordinary]`
  - `tests/test_rebuild.py::test_a_rebuild_and_its_check_beside_deadca7s_folder_leave_it_and_report_no_drift[zero-date-west-of-utc]`
  - `tests/test_rebuild.py::test_a_rebuild_is_not_refused_by_the_flag_it_exists_to_clear`
  - `tests/test_rebuild.py::test_a_rebuild_never_removes_a_membership_the_declaration_does_not_place`
  - ... and 15 more, see the JSON sidecar

Old text:

```
        out.setdefault((node.folder_display, node.playlist_display), []).append(node)
```

New text:

```
        out.setdefault((node.folder_display, node.folder_display), []).append(node)
```

### `r414.M10_skip_reason_reworded`

Reword the zero band's skip reason to the uncut reason

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M10_skip_reason_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest`

Old text:

```
"level-unrated"
```

New text:

```
"level-uncut"
```

### `r414.M11_byte_table_off_by_one`

Realistic nearby value in the byte table, 204 folds to three stars

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M11_byte_table_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 3 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_curve_already_on_the_star_scale_passes_through`
  - `tests/test_metadata_policy.py::test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest`
  - `tests/test_metadata_policy.py::test_the_shipped_curve_plans_one_to_five_stars_for_the_database`

Old text:

```
204: 4,
```

New text:

```
204: 3,
```

### `r414.M12_detail_key_renamed`

The refusal detail names the offending value under a different key

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M12_detail_key_renamed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 5 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[-1]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[20]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[256]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[50]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[6]`

Old text:

```
            {"rating": value},
```

New text:

```
            {"value": value},
```

### `r414.M13_remedy_swapped`

The refusal carries the doctor token instead of the configuration token

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M13_remedy_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 5 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[-1]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[20]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[256]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[50]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[6]`

Old text:

```
        remedy=Remedy.FIX_CONFIG_VALUES,
        scope=Scope.RUN,
        origin=("write", "metadata"),
        detail=dict(detail),
```

New text:

```
        remedy=Remedy.RUN_DOCTOR,
        scope=Scope.RUN,
        origin=("write", "metadata"),
        detail=dict(detail),
```

### `r414.M1_planner_writes_the_byte`

The planner writes the cut's export value instead of the folded star, which is R-414 itself

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M1_planner_writes_the_byte`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 3 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest`
  - `tests/test_metadata_policy.py::test_a_rating_backfill_fills_an_empty_rating_with_a_star_not_a_byte`
  - `tests/test_metadata_policy.py::test_the_shipped_curve_plans_one_to_five_stars_for_the_database`

Old text:

```
        stars = curve[rating]
```

New text:

```
        stars = rating
```

### `r414.M2_fold_returns_the_byte`

database_stars returns the value it was given instead of the star it folds to

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M2_fold_returns_the_byte`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 4 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest`
  - `tests/test_metadata_policy.py::test_a_rating_backfill_fills_an_empty_rating_with_a_star_not_a_byte`
  - `tests/test_metadata_policy.py::test_the_export_scale_is_what_rating_for_still_answers`
  - `tests/test_metadata_policy.py::test_the_shipped_curve_plans_one_to_five_stars_for_the_database`

Old text:

```
    return stars


def _database_curve(
```

New text:

```
    return value


def _database_curve(
```

### `r414.M3_unknown_value_not_refused`

Drop the refusal for a value on neither scale, so database_stars returns None

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M3_unknown_value_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 5 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[-1]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[20]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[256]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[50]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[6]`

Old text:

```
    if stars is None:
        raise _scale_unknown(
```

New text:

```
    if False:
        raise _scale_unknown(
```

### `r414.M4_star_passthrough_dropped`

A value already on the star scale is no longer passed through, so a star curve refuses

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M4_star_passthrough_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 2 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_curve_already_on_the_star_scale_passes_through`
  - `tests/test_metadata_policy.py::test_a_curve_mixing_the_two_scales_is_refused_at_plan_time`

Old text:

```
    if value == 0 or value in _DATABASE_STARS:
```

New text:

```
    if value == 0:
```

### `r414.M5_zero_passthrough_dropped`

Zero is no longer answered as zero, so a curve with an unrated band refuses the whole plan

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M5_zero_passthrough_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest`

Old text:

```
    if value == 0 or value in _DATABASE_STARS:
```

New text:

```
    if value in _DATABASE_STARS:
```

### `r414.M6_mixed_scale_not_refused`

Drop the mixed scale refusal in _database_curve

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M6_mixed_scale_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_curve_mixing_the_two_scales_is_refused_at_plan_time`

Old text:

```
    if bytes_ and stars:
```

New text:

```
    if False:
```

### `r414.M7_mixed_scale_needs_two_stars`

Nearby value, a mix is refused only when two or more star values sit beside the bytes

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M7_mixed_scale_needs_two_stars`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_curve_mixing_the_two_scales_is_refused_at_plan_time`

Old text:

```
    if bytes_ and stars:
```

New text:

```
    if bytes_ and len(stars) > 1:
```

### `r414.M8_curve_checked_lazily`

The curve is folded only over values it recognises, so a bad cut refuses only the rows landing in it, not the plan

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M8_curve_checked_lazily`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 5 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[-1]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[20]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[256]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[50]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[6]`

Old text:

```
    curve = _database_curve(cuts)
```

New text:

```
    curve = _database_curve(
        [c for c in cuts if c.rating == 0 or c.rating in _DATABASE_STARS or c.rating in _EXPORT_BYTE_STARS]
    )
```

### `r414.M9_zero_band_planned`

Drop the level-unrated skip, so a zero cut plans a zero rating as a change

- File: `src/cratekit/write/metadata.py`
- Source: `r414.json`, row `M9_zero_band_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_whitelist_membership.py`
- Collected: 116 against a baseline of 116
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_cut_that_declares_zero_skips_its_band_and_keeps_the_rest`

Old text:

```
        if stars == 0:
```

New text:

```
        if False:
```

### `u40-author-full.F2_genre_unknown_silent`

First caller sample: drop the genre-unknown skip, so an unresolvable answer disappears from the plan

- File: `src/cratekit/write/metadata.py`
- Source: `u40-author-full.json`, row `F2_genre_unknown_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_genre_the_library_has_never_seen_is_skipped_and_surfaced`
  - `tests/test_genre_retag.py::test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader`
  - `tests/test_metadata_policy.py::test_a_genre_with_no_lookup_row_is_skipped_and_surfaced`
  - `tests/test_metadata_policy.py::test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip`

Old text:

```
        if genre_id is None:
            skipped.append(Skipped(content_id, "genre-unknown", wanted))
            continue
```

New text:

```
        if genre_id is None:
            continue
```

### `u59.M1_permissive_default`

Restore the permissive default: an unreadable marker reads as active

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M1_permissive_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row`
  - `tests/test_metadata_policy.py::test_a_genre_row_that_cannot_report_the_marker_refuses_rather_than_resolving`
  - `tests/test_metadata_policy.py::test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip`

Old text:

```
        marker = getattr(row, rb_writer.SOFT_DELETE_COLUMN, _MARKER_ABSENT)
```

New text:

```
        marker = getattr(row, rb_writer.SOFT_DELETE_COLUMN, 0)
```

### `u59.M2_refusal_removed`

Delete the refusal entirely, so an absent marker falls through as falsey

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M2_refusal_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row`
  - `tests/test_metadata_policy.py::test_a_genre_row_that_cannot_report_the_marker_refuses_rather_than_resolving`
  - `tests/test_metadata_policy.py::test_an_explicit_none_marker_refuses_alongside_a_missing_attribute`
  - `tests/test_metadata_policy.py::test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip`

Old text:

```
        if marker is _MARKER_ABSENT or marker is None:
```

New text:

```
        if False:
```

### `u59.M3_none_admitted`

Stop refusing an explicit None; bool(None) is the same permissive answer

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M3_none_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_an_explicit_none_marker_refuses_alongside_a_missing_attribute`

Old text:

```
        if marker is _MARKER_ABSENT or marker is None:
```

New text:

```
        if marker is _MARKER_ABSENT:
```

### `u59.M4_tombstone_resolves`

Invert the active test, so a soft-deleted genre is the one that resolves

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M4_tombstone_resolves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 10 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_live_namesake_behind_a_tombstone_is_still_found_through_the_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`
  - `tests/test_genre_retag.py::test_a_written_file_is_relinked_to_the_existing_genre_row`
  - `tests/test_genre_retag.py::test_an_unregistered_operation_writes_nothing_and_the_apply_is_what_prevents_it`
  - `tests/test_genre_retag.py::test_re_applying_a_plan_over_an_already_linked_row_is_a_no_op`
  - `tests/test_metadata_policy.py::test_a_deleted_marker_is_not_an_error_here_the_way_it_is_for_a_track`
  - `tests/test_metadata_policy.py::test_a_genre_that_exists_is_linked_by_identifier`
  - `tests/test_metadata_policy.py::test_a_genre_whose_only_row_is_soft_deleted_resolves_to_nothing`
  - `tests/test_metadata_policy.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`

Old text:

```
        if not marker:
            return row.ID
```

New text:

```
        if marker:
            return row.ID
```

### `u59.M5_first_row_wins`

Return the first row rather than the first ACTIVE one, ending the loop

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M5_first_row_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 6 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_live_namesake_behind_a_tombstone_is_still_found_through_the_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`
  - `tests/test_metadata_policy.py::test_a_deleted_marker_is_not_an_error_here_the_way_it_is_for_a_track`
  - `tests/test_metadata_policy.py::test_a_genre_whose_only_row_is_soft_deleted_resolves_to_nothing`
  - `tests/test_metadata_policy.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`

Old text:

```
        if not marker:
            return row.ID
    return None
```

New text:

```
        return row.ID
    return None
```

### `u59.M6_reason_reworded`

Reword the refusal reason, which the plan and the report both key on

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M6_reason_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row`
  - `tests/test_metadata_policy.py::test_a_genre_row_that_cannot_report_the_marker_refuses_rather_than_resolving`
  - `tests/test_metadata_policy.py::test_an_explicit_none_marker_refuses_alongside_a_missing_attribute`
  - `tests/test_metadata_policy.py::test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip`

Old text:

```
                "soft-delete-marker-unreadable",
```

New text:

```
                "soft-delete-marker-unknown",
```

### `r239-b.S7_metadata_key_off`

mytags' open passes unlock=False

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r239-b.json`, row `S7_metadata_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 724 against a baseline of 724
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
        require_closed=writing,
        cfg=cfg,

```

New text:

```
        require_closed=writing,
        unlock=False,
        cfg=cfg,

```

### `r342.E1_cut_inclusive`

Existing guard sample: the with-vox cut becomes exclusive

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `E1_cut_inclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_vocal_tag_values_are_empty_below_the_cut`

Old text:

```
if voxlevel is None or voxlevel < cut:
```

New text:

```
if voxlevel is None or voxlevel <= cut:
```

### `r342.V13_detail_key`

Rename the calibration detail key the refusal carries

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V13_detail_key`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 10 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[boolean]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[empty]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[list]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[nan]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[no-key]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[null]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[overflow]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[text]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[truncated]`

Old text:

```
detail={"calibration": str(path), "kind": type(exc).__name__},
```

New text:

```
detail={"path": str(path), "kind": type(exc).__name__},
```

### `r342.V1_default_on_corrupt`

Restore the defect: an unreadable calibration returns the default cut instead of refusing

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V1_default_on_corrupt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 12 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_a_vocal_calibration_this_account_cannot_read_refuses`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[boolean]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[empty]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[list]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[nan]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[no-key]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[null]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[overflow]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[text]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[truncated]`

Old text:

```
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        raise refuse(

```

New text:

```
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        return DEFAULT_VOCAL_THRESHOLD
        raise refuse(

```

### `r342.V2_no_finite_check`

Drop the finiteness check, so NaN and Infinity read as a cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V2_no_finite_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[nan]`

Old text:

```
        if not math.isfinite(threshold):
            raise ValueError(f"threshold {threshold} is not a finite number")

```

New text:

```
(empty)
```

### `r342.V3_isnan_for_isfinite`

Nearby value: check only for NaN, so Infinity reads as a cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V3_isnan_for_isfinite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`

Old text:

```
if not math.isfinite(threshold):
```

New text:

```
if math.isnan(threshold):
```

### `r342.V4_no_bool_check`

Drop the boolean check, so true reads as a cut of 1.0

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V4_no_bool_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[boolean]`

Old text:

```
        if isinstance(raw, bool):
            raise TypeError(f"threshold {raw} is a boolean, not a number")

```

New text:

```
(empty)
```

### `r342.V5_tuple_drops_overflow`

Drop OverflowError from the except tuple, the review's finding

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V5_tuple_drops_overflow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[overflow]`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (OSError, ValueError, KeyError, TypeError) as exc:
```

### `r342.V6_tuple_drops_keyerror`

Drop KeyError from the except tuple, so a file with no threshold key crashes

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V6_tuple_drops_keyerror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[no-key]`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (OSError, ValueError, TypeError, OverflowError) as exc:
```

### `r342.V7_tuple_drops_typeerror`

Drop TypeError from the except tuple, so a list, null or boolean payload crashes

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V7_tuple_drops_typeerror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 3 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[boolean]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[list]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[null]`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (OSError, ValueError, KeyError, OverflowError) as exc:
```

### `r342.V8_tuple_drops_valueerror`

Drop ValueError from the except tuple, so truncated JSON crashes

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V8_tuple_drops_valueerror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 6 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[empty]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[nan]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[text]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[truncated]`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (OSError, KeyError, TypeError, OverflowError) as exc:
```

### `r342.V9_tuple_drops_oserror`

Drop OSError from the except tuple, so an unreadable file escapes unnamed

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V9_tuple_drops_oserror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_vocal_calibration_this_account_cannot_read_refuses`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (ValueError, KeyError, TypeError, OverflowError) as exc:
```

### `r372-a.A1_majority_boundary`

majority_unmapped: half is a majority, so 5 of 10 refuses

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A1_majority_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_majority_is_strictly_more_than_half_and_never_an_empty_collection[10-5-False]`

Old text:

```
        return self.active > 0 and self.unmapped * 2 > self.active
```

New text:

```
        return self.active > 0 and self.unmapped * 2 >= self.active
```

### `r372-a.A2_majority_coefficient`

majority_unmapped: two thirds rather than half, so 6 of 10 is not a majority

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A2_majority_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_majority_is_strictly_more_than_half_and_never_an_empty_collection[10-5-False]`

Old text:

```
        return self.active > 0 and self.unmapped * 2 > self.active
```

New text:

```
        return self.active > 0 and self.unmapped * 3 > self.active
```

### `r372-a.A3_pathless_rows_count_as_unmapped`

_survey: count every row that did not resolve as unmapped, streaming rows included

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A3_pathless_rows_count_as_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 17 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`
  - `tests/test_paths_resolved.py::test_a_minority_of_unmapped_rows_stays_ok_with_the_counts_visible`
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_a_row_whose_location_will_not_decode_counts_as_unresolved_not_a_defect`
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_minority_as_a_note_and_a_clean_collection_as_ok`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        if outcome.resolution is locations.Resolution.UNMAPPED:
```

New text:

```
        if outcome.path is None:
```

### `r372-a.A4_verb_never_refuses`

mytags_vocals: drop the majority refusal, so the plan reports ok over a majority

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A4_verb_never_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_an_apply_over_a_majority_refuses_the_same_way_and_writes_nothing`

Old text:

```
        if survey.totals.majority_unmapped:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
```

New text:

```
        if False:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
```

### `r372-a.A5_apply_proceeds`

mytags_vocals: refuse the plan alone and let the apply through

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A5_apply_proceeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_an_apply_over_a_majority_refuses_the_same_way_and_writes_nothing`

Old text:

```
        if survey.totals.majority_unmapped:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
```

New text:

```
        if survey.totals.majority_unmapped and not writing:
            empty = _plan_from(cfg, _Survey(survey.totals, ()))
```

### `r372-a.A6_decode_error_escapes`

_survey: let a location that will not decode raise through the plan and the check

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A6_decode_error_escapes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_row_whose_location_will_not_decode_counts_as_unresolved_not_a_defect`

Old text:

```
        except locations.LocationDecodeError:
```

New text:

```
        except ZeroDivisionError:
```

### `r372-a.A7_remedy_run_doctor`

majority_unmapped_cause: send the person to doctor, which sends them back

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A7_remedy_run_doctor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 3 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_the_two_synthetic_machines_answer_the_check_opposite_ways`

Old text:

```
        remedy=Remedy.RUN_SETUP,
        steps=(
```

New text:

```
        remedy=Remedy.RUN_DOCTOR,
        steps=(
```

### `r372-a.A8_refused_plan_reports_ok`

_refused_plan: outcome ok beside a cause, the envelope the validator rejects

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r372-a.json`, row `A8_refused_plan_reports_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_an_apply_over_a_majority_refuses_the_same_way_and_writes_nothing`

Old text:

```
        outcome=Outcome.FAILED,
        code=cause.code,
        data=plan,
```

New text:

```
        outcome=Outcome.OK,
        code=cause.code,
        data=plan,
```

### `r375-b.M2_a_noop_claims_a_commit`

_record_mytags_commit: record a commit for an apply that wrote nothing

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r375-b.json`, row `M2_a_noop_claims_a_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`

Old text:

```
    if written <= 0:
        return

```

New text:

```
(empty)
```

### `r375-b.M3_witnessed_commit_not_recorded`

mytags_vocals: ignore the witness, so a commit that landed and then raised closes as though nothing landed

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r375-b.json`, row `M3_witnessed_commit_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`

Old text:

```
                if witness.landed:
```

New text:

```
                if False:
```

### `r375-b.M4_summary_keyed_on_the_display_name`

_record_mytags_commit: key the change summary on the category's display name, which a person can rename (R19)

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r375-b.json`, row `M4_summary_keyed_on_the_display_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`

Old text:

```
session.TreeChange(tree=CHANGE_KEY, created=written)
```

New text:

```
session.TreeChange(tree=CATEGORY, created=written)
```

### `u25.G10_ignore_cut`

Every scored track is tagged, including those below the cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G10_ignore_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_vocal_tag_values_are_empty_below_the_cut`

Old text:

```
    if voxlevel is None or voxlevel < cut:
        return []

```

New text:

```
    if voxlevel is None:
        return []

```

### `u25.G11_gender_without_vox`

Gender tags are applied even when the track is below the cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G11_gender_without_vox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_vocal_tag_values_are_empty_below_the_cut`

Old text:

```
    if voxlevel is None or voxlevel < cut:
        return []
    values = [VALUE_VOX]
    if voxgender == "M":
        values.append(VALUE_MALE)
    elif voxgender == "F":
        values.append(VALUE_FEMALE)
    return values

```

New text:

```
    values = []
    if voxlevel is not None and voxlevel >= cut:
        values.append(VALUE_VOX)
    if voxgender == "M":
        values.append(VALUE_MALE)
    elif voxgender == "F":
        values.append(VALUE_FEMALE)
    return values

```

### `u25.G12_apply_by_default`

The plan path writes, so a dry run mutates the database

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G12_apply_by_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`

Old text:

```
        action="store_true",
        default=False,

```

New text:

```
        action="store_true",
        default=True,

```

### `u25.G13_skip_apply_gate`

Return the plan even when apply was requested, so nothing is written

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G13_skip_apply_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 8 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`

Old text:

```
        if not writing:
            return ctx.envelope(data=plan, outcome=Outcome.OK)

```

New text:

```
        if True:
            return ctx.envelope(data=plan, outcome=Outcome.OK)

```

### `u25.G24_content_column`

The My Tags apply also writes Rating, a content column

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G24_content_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 6 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`

Old text:

```
            if rb_writer.add_my_tag(db, value_row, content_id):
                written += 1
            else:
                already += 1

```

New text:

```
            if rb_writer.add_my_tag(db, value_row, content_id):
                written += 1
            else:
                already += 1
            row = db.get_content(ID=content_id)
            if row is not None:
                row.Rating = 5

```

### `u89.L1_absent_is_default`

load_vocal_threshold: an absent calibration returns the default cut instead of None, so routing files from a cut nobody fitted

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u89.json`, row `L1_absent_is_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_metadata_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 126 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_absent_vocal_calibration_is_the_default_cut`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`
  - `tests/test_routing_workers.py::test_a_25_minute_track_is_a_member_and_a_19_minute_one_is_not`
  - `tests/test_routing_workers.py::test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses`
  - `tests/test_routing_workers.py::test_a_clean_apply_names_no_skipped_file`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - ... and 111 more, see the JSON sidecar

Old text:

```
    if not path.is_file():
        return None
```

New text:

```
    if not path.is_file():
        return DEFAULT_VOCAL_THRESHOLD
```

### `u89.L2_tagging_default`

vocal_cut: drop the default fallback, so an uncalibrated My Tags pass has no cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u89.json`, row `L2_tagging_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_metadata_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 12 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_absent_vocal_calibration_is_the_default_cut`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`
  - `tests/test_routing_workers.py::test_the_loader_says_absent_as_none_and_the_tagging_cut_still_defaults`

Old text:

```
    return DEFAULT_VOCAL_THRESHOLD if threshold is None else threshold
```

New text:

```
    return threshold
```

### `u90-c.C6_wrapper_reads_nothing`

load_vocal_threshold stops delegating, so every caller sees an uncalibrated library

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u90-c.json`, row `C6_wrapper_reads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_metadata_cli.py`
- Collected: 203 against a baseline of 203
- Kills: 8 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_hand_cut_replaces_an_unreadable_calibration_and_says_it_could_not_be_read`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[0]`
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[100]`
  - `tests/test_metadata_cli.py::test_a_present_vocal_calibration_is_its_own_threshold`

Old text:

```
    return None if record is None else record["threshold"]
```

New text:

```
    return None
```

### `r172-a.A1_nothing_collides`

Hold nothing, which is the finding itself: two files rendering to one name are promised two renames and the apply performs one

- File: `src/cratekit/write/naming_cli.py`
- Source: `r172-a.json`, row `A1_nothing_collides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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
- Collected: 99 against a baseline of 99
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

### `r239-b.S8_naming_key_off`

the naming verb's collection read passes unlock=False

- File: `src/cratekit/write/naming_cli.py`
- Source: `r239-b.json`, row `S8_naming_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 724 against a baseline of 724
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
            require_closed=False,
            cfg=cfg,

```

New text:

```
            require_closed=False,
            unlock=False,
            cfg=cfg,

```

