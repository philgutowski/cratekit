# Mutation table: u331-after-03

Measured by `scripts/mutate.py` on 2026-11-24 02:09 UTC, branch `HEAD` at `d29860c2`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23132 collected. pytest invocations for this batch: 177.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 02:09 UTC for commit `d29860c2a9b3`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 33, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23132 against 23132. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u241.M14_a_changed_file_keeps_its_old_head` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 4 | killed |
| `u241.M15_identity_without_the_time` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 1 | killed |
| `u241.M16_changed_settings_keep_old_heads` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 3 | killed |
| `u241.M23_identity_without_the_size` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 1 | killed |
| `u241.M24_identity_after_the_read` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 2 | killed |
| `u276.K12_stream_worker_binding_names_whole` | `src/cratekit/analysis/ahead.py` | user | 3 file(s) | 305 | 1 | killed |
| `r1255.C1_check_landed_unlisted` | `src/cratekit/intake/rekordbox_check.py` | user | 2 file(s) | 86 | 1 | killed |
| `u167.M10_wheel_wrap` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 2 | killed |
| `u167.M13_suspect_state_guard` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u167.M14_dyn_excuses` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 2 | killed |
| `u167.M15_unread_suspect` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 5 | killed |
| `u167.M17_gone_counts_as_nothing` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 2 | killed |
| `u167.M19_landing_without_rows` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u167.M1_file_kind` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u167.M21_name_wins` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 7 | killed |
| `u167.M22_analysed_reading` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 3 | killed |
| `u167.M3_tag_fits` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 2 | killed |
| `u167.M4_grid_parse_failure` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u167.M5_short_header` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u167.M6_constant_test` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 5 | killed |
| `u167.M7_missing_folded` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 2 | killed |
| `u167.M8_empty_grid` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u167.M9_relative_key` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u259.M11_scope_carries_no_rows` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u259.M13_batch_failure_not_met_again` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u259.M14_batch_failure_reads_nothing` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u259.M15_id_not_text_judged` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u259.M16_id_skip_widened` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u259.M6_unanalysed_reads_by_id` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u259.M7_unanalysed_keeps_no_row` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 6 | killed |
| `u259.M8_check_rows_rereads_scope` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 1 | killed |
| `u259.M9_read_row_per_row` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 3 | killed |
| `u327.A23_check_not_suspect_on_keys` | `src/cratekit/intake/rekordbox_check.py` | user | 3 file(s) | 223 | 29 | killed |
| `u327.A2_tempo_tolerance` | `src/cratekit/intake/rekordbox_check.py` | user | 2 file(s) | 185 | 10 | killed |
| `u327.A4_tempo_rounds_half_up` | `src/cratekit/intake/rekordbox_check.py` | user | 2 file(s) | 185 | 6 | killed |
| `u327.A5_tempo_zero_is_no_answer` | `src/cratekit/intake/rekordbox_check.py` | user | 2 file(s) | 185 | 5 | killed |
| `u327.B2_differs_needs_a_title_head` | `src/cratekit/intake/rekordbox_check.py` | user | 2 file(s) | 185 | 3 | killed |
| `example-binaries-five-row.B1_broken_override_falls_through` | `src/cratekit/core/binaries.py` | user | 1 file(s) | 18 | 1 | killed |
| `example-binaries-five-row.B3_platform_binary_remedy` | `src/cratekit/core/binaries.py` | maintainer | 1 file(s) | 18 | 1 | killed |
| `example-binaries-five-row.B4_unknown_source_remedy` | `src/cratekit/core/binaries.py` | maintainer | 1 file(s) | 18 | 1 | killed |
| `example-binaries-five-row.B5_credential_strip` | `src/cratekit/core/binaries.py` | user | 1 file(s) | 18 | 1 | killed |
| `r301.V4_label_shape_loose` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 4 | killed |
| `r345.A1_colon_required` | `src/cratekit/core/config_schema.py` | user | 3 file(s) | 759 | 1 | killed |
| `r345.A2_single_letter` | `src/cratekit/core/config_schema.py` | user | 3 file(s) | 759 | 6 | killed |
| `r345.A3_name_shape` | `src/cratekit/core/config_schema.py` | user | 3 file(s) | 759 | 6 | killed |
| `r345.A4_leading_hyphen` | `src/cratekit/core/config_schema.py` | user | 3 file(s) | 759 | 3 | killed |
| `r345.A5_trailing_space` | `src/cratekit/core/config_schema.py` | user | 3 file(s) | 759 | 3 | killed |
| `r44-a.C3_identity_not_written` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 1 | killed |
| `r662-a.M2_spelled_path_compared_whole` | `src/cratekit/core/config_schema.py` | user | 2 file(s) | 670 | 2 | killed |
| `r662-b.M1b_several_remotes_compared` | `src/cratekit/core/config_schema.py` | user | 2 file(s) | 670 | 1 | killed |
| `r662-b.M3b_blank_remote_disagrees` | `src/cratekit/core/config_schema.py` | maintainer | 2 file(s) | 670 | 1 | killed |
| `u193.M13_default_coefficient` | `src/cratekit/core/config_schema.py` | user | 5 file(s) | 523 | 3 | killed |
| `u197-m6.M6_composite` | `src/cratekit/core/config_schema.py` | user | 3 file(s) | 827 | 2 | killed |
| `u197.M2_retired_mapping_empty` | `src/cratekit/core/config_schema.py` | user | 3 file(s) | 827 | 4 | killed |
| `u233.C1_schema_default_moves` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 19 | 1 | killed |
| `u233.C2_schema_gains_a_key` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 19 | 1 | killed |
| `u299.U12_pin_refusal_remedy` | `src/cratekit/core/config_schema.py` | user | 2 file(s) | 466 | 1 | killed |
| `r1255.S1_scan_unlisted_as_empty` | `src/cratekit/core/session.py` | user | 7 file(s) | 867 | 14 | killed |
| `r1255.S2_absent_log_unread` | `src/cratekit/core/session.py` | user | 7 file(s) | 867 | 46 | killed |
| `r1255.S3_log_file_absent` | `src/cratekit/core/session.py` | user | 2 file(s) | 432 | 1 | killed |
| `r1255.S4_under_a_file_unread` | `src/cratekit/core/session.py` | user | 2 file(s) | 432 | 1 | killed |
| `r1255.S5_json_filter` | `src/cratekit/core/session.py` | user | 7 file(s) | 867 | 1 | killed |
| `r1255.S6_records_refuses_unlisted` | `src/cratekit/core/session.py` | user | 4 file(s) | 628 | 4 | killed |
| `r1255.S7_log_unlisted_predicate` | `src/cratekit/core/session.py` | user | 4 file(s) | 143 | 11 | killed |
| `r1255.S8_clause_listing_wording` | `src/cratekit/core/session.py` | user | 3 file(s) | 116 | 8 | killed |
| `r1255.S9_gate_unlisted_detail` | `src/cratekit/core/session.py` | maintainer | 3 file(s) | 322 | 2 | killed |
| `r239-b.S11_readback_key_on` | `src/cratekit/core/session.py` | user | 7 file(s) | 724 | 1 | killed |
| `r375-a.S10_commit_not_persisted_at_once` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 1 | killed |
| `r375-a.S11_commit_replaces_the_summary` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 3 | killed |
| `r375-a.S1_keep_is_ignored` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 38 | killed |
| `r375-a.S2_record_inside_the_watch` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 3 | killed |
| `r375-a.S3_a_raise_is_not_abandoned` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 13 | killed |
| `r375-a.S4_abandon_failure_replaces_the_error` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 1 | killed |
| `r375-a.S5_clean_close_refusal_leaves_it_open` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 1 | killed |
| `r375-a.S6_close_ignores_the_intent` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 11 | killed |
| `r375-a.S7_close_drops_the_identity_seam` | `src/cratekit/core/session.py` | maintainer | 4 file(s) | 393 | 4 | killed |
| `r375-a.S8_record_names_no_actor` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 2 | killed |
| `r375-a.S9_record_names_no_acknowledgment` | `src/cratekit/core/session.py` | user | 4 file(s) | 393 | 2 | killed |
| `r501-a.S1_verify_state_guard` | `src/cratekit/core/session.py` | maintainer | 5 file(s) | 134 | 1 | killed |
| `r501-a.S2_excusal_capture` | `src/cratekit/core/session.py` | user | 5 file(s) | 134 | 1 | killed |
| `r501-a.S3_excusal_proof` | `src/cratekit/core/session.py` | user | 5 file(s) | 134 | 5 | killed |
| `r501-a.S4_excusal_state` | `src/cratekit/core/session.py` | user | 5 file(s) | 134 | 1 | killed |
| `r598-a.A5_holder_never_recorded` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 8 | killed |
| `r598-a.A6_record_holder_is_a_second_lookup` | `src/cratekit/core/session.py` | maintainer | 2 file(s) | 185 | 1 | killed |
| `r154-c.C1_digest_the_word` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `r154-c.C2_expected_volume_outside_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `r154-c.C3_hand_down_the_flag` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r154-c.C4_pull_flags_dropped` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 4 | killed |
| `r154-c.C5_stated_volume_stops_at_the_verb` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r1924.C1_refusal` | `src/cratekit/session/restore_cli.py` | user | 4 file(s) | 411 | 4 | killed |
| `r1924.C2_totals` | `src/cratekit/session/restore_cli.py` | user | 4 file(s) | 411 | 9 | killed |
| `r1924.C3_dry_run_message` | `src/cratekit/session/restore_cli.py` | user | 4 file(s) | 411 | 1 | killed |
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
| `r368.G8_target_without_the_off_machine_pull_is_allowed` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r368.G9_target_beside_a_capture_rollback_is_allowed` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `r592-b.B5_step_names_no_file` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r592-b.B7_sample_halves_split` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u211.R1_restore_says_what_the_mirror_left` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u27-restore-cli-author.G3_abort_restores_anyway` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u27-restore-cli-author.L1_an_unusable_capture_is_filtered_out_of_the_listing` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u27-restore-cli-author.N1_the_default_takes_the_newest_unusable_capture` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u27-restore-cli-author.P1_the_report_recomputes_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u27-restore-cli-author.P3_convergence_is_reported_for_a_run_that_spent_no_capture` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u27-restore-cli-author.R1_a_backup_refusal_becomes_an_internal_error` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 10 | killed |
| `u27-restore-cli-author.S1_plan_takes_its_own_lock` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 253 | 9 | killed |
| `u27-restore-cli-author.S6_the_named_decision_is_withdrawn` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 9 | killed |
| `u27-restore-cli-author.S8_a_rehearsal_performs_the_capture_restore` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u27-restore-cli-independent.I_A10_an_off_machine_refusal_is_swallowed` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 4 | killed |
| `u27-restore-cli-independent.I_A3_platform_seams_never_reach_the_session` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 2 | killed |
| `u27-restore-cli-independent.I_A8_discard_set_never_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 1 | killed |
| `u27-restore-cli-independent.I_B2_the_named_session_never_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 3 | killed |
| `u27-restore-cli-independent.I_B3_the_discard_flag_is_dropped_at_the_call` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 1 | killed |
| `u27-restore-cli-independent.I_B7_the_rehearsal_flag_is_dropped_at_the_call` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 1 | killed |
| `u27-restore-cli-independent.I_C1_discard_stops_being_repeatable` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 1 | killed |
| `u27-restore-cli-independent.I_C4_the_session_identifier_becomes_required` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 30 | killed |
| `u27-restore-cli-independent.I_C6_the_listing_verb_runs_the_restore` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 3 | killed |
| `u27-restore-cli-independent.I_E4_the_reason_a_capture_cannot_be_spent_is_blanked` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 2 | killed |
| `u27-restore-cli-independent.I_F3_an_unknown_identifier_becomes_a_defect_report` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 1 | killed |
| `u27-restore-cli-independent.I_F4_the_refusal_stops_naming_the_identifier` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 1 | killed |
| `u27-restore-cli-independent.X5_the_refusal_reason_is_flattened` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 1272 | 9 | killed |
| `u27-restore-cli-round-2.G1_gate_found_by_position` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 1113 | 1 | killed |
| `u27-restore-cli-round-2.O2_the_discard_set_leaves_the_digest` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u27-restore-cli-round-2.R2_the_reserved_remediation_is_replaced_by_the_class_default` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u27-restore-cli-round-2.S3_analysis_watch_watches_nothing` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 242 | 1 | killed |
| `u311.B1_verb_refusal_origin` | `src/cratekit/session/restore_cli.py` | user | 3 file(s) | 336 | 14 | killed |
| `u96-a.A13_completed_halves_recorded` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u96-a.A14_target_is_required` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u96-a.A1_acceptance_reaches_the_engine` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u96-a.A2_flag_reaches_the_function` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u96-a.A4_run_inside_the_held_session` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u96-a.A5_the_mirror_is_pulled` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u96-a.A6_a_half_at_a_time` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u259.M10_chunk_size` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 2 | killed |

## Considered and dropped

Recorded rows this replay left out and did NOT measure. They are not coverage, and `scripts/killset.py check` fails on one that was killed before and is neither a row nor mapped here.

- `u167.M11_sigmas`: KEY_AGREEMENT_SIGMAS: two standard errors rather than three Dropped because: gone at the head, removed by U343 on main (b1e44ba9), not by U331: U343's b1e44ba9 (feat(u343): analyze run measures no key and writes no head) dropped analyze check's key floor: it removed `KEY_AGREEMENT_SIGMAS = 3.0` from analysis/rekordbox_check.py, and its killing test test_the_key_floor_is_the_recorded_rate_less_three_standard_errors with it; nothing at the head measures a key agreement
- `u167.M12_floor_rate`: key_floor: take the rate over differs alone rather than over every compared key Dropped because: gone at the head, removed by U343 on main (b1e44ba9), not by U331: U343's b1e44ba9 removed `def key_floor(compared: int) -> float | None:` whole from analysis/rekordbox_check.py, its line `total = measured["equal"] + measured["differs"]` with it, and the check's key_suspect property; the head has no key floor

## Row definitions

### `u241.M14_a_changed_file_keeps_its_old_head`

ahead: a head measured ahead is used whatever file now sits at the path

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M14_a_changed_file_keeps_its_old_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_replaced_after_its_head_was_measured_is_measured_again`
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_at_the_same_length_is_measured_again_by_its_time_alone`
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_in_place_after_its_head_was_measured_is_measured_again`
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_with_its_time_put_back_is_measured_again_by_its_size_alone`

Old text:

```
    if measured_identity is None or measured_identity != identity_of(path):

```

New text:

```
    if False:

```

### `u241.M15_identity_without_the_time`

ahead.identity_of: no modification time, so a file rewritten at the same length keeps its old head

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M15_identity_without_the_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_at_the_same_length_is_measured_again_by_its_time_alone`

Old text:

```
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)

```

New text:

```
    return (found.st_dev, found.st_ino, found.st_size, 0)

```

### `u241.M16_changed_settings_keep_old_heads`

ahead: heads measured under the old calibration are used after it changes

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M16_changed_settings_keep_old_heads`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_each_setting_a_head_is_measured_under_is_compared[drift-cut]`
  - `tests/test_analysis_ahead.py::test_each_setting_a_head_is_measured_under_is_compared[tempo-window]`
  - `tests/test_analysis_ahead.py::test_settings_that_changed_mid_run_stop_the_pool_and_the_rest_is_measured_here`

Old text:

```
    if settings != session.settings:
        session.stop(STOPPED_SETTINGS)
        return None

```

New text:

```
(empty)
```

### `u241.M23_identity_without_the_size`

ahead.identity_of: no size, so a file rewritten with its time put back keeps its old head

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M23_identity_without_the_size`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_with_its_time_put_back_is_measured_again_by_its_size_alone`

Old text:

```
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)

```

New text:

```
    return (found.st_dev, found.st_ino, 0, found.st_mtime_ns)

```

### `u241.M24_identity_after_the_read`

ahead.measure: the identity is taken after the read, so a file written while it was read carries the written file's identity

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M24_identity_after_the_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_replaced_after_its_head_was_measured_is_measured_again`
  - `tests/test_analysis_ahead.py::test_the_identity_a_worker_returns_is_the_files_before_the_read`

Old text:

```
    found = identity_of(path)
    return found, light.analyse(path)

```

New text:

```
    head = light.analyse(path)
    return identity_of(path), head

```

### `u276.K12_stream_worker_binding_names_whole`

analysis/ahead.py: a stream worker's detector binding names the whole method, so a head measured ahead reads another key than the driver's

- File: `src/cratekit/analysis/ahead.py`
- Source: `u276.json`, row `K12_stream_worker_binding_names_whole`
- Surface: user
- Subset: test files importing cratekit.analysis.ahead
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_ahead_real.py`, `tests/test_restamp_scored_by.py`
- Collected: 305 against a baseline of 305
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_the_settings_a_worker_is_started_with_are_the_ones_the_item_binds`

Old text:

```
            drift_cut=float(drift_cut),
        )
    )
```

New text:

```
            drift_cut=float(drift_cut),
            key="whole",
        )
    )
```

### `r1255.C1_check_landed_unlisted`

_landed: never stop on the listing, so the pass lookup refuses in words of its own

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `r1255.json`, row `C1_check_landed_unlisted`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_analyze_check.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_the_check_refuses_an_unknown_landing_naming_the_listing`

Old text:

```
    if session.log_unlisted(unreadable, cfg):
        # NO LANDING CAN BE READ
```

New text:

```
    if False:
        # NO LANDING CAN BE READ
```

### `u167.M10_wheel_wrap`

key_relation: forget the wheel wraps, so 12 and 1 read far

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M10_wheel_wrap`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_title_key_is_equal_one_step_or_far_from_rekordbox_s[12B-1B-one_step]`
  - `tests/test_analyze_check.py::test_the_title_key_is_equal_one_step_or_far_from_rekordbox_s[1A-12A-one_step]`

Old text:

```
    if letter == other_letter and (number - other_number) % 12 in (1, 11):
```

New text:

```
    if letter == other_letter and abs(number - other_number) == 1:
```

### `u167.M13_suspect_state_guard`

suspect_grid: judge the grid of a row that is not analysed

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M13_suspect_state_guard`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_row_not_analysed_never_reads_suspect_whatever_grid_it_carries`

Old text:

```
        if self.state != ANALYSED:
            return False
        if self.grid.state == VARIABLE:
```

New text:

```
        if self.grid.state == VARIABLE:
```

### `u167.M14_dyn_excuses`

suspect_grid: a dyn mark no longer excuses a variable grid

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M14_dyn_excuses`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_variable_grid_on_a_row_marked_dyn_is_done`
  - `tests/test_analyze_check.py::test_the_same_variable_grid_on_a_row_marked_dyn_is_done`

Old text:

```
            return not self.dyn
```

New text:

```
            return True
```

### `u167.M15_unread_suspect`

suspect_grid: a missing or unreadable grid on an analysed row is not suspect

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M15_unread_suspect`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 5 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_variable_or_unread_grid_is_suspect[absent]`
  - `tests/test_analyze_check.py::test_a_variable_or_unread_grid_is_suspect[missing]`
  - `tests/test_analyze_check.py::test_a_variable_or_unread_grid_is_suspect[unreadable]`
  - `tests/test_analyze_check.py::test_an_analysed_row_whose_file_is_missing_is_suspect`
  - `tests/test_analyze_check.py::test_an_unread_grid_on_a_row_marked_dyn_is_still_suspect`

Old text:

```
        return self.grid.state in (ABSENT, MISSING, UNREADABLE)
```

New text:

```
        return False
```

### `u167.M17_gone_counts_as_nothing`

verdict: drop the all gone case, so a scope of removed rows reads done

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M17_gone_counts_as_nothing`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_named_landing_whose_every_row_left_the_collection_refuses`
  - `tests/test_analyze_check.py::test_no_row_or_only_gone_rows_is_nothing`

Old text:

```
        if not self.rows or self.counted(GONE) == len(self.rows):
```

New text:

```
        if not self.rows:
```

### `u167.M19_landing_without_rows`

resolve_scope: a named landing whose playlists hold no live row reads as an empty scope

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M19_landing_without_rows`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_pass_whose_playlists_hold_no_live_row_refuses_rather_than_reading_empty`

Old text:

```
        if not members:
            raise refuse(
```

New text:

```
        if False:
            raise refuse(
```

### `u167.M1_file_kind`

grid_ticks: accept any first four bytes, so a file that is not an analysis file is walked

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M1_file_kind`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_damaged_file_reads_unreadable_never_absent[not-an-analysis-file]`

Old text:

```
    if kind != _FILE_KIND:
```

New text:

```
    if False:
```

### `u167.M21_name_wins`

resolve_scope: the playlist wins over a named pass when it holds rows

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M21_name_wins`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 7 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_landing_nothing_recorded_refuses_rather_than_reading_empty[--pass]`
  - `tests/test_analyze_check.py::test_a_landing_nothing_recorded_refuses_rather_than_reading_empty[--session]`
  - `tests/test_analyze_check.py::test_a_landing_s_session_names_its_rows`
  - `tests/test_analyze_check.py::test_a_named_landing_whose_every_row_left_the_collection_refuses`
  - `tests/test_analyze_check.py::test_a_pass_names_its_landing_s_rows_over_the_playlist`
  - `tests/test_analyze_check.py::test_a_pass_whose_playlists_hold_no_live_row_refuses_rather_than_reading_empty`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_for_a_named_landing`

Old text:

```
    if pass_name is not None or session_id is not None:
        kind
```

New text:

```
    if (pass_name is not None or session_id is not None) and not _analyze_members(db, declared, registry)[0]:
        kind
```

### `u167.M22_analysed_reading`

read_row: a row the clear would leave waiting is read as analysed

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M22_analysed_reading`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_for_a_named_landing`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_in_inbox_analyze`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_over_every_row`

Old text:

```
    if one.action != analyzed.CLEAR:
```

New text:

```
    if one.why == analyzed.NOT_ANALYSED:
```

### `u167.M3_tag_fits`

grid_ticks: drop the tag fits check, so an overrunning or undersized tag is parsed

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M3_tag_fits`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_damaged_file_reads_unreadable_never_absent[a-tag-of-length-zero-before-the-grid]`
  - `tests/test_analyze_check.py::test_a_damaged_file_reads_unreadable_never_absent[a-tag-that-overruns]`

Old text:

```
        if tag_length < _HEADER.size or offset + tag_length > len(data):
```

New text:

```
        if False:
```

### `u167.M4_grid_parse_failure`

grid_ticks: read a grid tag that will not parse as a file with no grid

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M4_grid_parse_failure`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_damaged_file_reads_unreadable_never_absent[a-grid-tag-that-will-not-parse]`

Old text:

```
                raise ValueError(f"the grid tag would not parse: {exc}") from exc
```

New text:

```
                return None
```

### `u167.M5_short_header`

grid_ticks: drop the short file refusal, so ten bytes reach the unpack

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M5_short_header`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_damaged_file_reads_unreadable_never_absent[shorter-than-a-header]`

Old text:

```
    if len(data) < _HEADER.size:
```

New text:

```
    if False:
```

### `u167.M6_constant_test`

read_grid: call a grid constant when its ends are within a whole beat per minute

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M6_constant_test`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 5 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_removed_dyn_mark_does_not_excuse_a_variable_grid`
  - `tests/test_analyze_check.py::test_a_variable_grid_on_a_row_not_marked_dyn_is_suspect_and_exits_27`
  - `tests/test_analyze_check.py::test_a_variable_grid_reads_variable_with_its_span`
  - `tests/test_analyze_check.py::test_no_file_under_the_library_is_opened_for_writing`
  - `tests/test_analyze_check.py::test_suspect_outranks_waiting_through_the_verb`

Old text:

```
        state=CONSTANT if low == high else VARIABLE, beats=len(ticks), low=low, high=high
```

New text:

```
        state=CONSTANT if high - low < 1000 else VARIABLE, beats=len(ticks), low=low, high=high
```

### `u167.M7_missing_folded`

read_grid: read a missing analysis file as a file with no grid

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M7_missing_folded`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_missing_file_reads_missing`
  - `tests/test_analyze_check.py::test_an_analysed_row_whose_file_is_missing_is_suspect`

Old text:

```
        return Grid(state=MISSING, why=f"no analysis file at {path}")
```

New text:

```
        return Grid(state=ABSENT, why=f"no analysis file at {path}")
```

### `u167.M8_empty_grid`

read_grid: read a grid tag with no beats as constant

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M8_empty_grid`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_file_with_no_grid_tag_reads_absent_never_constant`

Old text:

```
    if not ticks:
        return Grid(state=ABSENT, why=f"{path} holds no beat grid")
```

New text:

```
    if ticks is None:
        return Grid(state=ABSENT, why=f"{path} holds no beat grid")
    if not ticks:
        return Grid(state=CONSTANT)
```

### `u167.M9_relative_key`

key_relation: the relative major or minor reads far, not one step

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u167.json`, row `M9_relative_key`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_title_key_is_equal_one_step_or_far_from_rekordbox_s[8A-8B-one_step]`

Old text:

```
    if number == other_number:
        return KEY_ONE_STEP
```

New text:

```
    if number == other_number:
        return KEY_FAR
```

### `u259.M11_scope_carries_no_rows`

resolve_scope: the unanalysed scope carries none of the rows it read

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u259.json`, row `M11_scope_carries_no_rows`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[unanalysed]`

Old text:

```
        read=waiting,
    )
```

New text:

```
    )
```

### `u259.M13_batch_failure_not_met_again`

check_rows: a batch the binding cannot load fails the check, ahead of an earlier row's refusal

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u259.json`, row `M13_batch_failure_not_met_again`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_row_the_binding_cannot_load_after_one_that_refuses_still_refuses_as_it_did`

Old text:

```
    except Exception:  # noqa: BLE001 - every failure is met again, in order, below
        held = None
```

New text:

```
    except Exception:  # noqa: BLE001 - every failure is met again, in order, below
        raise
```

### `u259.M14_batch_failure_reads_nothing`

check_rows: after a batch the binding cannot load, judge every row as missing rather than read it

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u259.json`, row `M14_batch_failure_reads_nothing`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_row_the_binding_cannot_load_after_one_that_refuses_still_refuses_as_it_did`

Old text:

```
            content=_UNREAD if held is None else held.get(content_id),
```

New text:

```
            content=None if held is None else held.get(content_id),
```

### `u259.M15_id_not_text_judged`

_unanalysed: judge a row whose ID is stored as bytes, so it joins a scope the read by ID never put it in

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u259.json`, row `M15_id_not_text_judged`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_row_whose_id_is_not_text_stays_out_of_every_row_as_it_did`

Old text:

```
        if isinstance(content.ID, bytes):
            continue
```

New text:

```
        if False:
            continue
```

### `u259.M16_id_skip_widened`

_unanalysed: leave out every ID that is not text, round one's fix, so integer IDs read as nothing to check

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u259.json`, row `M16_id_skip_widened`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[unanalysed]`

Old text:

```
        if isinstance(content.ID, bytes):
```

New text:

```
        if not isinstance(content.ID, str):
```

### `u259.M6_unanalysed_reads_by_id`

_unanalysed: ask for each collection row again by ID, the per row read U259 removed

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u259.json`, row `M6_unanalysed_reads_by_id`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[unanalysed]`

Old text:

```
        one = analyzed.judge(content_id, content)
```

New text:

```
        one = analyzed.member(db, content_id)
```

### `u259.M7_unanalysed_keeps_no_row`

_unanalysed: carry no row for a waiting ID, so every row of the scope reads as gone

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u259.json`, row `M7_unanalysed_keeps_no_row`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 6 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[unanalysed]`
  - `tests/test_analyze_check.py::test_a_row_whose_id_is_not_text_stays_out_of_every_row_as_it_did`
  - `tests/test_analyze_check.py::test_an_empty_analyze_playlist_falls_to_every_row_not_analysed`
  - `tests/test_analyze_check.py::test_an_intake_tree_not_cut_over_falls_to_every_row_not_analysed_and_says_why`
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[unanalysed]`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_over_every_row`

Old text:

```
            waiting[one.content_id] = content
```

New text:

```
            waiting[one.content_id] = None
```

### `u259.M8_check_rows_rereads_scope`

check_rows: ignore the rows the scope already read, so the unanalysed scope is read a second time

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u259.json`, row `M8_check_rows_rereads_scope`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[unanalysed]`

Old text:

```
    held: dict[str, Any] | None = dict(scope.read)
```

New text:

```
    held: dict[str, Any] | None = {}
```

### `u259.M9_read_row_per_row`

check_rows: hand read_row no row, so each row in scope is read by ID again

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u259.json`, row `M9_read_row_per_row`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[analyze]`
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[unanalysed]`

Old text:

```
            content=_UNREAD if held is None else held.get(content_id),
```

New text:

```
            content=_UNREAD,
```

### `u327.A23_check_not_suspect_on_keys`

Check.verdict: read suspect on key agreement again, so a visit whose titles differ is held

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u327.json`, row `A23_check_not_suspect_on_keys`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`, `tests/test_analyze_adopt.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 223 against a baseline of 223
- Kills: 29 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_bare_title_s_tempo_is_not_counted_as_differing`
  - `tests/test_analyze_adopt.py::test_the_check_after_the_adopt_reads_every_title_equal`
  - `tests/test_analyze_adopt.py::test_the_check_counts_only_a_title_whose_own_head_differs`
  - `tests/test_analyze_adopt.py::test_the_check_names_adopt_for_the_bare_titles_a_landing_since_u343_leaves`
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[analyze]`
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[unanalysed]`
  - `tests/test_analyze_check.py::test_a_landing_s_session_names_its_rows`
  - `tests/test_analyze_check.py::test_a_pass_names_its_landing_s_rows_over_the_playlist`
  - `tests/test_analyze_check.py::test_a_row_gone_from_the_collection_is_named_and_does_not_hold_the_visit`
  - `tests/test_analyze_check.py::test_a_row_not_analysed_is_waiting`
  - `tests/test_analyze_check.py::test_a_row_not_analysed_never_reads_suspect_whatever_grid_it_carries`
  - `tests/test_analyze_check.py::test_a_row_whose_id_is_not_text_stays_out_of_every_row_as_it_did`
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_a_variable_grid_on_a_row_marked_dyn_is_done`
  - `tests/test_analyze_check.py::test_an_analysed_row_with_no_head_in_its_title_is_counted_for_adopt_and_never_suspect`
  - ... and 14 more, see the JSON sidecar

Old text:

```
        if any(row.suspect_grid for row in self.rows):
            return SUSPECT
```

New text:

```
        if any(row.suspect_grid for row in self.rows) or self.key_suspect:
            return SUSPECT
```

### `u327.A2_tempo_tolerance`

rekordbox_check: a tempo tolerance of zero beats, so a head one beat off is rewritten and the check counts it

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u327.json`, row `A2_tempo_tolerance`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_analyze_check.py`
- Collected: 185 against a baseline of 185
- Kills: 10 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_that_cannot_be_written_keeps_its_row_s_title_and_is_named`
  - `tests/test_analyze_adopt.py::test_a_full_library_name_apply_after_the_adopt_brings_nothing_back`
  - `tests/test_analyze_adopt.py::test_a_headless_title_is_planned_stamped_apart_from_the_corrected_rows`
  - `tests/test_analyze_adopt.py::test_the_apply_writes_title_title_tag_and_key_tag_and_nothing_else`
  - `tests/test_analyze_adopt.py::test_the_check_after_the_adopt_reads_every_title_equal`
  - `tests/test_analyze_adopt.py::test_the_head_takes_rekordbox_s_key_and_tempo_and_no_other_byte[one-beat-off-left]`
  - `tests/test_analyze_adopt.py::test_the_head_takes_rekordbox_s_key_and_tempo_and_no_other_byte[one-beat-under-left]`
  - `tests/test_analyze_adopt.py::test_the_old_values_are_on_disk_before_the_first_file_is_written`
  - `tests/test_analyze_adopt.py::test_the_plan_shows_each_row_before_and_after_with_its_key_relation_and_tempo`
  - `tests/test_analyze_adopt.py::test_the_record_keeps_every_surface_s_old_value_for_a_restore`

Old text:

```
TEMPO_TOLERANCE = 1

```

New text:

```
TEMPO_TOLERANCE = 0

```

### `u327.A4_tempo_rounds_half_up`

reference_tempo: truncate the column's hundredths, so a dyn average of 124.84 reads 124

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u327.json`, row `A4_tempo_rounds_half_up`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_analyze_check.py`
- Collected: 185 against a baseline of 185
- Kills: 6 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_headless_title_is_planned_stamped_apart_from_the_corrected_rows`
  - `tests/test_analyze_adopt.py::test_leave_holds_a_stamped_row_out_in_the_plan_and_on_the_apply`
  - `tests/test_analyze_adopt.py::test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else`
  - `tests/test_analyze_adopt.py::test_the_plan_shows_each_row_before_and_after_with_its_key_relation_and_tempo`
  - `tests/test_analyze_adopt.py::test_the_tempo_is_the_column_rounded_half_up_or_zero[12450-expected1]`
  - `tests/test_analyze_adopt.py::test_the_tempo_is_the_column_rounded_half_up_or_zero[12484-expected0]`

Old text:

```
    return agreement.round_half_up(value / 100.0) if value > 0 else None
```

New text:

```
    return int(value / 100) if value > 0 else None
```

### `u327.A5_tempo_zero_is_no_answer`

reference_tempo: a BPM of zero reads as a tempo of zero, written into the head

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u327.json`, row `A5_tempo_zero_is_no_answer`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_analyze_check.py`
- Collected: 185 against a baseline of 185
- Kills: 5 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_headless_row_rekordbox_did_not_key_or_time_is_left_and_named`
  - `tests/test_analyze_adopt.py::test_a_missing_key_never_stops_the_tempo_nor_a_missing_tempo_the_key`
  - `tests/test_analyze_adopt.py::test_the_tempo_is_the_column_rounded_half_up_or_zero[0-expected4]`
  - `tests/test_analyze_adopt.py::test_the_tempo_is_the_column_rounded_half_up_or_zero[None-expected5]`
  - `tests/test_analyze_check.py::test_every_row_analysed_right_is_done_and_exits_zero`

Old text:

```
    return agreement.round_half_up(value / 100.0) if value > 0 else None
```

New text:

```
    return agreement.round_half_up(value / 100.0) if value >= 0 else None
```

### `u327.B2_differs_needs_a_title_head`

Row.differs: count a row whose title has no head, so the check names adopt for a row it leaves

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u327.json`, row `B2_differs_needs_a_title_head`
- Moved: the same text, now in src/cratekit/intake/rekordbox_check.py, was in src/cratekit/analysis/rekordbox_check.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_analyze_check.py`
- Collected: 185 against a baseline of 185
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_bare_title_s_tempo_is_not_counted_as_differing`
  - `tests/test_analyze_adopt.py::test_the_check_counts_only_a_title_whose_own_head_differs`
  - `tests/test_analyze_check.py::test_an_analysed_row_with_no_head_in_its_title_is_counted_for_adopt_and_never_suspect`

Old text:

```
        return self.headed and (
```

New text:

```
        return (
```

### `example-binaries-five-row.B1_broken_override_falls_through`

find() returns a broken per-binary override as if it worked, instead of None. The guard exists so a set-but-broken override never falls through to a different binary.

- File: `src/cratekit/core/binaries.py`
- Source: `example-binaries-five-row.json`, row `B1_broken_override_falls_through`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_find_never_raises_because_doctor_reports_on_all_of_them`

Old text:

```
        return override if _executable(Path(override)) else None

```

New text:

```
        return override

```

### `example-binaries-five-row.B3_platform_binary_remedy`

A platform-provided binary reports INSTALL_BINARY instead of UNSUPPORTED_PLATFORM, so the CLI would tell a user to install something the operating system ships.

- File: `src/cratekit/core/binaries.py`
- Source: `example-binaries-five-row.json`, row `B3_platform_binary_remedy`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_the_binary_failures_carry_four_different_remedies`

Old text:

```
            remedy=Remedy.UNSUPPORTED_PLATFORM,

```

New text:

```
            remedy=Remedy.INSTALL_BINARY,

```

### `example-binaries-five-row.B4_unknown_source_remedy`

Collapse the two None-hint cases onto one remedy token, which is the exact distinction the docstring says must not live in a None-check on a second attribute.

- File: `src/cratekit/core/binaries.py`
- Source: `example-binaries-five-row.json`, row `B4_unknown_source_remedy`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_the_binary_failures_carry_four_different_remedies`

Old text:

```
        remedy=Remedy.INSTALL_BINARY if hint is not None else Remedy.INSTALL_BINARY_SOURCE_UNKNOWN,

```

New text:

```
        remedy=Remedy.INSTALL_BINARY,

```

### `example-binaries-five-row.B5_credential_strip`

subprocess_env() stops stripping Cratekit credentials, so every spawned third-party binary receives a copy and the credential reaches a process listing.

- File: `src/cratekit/core/binaries.py`
- Source: `example-binaries-five-row.json`, row `B5_credential_strip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_a_spawned_process_does_not_inherit_an_opted_in_credential`

Old text:

```
        if not key.startswith(secrets.ENV_CREDENTIAL_PREFIX)

```

New text:

```
        if True

```

### `r301.V4_label_shape_loose`

A host label may hold anything, so a scheme, a path or a port passes

- File: `src/cratekit/core/config_schema.py`
- Source: `r301.json`, row `V4_label_shape_loose`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[-bad.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[Identify-EU-west-1.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[https://identify-eu-west-1.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify eu.acrcloud.com]`

Old text:

```
_HOST_LABEL = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
```

New text:

```
_HOST_LABEL = re.compile(r"^.+$")
```

### `r345.A1_colon_required`

backup_remote_name: accept a value with no colon, so a bare folder name names a remote (the brief's row)

- File: `src/cratekit/core/config_schema.py`
- Source: `r345.json`, row `A1_colon_required`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 759 against a baseline of 759
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_the_destination_keys_are_published_for_the_wizard_and_the_verb`

Old text:

```
    if not colon or len(name) < 2:
        return None
```

New text:

```
    if len(name) < 2:
        return None
```

### `r345.A2_single_letter`

backup_remote_name: accept a single character before the colon, so C:/x names a remote called C

- File: `src/cratekit/core/config_schema.py`
- Source: `r345.json`, row `A2_single_letter`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 759 against a baseline of 759
- Kills: 6 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-dest]`

Old text:

```
    if not colon or len(name) < 2:
        return None
```

New text:

```
    if not colon or len(name) < 1:
        return None
```

### `r345.A3_name_shape`

backup_remote_name: drop the rclone name rule, so -gdrive and a trailing space name a remote

- File: `src/cratekit/core/config_schema.py`
- Source: `r345.json`, row `A3_name_shape`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 759 against a baseline of 759
- Kills: 6 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-dest]`

Old text:

```
    if not _RCLONE_REMOTE_NAME.match(name):
        return None
```

New text:

```
    if False:
        return None
```

### `r345.A4_leading_hyphen`

the name rule admits a leading hyphen

- File: `src/cratekit/core/config_schema.py`
- Source: `r345.json`, row `A4_leading_hyphen`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 759 against a baseline of 759
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-dest]`

Old text:

```
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@][\w.+@ -]*(?<! )$")
```

New text:

```
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@-][\w.+@ -]*(?<! )$")
```

### `r345.A5_trailing_space`

the name rule admits a trailing space

- File: `src/cratekit/core/config_schema.py`
- Source: `r345.json`, row `A5_trailing_space`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_backup_cli.py`
- Collected: 759 against a baseline of 759
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-dest]`

Old text:

```
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@][\w.+@ -]*(?<! )$")
```

New text:

```
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@][\w.+@ -]*$")
```

### `r44-a.C3_identity_not_written`

Never write a rule's identity back out, so a saved configuration loses it

- File: `src/cratekit/core/config_schema.py`
- Source: `r44-a.json`, row `C3_identity_not_written`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_prefix_rule_carries_the_identity_of_the_volume_it_points_at`

Old text:

```
        if PREFIX_VOLUME_IDENTITY_KEY in out:
```

New text:

```
        if False:
```

### `r662-a.M2_spelled_path_compared_whole`

the spelled remote is compared whole rather than by its name, so gdrive: beside gdrive destinations reads as a disagreement

- File: `src/cratekit/core/config_schema.py`
- Source: `r662-a.json`, row `M2_spelled_path_compared_whole`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_spelled_backup_remote_that_matches_the_destinations_is_kept[gdrive:]`
  - `tests/test_config.py::test_a_spelled_backup_remote_that_matches_the_destinations_is_kept[gdrive:bucket]`

Old text:

```
    if remote.split(":", 1)[0] == expected:
        return None
    return remote, expected
```

New text:

```
    if remote == expected:
        return None
    return remote, expected
```

### `r662-b.M1b_several_remotes_compared`

M1 again after the round's test: destinations naming several remotes are compared against the spelled remote anyway

- File: `src/cratekit/core/config_schema.py`
- Source: `r662-b.json`, row `M1b_several_remotes_compared`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_no_disagreement_is_read_where_there_is_nothing_to_compare`

Old text:

```
    if len(named) != 1:
        return None
    expected = next(iter(named))
```

New text:

```
    if not named:
        return None
    expected = next(iter(named))
```

### `r662-b.M3b_blank_remote_disagrees`

M3 again after the round's test: a blank spelled remote is no longer treated as unset

- File: `src/cratekit/core/config_schema.py`
- Source: `r662-b.json`, row `M3b_blank_remote_disagrees`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_no_disagreement_is_read_where_there_is_nothing_to_compare`

Old text:

```
    if not isinstance(remote, str) or not remote.strip():
        return None
    named = {
```

New text:

```
    if not isinstance(remote, str):
        return None
    named = {
```

### `u193.M13_default_coefficient`

config: halve the default ceiling

- File: `src/cratekit/core/config_schema.py`
- Source: `u193.json`, row `M13_default_coefficient`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_an_estimate_over_the_call_ceiling_asks_even_under_the_builds_own_line`
  - `tests/test_label_playlists_releases.py::test_the_estimate_is_two_calls_a_release_at_the_configured_pace`
  - `tests/test_provider_gate.py::test_the_ceiling_defaults_to_five_hundred_and_round_trips`

Old text:

```
DEFAULT_PROVIDER_CALLS_PER_COMMAND = 500
```

New text:

```
DEFAULT_PROVIDER_CALLS_PER_COMMAND = 250
```

### `u197-m6.M6_composite`

What the default does hold: default to the alternative, a name the fold leaves alone, so a fresh configuration selects streamrip

- File: `src/cratekit/core/config_schema.py`
- Source: `u197-m6.json`, row `M6_composite`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`
- Collected: 827 against a baseline of 827
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_configured_adapter_name_resolves_through_the_registry`
  - `tests/test_config.py::test_the_vendored_adapter_is_the_default_under_its_neutral_name`

Old text:

```
    adapter: str = "vendored"
```

New text:

```
    adapter: str = "streamrip"
```

### `u197.M2_retired_mapping_empty`

RETIRED_ADAPTER_NAMES: forget the vendored downloader's old key, so an older configuration names an unknown adapter

- File: `src/cratekit/core/config_schema.py`
- Source: `u197.json`, row `M2_retired_mapping_empty`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_adapter_contract.py`
- Collected: 827 against a baseline of 827
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

### `u233.C1_schema_default_moves`

config: labels.offer_per_sweep's default goes from 10 to 12, so the guide's settings table states an old default

- File: `src/cratekit/core/config_schema.py`
- Source: `u233.json`, row `C1_schema_default_moves`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_docs_current.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_the_settings_table_is_the_schema`

Old text:

```
DEFAULT_LABEL_OFFER = 10
```

New text:

```
DEFAULT_LABEL_OFFER = 12
```

### `u233.C2_schema_gains_a_key`

config: LabelsConfig gains a key a person can set, which the guide's settings table has no row for

- File: `src/cratekit/core/config_schema.py`
- Source: `u233.json`, row `C2_schema_gains_a_key`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_docs_current.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_the_settings_table_is_the_schema`

Old text:

```
    new_playlist_age_days: int = DEFAULT_NEW_PLAYLIST_AGE_DAYS

```

New text:

```
    new_playlist_age_days: int = DEFAULT_NEW_PLAYLIST_AGE_DAYS
    sweep_note_days: int = 3

```

### `u299.U12_pin_refusal_remedy`

Config.assert_rekordbox_pin_recorded: the refusal moved behind a local import tells a person to fix the values, not record the pin

- File: `src/cratekit/core/config_schema.py`
- Source: `u299.json`, row `U12_pin_refusal_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_rb_writer_guard.py`
- Collected: 466 against a baseline of 466
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_an_unset_rekordbox_pin_refuses_to_write_with_its_own_remedy`

Old text:

```
                remedy=Remedy.RECORD_REKORDBOX_PIN,
```

New text:

```
                remedy=Remedy.FIX_CONFIG_VALUES,
```

### `r1255.S1_scan_unlisted_as_empty`

scan_log: answer a log it is refused as no record and none unread, the defect itself

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S1_scan_unlisted_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`, `tests/test_doctor.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 867 against a baseline of 867
- Kills: 14 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_session_log_this_account_cannot_list_is_failed_by_its_own_check`
  - `tests/test_doctor.py::test_status_names_a_session_log_it_cannot_list_and_still_reports_the_rest`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_a_listed_log_is_read_a_missing_one_is_no_record_and_a_file_in_its_place_is_unread`
  - `tests/test_session_log_unlisted.py::test_a_log_that_cannot_be_listed_is_the_one_unread_entry_and_its_clause_says_so`
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[closed-detail1-<lambda>-2026-10-20 Tidal playlists 2-so no batch name can be called free]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[committed-unverified-None-<lambda>-session-committed-unverified-cannot vouch that no session ended unresolved]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[open-None-<lambda>-readable2-so whether a run is still open was not established]`
  - `tests/test_session_log_unlisted.py::test_restore_list_and_run_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_check_refuses_an_unknown_landing_naming_the_listing`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_rotation_reads_the_listing_from_the_scan`

Old text:

```
        logger.debug("session log %s could not be listed: %s", directory, exc)
        return (), (directory,)
```

New text:

```
        logger.debug("session log %s could not be listed: %s", directory, exc)
        return (), ()
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

### `r1255.S3_log_file_absent`

_listed: read a log path that is itself a file as not there, so it is no record

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S3_log_file_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_doctor.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_listed_log_is_read_a_missing_one_is_no_record_and_a_file_in_its_place_is_unread`

Old text:

```
        if os.path.lexists(directory):
            raise
        return None
```

New text:

```
        return None
```

### `r1255.S4_under_a_file_unread`

_listed: read a log under a file as there and refused, rather than not there

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S4_under_a_file_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_doctor.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_listed_log_is_read_a_missing_one_is_no_record_and_a_file_in_its_place_is_unread`

Old text:

```
        if os.path.lexists(directory):
            raise
        return None
```

New text:

```
        raise
```

### `r1255.S5_json_filter`

scan_log: read every name in the log as a record, so a stray file reads as an unreadable record

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S5_json_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`, `tests/test_doctor.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 867 against a baseline of 867
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_listed_log_is_read_a_missing_one_is_no_record_and_a_file_in_its_place_is_unread`

Old text:

```
    entries = sorted(directory / name for name in names if fnmatch.fnmatchcase(name, "*.json"))
```

New text:

```
    entries = sorted(directory / name for name in names)
```

### `r1255.S6_records_refuses_unlisted`

records: answer an unlisted log as no session again, so restore list, restore run and session release read it as empty

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S6_records_refuses_unlisted`
- Moved: U953 folded this refusal's refuse call into the _defect builder, so the unlisted test now guards raise _defect and disabling it is the same log read as empty
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_session_cli.py`, `tests/test_restore.py`, `tests/test_doctor.py`
- Collected: 628 against a baseline of 628
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_session_log_that_cannot_be_listed_refuses_the_release_before_its_question`
  - `tests/test_session_log_unlisted.py::test_restore_list_and_run_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`

Old text:

```
    if log_unlisted(unreadable, cfg):
        raise _defect(
```

New text:

```
    if False:
        raise _defect(
```

### `r1255.S7_log_unlisted_predicate`

log_unlisted: never name the unread half as the log, so every refusal counts it as one entry

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S7_log_unlisted_predicate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`
- Collected: 143 against a baseline of 143
- Kills: 11 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_a_log_that_cannot_be_listed_is_the_one_unread_entry_and_its_clause_says_so`
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[closed-detail1-<lambda>-2026-10-20 Tidal playlists 2-so no batch name can be called free]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[committed-unverified-None-<lambda>-session-committed-unverified-cannot vouch that no session ended unresolved]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[open-None-<lambda>-readable2-so whether a run is still open was not established]`
  - `tests/test_session_log_unlisted.py::test_restore_list_and_run_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_check_refuses_an_unknown_landing_naming_the_listing`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_rotation_reads_the_listing_from_the_scan`

Old text:

```
    return log_dir(cfg) in unreadable
```

New text:

```
    return False
```

### `r1255.S8_clause_listing_wording`

unread_clause: word an unlisted log as the count of entries, so a gate sends a person to a damaged file

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S8_clause_listing_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`
- Collected: 116 against a baseline of 116
- Kills: 8 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_log_that_cannot_be_listed_is_the_one_unread_entry_and_its_clause_says_so`
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[closed-detail1-<lambda>-2026-10-20 Tidal playlists 2-so no batch name can be called free]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[committed-unverified-None-<lambda>-session-committed-unverified-cannot vouch that no session ended unresolved]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[open-None-<lambda>-readable2-so whether a run is still open was not established]`
  - `tests/test_session_log_unlisted.py::test_restore_list_and_run_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`

Old text:

```
        return "the session log exists and cannot be listed by this account"
```

New text:

```
        return "the session log holds 1 entry this build cannot read"
```

### `r1255.S9_gate_unlisted_detail`

assert_no_unresolved_session: drop the unlisted flag from the refusal's detail

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S9_gate_unlisted_detail`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 322 against a baseline of 322
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_an_unreadable_record_keeps_its_own_refusal`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[committed-unverified-None-<lambda>-session-committed-unverified-cannot vouch that no session ended unresolved]`

Old text:

```
                "unreadable": [str(path) for path in unreadable],
                "unlisted": log_unlisted(unreadable, cfg),
            },
        )


def resolve_unverified_session(
```

New text:

```
                "unreadable": [str(path) for path in unreadable],
            },
        )


def resolve_unverified_session(
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

### `r375-a.S10_commit_not_persisted_at_once`

record_commit: mark the source in memory and leave the write to the close, so a hard kill after the commit leaves a record that claims none

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S10_commit_not_persisted_at_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 393 against a baseline of 393
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_recorded_commit_is_on_disk_before_the_session_ends`

Old text:

```
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = record.change.merged(change)
    write_record(record, cfg)
```

New text:

```
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = record.change.merged(change)
```

### `r375-a.S11_commit_replaces_the_summary`

record_commit: replace the change summary instead of merging into it, so a second source erases the first one's counts

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S11_commit_replaces_the_summary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 393 against a baseline of 393
- Kills: 3 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_moves_removal_commit_that_lands_and_then_raises_is_still_recorded`
  - `tests/test_write_session.py::test_a_recorded_commit_is_on_disk_before_the_session_ends`
  - `tests/test_write_session.py::test_a_resume_skips_a_committed_source_and_finishes_the_rest`

Old text:

```
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = record.change.merged(change)
```

New text:

```
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = change
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

### `r375-a.S4_abandon_failure_replaces_the_error`

_recorded: re-raise a failed abandonment instead of logging it, so it replaces the error that ended the session

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S4_abandon_failure_replaces_the_error`
- Moved: U953 inlined _recorded into assert_gates, so the abandonment warning is now there, wrapped, and re-raising in its place is the same failed abandonment replacing the error
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 393 against a baseline of 393
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_log_that_cannot_record_the_abandonment_does_not_replace_the_error`

Old text:

```
                    logger.warning(
                        "session %s could not be recorded as abandoned",
                        record.session_id,
                        exc_info=True,
                    )
            raise
```

New text:

```
                    raise
            raise
```

### `r375-a.S5_clean_close_refusal_leaves_it_open`

_recorded: move the clean close out of the try, so a close that refuses leaves the record OPEN with no verb to abandon it

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S5_clean_close_refusal_leaves_it_open`
- Moved: U953 inlined _recorded into assert_gates, so the clean close now sits in that try, and moving it after the except is the same refused close left open
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 393 against a baseline of 393
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_clean_close_that_refuses_ends_abandoned_rather_than_open`

Old text:

```
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
                    )
            raise

```

New text:

```
        except BaseException:
            if record is not None:
                try:
                    close_session(record, resolved, state=SessionState.ABANDONED, now=now)
                except Exception:  # noqa: BLE001 - the session's own error is the one to surface
                    logger.warning(
                        "session %s could not be recorded as abandoned",
                        record.session_id,
                        exc_info=True,
                    )
            raise
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

### `r375-a.S7_close_drops_the_identity_seam`

_recorded: do not forward the identity provider to the gated close, so it asserts the volume through this machine's default

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S7_close_drops_the_identity_seam`
- Moved: U953 inlined _recorded into assert_gates, so the clean close is now there and not forwarding identity_provider to it is the same dropped seam
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 393 against a baseline of 393
- Kills: 4 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_recorded_commit_is_on_disk_before_the_session_ends`
  - `tests/test_write_session.py::test_a_supplied_holder_reaches_the_record_as_well_as_the_lock`
  - `tests/test_write_session.py::test_the_record_is_the_gates_own_workflow_actor_and_acknowledgment`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
                    intent=intent,
                    identity_provider=identity_provider,
                    mount_enumerator=mount_enumerator,
                    now=now,
                )
        except BaseException:
```

New text:

```
                    intent=intent,
                    mount_enumerator=mount_enumerator,
                    now=now,
                )
        except BaseException:
```

### `r375-a.S8_record_names_no_actor`

_recorded: record no actor, so the log cannot say who acknowledged the backup this write ran behind

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S8_record_names_no_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 393 against a baseline of 393
- Kills: 2 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts`
  - `tests/test_write_session.py::test_the_record_is_the_gates_own_workflow_actor_and_acknowledgment`

Old text:

```
        actor=acknowledgment.actor,
```

New text:

```
        actor=None,
```

### `r375-a.S9_record_names_no_acknowledgment`

_recorded: record no acknowledgment instant

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S9_record_names_no_acknowledgment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 393 against a baseline of 393
- Kills: 2 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts`
  - `tests/test_write_session.py::test_the_record_is_the_gates_own_workflow_actor_and_acknowledgment`

Old text:

```
        acknowledged_at=acknowledgment.recorded_at.isoformat(),
```

New text:

```
        acknowledged_at=None,
```

### `r501-a.S1_verify_state_guard`

session.mark_import_verified: drop the refusal of any state but awaiting-import, so any record can be marked proven

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S1_verify_state_guard`
- Moved: U953 folded this refusal's refuse call into the _defect builder, so the state test now guards raise _defect and disabling it is the same unguarded mark
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_only_a_run_waiting_on_an_import_has_one_to_verify`

Old text:

```
    if record.state is not SessionState.AWAITING_IMPORT:
        raise _defect(
```

New text:

```
    if False:
        raise _defect(
```

### `r501-a.S2_excusal_capture`

session.owes_only_deferred_routing: drop the no capture condition, so a run holding a capture is excused from the cutover precheck

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S2_excusal_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_holds_a_capture[holding-a-capture]`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.state is SessionState.OPEN
        and IMPORT_VERIFIED_KEY in record.detail
```

### `r501-a.S3_excusal_proof`

session.owes_only_deferred_routing: drop the proof condition, so any open run with no capture is excused, a crashed landing included

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S3_excusal_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 5 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_open_run_blocks_the_flip`
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_doctor_reads_a_proven_run_as_proven_and_not_as_in_progress`
  - `tests/test_intake_imported.py::test_the_precheck_refuses_an_open_run_with_no_proof_recorded`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
```

### `r501-a.S4_excusal_state`

session.owes_only_deferred_routing: drop the open state condition, so a committed-unverified run carrying the key is excused

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S4_excusal_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_holds_a_capture[not-open]`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

### `r598-a.A5_holder_never_recorded`

open_session: drop the holder instead of recording it, so no record is ever provably orphaned and a hard kill is a dead end again

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A5_holder_never_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 8 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_release_that_only_abandons_is_a_change_and_passes_the_contract`
  - `tests/test_write_session.py::test_a_supplied_holder_reaches_the_record_as_well_as_the_lock`
  - `tests/test_write_session.py::test_abandon_orphaned_sessions_ends_only_the_orphans`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`
  - `tests/test_write_session.py::test_the_sweep_ends_only_the_orphans_it_was_shown`

Old text:

```
        detail={HOLDER_KEY: holder.to_json()} if holder is not None else {},
```

New text:

```
        detail={},
```

### `r598-a.A6_record_holder_is_a_second_lookup`

assert_gates: record current_holder() in the record rather than the claimant the lock took, so a supplied holder splits the two copies

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A6_record_holder_is_a_second_lookup`
- Moved: U953 inlined _recorded into assert_gates, so the record is now opened there with the claimant directly, and a second current_holder() lookup in its place is the same split copy
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_supplied_holder_reaches_the_record_as_well_as_the_lock`

Old text:

```
                holder=claimant,
                now=now,
```

New text:

```
                holder=current_holder(),
                now=now,
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

### `r1924.C1_refusal`

perform_restore: answer ok whatever the files did

- File: `src/cratekit/session/restore_cli.py`
- Source: `r1924.json`, row `C1_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_dry_run_finds_a_file_gone_and_refuses_as_the_run_would`
  - `tests/test_restore_tags.py::test_a_file_gone_since_the_adopt_is_named`
  - `tests/test_restore_tags.py::test_a_file_that_cannot_be_written_is_named_and_the_run_is_not_ok`
  - `tests/test_restore_tags.py::test_a_file_that_does_not_read_back_is_named`

Old text:

```
    if report.outcome is None or not report.outcome.file_tags.unwritten:
```

New text:

```
    if True:
```

### `r1924.C2_totals`

_performed: carry no file counts in the answer

- File: `src/cratekit/session/restore_cli.py`
- Source: `r1924.json`, row `C2_totals`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 9 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_dry_run_puts_no_file_back`
  - `tests/test_restore_tags.py::test_a_file_that_cannot_be_written_is_named_and_the_run_is_not_ok`
  - `tests/test_restore_tags.py::test_a_later_adopt_that_wrote_files_and_no_rows_has_its_files_put_back[abandoned]`
  - `tests/test_restore_tags.py::test_a_later_adopt_that_wrote_files_and_no_rows_has_its_files_put_back[open]`
  - `tests/test_restore_tags.py::test_a_later_adopt_the_restore_discards_puts_its_files_back_too`
  - `tests/test_restore_tags.py::test_a_restore_of_the_later_adopt_leaves_the_earlier_one_s_files`
  - `tests/test_restore_tags.py::test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head`
  - `tests/test_restore_tags.py::test_a_restore_puts_the_row_the_title_tag_and_the_key_tag_back`
  - `tests/test_restore_tags.py::test_a_session_with_no_kept_tags_restores_as_before`

Old text:

```
        totals["file_tags"] = outcome.file_tags.to_json()
```

New text:

```
        totals["file_tags"] = {}
```

### `r1924.C3_dry_run_message`

_tags_unwritten: a dry run's refusal says the session was restored

- File: `src/cratekit/session/restore_cli.py`
- Source: `r1924.json`, row `C3_dry_run_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_dry_run_finds_a_file_gone_and_refuses_as_the_run_would`

Old text:

```
    if outcome.dry_run:
        return CratekitError(
```

New text:

```
    if False:
        return CratekitError(
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1272 against a baseline of 1272
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
- Collected: 1113 against a baseline of 1113
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

### `u259.M10_chunk_size`

_CHUNK: read 50 IDs to a statement rather than 500, so a scope's statements grow with it

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u259.json`, row `M10_chunk_size`
- Moved: U331's c222c10e, which routes every feature package's reach into core through a listed module, moved analysis/rekordbox_check.py to intake/rekordbox_check.py; the line also stands in write/row_defaults.py, a twin, so the after pass of killset rows could not place it, but this is the chunk rows_by_id reads its IDs by, the same constant narrowed the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[analyze]`

Old text:

```
_CHUNK = 500
```

New text:

```
_CHUNK = 50
```

