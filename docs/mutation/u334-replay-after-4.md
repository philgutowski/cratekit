# Mutation table: u334-replay-after-4

Measured by `scripts/mutate.py` on 2026-11-24 05:00 UTC, branch `HEAD` at `90c0cc08`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23214 collected. pytest invocations for this batch: 325.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 05:00 UTC for commit `90c0cc0829da`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 59, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23214 against 23214. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u41-naming-independent.E1_budget_bypassed` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1585 | 4 | killed |
| `u41-naming-independent.E3_budget_min_becomes_max` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1585 | 8 | killed |
| `u41-naming-independent.E4_path_separator_byte_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1585 | 3 | killed |
| `u41-naming-independent.E5_truncation_tail_not_reserved` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1585 | 5 | killed |
| `u41-naming-independent.F3_body_tag_preference_flipped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1585 | 31 | killed |
| `u41-naming-independent.F4_body_tag_fallback_dropped` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1585 | 52 | killed |
| `u41-naming-independent.F6_filename_prefers_the_title_body` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1585 | 51 | killed |
| `u41-naming-independent.F7_library_name_split_from_the_tag` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1585 | 3 | killed |
| `u293.L1_dead_mark_charged` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 3 | killed |
| `u293.L2_night_reset` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 4 | killed |
| `u293.L3_spent_off_by_one` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 2 | killed |
| `u293.L4_noon_to_noon` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 3 | killed |
| `u293.L6_unreadable_gate_refuses` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 1 | killed |
| `u12-independent-round-6.C2_reserve_halved` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 2 | killed |
| `u12-independent-round-6.C4_darwin_headroom` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 4 | killed |
| `u12-independent-round-6.C5_swap_threshold` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 4 | killed |
| `u12-independent-round-6.C6_used_percent_ceiling` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 2 | killed |
| `u12-independent-round-6.C7_max_tasks_per_child` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 3 | killed |
| `u12-independent-round-6.C8_probe_deadline` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.C9_reap_budget` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.G1_dotdot_not_refused` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.G2_containment_dropped` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 2 | killed |
| `u12-independent-round-6.G3_headroom_can_go_negative` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.G4_controller_substring_match` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 2 | killed |
| `u12-independent-round-6.G5_loosest_cap_wins` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.G6_cgroup_cap_ignored` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 3 | killed |
| `u12-independent-round-6.G7_valueerror_escapes_the_reader` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.M1_measurement_below_the_floor` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.M2_nonsense_measurement_accepted` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 2 | killed |
| `u12-independent-round-6.M3_zero_deadline_allowed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.M4_model_freed_before_the_reading` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.M5_terminate_rung_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 3 | killed |
| `u12-independent-round-6.M6_kill_rung_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.M7_parent_keeps_the_write_end` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.M8_no_reap_after_the_probe` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.P10_recycle_reported_for_in_process` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 2 | killed |
| `u12-independent-round-6.P12_unreadable_falls_back_to_ceiling` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 8 | killed |
| `u12-independent-round-6.P1_reserve_not_applied` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 13 | killed |
| `u12-independent-round-6.P2_order_reversed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 5 | killed |
| `u12-independent-round-6.P3_budget_can_go_negative` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 2 | killed |
| `u12-independent-round-6.P4_no_floor_of_one_worker` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 11 | killed |
| `u12-independent-round-6.P5_tie_goes_to_the_ceiling` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.P6_no_insufficient_memory_bound` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 5 | killed |
| `u12-independent-round-6.R1_available_type_check` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 5 | killed |
| `u12-independent-round-6.R2_available_never_raises` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 2 | killed |
| `u12-independent-round-6.R3_pressure_percent_range` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.R4_pressure_type_check` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 2 | killed |
| `u12-independent-round-6.X1_pool_of_one_built` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.X3_generation_boundary_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.X4_initargs_not_refused` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.X5_in_process_path_removed` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 1 | killed |
| `u12-independent-round-6.X7_generation_size_drops_the_width` | `src/cratekit/core/pool.py` | user | 1 file(s) | 268 | 9 | killed |
| `u241.M01_worker_takes_the_interrupt` | `src/cratekit/core/pool.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u241.M02_worker_outlives_its_parent` | `src/cratekit/core/pool.py` | user | 1 file(s) | 26 | 1 | killed |
| `u241.M03_close_waits_for_unread_work` | `src/cratekit/core/pool.py` | user | 1 file(s) | 26 | 1 | killed |
| `u241.M07_used_percent_gate_is_strict` | `src/cratekit/core/pool.py` | user | 2 file(s) | 294 | 3 | killed |
| `u241.M08_plan_forgets_which_gate` | `src/cratekit/core/pool.py` | user | 2 file(s) | 298 | 6 | killed |
| `u301.P1_initargs_refused_without_an_initializer` | `src/cratekit/core/pool.py` | user | 2 file(s) | 294 | 2 | killed |
| `u301.P2_initializer_held_to_the_rule` | `src/cratekit/core/pool.py` | user | 2 file(s) | 294 | 1 | killed |
| `r83-round-2.I1_fold_case` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 2830 | 18 | killed |
| `r83-round-2.I3_configured_compare_exact` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 2830 | 2 | killed |
| `r83-round-2.I4_elsewhere_compare_exact` | `src/cratekit/core/preflight.py` | user | 15 file(s) | 2830 | 1 | killed |
| `u27-round-8-independent.E4_path_missing_reads_ok` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 738 | 4 | killed |
| `u27-round-8-independent.E5_unmounted_reads_foreign` | `src/cratekit/core/preflight.py` | user | 5 file(s) | 738 | 5 | killed |
| `u301.F1_permission_read_as_absent` | `src/cratekit/core/preflight.py` | user | 3 file(s) | 499 | 2 | killed |
| `u173.M20_agent_process` | `src/cratekit/core/processes.py` | user | 1 file(s) | 38 | 1 | killed |
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
| `r705-a.G10_long_wait_under_the_lock` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 1 | killed |
| `r705-a.G11_lock_limit_without_the_interval` | `src/cratekit/core/provider_gate.py` | maintainer | 1 file(s) | 118 | 1 | killed |
| `r705-a.G12_park_forgotten` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 2 | killed |
| `r705-a.G13_process_calls_not_counted` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 20 | killed |
| `r705-a.G1_interval_halved` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 9 | killed |
| `r705-a.G2_last_call_ignored` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 9 | killed |
| `r705-a.G3_retry_after_ignored` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 3 | killed |
| `r705-a.G4_trip_after_off_by_one` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 3 | killed |
| `r705-a.G5_no_trip_on_long_retry_after` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 5 | killed |
| `r705-a.G6_cooldown_not_recorded` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 7 | killed |
| `r705-a.G7_success_keeps_the_run` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 1 | killed |
| `r705-a.G8_call_ignores_the_cooldown` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 2 | killed |
| `r705-a.G9_assert_open_ignores_the_cooldown` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 4 | killed |
| `r759-b.P4_lock_removed_r01` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 1 | 1 | killed |
| `r759.P1_interval_dropped` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 1 | 1 | killed |
| `r759.P5_lock_shared` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 1 | 1 | killed |
| `r759.P6_wait_skipped_stamp_kept` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 1 | 1 | killed |
| `u193.M10_config_not_read` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 523 | 4 | killed |
| `u193.M1_ceiling_check_removed` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 523 | 14 | killed |
| `u193.M2_ceiling_off_by_one` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 523 | 14 | killed |
| `u193.M3_spent_from_process_start` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 523 | 14 | killed |
| `u193.M7_env_parse_accepts_zero` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 523 | 1 | killed |
| `u193.M8_raised_ignored` | `src/cratekit/core/provider_gate.py` | user | 5 file(s) | 523 | 7 | killed |
| `u205.G8_since_keeps_earlier_app_calls` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 23214 | 7 (promoted) | killed |
| `u217.G1_ceiling_says_kept` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 118 | 1 | killed |
| `u278.M10_window_short` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 180 | 5 | killed |
| `u278.M11_window_dropped_on_read` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 180 | 25 | killed |
| `u278.M12_no_over_the_line_in_call` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 180 | 1 | killed |
| `u278.M13_over_the_line_loosened` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 180 | 3 | killed |
| `u278.M14_hour_raise_ignored` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 180 | 2 | killed |
| `u278.M15_hour_not_exported` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 180 | 1 | killed |
| `u278.M16_nested_class_kept` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 180 | 2 | killed |
| `u278.M17_spending_widens` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 290 | 1 | killed |
| `u278.M18_reading_noop` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 275 | 5 | killed |
| `u278.M2_future_minute_not_settled` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 180 | 2 | killed |
| `u278.M4_no_budget_check` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 275 | 17 | killed |
| `u278.M5_budget_off_by_one` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 180 | 16 | killed |
| `u278.M6_count_not_written` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 180 | 27 | killed |
| `u278.M7_identities_merged` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 180 | 2 | killed |
| `u278.M8_no_reserve` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 275 | 25 | killed |
| `u278.M9_continue_names_no_hour` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 250 | 3 | killed |
| `u293.G1_night_line_asked` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 283 | 6 | killed |
| `u293.G2_night_line_off_by_one` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 283 | 5 | killed |
| `u293.G3_total_below_mark` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 283 | 1 | killed |
| `u293.G4_child_reads_no_line` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 283 | 2 | killed |
| `u293.G5_line_held_to_ceiling` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 283 | 5 | killed |
| `u293.G6_nested_lower_line` | `src/cratekit/core/provider_gate.py` | maintainer | 4 file(s) | 283 | 1 | killed |
| `u293.G7_hour_never_raised` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 283 | 1 | killed |
| `u293.G8_line_exported` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 283 | 2 | killed |
| `u301.G1_positive_env_accepts_zero` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 234 | 1 | killed |
| `u301.G2_run_cause_retryable` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 234 | 4 | killed |
| `u301.G3_calls_word_plural` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 180 | 1 | killed |
| `u301.G4_parked_forgets_the_scope` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 234 | 3 | killed |
| `u329.A1_writer_accessor_returns_a_part` | `src/cratekit/core/rb_call_time.py` | user | 5 file(s) | 363 | 197 | killed |
| `r1665-b.C1_w5_composite` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 2 | killed |
| `r1665.W3_no_release_of_the_copy` | `src/cratekit/core/rb_copies.py` | maintainer | 1 file(s) | 14 | 1 | killed |
| `r1665.W6_refused_open_passes` | `src/cratekit/core/rb_copies.py` | user | 7 file(s) | 316 | 2 | killed |
| `r1677.R5_file_set_drops_playlist` | `src/cratekit/core/rb_copies.py` | user | 5 file(s) | 278 | 2 | killed |
| `r372-a.A10_copy_left_behind` | `src/cratekit/core/rb_copies.py` | maintainer | 3 file(s) | 494 | 15 | killed |
| `r372-a.A11_copy_under_a_running_application` | `src/cratekit/core/rb_copies.py` | maintainer | 3 file(s) | 494 | 1 | killed |
| `r372-a.A12_separator_kept` | `src/cratekit/core/rb_copies.py` | user | 3 file(s) | 494 | 7 | killed |
| `r663-a.M1_empty_not_refused_before_open` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 4 | killed |
| `r663-a.M5_failed_listing_returns_empty_set` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M6_listing_opened_with_the_key_always` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-b.M2_every_open_refusal_classified` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 51 | 1 | killed |
| `u329.P2_rb_copies_wrong_family` | `src/cratekit/core/rb_copies.py` | user | 5 file(s) | 164 | 83 | killed |
| `u285.M10_no_offset_edge` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 290 | 15 | killed |
| `u285.M11_value_error_message` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 290 | 2 | killed |
| `u285.M12_xml_bound_dropped` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 290 | 4 | killed |
| `u285.M13_xml_empty_update` | `src/cratekit/core/rb_dates.py` | maintainer | 4 file(s) | 290 | 1 | killed |
| `u285.M14_xml_update_installed` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 290 | 5 | killed |
| `u285.M2_overflow_reads_as_edge` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 290 | 24 | killed |
| `u285.M3_edge_hides_real_overflow` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 290 | 2 | killed |
| `u285.M4_floor_clamp` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 290 | 5 | killed |
| `u285.M5_ceiling_clamp` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 290 | 3 | killed |
| `u285.M6_floor_value` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 290 | 11 | killed |
| `u285.M7_ceiling_value` | `src/cratekit/core/rb_dates.py` | user | 4 file(s) | 290 | 10 | killed |
| `u285.M8_install_once` | `src/cratekit/core/rb_dates.py` | maintainer | 4 file(s) | 290 | 1 | killed |
| `u285.M9_aware_passes` | `src/cratekit/core/rb_dates.py` | maintainer | 4 file(s) | 290 | 1 | killed |
| `u953.M22_edge_reads_only_the_floor` | `src/cratekit/core/rb_dates.py` | user | 1 file(s) | 50 | 7 | killed |
| `r1890.P3_unreserved_slug_in_rb_nodes` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 224 | 1 | killed |
| `r1890.P4_unreadable_slug_in_rb_nodes` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 224 | 1 | killed |
| `u329.P3_rb_nodes_wrong_family` | `src/cratekit/core/rb_nodes.py` | user | 5 file(s) | 1314 | 18 | killed |
| `r1890.P2_system_exit_in_rb_probes` | `src/cratekit/core/rb_probes.py` | user | 2 file(s) | 224 | 1 | killed |
| `u211.W1_writer_falls_back` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 271 | 15 | killed |
| `u211.W3_strict_at_commit` | `src/cratekit/core/rb_probes.py` | user | 2 file(s) | 259 | 2 | killed |
| `u211.W7_writer_unconfirmed_with_nothing_read` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 271 | 2 | killed |
| `u300.S12_settings_read_in_the_part` | `src/cratekit/core/rb_probes.py` | user | 2 file(s) | 257 | 20 | killed |
| `u300.S1_probe_resolved_in_the_part` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 269 | 5 | killed |
| `u329.P4_rb_probes_wrong_family` | `src/cratekit/core/rb_probes.py` | user | 5 file(s) | 326 | 41 | killed |
| `r1890.P1_bare_runtime_error_in_rb_removal` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 224 | 1 | killed |
| `u329.P5_rb_removal_wrong_family` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 307 | 53 | killed |
| `u955.S05_prediction_one_past` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 17 | killed |
| `u955.S06_prediction_ignores_buffer` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 20 | killed |
| `u955.S07_unreadable_count_no_rollback` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 2 | killed |
| `u955.S08_time_form_no_space` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 23 | killed |
| `u955.S09_time_not_utc` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 1 | killed |
| `u955.S14_no_stamp_path_admits_stamps` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 1 | killed |
| `u955.S15_stamp_rule_skipped` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 12 | killed |
| `u955.S16_usn_unmoved_admitted` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 1 | killed |
| `u955.S17_usn_value_unchecked` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 1 | killed |
| `u955.S18_time_value_unchecked` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 1 | killed |
| `u955.S19_time_unmoved_admitted` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 5 | killed |
| `u955.S20_stamp_before_plan_admitted` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 1 | killed |
| `u955.S21_unreadable_plan_time_admitted` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 2 | killed |
| `u955.S22_plan_time_judged_with_no_row_moved` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 1 | killed |
| `u955.S23_read_back_count_unchecked` | `src/cratekit/core/rb_removal.py` | user | 3 file(s) | 337 | 2 | killed |
| `a32.A6_policy_left_behind` | `src/cratekit/core/rb_tables.py` | maintainer | 2 file(s) | 113 | 4 | killed |
| `a32.V4_policy_unrestricted` | `src/cratekit/core/rb_tables.py` | user | 1 file(s) | 60 | 1 | killed |
| `r923.N18_policy_owns_the_fields` | `src/cratekit/core/rb_tables.py` | user | 41 file(s) | 3808 | 1 | killed |
| `r923.N19_default_is_an_analysis_column` | `src/cratekit/core/rb_tables.py` | user | 41 file(s) | 3808 | 35 | killed |
| `u115.F3_file_id_policy_fill_if_empty` | `src/cratekit/core/rb_tables.py` | user | 41 file(s) | 3808 | 3 | killed |
| `u115.F4_binding_limit_coefficient` | `src/cratekit/core/rb_tables.py` | maintainer | 41 file(s) | 3808 | 1 | killed |
| `r1890.P11_process_name_typed_in_the_writer` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 12 | 1 | killed |
| `r239-a.A1_probe_to_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 122 | killed |
| `r239-a.A2_probe_to_false` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 7 | killed |
| `r239-a.A3_probe_removed` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 7 | killed |
| `r239-a.A4_open_default_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 121 | killed |
| `r239-a.A7_needed_always_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 122 | killed |
| `r239-a.A8_needed_always_false` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 8 | killed |
| `r239-a.A9_header_nearby_value` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 122 | killed |
| `r663-a.M10_detail_size_pinned` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 51 | 1 | killed |
| `r663-a.M3_unlistable_read_as_empty` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M4_one_canary_table_not_enough` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M7_message_drops_the_size` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 3 | killed |
| `r663-a.M8_message_names_the_copy` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 5 | killed |
| `r663-a.M9_remedy_restore` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 51 | 3 | killed |
| `u185.G5_reading_at_open` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 75 | 20 | killed |
| `u211.W4_probe_wrapped_at_commit` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 335 | 20 | killed |
| `u211.W5_probe_wrapped_at_open` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 335 | 76 | killed |
| `u267.M10_done_reading_leaks_own` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 111 | 3 | killed |
| `u267.M4_handle_opens_every_time` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 89 | 6 | killed |
| `u267.M5_handle_after_close` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 14 | 1 | killed |
| `u267.M6_release_keeps_rows` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 149 | 1 | killed |
| `u267.M7_release_any_handle` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 14 | 1 | killed |
| `u267.M8_close_closes_nothing` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 111 | 5 | killed |
| `u267.M9_done_reading_closes_shared` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 149 | 60 | killed |
| `u27-round-8-independent.W2_composite_wrong_file` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 23214 | 0 (promoted) | zero |
| `u27-round-8-independent.W3_canary_no_name_the_database` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 23214 | 0 (promoted) | zero |
| `u27-round-8-independent.W5_canary_message_no_path` | `src/cratekit/core/rb_writer.py` | user | 11 file(s) | 23214 | 0 (promoted) | zero |
| `u285.M1_seam_installs` | `src/cratekit/core/rb_writer.py` | user | 4 file(s) | 290 | 6 | killed |
| `u59.M9_column_repointed` | `src/cratekit/core/rb_writer.py` | user | 22 file(s) | 2744 | 176 | killed |
| `u953.M5_writable_library_asks_only_the_state_directory` | `src/cratekit/core/reconcile.py` | user | 2 file(s) | 271 | 10 | killed |
| `r1665.R1_log_not_restored` | `src/cratekit/core/restore.py` | user | 7 file(s) | 316 | 4 | killed |
| `u27-restore-cli-independent.X6_the_rekordbox_guard_itself_is_neutered` | `src/cratekit/core/restore.py` | user | 2 file(s) | 253 | 1 | killed |
| `u95-a.A1_never_rerooted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 7 | killed |
| `u95-a.A2_library_sessions_rerooted_too` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 2 | killed |
| `u95-a.A3_database_not_carried` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 4 | killed |
| `u95-a.A4_outside_database_refusal_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 1 | killed |
| `u95-a.A5_capture_path_not_rebased` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 2 | killed |
| `u95-a.A6_manifest_not_rebased_in_plan` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 3 | killed |
| `u95-a.A7_manifest_not_rebased_in_preflight` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 1 | killed |
| `u95-a.A8_run_not_rooted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 1 | killed |
| `u95-b.B2_manifest_database_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 2 | killed |
| `u95-b.B3_sources_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 3 | killed |
| `u95-b.B4_captured_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 2 | killed |
| `u95-b.B5_not_idempotent` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 506 | 1 | killed |
| `u95-b.B6_recorded_path_not_normalised` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 506 | 1 | killed |
| `u95-b.B8_outside_path_moved_anyway` | `src/cratekit/core/restore.py` | maintainer | 3 file(s) | 506 | 2 | killed |
| `u95-b1.B1_manifest_root_not_moved` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 1 | killed |
| `u95-c.C1_plan_side_guard_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 1 | killed |
| `u95-c.C2_run_side_guard_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 7 | killed |
| `u95-c.C3_step_authorisation_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 2 | killed |
| `u95-c.C4_restorable_membership_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 1 | killed |
| `u95-c.C5_staging_authorisation_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 2 | killed |
| `u95-c.C6_staging_store_rule_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 3 | killed |
| `u95-c.C7_staging_store_itself_admitted` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 1 | killed |
| `u95-c.C8_plan_root_assertion_removed` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 1 | killed |
| `u95-c.S1_authorises_everything` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 7 | killed |
| `u95-c.S2_issued_terms_not_compared` | `src/cratekit/core/restore.py` | user | 3 file(s) | 506 | 1 | killed |
| `u953.M13_spendable_capture_skips_the_verdict` | `src/cratekit/core/restore.py` | user | 2 file(s) | 253 | 2 | killed |
| `r1890.P13_convergence_fallback_filter_in_restore_perform` | `src/cratekit/core/restore_perform.py` | maintainer | 1 file(s) | 159 | 1 | killed |
| `u300.S19_replace_file_local` | `src/cratekit/core/restore_perform.py` | maintainer | 2 file(s) | 253 | 2 | killed |
| `u300.S20_stage_aside_local` | `src/cratekit/core/restore_perform.py` | maintainer | 2 file(s) | 253 | 1 | killed |
| `r592-a.A1_occupancy_guard_removed` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `r592-a.A2_database_dropped_from_fileset` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `r592-a.A3_companions_dropped_from_fileset` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 2 | killed |
| `r592-a.A4_fileset_not_rebased` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 4 | killed |
| `r592-a.A5_replacing_existing_inverted` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 8 | killed |
| `r592-a.A6_old_suffix_rule_restored` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 2 | killed |
| `r592-a.A7_companion_suffix_wrong` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 2 | killed |
| `r592-a.A8_sample_stub_check_beside` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 2 | killed |

## Zero rows and what they owe

- `u241.M01_worker_takes_the_interrupt` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.W2_composite_wrong_file` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.W3_canary_no_name_the_database` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.W5_canary_message_no_path` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u41-naming-independent.E1_budget_bypassed`

The fitted stem is discarded and the deduped one is returned, so nothing is ever shortened to the path ceiling

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `E1_budget_bypassed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1585 against a baseline of 1585
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_an_absent_field_contributes_zero_bytes_including_its_separator`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming_apply_cli.py::test_a_composed_body_over_the_ceiling_is_fitted_not_left_as_a_number`
  - `tests/test_naming_apply_cli.py::test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt`

Old text:

```
    return replace(spec, stem=fitted)

```

New text:

```
    return replace(spec, stem=deduped)

```

### `u41-naming-independent.E3_budget_min_becomes_max`

The two ceilings are combined with max rather than min, so the looser one wins

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `E3_budget_min_becomes_max`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1585 against a baseline of 1585
- Kills: 8 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming_apply_cli.py::test_a_name_over_the_byte_ceiling_is_truncated_not_rebuilt`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_a_character_count_would_have_passed_this_and_the_byte_count_does_not`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_an_unsatisfiable_budget_raises_rather_than_emitting`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_multibyte_never_splits_a_codepoint`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_over_budget_truncates_and_the_assembled_path_fits`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_padding_a_single_digit_key_cannot_push_a_fitted_name_over`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_two_budgets_in_one_process_give_two_answers`

Old text:

```
    max_stem = min(

```

New text:

```
    max_stem = max(

```

### `u41-naming-independent.E4_path_separator_byte_dropped`

The path separator's byte is no longer counted against the path budget

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `E4_path_separator_byte_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1585 against a baseline of 1585
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_over_budget_truncates_and_the_assembled_path_fits`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_padding_a_single_digit_key_cannot_push_a_fitted_name_over`

Old text:

```
        + 1  # the path separator

```

New text:

```
        + 0  # the path separator

```

### `u41-naming-independent.E5_truncation_tail_not_reserved`

The disambiguating tail's bytes are not reserved, so the assembled name overshoots the ceiling by its length

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `E5_truncation_tail_not_reserved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1585 against a baseline of 1585
- Kills: 5 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_a_character_count_would_have_passed_this_and_the_byte_count_does_not`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_multibyte_never_splits_a_codepoint`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_over_budget_truncates_and_the_assembled_path_fits`
  - `tests/test_naming_budget.py::TestFitStemToBudget::test_padding_a_single_digit_key_cannot_push_a_fitted_name_over`

Old text:

```
    avail = max_stem - len(tail)

```

New text:

```
    avail = max_stem

```

### `u41-naming-independent.F3_body_tag_preference_flipped`

The tag body prefers the filename's stem over the title, which is A2 reproduced inside the engine

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `F3_body_tag_preference_flipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1585 against a baseline of 1585
- Kills: 31 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[marker-in-body-marks-nothing]`
  - `tests/test_naming.py::TestRender::test_render[lossless-carries-no-marker]`
  - `tests/test_naming.py::TestRender::test_render[lossy-marks-right-after-the-head]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-optional-bpm]`
  - ... and 16 more, see the JSON sidecar

Old text:

```
    body_tag = spec.title if spec.title else spec.stem

```

New text:

```
    body_tag = spec.stem if spec.stem else spec.title

```

### `u41-naming-independent.F4_body_tag_fallback_dropped`

The tag body has no fallback at all, so a spec with no title renders None into the tag

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `F4_body_tag_fallback_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1585 against a baseline of 1585
- Kills: 52 (killed)
- Killed:
  - `tests/test_naming.py::TestAnalysisOff::test_a_lossy_file_is_still_marked_with_analysis_off`
  - `tests/test_naming.py::TestAnalysisOff::test_a_tempo_without_a_key_renders_no_head_at_all`
  - `tests/test_naming.py::TestAnalysisOff::test_absent_fields_are_omitted_not_rendered_empty`
  - `tests/test_naming.py::TestAnalysisOff::test_it_round_trips_through_the_parser`
  - `tests/test_naming.py::TestAnalysisOff::test_no_key_and_no_tempo_renders_the_body_alone`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_budget_head_equals_the_written_head_since_the_pad_moved_in`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_same_input_twice_yields_the_same_path`
  - `tests/test_naming.py::TestMarkerCoupling::test_a_lossless_file_renders_fine_under_the_same_template`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-8A-124-False]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-8A-124-True]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-8A-None-False]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-8A-None-True]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-None-None-False]`
  - `tests/test_naming.py::TestMarkerCoupling::test_all_three_surfaces_or_none[None-None-None-True]`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    body_tag = spec.title if spec.title else spec.stem

```

New text:

```
    body_tag = spec.title

```

### `u41-naming-independent.F6_filename_prefers_the_title_body`

R-168 reproduced one file over: the FILENAME is rendered from the title body when there is one, inside the engine rather than in the shell

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `F6_filename_prefers_the_title_body`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1585 against a baseline of 1585
- Kills: 51 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[marker-in-body-marks-nothing]`
  - `tests/test_naming.py::TestRender::test_render[lossless-carries-no-marker]`
  - `tests/test_naming.py::TestRender::test_render[lossy-marks-right-after-the-head]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-False-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-124-Title Tag-True-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-False-optional-bpm]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-custom]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-default]`
  - `tests/test_naming.py::test_every_rendered_name_strips_back_to_its_body[8A-None-Title Tag-True-optional-bpm]`
  - ... and 36 more, see the JSON sidecar

Old text:

```
        filename=head + spec.stem + spec.suffix,

```

New text:

```
        filename=head + (spec.title or spec.stem) + spec.suffix,

```

### `u41-naming-independent.F7_library_name_split_from_the_tag`

The library name is derived from the stem rather than from the rendered title tag, so the marker can go missing from one surface only

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `F7_library_name_split_from_the_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1585 against a baseline of 1585
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[marker-in-body-marks-nothing]`
  - `tests/test_naming.py::TestRender::test_render[lossless-carries-no-marker]`
  - `tests/test_naming.py::TestRender::test_render[lossy-marks-right-after-the-head]`

Old text:

```
        library_name=title_tag,

```

New text:

```
        library_name=head + spec.stem,

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
  - `tests/test_provider_gate_night.py::test_a_dead_firings_mark_is_charged_in_full_and_folded_on_a_refusal`
  - `tests/test_provider_gate_night.py::test_an_earlier_nights_unclosed_mark_at_the_new_night[a-dead-firings-mark-from-an-earlier-night-is-charged-to-tonight]`
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
  - `tests/test_provider_gate_night.py::test_a_later_firing_is_charged_what_its_own_night_spent[a-second-firing-of-the-night-has-only-what-is-left]`
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

### `u293.L4_noon_to_noon`

night_of: a night runs midnight to midnight, so a three in the morning firing starts a new night

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L4_noon_to_noon`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_firing_is_charged_before_its_first_call_and_closed_after`
  - `tests/test_provider_gate_night.py::test_a_later_firing_is_charged_what_its_own_night_spent[the-next-night-starts-from-nothing]`
  - `tests/test_provider_gate_night.py::test_a_night_runs_noon_to_noon_local_time`

Old text:

```
    return (local - timedelta(hours=NOON)).date().isoformat()
```

New text:

```
    return (local - timedelta(hours=0)).date().isoformat()
```

### `u293.L6_unreadable_gate_refuses`

_total: a gate file that cannot be read is a total of nothing

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L6_unreadable_gate_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_total_the_night_cannot_trust_refuses_saying_why[a-gate-that-cannot-be-read-refuses-the-night]`

Old text:

```
    if spend is None:
        raise _unreadable("the provider gate's state file could not be read", path)
```

New text:

```
    if spend is None:
        return 0
```

### `u12-independent-round-6.C2_reserve_halved`

Halve the absolute memory reserve coefficient, two gibibytes to one. A reserve that can be halved with a green suite is a reserve nothing pins.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C2_reserve_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_capped_service_on_a_huge_host_is_sized_by_the_service`
  - `tests/test_pool_sizing.py::test_the_absolute_reserve_is_two_gibibytes_of_the_reading_that_was_never_ours`

Old text:

```
DEFAULT_MEMORY_RESERVE_BYTES = 2 * 1024**3
```

New text:

```
DEFAULT_MEMORY_RESERVE_BYTES = 1 * 1024**3
```

### `u12-independent-round-6.C4_darwin_headroom`

Raise the darwin headroom share from half to three quarters, which is the value the measured inactive-queue split says is too optimistic.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C4_darwin_headroom`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 4 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_each_headroom_share_is_pinned_by_the_pool_it_produces[darwin-half-as-measured]`
  - `tests/test_pool_sizing.py::test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse[darwin-50]`
  - `tests/test_pool_sizing.py::test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse[linux-75]`
  - `tests/test_pool_sizing.py::test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse[win32-75]`

Old text:

```
DARWIN_HEADROOM_PERCENT = 50
```

New text:

```
DARWIN_HEADROOM_PERCENT = 75
```

### `u12-independent-round-6.C5_swap_threshold`

Raise the swap pressure threshold from one gibibyte to four, so the machine the documented kill happened on is no longer refused a pool.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C5_swap_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 4 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_gated_plan_still_reports_the_reading_it_was_gated_despite`
  - `tests/test_pool_sizing.py::test_the_machine_the_kill_happened_on_gets_no_pool_under_the_shipped_rule`
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[swap-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_swap_threshold_is_a_gibibyte_and_the_gibibyte_is_load_bearing[a-full-gibibyte]`

Old text:

```
DEFAULT_SWAP_PRESSURE_BYTES = 1 * 1024**3
```

New text:

```
DEFAULT_SWAP_PRESSURE_BYTES = 4 * 1024**3
```

### `u12-independent-round-6.C6_used_percent_ceiling`

Raise the used-percent ceiling from eighty five to ninety five.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C6_used_percent_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[percent-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_used_percent_ceiling_is_eighty_five_and_the_number_is_load_bearing[at-the-line]`

Old text:

```
DEFAULT_USED_PERCENT_CEILING = 85
```

New text:

```
DEFAULT_USED_PERCENT_CEILING = 95
```

### `u12-independent-round-6.C7_max_tasks_per_child`

Two and a half times the recycle budget, one hundred to two hundred fifty, so a child holds an allocator two and a half times longer before retiring.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C7_max_tasks_per_child`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 3 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_recycling_is_on_by_default_for_any_pool_wider_than_one`
  - `tests/test_pool_sizing.py::test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly[a-ten-thousand-track-folder]`
  - `tests/test_pool_sizing.py::test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly[an-ordinary-folder]`

Old text:

```
DEFAULT_MAX_TASKS_PER_CHILD = 100
```

New text:

```
DEFAULT_MAX_TASKS_PER_CHILD = 250
```

### `u12-independent-round-6.C8_probe_deadline`

Cut the probe deadline from two minutes to forty five seconds, below the twice-the-reference floor the docstring claims the suite states.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C8_probe_deadline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_probe_deadline_the_module_ships_outlasts_the_load_it_waits_for`

Old text:

```
DEFAULT_PROBE_TIMEOUT_SECONDS = 120.0
```

New text:

```
DEFAULT_PROBE_TIMEOUT_SECONDS = 45.0
```

### `u12-independent-round-6.C9_reap_budget`

Halve the reaping budget, one second to half a second, which the round six docstring names as the value that makes the terminate rung a race.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C9_reap_budget`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_reaping_budget_is_a_band_around_what_a_release_costs`

Old text:

```
_PROBE_REAP_SECONDS = 1.0
```

New text:

```
_PROBE_REAP_SECONDS = 0.5
```

### `u12-independent-round-6.G1_dotdot_not_refused`

Drop the refusal of a cgroup path containing dot dot, so a climbing path is rewritten into a real sibling cgroup and its tighter cap binds.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G1_dotdot_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_climb_that_lands_on_a_real_cgroup_inside_the_mount_is_refused_too[a-climb-in-the-middle]`

Old text:

```
    if ".." in fields:
        candidates = [mount]
    else:

```

New text:

```
    if False:
        candidates = [mount]
    else:

```

### `u12-independent-round-6.G2_containment_dropped`

Stop checking that a resolved level is still inside the mount, so a symlink out of the mount is read as a level of this process's cgroup.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G2_containment_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_component_that_symlinks_out_of_the_mount_is_not_read`
  - `tests/test_pool_sizing.py::test_a_limit_file_that_symlinks_out_of_the_mount_is_not_read`

Old text:

```
    if resolved is None or not resolved.is_relative_to(anchor):
        return None

```

New text:

```
    if resolved is None:
        return None

```

### `u12-independent-round-6.G3_headroom_can_go_negative`

Report a negative headroom for a cgroup already over its cap.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G3_headroom_can_go_negative`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_cgroup_cap_reports_what_is_left_inside_it[over-the-cap-is-zero-never-negative]`

Old text:

```
    return max(0, limit - used)

```

New text:

```
    return limit - used

```

### `u12-independent-round-6.G4_controller_substring_match`

Match the memory controller by substring, so a controller named memoryfoo sends the walk to an unrelated cgroup.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G4_controller_substring_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_controller_field_that_merely_contains_the_word_memory_is_not_it[a-name-that-contains-it]`
  - `tests/test_pool_sizing.py::test_a_controller_field_that_merely_contains_the_word_memory_is_not_it[a-name-that-starts-with-it]`

Old text:

```
        elif "memory" in controllers.split(","):

```

New text:

```
        elif "memory" in controllers:

```

### `u12-independent-round-6.G5_loosest_cap_wins`

Take the loosest cap on the chain rather than the tightest, so a generous unit inside a tight slice reports the unit's number.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G5_loosest_cap_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_tightest_cap_on_the_chain_is_the_one_that_binds`

Old text:

```
    return min(found) if found else None

```

New text:

```
    return max(found) if found else None

```

### `u12-independent-round-6.G6_cgroup_cap_ignored`

Ignore the cgroup cap entirely and return the host reading, which is the defect that sizes a container by its host.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G6_cgroup_cap_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 3 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_capped_service_on_a_huge_host_is_sized_by_the_service`
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_large_container_on_a_larger_host_is_still_sized_by_the_container`

Old text:

```
    return reading if capped is None else min(reading, capped)

```

New text:

```
    return reading

```

### `u12-independent-round-6.G7_valueerror_escapes_the_reader`

Narrow the kernel-file reader back to OSError, so undecodable bytes and an embedded null byte raise out of a function that promises a number.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G7_valueerror_escapes_the_reader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_kernel_file_that_is_not_readable_as_text_is_an_absent_reading[not-text-at-all]`

Old text:

```
    except (OSError, ValueError):
        return None

```

New text:

```
    except OSError:
        return None

```

### `u12-independent-round-6.M1_measurement_below_the_floor`

Return the measurement even when it is below the declared floor, so the floor becomes a fallback rather than a floor.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M1_measurement_below_the_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_probe_reports_its_measure_and_never_below_the_floor[never-below-the-floor]`

Old text:

```
    return max(measured, floor_bytes)

```

New text:

```
    return measured

```

### `u12-independent-round-6.M2_nonsense_measurement_accepted`

Accept a boolean, a float or a zero from the probe as a byte count.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M2_nonsense_measurement_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_that_answers_with_nonsense_returns_the_floor[none]`
  - `tests/test_pool_sizing.py::test_a_probe_that_answers_with_nonsense_returns_the_floor[text]`

Old text:

```
    if not isinstance(measured, int) or isinstance(measured, bool) or measured < 1:
        return floor_bytes

```

New text:

```
(empty)
```

### `u12-independent-round-6.M3_zero_deadline_allowed`

Allow a probe deadline of zero or less, which is a probe that can never answer reporting the floor as though it had measured.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M3_zero_deadline_allowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_asked_for_the_impossible_refuses_rather_than_reporting_the_floor[no-time-to-answer]`

Old text:

```
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must leave the probe some time to answer")

```

New text:

```
(empty)
```

### `u12-independent-round-6.M4_model_freed_before_the_reading`

Free the loaded object before the resident set is read, the allocator retention defect the probe was rewritten to fix.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M4_model_freed_before_the_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_real_probe_measures_a_freshly_spawned_child`

Old text:

```
        model = loader()
        try:
            measured = resident_bytes()
        finally:

```

New text:

```
        loader()
        try:
            measured = resident_bytes()
        finally:

```

### `u12-independent-round-6.M5_terminate_rung_removed`

Remove the terminate rung alone, so every abandoned probe child meets an unconditional kill with no chance to unwind.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M5_terminate_rung_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 3 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_child_that_can_unwind_is_asked_to_before_it_is_killed`
  - `tests/test_pool_sizing.py::test_a_probe_child_that_refuses_to_unwind_meets_the_kill_backstop`
  - `tests/test_pool_sizing.py::test_the_release_the_fixture_declares_is_what_the_ladder_was_timed_paying`

Old text:

```
    if worker.is_alive():
        worker.terminate()
        worker.join(_PROBE_REAP_SECONDS)

```

New text:

```
(empty)
```

### `u12-independent-round-6.M6_kill_rung_removed`

Remove the kill backstop alone, so a child that ignores its terminate is left running and still allocating.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M6_kill_rung_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_child_that_refuses_to_unwind_meets_the_kill_backstop`

Old text:

```
    if worker.is_alive():
        worker.kill()
        worker.join(_PROBE_REAP_SECONDS)

```

New text:

```
(empty)
```

### `u12-independent-round-6.M7_parent_keeps_the_write_end`

Leave the parent's copy of the pipe write end open, so a child that dies without answering is indistinguishable from a slow one.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M7_parent_keeps_the_write_end`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_that_gets_no_answer_lands_on_the_floor_in_time[a-child-that-dies-without-answering]`

Old text:

```
    # exactly like a slow one until the timeout expired.
    writer.close()

```

New text:

```
    # exactly like a slow one until the timeout expired.

```

### `u12-independent-round-6.M8_no_reap_after_the_probe`

Remove the reap from the probe's finally, so an abandoned child keeps its allocation on a machine already declared tight.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M8_no_reap_after_the_probe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_that_gave_up_leaves_no_child_still_allocating`

Old text:

```
        reader.close()
        _reap(worker)

```

New text:

```
        reader.close()

```

### `u12-independent-round-6.P10_recycle_reported_for_in_process`

Report a recycle count on a plan that runs in the calling process and has no child to retire.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P10_recycle_reported_for_in_process`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_in_process_plan_runs_no_generations_at_all`
  - `tests/test_pool_sizing.py::test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process`

Old text:

```
        max_tasks_per_child=None if workers == 1 else max_tasks_per_child,

```

New text:

```
        max_tasks_per_child=max_tasks_per_child,

```

### `u12-independent-round-6.P12_unreadable_falls_back_to_ceiling`

Make the unreadable-memory fallback the declared ceiling rather than one worker, which is the exact fallback the brief forbids.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P12_unreadable_falls_back_to_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 8 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_memory_read_failure_falls_back_to_one_worker_rather_than_raising`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[bool]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[float]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[negative]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[none]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[text]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[very-negative]`
  - `tests/test_pool_sizing.py::test_the_fallback_is_never_the_ceiling_or_the_item_count`

Old text:

```
        return PoolPlan(
            workers=1,
            items=items,
            bound=Bound.MEMORY_UNREADABLE,

```

New text:

```
        return PoolPlan(
            workers=ceiling,
            items=items,
            bound=Bound.MEMORY_UNREADABLE,

```

### `u12-independent-round-6.P1_reserve_not_applied`

Drop the absolute reserve from the budget entirely, so the whole reading is claimable before the percent scales it.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P1_reserve_not_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 13 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_capped_service_on_a_huge_host_is_sized_by_the_service`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is`
  - `tests/test_pool_sizing.py::test_a_measured_worker_size_flows_into_the_plan_it_was_taken_for`
  - `tests/test_pool_sizing.py::test_sixteen_gigabytes_is_bound_by_the_headroom_once_the_ceiling_is_raised`
  - `tests/test_pool_sizing.py::test_the_absolute_reserve_is_two_gibibytes_of_the_reading_that_was_never_ours`
  - `tests/test_pool_sizing.py::test_the_core_count_does_not_change_the_computed_cap`
  - `tests/test_pool_sizing.py::test_the_hard_ceiling_and_the_headroom_agree_at_the_point_they_cross`
  - `tests/test_pool_sizing.py::test_the_platform_limit_bounds_the_pool_where_the_platform_has_one[no-limit-contributes-nothing]`
  - `tests/test_pool_sizing.py::test_the_reserve_then_the_headroom_come_off_the_bytes_before_the_division[the-reserve-comes-off-before-the-share]`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[2]`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[3]`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[4]`
  - `tests/test_pool_sizing.py::test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process`

Old text:

```
    budget = max(0, available - reserve_bytes)

```

New text:

```
    budget = max(0, available)

```

### `u12-independent-round-6.P2_order_reversed`

Reverse the last two steps: divide into workers first and then scale the count, which the docstring says differs only at the boundaries.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P2_order_reversed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 5 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is`
  - `tests/test_pool_sizing.py::test_the_hard_ceiling_and_the_headroom_agree_at_the_point_they_cross`
  - `tests/test_pool_sizing.py::test_the_reserve_then_the_headroom_come_off_the_bytes_before_the_division[the-headroom-scales-the-bytes-not-the-count]`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[2]`
  - `tests/test_pool_sizing.py::test_the_worker_count_flips_exactly_at_the_affordable_boundary[4]`

Old text:

```
    affordable = budget * headroom_percent // 100 // worker_bytes

```

New text:

```
    affordable = budget // worker_bytes * headroom_percent // 100

```

### `u12-independent-round-6.P3_budget_can_go_negative`

Remove the floor at zero so a reading smaller than the reserve produces a negative budget and a negative affordable count.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P3_budget_can_go_negative`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_reading_smaller_than_the_reserve_affords_nothing_rather_than_going_negative`

Old text:

```
    budget = max(0, available - reserve_bytes)

```

New text:

```
    budget = available - reserve_bytes

```

### `u12-independent-round-6.P4_no_floor_of_one_worker`

Remove the floor of one worker, so a machine that affords none plans a pool of zero.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P4_no_floor_of_one_worker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 11 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is`
  - `tests/test_pool_sizing.py::test_a_plan_of_one_worker_explains_itself_as_in_process`
  - `tests/test_pool_sizing.py::test_a_plan_of_one_worker_runs_the_work_in_this_process`
  - `tests/test_pool_sizing.py::test_a_reading_smaller_than_the_reserve_affords_nothing_rather_than_going_negative`
  - `tests/test_pool_sizing.py::test_an_in_process_plan_refuses_to_hand_back_pool_arguments`
  - `tests/test_pool_sizing.py::test_an_in_process_plan_runs_no_generations_at_all`
  - `tests/test_pool_sizing.py::test_the_item_count_bounds_the_pool[no-work-is-one-not-zero]`
  - `tests/test_pool_sizing.py::test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process`
  - `tests/test_pool_sizing.py::test_what_no_child_could_receive_is_refused_before_anything_runs[a-function-no-child-could-receive]`
  - `tests/test_pool_sizing.py::test_what_no_child_could_receive_is_refused_before_anything_runs[an-initializer-argument-no-child-could-receive]`

Old text:

```
    workers = max(1, smallest)

```

New text:

```
    workers = smallest

```

### `u12-independent-round-6.P5_tie_goes_to_the_ceiling`

Put the ceiling ahead of available memory in the precedence list, so a tie is reported as the ceiling rather than as memory.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P5_tie_goes_to_the_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_hard_ceiling_and_the_headroom_agree_at_the_point_they_cross`

Old text:

```
        (Bound.AVAILABLE_MEMORY, affordable),
        (Bound.CEILING, ceiling),

```

New text:

```
        (Bound.CEILING, ceiling),
        (Bound.AVAILABLE_MEMORY, affordable),

```

### `u12-independent-round-6.P6_no_insufficient_memory_bound`

Remove the reclassification that tells a machine affording exactly one from a machine affording none.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `P6_no_insufficient_memory_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 5 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_container_capped_below_its_host_is_sized_by_the_cap`
  - `tests/test_pool_sizing.py::test_a_machine_that_affords_none_is_not_the_same_machine_and_does_not_say_it_is`
  - `tests/test_pool_sizing.py::test_a_reading_smaller_than_the_reserve_affords_nothing_rather_than_going_negative`
  - `tests/test_pool_sizing.py::test_the_absolute_reserve_is_two_gibibytes_of_the_reading_that_was_never_ours`
  - `tests/test_pool_sizing.py::test_two_gigabytes_against_a_one_gigabyte_worker_runs_in_process`

Old text:

```
        bound = Bound.INSUFFICIENT_MEMORY

```

New text:

```
        bound = Bound.AVAILABLE_MEMORY

```

### `u12-independent-round-6.R1_available_type_check`

Accept a non-integer or negative available reading as a real reading.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `R1_available_type_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 5 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[bool]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[float]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[negative]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[text]`
  - `tests/test_pool_sizing.py::test_a_reading_that_is_not_a_byte_count_is_treated_as_unreadable[very-negative]`

Old text:

```
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        return None
    return value

```

New text:

```
    return value

```

### `u12-independent-round-6.R2_available_never_raises`

Remove the catch around the injected available reader, so a reader that raises raises out of plan_pool.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `R2_available_never_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_memory_read_failure_falls_back_to_one_worker_rather_than_raising`
  - `tests/test_pool_sizing.py::test_the_fallback_is_never_the_ceiling_or_the_item_count`

Old text:

```
    try:
        value = reader()
    except Exception:
        return None
    if not isinstance(value, int)
```

New text:

```
    value = reader()
    if not isinstance(value, int)
```

### `u12-independent-round-6.R3_pressure_percent_range`

Accept a used-percent outside zero to one hundred as a real reading.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `R3_pressure_percent_range`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_unreadable_pressure_reading_does_not_collapse_the_pool[impossible-percent]`

Old text:

```
    if not 0 <= used <= 100:
        return None
    return value

```

New text:

```
    return value

```

### `u12-independent-round-6.R4_pressure_type_check`

Accept anything at all as a pressure reading, not only a Pressure.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `R4_pressure_type_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_unreadable_pressure_reading_does_not_collapse_the_pool[none]`
  - `tests/test_pool_sizing.py::test_an_unreadable_pressure_reading_does_not_collapse_the_pool[text]`

Old text:

```
    if not isinstance(value, Pressure):
        return None

```

New text:

```
(empty)
```

### `u12-independent-round-6.X1_pool_of_one_built`

Let executor_arguments build a pool for a plan of one worker instead of refusing at the seam.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X1_pool_of_one_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_in_process_plan_refuses_to_hand_back_pool_arguments`

Old text:

```
    if plan.in_process:
        raise ValueError(
            "a plan of one worker runs in the calling process; there is no pool "
            "to build. Branch on plan.in_process before asking for a pool."
        )

```

New text:

```
(empty)
```

### `u12-independent-round-6.X3_generation_boundary_removed`

Give one executor all of the work rather than one generation of it, which is the deadlock the generation boundary exists to prevent.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X3_generation_boundary_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_no_child_survives_a_generation_boundary_and_every_one_reloads_its_model`

Old text:

```
    generation = plan.tasks_per_generation or len(ordered) or 1

```

New text:

```
    generation = len(ordered) or 1

```

### `u12-independent-round-6.X4_initargs_not_refused`

Stop holding initializer arguments to the picklability rule, so the same call means two things on two machines again.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X4_initargs_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_what_no_child_could_receive_is_refused_before_anything_runs[an-initializer-argument-no-child-could-receive]`

Old text:

```
    for position, argument in enumerate(initargs):
        _refuse_what_no_child_could_receive(argument, f"initializer argument {position}")

```

New text:

```
(empty)
```

### `u12-independent-round-6.X5_in_process_path_removed`

Build a pool even for a plan of one worker, which is the brief's third requirement inverted.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X5_in_process_path_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_plan_of_one_worker_runs_the_work_in_this_process`

Old text:

```
    if plan.in_process:
        if initializer is not None:
            initializer(*initargs)
        return [function(item) for item in ordered]

```

New text:

```
(empty)
```

### `u12-independent-round-6.X7_generation_size_drops_the_width`

Size a generation by one child's budget rather than by the whole set of children, so the executor is rebuilt workers times too often.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `X7_generation_size_drops_the_width`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 268 against a baseline of 268
- Kills: 9 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_child_that_dies_mid_generation_ends_the_run_rather_than_hanging`
  - `tests/test_pool_sizing.py::test_a_plan_carries_the_item_count_it_was_decided_for`
  - `tests/test_pool_sizing.py::test_a_plan_says_how_many_generations_of_children_its_work_takes[16-2]`
  - `tests/test_pool_sizing.py::test_a_plan_says_how_many_generations_of_children_its_work_takes[17-3]`
  - `tests/test_pool_sizing.py::test_a_plan_says_how_many_generations_of_children_its_work_takes[8-1]`
  - `tests/test_pool_sizing.py::test_a_plan_says_how_many_generations_of_children_its_work_takes[9-2]`
  - `tests/test_pool_sizing.py::test_no_child_survives_a_generation_boundary_and_every_one_reloads_its_model`
  - `tests/test_pool_sizing.py::test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly[a-ten-thousand-track-folder]`
  - `tests/test_pool_sizing.py::test_the_recycle_budget_retires_a_child_occasionally_rather_than_constantly[an-ordinary-folder]`

Old text:

```
        return self.workers * self.max_tasks_per_child

```

New text:

```
        return self.max_tasks_per_child

```

### `u241.M01_worker_takes_the_interrupt`

stream worker: no longer ignore the terminal's interrupt, so Ctrl-C kills a worker mid item

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M01_worker_takes_the_interrupt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    _leave_when_the_parent_does()

```

New text:

```
    _leave_when_the_parent_does()

```

### `u241.M02_worker_outlives_its_parent`

stream worker: do not watch the parent, so a killed driver leaves its workers holding their memory

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M02_worker_outlives_its_parent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_stream.py::test_workers_leave_when_their_parent_is_killed_outright`

Old text:

```
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    _leave_when_the_parent_does()

```

New text:

```
    signal.signal(signal.SIGINT, signal.SIG_IGN)

```

### `u241.M03_close_waits_for_unread_work`

WorkStream._stop: do not end the workers, so a close waits for every item nobody will read

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M03_close_waits_for_unread_work`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_stream.py::test_a_close_ends_the_workers_without_waiting_for_work_nobody_will_read`

Old text:

```
        _end_workers(executor)
        executor.shutdown(wait=True, cancel_futures=True)

```

New text:

```
        executor.shutdown(wait=True, cancel_futures=True)

```

### `u241.M07_used_percent_gate_is_strict`

_gates_refusing: the used percent gate refuses only above its limit, not at it

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M07_used_percent_gate_is_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`, `tests/test_pool_sizing.py`
- Collected: 294 against a baseline of 294
- Kills: 3 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_pressure_gate_bites_at_its_two_lines_and_nowhere_else[percent-at-the-line]`
  - `tests/test_pool_sizing.py::test_the_used_percent_ceiling_is_eighty_five_and_the_number_is_load_bearing[at-the-line]`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_both_gates_names_both_swap_first`

Old text:

```
    if pressure.used_percent >= used_percent_ceiling:
        refused.append(

```

New text:

```
    if pressure.used_percent > used_percent_ceiling:
        refused.append(

```

### `u241.M08_plan_forgets_which_gate`

plan_pool: a plan refused by pressure no longer carries which gate refused it

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M08_plan_forgets_which_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`, `tests/test_analysis_ahead.py`
- Collected: 298 against a baseline of 298
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_machine_deep_in_swap_runs_one_worker_and_names_the_swap_gate`
  - `tests/test_analysis_ahead.py::test_a_machine_using_most_of_its_memory_names_the_used_percent_gate`
  - `tests/test_analysis_ahead.py::test_a_run_that_fails_part_way_says_its_pool_on_the_refusal_and_matches_the_serial_run`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_both_gates_names_both_swap_first`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_swap_names_the_gate_the_reading_and_the_limit`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_the_used_percent_names_that_gate`

Old text:

```
            ceiling=ceiling,
            refused_by=refused,

```

New text:

```
            ceiling=ceiling,

```

### `u301.P1_initargs_refused_without_an_initializer`

_refuse_unsendable: check the initializer's arguments only when there is an initializer, so map_workers and WorkStream pass a lambda argument on an in process plan

- File: `src/cratekit/core/pool.py`
- Source: `u301.json`, row `P1_initargs_refused_without_an_initializer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`, `tests/test_pool_stream.py`
- Collected: 294 against a baseline of 294
- Kills: 2 (killed)
- Killed:
  - `tests/test_pool_stream.py::test_an_unsendable_function_is_refused_at_construction_on_both_paths[in-process]`
  - `tests/test_pool_stream.py::test_an_unsendable_function_is_refused_at_construction_on_both_paths[pooled]`

Old text:

```
    for position, argument in enumerate(initargs):
        _refuse_what_no_child_could_receive(argument, f"initializer argument {position}")

```

New text:

```
    for position, argument in enumerate(initargs if initializer is not None else ()):
        _refuse_what_no_child_could_receive(argument, f"initializer argument {position}")

```

### `u301.P2_initializer_held_to_the_rule`

_refuse_unsendable: never check the initializer, so an unpicklable one passes an in process plan and fails a pooled one

- File: `src/cratekit/core/pool.py`
- Source: `u301.json`, row `P2_initializer_held_to_the_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`, `tests/test_pool_stream.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_an_initializer_no_child_could_receive_is_refused_on_the_same_terms`

Old text:

```
    if initializer is not None:
        _refuse_what_no_child_could_receive(initializer, "initializer")
    for position, argument in enumerate(initargs):
```

New text:

```
    for position, argument in enumerate(initargs):
```

### `r83-round-2.I1_fold_case`

R-344, after fix round 1: normalize_identity strips but no longer folds the case

- File: `src/cratekit/core/preflight.py`
- Source: `r83-round-2.json`, row `I1_fold_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_metadata_cli.py`, `tests/test_preflight.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2830 against a baseline of 2830
- Kills: 18 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_identity_typed_as_diskutil_prints_it_passes_the_mount_check`
  - `tests/test_preflight.py::test_an_identity_in_another_case_is_still_found_where_it_is_mounted`
  - `tests/test_preflight.py::test_an_identity_recorded_in_uppercase_matches_the_lowercase_the_kernel_reports`
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_backup_landing_between_the_two_acts_moves_the_digest`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_another_librarys_snapshot_is_refused_at_the_verb_and_names_both_volumes`
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_expected_volume_is_stated`
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_mirror_half_or_the_rehearsal_flag_is_added`
  - `tests/test_restore_cli.py::test_the_digest_moves_when_the_restore_is_pointed_somewhere_else`
  - `tests/test_restore_cli.py::test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    return identity.strip().lower()
```

New text:

```
    return identity.strip()
```

### `r83-round-2.I3_configured_compare_exact`

R-344, after fix round 1: the configured mount's compare goes back to exact equality

- File: `src/cratekit/core/preflight.py`
- Source: `r83-round-2.json`, row `I3_configured_compare_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_metadata_cli.py`, `tests/test_preflight.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2830 against a baseline of 2830
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_identity_typed_as_diskutil_prints_it_passes_the_mount_check`
  - `tests/test_preflight.py::test_an_identity_recorded_in_uppercase_matches_the_lowercase_the_kernel_reports`

Old text:

```
    if same_identity(recorded_identity, observed):
```

New text:

```
    if observed == recorded_identity:
```

### `r83-round-2.I4_elsewhere_compare_exact`

R-344, after fix round 1: the mounted elsewhere sweep's compare goes back to exact equality, the round 1 zero

- File: `src/cratekit/core/preflight.py`
- Source: `r83-round-2.json`, row `I4_elsewhere_compare_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_metadata_cli.py`, `tests/test_preflight.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2830 against a baseline of 2830
- Kills: 1 (killed)
- Killed:
  - `tests/test_preflight.py::test_an_identity_in_another_case_is_still_found_where_it_is_mounted`

Old text:

```
        if found is not None and same_identity(recorded_identity, found):
```

New text:

```
        if found == recorded_identity:
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

### `u301.F1_permission_read_as_absent`

_no_unless_refused: answer False over a permission error, so an attached volume under an untraversable directory reads as no volume

- File: `src/cratekit/core/preflight.py`
- Source: `u301.json`, row `F1_permission_read_as_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_preflight.py`, `tests/test_doctor.py`, `tests/test_paths_resolved.py`
- Collected: 499 against a baseline of 499
- Kills: 2 (killed)
- Killed:
  - `tests/test_preflight.py::test_a_refused_look_raises_rather_than_reading_as_no_mount[refusal0]`
  - `tests/test_preflight.py::test_a_refused_look_raises_rather_than_reading_as_no_mount[refusal1]`

Old text:

```
        if cause.permission_denied(exc) is not None:
            raise
        return False
    except ValueError:
```

New text:

```
        return False
    except ValueError:
```

### `u173.M20_agent_process`

processes: the agent's process name spelled otherwise, so the skill's pgrep waits on the wrong name

- File: `src/cratekit/core/processes.py`
- Source: `u173.json`, row `M20_agent_process`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_it_waits_on_the_processes_the_product_watches`

Old text:

```
REKORDBOX_PROCESSES: tuple[str, ...] = ("rekordbox", "rekordboxAgent")
```

New text:

```
REKORDBOX_PROCESSES: tuple[str, ...] = ("rekordbox", "rekordbox_agent")
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

### `r705-a.G10_long_wait_under_the_lock`

a Retry-After wait is slept holding the lock, so a second driver waits on the holder

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G10_long_wait_under_the_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released`

Old text:

```
                if due - now > self.settings.min_interval_s:

```

New text:

```
                if False:

```

### `r705-a.G11_lock_limit_without_the_interval`

the lock wait limit drops the one interval a holder may sleep under it

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G11_lock_limit_without_the_interval`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_lock_held_past_the_wait_is_refused_with_the_holder_named`

Old text:

```
                limit = LOCK_WAIT_S + self.settings.min_interval_s

```

New text:

```
                limit = LOCK_WAIT_S

```

### `r705-a.G12_park_forgotten`

a park the tool swallowed is not remembered, so the vendored adapter reads it as no file

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G12_park_forgotten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_held_lock_the_tool_swallowed_during_a_download_comes_out_of_fetch`
  - `tests/test_provider_gate.py::test_the_stop_is_remembered_so_a_swallowing_tool_still_parks`

Old text:

```
        if self._last_park is not None:
            raise self._last_park

```

New text:

```
        if False:
            raise self._last_park

```

### `r705-a.G13_process_calls_not_counted`

this process's call counter never moves, so the spend line reports nothing

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G13_process_calls_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 20 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_is_charged_only_for_its_own_calls`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate.py::test_a_nested_dispatch_keeps_the_outer_commands_count`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[excludes-another-processs-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[names-rate-limit-answers]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[reports-its-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[survives-a-refusal]`
  - `tests/test_provider_gate.py::test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_process_spend_is_this_process_alone`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        _PROCESS_CALLS += 1

```

New text:

```
        _PROCESS_CALLS += 0

```

### `r705-a.G1_interval_halved`

the shared interval is halved, so consecutive calls wait half of what the configuration says

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G1_interval_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 9 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_retry_after_holds_the_next_call_at_least_that_long[shorter-keeps-the-interval]`
  - `tests/test_provider_gate.py::test_a_retry_after_holds_the_next_call_at_least_that_long[unreadable-is-zero]`
  - `tests/test_provider_gate.py::test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released`
  - `tests/test_provider_gate.py::test_attach_routes_every_request_of_a_real_session_through_the_gate_once`
  - `tests/test_provider_gate.py::test_consecutive_calls_wait_out_the_interval`
  - `tests/test_provider_gate.py::test_the_interval_is_measured_from_the_last_call_by_any_gate`
  - `tests/test_provider_gate.py::test_the_interval_is_the_configured_one`
  - `tests/test_provider_gate.py::test_the_vendored_adapter_attaches_the_gate_to_an_injected_session`
  - `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`

Old text:

```
                due = max(state.last_call + self.settings.min_interval_s, state.not_before)

```

New text:

```
                due = max(state.last_call + self.settings.min_interval_s / 2, state.not_before)

```

### `r705-a.G2_last_call_ignored`

the interval is measured from now rather than from the last call any process made, so a second gate never waits on the first

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G2_last_call_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 9 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_retry_after_holds_the_next_call_at_least_that_long[shorter-keeps-the-interval]`
  - `tests/test_provider_gate.py::test_a_retry_after_holds_the_next_call_at_least_that_long[unreadable-is-zero]`
  - `tests/test_provider_gate.py::test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released`
  - `tests/test_provider_gate.py::test_attach_routes_every_request_of_a_real_session_through_the_gate_once`
  - `tests/test_provider_gate.py::test_consecutive_calls_wait_out_the_interval`
  - `tests/test_provider_gate.py::test_the_interval_is_measured_from_the_last_call_by_any_gate`
  - `tests/test_provider_gate.py::test_the_interval_is_the_configured_one`
  - `tests/test_provider_gate.py::test_the_vendored_adapter_attaches_the_gate_to_an_injected_session`
  - `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`

Old text:

```
                due = max(state.last_call + self.settings.min_interval_s, state.not_before)

```

New text:

```
                due = max(now, state.not_before)

```

### `r705-a.G3_retry_after_ignored`

a Retry-After the provider sends no longer holds the next call

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G3_retry_after_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_retry_after_holds_the_next_call_at_least_that_long[http-date-honoured]`
  - `tests/test_provider_gate.py::test_a_retry_after_holds_the_next_call_at_least_that_long[seconds-hold-the-next-call]`
  - `tests/test_provider_gate.py::test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released`

Old text:

```
                state.not_before = max(state.not_before, now + retry_after)

```

New text:

```
                state.not_before = state.not_before

```

### `r705-a.G4_trip_after_off_by_one`

the breaker trips one answer late, after seven rather than the six a spent ladder costs

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G4_trip_after_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_spent_ladder_through_the_gate_comes_out_as_the_park`
  - `tests/test_provider_gate.py::test_the_breaker_stops_a_sweep_at_the_first_surviving_rate_limit_with_the_rest_pending`
  - `tests/test_provider_gate.py::test_the_trip_count_is_one_spent_ladder`

Old text:

```
TRIP_AFTER = 6

```

New text:

```
TRIP_AFTER = 7

```

### `r705-a.G5_no_trip_on_long_retry_after`

a Retry-After at or above the cooldown no longer trips at once

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G5_no_trip_on_long_retry_after`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_client_session_as_the_park`
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_the_vendored_adapter_as_the_park`
  - `tests/test_provider_gate.py::test_a_retry_after_at_or_above_the_cooldown_trips_at_once[at-the-cooldown]`
  - `tests/test_provider_gate.py::test_a_retry_after_at_or_above_the_cooldown_trips_at_once[longer-than-the-cooldown]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[survives-a-refusal]`

Old text:

```
            if state.consecutive >= TRIP_AFTER or retry_after >= self.settings.cooldown_s:

```

New text:

```
            if state.consecutive >= TRIP_AFTER:

```

### `r705-a.G6_cooldown_not_recorded`

the trip lifts at once, so no later verb is refused

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G6_cooldown_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_retry_after_at_or_above_the_cooldown_trips_at_once[at-the-cooldown]`
  - `tests/test_provider_gate.py::test_a_retry_after_at_or_above_the_cooldown_trips_at_once[longer-than-the-cooldown]`
  - `tests/test_provider_gate.py::test_client_session_refuses_inside_the_cooldown_before_building_a_client`
  - `tests/test_provider_gate.py::test_inside_the_cooldown_assert_open_refuses_naming_the_lift_time`
  - `tests/test_provider_gate.py::test_the_cooldown_refuses_a_call_until_it_lifts[inside-a-call-is-refused-before-it-is-sent]`
  - `tests/test_provider_gate.py::test_the_sixth_consecutive_rate_limit_answer_trips_and_records_the_cooldown`
  - `tests/test_provider_gate.py::test_the_vendored_adapter_refuses_inside_the_cooldown_before_touching_the_tool`

Old text:

```
                state.lifts_at = now + max(self.settings.cooldown_s, retry_after)

```

New text:

```
                state.lifts_at = now

```

### `r705-a.G7_success_keeps_the_run`

a successful answer no longer breaks the run of rate limit answers, so six spread over a day trip the breaker

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G7_success_keeps_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_success_breaks_the_run_of_rate_limit_answers`

Old text:

```
        state.consecutive = 0
        state.not_before = 0.0
        self._last_park = None

```

New text:

```
        state.not_before = 0.0
        self._last_park = None

```

### `r705-a.G8_call_ignores_the_cooldown`

a call inside the cooldown is made anyway

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G8_call_ignores_the_cooldown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_cooldown_written_by_one_process_refuses_a_verb_started_in_another`
  - `tests/test_provider_gate.py::test_the_cooldown_refuses_a_call_until_it_lifts[inside-a-call-is-refused-before-it-is-sent]`

Old text:

```
                if state.cooling(now):
                    raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))

```

New text:

```
                if False:
                    raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))

```

### `r705-a.G9_assert_open_ignores_the_cooldown`

an opener asking the gate inside the cooldown is told to go ahead

- File: `src/cratekit/core/provider_gate.py`
- Source: `r705-a.json`, row `G9_assert_open_ignores_the_cooldown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_cooldown_written_by_one_process_refuses_a_verb_started_in_another`
  - `tests/test_provider_gate.py::test_client_session_refuses_inside_the_cooldown_before_building_a_client`
  - `tests/test_provider_gate.py::test_inside_the_cooldown_assert_open_refuses_naming_the_lift_time`
  - `tests/test_provider_gate.py::test_the_vendored_adapter_refuses_inside_the_cooldown_before_touching_the_tool`

Old text:

```
        if state.cooling(now):
            raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))

```

New text:

```
        if False:
            raise self._stopped(self._cooldown_cause(state, now, tripped_now=False))

```

### `r759-b.P4_lock_removed_r01`

the one call at a time lock is never taken, so two processes can have a request in flight together, repeat 1 of 10

- File: `src/cratekit/core/provider_gate.py`
- Source: `r759-b.json`, row `P4_lock_removed_r01`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py::test_two_processes_never_have_a_call_in_flight_together`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_two_processes_never_have_a_call_in_flight_together`

Old text:

```
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

```

New text:

```
                        pass

```

### `r759.P1_interval_dropped`

the interval is dropped from the due time, so a call waits on nothing but a Retry-After and two processes call back to back

- File: `src/cratekit/core/provider_gate.py`
- Source: `r759.json`, row `P1_interval_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`

Old text:

```
                due = max(state.last_call + self.settings.min_interval_s, state.not_before)

```

New text:

```
                due = max(state.last_call, state.not_before)

```

### `r759.P5_lock_shared`

the lock is taken shared rather than exclusive, so every process holds it at once

- File: `src/cratekit/core/provider_gate.py`
- Source: `r759.json`, row `P5_lock_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py::test_two_processes_never_have_a_call_in_flight_together`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_two_processes_never_have_a_call_in_flight_together`

Old text:

```
                        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

```

New text:

```
                        fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)

```

### `r759.P6_wait_skipped_stamp_kept`

the wait before a call is skipped while its stamp still reads the due time, so the stamps stay spaced and the requests go out back to back

- File: `src/cratekit/core/provider_gate.py`
- Source: `r759.json`, row `P6_wait_skipped_stamp_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_two_processes_keep_the_interval_between_every_call`

Old text:

```
        if due > now:
            self._sleep(due - now)
            now = max(self._clock(), due)

```

New text:

```
        if due > now:
            now = max(self._clock(), due)

```

### `u193.M10_config_not_read`

GateSettings.from_config: drop the configured ceiling, so the default always holds

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M10_config_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_defaults_to_five_hundred_and_round_trips`

Old text:

```
            calls_per_command=int(provider.calls_per_command),
```

New text:

```
(empty)
```

### `u193.M1_ceiling_check_removed`

Gate.call: never ask the ceiling, so a command spends past it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M1_ceiling_check_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 14 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_is_charged_only_for_its_own_calls`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate.py::test_a_nested_dispatch_keeps_the_outer_commands_count`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[spaced]`
  - `tests/test_provider_gate.py::test_the_stop_at_a_ceiling_of_one_is_said_in_words_a_person_reads[a-ceiling-of-one-says-one-call]`
  - `tests/test_provider_gate.py::test_the_stop_at_a_ceiling_of_one_is_said_in_words_a_person_reads[the-ceiling-never-says-kept-over-work-a-continue-does-again]`
  - `tests/test_provider_gate.py::test_the_stop_is_remembered_so_a_swallowing_tool_still_parks`

Old text:

```
                    if scope.spent() >= line:
```

New text:

```
                    if False:
```

### `u193.M2_ceiling_off_by_one`

Gate.call: stop only past the ceiling, so one call more than the line is sent

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M2_ceiling_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 14 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_is_charged_only_for_its_own_calls`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate.py::test_a_nested_dispatch_keeps_the_outer_commands_count`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[spaced]`
  - `tests/test_provider_gate.py::test_the_stop_at_a_ceiling_of_one_is_said_in_words_a_person_reads[a-ceiling-of-one-says-one-call]`
  - `tests/test_provider_gate.py::test_the_stop_at_a_ceiling_of_one_is_said_in_words_a_person_reads[the-ceiling-never-says-kept-over-work-a-continue-does-again]`
  - `tests/test_provider_gate.py::test_the_stop_is_remembered_so_a_swallowing_tool_still_parks`

Old text:

```
                    if scope.spent() >= line:
```

New text:

```
                    if scope.spent() > line:
```

### `u193.M3_spent_from_process_start`

Command.spent: count from process start, so a command is charged for calls before it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M3_spent_from_process_start`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 14 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_is_charged_only_for_its_own_calls`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate.py::test_a_nested_dispatch_keeps_the_outer_commands_count`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[spaced]`
  - `tests/test_provider_gate.py::test_the_stop_at_a_ceiling_of_one_is_said_in_words_a_person_reads[a-ceiling-of-one-says-one-call]`
  - `tests/test_provider_gate.py::test_the_stop_at_a_ceiling_of_one_is_said_in_words_a_person_reads[the-ceiling-never-says-kept-over-work-a-continue-does-again]`
  - `tests/test_provider_gate.py::test_the_stop_is_remembered_so_a_swallowing_tool_still_parks`

Old text:

```
        return max(0, _PROCESS_CALLS - self.started)
```

New text:

```
        return max(0, _PROCESS_CALLS)
```

### `u193.M7_env_parse_accepts_zero`

_raised_from_env: accept zero, so a hand written 0 sets a ceiling of nothing

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M7_env_parse_accepts_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_detached_child_reads_the_raised_ceiling_off_the_environment[0-None]`

Old text:

```
    return value if value > 0 else None
```

New text:

```
    return value
```

### `u193.M8_raised_ignored`

ceiling: ignore the raised ceiling, so --calls never lifts the line

- File: `src/cratekit/core/provider_gate.py`
- Source: `u193.json`, row `M8_raised_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_ceiling_raised_low_for_the_run_is_said_at_the_crawl_gate`
  - `tests/test_provider_gate.py::test_a_detached_child_reads_the_raised_ceiling_off_the_environment[700-700]`
  - `tests/test_provider_gate.py::test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[spaced]`

Old text:

```
    if scope is not None and scope.raised is not None:
        return scope.raised
```

New text:

```
    if False:
        return scope.raised
```

### `u205.G8_since_keeps_earlier_app_calls`

spend since: the app's share is not differenced, so a run is charged the app calls made before it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G8_since_keeps_earlier_app_calls`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 23214 against a baseline of 23214
- Kills: 7 (killed)
- Promoted: subset killed 0, full suite killed 7
- Killed:
  - `tests/intake/test_set_progress.py::test_the_watcher_reports_the_bytes_written_while_the_download_runs`
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[excludes-another-processs-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[names-rate-limit-answers]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[reports-its-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[survives-a-refusal]`
  - `tests/test_provider_gate.py::test_process_spend_is_this_process_alone`

Old text:

```
            app_calls=max(0, self.app_calls - earlier.app_calls),
```

New text:

```
            app_calls=self.app_calls,
```

### `u217.G1_ceiling_says_kept`

_ceiling_cause: say what it did is kept again, the words the card was filed over

- File: `src/cratekit/core/provider_gate.py`
- Source: `u217.json`, row `G1_ceiling_says_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_stop_at_a_ceiling_of_one_is_said_in_words_a_person_reads[the-ceiling-never-says-kept-over-work-a-continue-does-again]`

Old text:

```
                f"stay queued; what it read and did not keep is read again when it "
                f"continues"
```

New text:

```
                f"stay queued; what it did is kept"
```

### `u278.M10_window_short`

_expires: a minute leaves the window an hour after it STARTS, sixty seconds early

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M10_window_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 180 against a baseline of 180
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_doctor_names_an_identity_at_its_read_line_and_when_it_frees`
  - `tests/test_provider_budget.py::test_the_window_frees_as_its_oldest_minute_ages_out`

Old text:

```
    return float(bucket + BUCKET_S + WINDOW_S)
```

New text:

```
    return float(bucket + WINDOW_S)
```

### `u278.M11_window_dropped_on_read`

_State.from_json: drop the window on read, so every reader sees an empty hour

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M11_window_dropped_on_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 180 against a baseline of 180
- Kills: 25 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_call_made_under_a_redirected_state_directory_is_counted_by_the_live_gate`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_genre_walk_is_refused_over_its_group_alone[a-genre-walk-at-the-terminal-is-refused-over-its-group-alone]`
  - `tests/test_provider_budget.py::test_a_genre_walk_is_refused_over_its_group_alone[a-genre-walk-is-refused-in-its-own-words-over-its-group-alone]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-raised-ceiling-never-spends-the-reserve]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-write-verb-running-a-read-mode]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[calls-up-to-the-budget-on-a-read]`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - ... and 10 more, see the JSON sidecar

Old text:

```
        state.window = _window_from_json(data.get("window"))

```

New text:

```
(empty)
```

### `u278.M12_no_over_the_line_in_call`

Gate.call: drop the --calls past the line refusal

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M12_no_over_the_line_in_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 180 against a baseline of 180
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_calls_above_the_hours_budget_is_refused_before_any_call`

Old text:

```
                over = over_the_line(self.settings)
                if over is not None:
```

New text:

```
                over = over_the_line(self.settings)
                if False:
```

### `u278.M13_over_the_line_loosened`

over_the_line: let a --calls up to twice the hour's budget through

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M13_over_the_line_loosened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 180 against a baseline of 180
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_calls_above_the_hours_budget_is_refused_before_any_call`
  - `tests/test_provider_budget.py::test_calls_past_the_budget_is_refused_before_the_verb_runs[refused-before-a-verb-that-makes-no-call-runs]`
  - `tests/test_provider_budget.py::test_calls_past_the_budget_is_refused_before_the_verb_runs[the-continue-a-parked-job-prints-is-not-refused-by-its-own-calls]`

Old text:

```
    if scope.raised <= budget:
```

New text:

```
    if scope.raised <= budget * 2:
```

### `u278.M14_hour_raise_ignored`

hourly: ignore the hour raised for this run

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M14_hour_raise_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 180 against a baseline of 180
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_parked_jobs_continue_carries_the_hour_its_ceiling_needs`
  - `tests/test_provider_budget.py::test_the_hour_raised_for_one_run_lasts_that_run_and_reaches_a_child`

Old text:

```
    if scope is not None and scope.hourly is not None:
```

New text:

```
    if False:
```

### `u278.M15_hour_not_exported`

command: the raised hour never reaches a detached child

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M15_hour_not_exported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 180 against a baseline of 180
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_the_hour_raised_for_one_run_lasts_that_run_and_reaches_a_child`

Old text:

```
_exported(BUDGET_ENV, calls_per_hour)
```

New text:

```
_exported(BUDGET_ENV, None)
```

### `u278.M16_nested_class_kept`

command: a nested dispatch keeps the outer class

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M16_nested_class_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 180 against a baseline of 180
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`

Old text:

```
        outer.reserve = outer.declared = bool(reserve)

```

New text:

```
(empty)
```

### `u278.M17_spending_widens`

spending: widen to the reserve whatever the verb declared

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M17_spending_widens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync_go.py`
- Collected: 290 against a baseline of 290
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_spending_never_reaches_past_the_class_the_verb_declared`

Old text:

```
    scope.reserve = scope.declared

```

New text:

```
    scope.reserve = True

```

### `u278.M18_reading_noop`

reading: never narrow the command

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M18_reading_noop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`
- Collected: 275 against a baseline of 275
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_genre_walk_is_refused_over_its_group_alone[a-genre-walk-at-the-terminal-is-refused-over-its-group-alone]`
  - `tests/test_provider_budget.py::test_a_genre_walk_is_refused_over_its_group_alone[a-genre-walk-is-refused-in-its-own-words-over-its-group-alone]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-write-verb-running-a-read-mode]`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`
  - `tests/test_provider_budget.py::test_spending_never_reaches_past_the_class_the_verb_declared`

Old text:

```
    scope.reserve = False
    if settings is not None:
```

New text:

```
    if settings is not None:
```

### `u278.M2_future_minute_not_settled`

Gate.call: never write the settled window, so a minute stamped ahead slides with the clock and holds the line

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M2_future_minute_not_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 180 against a baseline of 180
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`

Old text:

```
                if state.settle(now):
                    try:
```

New text:

```
                if False:
                    try:
```

### `u278.M4_no_budget_check`

Gate.call: drop the hour's line, so a call past it is sent

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M4_no_budget_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`
- Collected: 275 against a baseline of 275
- Kills: 17 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-raised-ceiling-never-spends-the-reserve]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-write-verb-running-a-read-mode]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[calls-up-to-the-budget-on-a-read]`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_one_identity_at_its_line_leaves_the_other_open`
  - `tests/test_provider_budget.py::test_spending_never_reaches_past_the_class_the_verb_declared`
  - `tests/test_provider_budget.py::test_the_budget_counts_every_command_and_every_gate_on_the_file`
  - `tests/test_provider_budget.py::test_the_hour_raised_for_one_run_lasts_that_run_and_reaches_a_child`
  - ... and 2 more, see the JSON sidecar

Old text:

```
                if spent >= hour_line:
```

New text:

```
                if False:
```

### `u278.M5_budget_off_by_one`

Gate.call: let one call past the line

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M5_budget_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 180 against a baseline of 180
- Kills: 16 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-raised-ceiling-never-spends-the-reserve]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-write-verb-running-a-read-mode]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[calls-up-to-the-budget-on-a-read]`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_one_identity_at_its_line_leaves_the_other_open`
  - `tests/test_provider_budget.py::test_spending_never_reaches_past_the_class_the_verb_declared`
  - `tests/test_provider_budget.py::test_the_budget_counts_every_command_and_every_gate_on_the_file`
  - `tests/test_provider_budget.py::test_the_hour_raised_for_one_run_lasts_that_run_and_reaches_a_child`
  - `tests/test_provider_budget.py::test_the_window_frees_as_its_oldest_minute_ages_out`
  - ... and 1 more, see the JSON sidecar

Old text:

```
                if spent >= hour_line:
```

New text:

```
                if spent > hour_line:
```

### `u278.M6_count_not_written`

_send_now: stop counting calls in the window

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M6_count_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 180 against a baseline of 180
- Kills: 27 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_call_made_under_a_redirected_state_directory_is_counted_by_the_live_gate`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_genre_walk_is_refused_over_its_group_alone[a-genre-walk-at-the-terminal-is-refused-over-its-group-alone]`
  - `tests/test_provider_budget.py::test_a_genre_walk_is_refused_over_its_group_alone[a-genre-walk-is-refused-in-its-own-words-over-its-group-alone]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-raised-ceiling-never-spends-the-reserve]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-write-verb-running-a-read-mode]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[calls-up-to-the-budget-on-a-read]`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - ... and 12 more, see the JSON sidecar

Old text:

```
        state.count(identity, now)

```

New text:

```
(empty)
```

### `u278.M7_identities_merged`

Gate.call: read the account's window for every identity

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M7_identities_merged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 180 against a baseline of 180
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_one_identity_at_its_line_leaves_the_other_open`

Old text:

```
                spent = state.spent(identity, now)
```

New text:

```
                spent = state.spent(ACCOUNT, now)
```

### `u278.M8_no_reserve`

line_for: a read reaches the whole budget

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M8_no_reserve`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`
- Collected: 275 against a baseline of 275
- Kills: 25 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_budget.py::test_a_cooldown_still_refuses_first_and_keeps_its_own_reason`
  - `tests/test_provider_budget.py::test_a_genre_walk_is_refused_over_its_group_alone[a-genre-walk-at-the-terminal-is-refused-over-its-group-alone]`
  - `tests/test_provider_budget.py::test_a_genre_walk_is_refused_over_its_group_alone[a-genre-walk-is-refused-in-its-own-words-over-its-group-alone]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[account]`
  - `tests/test_provider_budget.py::test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer[app-credentials]`
  - `tests/test_provider_budget.py::test_a_read_dispatched_inside_a_write_runs_under_the_read_line`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-raised-ceiling-never-spends-the-reserve]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[a-write-verb-running-a-read-mode]`
  - `tests/test_provider_budget.py::test_a_read_is_held_to_the_read_line[calls-up-to-the-budget-on-a-read]`
  - `tests/test_provider_budget.py::test_a_read_stops_at_the_reserve_while_a_go_still_runs`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`
  - `tests/test_provider_budget.py::test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class`
  - `tests/test_provider_budget.py::test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope`
  - `tests/test_provider_budget.py::test_doctor_names_an_identity_at_its_read_line_and_when_it_frees`
  - ... and 10 more, see the JSON sidecar

Old text:

```
    return budget - reserve_of(budget, settings.reserve_share)
```

New text:

```
    return budget
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

### `u293.G1_night_line_asked`

Gate.call: never ask the night's line, so a night pass spends past its budget

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G1_night_line_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 283 against a baseline of 283
- Kills: 6 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_total_below_the_mark_is_a_spend_nobody_can_read_and_stops`
  - `tests/test_provider_gate_night.py::test_another_processs_calls_count_against_the_night`
  - `tests/test_provider_gate_night.py::test_outside_any_command_a_line_off_the_environment_holds_the_call`
  - `tests/test_provider_gate_night.py::test_the_call_past_the_nights_line_is_never_sent_and_parks_naming_the_night`
  - `tests/test_provider_gate_night.py::test_the_lower_of_the_ceiling_and_a_handed_line_stops_the_third_call[an-inherited-night-line-stops-a-child-at-the-nights-remainder]`
  - `tests/test_provider_gate_night.py::test_the_nights_line_is_held_to_what_is_left_of_the_command_ceiling`

Old text:

```
                if held_night is not None and (
```

New text:

```
                if False and (
```

### `u293.G2_night_line_off_by_one`

Gate.call: stop only past the line, so one call beyond the night's budget is sent

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G2_night_line_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 283 against a baseline of 283
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_another_processs_calls_count_against_the_night`
  - `tests/test_provider_gate_night.py::test_outside_any_command_a_line_off_the_environment_holds_the_call`
  - `tests/test_provider_gate_night.py::test_the_call_past_the_nights_line_is_never_sent_and_parks_naming_the_night`
  - `tests/test_provider_gate_night.py::test_the_lower_of_the_ceiling_and_a_handed_line_stops_the_third_call[an-inherited-night-line-stops-a-child-at-the-nights-remainder]`
  - `tests/test_provider_gate_night.py::test_the_nights_line_is_held_to_what_is_left_of_the_command_ceiling`

Old text:

```
                    state.calls - held_night.start >= held_night.budget
```

New text:

```
                    state.calls - held_night.start > held_night.budget
```

### `u293.G3_total_below_mark`

Gate.call: a total below the night's mark reads as nothing spent rather than stopping

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G3_total_below_mark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 283 against a baseline of 283
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_total_below_the_mark_is_a_spend_nobody_can_read_and_stops`

Old text:

```
                    or state.calls < held_night.start
```

New text:

```
                    or False
```

### `u293.G4_child_reads_no_line`

command: a scope opened in a child reads no night line off the environment

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G4_child_reads_no_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 283 against a baseline of 283
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_the_lower_of_the_ceiling_and_a_handed_line_stops_the_third_call[a-line-read-off-the-environment-is-held-beside-the-ceiling]`
  - `tests/test_provider_gate_night.py::test_the_lower_of_the_ceiling_and_a_handed_line_stops_the_third_call[an-inherited-night-line-stops-a-child-at-the-nights-remainder]`

Old text:

```
        night=_night_from_env(),
```

New text:

```
        night=None,
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

### `u293.G6_nested_lower_line`

night: a nested line widens the outer night's remainder

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G6_nested_lower_line`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 283 against a baseline of 283
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_nested_night_keeps_the_lower_line`

Old text:

```
        if left < held.budget:
```

New text:

```
        if False:
```

### `u293.G7_hour_never_raised`

night: the night's hour replaces the configured one, raising it when set higher

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G7_hour_never_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 283 against a baseline of 283
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_the_night_lowers_the_hour_and_never_raises_it`

Old text:

```
    hour = min(hourly(settings), max(1, int(calls_per_hour)))
```

New text:

```
    hour = max(1, int(calls_per_hour))
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

### `u301.G1_positive_env_accepts_zero`

_positive_env: read zero as a raise, so CRATEKIT calls of 0 lifts the ceiling to nothing

- File: `src/cratekit/core/provider_gate.py`
- Source: `u301.json`, row `G1_positive_env_accepts_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_provider_gate_night.py`
- Collected: 234 against a baseline of 234
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_detached_child_reads_the_raised_ceiling_off_the_environment[0-None]`

Old text:

```
    return value if value > 0 else None
```

New text:

```
    return value if value >= 0 else None
```

### `u301.G2_run_cause_retryable`

_run_cause: every gate refusal says retryable, so a cooldown or a ceiling invites an immediate retry

- File: `src/cratekit/core/provider_gate.py`
- Source: `u301.json`, row `G2_run_cause_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_provider_gate_night.py`
- Collected: 234 against a baseline of 234
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees`
  - `tests/test_provider_gate.py::test_a_lock_held_past_the_wait_is_refused_with_the_holder_named`
  - `tests/test_provider_gate.py::test_the_sixth_consecutive_rate_limit_answer_trips_and_records_the_cooldown`
  - `tests/test_provider_gate_night.py::test_the_call_past_the_nights_line_is_never_sent_and_parks_naming_the_night`

Old text:

```
        retryable=False, origin=("provider_gate",), detail=detail,
```

New text:

```
        retryable=True, origin=("provider_gate",), detail=detail,
```

### `u301.G3_calls_word_plural`

_calls_word: always the plural, so a refusal over one call reads 1 calls

- File: `src/cratekit/core/provider_gate.py`
- Source: `u301.json`, row `G3_calls_word_plural`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_provider_budget.py`
- Collected: 180 against a baseline of 180
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_stop_at_a_ceiling_of_one_is_said_in_words_a_person_reads[a-ceiling-of-one-says-one-call]`

Old text:

```
    return "call" if n == 1 else "calls"
```

New text:

```
    return "calls"
```

### `u301.G4_parked_forgets_the_scope`

Gate._parked: leave the open command's stop unset, so the next call in the same command is not refused

- File: `src/cratekit/core/provider_gate.py`
- Source: `u301.json`, row `G4_parked_forgets_the_scope`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_provider_gate_night.py`
- Collected: 234 against a baseline of 234
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling`
  - `tests/test_provider_gate_night.py::test_the_call_past_the_nights_line_is_never_sent_and_parks_naming_the_night`

Old text:

```
            scope.stopped = cause
        return self._stopped(cause)
```

New text:

```
            pass
        return self._stopped(cause)
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

### `r1665-b.C1_w5_composite`

The composite for the zero W5_unreadable_check_passes in r1665.md, what it holds with the open refusal: an open the gate refuses and a consistency check that raises both answer True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665-b.json`, row `C1_w5_composite`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, the module's names now read through the module
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

### `r1665.W3_no_release_of_the_copy`

integrity_ok: release only the session, leaving the pooled connection on the throwaway copy open while it is removed

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W3_no_release_of_the_copy`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, its comment cut to its rule by the prose pass,, the module's names now read through the module
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`

Old text:

```
                # The full release: the throwaway directory is removed next.
                _writer().close_db(db)
```

New text:

```
                # The full release: the throwaway directory is removed next.
                db.close()
```

### `r1665.W6_refused_open_passes`

integrity_ok: an open the gate refuses answers True

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W6_refused_open_passes`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, the module's names now read through the module
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

### `r1677.R5_file_set_drops_playlist`

_copy_file_set: copy the companions but not the playlist file, so the measured list and the copied list drift

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1677.json`, row `R5_file_set_drops_playlist`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_snapshot.py`, `tests/test_restore.py`
- Collected: 278 against a baseline of 278
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_snapshot.py::test_the_legacy_playlist_file_travels_with_the_database`
  - `tests/test_snapshot_check_room_r1677.py::test_the_file_set_measured_is_the_one_the_check_copies`

Old text:

```
    for companion in companions:
        if companion.exists():
```

New text:

```
    for companion in companions[:-1]:
        if companion.exists():
```

### `r372-a.A10_copy_left_behind`

disposable_copy: leave the temporary directory and the copy in it

- File: `src/cratekit/core/rb_copies.py`
- Source: `r372-a.json`, row `A10_copy_left_behind`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in disposable_copy, the module's names now read through the module
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 15 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_copy_it_could_not_open_as_unknown_rather_than_good`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_minority_as_a_note_and_a_clean_collection_as_ok`
  - `tests/test_paths_resolved.py::test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it`
  - `tests/test_paths_resolved.py::test_setup_leaves_a_damaged_library_to_the_notes_and_doctor`
  - `tests/test_paths_resolved.py::test_setup_notes_a_copy_it_could_not_open_and_leaves_the_verdict_to_doctor`
  - `tests/test_paths_resolved.py::test_setup_offers_a_rule_from_the_old_drive_to_where_the_library_now_is[a-current-drive-not-the-root]`
  - `tests/test_paths_resolved.py::test_setup_offers_a_rule_from_the_old_drive_to_where_the_library_now_is[the-root-when-the-old-name-is-recorded-twice]`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_rows_already_sit_where_they_say[the-root-sits-under-the-recorded-drive]`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_rows_already_sit_where_they_say[the-two-drive-names-agree]`
  - `tests/test_paths_resolved.py::test_setup_offers_the_rule_from_the_databases_own_drive_names_off_a_copy`
  - `tests/test_paths_resolved.py::test_setup_records_nothing_when_the_offer_goes_unanswered`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`
  - `tests/test_paths_resolved.py::test_the_disposable_copy_is_private_and_gone_afterwards`

Old text:

```
        shutil.rmtree(directory, ignore_errors=True)
```

New text:

```
        pass
```

### `r372-a.A11_copy_under_a_running_application`

read_only_copy: drop its own closed assertion, the layer beneath doctor and setup

- File: `src/cratekit/core/rb_copies.py`
- Source: `r372-a.json`, row `A11_copy_under_a_running_application`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in read_only_copy, the module's names now read through the module
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_the_read_only_copy_refuses_under_a_running_application_on_its_own`

Old text:

```
    _writer().assert_rekordbox_closed("copying the database for a read only look")
```

New text:

```
    pass
```

### `r372-a.A12_separator_kept`

recorded_db_drives: keep the trailing separator rekordbox stores, so the rule never matches

- File: `src/cratekit/core/rb_copies.py`
- Source: `r372-a.json`, row `A12_separator_kept`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 7 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_recorded_drives_strip_the_separator_rekordbox_stores_and_blank_is_none`
  - `tests/test_paths_resolved.py::test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it`
  - `tests/test_paths_resolved.py::test_setup_offers_a_rule_from_the_old_drive_to_where_the_library_now_is[a-current-drive-not-the-root]`
  - `tests/test_paths_resolved.py::test_setup_offers_a_rule_from_the_old_drive_to_where_the_library_now_is[the-root-when-the-old-name-is-recorded-twice]`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_rows_already_sit_where_they_say[the-root-sits-under-the-recorded-drive]`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_rows_already_sit_where_they_say[the-two-drive-names-agree]`
  - `tests/test_paths_resolved.py::test_setup_offers_the_rule_from_the_databases_own_drive_names_off_a_copy`

Old text:

```
        stripped = value.strip().rstrip("/\\")
```

New text:

```
        stripped = value.strip()
```

### `r663-a.M1_empty_not_refused_before_open`

the size of the copy is no longer asked before the open, so an empty copy reaches the binding and is classified only if the canary is what fails

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-a.json`, row `M1_empty_not_refused_before_open`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in read_only_copy, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 4 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[empty]`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`
  - `tests/test_paths_resolved.py::test_the_file_whose_tables_are_listed_is_only_ever_a_copy[empty]`

Old text:

```
        refusal = None if copied.stat().st_size else _writer()._not_a_library(Path(source), copied)
```

New text:

```
        refusal = None
```

### `r663-a.M5_failed_listing_returns_empty_set`

a table listing whose query fails answers an empty set rather than None, so a file that could not be read is reported as holding nothing

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-a.json`, row `M5_failed_listing_returns_empty_set`
- Moved: the same text, now in src/cratekit/core/rb_copies.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_file_holding_one_canary_table_or_no_sqlite_keeps_the_canarys_refusal[not-sqlite]`
  - `tests/test_paths_resolved.py::test_setup_leaves_a_damaged_library_to_the_notes_and_doctor`

Old text:

```
        return {str(row[0]) for row in rows}
    except Exception:  # noqa: BLE001 - an unlistable file keeps the canary's refusal
        return None
```

New text:

```
        return {str(row[0]) for row in rows}
    except Exception:  # noqa: BLE001 - an unlistable file keeps the canary's refusal
        return set()
```

### `r663-a.M6_listing_opened_with_the_key_always`

the table listing opens every copy with the key rather than asking the header, so a plain foreign file cannot be listed

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-a.json`, row `M6_listing_opened_with_the_key_always`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in _copy_tables, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[foreign]`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`

Old text:

```
            db = Rekordbox6Database(path=str(copied), unlock=_writer().unlock_needed(copied))
```

New text:

```
            db = Rekordbox6Database(path=str(copied), unlock=True)
```

### `r663-b.M2_every_open_refusal_classified`

the canary reason gate is removed, so any refusal on the way in, a pin or a failed open, is also asked whether the copy is a library

- File: `src/cratekit/core/rb_copies.py`
- Source: `r663-b.json`, row `M2_every_open_refusal_classified`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in read_only_copy, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_refusal_on_the_way_in_is_not_reclassified_as_a_wrong_path`

Old text:

```
            if exc.cause.reason != "canary-read-failed":
                raise
            refusal = _writer()._not_a_library(Path(source), copied)
```

New text:

```
            refusal = _writer()._not_a_library(Path(source), copied)
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

### `u285.M10_no_offset_edge`

placeable: catch OverflowError alone, so a year 1 stamp with no offset fails its row with ValueError in every zone

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M10_no_offset_edge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 15 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-AOE+12]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-JST-9]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-LINT-14]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-UTC0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-AOE+12]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-JST-9]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-LINT-14]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-UTC0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-AOE+12]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-JST-9]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-LINT-14]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-UTC0]`

Old text:

```
        except (OverflowError, ValueError) as exc:
```

New text:

```
        except OverflowError as exc:
```

### `u285.M11_value_error_message`

placeable: read any ValueError at an edge year as the bound, so text the binding cannot parse is hidden as the zero date

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M11_value_error_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_text_the_binding_cannot_parse_still_fails_as_it_did[0001-13-01 00:00:00]`
  - `tests/test_rb_dates.py::test_text_the_binding_cannot_parse_still_fails_as_it_did[9999-02-30 00:00:00]`

Old text:

```
            if isinstance(exc, ValueError) and str(exc) != _PAST_THE_EDGE[edge]:
```

New text:

```
            if False:
```

### `u285.M12_xml_bound_dropped`

keeps_bounds: hand a bound updated_at to the binding's XML update, so a commit writes the floor's instant into DEADCA7's nodes

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M12_xml_bound_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 4 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_bound_is_never_handed_to_the_xml_update`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[JST-9]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[UTC0]`

Old text:

```
        if isinstance(updated_at, datetime) and updated_at in (FLOOR, CEILING):
```

New text:

```
        if False:
```

### `u285.M13_xml_empty_update`

keeps_bounds: call the update with nothing to set rather than skipping it, which marks the file changed

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M13_xml_empty_update`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_bound_is_never_handed_to_the_xml_update`

Old text:

```
            if parent_id is None and attribute is None and lib_type is None and check_type is None:
                return None
```

New text:

```
            if False:
                return None
```

### `u285.M14_xml_update_installed`

install: leave the binding's XML update unwrapped, so only the read is guarded

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M14_xml_update_installed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[JST-9]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[UTC0]`
  - `tests/test_rb_dates.py::test_installing_twice_wraps_once`
  - `tests/test_rb_dates.py::test_the_open_seam_installs_the_wrapper`

Old text:

```
    aux_files.MasterPlaylistXml.update = keeps_bounds(aux_files.MasterPlaylistXml.update)
```

New text:

```
    pass
```

### `u285.M2_overflow_reads_as_edge`

placeable: re-raise every OverflowError, so the zero date fails west of UTC as before the unit

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M2_overflow_reads_as_edge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 24 (killed)
- Killed:
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-calendars-last-moment-reads-as-the-ceiling-JST-9]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-calendars-last-moment-reads-as-the-ceiling-LINT-14]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-zero-date-reads-as-the-floor-AOE+12]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-zero-date-reads-as-the-floor-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_handle_reads_the_whole_tree_over_a_zero_dated_push_and_writes_nothing`
  - `tests/test_rb_dates.py::test_a_wrapper_installed_after_a_handle_has_read_is_still_the_one_called`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-AOE+12]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-JST-9]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-LINT-14]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00-FLOOR-UTC0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-AOE+12]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[0001-01-01 00:00:00.000-FLOOR-EST5EDT,M3.2.0,M11.1.0]`
  - ... and 9 more, see the JSON sidecar

Old text:

```
            if edge is None:
                raise
```

New text:

```
            if True:
                raise
```

### `u285.M3_edge_hides_real_overflow`

_edge: answer FLOOR for any year, so an overflow away from the calendar's edge is hidden as the zero date

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M3_edge_hides_real_overflow`
- Moved: U953 rewrote _edge's two year comparisons as a lookup, so defaulting the lookup to FLOOR answers FLOOR for any other year as the old return FLOOR did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_an_overflow_away_from_the_calendars_edge_is_raised_as_it_came`
  - `tests/test_rb_dates.py::test_text_the_binding_cannot_parse_still_fails_as_it_did[0000-01-01 00:00:00]`

Old text:

```
    return {FLOOR.year: FLOOR, CEILING.year: CEILING}.get(int(found.group(1)))
```

New text:

```
    return {FLOOR.year: FLOOR, CEILING.year: CEILING}.get(int(found.group(1)), FLOOR)
```

### `u285.M4_floor_clamp`

placeable: drop the floor clamp, so east of UTC the zero date reads as 0001-01-01 09:00, which a reader cannot convert again

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M4_floor_clamp`
- Moved: U953 rewrote placeable's two clamps as one min of a max, so dropping the max is the same dropped floor clamp
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-zero-date-reads-as-the-floor-JST-9]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-zero-date-reads-as-the-floor-LINT-14]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-zero-date-reads-as-the-floor-UTC0]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[JST-9]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[UTC0]`

Old text:

```
        return min(max(moment, FLOOR), CEILING)
```

New text:

```
        return min(moment, CEILING)
```

### `u285.M5_ceiling_clamp`

placeable: drop the ceiling clamp, so west of UTC the calendar's last moment reads as itself, unconvertible again

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M5_ceiling_clamp`
- Moved: U953 rewrote placeable's two clamps as one min of a max, so dropping the min is the same dropped ceiling clamp
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 3 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-calendars-last-moment-reads-as-the-ceiling-AOE+12]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-calendars-last-moment-reads-as-the-ceiling-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-calendars-last-moment-reads-as-the-ceiling-UTC0]`

Old text:

```
        return min(max(moment, FLOOR), CEILING)
```

New text:

```
        return max(moment, FLOOR)
```

### `u285.M6_floor_value`

FLOOR: the calendar's first day rather than a day inside it, which no zone can convert back

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M6_floor_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 11 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-zero-date-reads-as-the-floor-AOE+12]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-zero-date-reads-as-the-floor-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-zero-date-reads-as-the-floor-JST-9]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-zero-date-reads-as-the-floor-LINT-14]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-zero-date-reads-as-the-floor-UTC0]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[JST-9]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[AOE+12]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[JST-9]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[LINT-14]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[UTC0]`

Old text:

```
FLOOR = datetime(1, 1, 2)
```

New text:

```
FLOOR = datetime(1, 1, 1)
```

### `u285.M7_ceiling_value`

CEILING: the calendar's last day rather than a day inside it

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M7_ceiling_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 10 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-calendars-last-moment-reads-as-the-ceiling-AOE+12]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-calendars-last-moment-reads-as-the-ceiling-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-calendars-last-moment-reads-as-the-ceiling-JST-9]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-calendars-last-moment-reads-as-the-ceiling-LINT-14]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-calendars-last-moment-reads-as-the-ceiling-UTC0]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[AOE+12]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[JST-9]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[LINT-14]`
  - `tests/test_rb_dates.py::test_each_bound_converts_back_in_every_zone[UTC0]`

Old text:

```
CEILING = datetime(9999, 12, 30)
```

New text:

```
CEILING = datetime(9999, 12, 31)
```

### `u285.M8_install_once`

placeable: wrap a wrapper again rather than answering it as it is, so a second open nests the conversion

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M8_install_once`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_installing_twice_wraps_once`

Old text:

```
    if getattr(convert, _MARK, False):
        return convert
```

New text:

```
    if False:
        return convert
```

### `u285.M9_aware_passes`

placeable: compare an aware answer with the naive bounds rather than handing it on

- File: `src/cratekit/core/rb_dates.py`
- Source: `u285.json`, row `M9_aware_passes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_an_aware_answer_is_handed_on_as_it_came`

Old text:

```
        if moment.tzinfo is not None:
```

New text:

```
        if False:
```

### `u953.M22_edge_reads_only_the_floor`

_edge reads a stamp at the ceiling's year as no edge, so it is not clamped

- File: `src/cratekit/core/rb_dates.py`
- Source: `u953.json`, row `M22_edge_reads_only_the_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`
- Collected: 50 against a baseline of 50
- Kills: 7 (killed)
- Killed:
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-calendars-last-moment-reads-as-the-ceiling-JST-9]`
  - `tests/test_rb_dates.py::test_a_calendar_edge_reads_as_its_bound_in_every_zone[the-calendars-last-moment-reads-as-the-ceiling-LINT-14]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-AOE+12]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-JST-9]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-LINT-14]`
  - `tests/test_rb_dates.py::test_an_edge_stamp_with_no_offset_reads_as_its_bound[9999-12-31 23:00:00-CEILING-UTC0]`

Old text:

```
    return {FLOOR.year: FLOOR, CEILING.year: CEILING}.get(int(found.group(1)))
```

New text:

```
    return {FLOOR.year: FLOOR}.get(int(found.group(1)))
```

### `r1890.P3_unreserved_slug_in_rb_nodes`

rb_nodes, a part, raises the node move's confinement refusal under a slug with no reserved code

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r1890.json`, row `P3_unreserved_slug_in_rb_nodes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_every_refusal_the_writer_or_a_part_raises_through_a_factory_is_reserved`

Old text:

```
        raise _writer()._unavailable(
            "whitelist-violation",
            "the node change reached rows it did not plan
```

New text:

```
        raise _writer()._unavailable(
            "node-change-unconfined",
            "the node change reached rows it did not plan
```

### `r1890.P4_unreadable_slug_in_rb_nodes`

rb_nodes, a part, raises the confinement refusal with its slug held in a name, which no scan reads

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r1890.json`, row `P4_unreadable_slug_in_rb_nodes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_every_refusal_names_its_reason_as_a_literal_the_scan_can_read`

Old text:

```
        raise _writer()._unavailable(
            "whitelist-violation",
            "the node change reached rows it did not plan
```

New text:

```
        reason = "node-change-unconfined"
        raise _writer()._unavailable(
            reason,
            "the node change reached rows it did not plan
```

### `u329.P3_rb_nodes_wrong_family`

rb_nodes binds _writer to the session's accessor, so every _writer().name reads the wrong module

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u329.json`, row `P3_rb_nodes_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_inbox_rotate.py`, `tests/test_cutover_cli.py`, `tests/test_rb_writer_parts_guard.py`, `tests/test_cli_contract.py`
- Collected: 1314 against a baseline of 1314
- Kills: 18 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_removal_or_a_move_beyond_the_plan_is_refused_and_rolled_back`
  - `tests/test_inbox_rotate.py::test_old_is_created_once_a_second_run_plans_nothing_and_still_asks_and_old_is_reused`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`
  - `tests/test_inbox_rotate.py::test_the_judge_admits_exactly_the_planned_change_and_refuses_one_never_made_or_a_renumbering`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after0-djmdContent]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after1-only a removed playlist]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after10-rb_local_deleted]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after11-unplanned]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after2-only its marker may go on]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after3-is still live]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after4-added or disappeared]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after5-not live under the planned]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after6-not live under the planned]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after7-['Name']]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after8-does not carry the marker]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
from cratekit.core.rb_call_time import writer as _writer
```

New text:

```
from cratekit.core.session_call_time import session as _writer
```

### `r1890.P2_system_exit_in_rb_probes`

rb_probes, a part, exits the process with SystemExit when a listed process has no probe

- File: `src/cratekit/core/rb_probes.py`
- Source: `r1890.json`, row `P2_system_exit_in_rb_probes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_no_part_of_the_writer_raises_a_bare_runtime_error_or_system_exit`

Old text:

```
        if probe_name is None:
            raise _writer()._running(
```

New text:

```
        if probe_name is None:
            raise SystemExit(1)
            raise _writer()._running(
```

### `u211.W1_writer_falls_back`

_asked_or_scanned: re-raise pyrekordbox's error instead of asking the careful scan, the defect itself

- File: `src/cratekit/core/rb_probes.py`
- Source: `u211.json`, row `W1_writer_falls_back`
- Moved: the same text, now in src/cratekit/core/rb_probes.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_probes.py, was in src/cratekit/core/rb_writer.py
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
- Moved: the same text, now in src/cratekit/core/rb_probes.py, was in src/cratekit/core/rb_writer.py
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

### `u300.S12_settings_read_in_the_part`

cloud_sync_state reads the settings with the part's own reader, so a patched reader is not asked

- File: `src/cratekit/core/rb_probes.py`
- Source: `u300.json`, row `S12_settings_read_in_the_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_rb_writer_db.py`
- Collected: 257 against a baseline of 257
- Kills: 20 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_playlist_creation_commits_because_the_table_is_whitelisted`
  - `tests/test_rb_writer_db.py::test_a_real_delete_is_refused_and_rolled_back`
  - `tests/test_rb_writer_db.py::test_a_registered_column_write_commits_and_persists`
  - `tests/test_rb_writer_db.py::test_a_registration_widens_the_gate_by_exactly_its_own_fields`
  - `tests/test_rb_writer_db.py::test_a_rehearsed_restore_returns_a_modified_database_to_its_pre_session_state`
  - `tests/test_rb_writer_db.py::test_a_write_intent_open_passes_the_process_refusal_and_the_recorded_pin`
  - `tests/test_rb_writer_db.py::test_an_analysis_column_write_is_refused_and_rolled_back`
  - `tests/test_rb_writer_db.py::test_the_batch_membership_primitive_reads_presence_once_and_inserts_what_is_absent`
  - `tests/test_rb_writer_db.py::test_the_tag_primitives_mirror_an_existing_category`
  - `tests/test_rb_writer_db.py::test_the_tree_primitives_are_idempotent`
  - `tests/test_rb_writer_db.py::test_the_write_lock_is_held_across_a_real_commit`
  - `tests/test_rb_writer_guard.py::test_a_probe_that_queries_cannot_flush_a_forbidden_write_past_the_guard`
  - `tests/test_rb_writer_guard.py::test_a_real_settings_file_parses_into_a_verdict`
  - `tests/test_rb_writer_guard.py::test_an_unreadable_settings_file_is_unknown_and_says_why`
  - `tests/test_rb_writer_guard.py::test_the_canary_reads_the_settings_file_and_NOTHING_ELSE`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        settings = _writer().read_rekordbox_settings()
```

New text:

```
        settings = read_rekordbox_settings()
```

### `u300.S1_probe_resolved_in_the_part`

rekordbox_processes_running asks the part's own probes, so a probe patched on rb_writer is not asked

- File: `src/cratekit/core/rb_probes.py`
- Source: `u300.json`, row `S1_probe_resolved_in_the_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_db.py`
- Collected: 269 against a baseline of 269
- Kills: 5 (killed)
- Killed:
  - `tests/test_process_guard.py::test_the_two_mechanisms_agree_on_the_same_machine_state`
  - `tests/test_rb_writer_db.py::test_the_commit_refuses_while_the_agent_is_running`
  - `tests/test_rb_writer_guard.py::test_agent_only_is_reported`
  - `tests/test_rb_writer_guard.py::test_commit_guarded_refuses_when_agent_running`
  - `tests/test_rb_writer_guard.py::test_processes_running_reports_both_names`

Old text:

```
            if getattr(_writer(), probe_name)():
```

New text:

```
            if globals()[probe_name]():
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

### `r1890.P1_bare_runtime_error_in_rb_removal`

rb_removal, a part, raises a bare RuntimeError where the binding maps no class, so the refusal has no code downstream

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1890.json`, row `P1_bare_runtime_error_in_rb_removal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_parts_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_parts_guard.py::test_no_part_of_the_writer_raises_a_bare_runtime_error_or_system_exit`

Old text:

```
    raise _writer()._unavailable(
        "whitelist-violation",
        f"the binding maps no class for {table!r}
```

New text:

```
    raise RuntimeError(
        f"the binding maps no class for {table!r}
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

### `u955.S07_unreadable_count_no_rollback`

counter_at_commit: a count that cannot be read refuses without rolling back

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S07_unreadable_count_no_rollback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_a_count_that_cannot_be_said_refuses_and_rolls_back[a-buffer-that-is-not-a-list]`
  - `tests/test_rb_removal_stamp.py::test_a_count_that_cannot_be_said_refuses_and_rolls_back[a-count-that-cannot-be-read]`

Old text:

```
        db.rollback()
        raise _writer()._unavailable(
            "whitelist-violation",
            "the binding's update count
```

New text:

```
        raise _writer()._unavailable(
            "whitelist-violation",
            "the binding's update count
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

### `u955.S09_time_not_utc`

stamp_time: a moment in another zone is written as its local clock, labelled UTC

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S09_time_not_utc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_a_stamp_s_time_is_rekordbox_s_text_form_in_utc[other-zone]`

Old text:

```
    utc = moment.astimezone(timezone.utc)
```

New text:

```
    utc = moment
```

### `u955.S14_no_stamp_path_admits_stamps`

_renumbering_violations: with no stamp planned, a row whose stamp columns moved is admitted

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S14_no_stamp_path_admits_stamps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_without_a_stamp_the_planned_row_moves_trackno_alone`

Old text:

```
        if new != old:
```

New text:

```
        if False:
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

### `u955.S16_usn_unmoved_admitted`

_stamp_violations: a count equal to the old one is not refused as unmoved

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S16_usn_unmoved_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_a_count_already_at_the_stamp_is_refused_as_unmoved`

Old text:

```
    if new_counter != stamp.counter or new_counter == old_counter:
```

New text:

```
    if new_counter != stamp.counter:
```

### `u955.S17_usn_value_unchecked`

_stamp_violations: any new count is admitted as long as it moved

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S17_usn_value_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_a_planned_row_with_any_of_the_three_wrong_or_unmoved_is_refused[usn-wrong]`

Old text:

```
    if new_counter != stamp.counter or new_counter == old_counter:
```

New text:

```
    if new_counter == old_counter:
```

### `u955.S18_time_value_unchecked`

_stamp_violations: any updated_at is admitted as long as it moved

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S18_time_value_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_a_planned_row_with_any_of_the_three_wrong_or_unmoved_is_refused[time-wrong]`

Old text:

```
    if new_time != stamp.at or new_time == old_time:
```

New text:

```
    if new_time == old_time:
```

### `u955.S19_time_unmoved_admitted`

_stamp_violations: an updated_at left as it was is admitted when it already reads the stamp

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S19_time_unmoved_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 5 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_the_time_a_row_held_is_never_read_against_another_clock_only_left_unmoved[a-later-clock]`
  - `tests/test_rb_removal_stamp.py::test_the_time_a_row_held_is_never_read_against_another_clock_only_left_unmoved[garbage]`
  - `tests/test_rb_removal_stamp.py::test_the_time_a_row_held_is_never_read_against_another_clock_only_left_unmoved[no-offset]`
  - `tests/test_rb_removal_stamp.py::test_the_time_a_row_held_is_never_read_against_another_clock_only_left_unmoved[null]`
  - `tests/test_rb_removal_stamp.py::test_the_time_a_row_held_is_never_read_against_another_clock_only_left_unmoved[the-stamp-s-moment]`

Old text:

```
    if new_time != stamp.at or new_time == old_time:
```

New text:

```
    if new_time != stamp.at:
```

### `u955.S20_stamp_before_plan_admitted`

_stamp_after_plan: a stamp earlier than the plan's reading is admitted

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S20_stamp_before_plan_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_a_stamp_earlier_than_the_plan_is_refused`

Old text:

```
    if stamped < read:
```

New text:

```
    if False:
```

### `u955.S21_unreadable_plan_time_admitted`

_stamp_after_plan: a plan with no readable time is admitted as forward

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S21_unreadable_plan_time_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_a_plan_with_no_readable_time_cannot_say_forward_and_refuses[garbage]`
  - `tests/test_rb_removal_stamp.py::test_a_plan_with_no_readable_time_cannot_say_forward_and_refuses[unread]`

Old text:

```
    if stamped is None or read is None:
```

New text:

```
    if stamped is None:
```

### `u955.S22_plan_time_judged_with_no_row_moved`

collection_removal_violations: the plan's time is judged when nothing was renumbered

- File: `src/cratekit/core/rb_removal.py`
- Source: `u955.json`, row `S22_plan_time_judged_with_no_row_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_removal_stamp.py`, `tests/test_sync_removed.py`, `tests/test_rb_writer_guard.py`
- Collected: 337 against a baseline of 337
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_removal_stamp.py::test_a_removal_that_renumbers_nothing_is_not_held_to_the_plan_s_time`

Old text:

```
    if stamp is not None and planned:
        violations.extend(_stamp_after_plan(before, stamp))
```

New text:

```
    if stamp is not None:
        violations.extend(_stamp_after_plan(before, stamp))
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

### `a32.A6_policy_left_behind`

The commit's policies are left registered after the body, in the shared context manager

- File: `src/cratekit/core/rb_tables.py`
- Source: `a32.json`, row `A6_policy_left_behind`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`, `tests/test_repair_rows.py`
- Collected: 113 against a baseline of 113
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_link.py::test_the_two_acts_write_each_triple_and_move_no_other_column`
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    finally:
        reset_field_policies()
        for policy in was.values():
            register_field_policy(policy)
```

New text:

```
    finally:
        for policy in was.values():
            register_field_policy(policy)
```

### `a32.V4_policy_unrestricted`

The probe policy builder admits a column outside the probe set

- File: `src/cratekit/core/rb_tables.py`
- Source: `a32.json`, row `V4_policy_unrestricted`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_probe_policy_names_exactly_the_columns_asked_and_refuses_any_other`

Old text:

```
    outside = wanted - set(ROW_PROBE_COLUMNS)
    if outside:
```

New text:

```
    outside = wanted - set(ROW_PROBE_COLUMNS)
    if False:
```

### `r923.N18_policy_owns_the_fields`

The defaults policy owns its fields outright instead of filling only an empty one

- File: `src/cratekit/core/rb_tables.py`
- Source: `r923.json`, row `N18_policy_owns_the_fields`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3808 against a baseline of 3808
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_every_default_is_a_real_column_and_none_is_an_analysis_column`

Old text:

```
    fields=MappingProxyType(dict.fromkeys(CONTENT_ROW_DEFAULTS, Ownership.FILL_IF_EMPTY)),
```

New text:

```
    fields=MappingProxyType(dict.fromkeys(CONTENT_ROW_DEFAULTS, Ownership.OWNED)),
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

### `u115.F3_file_id_policy_fill_if_empty`

The file id policy fills only an empty column, so a random id present on the row is never replaced

- File: `src/cratekit/core/rb_tables.py`
- Source: `u115.json`, row `F3_file_id_policy_fill_if_empty`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3808 against a baseline of 3808
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_the_file_id_is_a_real_column_owned_by_its_policy_and_hidden_from_no_guard`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    fields=MappingProxyType({FILE_ID_COLUMN: Ownership.OWNED}),
```

New text:

```
    fields=MappingProxyType({FILE_ID_COLUMN: Ownership.FILL_IF_EMPTY}),
```

### `u115.F4_binding_limit_coefficient`

The binding's id limit is taken as 32 bits rather than 28

- File: `src/cratekit/core/rb_tables.py`
- Source: `u115.json`, row `F4_binding_limit_coefficient`
- Moved: Moved from src/cratekit/core/rb_writer.py to src/cratekit/core/rb_tables.py by U300, which replayed this text there and kept the kill in u300-replay-after-a.json
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_export_collection.py`, `tests/test_genre_retag.py`, `tests/test_head_agreement.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_naming_apply_cli.py`, `tests/test_organize.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`, `tests/test_whitelist_membership.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 3808 against a baseline of 3808
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_file_id_is_a_real_column_owned_by_its_policy_and_hidden_from_no_guard`

Old text:

```
BINDING_ID_LIMIT = 1 << 28
```

New text:

```
BINDING_ID_LIMIT = 1 << 32
```

### `r1890.P11_process_name_typed_in_the_writer`

rb_writer, no longer exempt, compares the running list against a typed process name instead of the shared list

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1890.json`, row `P11_process_name_typed_in_the_writer`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_process_guard.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_guard.py::test_no_module_hardcodes_a_rekordbox_process_name_outside_the_one_list`

Old text:

```
    running = rekordbox_processes_running()
    if running:

```

New text:

```
    running = rekordbox_processes_running()
    if running in ("rekordbox", "rekordboxAgent") or running:

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

### `r663-a.M10_detail_size_pinned`

the detail's size is written as zero whatever the copy measured

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M10_detail_size_pinned`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`

Old text:

```
        detail={"path": str(source), "size": size, "tables_read": list(CANARY_TABLES)},
```

New text:

```
        detail={"path": str(source), "size": 0, "tables_read": list(CANARY_TABLES)},
```

### `r663-a.M3_unlistable_read_as_empty`

a copy whose tables could not be listed is no longer kept apart from one with none, so the None check is dropped

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M3_unlistable_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_file_holding_one_canary_table_or_no_sqlite_keeps_the_canarys_refusal[not-sqlite]`
  - `tests/test_paths_resolved.py::test_setup_leaves_a_damaged_library_to_the_notes_and_doctor`

Old text:

```
        if tables is None or tables.intersection(CANARY_TABLES):
```

New text:

```
        if tables and tables.intersection(CANARY_TABLES):
```

### `r663-a.M4_one_canary_table_not_enough`

a copy holding one of the two canary tables is classified as not a library, so schema drift is sent to setup

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M4_one_canary_table_not_enough`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_file_holding_one_canary_table_or_no_sqlite_keeps_the_canarys_refusal[agentRegistry]`
  - `tests/test_paths_resolved.py::test_a_file_holding_one_canary_table_or_no_sqlite_keeps_the_canarys_refusal[djmdContent]`

Old text:

```
        if tables is None or tables.intersection(CANARY_TABLES):
```

New text:

```
        if tables is None or tables.issuperset(CANARY_TABLES):
```

### `r663-a.M7_message_drops_the_size`

the empty file's message no longer names the size

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M7_message_drops_the_size`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 3 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[empty]`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`

Old text:

```
        what = "is empty, 0 bytes"
```

New text:

```
        what = "is not a database"
```

### `r663-a.M8_message_names_the_copy`

the message names the temporary copy rather than the configured path

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M8_message_names_the_copy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 5 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[empty]`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[foreign]`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`

Old text:

```
        f"the file configured as the rekordbox database, {source}, {what}, so it "
```

New text:

```
        f"the file configured as the rekordbox database, {copied}, {what}, so it "
```

### `r663-a.M9_remedy_restore`

the refusal carries the snapshot restore remedy instead of setup

- File: `src/cratekit/core/rb_writer.py`
- Source: `r663-a.json`, row `M9_remedy_restore`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 3 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_the_copy_names_a_file_holding_none_of_the_canary_tables`
  - `tests/test_paths_resolved.py::test_the_copy_names_an_empty_file_by_its_size_and_its_configured_path`

Old text:

```
        remedy=Remedy.RUN_SETUP,
```

New text:

```
        remedy=Remedy.RESTORE_FROM_SNAPSHOT,
```

### `u185.G5_reading_at_open`

open_db: keep no reading of the subtree as the handle opens

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G5_reading_at_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`, `tests/test_rb_writer_db.py`
- Collected: 75 against a baseline of 75
- Kills: 20 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_handle_with_no_reading_at_open_refuses_rather_than_assuming_nothing_is_there`
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_a_pushed_playlist_moved_out_of_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_write_beside_the_folder_commits_and_leaves_every_row_the_push_wrote`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-added]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-rewritten-to-another-owner]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[playlist-made-inside]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[position-named-at-the-top]`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`
  - `tests/test_foreign_tree.py::test_the_reading_at_open_names_the_push_and_not_a_namesake_below_the_top`
  - `tests/test_rb_writer_db.py::test_a_playlist_creation_commits_because_the_table_is_whitelisted`
  - `tests/test_rb_writer_db.py::test_a_registered_column_write_commits_and_persists`
  - `tests/test_rb_writer_db.py::test_a_registration_widens_the_gate_by_exactly_its_own_fields`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    foreign_tree.remember(db)
    return db
```

New text:

```
    return db
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

### `u267.M10_done_reading_leaks_own`

done_reading: never close a reader's own handle, so every reader of the run that answers a gate leaks one

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M10_done_reading_leaks_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_reader_with_no_shared_read_closes_its_own_handle`
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`

Old text:

```
    if shared is None:
        close_db(db)
```

New text:

```
    if shared is None:
        pass
```

### `u267.M4_handle_opens_every_time`

SharedRead.handle: open again on every call, keeping the last, so the report pays an open per reader and leaks the rest

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M4_handle_opens_every_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize_inspiration.py`, `tests/test_organize_mirror_edits_u204.py`
- Collected: 89 against a baseline of 89
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_report_reads_inspiration_twice_through_one_handle_and_locks_nothing_meanwhile`
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_shared_read_opens_at_its_first_read_and_once`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
        if self._db is None:
            self._db = open_db(
```

New text:

```
        if True:
            self._db = open_db(
```

### `u267.M5_handle_after_close`

SharedRead.handle: drop the refusal after close, so a closed shared read reopens silently

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M5_handle_after_close`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_shared_read_refuses_a_handle_not_its_own_and_a_read_after_close`

Old text:

```
        if self._closed:
            raise _defect("a read handle was asked of a shared read that was already closed")
```

New text:

```
        if False:
            raise _defect("a read handle was asked of a shared read that was already closed")
```

### `u267.M6_release_keeps_rows`

SharedRead.release: keep the identity map, so the next reader takes a row an earlier reader loaded as the row the database holds now

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M6_release_keeps_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_release_forgets_every_row_so_the_next_reader_reads_afresh`

Old text:

```
        db.session.expunge_all()
```

New text:

```
        db.session.flush()
```

### `u267.M7_release_any_handle`

SharedRead.release: drop the refusal of a handle that is not its own

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M7_release_any_handle`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_shared_read_refuses_a_handle_not_its_own_and_a_read_after_close`

Old text:

```
        if db is not self._db:
            raise _defect("a handle that is not the shared read's own was released through it")
```

New text:

```
        if False:
            raise _defect("a handle that is not the shared read's own was released through it")
```

### `u267.M8_close_closes_nothing`

SharedRead.close: forget the handle without close_db, so its engine and pooled connection stay open

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M8_close_closes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_shared_read_opens_at_its_first_read_and_once`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
        if db is not None:
            close_db(db)
```

New text:

```
        if db is not None:
            pass
```

### `u267.M9_done_reading_closes_shared`

done_reading: close the handle whatever its owner, so the first reader closes the shared handle under the rest

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M9_done_reading_closes_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`
- Collected: 149 against a baseline of 149
- Kills: 60 (killed)
- Killed:
  - `tests/test_organize.py::test_a_label_playlist_is_the_label_steps_and_a_set_the_archives`
  - `tests/test_organize.py::test_a_mark_put_back_is_no_mark_and_the_playlist_stays`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[False]`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[True]`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_playlist_of_the_sets_name_outside_inspiration_or_removed_proves_nothing`
  - `tests/test_organize.py::test_a_playlist_of_yours_already_in_a_folder_of_yours_is_not_listed`
  - `tests/test_organize.py::test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine`
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`
  - `tests/test_organize.py::test_a_set_archived_by_its_inspiration_proof_stays_archived_once_that_playlist_goes`
  - `tests/test_organize.py::test_a_set_found_prefixed_by_the_migration_is_still_filed_by_the_archive`
  - `tests/test_organize.py::test_a_set_in_its_folder_with_its_built_title_is_taken_and_not_moved`
  - ... and 45 more, see the JSON sidecar

Old text:

```
    if shared is None:
        close_db(db)
    else:
        shared.release(db)
```

New text:

```
    close_db(db)
```

### `u27-round-8-independent.W2_composite_wrong_file`

COMPOSITE for W2: the canary names a file that is not the one it opened

- File: `src/cratekit/core/rb_writer.py`
- Source: `u27-round-8-independent.json`, row `W2_composite_wrong_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        named = path if path is not None else handle_path(db)
```

New text:

```
        named = (str(path) + "-not-this-file") if path is not None else handle_path(db)
```

### `u27-round-8-independent.W3_canary_no_name_the_database`

Drop the name_the_database hand-off in the canary, so a chmod 000 database is unclassifiable

- File: `src/cratekit/core/rb_writer.py`
- Source: `u27-round-8-independent.json`, row `W3_canary_no_name_the_database`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if named is not None:
            name_the_database(exc, named)
```

New text:

```
(empty)
```

### `u27-round-8-independent.W5_canary_message_no_path`

Reword the canary refusal so its sentence no longer names the database file

- File: `src/cratekit/core/rb_writer.py`
- Source: `u27-round-8-independent.json`, row `W5_canary_message_no_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            f"the rekordbox database{where} opened but could not be read as "
            f"expected: {exc}",
```

New text:

```
            f"the rekordbox database could not be read as expected after it "
            f"opened: {exc}",
```

### `u285.M1_seam_installs`

open_db: drop the install, so a handle reads with the binding's own conversion and a zero dated push fails its row west of UTC

- File: `src/cratekit/core/rb_writer.py`
- Source: `u285.json`, row `M1_seam_installs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_dates.py`, `tests/test_organize.py`, `tests/test_rebuild.py`, `tests/test_foreign_tree.py`
- Collected: 290 against a baseline of 290
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[EST5EDT,M3.2.0,M11.1.0]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[JST-9]`
  - `tests/test_rb_dates.py::test_a_commit_leaves_the_pushed_nodes_xml_timestamps_and_still_syncs_its_own[UTC0]`
  - `tests/test_rb_dates.py::test_a_handle_reads_the_whole_tree_over_a_zero_dated_push_and_writes_nothing`
  - `tests/test_rb_dates.py::test_the_open_seam_installs_the_wrapper`

Old text:

```
    rb_dates.install()

```

New text:

```
    pass

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

### `u953.M5_writable_library_asks_only_the_state_directory`

_assert_library_is_writable drops the configured database from its one condition, so a library with a database and no state directory is refused

- File: `src/cratekit/core/reconcile.py`
- Source: `u953.json`, row `M5_writable_library_asks_only_the_state_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_rebuild.py`
- Collected: 271 against a baseline of 271
- Kills: 10 (killed)
- Killed:
  - `tests/test_restore.py::test_a_disposition_is_not_lost_under_concurrency`
  - `tests/test_restore.py::test_abandoning_a_run_is_never_gated_on_convergence`
  - `tests/test_restore.py::test_blocking_4_a_rebuilt_tree_does_not_pay_for_every_later_restore`
  - `tests/test_restore.py::test_blocking_4_recording_one_restore_twice_is_still_idempotent`
  - `tests/test_restore.py::test_blocking_4_two_restores_producing_the_same_triple_are_two_markers`
  - `tests/test_restore.py::test_recording_the_same_marker_twice_does_not_reopen_a_closed_one`
  - `tests/test_restore.py::test_retraction_touches_the_transient_latch_and_nothing_else`
  - `tests/test_restore.py::test_round2_a_close_against_a_husk_is_refused_by_the_volume_gate`
  - `tests/test_restore.py::test_round2_the_readers_still_answer_identically_on_a_gone_library`
  - `tests/test_restore.py::test_the_reconciliation_record_survives_eight_concurrent_writers`

Old text:

```
    if config.library_state_dir(cfg).is_dir() or Path(cfg.library.db_path).exists():
```

New text:

```
    if config.library_state_dir(cfg).is_dir():
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

### `u27-restore-cli-independent.X6_the_rekordbox_guard_itself_is_neutered`

What the process-lister zeros DO leave held: make the restore engine's rekordbox-closed assertion return without asking. Paired with I_A6 and I_A7, which stopped threading that guard's injected seam and killed nothing

- File: `src/cratekit/core/restore.py`
- Source: `u27-restore-cli-independent.json`, row `X6_the_rekordbox_guard_itself_is_neutered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_a_restore_refuses_while_rekordbox_holds_the_database`

Old text:

```
    running = processes.rekordbox_processes_running(lister=process_lister)
    if not running:
        return
```

New text:

```
    running = processes.rekordbox_processes_running(lister=process_lister)
    if running or not running:
        return
```

### `u95-a.A1_never_rerooted`

_rooted hands every session its configuration back unchanged, which is main's state: a bare-metal session resolves from the configured root again

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A1_never_rerooted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Moved: U953 moved the preflight's read, rebase and checks into the shared _spendable_capture helper, so rebasing onto the recorded root itself at the preflight's call is the same un-rebased manifest asked of the dead volume
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 506 against a baseline of 506
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`

Old text:

```
    _spendable_capture(decided.capture_root, recorded_root, Path(cfg.library.root))
```

New text:

```
    _spendable_capture(decided.capture_root, recorded_root, recorded_root)
```

### `u95-a.A8_run_not_rooted`

run resolves from the caller's configuration while plan resolves from the session, the two sources for one answer R-20 forbids

- File: `src/cratekit/core/restore.py`
- Source: `u95-a.json`, row `A8_run_not_rooted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Collected: 506 against a baseline of 506
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
- Moved: U953 folded this refusal's refuse call into the _defect builder, so the membership test now guards raise _defect and disabling it is the same admitted step
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 506 against a baseline of 506
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_step_aimed_at_the_authorised_directory_itself_is_refused`

Old text:

```
        if step.target not in allowed:
            raise _defect(
```

New text:

```
        if False:
            raise _defect(
```

### `u95-c.C5_staging_authorisation_removed`

Inside the guard, drop the authorisation of the staging directory and leave only the store rule

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C5_staging_authorisation_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 506 against a baseline of 506
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

### `u95-c.C6_staging_store_rule_removed`

Inside the guard, drop the store rule, so an authorised staging directory such as the library root hands the closing prune the directory ABOVE the library

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C6_staging_store_rule_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 506 against a baseline of 506
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[a-directory-in-the-library]`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-library-root]`
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-staging-store-itself]`

Old text:

```
    if pre_restore_root.parent != store:
```

New text:

```
    if False:
```

### `u95-c.C7_staging_store_itself_admitted`

A nearby value: admit the store itself as the staging directory, which makes the prune run one level up, inside the database directory

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C7_staging_store_itself_admitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 506 against a baseline of 506
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_staging_inside_the_library_but_not_under_its_store_is_refused[the-staging-store-itself]`

Old text:

```
    if pre_restore_root.parent != store:
```

New text:

```
    if pre_restore_root.parent != store and pre_restore_root != store:
```

### `u95-c.C8_plan_root_assertion_removed`

plan drops its assertion on the rooted root, which is also where it asks whether the session is still open and is a recovery

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `C8_plan_root_assertion_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 506 against a baseline of 506
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_u95_a_library_session_still_refuses_a_configuration_for_another_library`

Old text:

```
    assert_gates_are_open(held, writing=cfg.library.root)
    _assert_rekordbox_closed(process_lister)
    record = session.read_record(session_id, cfg)
```

New text:

```
    _assert_rekordbox_closed(process_lister)
    record = session.read_record(session_id, cfg)
```

### `u95-c.S1_authorises_everything`

EXISTING GUARD, fixed sample: Held.authorises_path answers yes to every path, which is the original bypass

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `S1_authorises_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 506 against a baseline of 506
- Kills: 7 (killed)
- Killed:
  - `tests/test_restore.py::test_blocking_1_a_bare_metal_session_cannot_be_spent_on_the_library_it_refused`
  - `tests/test_restore.py::test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name`
  - `tests/test_restore.py::test_u95_a_library_session_still_refuses_a_configuration_for_another_library`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`
  - `tests/test_restore.py::test_u95_plan_checks_its_own_answer_rather_than_trusting_the_derivation`
  - `tests/test_restore.py::test_u95_the_staging_directory_is_a_write_location_and_is_authorised_too`

Old text:

```
        return where == root or root in where.parents
```

New text:

```
        return True
```

### `u95-c.S2_issued_terms_not_compared`

EXISTING GUARD, fixed sample: still_open stops comparing the claim to what the guard issued, so a live token can be rebuilt around another directory

- File: `src/cratekit/core/restore.py`
- Source: `u95-c.json`, row `S2_issued_terms_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 506 against a baseline of 506
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_round2_a_held_rebuilt_around_a_live_token_is_refused`

Old text:

```
        if terms != (self.issued_by, str(self.authorises), str(self.lock.absolute())):
            return False
```

New text:

```
(empty)
```

### `u953.M13_spendable_capture_skips_the_verdict`

_spendable_capture no longer asks the capture's verdict, so an unverified capture is planned and spent

- File: `src/cratekit/core/restore.py`
- Source: `u953.json`, row `M13_spendable_capture_skips_the_verdict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_a_capture_that_failed_its_integrity_check_is_never_restored_from`
  - `tests/test_restore.py::test_blocking_2_a_capture_whose_database_is_gone_refuses_before_the_log_is_touched`

Old text:

```
    snapshot.assert_verified(captured)
```

New text:

```
    pass
```

### `r1890.P13_convergence_fallback_filter_in_restore_perform`

restore_perform, where the tree shortness handoff now lives, filters the unconverged tree kind core.convergence owns, the fallback the build must have deleted

- File: `src/cratekit/core/restore_perform.py`
- Source: `r1890.json`, row `P13_convergence_fallback_filter_in_restore_perform`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`
- Collected: 159 against a baseline of 159
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_the_convergence_fallback_expires_the_moment_both_modules_share_a_build`

Old text:

```
def _restore():
    """``restore`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import restore

    return restore

```

New text:

```
def _restore():
    """``restore`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import restore

    return restore


_SKIPPED = ("Kind.UNCONVERGED_TREE",)

```

### `u300.S19_replace_file_local`

the perform step replaces a file through the part's own _replace_file

- File: `src/cratekit/core/restore_perform.py`
- Source: `u300.json`, row `S19_replace_file_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_blocking_2_a_failure_mid_restore_is_a_structured_refusal`
  - `tests/test_restore.py::test_round6_a_retry_after_a_partial_failure_still_runs`

Old text:

```
            _restore()._replace_file(step.source, step.target)
```

New text:

```
            _replace_file(step.source, step.target)
```

### `u300.S20_stage_aside_local`

the perform step stages a companion aside through the part's own helper

- File: `src/cratekit/core/restore_perform.py`
- Source: `u300.json`, row `S20_stage_aside_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore.py::test_round6_the_performing_backstop_names_what_it_already_moved`

Old text:

```
            _restore()._stage_companion_aside(step.target, decided.pre_restore_root)
```

New text:

```
            _stage_companion_aside(step.target, decided.pre_restore_root)
```

### `r592-a.A1_occupancy_guard_removed`

assert_recovery_target: find nothing occupied whatever the target holds, so a library whose database sits where this one lands is replaced unasked

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A1_occupancy_guard_removed`
- Moved: Anchored where u300-replay-after-c.json replayed it: the same text, now in src/cratekit/core/restore_recovery.py, was in src/cratekit/core/restore.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    existing = [entry for entry in recovered_database_fileset(cfg, where) if entry.exists()]
```

New text:

```
    existing = []
```

### `r592-a.A2_database_dropped_from_fileset`

recovered_database_fileset: return the companions only, so a database already at the landing path is not an occupied target

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A2_database_dropped_from_fileset`
- Moved: Anchored where u300-replay-after-c.json replayed it: the same text, now in src/cratekit/core/restore_recovery.py, was in src/cratekit/core/restore.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    return (landing, *companions)
```

New text:

```
    return companions
```

### `r592-a.A3_companions_dropped_from_fileset`

recovered_database_fileset: return the database only, so a lone write-ahead log the database half would clear is not an occupied target

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A3_companions_dropped_from_fileset`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`

Old text:

```
    return (landing, *companions)
```

New text:

```
    return (landing,)
```

### `r592-a.A4_fileset_not_rebased`

recovered_database_fileset: land the database at its bare name at the top of the target for every layout, so the guard tests a path the transfer never writes

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A4_fileset_not_rebased`
- Moved: Anchored where u300-replay-after-c.json replayed it: the same text, now in src/cratekit/core/restore_recovery.py, was in src/cratekit/core/restore.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
        landing = target / database.relative_to(cfg.library.root)
    except ValueError:
```

New text:

```
        landing = target / database.name
    except ValueError:
```

### `r592-a.A5_replacing_existing_inverted`

assert_recovery_target: refuse an occupied target only when it WAS named for replacement

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A5_replacing_existing_inverted`
- Moved: Anchored where u300-replay-after-c.json replayed it: the same text, now in src/cratekit/core/restore_recovery.py, was in src/cratekit/core/restore.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 8 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_never_reads_the_capture_the_refused_library_holds`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    if existing and not replacing_existing:
```

New text:

```
    if existing and replacing_existing:
```

### `r592-a.A6_old_suffix_rule_restored`

assert_recovery_target: put the recursive any-database rule back, the behaviour R-592 records, so every interrupted recovery is refused on rerun

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A6_old_suffix_rule_restored`
- Moved: Anchored where u300-replay-after-c.json replayed it: the same text, now in src/cratekit/core/restore_recovery.py, was in src/cratekit/core/restore.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_opens_over_databases_it_would_not_replace`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`

Old text:

```
    existing = [entry for entry in recovered_database_fileset(cfg, where) if entry.exists()]
```

New text:

```
    existing = sorted(entry for entry in where.rglob("*.db") if entry.is_file())
```

### `r592-a.A7_companion_suffix_wrong`

recovered_database_fileset: name each companion with a dot before its suffix, master.db.-wal, so no real companion is ever found

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A7_companion_suffix_wrong`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`

Old text:

```
        landing.with_name(landing.name + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    return (landing, *companions)
```

New text:

```
        landing.with_name(landing.name + "." + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    return (landing, *companions)
```

### `r592-a.A8_sample_stub_check_beside`

SAMPLE, existing guard: assert_recovery_target refuses only a stub at or under the configured root, not the suffixed name beside it

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A8_sample_stub_check_beside`
- Moved: Moved from src/cratekit/core/restore.py to src/cratekit/core/restore_recovery.py by U300, which replayed this text there and kept the kill in u300-replay-after-c.json
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_the_stubs_beside_and_beneath_the_mount_point[library 1-why1]`
  - `tests/test_restore.py::test_round2_the_real_mount_probe_is_armed_by_default`

Old text:

```
    if (inside_configured or beside_configured) and not probe(where):
```

New text:

```
    if inside_configured and not probe(where):
```

