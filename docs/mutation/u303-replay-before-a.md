# Mutation table: u303-replay-before-a

Measured by `scripts/mutate.py` on 2026-11-22 23:38 UTC, branch `HEAD` at `fd8173d3`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 64.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 48, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `../known-replay.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 152 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r239-b.S5_converge_key_off` | `src/cratekit/cli/converge.py` | user | 7 file(s) | 733 | 2 | killed |
| `r685-b.C1_converge_opens_before_it_reads` | `src/cratekit/cli/converge.py` | user | 1 file(s) | 108 | 1 | killed |
| `r685-b.C2_converge_lets_the_refusal_escape` | `src/cratekit/cli/converge.py` | user | 1 file(s) | 108 | 1 | killed |
| `u89.C1_converge_threshold` | `src/cratekit/cli/converge.py` | user | 1 file(s) | 197 | 2 | killed |
| `r235-a.M10_verb_guard_removed` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 1 | killed |
| `r235-b.M15_first_of_several_roots` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 1 | killed |
| `r235-b.M16_native_tree_offered_again` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 2 | killed |
| `r235-b.M19_unready_library_asked` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 6 | killed |
| `r235-b.M20_refusal_without_the_table` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 5 | killed |
| `r235-b.M21_digest_blind_to_the_plan` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 1 | killed |
| `r787.V1_verb_own_list` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 1 | killed |
| `r787.V2_undeclared_step_routing_only` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 1 | killed |
| `r787.V3_catalogue_refusal_loses_set` | `src/cratekit/cli/cutover.py` | user | 1 file(s) | 40 | 1 | killed |
| `r-1.E1_dispatch_impl` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.E2_config_inside_checkout` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T10_no_yaml_falls_back` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T11_unreadable_config_falls_back` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 22933 | 0 (promoted) | zero |
| `r-1.T12_caller_ignores_unknown` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 2 | killed |
| `r-1.T13_missing_other_hook` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 2 | killed |
| `r-1.T14_unreadable_other_hook` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 22933 | 0 (promoted) | zero |
| `r-1.T15_other_dispatch` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T16_same_configuration` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T17_install_config_flag` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T18_remedy_floor` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T19_remedy_reads_config` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T1_manual_skip` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T20_stage_parameter` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 3 | killed |
| `r-1.T21_ok_names_others` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T22_pre_commit_floor` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 13 | killed |
| `r-1.T23_alias_value` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T2_alias_map` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 2 | killed |
| `r-1.T3_default_install_types` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T4_default_stages` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T5_hook_stages` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 12 | killed |
| `r-1.T6_unknown_stage` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 2 | killed |
| `r-1.T7_dedupe` | `src/cratekit/cli/doctor.py` | maintainer | 4 file(s) | 1673 | 2 | killed |
| `r-1.T8_not_a_mapping` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r-1.T9_yaml_error_falls_back` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `r1255.D1_doctor_branches_on_the_scan` | `src/cratekit/cli/doctor.py` | user | 2 file(s) | 438 | 1 | killed |
| `r1255.D2_status_names_the_log` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `r1255.D3_status_guard_precise` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `r372-b.B1_doctor_majority_is_info` | `src/cratekit/cli/doctor.py` | user | 3 file(s) | 494 | 2 | killed |
| `r372-b.B2_doctor_minority_fails` | `src/cratekit/cli/doctor.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-b.B4_doctor_reads_before_the_volume_checks` | `src/cratekit/cli/doctor.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-b.B5_doctor_opens_the_live_path` | `src/cratekit/cli/doctor.py` | user | 3 file(s) | 494 | 5 | killed |
| `r598-b.B6_doctor_clause_dropped` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `r757-c2.D1_due_a_day_late` | `src/cratekit/cli/doctor.py` | maintainer | 4 file(s) | 758 | 1 | killed |
| `r787.D1_doctor_own_list` | `src/cratekit/cli/doctor.py` | user | 12 file(s) | 2223 | 4 | killed |
| `r787.D2_set_guard_removed` | `src/cratekit/cli/doctor.py` | user | 12 file(s) | 2223 | 1 | killed |
| `r787.D3_source_guard_removed` | `src/cratekit/cli/doctor.py` | user | 12 file(s) | 2223 | 1 | killed |
| `u132.D1_doctor_behind` | `src/cratekit/cli/doctor.py` | user | 12 file(s) | 2223 | 2 | killed |
| `u132.D2_doctor_defect` | `src/cratekit/cli/doctor.py` | user | 12 file(s) | 2223 | 1 | killed |
| `u159.M10_unread_reads_none_published` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u159.M8_behind_reads_current` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 4 | killed |
| `u170.D1_kept_folded` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.D2_status_week` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.D3_open_runs_short` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.D4_line_dropped` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1704 | 3 | killed |
| `u181.D1_extras_row_never_ok` | `src/cratekit/cli/doctor.py` | user | 2 file(s) | 1414 | 2 | killed |
| `u181.D2_files_offered_reinstall` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u181.D3_release_form_dropped` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 3 | killed |
| `u181.D4_release_form_no_vocals` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 2 | killed |
| `u181.D5_upgrade_never_adds_vocals` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u181.D6_upgrade_always_adds_vocals` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 2 | killed |
| `u181.D7_scored_probe_false` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D1_volume_not_established` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D2_unreadable_is_a_note` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D3_remedy_chosen_here` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D4_expired_read_as_valid` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D5_wall_clock` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D6_hours_coefficient` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D7_rule_not_named` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u184.D8_check_unlisted` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 6 | killed |
| `u185.D1_push_newer_warns` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 2 | killed |
| `u185.D2_hidden_entries` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 4 | killed |
| `u185.D3_unread_folder` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 2 | killed |
| `u186.N1_note_age` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.N2_note_fails` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 34 | 2 | killed |
| `u186.N3_note_unreadable_dropped` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 34 | 2 | killed |
| `u206.M24_doctor_set_aside_unnamed` | `src/cratekit/cli/doctor.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u211.C1_doctor_closed_is_a_note` | `src/cratekit/cli/doctor.py` | user | 2 file(s) | 466 | 1 | killed |
| `u211.C2_doctor_paths_take_no_copy` | `src/cratekit/cli/doctor.py` | user | 3 file(s) | 517 | 1 | killed |
| `u224.M10_refused_backups_read_no_push` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M1_found_ignored` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 7 | killed |
| `u224.M2_unread_place_dropped` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M3_broken_installed_probe_silent` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M4_unread_support_read_absent` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M5_refused_stat_read_absent` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 4 | killed |
| `u224.M6_unread_folded_into_not_installed` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 4 | killed |
| `u224.M7_install_signals_always_asked` | `src/cratekit/cli/doctor.py` | maintainer | 1 file(s) | 417 | 1 | killed |
| `u224.M8_default_probe_empty` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u224.M9_path_through_a_file_unread` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u263.D21_doctor_names_verbs` | `src/cratekit/cli/doctor.py` | user | 1 file(s) | 417 | 1 | killed |
| `u27-reports-round-1.D2_required_gate` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `u27-reports-round-1.D3_trash_remedy` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `u27-reports-round-2.D1_probe_creates` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `u27-reports-round-3-fixes.F3_trash_absent_is_a_failure` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `u27-round-8-independent.D1_finding_no_classification` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 22933 | 0 (promoted) | zero |
| `u27-round-8-independent.D2_finding_no_remedy_override` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 22933 | 0 (promoted) | zero |
| `u27-round-8-independent.D4_composite_reason` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 22933 | 0 (promoted) | zero |
| `u27-round-8-independent.E1_mount_detail_swapped` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `u27-round-8-independent.E2_identity_verdict_green` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 3 | killed |
| `u27-round-8-independent.E3_found_at_dropped` | `src/cratekit/cli/doctor.py` | user | 4 file(s) | 1673 | 1 | killed |
| `u97-b.B1_doctor_routes_the_wrong_credential_token` | `src/cratekit/cli/doctor.py` | user | 3 file(s) | 1588 | 1 | killed |
| `r388-b.M12_listing_steps_say_take_a_backup` | `src/cratekit/cli/exit_codes.py` | user | 4 file(s) | 684 | 2 | killed |
| `r388-c.M13_credential_step_dropped` | `src/cratekit/cli/exit_codes.py` | user | 4 file(s) | 684 | 2 | killed |
| `r388-d.M16_named_stamp_step_dropped_remeasured` | `src/cratekit/cli/exit_codes.py` | user | 4 file(s) | 684 | 2 | killed |
| `u235.T1_tail_back_to_sixteen_bits` | `src/cratekit/cli/output.py` | user | 1 file(s) | 997 | 2 | killed |
| `u235.T2_tail_thirty_two_bits` | `src/cratekit/cli/output.py` | user | 1 file(s) | 997 | 1 | killed |
| `u235.T3_tail_fifty_six_bits` | `src/cratekit/cli/output.py` | user | 1 file(s) | 997 | 1 | killed |
| `u235.T4_tail_from_the_instant` | `src/cratekit/cli/output.py` | user | 1 file(s) | 997 | 1 | killed |
| `u235.T5_instant_ignored` | `src/cratekit/cli/output.py` | maintainer | 1 file(s) | 997 | 2 | killed |
| `u235.T6_stamp_loses_its_colons` | `src/cratekit/cli/output.py` | user | 1 file(s) | 997 | 2 | killed |
| `u298.H1_config_cause_reason` | `src/cratekit/cli/output.py` | user | 2 file(s) | 341 | 3 | killed |
| `u298.H2_config_cause_origin` | `src/cratekit/cli/output.py` | user | 2 file(s) | 341 | 3 | killed |
| `u298.H3_declared_gate_by_name` | `src/cratekit/cli/output.py` | user | 1 file(s) | 100 | 2 | killed |
| `u298.H4_confirm_gate_refusal` | `src/cratekit/cli/output.py` | user | 1 file(s) | 100 | 1 | killed |
| `u298.H5_approving_actor_default` | `src/cratekit/cli/output.py` | user | 1 file(s) | 100 | 1 | killed |
| `u298.H6_no_job_id_string` | `src/cratekit/cli/output.py` | user | 1 file(s) | 100 | 2 | killed |
| `r83.P1_flush` | `src/cratekit/cli/prompt.py` | user | 1 file(s) | 417 | 1 | killed |
| `r83.P2_nothing_entered_raise` | `src/cratekit/cli/prompt.py` | user | 1 file(s) | 417 | 2 | killed |
| `a32.R1_gate_not_explicit` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1056 | 5 | killed |
| `r185-r246-author.D2_cloud_gate_restored` | `src/cratekit/cli/registry.py` | user | 44 file(s) | 5993 | 2 | killed |
| `r312.R1_summary_promises_a_replace` | `src/cratekit/cli/registry.py` | user | 44 file(s) | 5993 | 1 | killed |
| `r372-b.B12_verb_does_not_declare_the_check` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 1465 | 1 | killed |
| `r424.A1_writes_narrowed` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1122 | 2 | killed |
| `r424.A2_cloud_gate_absent` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1122 | 2 | killed |
| `r424.A3_rekordbox_checks` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 1539 | 1 | killed |
| `r424.A4_library_mounted` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 1539 | 1 | killed |
| `r424.A5_summary_both_ways` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1122 | 1 | killed |
| `r770-d.C8_native_gate_answered_inline` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1044 | 9 | killed |
| `r773-b.R1_doctor_check_not_declared` | `src/cratekit/cli/registry.py` | maintainer | 1 file(s) | 97 | 1 | killed |
| `r923.N20_gate_takes_inline_answer` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 53 | 5 | killed |
| `u103-b.M1_identify_declared_adjudicating` | `src/cratekit/cli/registry.py` | maintainer | 2 file(s) | 1104 | collection error | collect-error |
| `u129-author.A10_export_set_without_library_mounted` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 24 | 1 | killed |
| `u129-author.A11_export_archive_without_library_mounted` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 24 | 1 | killed |
| `u129-author.A9_land_without_provider_check` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 24 | 1 | killed |
| `u263.D22_restamp_declares` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1414 | 1 | killed |
| `u27-adopt-apply-author.R1_marker_restored` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 1710 | collection error | collect-error |
| `u27-reports-round-1.R1_delete_review_precondition` | `src/cratekit/cli/registry.py` | user | 14 file(s) | 3872 | 2 | killed |
| `u27-restore-cli-independent.I_H1_the_landed_verb_keeps_its_marker` | `src/cratekit/cli/registry.py` | maintainer | 2 file(s) | 1095 | collection error | collect-error |
| `u28-skills-independent.R1_planned_in_restored` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 993 | collection error | collect-error |
| `u39-author-full.W2_unreachable_gate_restored` | `src/cratekit/cli/registry.py` | user | 19 file(s) | 4049 | 1 | killed |
| `u40-author-full.R3_ungated` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 997 | 1 | killed |
| `u40-author-full.R5_row_unclaimed` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1005 | 5 | killed |
| `u40-author-full.R6_row_still_cut` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1005 | 1 | killed |
| `u40-author-round-2.R8_not_long_running` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 18 | collection error | collect-error |
| `u42-author-round-2.R2_handler_lookup_imports` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 997 | 1 | killed |
| `u42-author.R1_planned_marker_returns` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 1026 | collection error | collect-error |
| `u43-author-light.R1_marker_restored` | `src/cratekit/cli/registry.py` | maintainer | 21 file(s) | 4181 | collection error | collect-error |
| `u44-author.D1_registry_drops_long_running` | `src/cratekit/cli/registry.py` | maintainer | 22 file(s) | 4257 | collection error | collect-error |
| `u45-round-1.V3_marker_restored` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 4377 | collection error | collect-error |
| `u45-round-1.V5_module_toggle_dropped` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 4380 | collection error | collect-error |
| `u69-b.M20_registry_schema` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1069 | 43 | killed |
| `u72.M8_registry_digest_source` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 48 | 7 | killed |
| `u91.G1_registry_xml` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1194 | 1 | killed |
| `u96-b.B1_no_library_check_declared` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1095 | 1 | killed |
| `u27-reports-round-1.S1_limit_floor` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.S2_truncation_row` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-1.S3_summary_total` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-2.S5_handler_key_wrong` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-3-fixes.F1_as_of_falsiness` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-3-fixes.F5_gap_row_flood` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `r679-a.E1_cli_offers_every_verdict` | `src/cratekit/cli/review.py` | user | 3 file(s) | 879 | 1 | killed |
| `r679-a.E2_listing_drops_the_actor` | `src/cratekit/cli/review.py` | user | 3 file(s) | 879 | 1 | killed |
| `r790-d.V1_group_page_refusal` | `src/cratekit/cli/review.py` | user | 2 file(s) | 201 | 2 | killed |

## Zero rows and what they owe

- `r-1.T11_unreadable_config_falls_back` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r-1.T14_unreadable_other_hook` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.D1_finding_no_classification` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.D2_finding_no_remedy_override` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.D4_composite_reason` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r239-b.S5_converge_key_off`

converge passes unlock=False again, so every native tree reads not compared on a real library

- File: `src/cratekit/cli/converge.py`
- Source: `r239-b.json`, row `S5_converge_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 733 against a baseline of 733
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`

Old text:

```
            handle = rb_writer.open_db(cfg=cfg)
```

New text:

```
            handle = rb_writer.open_db(cfg=cfg, unlock=False)
```

### `r685-b.C1_converge_opens_before_it_reads`

Converge opens the database before reading the declaration, the order the review found

- File: `src/cratekit/cli/converge.py`
- Source: `r685-b.json`, row `C1_converge_opens_before_it_reads`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild.py::test_an_active_taxonomy_that_cannot_be_read_is_not_compared_and_opens_nothing`

Old text:

```
            declared = active_taxonomy.load(cfg)
            handle = rb_writer.open_db(cfg=cfg)

```

New text:

```
            handle = rb_writer.open_db(cfg=cfg)
            declared = active_taxonomy.load(cfg)

```

### `r685-b.C2_converge_lets_the_refusal_escape`

The declaration is read outside the try, so a refusal escapes instead of reading NOT COMPARED

- File: `src/cratekit/cli/converge.py`
- Source: `r685-b.json`, row `C2_converge_lets_the_refusal_escape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild.py::test_an_active_taxonomy_that_cannot_be_read_is_not_compared_and_opens_nothing`

Old text:

```
        handle = declared = None
        try:
            declared = active_taxonomy.load(cfg)
            handle = rb_writer.open_db(cfg=cfg)

```

New text:

```
        handle = declared = None
        declared = active_taxonomy.load(cfg)
        try:
            handle = rb_writer.open_db(cfg=cfg)

```

### `u89.C1_converge_threshold`

converge _compare: pass None instead of the loaded cut

- File: `src/cratekit/cli/converge.py`
- Source: `u89.json`, row `C1_converge_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_is_converge_not_comparing_rather_than_a_match`
  - `tests/test_routing_workers.py::test_converge_compares_the_vocal_sub_once_calibrated`

Old text:

```
            vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
```

New text:

```
            vocal_threshold=None,
```

### `r235-a.M10_verb_guard_removed`

the revert verb no longer asks before the gate, leaving only the library's check after the approval

- File: `src/cratekit/cli/cutover.py`
- Source: `r235-a.json`, row `M10_verb_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_revert_after_a_native_write_refuses_and_the_tree_stays_native`

Old text:

```
    tree_registry.assert_revertible(cfg, tree_id)
    item = {**_recorded(standing), "registry": str(tree_registry.path_for(cfg))}
```

New text:

```
    item = {**_recorded(standing), "registry": str(tree_registry.path_for(cfg))}
```

### `r235-b.M15_first_of_several_roots`

more than one root no longer refuses, the first is adopted

- File: `src/cratekit/cli/cutover.py`
- Source: `r235-b.json`, row `M15_first_of_several_roots`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_two_roots_of_one_name_are_refused`

Old text:

```
    if len(roots) == 1:
        return roots[0]
```

New text:

```
    if len(roots) >= 1:
        return roots[0]
```

### `r235-b.M16_native_tree_offered_again`

the verb no longer answers a tree already native before it asks

- File: `src/cratekit/cli/cutover.py`
- Source: `r235-b.json`, row `M16_native_tree_offered_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_tree_already_native_records_nothing_and_asks_nothing`
  - `tests/test_cutover_cli.py::test_two_cutovers_offered_before_either_was_approved_record_one`

Old text:

```
    if standing is not None and standing.mode == tree_registry.Mode.DATABASE:
        return ctx.envelope(
            data=_digested("tree.cutover", _recorded(standing), {"recorded": False}),
```

New text:

```
    if False:
        return ctx.envelope(
            data=_digested("tree.cutover", _recorded(standing), {"recorded": False}),
```

### `r235-b.M19_unready_library_asked`

a library that fails its precheck is offered the plan instead of being refused

- File: `src/cratekit/cli/cutover.py`
- Source: `r235-b.json`, row `M19_unready_library_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 6 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_an_empty_export_is_no_export`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_leave_intake_xml-cutover-xml-pending-no-pending-intake-xml]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_open_a_run-cutover-open-run-no-open-run]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_export-cutover-export-missing-fresh-export]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_snapshot-cutover-snapshot-missing-verified-snapshot]`
  - `tests/test_cutover_cli.py::test_two_failing_prechecks_are_both_named_on_one_run`

Old text:

```
    results = tree_registry.cutover_precheck(cfg, export=export)
    _refuse_unready(results)
```

New text:

```
    results = tree_registry.cutover_precheck(cfg, export=export)
```

### `r235-b.M20_refusal_without_the_table`

the precheck refusal no longer carries every check's result

- File: `src/cratekit/cli/cutover.py`
- Source: `r235-b.json`, row `M20_refusal_without_the_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 5 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_leave_intake_xml-cutover-xml-pending-no-pending-intake-xml]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_open_a_run-cutover-open-run-no-open-run]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_export-cutover-export-missing-fresh-export]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_snapshot-cutover-snapshot-missing-verified-snapshot]`
  - `tests/test_cutover_cli.py::test_two_failing_prechecks_are_both_named_on_one_run`

Old text:

```
                detail={**cause.detail, "precheck": _precheck_rows(results)},
```

New text:

```
                detail=dict(cause.detail),
```

### `r235-b.M21_digest_blind_to_the_plan`

the digest covers the kind of plan and not its item, so a root that changed leaves the approval standing

- File: `src/cratekit/cli/cutover.py`
- Source: `r235-b.json`, row `M21_digest_blind_to_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_root_that_changed_after_the_offer_makes_the_approval_stale`

Old text:

```
        "digest": digest_of({"kind": kind, "items": [item]}),
```

New text:

```
        "digest": digest_of({"kind": kind}),
```

### `r787.V1_verb_own_list`

derivation_source keeps a list of its own, the routing tree and intake tree spelled inline, instead of asking cutover_trees

- File: `src/cratekit/cli/cutover.py`
- Source: `r787.json`, row `V1_verb_own_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_and_the_verb_read_one_set_of_cutover_trees`

Old text:

```
    if tree_id in accepted:
        return tree_registry.DerivationSource.TAXONOMY
```

New text:

```
    if tree_id in (declared.tree.id, declared.intake.id):
        return tree_registry.DerivationSource.TAXONOMY
```

### `r787.V2_undeclared_step_routing_only`

the undeclared refusal's step names the routing tree alone rather than the set

- File: `src/cratekit/cli/cutover.py`
- Source: `r787.json`, row `V2_undeclared_step_routing_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_tree_the_taxonomy_does_not_declare_is_refused`

Old text:

```
            f"name a tree a cutover records, which this library declares as "
            f"{', '.join(repr(t) for t in named)}",
```

New text:

```
            f"name a tree a cutover records, which this library declares as "
            f"{declared.tree.id!r}",
```

### `r787.V3_catalogue_refusal_loses_set`

the catalogue refusal carries the registry's detail alone, without the set a cutover accepts

- File: `src/cratekit/cli/cutover.py`
- Source: `r787.json`, row `V3_catalogue_refusal_loses_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_the_catalogue_tree_is_refused_as_not_rebuildable`

Old text:

```
                detail={
                    **cause.detail,
                    "cutover_trees": sorted(tree_registry.cutover_trees(declared)),
                },
```

New text:

```
                detail={**cause.detail},
```

### `r-1.E1_dispatch_impl`

Existing guard, sample: drop the requirement that the hook invokes hook-impl

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `E1_dispatch_impl`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `E2_config_inside_checkout`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T10_no_yaml_falls_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

### `r-1.T11_unreadable_config_falls_back`

A configuration that cannot be read falls back to the pre-commit floor instead of a sentence

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T11_unreadable_config_falls_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        return (
            (),
            f"{config_file} could not be read ({exc})",
            access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
        )

```

New text:

```
        return ("pre-commit",), None, None

```

### `r-1.T12_caller_ignores_unknown`

The check ignores an unknown configuration and reports on no extra types

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T12_caller_ignores_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T13_missing_other_hook`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

### `r-1.T14_unreadable_other_hook`

A configured hook file this account cannot read is skipped instead of reported unknown

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T14_unreadable_other_hook`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        except (OSError, UnicodeDecodeError) as exc:
            # The same split the pre-commit hook makes above:
```

New text:

```
        except (OSError, UnicodeDecodeError) as exc:
            continue
            # The same split the pre-commit hook makes above:
```

### `r-1.T15_other_dispatch`

A configured hook that does not dispatch for its own stage is not reported

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T15_other_dispatch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T16_same_configuration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T17_install_config_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T18_remedy_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T19_remedy_reads_config`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

### `r-1.T1_manual_skip`

Stop skipping the manual stage, so a manual-only hook reads as an unknown stage

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T1_manual_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text5-expected5]`

Old text:

```
        if hook_type == "manual":  # run by hand, never by git
            continue

```

New text:

```
(empty)
```

### `r-1.T20_stage_parameter`

The dispatch check ignores the hook type it was asked about and always wants pre-commit

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T20_stage_parameter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T21_ok_names_others`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T22_pre_commit_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

### `r-1.T23_alias_value`

Map merge-commit to a realistic nearby wrong hook, pre-commit

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T23_alias_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text4-expected4]`

Old text:

```
"merge-commit": "pre-merge-commit"
```

New text:

```
"merge-commit": "pre-commit"
```

### `r-1.T2_alias_map`

Stop mapping the legacy stage spellings (commit, push, merge-commit) to their hook types

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T2_alias_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_stages: [push]\nrepos: []\n-expected3]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text4-expected4]`

Old text:

```
hook_type = _STAGE_ALIASES.get(stage, stage) if isinstance(stage, str) else None
```

New text:

```
hook_type = stage if isinstance(stage, str) else None
```

### `r-1.T3_default_install_types`

Ignore default_install_hook_types when deriving the needed hook types

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T3_default_install_types`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_install_hook_types: [pre-push]\nrepos: []\n-expected2]`

Old text:

```
    named.extend(document.get("default_install_hook_types") or [])

```

New text:

```
(empty)
```

### `r-1.T4_default_stages`

Ignore default_stages when deriving the needed hook types

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T4_default_stages`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[default_stages: [push]\nrepos: []\n-expected3]`

Old text:

```
    named.extend(document.get("default_stages") or [])

```

New text:

```
(empty)
```

### `r-1.T5_hook_stages`

Ignore every hook's own stages, the reading that finds this repository's commit-msg stage

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T5_hook_stages`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

### `r-1.T6_unknown_stage`

Skip an unknown stage instead of refusing the configuration

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T6_unknown_stage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[text0-'on-commit']`
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[text1-installs no hook for]`

Old text:

```
        if hook_type not in _HOOK_TYPES:
            return (
                (),
                f"{config_file} names a stage pre-commit installs no hook for, {stage!r}",
                None,
            )

```

New text:

```
        if hook_type not in _HOOK_TYPES:
            continue

```

### `r-1.T7_dedupe`

Append a type every time it is named rather than once

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T7_dedupe`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text4-expected4]`
  - `tests/test_doctor.py::test_the_hook_types_a_configuration_needs[text6-expected6]`

Old text:

```
        if hook_type not in types:
            types.append(hook_type)

```

New text:

```
        types.append(hook_type)

```

### `r-1.T8_not_a_mapping`

Drop the guard refusing a configuration whose top level is not a mapping

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T8_not_a_mapping`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_this_cannot_understand_is_a_sentence[- just\n- a list\n-is not a pre-commit configuration]`

Old text:

```
    if not isinstance(document, dict):
        return (), f"{config_file} is not a pre-commit configuration", None

```

New text:

```
(empty)
```

### `r-1.T9_yaml_error_falls_back`

A configuration that does not parse falls back to the pre-commit floor instead of a sentence

- File: `src/cratekit/cli/doctor.py`
- Source: `r-1.json`, row `T9_yaml_error_falls_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

### `r1255.D1_doctor_branches_on_the_scan`

doctor _check_unresolved_session: never branch on the listing, so the log directory is named as an unreadable record

- File: `src/cratekit/cli/doctor.py`
- Source: `r1255.json`, row `D1_doctor_branches_on_the_scan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_session_log_unlisted.py`
- Collected: 438 against a baseline of 438
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

### `r1255.D2_status_names_the_log`

status _source_findings: never name an unlisted log, so a refused source reads as none in flight

- File: `src/cratekit/cli/doctor.py`
- Source: `r1255.json`, row `D2_status_names_the_log`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_status_names_a_session_log_it_cannot_list_and_still_reports_the_rest`

Old text:

```
    if session.log_unlisted(unreadable, cfg):
        # A LOG NOBODY COULD LIST IS SAID
```

New text:

```
    if False:
        # A LOG NOBODY COULD LIST IS SAID
```

### `r1255.D3_status_guard_precise`

status _source_findings: name any unread entry as an unlisted log, so one damaged record hides every source

- File: `src/cratekit/cli/doctor.py`
- Source: `r1255.json`, row `D3_status_guard_precise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_status_reads_one_damaged_record_as_a_record_not_as_an_unlisted_log`

Old text:

```
    if session.log_unlisted(unreadable, cfg):
        # A LOG NOBODY COULD LIST IS SAID
```

New text:

```
    if unreadable:
        # A LOG NOBODY COULD LIST IS SAID
```

### `r372-b.B1_doctor_majority_is_info`

_check_paths_resolved: a majority is a note, so doctor stays green over it

- File: `src/cratekit/cli/doctor.py`
- Source: `r372-b.json`, row `B1_doctor_majority_is_info`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_the_two_synthetic_machines_answer_the_check_opposite_ways`

Old text:

```
    if totals.majority_unmapped:
        cause = metadata_cli.majority_unmapped_cause(cfg, totals)
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
```

New text:

```
    if totals.majority_unmapped:
        cause = metadata_cli.majority_unmapped_cause(cfg, totals)
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
```

### `r372-b.B2_doctor_minority_fails`

_check_paths_resolved: a minority refuses, the sitting's own state after the hand edit

- File: `src/cratekit/cli/doctor.py`
- Source: `r372-b.json`, row `B2_doctor_minority_fails`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_a_minority_as_a_note_and_a_clean_collection_as_ok`

Old text:

```
    if totals.unmapped:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
```

New text:

```
    if totals.unmapped:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
```

### `r372-b.B4_doctor_reads_before_the_volume_checks`

_check_paths_resolved: survey a database on a volume the mount checks could not recognise

- File: `src/cratekit/cli/doctor.py`
- Source: `r372-b.json`, row `B4_doctor_reads_before_the_volume_checks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_defers_to_the_volume_checks_before_reading_anything`

Old text:

```
    unreadable = _library_state_unreadable(inputs, "the database")
    if unreadable is not None:
```

New text:

```
    unreadable = _library_state_unreadable(inputs, "the database")
    if False:
```

### `r372-b.B5_doctor_opens_the_live_path`

_survey_paths: open the configured database itself rather than a copy

- File: `src/cratekit/cli/doctor.py`
- Source: `r372-b.json`, row `B5_doctor_opens_the_live_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 5 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_copy_it_could_not_open_as_unknown_rather_than_good`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_minority_as_a_note_and_a_clean_collection_as_ok`
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it`

Old text:

```
    with rb_writer.read_only_copy(source, cfg=cfg) as db:
        return metadata_cli.resolution_totals(cfg, db)
```

New text:

```
    db = rb_writer.open_db(source, check_app_version=False, cfg=cfg)
    try:
        return metadata_cli.resolution_totals(cfg, db)
    finally:
        rb_writer.close_db(db)
```

### `r598-b.B6_doctor_clause_dropped`

_open_state: list an orphaned record bare, so it reads as a run in progress with no verb named

- File: `src/cratekit/cli/doctor.py`
- Source: `r598-b.json`, row `B6_doctor_clause_dropped`
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

### `r757-c2.D1_due_a_day_late`

_check_full_comparison: say to run one only past the bound and not at it

- File: `src/cratekit/cli/doctor.py`
- Source: `r757-c2.json`, row `D1_due_a_day_late`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_doctor_says_how_long_ago_a_full_comparison_last_ran`

Old text:

```
    due = f". {run_one}" if days >= FULL_COMPARISON_DUE_DAYS else ""
```

New text:

```
    due = f". {run_one}" if days > FULL_COMPARISON_DUE_DAYS else ""
```

### `r787.D1_doctor_own_list`

doctor's _declared_trees keeps a list of its own, the routing tree alone, instead of asking cutover_trees

- File: `src/cratekit/cli/doctor.py`
- Source: `r787.json`, row `D1_doctor_own_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2223 against a baseline of 2223
- Kills: 4 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_and_the_verb_read_one_set_of_cutover_trees`
  - `tests/test_cutover_cli.py::test_doctor_fails_on_a_native_record_the_cutover_would_refuse_to_create`
  - `tests/test_cutover_cli.py::test_doctor_reads_a_native_inbox_record_as_ok`
  - `tests/test_cutover_cli.py::test_doctor_reads_an_inbox_the_verb_cut_over_as_ok`

Old text:

```
    return tuple(named), tree_registry.cutover_trees(declared), None
```

New text:

```
    return tuple(named), frozenset({declared.tree.id}), None
```

### `r787.D2_set_guard_removed`

doctor stops judging a native record by the set, so a native catalogue tree reads ok

- File: `src/cratekit/cli/doctor.py`
- Source: `r787.json`, row `D2_set_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2223 against a baseline of 2223
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_lists_and_fails_a_recorded_tree_the_taxonomy_does_not_declare`

Old text:

```
            tree_id not in may_cut_over or record.source not in tree_registry.REBUILDABLE
```

New text:

```
            record.source not in tree_registry.REBUILDABLE
```

### `r787.D3_source_guard_removed`

doctor stops judging a native record by its source, so a native inbox from a catalogue crawl reads ok

- File: `src/cratekit/cli/doctor.py`
- Source: `r787.json`, row `D3_source_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2223 against a baseline of 2223
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_fails_a_native_inbox_whose_source_no_rebuild_reproduces`

Old text:

```
            tree_id not in may_cut_over or record.source not in tree_registry.REBUILDABLE
```

New text:

```
            tree_id not in may_cut_over
```

### `u132.D1_doctor_behind`

Doctor reads a copy behind the shipped schema as OK

- File: `src/cratekit/cli/doctor.py`
- Source: `u132.json`, row `D1_doctor_behind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2223 against a baseline of 2223
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u132.json`, row `D2_doctor_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2223 against a baseline of 2223
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

### `u159.M10_unread_reads_none_published`

_release_tags: a refused read answers no tags, so doctor says none is published

- File: `src/cratekit/cli/doctor.py`
- Source: `u159.json`, row `M10_unread_reads_none_published`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_release_read_parses_ls_remote_and_refuses_on_failure`

Old text:

```
    if done.returncode != 0:
        return None
    tags = []
```

New text:

```
    if done.returncode != 0:
        return ()
    tags = []
```

### `u159.M8_behind_reads_current`

_check_release: any parseable installed version passes, so a copy behind reads as current

- File: `src/cratekit/cli/doctor.py`
- Source: `u159.json`, row `M8_behind_reads_current`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_newer_release_warns_with_the_one_pipx_command_keeping_the_extras`
  - `tests/test_doctor.py::test_a_newer_release_without_extras_names_plain_cratekit`
  - `tests/test_doctor.py::test_an_upgrade_adds_vocals_when_the_library_has_scored_a_track`
  - `tests/test_doctor.py::test_an_upgrade_keeps_the_extras_and_adds_nothing_for_a_library_never_scored`

Old text:

```
    if installed >= newest:
```

New text:

```
    if True:
```

### `u170.D1_kept_folded`

status: fold every old gate, the kept ones too

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D1_kept_folded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_old_gate_the_command_would_keep_is_listed_and_never_collapsed`

Old text:

```
            if aged is not None and aged.retirable:
```

New text:

```
            if aged is not None:
```

### `u170.D2_status_week`

status: threshold fixed at seven days, not the file's

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D2_status_week`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_status_reads_the_threshold_from_the_file`

Old text:

```
    runs, folded = _run_report(timedelta(days=cfg.reports.open_gate_stale_days))
```

New text:

```
    runs, folded = _run_report(timedelta(days=7))
```

### `u170.D3_open_runs_short`

status: open_runs leaves the folded gates out

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D3_open_runs_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_status_collapses_old_gates_into_one_line_and_lists_new_ones_as_before`

Old text:

```
            "open_runs": sum(1 for f in findings if f.key.startswith("run.")) + folded,
```

New text:

```
            "open_runs": sum(1 for f in findings if f.key.startswith("run.")),
```

### `u170.D4_line_dropped`

status: fold the gates and print no line for them

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D4_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 3 (killed)
- Killed:
  - `tests/test_run_retire.py::test_status_collapses_old_gates_into_one_line_and_lists_new_ones_as_before`
  - `tests/test_run_retire.py::test_status_reads_the_threshold_from_the_file`
  - `tests/test_run_retire.py::test_the_collapsed_line_names_the_dates_it_spans_and_reaches_a_person`

Old text:

```
    if old and older_than is not None:
```

New text:

```
    if False:
```

### `u181.D1_extras_row_never_ok`

doctor install.extras: never report ok, so a copy whose model scores is told the extra is absent

- File: `src/cratekit/cli/doctor.py`
- Source: `u181.json`, row `D1_extras_row_never_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_cli_contract.py`
- Collected: 1414 against a baseline of 1414
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_copy_whose_vocal_model_can_score_is_ok`
  - `tests/test_doctor.py::test_the_row_reads_the_vocals_modules_own_probe_with_the_loader_bound_or_not`

Old text:

```
    missing = inputs.probes.vocal_requirement()
    if missing is None:
```

New text:

```
    missing = inputs.probes.vocal_requirement() or ("extra", "forced")
    if missing is None:
```

### `u181.D2_files_offered_reinstall`

doctor install.extras: treat missing model files as the extra, so a reinstall that places nothing is printed

- File: `src/cratekit/cli/doctor.py`
- Source: `u181.json`, row `D2_files_offered_reinstall`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_missing_model_files_are_named_and_no_reinstall_is_offered_for_them`

Old text:

```
    if kind != vocal_scoring.MISSING_EXTRA:
```

New text:

```
    if False:
```

### `u181.D3_release_form_dropped`

doctor vocals_install_command: ignore a release install, so the command is the folder or pip form

- File: `src/cratekit/cli/doctor.py`
- Source: `u181.json`, row `D3_release_form_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_copy_without_the_vocals_extra_says_so_and_prints_the_reinstall_command`
  - `tests/test_doctor.py::test_a_git_install_of_a_branch_head_names_no_tag_that_does_not_exist`
  - `tests/test_doctor.py::test_the_row_reads_the_vocals_modules_own_probe_with_the_loader_bound_or_not`

Old text:

```
    if origin.kind == "vcs" and origin.url and origin.version and _is_release(origin.version):
        extras = sorted({*origin.extras, VOCALS_EXTRA})
```

New text:

```
    if False:
        extras = sorted({*origin.extras, VOCALS_EXTRA})
```

### `u181.D4_release_form_no_vocals`

doctor vocals_install_command: the release form keeps the extras and does not add vocals

- File: `src/cratekit/cli/doctor.py`
- Source: `u181.json`, row `D4_release_form_no_vocals`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_copy_without_the_vocals_extra_says_so_and_prints_the_reinstall_command`
  - `tests/test_doctor.py::test_the_row_reads_the_vocals_modules_own_probe_with_the_loader_bound_or_not`

Old text:

```
        extras = sorted({*origin.extras, VOCALS_EXTRA})
```

New text:

```
        extras = sorted({*origin.extras})
```

### `u181.D5_upgrade_never_adds_vocals`

doctor _kept: the upgrade command never adds vocals, so a scored library upgrades without it

- File: `src/cratekit/cli/doctor.py`
- Source: `u181.json`, row `D5_upgrade_never_adds_vocals`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_upgrade_adds_vocals_when_the_library_has_scored_a_track`

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

- File: `src/cratekit/cli/doctor.py`
- Source: `u181.json`, row `D6_upgrade_always_adds_vocals`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_newer_release_without_extras_names_plain_cratekit`
  - `tests/test_doctor.py::test_an_upgrade_keeps_the_extras_and_adds_nothing_for_a_library_never_scored`

Old text:

```
    if VOCALS_EXTRA in origin.extras or not inputs.probes.vocals_scored(inputs.cfg):
```

New text:

```
    if VOCALS_EXTRA in origin.extras:
```

### `u181.D7_scored_probe_false`

doctor _vocals_scored: never see the recorded calibration

- File: `src/cratekit/cli/doctor.py`
- Source: `u181.json`, row `D7_scored_probe_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_library_has_scored_when_a_vocal_calibration_is_recorded`

Old text:

```
    return config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, cfg).is_file()
```

New text:

```
    return False
```

### `u184.D1_volume_not_established`

_check_backup_acknowledgment: read the record off a volume nobody established, so a missing disk reads as none on record

- File: `src/cratekit/cli/doctor.py`
- Source: `u184.json`, row `D1_volume_not_established`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u184.json`, row `D2_unreadable_is_a_note`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u184.json`, row `D3_remedy_chosen_here`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u184.json`, row `D4_expired_read_as_valid`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u184.json`, row `D5_wall_clock`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u184.json`, row `D6_hours_coefficient`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u184.json`, row `D7_rule_not_named`
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

### `u185.D1_push_newer_warns`

deadca7.push: invert the comparison, so a push after the last backup reads as held by it

- File: `src/cratekit/cli/doctor.py`
- Source: `u185.json`, row `D1_push_newer_warns`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u185.json`, row `D2_hidden_entries`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u185.json`, row `D3_unread_folder`
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

### `u186.N1_note_age`

doctor: the note's age halved to twelve hours, so a gate open twenty hours is listed

- File: `src/cratekit/cli/doctor.py`
- Source: `u186.json`, row `N1_note_age`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_doctor_leaves_a_gate_open_twenty_hours_off_the_list`

Old text:

```
OPEN_GATE_NOTE_AGE = timedelta(days=1)
```

New text:

```
OPEN_GATE_NOTE_AGE = timedelta(hours=12)
```

### `u186.N2_note_fails`

doctor: the note is a failure when it lists a run, though the brief says never

- File: `src/cratekit/cli/doctor.py`
- Source: `u186.json`, row `N2_note_fails`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_doctor_lists_a_gate_open_two_days_and_not_one_open_an_hour`
  - `tests/test_gate_siblings.py::test_doctor_names_a_session_ack_left_blocked_as_sitting_51_left_one`

Old text:

```
    return Finding(key=OPEN_GATES_CHECK, title="runs at a gate", status=Status.INFO, detail=detail)
```

New text:

```
    return Finding(key=OPEN_GATES_CHECK, title="runs at a gate", status=Status.FAIL if blocked else Status.INFO, detail=detail)
```

### `u186.N3_note_unreadable_dropped`

doctor: a record that cannot be read is skipped, so the note reads as clean over it

- File: `src/cratekit/cli/doctor.py`
- Source: `u186.json`, row `N3_note_unreadable_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_record_missing_a_field_is_named_unreadable_at_the_gate_and_in_doctor`
  - `tests/test_gate_siblings.py::test_doctor_says_a_record_it_could_not_read_and_still_never_fails`

Old text:

```
        except Exception:  # noqa: BLE001 - a note never fails; an unread record is named
            unreadable.append(path.stem)
            continue
```

New text:

```
        except Exception:  # noqa: BLE001 - a note never fails; an unread record is named
            continue
```

### `u206.M24_doctor_set_aside_unnamed`

_check_isrc_cache: leave the set aside files out of the note

- File: `src/cratekit/cli/doctor.py`
- Source: `u206.json`, row `M24_doctor_set_aside_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_doctor_names_a_set_aside_file_and_never_fails`

Old text:

```
    aside = cache.set_aside()
    if aside:
```

New text:

```
    aside = cache.set_aside()
    if False:
```

### `u211.C1_doctor_closed_is_a_note`

doctor rekordbox.closed: report an unconfirmed absence as OK rather than as a note

- File: `src/cratekit/cli/doctor.py`
- Source: `u211.json`, row `C1_doctor_closed_is_a_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_doctor.py`
- Collected: 466 against a baseline of 466
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_doctor_names_an_unreadable_live_process_as_a_note`

Old text:

```
            status=Status.INFO,
            detail=(
                f"{exc.cause.message}. Every database write refuses until the scan "
```

New text:

```
            status=Status.OK,
            detail=(
                f"{exc.cause.message}. Every database write refuses until the scan "
```

### `u211.C2_doctor_paths_take_no_copy`

doctor library.paths_resolved: let the unconfirmed refusal escape the check, so the rescue files it as a check that did not complete

- File: `src/cratekit/cli/doctor.py`
- Source: `u211.json`, row `C2_doctor_paths_take_no_copy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_doctor.py`, `tests/test_paths_resolved.py`
- Collected: 517 against a baseline of 517
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_doctor_names_an_unreadable_live_process_as_a_note`

Old text:

```
    except processes.AbsenceUnconfirmed as exc:
        # NO COPY OVER AN ABSENCE NOBODY CONFIRMED (U211), said as unknown and
```

New text:

```
    except LookupError as exc:
        # NO COPY OVER AN ABSENCE NOBODY CONFIRMED (U211), said as unknown and
```

### `u224.M10_refused_backups_read_no_push`

_check_deadca7_push: a backup folder whose stat is refused reads as absent, so no push

- File: `src/cratekit/cli/doctor.py`
- Source: `u224.json`, row `M10_refused_backups_read_no_push`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u224.json`, row `M1_found_ignored`
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
  - `tests/test_doctor.py::test_sitting_68s_mac_the_bundle_and_no_support_folder_reads_installed_with_no_push`
  - `tests/test_doctor.py::test_the_bundle_in_the_accounts_own_applications_folder_reads_installed`
  - `tests/test_doctor.py::test_the_deadcatalog_state_folder_alone_reads_installed_with_no_push`

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

- File: `src/cratekit/cli/doctor.py`
- Source: `u224.json`, row `M2_unread_place_dropped`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u224.json`, row `M3_broken_installed_probe_silent`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u224.json`, row `M4_unread_support_read_absent`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u224.json`, row `M5_refused_stat_read_absent`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u224.json`, row `M6_unread_folded_into_not_installed`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u224.json`, row `M7_install_signals_always_asked`
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

### `u224.M8_default_probe_empty`

Probes: the install probe's default answers nothing, the regression that re-creates the bug

- File: `src/cratekit/cli/doctor.py`
- Source: `u224.json`, row `M8_default_probe_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_real_probes_value_asks_the_installed_probe`

Old text:

```
    deadca7_installed: Callable[[], tuple[Path, ...]] = _deadca7_installed
```

New text:

```
    deadca7_installed: Callable[[], tuple[Path, ...]] = lambda: ()
```

### `u224.M9_path_through_a_file_unread`

_folder_presence: a stat through a file reads unread rather than absent

- File: `src/cratekit/cli/doctor.py`
- Source: `u224.json`, row `M9_path_through_a_file_unread`
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u263.json`, row `D21_doctor_names_verbs`
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

### `u27-reports-round-1.D2_required_gate`

Report a broken Trash as a failure even where no verb needs it

- File: `src/cratekit/cli/doctor.py`
- Source: `u27-reports-round-1.json`, row `D2_required_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

### `u27-reports-round-1.D3_trash_remedy`

Answer a broken Trash with run-doctor, which is the token that sends a person here

- File: `src/cratekit/cli/doctor.py`
- Source: `u27-reports-round-1.json`, row `D3_trash_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_volume_with_no_usable_trash_refuses_because_a_verb_depends_on_it`

Old text:

```
        remedy=Remedy.GRANT_PATH_ACCESS,
```

New text:

```
        remedy=Remedy.RUN_DOCTOR,
```

### `u27-reports-round-2.D1_probe_creates`

Round 1 zero, re-run against the replacement guard: take the creating default

- File: `src/cratekit/cli/doctor.py`
- Source: `u27-reports-round-2.json`, row `D1_probe_creates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_trash_check_cannot_pass_by_having_run`

Old text:

```
    return trash.probe(path, create=False)
```

New text:

```
    return trash.probe(path, create=True)
```

### `u27-reports-round-3-fixes.F3_trash_absent_is_a_failure`

Report a volume whose Trash has not been created yet as a failure again

- File: `src/cratekit/cli/doctor.py`
- Source: `u27-reports-round-3-fixes.json`, row `F3_trash_absent_is_a_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

### `u27-round-8-independent.D1_finding_no_classification`

Invert the entry guard so a Finding carrying an exception is never classified

- File: `src/cratekit/cli/doctor.py`
- Source: `u27-round-8-independent.json`, row `D1_finding_no_classification`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if self.error is None:
            return
```

New text:

```
        if self.error is not None:
            return
```

### `u27-round-8-independent.D2_finding_no_remedy_override`

Keep the branch's hard coded remedy token instead of the one the refusal kind chooses

- File: `src/cratekit/cli/doctor.py`
- Source: `u27-round-8-independent.json`, row `D2_finding_no_remedy_override`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if self.remedy is not refusal.remedy:
            object.__setattr__(self, "remedy", refusal.remedy)
```

New text:

```
(empty)
```

### `u27-round-8-independent.D4_composite_reason`

COMPOSITE for D4: the cause a finding gains carries the wrong reason slug

- File: `src/cratekit/cli/doctor.py`
- Source: `u27-round-8-independent.json`, row `D4_composite_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                Cause(
                    reason=refusal.reason,
```

New text:

```
                Cause(
                    reason="internal-error",
```

### `u27-round-8-independent.E1_mount_detail_swapped`

Swap the NOT_MOUNTED and MOUNTED_ELSEWHERE sentences, conflating unmounted with moved

- File: `src/cratekit/cli/doctor.py`
- Source: `u27-round-8-independent.json`, row `E1_mount_detail_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u27-round-8-independent.json`, row `E2_identity_verdict_green`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

- File: `src/cratekit/cli/doctor.py`
- Source: `u27-round-8-independent.json`, row `E3_found_at_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_packaging.py`
- Collected: 1673 against a baseline of 1673
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

### `u97-b.B1_doctor_routes_the_wrong_credential_token`

doctor _CREDENTIAL_REMEDY: answer the provider check with SET_CREDENTIAL, the recognition token, so the report tells a person to paste a key they cannot have

- File: `src/cratekit/cli/doctor.py`
- Source: `u97-b.json`, row `B1_doctor_routes_the_wrong_credential_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1588 against a baseline of 1588
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb`

Old text:

```
        "credential.provider": Remedy.AUTHENTICATE_PROVIDER,
```

New text:

```
        "credential.provider": Remedy.SET_CREDENTIAL,
```

### `r388-b.M12_listing_steps_say_take_a_backup`

Replace the listing failure's first reserved step with the take a backup step it replaced

- File: `src/cratekit/cli/exit_codes.py`
- Source: `r388-b.json`, row `M12_listing_steps_say_take_a_backup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 684 against a baseline of 684
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-identity]`

Old text:

```
            "check the backup remote is reachable from this machine; the snapshot "
            "is not known to be missing, a listing of it failed",
```

New text:

```
            "no dated database snapshot exists for this library yet; take a "
            "backup before a restore can be planned",
```

### `r388-c.M13_credential_step_dropped`

Drop the credential step from the listing failure's reservation

- File: `src/cratekit/cli/exit_codes.py`
- Source: `r388-c.json`, row `M13_credential_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 684 against a baseline of 684
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-identity]`

Old text:

```
            "check the remote's credential has not expired or been revoked, and "
            "reconnect it in rclone if it has",

```

New text:

```
(empty)
```

### `r388-d.M16_named_stamp_step_dropped_remeasured`

Re-measure of M16 after the pin: drop the named stamp step added to no-snapshot-available

- File: `src/cratekit/cli/exit_codes.py`
- Source: `r388-d.json`, row `M16_named_stamp_step_dropped_remeasured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 684 against a baseline of 684
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-contents-2026-08-01T000000Z-holds no database folder]`
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-identity-2026-08-01T000000Z-the snapshot 2026-08-01T000000Z was not found]`

Old text:

```
            "when --snapshot named a stamp, that snapshot or its database "
            "folder is not on the remote; check the stamp, or leave the flag "
            "off to take the newest",

```

New text:

```
(empty)
```

### `u235.T1_tail_back_to_sixteen_bits`

new_run_id: the tail goes back to token_hex(2), four hex characters, the width the card's failure came from

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T1_tail_back_to_sixteen_bits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_identifier_carries_sixty_four_bits_of_random_tail`
  - `tests/test_cli_contract.py::test_two_thousand_identifiers_minted_inside_one_second_are_all_distinct`

Old text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

New text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(2)}"
```

### `u235.T2_tail_thirty_two_bits`

new_run_id: the tail narrows to token_hex(4), eight hex characters, a width the distinct test alone cannot tell from sixty four

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T2_tail_thirty_two_bits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_identifier_carries_sixty_four_bits_of_random_tail`

Old text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

New text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(4)}"
```

### `u235.T3_tail_fifty_six_bits`

new_run_id: the tail narrows by one byte, token_hex(7), fourteen hex characters

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T3_tail_fifty_six_bits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_identifier_carries_sixty_four_bits_of_random_tail`

Old text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

New text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(7)}"
```

### `u235.T4_tail_from_the_instant`

new_run_id: the tail keeps its sixteen hex characters but is read off the instant's microseconds, so two ids at one instant are equal

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T4_tail_from_the_instant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_two_thousand_identifiers_minted_inside_one_second_are_all_distinct`

Old text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

New text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{moment.microsecond:016x}"
```

### `u235.T5_instant_ignored`

new_run_id: the instant a caller hands it is ignored and the clock is read instead

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T5_instant_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_identifier_carries_sixty_four_bits_of_random_tail`
  - `tests/test_cli_contract.py::test_two_thousand_identifiers_minted_inside_one_second_are_all_distinct`

Old text:

```
    moment = now or datetime.now(timezone.utc)
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

New text:

```
    moment = datetime.now(timezone.utc)
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

### `u235.T6_stamp_loses_its_colons`

new_run_id: the stamp drops its colons, so an id minted after the widening no longer reads like one minted before it

- File: `src/cratekit/cli/output.py`
- Source: `u235.json`, row `T6_stamp_loses_its_colons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_identifier_carries_sixty_four_bits_of_random_tail`
  - `tests/test_cli_contract.py::test_two_thousand_identifiers_minted_inside_one_second_are_all_distinct`

Old text:

```
    return f"{moment.strftime('%Y-%m-%dT%H:%M:%SZ')}-{secrets.token_hex(8)}"
```

New text:

```
    return f"{moment.strftime('%Y-%m-%dT%H%M%SZ')}-{secrets.token_hex(8)}"
```

### `u298.H1_config_cause_reason`

load_config: an unusable config ends a cause other than config-unusable

- File: `src/cratekit/cli/output.py`
- Source: `u298.json`, row `H1_config_cause_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 341 against a baseline of 341
- Kills: 3 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it[failure0-run-setup]`
  - `tests/test_shared_homes.py::test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it[failure1-fix-config-values]`
  - `tests/test_shared_homes.py::test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it[failure2-run-doctor]`

Old text:

```
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=origin,
```

New text:

```
                reason="internal-error",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=origin,
```

### `u298.H2_config_cause_origin`

load_config: the refusal no longer names the verb that met it

- File: `src/cratekit/cli/output.py`
- Source: `u298.json`, row `H2_config_cause_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 341 against a baseline of 341
- Kills: 3 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it[failure0-run-setup]`
  - `tests/test_shared_homes.py::test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it[failure1-fix-config-values]`
  - `tests/test_shared_homes.py::test_an_unusable_config_is_one_typed_cause_whatever_verb_met_it[failure2-run-doctor]`

Old text:

```
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=origin,
                detail={"kind": type(exc).__name__},
```

New text:

```
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=(),
                detail={"kind": type(exc).__name__},
```

### `u298.H3_declared_gate_by_name`

declared_gate: the first gate on the entry is returned whatever its name

- File: `src/cratekit/cli/output.py`
- Source: `u298.json`, row `H3_declared_gate_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`
- Collected: 100 against a baseline of 100
- Kills: 2 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_gate_is_found_by_its_name_and_not_by_where_it_stands`
  - `tests/test_shared_homes.py::test_a_missing_gate_is_a_runtime_error_for_the_verbs_that_always_raised_one`

Old text:

```
    for spec in entry.gates:
        if spec.name == name:
            return spec
    raise RuntimeError(
```

New text:

```
    for spec in entry.gates:
        return spec
    raise RuntimeError(
```

### `u298.H4_confirm_gate_refusal`

confirm_gate: a verb with no gate of the name gets None instead of the typed refusal

- File: `src/cratekit/cli/output.py`
- Source: `u298.json`, row `H4_confirm_gate_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_missing_gate_is_a_typed_refusal_for_the_verbs_that_ask_before_they_write`

Old text:

```
            return spec
    raise refuse(
        "internal-error",
        f"{entry.name} declares no gate named {name!r}, so there is no "
```

New text:

```
            return spec
    return None
    raise refuse(
        "internal-error",
        f"{entry.name} declares no gate named {name!r}, so there is no "
```

### `u298.H5_approving_actor_default`

approving_actor: a run nobody decided reads as the cli actor

- File: `src/cratekit/cli/output.py`
- Source: `u298.json`, row `H5_approving_actor_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_the_approving_actor_is_read_off_the_recorded_decision`

Old text:

```
    return decision.actor if decision is not None else ""
```

New text:

```
    return decision.actor if decision is not None else "cli"
```

### `u298.H6_no_job_id_string`

no_job: the job id of a run that queued nothing is null, which fails the job_state schema

- File: `src/cratekit/cli/output.py`
- Source: `u298.json`, row `H6_no_job_id_string`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`
- Collected: 100 against a baseline of 100
- Kills: 2 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_run_that_queued_nothing_reports_an_empty_string_for_its_job`
  - `tests/test_shared_homes.py::test_what_a_no_op_names_rides_under_progress_as_a_job_reports_it`

Old text:

```
    return {"job_id": "", "state": state, "cause": None, "progress": dict(progress)}
```

New text:

```
    return {"job_id": None, "state": state, "cause": None, "progress": dict(progress)}
```

### `r83.P1_flush`

R-346: drop the flush from the prompter's writer, the defect as found

- File: `src/cratekit/cli/prompt.py`
- Source: `r83.json`, row `P1_flush`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_question_reaches_a_real_pipe_before_its_answer_is_read`

Old text:

```
    print(text, file=sys.stderr, end="", flush=True)
```

New text:

```
    print(text, file=sys.stderr, end="")
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

### `a32.R1_gate_not_explicit`

The confirm gate is answerable inline

- File: `src/cratekit/cli/registry.py`
- Source: `a32.json`, row `R1_gate_not_explicit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`, `tests/test_cli_contract.py`
- Collected: 1056 against a baseline of 1056
- Kills: 5 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_moved_after_the_commit_refuses_through_the_verb`
  - `tests/test_repair_link.py::test_a_plan_where_every_row_is_already_at_its_value_still_asks_and_writes_nothing`
  - `tests/test_repair_link.py::test_a_triple_already_at_its_value_is_shown_and_not_written`
  - `tests/test_repair_link.py::test_the_gate_takes_no_inline_answer`
  - `tests/test_repair_link.py::test_the_two_acts_write_each_triple_and_move_no_other_column`

Old text:

```
                prompt="Write these probe values onto these rows?",
                #: EXPLICIT (R34). A write to a row of a live library is
                #: answered by a separate recorded act with an actor.
                explicit=True,
```

New text:

```
                prompt="Write these probe values onto these rows?",
                #: EXPLICIT (R34). A write to a row of a live library is
                #: answered by a separate recorded act with an actor.
                explicit=False,
```

### `r185-r246-author.D2_cloud_gate_restored`

Declare the cloud sync decision on a verb that opens no database, the half the contract suite calls spurious

- File: `src/cratekit/cli/registry.py`
- Source: `r185-r246-author.json`, row `D2_cloud_gate_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 5993 against a baseline of 5993
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`
  - `tests/test_tag_workers.py::test_the_retag_entry_declares_the_file_surface_alone_and_no_database_decision`

Old text:

```
                explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="name.apply",
```

New text:

```
                explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="name.apply",
```

### `r312.R1_summary_promises_a_replace`

Put the registry summary back to the promise the verb does not keep

- File: `src/cratekit/cli/registry.py`
- Source: `r312.json`, row `R1_summary_promises_a_replace`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 5993 against a baseline of 5993
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_resort_summary_says_the_verb_is_additive`

Old text:

```
        summary="add already-routed tracks to their new place after a genre or energy "
        "change, additive, the old membership stays and is named",
```

New text:

```
        summary="re-place already-routed tracks after a genre or energy change",
```

### `r372-b.B12_verb_does_not_declare_the_check`

registry: the My Tags verb stops declaring library.paths_resolved

- File: `src/cratekit/cli/registry.py`
- Source: `r372-b.json`, row `B12_verb_does_not_declare_the_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1465 against a baseline of 1465
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_the_verb_declares_the_check_and_the_slug_is_registered`

Old text:

```
            # reads the same ratio the verb refuses on.
            "library.paths_resolved",
```

New text:

```
            # reads the same ratio the verb refuses on.
```

### `r424.A1_writes_narrowed`

Restore the four local write surfaces the verb never reaches

- File: `src/cratekit/cli/registry.py`
- Source: `r424.json`, row `A1_writes_narrowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`
- Collected: 1122 against a baseline of 1122
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`
  - `tests/test_outbound_workers.py::test_the_verb_declares_the_remote_account_and_no_local_surface`

Old text:

```
        writes=frozenset({"remote"}),
        adjudicates=True,
        destructive=True,
```

New text:

```
        writes=frozenset({"db_tree", "db_metadata", "xml", "files", "remote"}),
        adjudicates=True,
        destructive=True,
```

### `r424.A2_cloud_gate_absent`

Restore the cloud sync decision on a verb that never opens the database

- File: `src/cratekit/cli/registry.py`
- Source: `r424.json`, row `A2_cloud_gate_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`
- Collected: 1122 against a baseline of 1122
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`
  - `tests/test_outbound_workers.py::test_the_verb_asks_no_question_its_work_cannot_raise`

Old text:

```
                digest_source="plan",
            ),
        ),
        # Landed by U33.
```

New text:

```
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
        # Landed by U33.
```

### `r424.A3_rekordbox_checks`

Restore both rekordbox doctor checks for a verb that reads an export

- File: `src/cratekit/cli/registry.py`
- Source: `r424.json`, row `A3_rekordbox_checks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`, `tests/test_doctor.py`
- Collected: 1539 against a baseline of 1539
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_doctor_asks_neither_rekordbox_question_for_a_sweep_that_reads_an_export`

Old text:

```
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="sync.favorites.confirm",
```

New text:

```
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins", "credential.provider"),
        gates=(
            GateSpec(
                name="sync.favorites.confirm",
```

### `r424.A4_library_mounted`

Drop library.mounted, which the outbound write ledger needs

- File: `src/cratekit/cli/registry.py`
- Source: `r424.json`, row `A4_library_mounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`, `tests/test_doctor.py`
- Collected: 1539 against a baseline of 1539
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_doctor_asks_neither_rekordbox_question_for_a_sweep_that_reads_an_export`

Old text:

```
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="sync.favorites.confirm",
```

New text:

```
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="sync.favorites.confirm",
```

### `r424.A5_summary_both_ways`

Restore the summary that claims the verb moves favourites both ways

- File: `src/cratekit/cli/registry.py`
- Source: `r424.json`, row `A5_summary_both_ways`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`
- Collected: 1122 against a baseline of 1122
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_verb_declares_the_remote_account_and_no_local_surface`

Old text:

```
        summary="heart the library's favourites on the streaming service; add-only, never un-hearts",
```

New text:

```
        summary="sync hearted tracks both ways; add-only, never un-hearts",
```

### `r770-d.C8_native_gate_answered_inline`

registry: declare intake.file.native as an ordinary gate, answerable on the run that found it

- File: `src/cratekit/cli/registry.py`
- Source: `r770-d.json`, row `C8_native_gate_answered_inline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_cli_contract.py`
- Collected: 1044 against a baseline of 1044
- Kills: 9 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_binding_failure_past_the_gate_says_what_it_leaves`
  - `tests/test_intake_writers_native.py::test_a_file_already_in_the_collection_gains_a_membership_and_no_second_row`
  - `tests/test_intake_writers_native.py::test_a_file_named_through_a_link_is_stored_under_the_configured_root`
  - `tests/test_intake_writers_native.py::test_a_refusal_past_the_gate_keeps_its_reason_and_remedy`
  - `tests/test_intake_writers_native.py::test_after_the_write_no_analysis_value_is_on_the_new_row_column_by_column`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_writers_native.py::test_the_native_gate_takes_no_inline_answer`
  - `tests/test_intake_writers_native.py::test_the_row_carries_the_librarys_own_device`

Old text:

```
                prompt="Add this file to the collection?",
                explicit=True,
```

New text:

```
                prompt="Add this file to the collection?",
                explicit=False,
```

### `r773-b.R1_doctor_check_not_declared`

registry: the verb no longer declares library.paths_resolved

- File: `src/cratekit/cli/registry.py`
- Source: `r773-b.json`, row `R1_doctor_check_not_declared`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_verb_declares_one_xml_no_database_surface_and_asks_nothing`

Old text:

```
        doctor_checks=("library.mounted", "rekordbox.closed", "library.paths_resolved"),
```

New text:

```
        doctor_checks=("library.mounted", "rekordbox.closed"),
```

### `r923.N20_gate_takes_inline_answer`

The repair's gate accepts an inline answer, so a flag on the command writes the rows

- File: `src/cratekit/cli/registry.py`
- Source: `r923.json`, row `N20_gate_takes_inline_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 5 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_gate_takes_no_inline_answer`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
                name="repair.rows.confirm",
                options=("apply", "abort"),
                prompt="Give these rows rekordbox's own defaults?",
                #: EXPLICIT (R34). A write to rows of a live library is answered
                #: by a separate recorded act with an actor.
                explicit=True,
```

New text:

```
                name="repair.rows.confirm",
                options=("apply", "abort"),
                prompt="Give these rows rekordbox's own defaults?",
                #: EXPLICIT (R34). A write to rows of a live library is answered
                #: by a separate recorded act with an actor.
                explicit=False,
```

### `u103-b.M1_identify_declared_adjudicating`

Take the adjudicates declaration off intake.identify

- File: `src/cratekit/cli/registry.py`
- Source: `u103-b.json`, row `M1_identify_declared_adjudicating`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_cli_contract.py`
- Collected: 1104 against a baseline of 1105
- Kills: 1 (collect-error)
- Note: collection changed: 1104 collected against a baseline of 1105. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/intake/test_workers.py::test_identify_is_declared_adjudicating_because_it_offers_under_its_own_key`

Old text:

```
        # missing`` sets.
        adjudicates=True,

```

New text:

```
        # missing`` sets.

```

### `u129-author.A10_export_set_without_library_mounted`

Drop library.mounted from export.set so the INSPIRATION backfill opens a database doctor never checked

- File: `src/cratekit/cli/registry.py`
- Source: `u129-author.json`, row `A10_export_set_without_library_mounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_set_and_archive_declare_library_mounted_for_backfill`

Old text:

```
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="export.set.confirm",

```

New text:

```
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="export.set.confirm",

```

### `u129-author.A11_export_archive_without_library_mounted`

Drop library.mounted from export.archive so the no-name backfill opens library paths doctor never checked

- File: `src/cratekit/cli/registry.py`
- Source: `u129-author.json`, row `A11_export_archive_without_library_mounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_set_and_archive_declare_library_mounted_for_backfill`

Old text:

```
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="export.archive.confirm",

```

New text:

```
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="export.archive.confirm",

```

### `u129-author.A9_land_without_provider_check`

Drop credential.provider from intake.land so doctor never names the archive's session

- File: `src/cratekit/cli/registry.py`
- Source: `u129-author.json`, row `A9_land_without_provider_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_intake_land_declares_remote_and_provider_for_the_archive`

Old text:

```
            "library.paths_resolved",
            "credential.provider",
        ),

```

New text:

```
            "library.paths_resolved",
        ),

```

### `u263.D22_restamp_declares`

registry: analyze restamp no longer declares binary.ffmpeg

- File: `src/cratekit/cli/registry.py`
- Source: `u263.json`, row `D22_restamp_declares`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_cli_contract.py`
- Collected: 1414 against a baseline of 1414
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

### `u27-adopt-apply-author.R1_marker_restored`

Put planned_in back on the entry, so the conformance suite stops driving the landed verb

- File: `src/cratekit/cli/registry.py`
- Source: `u27-adopt-apply-author.json`, row `R1_marker_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_adoption.py`, `tests/test_pending_units.py`
- Collected: 1710 against a baseline of 1713
- Kills: 3 (collect-error)
- Note: collection changed: 1710 collected against a baseline of 1713. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_adoption.py::test_no_landed_adoption_verb_still_owes_the_file_the_board_reads`
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
  - `tests/test_cli_contract.py::test_every_verb_acknowledged_for_conformance_is_refused_without_one_elsewhere`

Old text:

```
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── Deletion: one surface, TWO MODULES, and the split is the decision ────
```

New text:

```
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
        planned_in=ADOPT_APPLY_CLI_UNIT,
    ),
    # ── Deletion: one surface, TWO MODULES, and the split is the decision ────
```

### `u27-reports-round-1.R1_delete_review_precondition`

Stop delete.review declaring the Trash check as a precondition

- File: `src/cratekit/cli/registry.py`
- Source: `u27-reports-round-1.json`, row `R1_delete_review_precondition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 3872 against a baseline of 3872
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_trash_probe_the_operating_system_refuses_is_a_failure_with_the_right_act`
  - `tests/test_doctor.py::test_a_volume_with_no_usable_trash_refuses_because_a_verb_depends_on_it`

Old text:

```
            "library.identity",
            "library.trash",
            "rekordbox.closed",
```

New text:

```
            "library.identity",
            "rekordbox.closed",
```

### `u27-restore-cli-independent.I_H1_the_landed_verb_keeps_its_marker`

Put planned_in back on restore.list, which is what would disarm the conformance properties again

- File: `src/cratekit/cli/registry.py`
- Source: `u27-restore-cli-independent.json`, row `I_H1_the_landed_verb_keeps_its_marker`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_pending_units.py`
- Collected: 1095 against a baseline of 1098
- Kills: 1 (collect-error)
- Note: collection changed: 1095 collected against a baseline of 1098. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`

Old text:

```
        # U27 LANDED IT. The marker was U32's, then U27's, and it is now gone
```

New text:

```
        planned_in="U27",
        # U27 LANDED IT. The marker was U32's, then U27's, and it is now gone
```

### `u28-skills-independent.R1_planned_in_restored`

the skills.install registry entry gets planned_in back, so the conformance properties skip it again

- File: `src/cratekit/cli/registry.py`
- Source: `u28-skills-independent.json`, row `R1_planned_in_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 993 against a baseline of 997
- Kills: 1 (collect-error)
- Note: collection changed: 993 collected against a baseline of 997. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`

Old text:

```
        module_id="skills",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
```

New text:

```
        module_id="skills",
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        planned_in="U28",
```

### `u39-author-full.W2_unreachable_gate_restored`

name.apply redeclares the cloud sync decision its work can never raise

- File: `src/cratekit/cli/registry.py`
- Source: `u39-author-full.json`, row `W2_unreachable_gate_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 4049 against a baseline of 4049
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`

Old text:

```
            GateSpec(
                name="name.apply.confirm",
                options=("apply", "abort"),
                prompt="Apply these renames?",
                digest_source="plan",
            ),
        ),

```

New text:

```
            GateSpec(
                name="name.apply.confirm",
                options=("apply", "abort"),
                prompt="Apply these renames?",
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),

```

### `u40-author-full.R3_ungated`

Drop the module toggle, so a Module row ships on in the slim profile (R5)

- File: `src/cratekit/cli/registry.py`
- Source: `u40-author-full.json`, row `R3_ungated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`

Old text:

```
        module_id="repair",
        argv_builder="retag_argv",
```

New text:

```
        argv_builder="retag_argv",
```

### `u40-author-full.R5_row_unclaimed`

Claim no feature row, so row 18 becomes a Module the product owes and no verb cites

- File: `src/cratekit/cli/registry.py`
- Source: `u40-author-full.json`, row `R5_row_unclaimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`
- Collected: 1005 against a baseline of 1005
- Kills: 5 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`
  - `tests/test_cutover_parity.py::test_a_row_cited_by_nothing_is_a_decision_and_not_an_oversight`
  - `tests/test_cutover_parity.py::test_the_backlog_is_every_owed_row_without_a_landed_verb`
  - `tests/test_cutover_parity.py::test_the_cutover_is_mechanically_possible_and_says_what_is_left`
  - `tests/test_cutover_parity.py::test_the_parity_table_renders_for_a_person`

Old text:

```
        feature_rows=(18,),
```

New text:

```
        feature_rows=(),
```

### `u40-author-full.R6_row_still_cut`

Leave row 18 dispositioned Cut while a verb claims it, which is the coupling across two trees

- File: `src/cratekit/cli/registry.py`
- Source: `u40-author-full.json`, row `R6_row_still_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`
- Collected: 1005 against a baseline of 1005
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`

Old text:

```
    Feature(18, "genre correction for a tag already too coarse", "module"),
```

New text:

```
    Feature(18, "genre correction for a tag already too coarse", "cut"),
```

### `u40-author-round-2.R8_not_long_running`

Round one COLLECT ERROR rather than a zero, and the error was the finding. Declaring the sweep short removes the verb from every derived guard in the resume contract, so the suite loses three tests and goes green

- File: `src/cratekit/cli/registry.py`
- Source: `u40-author-round-2.json`, row `R8_not_long_running`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_queued_resume_contract.py`
- Collected: 18 against a baseline of 20
- Kills: 0 (collect-error)
- Note: collection changed: 18 collected against a baseline of 20. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.

Old text:

```
        argv_builder="retag_argv",
        long_running=True,
```

New text:

```
        argv_builder="retag_argv",
```

### `u42-author-round-2.R2_handler_lookup_imports`

Make by_handler_key import the module, which is what the rewritten guard forbids

- File: `src/cratekit/cli/registry.py`
- Source: `u42-author-round-2.json`, row `R2_handler_lookup_imports`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 997 against a baseline of 997
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_handler_key_resolves_without_importing_the_module`

Old text:

```
def by_handler_key(key: str) -> Entry:
```

New text:

```
def by_handler_key(key: str) -> Entry:
    import importlib

    importlib.import_module("cratekit.acquire.cli")
```

### `u42-author.R1_planned_marker_returns`

Restore planned_in on acquire.download, which is the state that hid rows 6 and 7

- File: `src/cratekit/cli/registry.py`
- Source: `u42-author.json`, row `R1_planned_marker_returns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_cutover_parity.py`, `tests/test_cli_contract.py`
- Collected: 1026 against a baseline of 1029
- Kills: 7 (collect-error)
- Note: collection changed: 1026 collected against a baseline of 1029. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_acquire_cli.py::test_download_argv_round_trips_the_frozen_payload_and_carries_no_run`
  - `tests/test_acquire_cli.py::test_download_on_an_absent_job_refuses_with_a_vocabulary_code`
  - `tests/test_acquire_cli.py::test_download_over_an_absent_list_refuses_by_name`
  - `tests/test_acquire_cli.py::test_download_reaches_no_provider_and_no_network`
  - `tests/test_acquire_cli.py::test_the_verb_appears_in_help_and_dispatches[acquire.download]`
  - `tests/test_acquire_cli.py::test_the_verb_is_landed_rather_than_planned[acquire.download]`
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`

Old text:

```
        doctor_checks=("credential.provider", "binary.ffmpeg"),
        # U42 LANDED IT.
```

New text:

```
        doctor_checks=("credential.provider", "binary.ffmpeg"),
        planned_in="U15",
        # U42 LANDED IT.
```

### `u43-author-light.R1_marker_restored`

The planned_in marker is put back on the setbuild entry, which withdraws the verb from every conformance property that only drives landed entries

- File: `src/cratekit/cli/registry.py`
- Source: `u43-author-light.json`, row `R1_marker_restored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4181 against a baseline of 4185
- Kills: 33 (collect-error)
- Note: collection changed: 4181 collected against a baseline of 4185. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
  - `tests/test_cutover_parity.py::test_the_cutover_is_mechanically_possible_and_says_what_is_left`
  - `tests/test_cutover_parity.py::test_the_parity_table_renders_for_a_person`
  - `tests/test_setbuilder_cli.py::test_a_cache_that_cannot_be_written_does_not_cost_the_set`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_the_parsers_verdict_and_not_a_refusal`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_the_parsers_verdict`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_a_lossy_marked_companion_comes_back_with_a_clean_title`
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[path]`
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[unowned]`
  - `tests/test_setbuilder_cli.py::test_a_name_the_library_does_not_hold_refuses_as_not_indexed`
  - `tests/test_setbuilder_cli.py::test_a_path_anchor_is_unchanged_by_the_unowned_form`
  - `tests/test_setbuilder_cli.py::test_a_path_and_an_unowned_label_together_are_the_parsers_verdict`
  - `tests/test_setbuilder_cli.py::test_a_second_run_reads_no_tag_it_already_holds`
  - `tests/test_setbuilder_cli.py::test_a_supplied_key_beside_a_name_refuses_rather_than_being_ignored`
  - ... and 18 more, see the JSON sidecar

Old text:

```
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        # U43 LANDED IT.
```

New text:

```
        emits=frozenset({"plan"}),
        output_schema="plan/1",
        planned_in="U35",
        # U43 LANDED IT.
```

### `u44-author.D1_registry_drops_long_running`

Remove long_running from the master entry, which should shrink two derived populations

- File: `src/cratekit/cli/registry.py`
- Source: `u44-author.json`, row `D1_registry_drops_long_running`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4257 against a baseline of 4258
- Kills: 2 (collect-error)
- Note: collection changed: 4257 collected against a baseline of 4258. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_verb_carrying_a_resume_argv_builder_declares_that_it_queues`
  - `tests/test_master_cli.py::test_the_entry_is_landed_and_declares_no_gate`

Old text:

```
        argv_builder="master_argv",
        long_running=True,
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("binary.ffmpeg",),
```

New text:

```
        argv_builder="master_argv",
        emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        writes=frozenset({"files"}),
        destructive=True,
        doctor_checks=("binary.ffmpeg",),
```

### `u45-round-1.V3_marker_restored`

Put planned_in back, so the verb reads as unlanded and every conformance property stops arming against it

- File: `src/cratekit/cli/registry.py`
- Source: `u45-round-1.json`, row `V3_marker_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4377 against a baseline of 4381
- Kills: 58 (collect-error)
- Note: collection changed: 4377 collected against a baseline of 4381. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[cancelled]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[failed]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[succeeded]`
  - `tests/test_backup_cli.py::test_a_backup_to_a_destination_nobody_is_backing_up_to_is_its_own_job`
  - `tests/test_backup_cli.py::test_a_contained_analysis_share_draws_no_warning_from_the_verb`
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_job_queued_before_the_worker_existed_refuses_rather_than_succeeding`
  - `tests/test_backup_cli.py::test_a_job_that_can_never_run_does_not_stand_in_for_a_backup`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_library_with_an_identity_draws_no_such_warning`
  - ... and 43 more, see the JSON sidecar

Old text:

```
        doctor_checks=("library.mounted", "binary.rclone"),
        # U45 LANDED IT.
```

New text:

```
        doctor_checks=("library.mounted", "binary.rclone"),
        planned_in="U35",
        # U45 LANDED IT.
```

### `u45-round-1.V5_module_toggle_dropped`

Drop the module toggle, so the verb is offered on a slim install that has no backup module

- File: `src/cratekit/cli/registry.py`
- Source: `u45-round-1.json`, row `V5_module_toggle_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4380 against a baseline of 4381
- Kills: 6 (collect-error)
- Note: collection changed: 4380 collected against a baseline of 4381. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_backup_cli.py::test_the_verb_is_declared_landed_and_names_this_module`
  - `tests/test_backup_cli.py::test_the_verb_is_offered_on_the_full_profile_and_withheld_on_the_slim_one`
  - `tests/test_cli_contract.py::test_every_declared_module_toggle_is_used_by_at_least_one_verb`
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`
  - `tests/test_cli_contract.py::test_every_live_toggle_is_driven_by_the_toggle_test_below`
  - `tests/test_doctor.py::test_a_binary_no_enabled_verb_needs_is_a_note_rather_than_a_failure`

Old text:

```
        source_scripts=("backup.sh",),
        module_id="backup",
```

New text:

```
        source_scripts=("backup.sh",),
```

### `u69-b.M20_registry_schema`

Declare the verb plan/1 in the registry, which the human renderer does not show

- File: `src/cratekit/cli/registry.py`
- Source: `u69-b.json`, row `M20_registry_schema`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_cli_contract.py`
- Collected: 1069 against a baseline of 1069
- Kills: 43 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_credited_row_never_withholds_another_remix_of_the_recording`
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_a_job_of_another_verb_in_the_same_run_is_not_listed`
  - `tests/test_intake_missing.py::test_a_job_queued_by_hand_is_not_part_of_any_run`
  - `tests/test_intake_missing.py::test_a_job_with_nothing_missing_does_not_need_the_library`
  - `tests/test_intake_missing.py::test_a_job_with_nothing_missing_is_no_op_and_writes_nothing`
  - `tests/test_intake_missing.py::test_a_missing_row_from_no_provider_is_reported_unlisted_as_a_failing_check`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_rejection_after_a_listing_refuses_over_the_earlier_list_and_says_why`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_row_tombstoned_since_the_job_is_not_listed_and_counted_suppressed`
  - `tests/test_intake_missing.py::test_a_run_asks_each_missing_row_again_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_run_list_is_one_file_a_second_listing_reproduces`
  - ... and 28 more, see the JSON sidecar

Old text:

```
        # nothing else, and the one thing a person needs from this verb is the
        # list's path and the command that downloads it (R-400).
        emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
```

New text:

```
        # nothing else, and the one thing a person needs from this verb is the
        # list's path and the command that downloads it (R-400).
        emits=frozenset({"plan"}),
        output_schema="plan/1",
```

### `u72.M8_registry_digest_source`

The registry gate declares no digest source

- File: `src/cratekit/cli/registry.py`
- Source: `u72.json`, row `M8_registry_digest_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 48 against a baseline of 48
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_over_a_usable_export_reaches_the_gate_with_the_digest_it_had_before`
  - `tests/test_intake_land.py::test_a_stale_answer_is_refused_and_moves_nothing`
  - `tests/test_intake_land.py::test_a_stale_answer_stays_stale_over_an_export_that_is_not_there`
  - `tests/test_intake_land.py::test_an_answer_given_against_one_export_is_stale_for_another`
  - `tests/test_intake_land.py::test_an_answer_given_against_one_manifest_is_stale_once_it_is_rewritten`
  - `tests/test_intake_land.py::test_an_answer_given_for_one_batch_name_is_stale_for_another`
  - `tests/test_intake_land.py::test_an_answer_given_for_one_folder_is_stale_for_another_holding_the_same_names`

Old text:

```
                prompt="Move these files into the library and write the intake file?",
                digest_source="plan",
```

New text:

```
                prompt="Move these files into the library and write the intake file?",
```

### `u91.G1_registry_xml`

registry route.unplaced: declare no write surface, so doctor and conformance 8 no longer see the xml write

- File: `src/cratekit/cli/registry.py`
- Source: `u91.json`, row `G1_registry_xml`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_cli_contract.py`
- Collected: 1194 against a baseline of 1194
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_declares_no_write_and_needs_only_what_a_read_needs`

Old text:

```
        writes=frozenset({"xml"}),
        taxonomy_terms=("genre_energy",),
```

New text:

```
        taxonomy_terms=("genre_energy",),
```

### `u96-b.B1_no_library_check_declared`

registry: declare library.mounted on the recovery verb, a check it needs to FAIL

- File: `src/cratekit/cli/registry.py`
- Source: `u96-b.json`, row `B1_no_library_check_declared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_cli_contract.py`
- Collected: 1095 against a baseline of 1095
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_recovery_verb_declares_no_gate_and_no_check_it_needs_to_fail`

Old text:

```
        doctor_checks=("rekordbox.closed",),
        # U96.
```

New text:

```
        doctor_checks=("rekordbox.closed", "library.mounted"),
        # U96.
```

### `u27-reports-round-1.S1_limit_floor`

Pass the limit through unfloored, so a negative one becomes a slice from the end

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S1_limit_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_negative_limit_is_read_as_zero_rather_than_as_a_slice_from_the_end`

Old text:

```
    limit = max(0, int(ctx.args.limit))
```

New text:

```
    limit = int(ctx.args.limit)
```

### `u27-reports-round-1.S2_truncation_row`

Drop the row that says the list was capped

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S2_truncation_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_limit_of_zero_lists_nothing_and_still_counts_everything`
  - `tests/test_reports_cli.py::test_a_limit_that_drops_rows_says_so_and_still_reports_the_true_total`

Old text:

```
    if len(listed) < len(report.uncovered):
        findings.append(
            Finding(
                key="coverage.truncated",
                title="the list above is not the whole answer",
                status=Status.INFO,
                detail=(
                    f"{len(listed)} of {len(report.uncovered)} uncovered tracks "
                    f"are listed; raise the limit to see the rest"
                ),
            )
        )

```

New text:

```
(empty)
```

### `u27-reports-round-1.S3_summary_total`

Derive the summary total from the truncated list, the arithmetic that hides the cap

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S3_summary_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_limit_of_zero_lists_nothing_and_still_counts_everything`
  - `tests/test_reports_cli.py::test_a_limit_that_drops_rows_says_so_and_still_reports_the_true_total`

Old text:

```
            "uncovered": len(report.uncovered),
```

New text:

```
            "uncovered": len(listed),
```

### `u27-reports-round-2.S5_handler_key_wrong`

Round 1's S5 was inert because the engine default matched; pass a WRONG key instead

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-2.json`, row `S5_handler_key_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_duplicates_offers_the_pair_into_the_queue_under_its_own_handler_key`
  - `tests/test_reports_cli.py::test_the_shell_passes_the_REGISTRY_key_rather_than_letting_the_engine_default`

Old text:

```
            view, store, template=_template(cfg), handler_key=ctx.entry.handler_key
```

New text:

```
            view, store, template=_template(cfg), handler_key="duplicates"
```

### `u27-reports-round-3-fixes.F1_as_of_falsiness`

Restore the falsiness test, so an explicitly empty as-of is read as an absent flag

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-3-fixes.json`, row `F1_as_of_falsiness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_an_explicitly_empty_as_of_refuses_rather_than_answering_for_today`

Old text:

```
    if written is None:
```

New text:

```
    if not written:
```

### `u27-reports-round-3-fixes.F5_gap_row_flood`

Render one gap row per declared bucket again when the governed tree is absent

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-3-fixes.json`, row `F5_gap_row_flood`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_missing_tree_is_named_once_rather_than_as_a_row_per_bucket`

Old text:

```
    if stats.shape.folders == 0:
```

New text:

```
    if False:
```

### `r679-a.E1_cli_offers_every_verdict`

review resolve: offer the whole enum as --verdict choices

- File: `src/cratekit/cli/review.py`
- Source: `r679-a.json`, row `E1_cli_offers_every_verdict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_review_queue.py::test_the_command_line_offers_a_person_only_the_persons_verdicts`

Old text:

```
        choices=tuple(str(member) for member in review.PERSON_VERDICTS),
```

New text:

```
        choices=tuple(str(member) for member in review.Verdict),
```

### `r679-a.E2_listing_drops_the_actor`

review list: leave the actor out of the listing, so a superseded row shows no rule

- File: `src/cratekit/cli/review.py`
- Source: `r679-a.json`, row `E2_listing_drops_the_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`

Old text:

```
        "option": item.option,
        "actor": item.actor,
    }
```

New text:

```
        "option": item.option,
    }
```

### `r790-d.V1_group_page_refusal`

_list_grouped: accept --after and --limit and ignore them

- File: `src/cratekit/cli/review.py`
- Source: `r790-d.json`, row `V1_group_page_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_review_queue.py`
- Collected: 201 against a baseline of 201
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_page_limit_with_a_grouping_refuses_rather_than_being_ignored`
  - `tests/test_label_offer_window.py::test_grouping_needs_a_queue_and_has_no_pages`

Old text:

```
    if not ctx.args.queue or ctx.args.after is not None or ctx.args.limit is not None:
```

New text:

```
    if not ctx.args.queue:
```

