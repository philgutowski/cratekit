# Mutation table: u335-after-03

Measured by `scripts/mutate.py` on 2026-11-24 06:17 UTC, branch `HEAD` at `1a401a39`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23223 collected. pytest invocations for this batch: 286.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 06:17 UTC for commit `1a401a39247d`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 70, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23223 against 23223. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u272.C4_full_flush_never_asked` | `src/cratekit/core/config.py` | user | 7 file(s) | 642 | 5 | killed |
| `u272.C6_no_plain_sync` | `src/cratekit/core/config.py` | user | 7 file(s) | 642 | 12 | killed |
| `u298.H11_read_json_refuses_garbage` | `src/cratekit/core/config.py` | user | 2 file(s) | 353 | 4 | killed |
| `u331.S04_membership_ignores_explicit_toggles` | `src/cratekit/core/config_schema.py` | user | 3 file(s) | 466 | 2 | killed |
| `r1991.C1_claimed_node_rebound` | `src/cratekit/core/convergence.py` | user | 19 file(s) | 1152 | 1 | killed |
| `r1991.C2_bound_destination_moved` | `src/cratekit/core/convergence.py` | user | 19 file(s) | 1152 | 1 | killed |
| `r1991.C3_keep_recorded_ignored` | `src/cratekit/core/convergence.py` | user | 19 file(s) | 1152 | 2 | killed |
| `u93-recursive-analysis.D12_parent_id` | `src/cratekit/core/discovery.py` | maintainer | 2 file(s) | 69 | 3 | killed |
| `u93-recursive-analysis.D15_unreadable_empty` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 69 | 8 | killed |
| `u93-recursive-analysis.D16_none_filter` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 69 | 30 | killed |
| `u93-recursive-analysis.D1_dotfile` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 69 | 2 | killed |
| `u93-recursive-analysis.D20_frozen_links` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 69 | 2 | killed |
| `u93-recursive-analysis.D4_default_mode` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 69 | 3 | killed |
| `u93-recursive-analysis.D5_dot_directory` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 69 | 2 | killed |
| `u93-recursive-analysis.D6_link_declined` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 69 | 6 | killed |
| `u93-recursive-analysis.D7_prune_in_place` | `src/cratekit/core/discovery.py` | user | 2 file(s) | 69 | 2 | killed |
| `r290-author.J1_blocked_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2532 | 49 | killed |
| `r290-author.J2_blocked_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2532 | 48 | killed |
| `r290-author.J3_closed_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2532 | 109 | killed |
| `r290-author.J4_predicate_narrowed_to_failed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2532 | 29 | killed |
| `r290-author.J7_cancelled_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2532 | 25 | killed |
| `r290-author.S11_tagging_shell_call_removed` | `src/cratekit/core/jobs.py` | user | 5 file(s) | 349 | 48 | killed |
| `u140.B3_refreeze_any_state` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B4_refreeze_writes_nothing_new` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 29 | 7 | killed |
| `u227.R16_join_state` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 130 | 5 | killed |
| `u227.R17_join_held` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 130 | 1 | killed |
| `u227.R18_join_blank` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 130 | 1 | killed |
| `u298.H16_reported_extra_under_progress` | `src/cratekit/core/jobs.py` | user | 18 file(s) | 1400 | 122 | killed |
| `u298.H21_advance_refuses_empty` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 131 | 3 | killed |
| `u331.S16_item_path_reexport_joins_plainly` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 270 | 84 | killed |
| `u56-catalogue-searcher-and-tag-workers.R34_empty_job_is_driven` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R35_extra_rides_beside_progress` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 47 | killed |
| `r740-a.N1_no_fill` | `src/cratekit/core/naming.py` | user | 4 file(s) | 249 | 17 | killed |
| `r740-a.N5_no_marker_fill` | `src/cratekit/core/naming.py` | user | 4 file(s) | 249 | 4 | killed |
| `u293.L1_dead_mark_charged` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 3 | killed |
| `u293.L2_night_reset` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 4 | killed |
| `u293.L3_spent_off_by_one` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 2 | killed |
| `u293.L5_close_adds_to_night` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 1 | killed |
| `u27-round-8-independent.E4_path_missing_reads_ok` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 738 | 4 | killed |
| `u27-round-8-independent.E5_unmounted_reads_foreign` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 738 | 5 | killed |
| `u211.P10_read_rekordbox_is_running` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 5 | killed |
| `u211.P11_unconfirmed_is_not_absent` | `src/cratekit/core/processes.py` | user | 3 file(s) | 109 | 11 | killed |
| `u211.P12_careful_pid_refuses` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 8 | killed |
| `u211.P1_denied_is_skipped` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 1 | killed |
| `u211.P2_gone_is_skipped` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 1 | killed |
| `u211.P3_recheck_before_refusing` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 9 | killed |
| `u211.P4_zombie_status_reads_zombie` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 8 | killed |
| `u211.P5_gone_on_status_read` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 1 | killed |
| `u211.P6_unreadable_status_is_not_gone` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 2 | killed |
| `u211.P7_unreadable_refuses` | `src/cratekit/core/processes.py` | user | 3 file(s) | 109 | 17 | killed |
| `u211.P8_unreadable_pid_list_refuses` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 1 | killed |
| `u211.P9_whole_list_walked` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 3 | killed |
| `u278.M9_continue_names_no_hour` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 250 | 3 | killed |
| `u293.G5_line_held_to_ceiling` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 283 | 5 | killed |
| `u293.G8_line_exported` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 283 | 2 | killed |
| `u329.A1_writer_accessor_returns_a_part` | `src/cratekit/core/rb_call_time.py` | user | 5 file(s) | 363 | 197 | killed |
| `r746-a.G3_content_row_admitted_without_asking` | `src/cratekit/core/rb_changes.py` | user | 3 file(s) | 279 | 5 | killed |
| `u288.M1_delete_admitted_by_any_name` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 296 | 2 | killed |
| `u300.S11_registry_changes_local` | `src/cratekit/core/rb_changes.py` | maintainer | 1 file(s) | 22 | 4 | killed |
| `u329.P1_rb_changes_wrong_family` | `src/cratekit/core/rb_changes.py` | user | 5 file(s) | 449 | 201 | killed |
| `r1665-b.C1_w5_composite` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 2 | killed |
| `r1665.W1_check_opens_the_capture` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 18 | killed |
| `r1665.W2_failed_copy_passes` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.W4_quick_check_ignored` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 1 | killed |
| `r1665.W6_refused_open_passes` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 2 | killed |
| `r1677.R1_raise_after_copy` | `src/cratekit/core/rb_copies.py` | user | 4 file(s) | 123 | 1 | killed |
| `r1677.R3_copied_never_set` | `src/cratekit/core/rb_copies.py` | user | 4 file(s) | 123 | 1 | killed |
| `u329.P2_rb_copies_wrong_family` | `src/cratekit/core/rb_copies.py` | user | 5 file(s) | 164 | 83 | killed |
| `u288.M15_append_past_highest` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 96 | 2 | killed |
| `u211.W1_writer_falls_back` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 271 | 15 | killed |
| `u211.W3_strict_at_commit` | `src/cratekit/core/rb_probes.py` | user | 2 file(s) | 259 | 2 | killed |
| `u211.W7_writer_unconfirmed_with_nothing_read` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 271 | 2 | killed |
| `u329.P4_rb_probes_wrong_family` | `src/cratekit/core/rb_probes.py` | user | 5 file(s) | 326 | 41 | killed |
| `r1830.M10_planned_number_not_asked` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 83 | 1 | killed |
| `r1830.M17_positions_never_read` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 83 | 21 | killed |
| `r1830.M23_unreadable_marker_passed_over` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 83 | 1 | killed |
| `r1830.M2_marked_removed_row_counted` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 296 | 3 | killed |
| `r1830.M4_one_place_whatever_removed` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 296 | 3 | killed |
| `r1830.M5_any_playlist_counts` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 296 | 19 | killed |
| `r1830.M9_moved_row_not_refused` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 83 | 1 | killed |
| `u288.M10_changed_rows` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 296 | 8 | killed |
| `u288.M12_still_names` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 296 | 1 | killed |
| `u288.M3_unmeasured_tables_skipped` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 83 | 3 | killed |
| `u288.M4_target_id_not_asked` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 83 | 1 | killed |
| `u288.M8_memberships_kept` | `src/cratekit/core/rb_removal.py` | user | 1 file(s) | 83 | 28 | killed |
| `u329.P5_rb_removal_wrong_family` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 307 | 53 | killed |
| `u955.S01_update_omits_usn` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 19 | killed |
| `u955.S02_update_omits_time` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 19 | killed |
| `u955.S03_count_one_short` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 19 | killed |
| `u955.S04_trackno_guard_dropped` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 1 | killed |
| `u955.S05_prediction_one_past` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 17 | killed |
| `u955.S06_prediction_ignores_buffer` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 20 | killed |
| `u955.S08_time_form_no_space` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 23 | killed |
| `u955.S11_rest_digest_keeps_stamps` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 18 | killed |
| `u955.S12_stamps_not_read` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 18 | killed |
| `u955.S15_stamp_rule_skipped` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 12 | killed |
| `u955.S23_read_back_count_unchecked` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 2 | killed |
| `u955.S24_precommit_recheck_dropped` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 2 | killed |
| `r923.N19_default_is_an_analysis_column` | `src/cratekit/core/rb_tables.py` | user | 41 file(s) | 3808 | 35 | killed |
| `r1830.M21_record_omits_the_rows` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 83 | 1 | killed |
| `r1830.M6_prepare_plans_no_renumbering` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 83 | 23 | killed |
| `r239-a.A1_probe_to_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 122 | killed |
| `r239-a.A2_probe_to_false` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 7 | killed |
| `r239-a.A3_probe_removed` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 7 | killed |
| `r239-a.A4_open_default_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 121 | killed |
| `r239-a.A7_needed_always_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 122 | killed |
| `r239-a.A8_needed_always_false` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 8 | killed |
| `r239-a.A9_header_nearby_value` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 122 | killed |
| `r375-c.W1_listener_left_on_the_handle` | `src/cratekit/core/rb_writer.py` | maintainer | 2 file(s) | 86 | 1 | killed |
| `r375-c.W2_witness_listens_one_event_early` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 86 | 2 | killed |
| `r746-a.G4_read_back_walks_session_new_only` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 66 | 2 | killed |
| `u211.W4_probe_wrapped_at_commit` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 335 | 20 | killed |
| `u211.W5_probe_wrapped_at_open` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 335 | 76 | killed |
| `u288.M5_prepare_liveness` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 83 | 2 | killed |
| `u288.M6_prepare_unmeasured_refusal` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 83 | 3 | killed |
| `u288.M7_prepare_identity` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 83 | 1 | killed |
| `u59.M9_column_repointed` | `src/cratekit/core/rb_writer.py` | user | 22 file(s) | 2744 | 176 | killed |
| `u953.M8_live_row_or_becomes_and` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 340 | 2 | killed |
| `u955.S25_stamp_before_deletes` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 337 | 18 | killed |
| `u955.S26_confinement_given_no_stamp` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 337 | 23 | killed |
| `r1665.R1_log_not_restored` | `src/cratekit/core/restore.py` | user | 7 file(s) | 316 | 4 | killed |
| `r1924.R1_later_sessions_read` | `src/cratekit/core/restore.py` | user | 4 file(s) | 411 | 4 | killed |
| `r1924.R2_uncommitted_read` | `src/cratekit/core/restore.py` | user | 4 file(s) | 411 | 2 | killed |
| `r1924.R3_after_the_database` | `src/cratekit/core/restore.py` | user | 4 file(s) | 411 | 1 | killed |
| `r1924.R4_dry_run_passed` | `src/cratekit/core/restore.py` | user | 4 file(s) | 411 | 2 | killed |
| `u953.M14_spendable_capture_skips_the_sources` | `src/cratekit/core/restore.py` | user | 1 file(s) | 23 | 1 | killed |
| `r1924.T10_blank_is_cleared` | `src/cratekit/core/restore_tags.py` | user | 4 file(s) | 411 | 12 | killed |
| `r1924.T11_both_halves_written` | `src/cratekit/core/restore_tags.py` | user | 4 file(s) | 411 | 12 | killed |
| `r1924.T14_dry_run_writes` | `src/cratekit/core/restore_tags.py` | user | 4 file(s) | 411 | 3 | killed |
| `r1924.T15_only_what_differs` | `src/cratekit/core/restore_tags.py` | user | 4 file(s) | 411 | 2 | killed |
| `r1924.T16_write_failure_counted` | `src/cratekit/core/restore_tags.py` | user | 4 file(s) | 411 | 3 | killed |
| `r1924.T18_unwritten_includes_wrong` | `src/cratekit/core/restore_tags.py` | user | 4 file(s) | 411 | 2 | killed |
| `u339.M19_restore_per_field` | `src/cratekit/core/restore_tags.py` | user | 2 file(s) | 95 | 3 | killed |
| `r431-a.A6_a_standing_companion_is_rewritten` | `src/cratekit/core/review.py` | maintainer | 20 file(s) | 3018 | 1 | killed |
| `r431-a.A7_beside_written_when_the_record_stood` | `src/cratekit/core/review.py` | user | 20 file(s) | 3018 | 2 | killed |
| `r431-a.A8_also_is_never_asked` | `src/cratekit/core/review.py` | user | 20 file(s) | 3018 | 6 | killed |
| `r431-a.A9_an_already_lifted_record_is_lifted_again` | `src/cratekit/core/review.py` | maintainer | 20 file(s) | 3018 | 1 | killed |
| `r679-a.A1_supersede_guard_both_layers` | `src/cratekit/core/review.py` | user | 3 file(s) | 834 | 5 | killed |
| `r679-a.A3_supersede_readers_predicate` | `src/cratekit/core/review.py` | user | 3 file(s) | 834 | 1 | killed |
| `r679-a.A8_actor_is_not_the_rule` | `src/cratekit/core/review.py` | user | 3 file(s) | 834 | 11 | killed |
| `u301.R2_revoke_drops_the_actor` | `src/cratekit/core/review.py` | user | 3 file(s) | 226 | 3 | killed |
| `r798-d.K11_the_shared_matcher_reads_a_substring_needle` | `src/cratekit/core/routing.py` | user | 3 file(s) | 1150 | 101 | killed |
| `r799-a.R1_a_table_is_read_only_for_its_source` | `src/cratekit/core/routing.py` | user | 3 file(s) | 511 | 2 | killed |
| `u155.R4_genre_sub_named` | `src/cratekit/core/routing.py` | user | 1 file(s) | 197 | 3 | killed |
| `u340.R01_too_coarse_files` | `src/cratekit/core/routing.py` | user | 2 file(s) | 71 | 4 | killed |
| `u340.R02_fallback_files` | `src/cratekit/core/routing.py` | user | 2 file(s) | 71 | 5 | killed |
| `u340.R03_same_folder` | `src/cratekit/core/routing.py` | user | 3 file(s) | 183 | 4 | killed |
| `u340.R04_first_files_nowhere` | `src/cratekit/core/routing.py` | user | 2 file(s) | 71 | 3 | killed |
| `r1255.S1_scan_unlisted_as_empty` | `src/cratekit/core/session.py` | user | 7 file(s) | 867 | 14 | killed |
| `r1255.S2_absent_log_unread` | `src/cratekit/core/session.py` | user | 7 file(s) | 867 | 46 | killed |
| `r1255.S3_log_file_absent` | `src/cratekit/core/session.py` | user | 2 file(s) | 432 | 1 | killed |
| `r1255.S4_under_a_file_unread` | `src/cratekit/core/session.py` | user | 2 file(s) | 432 | 1 | killed |
| `r1255.S5_json_filter` | `src/cratekit/core/session.py` | user | 7 file(s) | 867 | 1 | killed |
| `r1255.S6_records_refuses_unlisted` | `src/cratekit/core/session.py` | user | 4 file(s) | 628 | 4 | killed |
| `r1255.S7_log_unlisted_predicate` | `src/cratekit/core/session.py` | user | 4 file(s) | 143 | 11 | killed |
| `r1255.S8_clause_listing_wording` | `src/cratekit/core/session.py` | user | 3 file(s) | 116 | 8 | killed |
| `r1255.S9_gate_unlisted_detail` | `src/cratekit/core/session.py` | maintainer | 3 file(s) | 322 | 2 | killed |
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
| `r598-a.A5_holder_never_recorded` | `src/cratekit/core/session.py` | user | 3 file(s) | 602 | 8 | killed |
| `r598-a.A6_record_holder_is_a_second_lookup` | `src/cratekit/core/session.py` | maintainer | 2 file(s) | 185 | 1 | killed |
| `u138.E1_terminal_check` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4050 | 4 | killed |
| `u138.S11_rule_not_written` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4050 | 4 | killed |
| `u138.S12_message_names_the_portion` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4050 | 4 | killed |
| `u138.S13_remedy_points_back_at_ack` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4050 | 8 | killed |
| `u138.S1_session_rule_gone` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4050 | 20 | killed |
| `u138.S2_any_answer_gets_the_age_rule` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4050 | 13 | killed |
| `u138.S3_stale_not_refused` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4050 | 10 | killed |
| `u138.S6_bound_six_days` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4050 | 5 | killed |
| `u138.S8_rule_not_recorded` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4050 | 6 | killed |
| `u138.S9_answer_not_recorded` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4050 | 4 | killed |
| `u300.S15_terminal_probe_local` | `src/cratekit/core/session_ack.py` | maintainer | 2 file(s) | 185 | 10 | killed |
| `u300.S16_derive_actor_local` | `src/cratekit/core/session_ack.py` | maintainer | 2 file(s) | 185 | 1 | killed |
| `u329.P6_session_ack_wrong_family` | `src/cratekit/core/session_ack.py` | user | 5 file(s) | 362 | 69 | killed |
| `u48-author.S1_remedy_fixed_at_repair` | `src/cratekit/core/session_ack.py` | user | 11 file(s) | 1535 | 1 | killed |
| `u48-author.S2_remedy_fixed_at_grant` | `src/cratekit/core/session_ack.py` | user | 11 file(s) | 1535 | 2 | killed |
| `u329.A2_session_accessor_returns_the_writer` | `src/cratekit/core/session_call_time.py` | user | 4 file(s) | 542 | 210 | killed |
| `r598-a.A1_state_check_widened_to_non_terminal` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 4 | killed |
| `r598-a.A2_no_holder_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r598-a.A3_liveness_not_consulted` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 8 | killed |
| `r598-a.A4_unreadable_holder_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r598-a.A7_sweep_ignores_the_shown_list` | `src/cratekit/core/session_holders.py` | user | 2 file(s) | 185 | 1 | killed |
| `r598-b.B7_sample_live_holder_released` | `src/cratekit/core/session_holders.py` | user | 2 file(s) | 185 | 4 | killed |
| `r647-a.B10_live_identifier_not_asked` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B11_start_time_compared_again` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B12_cross_boot_never_judged` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 4 | killed |
| `r647-a.B13_current_holder_names_no_machine` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B14_machine_not_read_back` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 5 | killed |
| `r647-a.B15_machine_not_written` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 5 | killed |
| `r647-a.B1_unknown_machine_not_refused` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B2_machine_equality_dropped` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 3 | killed |
| `r647-a.B3_unparsable_boot_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B4_infinite_boot_accepted` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B5_drift_margin_halved` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 2 | killed |
| `r647-a.B6_drift_margin_doubled` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B7_margin_boundary_exclusive` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B8_direction_ignored` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `r647-a.B9_platform_silence_read_as_gone` | `src/cratekit/core/session_holders.py` | user | 3 file(s) | 602 | 1 | killed |
| `u300.S13_process_exists_local` | `src/cratekit/core/session_holders.py` | maintainer | 2 file(s) | 185 | 1 | killed |
| `u329.P7_session_holders_wrong_family` | `src/cratekit/core/session_holders.py` | user | 5 file(s) | 708 | 81 | killed |
| `u49-author.L4_a_malformed_holder_raises_again` | `src/cratekit/core/session_holders.py` | user | 13 file(s) | 2592 | 1 | killed |
| `r44-a.S10_default_slug` | `src/cratekit/core/session_volumes.py` | maintainer | 2 file(s) | 479 | 1 | killed |
| `r44-a.S1_empty_slot` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 2 | killed |
| `r44-a.S2_proved_widened` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 4 | killed |
| `r44-a.S3_default_to_library` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 2 | killed |
| `r44-a.S4_inside_root_unheld` | `src/cratekit/core/session_volumes.py` | user | 2 file(s) | 479 | 6 | killed |

## Row definitions

### `u272.C4_full_flush_never_asked`

_flush_descriptor: never ask for the full flush, the plain sync on every platform

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C4_full_flush_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 642 against a baseline of 642
- Kills: 5 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[EINVAL]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTSUP]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTTY]`
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one[full-flush-offered]`

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

### `u272.C6_no_plain_sync`

_flush_descriptor: drop the plain sync, so a platform without the full flush flushes nothing

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C6_no_plain_sync`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 642 against a baseline of 642
- Kills: 12 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[EINVAL]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTSUP]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTTY]`
  - `tests/test_snapshot_flush_u272.py::test_a_plain_sync_that_fails_raises`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed`
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one[a-directory]`
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one[no-full-flush]`
  - `tests/test_snapshot_flush_u272.py::test_the_manifest_is_followed_by_a_flush_of_the_directory_that_holds_it`

Old text:

```
                raise
    os.fsync(fd)

```

New text:

```
                raise

```

### `u298.H11_read_json_refuses_garbage`

read_json: a document that is not JSON reads as an empty record

- File: `src/cratekit/core/config.py`
- Source: `u298.json`, row `H11_read_json_refuses_garbage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_config.py`
- Collected: 353 against a baseline of 353
- Kills: 4 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_document_that_cannot_be_read_is_refused_and_never_read_as_empty[empty]`
  - `tests/test_shared_homes.py::test_a_document_that_cannot_be_read_is_refused_and_never_read_as_empty[not-json]`
  - `tests/test_shared_homes.py::test_a_document_that_cannot_be_read_is_refused_and_never_read_as_empty[not-utf-8]`
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

### `u331.S04_membership_ignores_explicit_toggles`

Config.membership: resolve the profile's preset alone, so a toggle the configuration turns on or off is ignored where a feature package reads the membership

- File: `src/cratekit/core/config_schema.py`
- Source: `u331.json`, row `S04_membership_ignores_explicit_toggles`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_sync_all.py`, `tests/test_organize.py`
- Collected: 466 against a baseline of 466
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_the_membership_is_the_profiles_preset_then_the_explicit_toggles`
  - `tests/test_sync_all.py::test_an_explicit_toggle_puts_back_the_source_its_profile_leaves_out`

Old text:

```
        """The resolved membership: the profile's preset, then the explicit toggles."""
        return profiles.resolve(self.profile.name, self.modules.explicit)
```

New text:

```
        """The resolved membership: the profile's preset, then the explicit toggles."""
        return profiles.resolve(self.profile.name, {})
```

### `r1991.C1_claimed_node_rebound`

record_nodes keep_recorded: give a node already bound another destination, so the record is not one to one and raises after the write

- File: `src/cratekit/core/convergence.py`
- Source: `r1991.json`, row `C1_claimed_node_rebound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_analyze_adopt.py`, `tests/test_deferred_routing.py`, `tests/test_genre_favorites.py`, `tests/test_organize_inspiration.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_restore.py`, `tests/test_second_genre.py`, `tests/test_sync_pair_back.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_unrecorded_genre_folder.py`
- Collected: 1152 against a baseline of 1152
- Kills: 1 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_the_writer_gives_no_node_a_second_destination`

Old text:

```
        if destination in taken or node in claimed:
```

New text:

```
        if destination in taken:
```

### `r1991.C2_bound_destination_moved`

record_nodes keep_recorded: move a destination the record already binds to the node adoption filed into

- File: `src/cratekit/core/convergence.py`
- Source: `r1991.json`, row `C2_bound_destination_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_analyze_adopt.py`, `tests/test_deferred_routing.py`, `tests/test_genre_favorites.py`, `tests/test_organize_inspiration.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_restore.py`, `tests/test_second_genre.py`, `tests/test_sync_pair_back.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_unrecorded_genre_folder.py`
- Collected: 1152 against a baseline of 1152
- Kills: 1 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_the_writer_never_moves_a_destination_the_record_already_binds`

Old text:

```
        if destination in taken or node in claimed:
```

New text:

```
        if node in claimed:
```

### `r1991.C3_keep_recorded_ignored`

record_nodes: keep_recorded filters nothing, so it merges as a plain record would

- File: `src/cratekit/core/convergence.py`
- Source: `r1991.json`, row `C3_keep_recorded_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_analyze_adopt.py`, `tests/test_deferred_routing.py`, `tests/test_genre_favorites.py`, `tests/test_organize_inspiration.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_restore.py`, `tests/test_second_genre.py`, `tests/test_sync_pair_back.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_unrecorded_genre_folder.py`
- Collected: 1152 against a baseline of 1152
- Kills: 2 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_the_writer_gives_no_node_a_second_destination`
  - `tests/test_unrecorded_genre_folder.py::test_the_writer_never_moves_a_destination_the_record_already_binds`

Old text:

```
            nodes = _unrecorded(current, nodes)

```

New text:

```
            nodes = list(nodes)

```

### `u93-recursive-analysis.D12_parent_id`

Drop the dot dot clause from item_path, so an id walks out of the frozen folder

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D12_parent_id`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 69 against a baseline of 69
- Kills: 3 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_parent_segment_is_refused`
  - `tests/test_discovery.py::test_the_refusal_names_the_folder_it_was_leaving`
  - `tests/test_vocals_cli.py::test_a_vocals_item_that_would_leave_the_frozen_folder_is_refused`

Old text:

```
    if candidate.is_absolute() or ".." in candidate.parts:
        raise _escapes(folder, item_id)
```

New text:

```
    if candidate.is_absolute():
        raise _escapes(folder, item_id)
```

### `u93-recursive-analysis.D15_unreadable_empty`

unreadable_warning reports over an empty list, the same false omission on the other code

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D15_unreadable_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 69 against a baseline of 69
- Kills: 8 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_payload_from_a_build_that_never_walked_a_tree_says_nothing`
  - `tests/test_discovery.py::test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising`
  - `tests/test_discovery.py::test_a_resume_says_what_the_queue_said_from_the_payload_alone`
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`
  - `tests/test_discovery.py::test_there_is_nothing_to_say_when_no_link_was_declined`
  - `tests/test_vocals_cli.py::test_a_one_level_vocals_resume_says_nothing_about_a_walk_it_never_did`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    """What a recursive walk could not list, phrased for an envelope."""
    if not paths:
        return None

```

New text:

```
    """What a recursive walk could not list, phrased for an envelope."""

```

### `u93-recursive-analysis.D16_none_filter`

walk_warnings stops dropping the Nones, so an envelope carries a null warning

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D16_none_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 69 against a baseline of 69
- Kills: 30 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_payload_from_a_build_that_never_walked_a_tree_says_nothing`
  - `tests/test_discovery.py::test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising`
  - `tests/test_discovery.py::test_a_resume_repeats_the_unreadable_half_and_not_only_the_links`
  - `tests/test_discovery.py::test_a_resume_says_what_the_queue_said_from_the_payload_alone`
  - `tests/test_discovery.py::test_an_error_carrying_no_filename_is_still_reported`
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_unreadable_warning_is_its_own_code_with_its_own_remedy`
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`
  - `tests/test_discovery.py::test_there_is_nothing_to_say_when_no_link_was_declined`
  - `tests/test_vocals_cli.py::test_a_file_finalized_with_no_voxlevel_is_scored_once_the_model_is_bound`
  - `tests/test_vocals_cli.py::test_a_folder_with_no_audio_queues_nothing`
  - `tests/test_vocals_cli.py::test_a_nested_file_deleted_after_the_vocals_queue_refuses_that_item_only`
  - `tests/test_vocals_cli.py::test_a_one_level_vocals_resume_says_nothing_about_a_walk_it_never_did`
  - `tests/test_vocals_cli.py::test_a_prefixed_file_is_scored_by_analyze_vocals_and_not_skipped`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_says_which_linked_folders_it_did_not_walk`
  - ... and 15 more, see the JSON sidecar

Old text:

```
    return tuple(one for one in said if one is not None)
```

New text:

```
    return said
```

### `u93-recursive-analysis.D1_dotfile`

Drop the dotfile clause from _is_audio, which is what lets an AppleDouble sidecar become an item

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D1_dotfile`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[appledouble-sidecar-skipped]`
  - `tests/test_vocals_cli.py::test_a_vocals_pass_queues_each_file_its_walk_finds_in_sorted_order[no-sidecar-or-dot-directory]`

Old text:

```
        path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in AUDIO_EXTS
```

New text:

```
        path.is_file()
        and path.suffix.lower() in AUDIO_EXTS
```

### `u93-recursive-analysis.D20_frozen_links`

frozen stops recording the declined links, so the resume has nothing to read back

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D20_frozen_links`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_the_frozen_payload_carries_the_mode_and_both_omissions`
  - `tests/test_vocals_cli.py::test_the_vocals_resume_repeats_what_the_walk_left_out`

Old text:

```
        PAYLOAD_SKIPPED_LINKS: list(scan.skipped_links),
```

New text:

```
        PAYLOAD_SKIPPED_LINKS: [],
```

### `u93-recursive-analysis.D4_default_mode`

Drop the one level early return, so every caller walks the tree whether it asked or not

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D4_default_mode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 69 against a baseline of 69
- Kills: 3 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_one_level_scan_reports_no_links_even_when_one_is_there`
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[one-level-default-skips-a-subfolder]`
  - `tests/test_vocals_cli.py::test_a_vocals_pass_queues_each_file_its_walk_finds_in_sorted_order[one-level-by-default]`

Old text:

```
    if not recursive:
        return Scan(
            items=tuple(sorted(path.name for path in folder.iterdir() if _is_audio(path))),
            skipped_links=(),
            unreadable=(),
        )

```

New text:

```
(empty)
```

### `u93-recursive-analysis.D5_dot_directory`

Stop pruning dot directories, so .Trashes and .Spotlight-V100 are walked

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D5_dot_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[dot-directory-not-descended]`
  - `tests/test_vocals_cli.py::test_a_vocals_pass_queues_each_file_its_walk_finds_in_sorted_order[no-sidecar-or-dot-directory]`

Old text:

```
            if name.startswith("."):
                continue
            if (here / name).is_symlink():
```

New text:

```
            if (here / name).is_symlink():
```

### `u93-recursive-analysis.D6_link_declined`

Walk a directory symlink and report nothing, which is the loop hazard and the silent skip at once

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D6_link_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 69 against a baseline of 69
- Kills: 6 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_symlinked_directory_is_not_walked_and_is_reported`
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_frozen_payload_carries_the_mode_and_both_omissions`
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_says_which_linked_folders_it_did_not_walk`
  - `tests/test_vocals_cli.py::test_the_vocals_resume_repeats_what_the_walk_left_out`

Old text:

```
            if (here / name).is_symlink():
                skipped.append(_relative(folder, here / name))
                continue
            kept.append(name)
```

New text:

```
            kept.append(name)
```

### `u93-recursive-analysis.D7_prune_in_place`

Assign the filtered list to a new name instead of the slice, which leaves os.walk descending everything

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D7_prune_in_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`, `tests/test_vocals_cli.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[dot-directory-not-descended]`
  - `tests/test_vocals_cli.py::test_a_vocals_pass_queues_each_file_its_walk_finds_in_sorted_order[no-sidecar-or-dot-directory]`

Old text:

```
        dirnames[:] = kept
```

New text:

```
        dirnames = kept  # noqa: F841
```

### `r290-author.J1_blocked_branch_removed`

Skip the blocked branch of raise_for_state, so a parked job falls through to the closed predicate that cannot see it, which is R-290 itself

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J1_blocked_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2532 against a baseline of 2532
- Kills: 49 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_blocked_job_raises_the_blocked_type_carrying_the_jobs_own_cause`
  - `tests/test_job_outcome.py::test_a_blocked_job_recording_no_reason_is_still_not_a_success`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - ... and 34 more, see the JSON sidecar

Old text:

```
    if job.state is JobState.BLOCKED:
        # ``transition`` refuses
```

New text:

```
    if False and job.state is JobState.BLOCKED:
        # ``transition`` refuses
```

### `r290-author.J2_blocked_raises_the_plain_type`

Raise a plain CratekitError for a parked job, so the verb exits non zero and the outcome word says failed

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J2_blocked_raises_the_plain_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2532 against a baseline of 2532
- Kills: 48 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_blocked_job_raises_the_blocked_type_carrying_the_jobs_own_cause`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[export.playlist]`
  - ... and 33 more, see the JSON sidecar

Old text:

```
        raise JobBlocked(job.cause)
```

New text:

```
        raise CratekitError(job.cause)
```

### `r290-author.J3_closed_branch_removed`

Drop the closed and carrying a cause branch, so a half failed or cancelled job is reported, which is R-225 in every verb at once

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J3_closed_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2532 against a baseline of 2532
- Kills: 109 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - ... and 94 more, see the JSON sidecar

Old text:

```
    if not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

New text:

```
    if False and not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

### `r290-author.J4_predicate_narrowed_to_failed`

Narrow the closed predicate to FAILED alone, so a run stopped by a signal is reported through a normal envelope

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J4_predicate_narrowed_to_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2532 against a baseline of 2532
- Kills: 29 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.set]`
  - ... and 14 more, see the JSON sidecar

Old text:

```
    if not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

New text:

```
    if job.state is JobState.FAILED and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

### `r290-author.J7_cancelled_raises_the_plain_type`

Raise a plain CratekitError for a cancelled job, so a person who stopped a run is told it failed

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J7_cancelled_raises_the_plain_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2532 against a baseline of 2532
- Kills: 25 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.import]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
            raise JobCancelled(job.cause)
```

New text:

```
            raise CratekitError(job.cause)
```

### `r290-author.S11_tagging_shell_call_removed`

Remove the one jobs.raise_for_state call from tagging/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `S11_tagging_shell_call_removed`
- Moved: U298 replaced the resume tails of tagging.shell.advance, adopt.shell.advance, acquire fallback-fetch and master with core.jobs.resumed, which advance calls; its one raise_for_state call is the mapping each of those four shells made, and tests/test_job_outcome.py names that function as the shared tail. The tests are this row's own plus those of the three rows mapped to it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`, `tests/test_adopt_workers.py`, `tests/test_master_cli.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 349 against a baseline of 349
- Kills: 48 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.retag]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[label.judge]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[master]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[tag.folder]`
  - ... and 33 more, see the JSON sidecar

Old text:

```
    raise_for_state(job)
    return job, warnings
```

New text:

```
    get  # the mapping call, removed
    return job, warnings
```

### `u140.B3_refreeze_any_state`

jobs.refreeze drops the succeeded state check, so a job that may still run is rewritten

- File: `src/cratekit/core/jobs.py`
- Source: `u140.json`, row `B3_refreeze_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_refreeze_refuses_a_job_that_has_not_succeeded`

Old text:

```
        if current.state is not JobState.SUCCEEDED:
            raise refuse(
                "internal-error",
                f"job {job_id} is {current.state}, and only a succeeded job's frozen "

```

New text:

```
        if False:
            raise refuse(
                "internal-error",
                f"job {job_id} is {current.state}, and only a succeeded job's frozen "

```

### `u140.B4_refreeze_writes_nothing_new`

jobs.refreeze writes the payload back without the new value

- File: `src/cratekit/core/jobs.py`
- Source: `u140.json`, row `B4_refreeze_writes_nothing_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 7 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_job_with_no_frozen_name_is_found_by_the_queued_day_and_refrozen`
  - `tests/test_export_set_rename.py::test_a_ledger_left_under_the_old_key_is_moved_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_renamed_inspiration_playlist_renames_the_account_playlist_ledger_and_job`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`

Old text:

```
        payload[key] = str(value)

```

New text:

```
        payload.setdefault(key, str(value))

```

### `u227.R16_join_state`

join_run: write a job in any state, so a running or finished job is moved into a pass

- File: `src/cratekit/core/jobs.py`
- Source: `u227.json`, row `R16_join_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_mirror_downloads.py`, `tests/test_jobs.py`, `tests/test_export_set_rename.py`
- Collected: 130 against a baseline of 130
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[blocked]`
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[cancelled]`
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[failed]`
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[running]`
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[succeeded]`

Old text:

```
        if current.state is not JobState.QUEUED or held:
```

New text:

```
        if held:
```

### `u227.R17_join_held`

join_run: write a job that already carries a run, moving it between passes

- File: `src/cratekit/core/jobs.py`
- Source: `u227.json`, row `R17_join_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_mirror_downloads.py`, `tests/test_jobs.py`, `tests/test_export_set_rename.py`
- Collected: 130 against a baseline of 130
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[has-a-run]`

Old text:

```
        if current.state is not JobState.QUEUED or held:
```

New text:

```
        if current.state is not JobState.QUEUED:
```

### `u227.R18_join_blank`

join_run: accept a blank run

- File: `src/cratekit/core/jobs.py`
- Source: `u227.json`, row `R18_join_blank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_mirror_downloads.py`, `tests/test_jobs.py`, `tests/test_export_set_rename.py`
- Collected: 130 against a baseline of 130
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_join_run_refuses_every_other_job[blank]`

Old text:

```
    if not wanted:
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `u298.H16_reported_extra_under_progress`

reported: a verb's own detail is dropped from progress

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H16_reported_extra_under_progress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_missing.py`, `tests/test_label_genre.py`, `tests/test_label_judge.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_refused.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_vocals_cli.py`
- Collected: 1400 against a baseline of 1400
- Kills: 122 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_mix_url_runs_the_ordinary_set_pipeline_over_the_fetched_file`
  - `tests/intake/test_set_progress.py::test_json_output_carries_no_progress_and_stays_one_document`
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_resolution_with_nothing_missing_names_no_next_command`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_identify_then_set_pays_for_recognition_once_and_the_job_says_it_cost_nothing`
  - `tests/intake/test_workers.py::test_queueing_a_set_identifies_it_and_gives_the_driver_one_item_per_track`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/intake/test_workers.py::test_set_and_identify_write_the_same_tracklist_naming_every_row_in_order`
  - `tests/intake/test_workers.py::test_the_tracklist_is_a_list_the_match_verb_reads_back_row_for_row`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - ... and 107 more, see the JSON sidecar

Old text:

```
    if extra:
        counted.update(extra)
```

New text:

```
(empty)
```

### `u298.H21_advance_refuses_empty`

advance: a job with no items is driven straight to succeeded

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H21_advance_refuses_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_job_queued_with_no_items_refuses_rather_than_reporting_success[adopt.apply]`
  - `tests/test_adopt_workers.py::test_a_job_queued_with_no_items_refuses_rather_than_reporting_success[adopt.scan]`
  - `tests/test_tag_workers.py::test_a_job_with_no_items_is_refused_rather_than_driven`

Old text:

```
    if job.is_open() and not items(store, job.job_id):
```

New text:

```
    if False:
```

### `u331.S16_item_path_reexport_joins_plainly`

jobs: drop the item_path re-export analysis and vocals resolve an item through, so a feature package reaching it through the listed module finds nothing

- File: `src/cratekit/core/jobs.py`
- Source: `u331.json`, row `S16_item_path_reexport_joins_plainly`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 270 against a baseline of 270
- Kills: 84 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_calibrated_level_is_written_and_routes_to_a_band`
  - `tests/test_analysis_workers.py::test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug`
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_corrupt_undo_log_refuses_by_name_rather_than_failing_every_item_as_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_detector_shaped_like_the_batch_fakes_is_accepted`
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone`
  - `tests/test_analysis_workers.py::test_a_file_beside_its_headed_twin_is_measured_where_it_is_and_named_nothing`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_file_whose_level_did_not_move_is_reported_unchanged_and_not_rewritten`
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_job_an_older_build_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_keyless_track_is_a_terminal_skip_with_nothing_written`
  - ... and 69 more, see the JSON sidecar

Old text:

```
    frozen_walk,
    item_path,
    scan_audio,
```

New text:

```
    frozen_walk,
    scan_audio,
```

### `u56-catalogue-searcher-and-tag-workers.R34_empty_job_is_driven`

A job frozen with no items drives straight to SUCCEEDED, which is a clean report over work it never did

- File: `src/cratekit/core/jobs.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R34_empty_job_is_driven`
- Moved: U298 replaced tagging.shell.advance with core.jobs.advance, which the tagging shell imports under the same name; the refusal of an open job with no items is the same check, now one condition, and the mutation drops only its items half
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_job_with_no_items_is_refused_rather_than_driven`

Old text:

```
    if job.is_open() and not items(store, job.job_id):
```

New text:

```
    if job.is_open() and False:
```

### `u56-catalogue-searcher-and-tag-workers.R35_extra_rides_beside_progress`

A per verb detail at the top level is an undeclared field on job_state/1, so a consumer generated from the committed schema rejects every envelope

- File: `src/cratekit/core/jobs.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R35_extra_rides_beside_progress`
- Moved: U298 replaced tagging.shell.reported with core.jobs.reported, which the tagging shell imports under the same name; the same placement of extra under progress, with the local renamed counted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 47 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[-read_back1-no-genre]`
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[Ambient-read_back0-genre-specific]`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - ... and 32 more, see the JSON sidecar

Old text:

```
    counted = dict(progress(store, job.job_id))
    if extra:
        counted.update(extra)
    return {
        "job_id": job.job_id,
```

New text:

```
    counted = dict(progress(store, job.job_id))
    return {
        **dict(extra or {}),
        "job_id": job.job_id,
```

### `r740-a.N1_no_fill`

normalize_spec: never fill a spec field from the stripped head, the R-740 loss itself

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N1_no_fill`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 249 against a baseline of 249
- Kills: 17 (killed)
- Killed:
  - `tests/test_landing_head.py::test_a_second_landing_of_the_same_file_renders_the_same_name`
  - `tests/test_landing_head.py::test_intake_file_names_its_track_from_the_same_head`
  - `tests/test_landing_head.py::test_the_lossy_flag_reported_is_the_one_the_name_was_rendered_from`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[01A - 112 - Ain't Gonna Hurt Nobody.flac-fields0-01A - 112 - Ain't Gonna Hurt Nobody-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields4-05B - 98 - Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields5-05B - 98 - Body-8A]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[08A - 124 - [MP3] Body.flac-fields8-08A - 124 - [MP3] Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields1-08A - 124 - Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields2-08A - 124 - Body-3B]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields3-08A - 124 - Body-Am]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[disagreeing-title-head-leaves-stem-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[key-only-spec-keeps-the-whole-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[marker-in-stripped-head-marks-the-spec]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[no-fields-takes-both-from-the-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[stem-head-fills-when-title-has-none]`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            filled.update(
                (name, value) for name, value in values.items() if current[name] is None
            )
```

New text:

```
            pass
```

### `r740-a.N5_no_marker_fill`

normalize_spec: a marker in the stripped head no longer marks the spec, so R21's marker is dropped

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N5_no_marker_fill`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 249 against a baseline of 249
- Kills: 4 (killed)
- Killed:
  - `tests/test_landing_head.py::test_the_lossy_flag_reported_is_the_one_the_name_was_rendered_from`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[08A - 124 - [MP3] Body.flac-fields8-08A - 124 - [MP3] Body-None]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[marker-in-stripped-head-marks-the-spec]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[marker-only-head-invents-no-field]`

Old text:

```
            if rule.literal in head:
                filled[rule.field] = True
```

New text:

```
            if rule.literal in head:
                pass
```

### `u293.L1_dead_mark_charged`

open_night: a dead firing's mark is not charged, so a crash is a free night

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L1_dead_mark_charged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_dead_firings_mark_from_an_earlier_night_is_charged_to_tonight`
  - `tests/test_provider_gate_night.py::test_a_dead_firings_mark_is_charged_in_full_and_folded_on_a_refusal`
  - `tests/test_sync_night.py::test_a_firing_that_died_is_charged_to_the_next_of_the_same_night`

Old text:

```
        spent += max(0, moved)
```

New text:

```
        spent += 0
```

### `u293.L2_night_reset`

open_night: every firing starts from nothing, whatever the night spent

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L2_night_reset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_second_firing_of_the_night_has_only_what_is_left`
  - `tests/test_provider_gate_night.py::test_a_spent_night_refuses_and_names_when_it_frees`
  - `tests/test_sync_night.py::test_a_firing_that_died_is_charged_to_the_next_of_the_same_night`
  - `tests/test_sync_night.py::test_a_night_already_spent_refuses_before_any_call`

Old text:

```
    spent = ledger.spent if ledger.night == night else 0
    if ledger.open_start is not None:
        # A DEAD
```

New text:

```
    spent = 0
    if ledger.open_start is not None:
        # A DEAD
```

### `u293.L3_spent_off_by_one`

open_night: a night with exactly its budget spent is not refused

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L3_spent_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_spent_night_refuses_and_names_when_it_frees`
  - `tests/test_sync_night.py::test_a_night_already_spent_refuses_before_any_call`

Old text:

```
    if spent >= budget:
```

New text:

```
    if spent > budget:
```

### `u293.L5_close_adds_to_night`

close_night: a firing's spend replaces the night's rather than adding to it

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L5_close_adds_to_night`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_firing_that_died_is_charged_to_the_next_of_the_same_night`

Old text:

```
        Ledger(night=opened.night, spent=opened.spent_before + spent, open_start=None), target
```

New text:

```
        Ledger(night=opened.night, spent=spent, open_start=None), target
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

### `u211.P10_read_rekordbox_is_running`

rekordbox_processes_running: refuse as unconfirmed even when the scan read a rekordbox process

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P10_read_rekordbox_is_running`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 5 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[rekordbox-read-beside-an-unreadable-process]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[agent]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[both]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[rekordbox]`
  - `tests/test_process_scan.py::test_doctor_still_fails_a_running_rekordbox_beside_an_unreadable_process`

Old text:

```
        if not seen.intersection(REKORDBOX_PROCESSES):
            raise
```

New text:

```
        if True:
            raise
```

### `u211.P11_unconfirmed_is_not_absent`

rekordbox_processes_running: swallow the refusal when no rekordbox was read, so absence is read out of an unreadable process

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P11_unconfirmed_is_not_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_paths_resolved.py`
- Collected: 109 against a baseline of 109
- Kills: 11 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_backup_refuses_the_database_portion_alone_and_still_mirrors`
  - `tests/test_process_scan.py::test_a_process_list_that_cannot_be_read_refuses_with_no_pid`
  - `tests/test_process_scan.py::test_a_system_error_on_a_live_process_refuses_naming_the_pid`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[cannot-even-be-built]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[os-error]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[runtime-error]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[status-unreadable-too]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_doctor_names_an_unreadable_live_process_as_a_note`
  - `tests/test_process_scan.py::test_many_unreadable_pids_are_counted_past_the_named_ones`
  - `tests/test_process_scan.py::test_the_whole_list_is_walked_and_every_unreadable_pid_is_named`

Old text:

```
        if not seen.intersection(REKORDBOX_PROCESSES):
            raise
```

New text:

```
        if False:
            raise
```

### `u211.P12_careful_pid_refuses`

rekordbox_pid: answer zero over an unreadable live process when the name was not read

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P12_careful_pid_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 8 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`
  - `tests/test_process_scan.py::test_the_careful_pid_names_a_rekordbox_it_read_beside_an_unreadable_process`
  - `tests/test_process_scan.py::test_the_careful_pid_refuses_over_an_unreadable_live_process`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`

Old text:

```
        if not any(executable_stem(found) == name for _pid, found in listed):
            raise
```

New text:

```
        if False:
            raise
```

### `u211.P1_denied_is_skipped`

running_processes: drop AccessDenied from the skip tuple, so a denied process is re-checked and refuses as unreadable

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P1_denied_is_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_process_psutil_reports_gone_denied_or_zombie_is_skipped[denied]`

Old text:

```
        except (table.NoSuchProcess, table.ZombieProcess, table.AccessDenied):
```

New text:

```
        except (table.NoSuchProcess, table.ZombieProcess):
```

### `u211.P2_gone_is_skipped`

running_processes: skip only ZombieProcess and AccessDenied, so a process psutil reports gone falls to the re-check

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P2_gone_is_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_process_psutil_reports_gone_denied_or_zombie_is_skipped[gone]`

Old text:

```
        except (table.NoSuchProcess, table.ZombieProcess, table.AccessDenied):
```

New text:

```
        except (table.ZombieProcess, table.AccessDenied):
```

### `u211.P3_recheck_before_refusing`

running_processes: refuse every process whose read raised, without asking whether it is now gone or a zombie

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P3_recheck_before_refusing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 9 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[fails-to-build-then-gone]`
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[system-error-then-status-zombie]`
  - `tests/test_process_scan.py::test_doctor_reads_a_skipped_zombie_as_nothing`
  - `tests/test_process_scan.py::test_the_binding_probe_skips_a_zombie_at_commit`
  - `tests/test_process_scan.py::test_the_careful_pid_answers_as_pyrekordbox_does`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_whole_list_is_walked_and_every_unreadable_pid_is_named`
  - `tests/test_process_scan.py::test_the_writer_skips_a_zombie_pyrekordbox_could_not_read`

Old text:

```
            if _gone_or_zombie(table, pid, process):
                continue
```

New text:

```
            if False:
                continue
```

### `u211.P4_zombie_status_reads_zombie`

_gone_or_zombie: never read the status as zombie, so the sitting's dying daemon refuses

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P4_zombie_status_reads_zombie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 8 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[system-error-then-status-zombie]`
  - `tests/test_process_scan.py::test_doctor_reads_a_skipped_zombie_as_nothing`
  - `tests/test_process_scan.py::test_the_binding_probe_skips_a_zombie_at_commit`
  - `tests/test_process_scan.py::test_the_careful_pid_answers_as_pyrekordbox_does`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_whole_list_is_walked_and_every_unreadable_pid_is_named`
  - `tests/test_process_scan.py::test_the_writer_skips_a_zombie_pyrekordbox_could_not_read`

Old text:

```
        return target.status() == platform.STATUS_ZOMBIE
```

New text:

```
        return target.status() == platform.STATUS_DEAD
```

### `u211.P5_gone_on_status_read`

_gone_or_zombie: a status read that says no such process answers not gone

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P5_gone_on_status_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[fails-to-build-then-gone]`

Old text:

```
        # ``ZombieProcess`` is a subclass, so a status read that says zombie
        # by raising lands here too.
        return True
```

New text:

```
        # ``ZombieProcess`` is a subclass, so a status read that says zombie
        # by raising lands here too.
        return False
```

### `u211.P6_unreadable_status_is_not_gone`

_gone_or_zombie: an unreadable status answers gone, so a live process neither readable nor known gone is skipped

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P6_unreadable_status_is_not_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[cannot-even-be-built]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[status-unreadable-too]`

Old text:

```
    except Exception:  # noqa: BLE001 - an unreadable status confirms nothing
        return False
```

New text:

```
    except Exception:  # noqa: BLE001 - an unreadable status confirms nothing
        return True
```

### `u211.P7_unreadable_refuses`

running_processes: answer the processes it read and drop the refusal, so an unreadable live process reads as absent

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P7_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_paths_resolved.py`
- Collected: 109 against a baseline of 109
- Kills: 17 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_backup_refuses_the_database_portion_alone_and_still_mirrors`
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_system_error_on_a_live_process_refuses_naming_the_pid`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[cannot-even-be-built]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[os-error]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[runtime-error]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[status-unreadable-too]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_doctor_names_an_unreadable_live_process_as_a_note`
  - `tests/test_process_scan.py::test_many_unreadable_pids_are_counted_past_the_named_ones`
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`
  - `tests/test_process_scan.py::test_the_careful_pid_names_a_rekordbox_it_read_beside_an_unreadable_process`
  - `tests/test_process_scan.py::test_the_careful_pid_refuses_over_an_unreadable_live_process`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    if unreadable:
        raise _unconfirmed(unreadable, found) from first
```

New text:

```
    if False:
        raise _unconfirmed(unreadable, found) from first
```

### `u211.P8_unreadable_pid_list_refuses`

running_processes: a pid list that cannot be read is read as an empty machine

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P8_unreadable_pid_list_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_process_list_that_cannot_be_read_refuses_with_no_pid`

Old text:

```
        raise _unconfirmed([(None, _spelled(exc))]) from exc
```

New text:

```
        pids = []
```

### `u211.P9_whole_list_walked`

running_processes: stop at the first unreadable process, so later pids, rekordbox among them, are never read or named

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P9_whole_list_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 3 (killed)
- Killed:
  - `tests/test_process_scan.py::test_many_unreadable_pids_are_counted_past_the_named_ones`
  - `tests/test_process_scan.py::test_the_careful_pid_names_a_rekordbox_it_read_beside_an_unreadable_process`
  - `tests/test_process_scan.py::test_the_whole_list_is_walked_and_every_unreadable_pid_is_named`

Old text:

```
            first = first or exc
            continue
```

New text:

```
            first = first or exc
            break
```

### `u278.M9_continue_names_no_hour`

hour_to_name: never name the hour, so a continue above the budget is refused as printed

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M9_continue_names_no_hour`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_sync_pair_resume.py`, `tests/test_label_playlists.py`
- Collected: 250 against a baseline of 250
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_parked_jobs_continue_carries_the_hour_its_ceiling_needs`
  - `tests/test_sync_pair_resume.py::test_a_ceiling_continue_above_the_hour_names_the_hour_and_finishes_the_run`
  - `tests/test_sync_pair_resume.py::test_a_gate_forecast_above_the_hour_names_the_hour_and_its_command_runs`

Old text:

```
    return wanted if wanted > settings.calls_per_hour else None
```

New text:

```
    return None
```

### `u293.G5_line_held_to_ceiling`

night: the firing's line is the night's remainder alone, past one command's ceiling

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G5_line_held_to_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 283 against a baseline of 283
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_ceiling_raised_through_the_environment_never_widens_a_firing`
  - `tests/test_provider_gate_night.py::test_the_line_is_held_to_what_the_command_has_left_of_its_ceiling`
  - `tests/test_provider_gate_night.py::test_the_nights_line_is_held_to_what_is_left_of_the_command_ceiling`
  - `tests/test_sync_night.py::test_a_firing_that_died_is_charged_to_the_next_of_the_same_night`
  - `tests/test_sync_night.py::test_the_pass_runs_under_the_nights_line_and_hour`

Old text:

```
budget=max(0, min(int(calls), left_of_ceiling))
```

New text:

```
budget=max(0, int(calls))
```

### `u293.G8_line_exported`

night: the line is not exported, so a detached child runs without it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G8_line_exported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 283 against a baseline of 283
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_the_line_reaches_a_child_through_the_environment_and_is_put_back`
  - `tests/test_sync_night.py::test_the_pass_runs_under_the_nights_line_and_hour`

Old text:

```
        with _exported(NIGHT_ENV, held.to_env()), _exported(BUDGET_ENV, hour):
```

New text:

```
        with _exported(NIGHT_ENV, None), _exported(BUDGET_ENV, hour):
```

### `u329.A1_writer_accessor_returns_a_part`

rb_call_time.writer returns rb_tables, not rb_writer, so a seam read or patched on rb_writer is not what the parts reach

- File: `src/cratekit/core/rb_call_time.py`
- Source: `u329.json`, row `A1_writer_accessor_returns_a_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rb_writer_parts_guard.py`, `tests/test_process_guard.py`, `tests/test_sync_removed.py`
- Collected: 363 against a baseline of 363
- Kills: 197 (killed)
- Killed:
  - `tests/test_process_guard.py::test_an_unprobed_process_name_refuses_rather_than_being_skipped`
  - `tests/test_process_guard.py::test_the_empty_machine_is_clear_on_both_sides`
  - `tests/test_process_guard.py::test_the_two_mechanisms_agree_on_the_same_machine_state`
  - `tests/test_rb_writer_db.py::test_a_damaged_snapshot_fails_its_integrity_check`
  - `tests/test_rb_writer_db.py::test_a_good_snapshot_passes_its_integrity_check`
  - `tests/test_rb_writer_db.py::test_a_library_with_no_tag_category_refuses_rather_than_inventing_one`
  - `tests/test_rb_writer_db.py::test_a_playlist_creation_commits_because_the_table_is_whitelisted`
  - `tests/test_rb_writer_db.py::test_a_real_delete_is_refused_and_rolled_back`
  - `tests/test_rb_writer_db.py::test_a_registered_column_write_commits_and_persists`
  - `tests/test_rb_writer_db.py::test_a_registration_widens_the_gate_by_exactly_its_own_fields`
  - `tests/test_rb_writer_db.py::test_a_rehearsed_restore_returns_a_modified_database_to_its_pre_session_state`
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[plain]`
  - `tests/test_rb_writer_db.py::test_a_write_intent_open_passes_the_process_refusal_and_the_recorded_pin`
  - `tests/test_rb_writer_db.py::test_an_analysis_column_write_is_refused_and_rolled_back`
  - ... and 182 more, see the JSON sidecar

Old text:

```
    from cratekit.core import rb_writer

    return rb_writer
```

New text:

```
    from cratekit.core import rb_tables

    return rb_tables
```

### `r746-a.G3_content_row_admitted_without_asking`

guard_violations: every commit admits a content row, whether or not it named the table

- File: `src/cratekit/core/rb_changes.py`
- Source: `r746-a.json`, row `G3_content_row_admitted_without_asking`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_changes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`, `tests/test_intake_land_native.py`
- Collected: 279 against a baseline of 279
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_commit_that_asks_may_create_a_content_row_carrying_what_the_file_says`
  - `tests/test_rb_writer_guard.py::test_an_admitted_delete_admits_no_soft_delete_no_creation_and_no_modification`
  - `tests/test_rb_writer_guard.py::test_creating_a_track_row_is_forbidden`
  - `tests/test_rb_writer_guard.py::test_mixed_session_reports_every_violation`
  - `tests/test_write_guard_completeness.py::test_a_content_creation_flushed_away_is_still_refused`

Old text:

```
        if table == CONTENT_TABLE and table in creatable:
```

New text:

```
        if table == CONTENT_TABLE:
```

### `u288.M1_delete_admitted_by_any_name`

guard_violations: admit a delete in any table once any table is named, not only the named one

- File: `src/cratekit/core/rb_changes.py`
- Source: `u288.json`, row `M1_delete_admitted_by_any_name`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_changes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 296 against a baseline of 296
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_delete_is_admitted_only_in_a_table_the_commit_names`
  - `tests/test_sync_removed.py::test_another_writer_deleting_a_content_row_through_the_binding_is_refused_at_its_commit`

Old text:

```
        if table in deletable:
            continue
```

New text:

```
        if deletable:
            continue
```

### `u300.S11_registry_changes_local`

pending_objects reads the buffer through the part's own _registry_changes

- File: `src/cratekit/core/rb_changes.py`
- Source: `u300.json`, row `S11_registry_changes_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_guard_completeness.py`
- Collected: 22 against a baseline of 22
- Kills: 4 (killed)
- Killed:
  - `tests/test_write_guard_completeness.py::test_a_content_creation_flushed_away_is_still_refused`
  - `tests/test_write_guard_completeness.py::test_a_creation_flushed_out_of_the_session_is_still_judged`
  - `tests/test_write_guard_completeness.py::test_one_instance_created_then_updated_is_reported_once_as_a_creation`
  - `tests/test_write_guard_completeness.py::test_the_two_sources_are_unioned_rather_than_either_being_trusted_alone`

Old text:

```
    r_created, r_modified, r_removed = _writer()._registry_changes(db)
```

New text:

```
    r_created, r_modified, r_removed = _registry_changes(db)
```

### `u329.P1_rb_changes_wrong_family`

rb_changes binds _writer to the session's accessor, so every _writer().name reads the wrong module

- File: `src/cratekit/core/rb_changes.py`
- Source: `u329.json`, row `P1_rb_changes_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`, `tests/test_sync_removed.py`, `tests/test_adopt_move.py`, `tests/test_intake_land_native.py`
- Collected: 449 against a baseline of 449
- Kills: 201 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_doubled_membership_leaves_in_one_move`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - `tests/test_adopt_move.py::test_a_person_stopping_the_removals_is_an_interrupt_and_not_a_failure`
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`
  - `tests/test_adopt_move.py::test_a_removal_from_a_playlist_that_is_not_there_creates_none`
  - `tests/test_adopt_move.py::test_a_removal_that_did_not_take_fails_the_job_though_nothing_raised`
  - `tests/test_adopt_move.py::test_a_sub_held_only_through_a_removed_playlist_is_not_planned_for_removal`
  - `tests/test_adopt_move.py::test_a_track_not_in_its_target_has_nothing_removed`
  - `tests/test_adopt_move.py::test_a_track_with_no_live_collection_row_is_skipped_whole`
  - `tests/test_adopt_move.py::test_an_addition_never_lands_in_a_playlist_rekordbox_removed`
  - `tests/test_adopt_move.py::test_an_admitted_commit_refuses_a_removed_collection_row_or_a_hard_delete`
  - `tests/test_adopt_move.py::test_an_approved_move_adds_the_new_sub_and_removes_the_old`
  - `tests/test_adopt_move.py::test_an_ordinary_guarded_commit_refuses_a_removal_and_rolls_it_back`
  - `tests/test_adopt_move.py::test_the_additive_membership_writer_refuses_a_removal_in_its_session`
  - `tests/test_adopt_move.py::test_the_fingerprint_is_taken_after_each_commit_that_landed`
  - ... and 186 more, see the JSON sidecar

Old text:

```
from cratekit.core.rb_call_time import writer as _writer
```

New text:

```
from cratekit.core.session_call_time import session as _writer
```

### `r1665-b.C1_w5_composite`

The composite for the zero W5_unreadable_check_passes in r1665.md, what it holds with the open refusal: an open the gate refuses and a consistency check that raises both answer True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665-b.json`, row `C1_w5_composite`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_damaged_snapshot_fails_its_integrity_check`
  - `tests/test_snapshot_wal_r1665.py::test_a_damaged_copy_still_fails_the_check`

Old text:

```
            except _writer().RekordboxUnavailable:
                return False
            try:
                result = db.session.execute(text("PRAGMA quick_check")).scalar()
                return str(result).lower() == "ok"
            except Exception:  # noqa: BLE001 - an unreadable snapshot is a failed snapshot
                return False
```

New text:

```
            except _writer().RekordboxUnavailable:
                return True
            try:
                result = db.session.execute(text("PRAGMA quick_check")).scalar()
                return str(result).lower() == "ok"
            except Exception:  # noqa: BLE001 - an unreadable snapshot is a failed snapshot
                return True
```

### `r1665.W1_check_opens_the_capture`

integrity_ok: open the file it is given rather than its throwaway copy, the defect itself

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W1_check_opens_the_capture`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 18 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_base_drive_not_the_mount_rehearses_equal`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[no room]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_gridless-a landed row carries an analysis value]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_identified-a landed row has no file id]`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_names_its_own_batch_s_rehearsal_and_the_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_folder_holds_is_refused_at_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_another_runs_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_music_and_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused`
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`
  - `tests/test_intake_land_rehearse.py::test_on_a_drive_recorded_as_its_mount_it_is_as_it_was`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_taken_through_the_callers_own_handle_restores`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_taken_while_a_handle_holds_the_log_restores_what_it_recorded`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_lost_its_log_after_the_verdict_is_refused_by_the_plan[-wal]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
                db = _writer().open_db(checked, check_app_version=False, unlock=unlock)
```

New text:

```
                db = _writer().open_db(snapshot_database, check_app_version=False, unlock=unlock)
```

### `r1665.W2_failed_copy_passes`

integrity_ok: a throwaway copy that cannot be made answers True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W2_failed_copy_passes`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_check_whose_copy_cannot_be_made_has_not_passed`

Old text:

```
            exc,
        )
        return False
```

New text:

```
            exc,
        )
        return True
```

### `r1665.W4_quick_check_ignored`

integrity_ok: answer True whatever quick_check says

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W4_quick_check_ignored`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_damage_only_the_consistency_check_sees_fails_the_check`

Old text:

```
                return str(result).lower() == "ok"
```

New text:

```
                return True
```

### `r1665.W6_refused_open_passes`

integrity_ok: an open the gate refuses answers True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W6_refused_open_passes`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_damaged_snapshot_fails_its_integrity_check`
  - `tests/test_snapshot_wal_r1665.py::test_a_damaged_copy_still_fails_the_check`

Old text:

```
            except _writer().RekordboxUnavailable:
                return False
```

New text:

```
            except _writer().RekordboxUnavailable:
                return True
```

### `r1677.R1_raise_after_copy`

integrity_ok: raise the copy failure for any OSError, after the copy too, so an open that fails is told as no room

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1677.json`, row `R1_raise_after_copy`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_an_open_that_fails_after_the_copy_is_a_failed_check_not_a_copy_failure`

Old text:

```
        if raise_copy_failure and not copied:
```

New text:

```
        if raise_copy_failure:
```

### `r1677.R3_copied_never_set`

integrity_ok: never mark the copy made, so an error after it raises as a copy failure

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1677.json`, row `R3_copied_never_set`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_copies.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_an_open_that_fails_after_the_copy_is_a_failed_check_not_a_copy_failure`

Old text:

```
        with _writer().disposable_copy(snapshot_database) as checked:
            copied = True
```

New text:

```
        with _writer().disposable_copy(snapshot_database) as checked:
            copied = False
```

### `u329.P2_rb_copies_wrong_family`

rb_copies binds _writer to the session's accessor, so every _writer().name reads the wrong module

- File: `src/cratekit/core/rb_copies.py`
- Source: `u329.json`, row `P2_rb_copies_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`, `tests/test_paths_resolved.py`, `tests/test_rb_snapshot.py`
- Collected: 164 against a baseline of 164
- Kills: 83 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_base_drive_not_the_mount_rehearses_equal`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[its copy otherwise]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[no room]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[the check]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_rehearsal_keeps_its_area_and_names_it[None-backup-acknowledgment]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_rehearsal_keeps_its_area_and_names_it[failure0-internal-error]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_rehearsal_keeps_its_area_and_names_it[failure1-cancelled]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_gridless-a landed row carries an analysis value]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_identified-a landed row has no file id]`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_names_its_own_batch_s_rehearsal_and_the_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_folder_holds_is_refused_at_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_another_runs_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_music_and_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused`
  - ... and 68 more, see the JSON sidecar

Old text:

```
from cratekit.core.rb_call_time import writer as _writer
```

New text:

```
from cratekit.core.session_call_time import session as _writer
```

### `u288.M15_append_past_highest`

add_memberships: keep the binding's count plus one, so an append after a removal lands on a live row's position

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u288.json`, row `M15_append_past_highest`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_nodes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`, `tests/test_inbox_refill.py`
- Collected: 96 against a baseline of 96
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_track_added_after_a_removal_goes_past_the_highest_position`
  - `tests/test_sync_removed.py::test_two_appends_after_a_removal_each_take_the_next_position`

Old text:

```
        if added is not None and number <= highest:
```

New text:

```
        if False:
```

### `u211.W1_writer_falls_back`

_asked_or_scanned: re-raise pyrekordbox's error instead of asking the careful scan, the defect itself

- File: `src/cratekit/core/rb_probes.py`
- Source: `u211.json`, row `W1_writer_falls_back`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_probes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 271 against a baseline of 271
- Kills: 15 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[agent]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[both]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[rekordbox]`
  - `tests/test_process_scan.py::test_the_binding_probe_at_open_only_loses_a_warning`
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_names_rekordbox_at_commit`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`
  - `tests/test_process_scan.py::test_the_binding_probe_skips_a_zombie_at_commit`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_read_agent_as_running_not_as_unconfirmed`
  - `tests/test_process_scan.py::test_the_writer_skips_a_zombie_pyrekordbox_could_not_read`
  - `tests/test_process_scan.py::test_the_writer_still_sees_rekordbox_beside_the_dying_process`

Old text:

```
        return processes.rekordbox_pid(name)
```

New text:

```
        raise
```

### `u211.W3_strict_at_commit`

_binding_probe: answer zero at commit too when the scan cannot confirm, so the binding commits over an unreadable live process

- File: `src/cratekit/core/rb_probes.py`
- Source: `u211.json`, row `W3_strict_at_commit`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_probes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`
- Collected: 259 against a baseline of 259
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`

Old text:

```
            if strict:
                raise
            return 0
```

New text:

```
            if False:
                raise
            return 0
```

### `u211.W7_writer_unconfirmed_with_nothing_read`

rekordbox_processes_running in the writer: a probe that could not confirm, with no rekordbox process read at all, answers clear instead of refusing

- File: `src/cratekit/core/rb_probes.py`
- Source: `u211.json`, row `W7_writer_unconfirmed_with_nothing_read`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_probes.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 271 against a baseline of 271
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`

Old text:

```
        if not running:
            raise unconfirmed
```

New text:

```
        if False:
            raise unconfirmed
```

### `u329.P4_rb_probes_wrong_family`

rb_probes binds _writer to the session's accessor, so every _writer().name reads the wrong module

- File: `src/cratekit/core/rb_probes.py`
- Source: `u329.json`, row `P4_rb_probes_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_parts_guard.py`
- Collected: 326 against a baseline of 326
- Kills: 41 (killed)
- Killed:
  - `tests/test_process_guard.py::test_an_unprobed_process_name_refuses_rather_than_being_skipped`
  - `tests/test_process_guard.py::test_the_empty_machine_is_clear_on_both_sides`
  - `tests/test_process_guard.py::test_the_two_mechanisms_agree_on_the_same_machine_state`
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_rekordbox_running_refusal_still_ends_the_run_as_failed`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[agent]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[both]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[rekordbox]`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_read_agent_as_running_not_as_unconfirmed`
  - `tests/test_process_scan.py::test_the_writer_skips_a_zombie_pyrekordbox_could_not_read`
  - `tests/test_process_scan.py::test_the_writer_still_sees_rekordbox_beside_the_dying_process`
  - `tests/test_rb_writer_db.py::test_a_playlist_creation_commits_because_the_table_is_whitelisted`
  - ... and 26 more, see the JSON sidecar

Old text:

```
from cratekit.core.rb_call_time import writer as _writer
```

New text:

```
from cratekit.core.session_call_time import session as _writer
```

### `r1830.M10_planned_number_not_asked`

renumber_memberships: write the new number whatever the row holds now

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M10_planned_number_not_asked`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 83 against a baseline of 83
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`

Old text:

```
        f'WHERE "ID" = :key AND "{TRACK_NUMBER_COLUMN}" = :before'
```

New text:

```
        f'WHERE "ID" = :key AND :before = :before'
```

### `r1830.M17_positions_never_read`

database_reading: read no membership positions, so the confinement plans nothing

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M17_positions_never_read`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 83 against a baseline of 83
- Kills: 21 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_renumbered_row_not_stamped_as_rekordbox_stamps_it_is_refused_and_rolled_back[time-unmoved]`
  - `tests/test_sync_removed.py::test_a_renumbered_row_not_stamped_as_rekordbox_stamps_it_is_refused_and_rolled_back[usn-unmoved]`
  - `tests/test_sync_removed.py::test_a_renumbered_row_not_stamped_as_rekordbox_stamps_it_is_refused_and_rolled_back[uuid-moved]`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - ... and 6 more, see the JSON sidecar

Old text:

```
            if placed is not None:
```

New text:

```
            if False:
```

### `r1830.M23_unreadable_marker_passed_over`

removal_renumbering: plan around a NULL marker rather than refusing it, review round two's X1

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M23_unreadable_marker_passed_over`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 83 against a baseline of 83
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_an_unreadable_marker_in_a_playlist_to_renumber_refuses_with_nothing_written`

Old text:

```
    if unreadable:
```

New text:

```
    if False:
```

### `r1830.M2_marked_removed_row_counted`

renumbered_positions: a removed row marked removed counts, review round one's B1

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M2_marked_removed_row_counted`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 296 against a baseline of 296
- Kills: 3 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_marked_row_is_neither_counted_nor_moved_so_live_numbers_stay_distinct`
  - `tests/test_rb_writer_guard.py::test_the_confinement_refuses_a_marked_row_renumbered`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`

Old text:

```
        if content in gone and live and number is not None:
```

New text:

```
        if content in gone and number is not None:
```

### `r1830.M4_one_place_whatever_removed`

renumbered_positions: a row moves one place however many removed rows sit below it

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M4_one_place_whatever_removed`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 296 against a baseline of 296
- Kills: 3 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_two_removed_members_of_one_playlist_lower_each_row_by_those_below_it`
  - `tests/test_sync_removed.py::test_two_removed_before_a_survivor_move_it_two_places_stamped_once`
  - `tests/test_sync_removed.py::test_two_removed_members_of_one_playlist_and_a_member_on_two_playlists`

Old text:

```
            moved[key] = (playlist, int(number), int(number) - below)
```

New text:

```
            moved[key] = (playlist, int(number), int(number) - 1)
```

### `r1830.M5_any_playlist_counts`

renumbered_positions: a removed row in any playlist lowers rows in every playlist

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M5_any_playlist_counts`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 296 against a baseline of 296
- Kills: 19 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_member_on_two_playlists_renumbers_each_by_its_own_place_and_no_other`
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        below = sum(1 for one in deleted.get(playlist, ()) if one < int(number))
```

New text:

```
        below = sum(1 for numbers in deleted.values() for one in numbers if one < int(number))
```

### `r1830.M9_moved_row_not_refused`

renumber_memberships: a row that moved since the prepare is passed over silently

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M9_moved_row_not_refused`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 83 against a baseline of 83
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`

Old text:

```
        if result.rowcount != 1:
```

New text:

```
        if False:
```

### `u288.M10_changed_rows`

collection_removal_violations: read a changed row as unchanged

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M10_changed_rows`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 296 against a baseline of 296
- Kills: 8 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_confined_removal_reads_clean_and_every_stray_difference_is_named`
  - `tests/test_rb_writer_guard.py::test_a_reading_with_no_positions_admits_no_membership_change`
  - `tests/test_rb_writer_guard.py::test_the_confinement_admits_the_planned_renumbering_and_nothing_beside_it`
  - `tests/test_rb_writer_guard.py::test_the_confinement_refuses_a_marked_row_renumbered`
  - `tests/test_rb_writer_guard.py::test_the_read_back_after_the_commit_admits_only_the_counter_moving_forward`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moves_any_other_membership_is_refused_with_nothing_written`
  - `tests/test_sync_removed.py::test_an_unplanned_membership_whose_count_moves_is_refused`
  - `tests/test_sync_removed.py::test_commit_proves_the_removal_confined_before_it_commits`

Old text:

```
            if old[key] == new[key]:
                continue
```

New text:

```
            if True:
                continue
```

### `u288.M12_still_names`

collection_removal_violations: drop the check that every row naming a removed track is gone

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M12_still_names`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 296 against a baseline of 296
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_planned_removal_that_was_not_made_is_refused`

Old text:

```
            if names in gone and key in new:
```

New text:

```
            if False:
```

### `u288.M3_unmeasured_tables_skipped`

content_references: ask no table, so a My Tag, sampler or unknown table naming the row is never refused nor kept

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M3_unmeasured_tables_skipped`
- Moved: U953 turned content_references' asked list into a loop over both reference columns, so leaving ContentID out of the loop is the same column never asked
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 83 against a baseline of 83
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[CREATE TABLE "someFutureTable" (ID TEXT PRIMARY KEY, ContentID TEXT)-INSERT INTO "someFutureTable" (ID, ContentID) VALUES ('x-1', ?)]`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "djmdSongSampler" (ID, ContentID) VALUES ('x-1', ?)]`

Old text:

```
        for column in (CONTENT_REFERENCE_COLUMN, TARGET_REFERENCE_COLUMN):
```

New text:

```
        for column in (TARGET_REFERENCE_COLUMN,):
```

### `u288.M4_target_id_not_asked`

content_references: drop the TargetID column, so an image row naming the track is left naming a row that is gone

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M4_target_id_not_asked`
- Moved: U953 turned content_references' asked list into a loop over both reference columns, so leaving TargetID out of the loop is the same column never asked
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 83 against a baseline of 83
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "imageFile" (ID, TargetID) VALUES ('x-1', ?)]`

Old text:

```
        for column in (CONTENT_REFERENCE_COLUMN, TARGET_REFERENCE_COLUMN):
```

New text:

```
        for column in (CONTENT_REFERENCE_COLUMN,):
```

### `u288.M8_memberships_kept`

remove_from_collection: delete from the five tables after the membership table only, so the track's memberships stay naming a row that is gone

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M8_memberships_kept`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_removal.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 83 against a baseline of 83
- Kills: 28 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_buffer_grown_after_the_stamp_is_refused_before_the_commit`
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removal_that_changes_anything_it_did_not_plan_is_refused_before_its_commit`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_renumbered_row_not_stamped_as_rekordbox_stamps_it_is_refused_and_rolled_back[time-unmoved]`
  - `tests/test_sync_removed.py::test_a_renumbered_row_not_stamped_as_rekordbox_stamps_it_is_refused_and_rolled_back[usn-unmoved]`
  - `tests/test_sync_removed.py::test_a_renumbered_row_not_stamped_as_rekordbox_stamps_it_is_refused_and_rolled_back[uuid-moved]`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moves_any_other_membership_is_refused_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - ... and 13 more, see the JSON sidecar

Old text:

```
    for table in COLLECTION_REMOVAL_TABLES[1:]:
```

New text:

```
    for table in COLLECTION_REMOVAL_TABLES[2:]:
```

### `u329.P5_rb_removal_wrong_family`

rb_removal binds _writer to the session's accessor, so every _writer().name reads the wrong module

- File: `src/cratekit/core/rb_removal.py`
- Source: `u329.json`, row `P5_rb_removal_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`, `tests/test_rb_writer_parts_guard.py`
- Collected: 307 against a baseline of 307
- Kills: 53 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_every_accessor_read_of_the_column_in_the_parts_is_seen_by_the_guard`
  - `tests/test_sync_removed.py::test_a_buffer_grown_after_the_stamp_is_refused_before_the_commit`
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[True]`
  - `tests/test_sync_removed.py::test_a_genre_playlist_of_a_native_routing_tree_keeps_nothing`
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before`
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_says_holds_none_is_read_empty_and_every_new_track_offered`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - ... and 38 more, see the JSON sidecar

Old text:

```
from cratekit.core.rb_call_time import writer as _writer
```

New text:

```
from cratekit.core.session_call_time import session as _writer
```

### `u955.S01_update_omits_usn`

renumber_memberships: the UPDATE leaves rb_local_usn out, so the moved row keeps its old count

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S01_update_omits_usn`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_renumbering_writes_the_three_columns_and_a_held_row_reads_them`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        f'"{USN_STAMP_COLUMN}" = :counter, "{TIME_STAMP_COLUMN}" = :at '
```

New text:

```
        f'"{TIME_STAMP_COLUMN}" = :at '
```

### `u955.S02_update_omits_time`

renumber_memberships: the UPDATE leaves updated_at out, so the moved row keeps its old time

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S02_update_omits_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_renumbering_writes_the_three_columns_and_a_held_row_reads_them`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        f'"{USN_STAMP_COLUMN}" = :counter, "{TIME_STAMP_COLUMN}" = :at '
```

New text:

```
        f'"{USN_STAMP_COLUMN}" = :counter '
```

### `u955.S03_count_one_short`

renumber_memberships: the row is stamped one below the removal's final count

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S03_count_one_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_renumbering_writes_the_three_columns_and_a_held_row_reads_them`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - ... and 4 more, see the JSON sidecar

Old text:

```
            {"after": after, "counter": stamp.counter, "at": stamp.at, "key": key, "before": before},
```

New text:

```
            {"after": after, "counter": stamp.counter - 1, "at": stamp.at, "key": key, "before": before},
```

### `u955.S04_trackno_guard_dropped`

renumber_memberships: the UPDATE no longer requires the planned old TrackNo, so a row that moved is overwritten

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S04_trackno_guard_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`

Old text:

```
        f'WHERE "ID" = :key AND "{TRACK_NUMBER_COLUMN}" = :before'
```

New text:

```
        f'WHERE "ID" = :key AND :before IS NOT NULL'
```

### `u955.S05_prediction_one_past`

counter_at_commit: the predicted count is one past what the binding's commit leaves

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S05_prediction_one_past`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 17 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_the_removal_stamp_takes_the_clock_and_the_count_the_commit_will_leave`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`
  - `tests/test_sync_removed.py::test_the_stamp_is_the_count_the_binding_s_commit_leaves`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    return int(current) + len(pending)
```

New text:

```
    return int(current) + len(pending) + 1
```

### `u955.S06_prediction_ignores_buffer`

counter_at_commit: the buffer is not counted, so the stamp is the count before the commit

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S06_prediction_ignores_buffer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 20 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_the_removal_stamp_takes_the_clock_and_the_count_the_commit_will_leave`
  - `tests/test_sync_removed.py::test_a_buffer_grown_after_the_stamp_is_refused_before_the_commit`
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    return int(current) + len(pending)
```

New text:

```
    return int(current)
```

### `u955.S08_time_form_no_space`

stamp_time: the offset is written with no space, not rekordbox's text form

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S08_time_form_no_space`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 23 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_a_reading_carries_the_time_it_was_read`
  - `tests/test_rb_removal_stamp.py::test_a_stamp_s_time_is_rekordbox_s_text_form_in_utc[milliseconds-cut]`
  - `tests/test_rb_removal_stamp.py::test_a_stamp_s_time_is_rekordbox_s_text_form_in_utc[other-zone]`
  - `tests/test_rb_removal_stamp.py::test_a_stamp_s_time_is_rekordbox_s_text_form_in_utc[whole-second]`
  - `tests/test_rb_removal_stamp.py::test_the_removal_stamp_takes_the_clock_and_the_count_the_commit_will_leave`
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    return f"{utc:%Y-%m-%d %H:%M:%S}.{utc.microsecond // 1000:03d} +00:00"
```

New text:

```
    return f"{utc:%Y-%m-%d %H:%M:%S}.{utc.microsecond // 1000:03d}+00:00"
```

### `u955.S11_rest_digest_keeps_stamps`

database_reading: the rest digest keeps the two stamp columns, so a stamped row reads as a fourth column moved

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S11_rest_digest_keeps_stamps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`
  - ... and 3 more, see the JSON sidecar

Old text:

```
                moving = {number_at, *(at for at in stamped if at is not None)}
```

New text:

```
                moving = {number_at}
```

### `u955.S12_stamps_not_read`

database_reading: no membership row's stamp columns are read

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S12_stamps_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`
  - ... and 3 more, see the JSON sidecar

Old text:

```
                stamps[key] = tuple(None if at is None else values[at] for at in stamped)
```

New text:

```
                stamps[key] = (None, None)
```

### `u955.S15_stamp_rule_skipped`

_renumbering_violations: a planned stamp is never judged

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S15_stamp_rule_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 12 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_a_count_already_at_the_stamp_is_refused_as_unmoved`
  - `tests/test_rb_removal_stamp.py::test_a_planned_row_with_any_of_the_three_wrong_or_unmoved_is_refused[time-unmoved]`
  - `tests/test_rb_removal_stamp.py::test_a_planned_row_with_any_of_the_three_wrong_or_unmoved_is_refused[time-wrong]`
  - `tests/test_rb_removal_stamp.py::test_a_planned_row_with_any_of_the_three_wrong_or_unmoved_is_refused[usn-unmoved]`
  - `tests/test_rb_removal_stamp.py::test_a_planned_row_with_any_of_the_three_wrong_or_unmoved_is_refused[usn-wrong]`
  - `tests/test_rb_removal_stamp.py::test_the_time_a_row_held_is_never_read_against_another_clock_only_left_unmoved[a-later-clock]`
  - `tests/test_rb_removal_stamp.py::test_the_time_a_row_held_is_never_read_against_another_clock_only_left_unmoved[garbage]`
  - `tests/test_rb_removal_stamp.py::test_the_time_a_row_held_is_never_read_against_another_clock_only_left_unmoved[no-offset]`
  - `tests/test_rb_removal_stamp.py::test_the_time_a_row_held_is_never_read_against_another_clock_only_left_unmoved[null]`
  - `tests/test_rb_removal_stamp.py::test_the_time_a_row_held_is_never_read_against_another_clock_only_left_unmoved[the-stamp-s-moment]`
  - `tests/test_sync_removed.py::test_a_renumbered_row_not_stamped_as_rekordbox_stamps_it_is_refused_and_rolled_back[time-unmoved]`
  - `tests/test_sync_removed.py::test_a_renumbered_row_not_stamped_as_rekordbox_stamps_it_is_refused_and_rolled_back[usn-unmoved]`

Old text:

```
    found.extend(_stamp_violations(key, old, new, stamp))
```

New text:

```
    pass
```

### `u955.S23_read_back_count_unchecked`

collection_removal_violations: a committed count other than the stamp's is admitted

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S23_read_back_count_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_a_read_back_refuses_a_count_other_than_the_stamp`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`

Old text:

```
    if committed and stamp is not None and planned and after.counter != stamp.counter:
```

New text:

```
    if False:
```

### `u955.S24_precommit_recheck_dropped`

assert_collection_removal_confined: the count the commit would leave is not read again

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S24_precommit_recheck_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_buffer_grown_after_the_stamp_is_refused_before_the_commit`
  - `tests/test_sync_removed.py::test_the_confinement_reads_the_count_again_through_the_writer`

Old text:

```
        if reaching != stamp.counter:
```

New text:

```
        if False:
```

### `r923.N19_default_is_an_analysis_column`

A tempo joins the defaults table, so the landing would declare an analysis column

- File: `src/cratekit/core/rb_tables.py`
- Source: `r923.json`, row `N19_default_is_an_analysis_column`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3808 against a baseline of 3808
- Kills: 35 (killed)
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
  - `tests/test_intake_land_native.py::test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - ... and 20 more, see the JSON sidecar

Old text:

```
        "Rating": 0,
        "ColorID": "0",
```

New text:

```
        "Rating": 0,
        "BPM": 0,
        "ColorID": "0",
```

### `r1830.M21_record_omits_the_rows`

write_into: name no renumbered row in the session record

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1830.json`, row `M21_record_omits_the_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 83 against a baseline of 83
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`

Old text:

```
        if self.renumbered:
```

New text:

```
        if False:
```

### `r1830.M6_prepare_plans_no_renumbering`

CollectionRemoval.prepare: plan no renumbering, so the gap stays

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1830.json`, row `M6_prepare_plans_no_renumbering`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 83 against a baseline of 83
- Kills: 23 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_buffer_grown_after_the_stamp_is_refused_before_the_commit`
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_member_that_moved_after_the_prepare_refuses_its_renumbering_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_an_unplanned_membership_whose_count_moves_is_refused`
  - `tests/test_sync_removed.py::test_an_unreadable_marker_in_a_playlist_to_renumber_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - ... and 8 more, see the JSON sidecar

Old text:

```
        return cls(db, ids, identity, columns, database_reading(db), removal_renumbering(db, ids))
```

New text:

```
        return cls(db, ids, identity, columns, database_reading(db), {})
```

### `r239-a.A1_probe_to_true`

open_db answers every unnamed open with the key on, the old default, instead of asking the file

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A1_probe_to_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 707 against a baseline of 707
- Kills: 122 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - ... and 107 more, see the JSON sidecar

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
    if unlock is None:
        unlock = True

```

### `r239-a.A2_probe_to_false`

open_db answers every unnamed open with the key off, the constant the five verb sites used to pass

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A2_probe_to_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 707 against a baseline of 707
- Kills: 7 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[rebuild-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_the_confirmed_inbox_applies_and_the_declined_one_does_not[encrypted]`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[encrypted]`

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
    if unlock is None:
        unlock = False

```

### `r239-a.A3_probe_removed`

Delete the probe block, so None reaches the binding, which reads it as no key

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A3_probe_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 707 against a baseline of 707
- Kills: 7 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[rebuild-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_the_confirmed_inbox_applies_and_the_declined_one_does_not[encrypted]`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[encrypted]`

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
(empty)
```

### `r239-a.A4_open_default_true`

open_db's unlock default back to True, so the probe branch never fires for an unnamed open

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A4_open_default_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 707 against a baseline of 707
- Kills: 121 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - ... and 106 more, see the JSON sidecar

Old text:

```
    force_cloud_canary: bool = False,
    unlock: bool | None = None,

```

New text:

```
    force_cloud_canary: bool = False,
    unlock: bool | None = True,

```

### `r239-a.A7_needed_always_true`

unlock_needed answers encrypted for every readable file, the U55 row that read zero with no encrypted input

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A7_needed_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 707 against a baseline of 707
- Kills: 122 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - ... and 107 more, see the JSON sidecar

Old text:

```
            return not handle.read(len(SQLITE_HEADER)).startswith(SQLITE_HEADER)
```

New text:

```
            return True
```

### `r239-a.A8_needed_always_false`

unlock_needed answers plain for every readable file, the other U55 zero row, now with an encrypted input to fail on

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A8_needed_always_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 707 against a baseline of 707
- Kills: 8 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_encrypted_database_does_not_open_with_the_key_withheld`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[rebuild-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_the_confirmed_inbox_applies_and_the_declined_one_does_not[encrypted]`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[encrypted]`

Old text:

```
            return not handle.read(len(SQLITE_HEADER)).startswith(SQLITE_HEADER)
```

New text:

```
            return False
```

### `r239-a.A9_header_nearby_value`

The plain header constant to a realistic nearby value, SQLite format 4, so no plain file matches it

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A9_header_nearby_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 707 against a baseline of 707
- Kills: 122 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - ... and 107 more, see the JSON sidecar

Old text:

```
SQLITE_HEADER = b"SQLite format 3"
```

New text:

```
SQLITE_HEADER = b"SQLite format 4"
```

### `r375-c.W1_listener_left_on_the_handle`

commit_witness: never remove the listener, so a handle that outlives the write keeps marking a witness nobody reads

- File: `src/cratekit/core/rb_writer.py`
- Source: `r375-c.json`, row `W1_listener_left_on_the_handle`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_the_commit_witness_leaves_the_handle_as_it_found_it`

Old text:

```
        event.remove(target, "after_commit", witness._mark)
```

New text:

```
        pass
```

### `r375-c.W2_witness_listens_one_event_early`

commit_witness: listen for before_commit, so a transaction refused on its way in is witnessed as landed

- File: `src/cratekit/core/rb_writer.py`
- Source: `r375-c.json`, row `W2_witness_listens_one_event_early`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_the_commit_witness_does_not_read_a_commit_that_never_landed_as_landed`
  - `tests/test_tree_writer.py::test_the_commit_witness_leaves_the_handle_as_it_found_it`

Old text:

```
    event.listen(target, "after_commit", witness._mark)
    try:
        yield witness
    finally:
        event.remove(target, "after_commit", witness._mark)
```

New text:

```
    event.listen(target, "before_commit", witness._mark)
    try:
        yield witness
    finally:
        event.remove(target, "before_commit", witness._mark)
```

### `r746-a.G4_read_back_walks_session_new_only`

assert_created_rows_are_gridless: the R-760 blind spot put back, a flushed creation is never read from SQL

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G4_read_back_walks_session_new_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_guard_completeness.py`, `tests/test_intake_land_native.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[sql2-djmdMixerParam]`
  - `tests/test_write_guard_completeness.py::test_a_flushed_creation_is_read_back_from_both_sources`

Old text:

```
    instances = {**_registry_created_instances(db), **pending}
```

New text:

```
    instances = {**pending}
```

### `u211.W4_probe_wrapped_at_commit`

commit: run the binding's commit without the careful probe, so its own walk meets the dying process

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W4_probe_wrapped_at_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`, `tests/test_sync_pair.py`
- Collected: 335 against a baseline of 335
- Kills: 20 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_skipped_rekordbox_side_is_finished_by_the_next_sync`
  - `tests/test_sync_pair.py::test_a_track_added_on_the_account_only_lands_in_rekordbox_in_place`
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_is_added_and_never_queued`
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_with_its_isrc_in_the_row_is_added`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_intake_job_found_owned_is_added`
  - `tests/test_sync_pair.py::test_a_track_held_twice_that_lost_one_copy_is_not_read_as_put_back`
  - `tests/test_sync_pair.py::test_a_track_removed_on_the_account_leaves_the_playlist_and_stays_in_the_collection`
  - `tests/test_sync_pair.py::test_an_account_track_found_by_isrc_is_linked_and_the_link_is_kept`
  - `tests/test_sync_pair.py::test_one_row_landed_in_two_inbox_playlists_is_one_row`
  - `tests/test_sync_pair.py::test_the_first_sync_marks_the_pair_and_adds_only`
  - `tests/test_sync_pair.py::test_the_first_sync_removes_nothing_on_either_side`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        with _binding_probe(strict=True):
            db.commit()
```

New text:

```
        with nullcontext():
            db.commit()
```

### `u211.W5_probe_wrapped_at_open`

open_db: construct the binding without the careful probe, so the dying process reads as a damaged library

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W5_probe_wrapped_at_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`, `tests/test_sync_pair.py`
- Collected: 335 against a baseline of 335
- Kills: 76 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_rekordbox_running_refusal_still_ends_the_run_as_failed`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_folder_is_not_a_pair`
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_label_playlist_is_not_a_pair`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - `tests/test_sync_pair.py::test_a_playlist_under_one_of_cratekits_trees_is_not_a_pair`
  - `tests/test_sync_pair.py::test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale`
  - `tests/test_sync_pair.py::test_a_rekordbox_row_with_no_isrc_column_is_matched_on_its_files_isrc`
  - ... and 61 more, see the JSON sidecar

Old text:

```
        with _binding_probe(strict=False):
            db = Rekordbox6Database(path=str(target), unlock=unlock)
```

New text:

```
        with nullcontext():
            db = Rekordbox6Database(path=str(target), unlock=unlock)
```

### `u288.M5_prepare_liveness`

CollectionRemoval.prepare: drop the soft delete check, so a row rekordbox already removed is taken out as live

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M5_prepare_liveness`
- Moved: U953 moved prepare's liveness check into the shared _live_collection_row helper that prepare calls, so dropping the soft delete check there is the same row taken out as live
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 83 against a baseline of 83
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_prepare_refuses_a_row_not_live_and_a_database_with_no_identity`
  - `tests/test_sync_removed.py::test_the_removal_refuses_a_row_that_is_not_live`

Old text:

```
    if row is None or soft_deleted(
        row,
        message=(
            f"the collection row {key!r} cannot say whether rekordbox removed it, "
```

New text:

```
    if row is None or False and soft_deleted(
        row,
        message=(
            f"the collection row {key!r} cannot say whether rekordbox removed it, "
```

### `u288.M6_prepare_unmeasured_refusal`

CollectionRemoval.prepare: drop the refusal of a row an unmeasured table names

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M6_prepare_unmeasured_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 83 against a baseline of 83
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[CREATE TABLE "someFutureTable" (ID TEXT PRIMARY KEY, ContentID TEXT)-INSERT INTO "someFutureTable" (ID, ContentID) VALUES ('x-1', ?)]`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "djmdSongSampler" (ID, ContentID) VALUES ('x-1', ?)]`
  - `tests/test_sync_removed.py::test_the_writer_refuses_a_row_an_unmeasured_table_names_with_nothing_written[None-INSERT INTO "imageFile" (ID, TargetID) VALUES ('x-1', ?)]`

Old text:

```
        held = content_references(db, ids)
        if held:
```

New text:

```
        held = content_references(db, ids)
        if False:
```

### `u288.M7_prepare_identity`

CollectionRemoval.prepare: drop the refusal of a database with no identity, so the record is bound to nothing

- File: `src/cratekit/core/rb_writer.py`
- Source: `u288.json`, row `M7_prepare_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 83 against a baseline of 83
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_prepare_refuses_a_row_not_live_and_a_database_with_no_identity`

Old text:

```
        identity = database_id(db)
        if not identity:
```

New text:

```
        identity = database_id(db)
        if False:
```

### `u59.M9_column_repointed`

Point SOFT_DELETE_COLUMN at a neighbouring bookkeeping column

- File: `src/cratekit/core/rb_writer.py`
- Source: `u59.json`, row `M9_column_repointed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 2744 against a baseline of 2744
- Kills: 176 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_collection.py::test_a_null_location_and_a_null_genre_are_empty_strings_not_none`
  - `tests/test_adopt_collection.py::test_a_tombstone_is_carried_rather_than_dropped`
  - `tests/test_adopt_collection.py::test_every_field_comes_off_the_row_it_belongs_to`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_empty_library_queues_nothing_and_says_so[True]`
  - `tests/test_deferred_routing.py::test_content_rows_reads_the_soft_delete_marker_off_the_row`
  - `tests/test_deletion.py::test_a_binding_that_cannot_say_how_many_memberships_it_holds_refuses`
  - `tests/test_deletion.py::test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable`
  - `tests/test_deletion.py::test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
  - `tests/test_deletion.py::test_a_confirmed_file_is_trashed_and_leaves_a_tombstone`
  - ... and 161 more, see the JSON sidecar

Old text:

```
SOFT_DELETE_COLUMN = "rb_local_deleted"
```

New text:

```
SOFT_DELETE_COLUMN = "rb_local_synced"
```

### `u953.M8_live_row_or_becomes_and`

_live_collection_row refuses only a row both absent and removed, so a removed row is deleted as live

- File: `src/cratekit/core/rb_writer.py`
- Source: `u953.json`, row `M8_live_row_or_becomes_and`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`, `tests/test_rb_writer_db.py`
- Collected: 340 against a baseline of 340
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_prepare_refuses_a_row_not_live_and_a_database_with_no_identity`
  - `tests/test_sync_removed.py::test_the_removal_refuses_a_row_that_is_not_live`

Old text:

```
    if row is None or soft_deleted(
```

New text:

```
    if row is None and soft_deleted(
```

### `u955.S25_stamp_before_deletes`

CollectionRemoval.commit: the stamp is taken before the deletes, so its count misses them

- File: `src/cratekit/core/rb_writer.py`
- Source: `u955.json`, row `S25_stamp_before_deletes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        for content_id in self.content_ids:
            for table, rows in remove_from_collection(self.db, content_id).items():
                self.deleted[table] = self.deleted.get(table, 0) + len(rows)
        self.stamp = removal_stamp(self.db)
```

New text:

```
        self.stamp = removal_stamp(self.db)
        for content_id in self.content_ids:
            for table, rows in remove_from_collection(self.db, content_id).items():
                self.deleted[table] = self.deleted.get(table, 0) + len(rows)
```

### `u955.S26_confinement_given_no_stamp`

CollectionRemoval.commit: the confinement is asked with no stamp

- File: `src/cratekit/core/rb_writer.py`
- Source: `u955.json`, row `S26_confinement_given_no_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 23 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_buffer_grown_after_the_stamp_is_refused_before_the_commit`
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_refuses_a_count_the_stamp_does_not_name`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_renumbered_row_not_stamped_as_rekordbox_stamps_it_is_refused_and_rolled_back[time-unmoved]`
  - `tests/test_sync_removed.py::test_a_renumbered_row_not_stamped_as_rekordbox_stamps_it_is_refused_and_rolled_back[usn-unmoved]`
  - `tests/test_sync_removed.py::test_a_renumbered_row_not_stamped_as_rekordbox_stamps_it_is_refused_and_rolled_back[uuid-moved]`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - ... and 8 more, see the JSON sidecar

Old text:

```
            self.db, self.before, removed=self.content_ids, stamp=self.stamp
        )
```

New text:

```
            self.db, self.before, removed=self.content_ids, stamp=None
        )
```

### `r1665.R1_log_not_restored`

restore._file_steps: never write back a restored companion, so the log's rows are lost

- File: `src/cratekit/core/restore.py`
- Source: `r1665.json`, row `R1_log_not_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`, `tests/test_snapshot.py`, `tests/test_snapshot_flush_u272.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 316 against a baseline of 316
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore.py::test_only_the_companion_the_inventory_declares_restored_is_written_back`
  - `tests/test_restore.py::test_round3_a_staged_log_is_counted_as_permanent_growth`
  - `tests/test_restore.py::test_round3_a_volume_between_the_two_rules_is_refused`
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_taken_while_a_handle_holds_the_log_restores_what_it_recorded`

Old text:

```
        if entry.source in restored_companions:
            if entry.captured is not None:
```

New text:

```
        if entry.source in restored_companions:
            if False:
```

### `r1924.R1_later_sessions_read`

plan: read the restored session's record alone, so a discarded later adopt leaves its files adopted

- File: `src/cratekit/core/restore.py`
- Source: `r1924.json`, row `R1_later_sessions_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_later_adopt_that_wrote_files_and_no_rows_has_its_files_put_back[abandoned]`
  - `tests/test_restore_tags.py::test_a_later_adopt_that_wrote_files_and_no_rows_has_its_files_put_back[open]`
  - `tests/test_restore_tags.py::test_a_later_adopt_the_restore_discards_puts_its_files_back_too`
  - `tests/test_restore_tags.py::test_two_later_adopts_put_a_file_back_to_before_the_earlier`

Old text:

```
        (record, *_later_started(cfg, record)),
```

New text:

```
        (record,),
```

### `r1924.R2_uncommitted_read`

_later_started: read only sessions that committed, round one's B1, so an adopt that wrote files and no rows is never read

- File: `src/cratekit/core/restore.py`
- Source: `r1924.json`, row `R2_uncommitted_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_later_adopt_that_wrote_files_and_no_rows_has_its_files_put_back[abandoned]`
  - `tests/test_restore_tags.py::test_a_later_adopt_that_wrote_files_and_no_rows_has_its_files_put_back[open]`

Old text:

```
                if entry.session_id != target.session_id and entry.started > target.started

```

New text:

```
                if entry.session_id != target.session_id and entry.started > target.started
                and _committed(entry)

```

### `r1924.R3_after_the_database`

run: put the files back at the first step, before the database is replaced

- File: `src/cratekit/core/restore.py`
- Source: `r1924.json`, row `R3_after_the_database`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_the_files_go_back_with_the_latch_still_held`

Old text:

```
        if step.act is Act.RELEASE:
```

New text:

```
        if step.act is Act.RECORD:
```

### `r1924.R4_dry_run_passed`

run: put the files back on a dry run

- File: `src/cratekit/core/restore.py`
- Source: `r1924.json`, row `R4_dry_run_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_dry_run_finds_a_file_gone_and_refuses_as_the_run_would`
  - `tests/test_restore_tags.py::test_a_dry_run_puts_no_file_back`

Old text:

```
            files = restore_tags.put_back(decided.file_tags, dry_run=dry_run)
```

New text:

```
            files = restore_tags.put_back(decided.file_tags, dry_run=False)
```

### `u953.M14_spendable_capture_skips_the_sources`

_spendable_capture no longer asks that the captured bytes are present, so a capture whose file vanished is spent

- File: `src/cratekit/core/restore.py`
- Source: `u953.json`, row `M14_spendable_capture_skips_the_sources`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_wal_r1665.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_wal_r1665.py::test_a_capture_that_lost_its_log_after_the_verdict_is_refused_by_the_plan[-wal]`

Old text:

```
    snapshot.assert_sources_present(captured)
```

New text:

```
    pass
```

### `r1924.T10_blank_is_cleared`

_write: clear nothing, so a key tag absent before the adopt keeps the adopted key

- File: `src/cratekit/core/restore_tags.py`
- Source: `r1924.json`, row `T10_blank_is_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 12 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_blank_key_tag_is_put_back_absent_never_an_empty_tag`
  - `tests/test_restore_tags.py::test_a_clear_that_fails_is_a_failed_file`
  - `tests/test_restore_tags.py::test_a_file_that_cannot_be_written_is_named_and_the_run_is_not_ok`
  - `tests/test_restore_tags.py::test_a_file_that_does_not_read_back_is_named`
  - `tests/test_restore_tags.py::test_a_later_adopt_that_wrote_files_and_no_rows_has_its_files_put_back[abandoned]`
  - `tests/test_restore_tags.py::test_a_later_adopt_that_wrote_files_and_no_rows_has_its_files_put_back[open]`
  - `tests/test_restore_tags.py::test_a_later_adopt_the_restore_discards_puts_its_files_back_too`
  - `tests/test_restore_tags.py::test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head`
  - `tests/test_restore_tags.py::test_a_restore_puts_the_row_the_title_tag_and_the_key_tag_back`
  - `tests/test_restore_tags.py::test_the_files_go_back_with_the_latch_still_held`
  - `tests/test_restore_tags.py::test_the_title_tag_goes_back_to_the_file_s_own_value_not_the_row_s`
  - `tests/test_restore_tags.py::test_two_later_adopts_put_a_file_back_to_before_the_earlier`

Old text:

```
    cleared = [name for name, value in changes.items() if not value]
```

New text:

```
    cleared = []
```

### `r1924.T11_both_halves_written`

_write: a successful write of the non-blank values skips the clear

- File: `src/cratekit/core/restore_tags.py`
- Source: `r1924.json`, row `T11_both_halves_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 12 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_blank_key_tag_is_put_back_absent_never_an_empty_tag`
  - `tests/test_restore_tags.py::test_a_clear_that_fails_is_a_failed_file`
  - `tests/test_restore_tags.py::test_a_file_that_cannot_be_written_is_named_and_the_run_is_not_ok`
  - `tests/test_restore_tags.py::test_a_file_that_does_not_read_back_is_named`
  - `tests/test_restore_tags.py::test_a_later_adopt_that_wrote_files_and_no_rows_has_its_files_put_back[abandoned]`
  - `tests/test_restore_tags.py::test_a_later_adopt_that_wrote_files_and_no_rows_has_its_files_put_back[open]`
  - `tests/test_restore_tags.py::test_a_later_adopt_the_restore_discards_puts_its_files_back_too`
  - `tests/test_restore_tags.py::test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head`
  - `tests/test_restore_tags.py::test_a_restore_puts_the_row_the_title_tag_and_the_key_tag_back`
  - `tests/test_restore_tags.py::test_the_files_go_back_with_the_latch_still_held`
  - `tests/test_restore_tags.py::test_the_title_tag_goes_back_to_the_file_s_own_value_not_the_row_s`
  - `tests/test_restore_tags.py::test_two_later_adopts_put_a_file_back_to_before_the_earlier`

Old text:

```
            and (not cleared or tags.clear_tags(path, cleared))
```

New text:

```
            or (not cleared or tags.clear_tags(path, cleared))
```

### `r1924.T14_dry_run_writes`

put_back: ignore the dry run, so a rehearsal writes the files

- File: `src/cratekit/core/restore_tags.py`
- Source: `r1924.json`, row `T14_dry_run_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_dry_run_finds_a_file_gone_and_refuses_as_the_run_would`
  - `tests/test_restore_tags.py::test_a_dry_run_puts_no_file_back`
  - `tests/test_restore_tags.py::test_a_dry_run_writes_no_file`

Old text:

```
        if dry_run:
            if now is None:
```

New text:

```
        if False:
            if now is None:
```

### `r1924.T15_only_what_differs`

put_back: write both tags whatever the file holds

- File: `src/cratekit/core/restore_tags.py`
- Source: `r1924.json`, row `T15_only_what_differs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_file_already_as_it_was_writes_nothing_and_reads_back`
  - `tests/test_restore_tags.py::test_only_the_tag_that_differs_is_written`

Old text:

```
            if now is None or now[name] != before.value(name)
```

New text:

```
            if True
```

### `r1924.T16_write_failure_counted`

put_back: a write that fails is not counted failed and falls through to the read back

- File: `src/cratekit/core/restore_tags.py`
- Source: `r1924.json`, row `T16_write_failure_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_clear_that_fails_is_a_failed_file`
  - `tests/test_restore_tags.py::test_a_file_that_cannot_be_written_is_named_and_the_run_is_not_ok`
  - `tests/test_restore_tags.py::test_an_unknown_container_is_one_failed_file`

Old text:

```
        if changes and not _write(before.path, changes):
```

New text:

```
        if changes and not _write(before.path, changes) and False:
```

### `r1924.T18_unwritten_includes_wrong`

TagsPutBack.unwritten: name only the files that failed, so one that does not read back ends ok

- File: `src/cratekit/core/restore_tags.py`
- Source: `r1924.json`, row `T18_unwritten_includes_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 411 against a baseline of 411
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_file_that_does_not_read_back_is_named`
  - `tests/test_restore_tags.py::test_the_answer_carries_every_count_and_every_name`

Old text:

```
        return self.failed + self.wrong
```

New text:

```
        return self.failed
```

### `u339.M19_restore_per_field`

befores: a later record's tag overwrites the earlier record's for a file

- File: `src/cratekit/core/restore_tags.py`
- Source: `u339.json`, row `M19_restore_per_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_tags.py`, `tests/test_tag_set.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_tags.py::test_a_later_adopt_the_restore_discards_puts_its_files_back_too`
  - `tests/test_restore_tags.py::test_the_first_record_to_name_a_file_wins_and_each_path_is_rebased`
  - `tests/test_restore_tags.py::test_two_later_adopts_put_a_file_back_to_before_the_earlier`

Old text:

```
                if held.value(name) is None and kept.value(name) is not None
```

New text:

```
                if kept.value(name) is not None
```

### `r431-a.A6_a_standing_companion_is_rewritten`

beside overwrites a companion that already stands, so a second guest's deletion restamps the shared one

- File: `src/cratekit/core/review.py`
- Source: `r431-a.json`, row `A6_a_standing_companion_is_rewritten`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_reports.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adoption.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_reports_cli.py`, `tests/test_review_queue.py`, `tests/test_tag_workers.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 3018 against a baseline of 3018
- Kills: 1 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_second_deletion_leaves_the_shared_companion_exactly_as_it_stood`

Old text:

```
                if standing is not None and standing.suppressing:
                    continue
```

New text:

```
                if standing is None and standing is not None:
                    continue
```

### `r431-a.A7_beside_written_when_the_record_stood`

A record that already stood still writes its beside records, so a companion lifted alone comes back

- File: `src/cratekit/core/review.py`
- Source: `r431-a.json`, row `A7_beside_written_when_the_record_stood`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_reports.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adoption.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_reports_cli.py`, `tests/test_review_queue.py`, `tests/test_tag_workers.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 3018 against a baseline of 3018
- Kills: 2 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_lifted_alone_does_not_come_back_behind_a_persons_back`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_that_already_stood_gains_no_companion`

Old text:

```
            if existing is not None and existing.suppressing:
                return existing
            suppression = Suppression(
```

New text:

```
            if existing is not None and existing.suppressing and not beside:
                return existing
            suppression = Suppression(
```

### `r431-a.A8_also_is_never_asked`

revoke ignores also, so lifting a credited tombstone leaves its companion suppressing

- File: `src/cratekit/core/review.py`
- Source: `r431-a.json`, row `A8_also_is_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_reports.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adoption.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_reports_cli.py`, `tests/test_review_queue.py`, `tests/test_tag_workers.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 3018 against a baseline of 3018
- Kills: 6 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_is_found_by_its_pointer_when_the_stripping_rule_has_moved`
  - `tests/test_uncredited_tombstone.py::test_a_companion_two_deletions_share_outlives_the_first_lift_and_not_the_second`
  - `tests/test_uncredited_tombstone.py::test_a_credited_deletion_is_one_write_and_so_is_lifting_it`
  - `tests/test_uncredited_tombstone.py::test_a_tombstone_with_no_pointer_still_accounts_for_the_companion_it_strips_to`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_credited_tombstone_lifts_its_companion`
  - `tests/test_uncredited_tombstone.py::test_the_shared_companion_is_also_found_in_the_other_order`

Old text:

```
            with_it = tuple(also(existing, dict(recorded))) if also is not None else ()
```

New text:

```
            with_it = ()
```

### `r431-a.A9_an_already_lifted_record_is_lifted_again`

also restamps a record that was already lifted, and fails on an identifier that names nothing

- File: `src/cratekit/core/review.py`
- Source: `r431-a.json`, row `A9_an_already_lifted_record_is_lifted_again`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_reports.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adoption.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_match_states.py`, `tests/test_reports_cli.py`, `tests/test_review_queue.py`, `tests/test_tag_workers.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 3018 against a baseline of 3018
- Kills: 1 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_companion_already_lifted_keeps_the_lift_it_was_given`

Old text:

```
                if other is not None and other.suppressing:
                    recorded[other_id] = lifted(other)
```

New text:

```
                if other is not None:
                    recorded[other_id] = lifted(other)
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

### `r679-a.A3_supersede_readers_predicate`

supersede: widen the write's condition to the reader's unresolved predicate, so a verdict a newer build wrote is overwritten

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A3_supersede_readers_predicate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 834 against a baseline of 834
- Kills: 1 (killed)
- Killed:
  - `tests/test_review_queue.py::test_supersede_never_overwrites_a_verdict_this_build_cannot_read`

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
            f"AND (verdict IS NULL OR verdict NOT IN ('accepted', 'rejected', 'superseded')) ORDER BY ordinal",
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
            f"updated = ? WHERE item_id IN ({marks}) AND (verdict IS NULL OR verdict NOT IN ('accepted', 'rejected', 'superseded'))",
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

### `u301.R2_revoke_drops_the_actor`

DecisionStore.revoke: record no actor on a lifted record, so a revocation names nobody

- File: `src/cratekit/core/review.py`
- Source: `u301.json`, row `R2_revoke_drops_the_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_tombstones.py`, `tests/test_uncredited_tombstone.py`
- Collected: 226 against a baseline of 226
- Kills: 3 (killed)
- Killed:
  - `tests/test_tombstones.py::test_a_revoked_tombstone_stays_listable_so_the_two_cases_can_be_told_apart`
  - `tests/test_uncredited_tombstone.py::test_a_companion_already_lifted_keeps_the_lift_it_was_given`
  - `tests/test_uncredited_tombstone.py::test_lifting_a_credited_tombstone_lifts_its_companion`

Old text:

```
                return replace(one, revoked=True, revoked_at=lifted_at, revoked_by=actor)
```

New text:

```
                return replace(one, revoked=True, revoked_at=lifted_at, revoked_by=None)
```

### `r798-d.K11_the_shared_matcher_reads_a_substring_needle`

_rule_matches: drop the any_of arm of the matcher the second review made one function of, so no rule of either table that names a substring claims a word

- File: `src/cratekit/core/routing.py`
- Source: `r798-d.json`, row `K11_the_shared_matcher_reads_a_substring_needle`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_taxonomy.py`, `tests/test_routing_parity.py`
- Collected: 1150 against a baseline of 1150
- Kills: 101 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[African Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Alternative]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Asian Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Blues]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Brazilian Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Christian]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Classical]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Country]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Cumbia]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Dance]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Electro]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Films/Games]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Folk]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Indian Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Jazz]`
  - ... and 86 more, see the JSON sidecar

Old text:

```
        or (rule.any_of and any(needle in value for needle in rule.any_of))
    )


def gate_decisions(
```

New text:

```
    )


def gate_decisions(
```

### `r799-a.R1_a_table_is_read_only_for_its_source`

resolver: read the general catalogue's table for every caller, a record shop's included

- File: `src/cratekit/core/routing.py`
- Source: `r799-a.json`, row `R1_a_table_is_read_only_for_its_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocabulary.py`, `tests/test_published_genre.py`, `tests/test_tag_remap.py`
- Collected: 511 against a baseline of 511
- Kills: 2 (killed)
- Killed:
  - `tests/test_vocabulary.py::test_a_record_shops_pop_goes_where_it_went_before[None]`
  - `tests/test_vocabulary.py::test_the_record_shops_searcher_names_no_source_to_the_resolver`

Old text:

```
    table = taxonomy.vocabulary(source) if source is not None else None
```

New text:

```
    table = taxonomy.vocabulary(source or "deezer")
```

### `u155.R4_genre_sub_named`

genre_sub_named: answer False, so a gate shows the genre sub as the energy sub

- File: `src/cratekit/core/routing.py`
- Source: `u155.json`, row `R4_genre_sub_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_unplaced_export_names_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
    return _genre_sub_by_id(taxonomy.bucket(bucket_id), sub_id) is not None
```

New text:

```
    return False
```

### `u340.R01_too_coarse_files`

files_by_genre: drop the too coarse test, so a coarse second genre names the fallback's folder

- File: `src/cratekit/core/routing.py`
- Source: `u340.json`, row `R01_too_coarse_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_tag_second.py`
- Collected: 71 against a baseline of 71
- Kills: 4 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_move_into_the_fallback_folder_is_not_taken[first]`
  - `tests/test_second_genre.py::test_a_move_into_the_fallback_folder_is_not_taken[second]`
  - `tests/test_tag_second.py::test_a_genre_that_files_nowhere_refuses_before_anything_is_read[Electronica]`
  - `tests/test_tag_second.py::test_the_shipped_words_this_suite_names_file_as_it_assumes`

Old text:

```
    if not value or taxonomy.is_too_coarse_as_source(value):
        return None
    resolution = resolve_bucket(taxonomy, value)
```

New text:

```
    if not value:
        return None
    resolution = resolve_bucket(taxonomy, value)
```

### `u340.R02_fallback_files`

files_by_genre: let a fallback match name its bucket, so an unknown word files a track into the fallback folder

- File: `src/cratekit/core/routing.py`
- Source: `u340.json`, row `R02_fallback_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_tag_second.py`
- Collected: 71 against a baseline of 71
- Kills: 5 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_second_genre_names_a_second_folder_only_beside_a_genre_that_names_one[fallback]`
  - `tests/test_second_genre.py::test_a_second_genre_names_a_second_folder_only_beside_a_genre_that_names_one[first-fallback]`
  - `tests/test_tag_second.py::test_a_genre_that_files_nowhere_refuses_before_anything_is_read[Polka]`
  - `tests/test_tag_second.py::test_the_shipped_words_this_suite_names_file_as_it_assumes`
  - `tests/test_tag_second.py::test_the_verb_refuses_a_request_it_cannot_plan[files-nowhere]`

Old text:

```
    resolution = resolve_bucket(taxonomy, value)
    if resolution.match is Match.FALLBACK:
        return None
    return resolution.bucket_id
```

New text:

```
    resolution = resolve_bucket(taxonomy, value)
    return resolution.bucket_id
```

### `u340.R03_same_folder`

second_bucket: drop the same folder test, so a second genre naming the first's folder files a second entry there

- File: `src/cratekit/core/routing.py`
- Source: `u340.json`, row `R03_same_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_tag_second.py`, `tests/test_rebuild.py`
- Collected: 183 against a baseline of 183
- Kills: 4 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_one_genre_track_derives_exactly_as_before`
  - `tests/test_second_genre.py::test_a_second_genre_names_a_second_folder_only_beside_a_genre_that_names_one[same-folder]`
  - `tests/test_tag_second.py::test_each_chosen_row_lands_in_one_outcome`
  - `tests/test_tag_second.py::test_the_shipped_words_this_suite_names_file_as_it_assumes`

Old text:

```
    if second is None or second == first:
```

New text:

```
    if second is None:
```

### `u340.R04_first_files_nowhere`

second_bucket: drop the first genre test, so a track with no routable genre is filed by its second alone

- File: `src/cratekit/core/routing.py`
- Source: `u340.json`, row `R04_first_files_nowhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_tag_second.py`
- Collected: 71 against a baseline of 71
- Kills: 3 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_move_into_the_fallback_folder_is_not_taken[first]`
  - `tests/test_second_genre.py::test_a_second_genre_names_a_second_folder_only_beside_a_genre_that_names_one[first-blank]`
  - `tests/test_second_genre.py::test_a_second_genre_names_a_second_folder_only_beside_a_genre_that_names_one[first-fallback]`

Old text:

```
    first = files_by_genre(taxonomy, raw_genre)
    if first is None:
        return None
    second
```

New text:

```
    first = files_by_genre(taxonomy, raw_genre)
    second
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

### `u138.E1_terminal_check`

Existing guard sample: the terminal check on a person's answer

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `E1_terminal_check`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4050 against a baseline of 4050
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_without_a_terminal_is_still_refused_over_fresh_backups`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_write_session.py::test_an_agent_shaped_invocation_cannot_mint_the_acknowledgment`
  - `tests/test_write_session.py::test_the_terminal_probe_the_mint_uses_by_default_is_the_real_one`

Old text:

```
        if not probe():

```

New text:

```
        if False:

```

### `u138.S11_rule_not_written`

The record's rule key is not written to the file

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S11_rule_not_written`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4050 against a baseline of 4050
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
            "rule": self.rule,

```

New text:

```
(empty)
```

### `u138.S12_message_names_the_portion`

Reword the refusal so it no longer names the portion's age

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S12_message_names_the_portion`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4050 against a baseline of 4050
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
                f"the {entry.portion} portion is {entry.age_seconds / 86400:.1f} days old"

```

New text:

```
                f"a backup portion is too old ({entry.portion})"

```

### `u138.S13_remedy_points_back_at_ack`

The too old refusal tells a person to acknowledge again rather than to run a backup

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S13_remedy_points_back_at_ack`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4050 against a baseline of 4050
- Kills: 8 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
                remedy=Remedy.RUN_BACKUP,

```

New text:

```
                remedy=Remedy.ACKNOWLEDGE_BACKUP,

```

### `u138.S1_session_rule_gone`

A session's answer falls to the terminal check, as before U138

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S1_session_rule_gone`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4050 against a baseline of 4050
- Kills: 20 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_names_when_an_acknowledgment_lapsed`
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    if decided_by == SESSION_ACTOR:

```

New text:

```
    if False:

```

### `u138.S2_any_answer_gets_the_age_rule`

Any recorded answer, a person's included, mints without a terminal on young backups

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S2_any_answer_gets_the_age_rule`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4050 against a baseline of 4050
- Kills: 13 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[session.ack]`
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_a_person_without_a_terminal_is_still_refused_over_fresh_backups`
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_second_mint_replaces_the_record_and_moves_the_window`
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`
  - `tests/test_session_cli.py::test_the_cli_mints_an_acknowledgment_a_real_destructive_verb_then_spends`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
    if decided_by == SESSION_ACTOR:

```

New text:

```
    if decided_by is not None:

```

### `u138.S3_stale_not_refused`

The session mints over a portion five days old or of unknown age

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S3_stale_not_refused`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4050 against a baseline of 4050
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
        if stale:
```

New text:

```
        if False:
```

### `u138.S6_bound_six_days`

The bound is six days rather than five

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S6_bound_six_days`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4050 against a baseline of 4050
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_five_days_as_the_author_set_it`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`

Old text:

```
SESSION_MAX_BACKUP_AGE = timedelta(days=5)

```

New text:

```
SESSION_MAX_BACKUP_AGE = timedelta(days=6)

```

### `u138.S8_rule_not_recorded`

The record always says the terminal rule minted it

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S8_rule_not_recorded`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4050 against a baseline of 4050
- Kills: 6 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        shown=shown,
        rule=rule,

```

New text:

```
        shown=shown,
        rule=RULE_TERMINAL,

```

### `u138.S9_answer_not_recorded`

The record never says who answered the gate

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S9_answer_not_recorded`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4050 against a baseline of 4050
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        rule=rule,
        decided_by=decided_by,

```

New text:

```
        rule=rule,
        decided_by=None,

```

### `u300.S15_terminal_probe_local`

record_acknowledgment asks the part's own terminal probe, so a patched probe is not asked

- File: `src/cratekit/core/session_ack.py`
- Source: `u300.json`, row `S15_terminal_probe_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_second_mint_replaces_the_record_and_moves_the_window`
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`
  - `tests/test_session_cli.py::test_the_cli_mints_an_acknowledgment_a_real_destructive_verb_then_spends`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`
  - `tests/test_write_session.py::test_the_terminal_probe_the_mint_uses_by_default_is_the_real_one`

Old text:

```
        probe = terminal or _session().has_controlling_terminal
```

New text:

```
        probe = terminal or has_controlling_terminal
```

### `u300.S16_derive_actor_local`

record_acknowledgment names its actor with the part's own derive_actor

- File: `src/cratekit/core/session_ack.py`
- Source: `u300.json`, row `S16_derive_actor_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_the_recorded_actor_is_the_derived_one_and_not_a_name_from_anywhere_else`

Old text:

```
        actor=_session().derive_actor(),
```

New text:

```
        actor=derive_actor(),
```

### `u329.P6_session_ack_wrong_family`

session_ack binds _session to the writer's accessor, so every _session().name reads the wrong module

- File: `src/cratekit/core/session_ack.py`
- Source: `u329.json`, row `P6_session_ack_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`
- Collected: 362 against a baseline of 362
- Kills: 69 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_declined_run_queues_nothing_at_all`
  - `tests/test_adopt_apply_cli.py::test_a_nested_session_is_refused_rather_than_deadlocking`
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_a_second_run_holding_the_lock_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_a_volume_whose_identity_moved_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_an_approval_recorded_against_a_plan_that_has_since_moved_is_refused`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_is_armed_on_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_reaches_a_share_outside_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_shows_every_entry_the_digest_was_taken_over`
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_a_run_whose_every_transfer_failed_publishes_no_age_at_all`
  - `tests/test_deferred_routing.py::test_a_bucket_folder_that_does_not_exist_yet_is_not_mistaken_for_a_rename`
  - `tests/test_deferred_routing.py::test_a_crash_between_the_commit_and_the_mark_converges`
  - ... and 54 more, see the JSON sidecar

Old text:

```
from cratekit.core.session_call_time import session as _session
```

New text:

```
from cratekit.core.rb_call_time import writer as _session
```

### `u48-author.S1_remedy_fixed_at_repair`

The session names the repair token again, which is the defect this unit closed

- File: `src/cratekit/core/session_ack.py`
- Source: `u48-author.json`, row `S1_remedy_fixed_at_repair`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1535 against a baseline of 1535
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_fact_file_from_a_newer_build_asks_for_an_upgrade`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
```

New text:

```
            remedy=Remedy.REPAIR_BACKUP_FACTS,
```

### `u48-author.S2_remedy_fixed_at_grant`

The same defect mirrored: hard code the permission token over every condition

- File: `src/cratekit/core/session_ack.py`
- Source: `u48-author.json`, row `S2_remedy_fixed_at_grant`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_ack.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 1535 against a baseline of 1535
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_fact_file_from_a_newer_build_asks_for_an_upgrade`
  - `tests/test_write_session.py::test_an_unreadable_backup_fact_file_refuses_the_mint`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
```

New text:

```
            remedy=Remedy.GRANT_PATH_ACCESS,
```

### `u329.A2_session_accessor_returns_the_writer`

session_call_time.session returns rb_writer, not session, so the session parts read the writer's names

- File: `src/cratekit/core/session_call_time.py`
- Source: `u329.json`, row `A2_session_accessor_returns_the_writer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_deletion.py`, `tests/test_session_ack_by_session.py`
- Collected: 542 against a baseline of 542
- Kills: 210 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_binding_that_cannot_say_how_many_memberships_it_holds_refuses`
  - `tests/test_deletion.py::test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable`
  - `tests/test_deletion.py::test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
  - `tests/test_deletion.py::test_a_confirmed_file_is_trashed_and_leaves_a_tombstone`
  - `tests/test_deletion.py::test_a_confirmed_item_invalidated_before_the_move_is_refused_at_move_time`
  - `tests/test_deletion.py::test_a_confirmed_removal_the_person_deleted_in_the_finder_does_not_block_the_next_one`
  - `tests/test_deletion.py::test_a_corrected_prefix_rule_lets_the_confirmed_deletion_through_on_the_retry`
  - `tests/test_deletion.py::test_a_dead_prefix_rule_stops_the_whole_pass_before_anything_is_offered`
  - `tests/test_deletion.py::test_a_decline_recorded_between_the_plan_and_the_move_stops_the_move`
  - `tests/test_deletion.py::test_a_decline_the_queue_simply_does_not_hold_is_still_addressable`
  - `tests/test_deletion.py::test_a_decline_whose_review_item_cannot_be_addressed_refuses`
  - `tests/test_deletion.py::test_a_declined_row_holds_the_watermark_and_lets_it_go_when_revoked`
  - `tests/test_deletion.py::test_a_decoy_volume_at_the_configured_path_refuses_before_anything_resolves`
  - `tests/test_deletion.py::test_a_different_disk_at_a_mapped_target_stops_the_apply_before_any_file_moves`
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_retires_nothing_nobody_answered_for`
  - ... and 195 more, see the JSON sidecar

Old text:

```
    from cratekit.core import session

    return session
```

New text:

```
    from cratekit.core import rb_writer as session

    return session
```

### `r598-a.A1_state_check_widened_to_non_terminal`

orphaned: accept any non terminal record rather than only open, so awaiting-import and committed-unverified records with a dead holder are abandoned and their own remedies hidden

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A1_state_check_widened_to_non_terminal`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_the_two_states_with_their_own_remedy_are_never_abandoned[awaiting-import]`
  - `tests/test_session_cli.py::test_the_two_states_with_their_own_remedy_are_never_abandoned[committed-unverified]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[awaiting-import-gone-False]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[committed-unverified-gone-False]`

Old text:

```
    if record.state is not _session().SessionState.OPEN:
        return False
    recorded = record.detail.get(_session().HOLDER_KEY)
```

New text:

```
    if record.terminal:
        return False
    recorded = record.detail.get(_session().HOLDER_KEY)
```

### `r598-a.A2_no_holder_read_as_gone`

orphaned: read a record with no recorded holder as orphaned, so every intake landing left open for a deferred placement is abandoned

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A2_no_holder_read_as_gone`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_open_record_that_names_no_holder_is_never_abandoned`
  - `tests/test_write_session.py::test_abandon_orphaned_sessions_ends_only_the_orphans`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-None-False]`

Old text:

```
    if not isinstance(recorded, Mapping):
        return False
```

New text:

```
    if not isinstance(recorded, Mapping):
        return True
```

### `r598-a.A3_liveness_not_consulted`

orphaned: skip holder_alive and judge every open record with a holder orphaned, so a running write's record is ended behind it

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A3_liveness_not_consulted`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 8 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[alive]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_write_session.py::test_abandon_orphaned_sessions_ends_only_the_orphans`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-here-False]`
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-other-host-False]`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
    return not holder_alive(holder, here=here)
```

New text:

```
    return True
```

### `r598-a.A4_unreadable_holder_read_as_gone`

orphaned: judge a holder this build cannot parse as gone rather than alive

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A4_unreadable_holder_read_as_gone`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_orphaned_needs_open_a_recorded_holder_and_proof_it_is_gone[open-unreadable-False]`

Old text:

```
    except (TypeError, ValueError):
        return False
    return not holder_alive(holder, here=here)
```

New text:

```
    except (TypeError, ValueError):
        return True
    return not holder_alive(holder, here=here)
```

### `r598-a.A7_sweep_ignores_the_shown_list`

abandon_orphaned_sessions: end every orphan rather than only those shown, so one answer ends records the question never listed

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A7_sweep_ignores_the_shown_list`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_the_sweep_ends_only_the_orphans_it_was_shown`

Old text:

```
        if (shown is None or record.session_id in shown) and orphaned(record, here=here)
```

New text:

```
        if orphaned(record, here=here)
```

### `r598-b.B7_sample_live_holder_released`

release_stale_lock: skip the live holder refusal (existing guard, sampled because the sweep now sits behind it)

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-b.json`, row `B7_sample_live_holder_released`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`, `tests/test_write_session.py`
- Collected: 185 against a baseline of 185
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_refused_or_aborted_release_abandons_nothing[live-lock-holder]`
  - `tests/test_write_session.py::test_a_live_holder_this_platform_will_not_describe_is_assumed_alive`
  - `tests/test_write_session.py::test_the_lock_left_by_another_machine_with_this_host_name_is_not_releasable`

Old text:

```
    if holder_alive(recorded):
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r647-a.B10_live_identifier_not_asked`

_gone_since_an_earlier_boot: skip the live process check, so a live holder read through a moved clock has its claim cleared mid write

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B10_live_identifier_not_asked`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_live_process_read_through_a_moved_clock_is_kept`
  - `tests/test_write_session.py::test_a_live_process_whose_start_time_moved_with_the_clock_is_kept`
  - `tests/test_write_session.py::test_a_platform_that_cannot_say_whether_the_process_exists_keeps_it`

Old text:

```
    return _session().process_exists(holder.pid) is False
```

New text:

```
    return True
```

### `r647-a.B11_start_time_compared_again`

_gone_since_an_earlier_boot: the review's defect restored, a live identifier keeps the claim only when its start time matches, so the Linux shape of a stepped clock clears a live claim

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B11_start_time_compared_again`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_live_process_whose_start_time_moved_with_the_clock_is_kept`

Old text:

```
    return _session().process_exists(holder.pid) is False
```

New text:

```
    exists = _session().process_exists(holder.pid)
    if exists is None:
        return False
    return not (exists and _session().process_started(holder.pid) == holder.started)
```

### `r647-a.B12_cross_boot_never_judged`

holder_alive: every other boot judged alive again, the state before this unit, so a power loss stays a dead end

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B12_cross_boot_never_judged`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_write_session.py::test_a_boot_just_past_the_drift_margin_is_gone`
  - `tests/test_write_session.py::test_a_holder_from_an_earlier_boot_of_this_machine_is_gone`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`

Old text:

```
    if holder.boot != reference.boot:
        return not _gone_since_an_earlier_boot(holder, reference)
```

New text:

```
    if holder.boot != reference.boot:
        return True
```

### `r647-a.B13_current_holder_names_no_machine`

current_holder: record the declared unknown instead of the machine identity, so no holder is ever provably this machine's

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B13_current_holder_names_no_machine`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`
  - `tests/test_write_session.py::test_this_platform_names_its_machine_as_a_digest_not_the_serial`

Old text:

```
        machine=_session().machine_identity(),
```

New text:

```
        machine=UNKNOWN_IDENTITY,
```

### `r647-a.B14_machine_not_read_back`

Holder.from_json: ignore the recorded machine, so a record or lock read from disk never names one

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B14_machine_not_read_back`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_write_session.py::test_the_holder_carries_all_five_identifying_fields`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
            machine=str(data.get("machine", UNKNOWN_IDENTITY)),
```

New text:

```
            machine=UNKNOWN_IDENTITY,
```

### `r647-a.B15_machine_not_written`

Holder.to_json: omit the machine, so nothing on disk carries it

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B15_machine_not_written`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_write_session.py::test_the_holder_carries_all_five_identifying_fields`
  - `tests/test_write_session.py::test_the_lock_left_by_this_machines_earlier_boot_is_releasable`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
            "machine": self.machine,

```

New text:

```
(empty)
```

### `r647-a.B1_unknown_machine_not_refused`

_gone_since_an_earlier_boot: drop the unknown machine check, so two holders that both name no machine compare equal as text and a holder recorded before the field existed is cleared on a machine that cannot name itself

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B1_unknown_machine_not_refused`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_two_unknown_machine_identities_are_not_one_machine`

Old text:

```
    if UNKNOWN_IDENTITY in (holder.machine, reference.machine):
        return False
    if holder.machine != reference.machine:
```

New text:

```
    if holder.machine != reference.machine:
```

### `r647-a.B2_machine_equality_dropped`

_gone_since_an_earlier_boot: stop comparing machine identities, so another machine sharing the host name and the library drive has its claim cleared on the host name alone

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B2_machine_equality_dropped`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[another-machine-with-this-host-name]`
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[another machine with this host name-changes0]`
  - `tests/test_write_session.py::test_the_lock_left_by_another_machine_with_this_host_name_is_not_releasable`

Old text:

```
    if holder.machine != reference.machine:
        return False
```

New text:

```
    if holder.machine is None:
        return False
```

### `r647-a.B3_unparsable_boot_read_as_gone`

_gone_since_an_earlier_boot: judge a boot that is not a number as proof of an earlier boot rather than as no proof

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B3_unparsable_boot_read_as_gone`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot that is not a number-changes5]`

Old text:

```
    except ValueError:
        return False
    if not math.isfinite(earlier_by)
```

New text:

```
    except ValueError:
        return process_exists(holder.pid) is False
    if not math.isfinite(earlier_by)
```

### `r647-a.B4_infinite_boot_accepted`

_gone_since_an_earlier_boot: drop the finiteness check, so a boot recorded as minus infinity reads as infinitely earlier

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B4_infinite_boot_accepted`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot that is not finite-changes6]`

Old text:

```
    if not math.isfinite(earlier_by) or earlier_by <= BOOT_DRIFT_SECONDS:
```

New text:

```
    if earlier_by <= BOOT_DRIFT_SECONDS:
```

### `r647-a.B5_drift_margin_halved`

BOOT_DRIFT_SECONDS: 60 to 30, a realistic nearby value, so a clock adjustment of forty seconds reads as a restart

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B5_drift_margin_halved`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_boot_just_past_the_drift_margin_is_gone`
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot exactly at the drift margin-changes3]`

Old text:

```
BOOT_DRIFT_SECONDS = 60.0
```

New text:

```
BOOT_DRIFT_SECONDS = 30.0
```

### `r647-a.B6_drift_margin_doubled`

BOOT_DRIFT_SECONDS: 60 to 120, so a restart a minute and a half apart is kept for no reason

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B6_drift_margin_doubled`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_boot_just_past_the_drift_margin_is_gone`

Old text:

```
BOOT_DRIFT_SECONDS = 60.0
```

New text:

```
BOOT_DRIFT_SECONDS = 120.0
```

### `r647-a.B7_margin_boundary_exclusive`

_gone_since_an_earlier_boot: less than instead of less than or equal, so a boot exactly at the margin is judged earlier

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B7_margin_boundary_exclusive`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a boot exactly at the drift margin-changes3]`

Old text:

```
earlier_by <= BOOT_DRIFT_SECONDS:
```

New text:

```
earlier_by < BOOT_DRIFT_SECONDS:
```

### `r647-a.B8_direction_ignored`

_gone_since_an_earlier_boot: take the distance between the boots rather than which came first, so a LATER boot reading reads as an earlier boot

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B8_direction_ignored`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_holder_from_another_boot_is_kept_without_proof_it_was_this_machine[a later boot-changes4]`

Old text:

```
        earlier_by = float(reference.boot) - float(holder.boot)
```

New text:

```
        earlier_by = abs(float(reference.boot) - float(holder.boot))
```

### `r647-a.B9_platform_silence_read_as_gone`

_gone_since_an_earlier_boot: read a platform declining to say whether the process exists as gone

- File: `src/cratekit/core/session_holders.py`
- Source: `r647-a.json`, row `B9_platform_silence_read_as_gone`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_holders.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`
- Collected: 602 against a baseline of 602
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_platform_that_cannot_say_whether_the_process_exists_keeps_it`

Old text:

```
    return _session().process_exists(holder.pid) is False
```

New text:

```
    return _session().process_exists(holder.pid) is not True
```

### `u300.S13_process_exists_local`

a holder's death since an earlier boot is judged by the part's own process_exists

- File: `src/cratekit/core/session_holders.py`
- Source: `u300.json`, row `S13_process_exists_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_platform_that_cannot_say_whether_the_process_exists_keeps_it`

Old text:

```
    return _session().process_exists(holder.pid) is False
```

New text:

```
    return process_exists(holder.pid) is False
```

### `u329.P7_session_holders_wrong_family`

session_holders binds _session to the writer's accessor, so every _session().name reads the wrong module

- File: `src/cratekit/core/session_holders.py`
- Source: `u329.json`, row `P7_session_holders_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`, `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`
- Collected: 708 against a baseline of 708
- Kills: 81 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_nested_session_is_refused_rather_than_deadlocking`
  - `tests/test_adopt_apply_cli.py::test_a_second_run_holding_the_lock_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_is_armed_on_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_reaches_a_share_outside_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_dead_holders_claim_is_cleared_and_the_refusal_named_it_first`
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_lock_record_that_cannot_be_understood_refuses_by_name`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[alive]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_session_cli.py::test_a_refused_or_aborted_release_abandons_nothing[abort]`
  - ... and 66 more, see the JSON sidecar

Old text:

```
from cratekit.core.session_call_time import session as _session
```

New text:

```
from cratekit.core.rb_call_time import writer as _session
```

### `u49-author.L4_a_malformed_holder_raises_again`

Remove the coercion guard from read_lock_holder, so a lock record with a non numeric pid escapes as a traceback rather than a typed refusal

- File: `src/cratekit/core/session_holders.py`
- Source: `u49-author.json`, row `L4_a_malformed_holder_raises_again`
- Moved: U953 merged read_lock_holder's JSON parse and holder coercion under one try, so narrowing its except to the parse error alone is the same removed coercion guard, the parse still answering None
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2592 against a baseline of 2592
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_lock_record_that_cannot_be_understood_refuses_by_name`

Old text:

```
    except (TypeError, ValueError, AttributeError):
```

New text:

```
    except json.JSONDecodeError:
```

### `r44-a.S10_default_slug`

Look the slug up with a default, so a verdict in neither table wears the mismatch slug

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S10_default_slug`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_verdict_in_neither_table_fails_rather_than_wearing_the_mismatch_slug`

Old text:

```
            reason = _session()._MAPPED_REASONS[status.state]
```

New text:

```
            reason = _session()._MAPPED_REASONS.get(status.state, "mapped-volume-mismatch")
```

### `r44-a.S1_empty_slot`

Never refuse an empty mount slot, so an identity read through an ejected drive's leftover directory is compared and can match

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S1_empty_slot`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_an_ejected_drive_is_never_offered_the_boot_disks_identity_to_record`
  - `tests/test_write_session.py::test_an_empty_mount_slot_refuses_even_when_the_recorded_identity_matches_it`

Old text:

```
        source = preflight.identity_source(probe)
        if source is None:
```

New text:

```
        source = preflight.identity_source(probe)
        if False:
```

### `r44-a.S2_proved_widened`

Let NOT_MOUNTED count as a proved identity, which is the pass set widening by one verdict

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S2_proved_widened`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 4 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_write_session.py::test_a_recorded_volume_that_is_not_mounted_anywhere_has_its_own_slug`
  - `tests/test_write_session.py::test_every_mount_verdict_about_a_rule_target_was_decided_exactly_once[MountState.NOT_MOUNTED]`
  - `tests/test_write_session.py::test_the_verdicts_that_prove_a_rule_target_are_spelled_out`

Old text:

```
    {preflight.MountState.OK, preflight.MountState.LIBRARY_PATH_MISSING}
)
```

New text:

```
    {
        preflight.MountState.OK,
        preflight.MountState.LIBRARY_PATH_MISSING,
        preflight.MountState.NOT_MOUNTED,
    }
)
```

### `r44-a.S3_default_to_library`

Hold a rule outside the library root with nothing recorded to the LIBRARY'S identity instead of refusing it

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S3_default_to_library`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_rule_is_held_to_its_own_identity_then_the_librarys_then_to_nothing`
  - `tests/test_write_session.py::test_a_target_outside_the_root_with_nothing_recorded_refuses_and_hands_over_the_identity`

Old text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return None
```

New text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return cfg.library.volume_id
```

### `r44-a.S4_inside_root_unheld`

Hold a rule inside the library root to nothing of the library's, so a nested foreign volume is judged as unrecorded rather than foreign

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S4_inside_root_unheld`
- Moved: Moved from src/cratekit/core/session.py to src/cratekit/core/session_volumes.py by U300, which replayed this text there and kept the kill in u300-replay-after-b.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_deletion.py`
- Collected: 479 against a baseline of 479
- Kills: 6 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`
  - `tests/test_write_session.py::test_a_different_disk_at_a_rules_target_refuses_and_names_the_rule`
  - `tests/test_write_session.py::test_a_foreign_volume_under_a_rule_that_recorded_nothing_offers_nothing_to_record`
  - `tests/test_write_session.py::test_a_rule_is_held_to_its_own_identity_then_the_librarys_then_to_nothing`
  - `tests/test_write_session.py::test_a_volume_nested_under_the_library_root_is_not_the_library`
  - `tests/test_write_session.py::test_the_file_is_proved_where_the_file_is_and_not_where_the_rule_points`

Old text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return None
```

New text:

```
    return None
```

