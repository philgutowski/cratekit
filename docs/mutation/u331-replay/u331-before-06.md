# Mutation table: u331-before-06

Measured by `scripts/mutate.py` on 2026-11-23 22:11 UTC, branch `HEAD` at `04a5f695`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22808 collected. pytest invocations for this batch: 57.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 21:16 UTC for commit `04a5f695bb07`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 55, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 162 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22808 against 22808. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u104-e.E5_install_hint_steps` | `src/cratekit/core/binary_refusal.py` | user | 3 file(s) | 113 | 4 | killed |
| `r1372.K10_carried_read_error_silent` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 2 | killed |
| `r1372.K11_carried_place_unchecked` | `src/cratekit/core/held_plan.py` | maintainer | 7 file(s) | 227 | 1 | killed |
| `r1372.K12_carried_run_unchecked` | `src/cratekit/core/held_plan.py` | maintainer | 7 file(s) | 227 | 1 | killed |
| `r1372.K14_unlistable_read_as_none` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 1 | killed |
| `r1372.K15_let_go_keeps` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 5 | killed |
| `r1372.K25_name_filter_gone` | `src/cratekit/core/held_plan.py` | maintainer | 1 file(s) | 22808 | 0 (promoted) | zero |
| `r1372.K2_carry_writes_nothing` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 15 | killed |
| `r1372.K3_carry_empty_steps` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 10 | killed |
| `r1372.K5_carried_under_held_plans` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 3 | killed |
| `u209.H4_load_digest_unchecked` | `src/cratekit/core/held_plan.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.H6_load_age_unchecked` | `src/cratekit/core/held_plan.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.H7_hold_equality_unchecked` | `src/cratekit/core/held_plan.py` | user | 1 file(s) | 22808 | 0 (promoted) | zero |
| `u225.M12_age_unchecked` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 1 | killed |
| `u225.M13_unreadable_silent` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 2 | killed |
| `r289-b.D1_no_chunking` | `src/cratekit/core/jobs.py` | user | 30 file(s) | 2397 | 1 | killed |
| `r289-b.D3_unknown_name_gets_a_state` | `src/cratekit/core/jobs.py` | user | 30 file(s) | 2397 | 2 | killed |
| `r290-author.J1_blocked_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2523 | 49 | killed |
| `r290-author.J2_blocked_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2523 | 48 | killed |
| `r290-author.J3_closed_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2523 | 111 | killed |
| `r290-author.J4_predicate_narrowed_to_failed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2523 | 30 | killed |
| `r290-author.J5_causeless_block_returns` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2523 | 1 | killed |
| `r290-author.J6_causeless_block_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2523 | 1 | killed |
| `r290-author.J7_cancelled_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2523 | 26 | killed |
| `r290-author.S11_tagging_shell_call_removed` | `src/cratekit/core/jobs.py` | user | 5 file(s) | 347 | 48 | killed |
| `r390-a.A1_retry_re_arms_unconditionally` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 0 | 0 | error |
| `r390-a.A2_retry_refuses_any_closed_job_with_a_cause` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 296 | 9 | killed |
| `r390-a.A3_a_failed_job_with_no_cause_is_refused` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `r390-a.A4_refusal_drops_the_permanent_reasons` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `r390-a.A5_refusal_drops_the_inner_cause` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 210 | 4 | killed |
| `r390-b.B6_envelope_drops_the_reasons` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `u140.B3_refreeze_any_state` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B4_refreeze_writes_nothing_new` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 29 | 7 | killed |
| `u227.R16_join_state` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 130 | 5 | killed |
| `u227.R17_join_held` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 130 | 1 | killed |
| `u227.R18_join_blank` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 130 | 1 | killed |
| `u235.S1_enqueue_ignores_a_given_job_id` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 26 | killed |
| `u270.J1_claim_batch_size_floor` | `src/cratekit/core/jobs.py` | maintainer | 3 file(s) | 136 | 1 | killed |
| `u270.J2_claim_batch_order` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 165 | 22 | killed |
| `u298.H16_reported_extra_under_progress` | `src/cratekit/core/jobs.py` | user | 18 file(s) | 1391 | 121 | killed |
| `u298.H17_reported_cause` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 1 | killed |
| `u298.H18_staged_path_cleared` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 184 | 1 | killed |
| `u298.H19_by_ordinal_numeric` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 184 | 1 | killed |
| `u298.H20_by_ordinal_filters` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 184 | 1 | killed |
| `u298.H21_advance_refuses_empty` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 129 | 3 | killed |
| `u298.H22_resumed_raises_state` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 184 | 2 | killed |
| `u298.H23_artifacts_names_differ` | `src/cratekit/core/jobs.py` | maintainer | 1 file(s) | 100 | 1 | killed |
| `u301.J1_job_row_answers_none` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 187 | 2 | killed |
| `u301.J2_release_claims_any_driver` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 104 | 1 | killed |
| `u46-round-2.M2_resume_does_not_drive` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 59 | 15 | killed |
| `u56-catalogue-searcher-and-tag-workers.R34_empty_job_is_driven` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R35_extra_rides_beside_progress` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 47 | killed |
| `u56-catalogue-searcher-and-tag-workers.R37_artifact_named_by_item_id` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R38_staging_not_cleared` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 102 | 1 | killed |
| `u57-recognition-and-items.C12_stray_file_sorted` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 67 | 1 | killed |
| `r770-b.B2_gate_asked_before_the_acknowledgment` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 77 | 2 | killed |
| `r770-b.B3_an_abort_writes` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 77 | 2 | killed |
| `u120.C1_no_skip_note` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 13 | 2 | killed |
| `u126.P3_gate_fact` | `src/cratekit/intake/land_native.py` | user | 10 file(s) | 438 | 4 | killed |
| `u127.L1_screen_line_blind` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 1 | killed |
| `u127.L2_items_carry_no_vox` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 6 | killed |
| `u127.L3_totals_from_writer` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 1 | killed |
| `u127.L4_missing_unsaid` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 1 | killed |
| `u127.L5_unscored_unsaid` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 1 | killed |
| `u127.L7_land_warnings_unsaid` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 7 | killed |
| `u128-b.N3_native_owned_not_found` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 3 | killed |
| `u128.L2_native_warning_unsaid` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 2 | killed |
| `u129-author.A4_archive_raise_fails_landing` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 76 | 2 | killed |
| `u129-author.A5_archive_return_discarded` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 76 | 2 | killed |
| `u135.A3_found_vs_made_collapsed` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 9 | 6 | killed |
| `u146-c.L3_gate_asked_for_nothing` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 12 | 2 | killed |
| `u146-c.L4_missing_source_refuses` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u153.L1_facts_colour_count` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 25 | 1 | killed |
| `u153.L3_notes_colour_skipped` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 13 | 1 | killed |
| `u157.L1_selection_counts` | `src/cratekit/intake/land_native.py` | user | 5 file(s) | 186 | 1 | killed |
| `u157.L2_blocked_unnamed` | `src/cratekit/intake/land_native.py` | user | 3 file(s) | 126 | 1 | killed |
| `u161.L1_landing_pins_nothing` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u161.P6_screen_drops_path` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 44 | 2 | killed |
| `u165.L1_bridge_skip` | `src/cratekit/intake/land_native.py` | user | 4 file(s) | 98 | 2 | killed |
| `u165.L2_land_only` | `src/cratekit/intake/land_native.py` | user | 4 file(s) | 98 | 3 | killed |
| `u165.L4_files_into` | `src/cratekit/intake/land_native.py` | user | 4 file(s) | 98 | 2 | killed |
| `u166.A11_warning_names_batch` | `src/cratekit/intake/land_native.py` | user | 7 file(s) | 185 | 3 | killed |
| `u177.C4_flag_ignored` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 46 | 4 | killed |
| `u181.L1_half_is_a_warning` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u181.L2_coefficient` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u307.R22_colour_notes_drop_held` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 25 | 2 | killed |
| `u319.M8_ok_on_any_field` | `src/cratekit/intake/land_native.py` | user | 3 file(s) | 88 | 2 | killed |
| `u319.M9_warning_drops_the_short_path` | `src/cratekit/intake/land_native.py` | user | 3 file(s) | 74 | 1 | killed |
| `r1289.M10_warning_ready_filter` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 1 | killed |
| `r1289.M11_warning_absent` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `r1289.M12_warning_promise` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `r1289.M13_warning_names` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `r227.C6_composed_limit_spelled` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M5_unwired` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M6_no_append` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M7_note_before_describe` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r504-b.B10_check_no_numbers` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B7_sync_drops_short` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B8_check_passes` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B9_all_withheld_says_no_hearts` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r515-operator.S13_sweep_no_warning` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r835-c.S2_sync_hands_the_ledger_to_the_sweep_again` | `src/cratekit/sync/cli.py` | user | 4 file(s) | 298 | 1 | killed |
| `r837-a.A17_sweep_hand_off` | `src/cratekit/sync/cli.py` | user | 5 file(s) | 361 | 1 | killed |
| `u109-a.A1_plan_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 9 | killed |
| `u109-a.A2_guided_empty` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 6 | killed |
| `u109-a.A3_no_check_row` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u109-a.A4_summary_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u109-a.A5_gate_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A6_refusal_step_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u109-a.A7_refusal_step_first` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A8_row_reworded` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u147-c.M19_sweep_handoff` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `u73-c.C3_next_only_with_intake_jobs` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 5 | killed |
| `u73-c.C4_next_counts_intake_jobs_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u73-c.C5_next_check_row` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B10_refused_check_status` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u74-b.B11_gate_screen` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B12_next_step_outbound_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B1_source_id_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 9 | killed |
| `u74-b.B2_compose_skips_inbound` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 16 | killed |
| `u74-b.B3_queue_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u74-b.B4_filed_outbound_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 10 | killed |
| `u74-b.B5_inbound_refusal_not_counted` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B6_inbound_warning` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B7_block_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 13 | killed |
| `u74-b.B8_check_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 10 | killed |
| `u74-b.B9_check_wording` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A10_export_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 15 | killed |
| `u74.A11_queue_not_bound` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 17 | killed |
| `u74.A12_run_id_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u74.A3_handler_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A4_source_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A5_library_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A6_open_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u74.A7_in_flight_guard` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u74.A8_empty_guard` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 4 | killed |
| `u74.A9_listing_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 19 | killed |
| `u210.R16_forecast_line` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 2 | killed |
| `u210.R9_skip_done` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 1 | killed |
| `u220.P5_no_stop_after_loop` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 306 | 9 | killed |
| `u226.M23_totals_no_read_backs` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 267 | 1 | killed |
| `u304.S12_pair_cli_offers_file_identity` | `src/cratekit/sync/pair_cli.py` | maintainer | 2 file(s) | 71 | 2 | killed |
| `u304.S13_pair_cli_offers_scope_account` | `src/cratekit/sync/pair_cli.py` | maintainer | 1 file(s) | 34 | 1 | killed |
| `r1372.K22_mark_guard_gone` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 2 | killed |
| `r1372.K23_mark_guard_inclusive` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 1 | killed |
| `r1372.K6_reader_ignores_carried` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 7 | killed |
| `r1372.K7_copy_never_gives_way` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 1 | killed |
| `r1372.K8_copy_gives_way_to_any_plan` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 1 | killed |
| `r1372.K9_carried_unread_unsaid` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 1 | killed |
| `r1376.F13_snapshot_guard_inclusive` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 34 | killed |
| `r1376.F1_first_stop_none` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 7 | killed |
| `r1383.M19_sampled_mirrors_empty` | `src/cratekit/sync/pair_read.py` | user | 3 file(s) | 137 | 11 | killed |
| `r1383.M1_scan_drops_unread` | `src/cratekit/sync/pair_read.py` | user | 4 file(s) | 183 | 5 | killed |
| `r1385.M11_name_fallback` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 1 | killed |
| `r1385.M15_failed_jobs_hold` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 2 | killed |
| `r1385.M1_no_job_holds_anything` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 13 | killed |
| `u225.M14_superseded_unchecked` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 4 | killed |
| `u229.M10_file_isrc_fallback` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 10 | killed |
| `u229.M11_mirror_cache` | `src/cratekit/sync/pair_read.py` | maintainer | 8 file(s) | 292 | 1 | killed |
| `u229.M12_own_mirrors_bypass_cache` | `src/cratekit/sync/pair_read.py` | maintainer | 8 file(s) | 292 | 1 | killed |
| `u229.M2_wide_landed_reads_own_only` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.M6_config_error_not_caught` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.M9_landed_dedup` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 1 | killed |

## Zero rows and what they owe

- `r1372.K25_name_filter_gone` (maintainer facing): maintainer facing, composite not required
- `u209.H7_hold_equality_unchecked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u104-e.E5_install_hint_steps`

Drop the install step from the yt-dlp-missing refusal, so a missing binary refuses without saying how to get it

- File: `src/cratekit/core/binary_refusal.py`
- Source: `u104-e.json`, row `E5_install_hint_steps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 113 against a baseline of 113
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_missing_yt_dlp_refuses_a_url_with_the_install_hint`
  - `tests/test_acquire_fallback.py::test_a_broken_override_is_its_own_refusal`
  - `tests/test_acquire_fallback.py::test_a_missing_binary_refuses_with_the_install_hint`
  - `tests/test_acquire_fallback_fetch.py::test_a_missing_yt_dlp_parks_the_job_rather_than_failing_every_item`

Old text:

```
            if hint is not None
            else ()
        ),
        scope=Scope.RUN,
```

New text:

```
            if hint is None
            else ()
        ),
        scope=Scope.RUN,
```

### `r1372.K10_carried_read_error_silent`

carried: a record that cannot be read is skipped without a word

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K10_carried_read_error_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_record_that_cannot_be_read_is_named_never_read_as_no_write`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`

Old text:

```
            problems.append(
                f"run {run_id}'s carried steps could not be read ({type(exc).__name__}: {exc})"
            )
            continue
```

New text:

```
            continue
```

### `r1372.K11_carried_place_unchecked`

carried: a record not at the place its run and key name is read

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K11_carried_place_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_record_that_cannot_be_read_is_named_never_read_as_no_write`

Old text:

```
            or carried_path(run_id, key) != one
```

New text:

```
            or False
```

### `r1372.K12_carried_run_unchecked`

carried: a record naming another run than its file is read under its file's run

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K12_carried_run_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_record_naming_another_run_is_named`

Old text:

```
            raw.get("run_id") != run_id
            or not isinstance(key, str)
```

New text:

```
            not isinstance(key, str)
```

### `r1372.K14_unlistable_read_as_none`

carried: a directory that cannot be listed reads as no record

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K14_unlistable_read_as_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_directory_that_cannot_be_listed_is_named_never_read_as_none`

Old text:

```
    except OSError as exc:
        return [], [f"the carried steps could not be listed ({type(exc).__name__}: {exc})"]
```

New text:

```
    except OSError:
        return [], []
```

### `r1372.K15_let_go_keeps`

let_go: the record is never removed

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K15_let_go_keeps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_is_kept_from_prune_and_release_and_let_go_only_when_asked`
  - `tests/test_sync_pair_stopped.py::test_two_items_of_one_run_are_carried_apart`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_run_that_finished_the_pair_without_moving_its_snapshot_keeps_nothing_of_its_own`

Old text:

```
        carried_path(run_id, key).unlink(missing_ok=True)
```

New text:

```
        carried_path(run_id, key).exists()
```

### `r1372.K25_name_filter_gone`

carried: every entry in the directory is read, a leftover temporary file among them

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K25_name_filter_gone`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 22808 against a baseline of 22808
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            one for one in carried_dir().iterdir() if one.name.endswith(".json")
```

New text:

```
            one for one in carried_dir().iterdir()
```

### `r1372.K2_carry_writes_nothing`

carry: the record is built and never written

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K2_carry_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_is_kept_from_prune_and_release_and_let_go_only_when_asked`
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_reads_back_as_its_runs_steps_for_that_item_whatever_its_age`
  - `tests/test_sync_pair_stopped.py::test_a_carried_record_that_cannot_be_read_is_named_never_read_as_no_write`
  - `tests/test_sync_pair_stopped.py::test_a_carry_that_cannot_be_written_raises`
  - `tests/test_sync_pair_stopped.py::test_two_items_of_one_run_are_carried_apart`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_run_that_finished_the_pair_without_moving_its_snapshot_keeps_nothing_of_its_own`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
    config.atomic_write_bytes(payload, carried_path(steps.run_id, key))
```

New text:

```
    payload = payload
```

### `r1372.K3_carry_empty_steps`

carry: the record keeps an empty item, so its ordering detail is lost

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K3_carry_empty_steps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_reads_back_as_its_runs_steps_for_that_item_whatever_its_age`
  - `tests/test_sync_pair_stopped.py::test_two_items_of_one_run_are_carried_apart`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
        "steps": dict(steps.done.get(str(key), {})),
```

New text:

```
        "steps": {},
```

### `r1372.K5_carried_under_held_plans`

carried_dir: the records are kept beside the held plans, where prune takes them

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K5_carried_under_held_plans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_is_kept_from_prune_and_release_and_let_go_only_when_asked`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go`

Old text:

```
    return config.state_path(STATE_KEY) / CARRIED_DIR
```

New text:

```
    return config.state_path(STATE_KEY)
```

### `u209.H4_load_digest_unchecked`

held_plan.load: accept a plan that does not digest as the digest held beside it

- File: `src/cratekit/core/held_plan.py`
- Source: `u209.json`, row `H4_load_digest_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_held_plan_of_another_kind_or_run_is_no_plan`

Old text:

```
    if actual != held:
```

New text:

```
    if False:
```

### `u209.H6_load_age_unchecked`

held_plan.load: read back a held plan older than it is kept

- File: `src/cratekit/core/held_plan.py`
- Source: `u209.json`, row `H6_load_age_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_held_plan_older_than_it_is_kept_is_planned_again`

Old text:

```
    if age > KEEP.total_seconds():
```

New text:

```
    if False:
```

### `u209.H7_hold_equality_unchecked`

held_plan.hold: hold a plan that does not read back equal to itself

- File: `src/cratekit/core/held_plan.py`
- Source: `u209.json`, row `H7_hold_equality_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 22808 against a baseline of 22808
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if decode(encoded, registry) != plan:
```

New text:

```
        if False:
```

### `u225.M12_age_unchecked`

recorded_steps: a record older than a held plan is kept is still read

- File: `src/cratekit/core/held_plan.py`
- Source: `u225.json`, row `M12_age_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_record_older_than_a_held_plan_is_kept_is_none`

Old text:

```
            if one.stat().st_mtime < cutoff:
                continue
            raw = json.loads(one.read_text())
```

New text:

```
            raw = json.loads(one.read_text())
```

### `u225.M13_unreadable_silent`

recorded_steps: a record that cannot be read is dropped unnamed

- File: `src/cratekit/core/held_plan.py`
- Source: `u225.json`, row `M13_unreadable_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_every_kept_runs_steps_are_read_and_an_unreadable_one_is_named`
  - `tests/test_sync_pair_stopped_order.py::test_a_runs_steps_that_cannot_be_read_are_named_never_read_as_no_write`

Old text:

```
            problems.append(
                f"run {run_id}'s steps could not be read ({type(exc).__name__}: {exc})"
            )
```

New text:

```
            pass
```

### `r289-b.D1_no_chunking`

Ask about every name in one statement, past the parameter limit

- File: `src/cratekit/core/jobs.py`
- Source: `r289-b.json`, row `D1_no_chunking`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2397 against a baseline of 2397
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_states_of_answers_past_the_parameter_limit_of_one_statement`

Old text:

```
_ID_CHUNK = 500
```

New text:

```
_ID_CHUNK = 1_000_000
```

### `r289-b.D3_unknown_name_gets_a_state`

Answer for every name asked about, inventing queued for the unknown ones

- File: `src/cratekit/core/jobs.py`
- Source: `r289-b.json`, row `D3_unknown_name_gets_a_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2397 against a baseline of 2397
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_states_of_answers_for_the_names_it_knows_and_omits_the_rest`
  - `tests/test_jobs.py::test_states_of_answers_past_the_parameter_limit_of_one_statement`

Old text:

```
    found: dict[str, JobState] = {}
    wanted = list(job_ids)
```

New text:

```
    wanted = list(job_ids)
    found: dict[str, JobState] = dict.fromkeys(wanted, JobState.QUEUED)
```

### `r290-author.J1_blocked_branch_removed`

Skip the blocked branch of raise_for_state, so a parked job falls through to the closed predicate that cannot see it, which is R-290 itself

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J1_blocked_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2523 against a baseline of 2523
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
- Collected: 2523 against a baseline of 2523
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
- Collected: 2523 against a baseline of 2523
- Kills: 111 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_a_taken_target_name_fails_the_item_and_keeps_the_written_head_in_the_title`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - ... and 96 more, see the JSON sidecar

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
- Collected: 2523 against a baseline of 2523
- Kills: 30 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command`
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
  - ... and 15 more, see the JSON sidecar

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

### `r290-author.J5_causeless_block_returns`

Return for a blocked job that records no reason, reading a missing reason as a missing problem

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J5_causeless_block_returns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2523 against a baseline of 2523
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_blocked_job_recording_no_reason_is_still_not_a_success`

Old text:

```
        if job.cause is None:
            raise JobBlocked(
                refuse(
```

New text:

```
        if job.cause is None:
            return
            raise JobBlocked(
                refuse(
```

### `r290-author.J6_causeless_block_raises_the_plain_type`

Refuse a blocked job that records no reason as a plain error, so the envelope says failed over a row the job listing calls blocked

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J6_causeless_block_raises_the_plain_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2523 against a baseline of 2523
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_blocked_job_recording_no_reason_is_still_not_a_success`

Old text:

```
        if job.cause is None:
            raise JobBlocked(
                refuse(
```

New text:

```
        if job.cause is None:
            raise CratekitError(
                refuse(
```

### `r290-author.J7_cancelled_raises_the_plain_type`

Raise a plain CratekitError for a cancelled job, so a person who stopped a run is told it failed

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J7_cancelled_raises_the_plain_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2523 against a baseline of 2523
- Kills: 26 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command`
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
  - ... and 11 more, see the JSON sidecar

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
- Collected: 347 against a baseline of 347
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

### `r390-a.A1_retry_re_arms_unconditionally`

the original defect: retry re-arms every failed item whatever the job cause says

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A1_retry_re_arms_unconditionally`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_acquire_workers.py`
- Collected: 0 against a baseline of 210
- Kills: 0 (error)
- Note: OSError: [Errno 39] Directory not empty: 'popen-gw0'

Old text:

```
    if current.cause is not None and not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
            f"job {job_id} {current.state} with a cause that is not retryable, "
            f"so resuming it cannot succeed and its items were left as they are",
            steps=(
                "inspect each failed item's cause on the job's own record",
                "queue the work again the way it was queued the first time, "
                "once the reason is addressed",
            ),
            origin=("jobs",),
            detail={
                "job_id": job_id,
                "state": str(current.state),
                # Named on the refusal as the job cause names them (R-391), so
                # a person is not sent into the nested cause to learn which.
                **_permanent_reasons_of(current.cause),
            },
            inner=current.cause,
        )

```

New text:

```
(empty)
```

### `r390-a.A2_retry_refuses_any_closed_job_with_a_cause`

the flag is not read: a cancelled job and a retryable failure are refused too

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A2_retry_refuses_any_closed_job_with_a_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_backup_cli.py`, `tests/test_outbound_workers.py`
- Collected: 296 against a baseline of 296
- Kills: 9 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_jobs.py::test_a_cancelled_job_can_be_resumed_and_a_succeeded_one_cannot`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_refused_request_fails_every_item_it_carried_and_the_resume_adds_each_once`
  - `tests/test_outbound_workers.py::test_a_resumed_export_counts_across_both_runs_and_each_item_once`

Old text:

```
    if current.cause is not None and not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
```

New text:

```
    if current.cause is not None:
        raise refuse(
            "job-not-retryable",
```

### `r390-a.A3_a_failed_job_with_no_cause_is_refused`

a missing verdict is read as a permanent one

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A3_a_failed_job_with_no_cause_is_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_failed_job_with_no_recorded_cause_still_re_arms`

Old text:

```
    if current.cause is not None and not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
```

New text:

```
    if current.cause is None or not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
```

### `r390-a.A4_refusal_drops_the_permanent_reasons`

the resume refusal no longer names the mixed reasons at its own top level

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A4_refusal_drops_the_permanent_reasons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
                "state": str(current.state),
                # Named on the refusal as the job cause names them (R-391), so
                # a person is not sent into the nested cause to learn which.
                **_permanent_reasons_of(current.cause),
            },
            inner=current.cause,
```

New text:

```
                "state": str(current.state),
            },
            inner=current.cause,
```

### `r390-a.A5_refusal_drops_the_inner_cause`

the refusal no longer nests the job's own cause, so the item's reason is unreachable

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A5_refusal_drops_the_inner_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_acquire_workers.py`
- Collected: 210 against a baseline of 210
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
  - `tests/test_jobs.py::test_resuming_a_job_of_permanent_failures_through_the_verb_refuses`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`

Old text:

```
                **_permanent_reasons_of(current.cause),
            },
            inner=current.cause,
        )
```

New text:

```
                **_permanent_reasons_of(current.cause),
            },
        )
```

### `r390-b.B6_envelope_drops_the_reasons`

the all failed envelope keeps the item nested and drops the reasons beside it

- File: `src/cratekit/core/jobs.py`
- Source: `r390-b.json`, row `B6_envelope_drops_the_reasons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
        message += (
            f"; the failures carry {len(permanent_reasons)} distinct permanent "
            f"reasons: {', '.join(permanent_reasons)}"
        )
        detail[PERMANENT_REASONS] = tuple(permanent_reasons)
```

New text:

```
        pass
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

### `u235.S1_enqueue_ignores_a_given_job_id`

jobs.enqueue: a job id the caller names is ignored and a fresh identifier minted, a sample of the guard that hands new_run_id to every job

- File: `src/cratekit/core/jobs.py`
- Source: `u235.json`, row `S1_enqueue_ignores_a_given_job_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 26 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_bad_stale_cancel_is_the_parsers_usage_error_and_cancels_nothing[job-id-beside-stale-days]`
  - `tests/test_jobs.py::test_a_bad_stale_cancel_is_the_parsers_usage_error_and_cancels_nothing[negative-days]`
  - `tests/test_jobs.py::test_a_bad_stale_cancel_is_the_parsers_usage_error_and_cancels_nothing[zero-days]`
  - `tests/test_jobs.py::test_a_blocked_job_or_another_librarys_is_left_by_the_stale_cancel`
  - `tests/test_jobs.py::test_a_cancelled_stale_job_reports_cancelled_and_resumes_by_its_own_command`
  - `tests/test_jobs.py::test_a_dry_run_lists_a_queued_job_a_live_driver_holds_as_left`
  - `tests/test_jobs.py::test_a_dry_run_lists_three_stale_jobs_and_names_the_keeper_of_the_identical_two`
  - `tests/test_jobs.py::test_a_dry_run_of_one_job_cancels_nothing`
  - `tests/test_jobs.py::test_a_job_whose_queued_time_cannot_be_read_is_never_stale`
  - `tests/test_jobs.py::test_a_running_job_is_never_listed_for_cancel_however_old`
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[another-open-job-holds-it]`
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[unparseable-url]`
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[url-typed-by-hand-holds-the-swept-id]`
  - `tests/test_jobs.py::test_a_stale_set_or_hearts_job_names_no_playlist_and_says_what_it_frees[hearts-job]`
  - `tests/test_jobs.py::test_a_stale_set_or_hearts_job_names_no_playlist_and_says_what_it_frees[set-job]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    identifier = job_id or new_run_id()
```

New text:

```
    identifier = new_run_id()
```

### `u270.J1_claim_batch_size_floor`

claim_batch: accept a batch of zero items, so a size the binding never checks claims nothing and the job reads as finished

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J1_claim_batch_size_floor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_jobs.py`, `tests/test_handlers.py`
- Collected: 136 against a baseline of 136
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_claim_batch_refuses_a_batch_of_no_items[0]`

Old text:

```
    if limit < 1:
        raise refuse(
            "internal-error",
            f"a batch of {limit} items was asked for; a batch takes at least one",
```

New text:

```
    if limit < 0:
        raise refuse(
            "internal-error",
            f"a batch of {limit} items was asked for; a batch takes at least one",
```

### `u270.J2_claim_batch_order`

claim_batch: claim the highest ordinals first, so a batch writes its tracks in the reverse of the crate's order

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J2_claim_batch_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 165 against a baseline of 165
- Kills: 22 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_answered_under_a_signal_is_released_whole_and_the_job_cancelled`
  - `tests/test_jobs_batch.py::test_a_batch_is_claimed_in_ordinal_order_up_to_its_size`
  - `tests/test_jobs_batch.py::test_a_park_raised_by_the_batch_releases_it_whole_and_blocks_the_job`
  - `tests/test_jobs_batch.py::test_a_parked_batch_is_driven_again_from_its_first_item`
  - `tests/test_jobs_batch.py::test_a_raise_out_of_the_batch_handler_is_every_items_outcome`
  - `tests/test_jobs_batch.py::test_a_signal_after_one_batch_keeps_it_done_and_claims_no_other`
  - `tests/test_jobs_batch.py::test_claim_batch_takes_only_pending_items_and_none_when_nothing_is_left`
  - `tests/test_jobs_batch.py::test_every_item_of_a_batch_is_held_claimed_while_its_handler_runs`
  - `tests/test_outbound_export_batches.py::test_a_created_playlist_is_said_once_for_the_batch`
  - `tests/test_outbound_export_batches.py::test_a_job_of_two_hundred_and_fifty_tracks_makes_fifteen_requests`
  - `tests/test_outbound_export_batches.py::test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice`
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_through_the_driver_finishes_the_job`
  - `tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - ... and 7 more, see the JSON sidecar

Old text:

```
            "ORDER BY ordinal LIMIT ?",
```

New text:

```
            "ORDER BY ordinal DESC LIMIT ?",
```

### `u298.H16_reported_extra_under_progress`

reported: a verb's own detail is dropped from progress

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H16_reported_extra_under_progress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_missing.py`, `tests/test_label_genre.py`, `tests/test_label_judge.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_refused.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_vocals_cli.py`
- Collected: 1391 against a baseline of 1391
- Kills: 121 (killed)
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
  - ... and 106 more, see the JSON sidecar

Old text:

```
    if extra:
        counted.update(extra)
```

New text:

```
(empty)
```

### `u298.H17_reported_cause`

reported: a job closed on a cause reports no cause

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H17_reported_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_job_carrying_a_cause_reports_it_as_the_declared_object`

Old text:

```
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": counted,
```

New text:

```
        "cause": None,
        "progress": counted,
```

### `u298.H18_staged_path_cleared`

Artifacts.staged_path: a half written report from an attempt that died is left in staging

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H18_staged_path_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_jobs.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_staging_directory_is_cleared_of_the_attempt_before_it`

Old text:

```
        directory = self.staging_dir(cfg, job_id) / str(ordinal)
        if directory.exists():
            shutil.rmtree(directory)
```

New text:

```
        directory = self.staging_dir(cfg, job_id) / str(ordinal)
```

### `u298.H19_by_ordinal_numeric`

by_ordinal: reports sorted as text, so the ten thousandth comes before the second

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H19_by_ordinal_numeric`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_jobs.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_committed_reports_are_read_back_in_item_order_as_numbers`

Old text:

```
    return sorted((path for path in paths if path.stem.isdigit()), key=lambda item: int(item.stem))
```

New text:

```
    return sorted((path for path in paths if path.stem.isdigit()), key=lambda item: item.stem)
```

### `u298.H20_by_ordinal_filters`

by_ordinal: a stray non ordinal file reaches the sort key and raises

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H20_by_ordinal_filters`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_jobs.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_file_that_is_named_for_no_ordinal_is_no_report`

Old text:

```
    return sorted((path for path in paths if path.stem.isdigit()), key=lambda item: int(item.stem))
```

New text:

```
    return sorted((path for path in paths), key=lambda item: int(item.stem))
```

### `u298.H21_advance_refuses_empty`

advance: a job with no items is driven straight to succeeded

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H21_advance_refuses_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 129 against a baseline of 129
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

### `u298.H22_resumed_raises_state`

resumed: a job that did not end cleanly is an ok exit

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H22_resumed_raises_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_jobs.py`
- Collected: 184 against a baseline of 184
- Kills: 2 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_job_already_closed_is_judged_without_being_driven`
  - `tests/test_shared_homes.py::test_a_job_still_open_is_driven_once_and_read_again_before_it_is_judged`

Old text:

```
        job = get(store, job.job_id)
    raise_for_state(job)
    return job, warnings
```

New text:

```
        job = get(store, job.job_id)
    return job, warnings
```

### `u298.H23_artifacts_names_differ`

Artifacts: a staging name equal to the final name is accepted

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H23_artifacts_names_differ`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_a_report_location_is_two_different_directory_names[same-same]`

Old text:

```
        if self.final == self.staging:
```

New text:

```
        if False:
```

### `u301.J1_job_row_answers_none`

_job_row: answer None for an unknown job instead of refusing, so get, refreeze and join_run fail on an attribute rather than job-unknown

- File: `src/cratekit/core/jobs.py`
- Source: `u301.json`, row `J1_job_row_answers_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_job_resume.py`, `tests/test_shared_homes.py`
- Collected: 187 against a baseline of 187
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_an_unknown_job_refuses_with_a_code_from_the_vocabulary`
  - `tests/test_jobs.py::test_every_job_verb_refuses_an_unknown_identifier_with_the_same_code`

Old text:

```
    row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
    if row is None:
        raise refuse(
            "job-unknown",
```

New text:

```
    row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
    if row is None and False:
        raise refuse(
            "job-unknown",
```

### `u301.J2_release_claims_any_driver`

release_claims: release every driver's claims when one driver is named, so a parked driver frees an item a second driver holds

- File: `src/cratekit/core/jobs.py`
- Source: `u301.json`, row `J2_release_claims_any_driver`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_jobs_batch.py`
- Collected: 104 against a baseline of 104
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_releasing_one_drivers_claims_leaves_another_drivers_claim`

Old text:

```
    if driver is not None:
        query += " AND claimed_by = ?"
        params += (driver,)
```

New text:

```
    if False:
        query += " AND claimed_by = ?"
        params += (driver,)
```

### `u46-round-2.M2_resume_does_not_drive`

Report the queued job on resume without running any of it, which is the state R-198 describes

- File: `src/cratekit/core/jobs.py`
- Source: `u46-round-2.json`, row `M2_resume_does_not_drive`
- Moved: U298 replaced master's resume with core.jobs.resumed, which master_recording now calls after its reconcile; the drive inside its is_open branch is the same two lines, so removing it reports the queued job without running any of it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 59 against a baseline of 59
- Kills: 15 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume`
  - `tests/test_master_cli.py::test_a_handler_that_raises_an_undeclared_error_fails_the_item_not_the_driver`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_nothing_is_created_beside_a_destination_for_a_recording_that_is_not_there`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_the_encode_lands_in_staging_and_is_committed_rather_than_written_in_place`

Old text:

```
        _result, warnings = ctx.run_job(store, job)
        job = get(store, job.job_id)
```

New text:

```
        pass
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

### `u56-catalogue-searcher-and-tag-workers.R37_artifact_named_by_item_id`

A filename built from a tagging item identifier is a path traversal wearing a report, because the identifier is a path relative to a folder

- File: `src/cratekit/core/jobs.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R37_artifact_named_by_item_id`
- Moved: U298 folded tagging/artifacts.final_path into core.jobs.Artifacts.final_path, which tagging binds as final_path; the same name built from the ordinal
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_item_identifier_holding_a_separator_cannot_escape_the_directory`

Old text:

```
        directory = self.final_dir(cfg, job_id)
        config.mkdir_private(directory)
        return directory / f"{ordinal:04d}.json"
```

New text:

```
        directory = self.final_dir(cfg, job_id)
        config.mkdir_private(directory)
        return directory / f"{ordinal}.json"
```

### `u56-catalogue-searcher-and-tag-workers.R38_staging_not_cleared`

A half written report from an attempt that did not finish is committed by the next attempt as though it described that attempt

- File: `src/cratekit/core/jobs.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R38_staging_not_cleared`
- Moved: U298 folded tagging/artifacts.staged_path into core.jobs.Artifacts.staged_path, which tagging binds as staged_path and produced calls; the same clearing of a stale attempt
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_staging_is_cleared_before_an_attempt_writes_into_it`

Old text:

```
        if directory.exists():
            shutil.rmtree(directory)
```

New text:

```
        if False:
            shutil.rmtree(directory)
```

### `u57-recognition-and-items.C12_stray_file_sorted`

The report reader sorts every json file by its stem as a number again

- File: `src/cratekit/core/jobs.py`
- Source: `u57-recognition-and-items.json`, row `C12_stray_file_sorted`
- Moved: U298 deleted core/artifacts.py and folded its committed reader into core.jobs.Artifacts.committed, whose default order is by_ordinal; the filter to ordinal named files before the numeric sort is that function's, and dropping it lets a stray json file reach int() as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`

Old text:

```
    return sorted((path for path in paths if path.stem.isdigit()), key=lambda item: int(item.stem))
```

New text:

```
    return sorted(paths, key=lambda item: int(item.stem))
```

### `r770-b.B2_gate_asked_before_the_acknowledgment`

ask_then_write: ask the gate without reading the backup acknowledgment first, on both verbs

- File: `src/cratekit/intake/land_native.py`
- Source: `r770-b.json`, row `B2_gate_asked_before_the_acknowledgment`
- Moved: the same acknowledgment read before the gate is asked, in the shared ask then write of the native landing, which U307 moved from land_cli.py to land_native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_acknowledgment_refuses_before_the_gate`
  - `tests/test_intake_writers_native.py::test_no_acknowledgment_refuses_before_the_gate`

Old text:

```
        session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `r770-b.B3_an_abort_writes`

ask_then_write: write whatever the answer was

- File: `src/cratekit/intake/land_native.py`
- Source: `r770-b.json`, row `B3_an_abort_writes`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_an_abort_moves_nothing_and_writes_nothing, test_an_abort_writes_nothing, were folded by the trim into test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database, test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database, the abort test's steps and checks, verbatim at the end of each file's gate screen test
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
        if option != "apply":
```

New text:

```
        if option == "never":
```

### `u120.C1_no_skip_note`

favorites_notes: a skipped placement is not said

- File: `src/cratekit/intake/land_native.py`
- Source: `u120.json`, row `C1_no_skip_note`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_two_source_playlists_skip_the_placement_too`
  - `tests/test_intake_land_hearts_native.py::test_with_no_source_playlist_the_batch_lands_and_the_placement_is_skipped_and_said`

Old text:

```
    if skipped:
        return [
            {
                "code": FAVORITES_SKIPPED,
```

New text:

```
    if False:
        return [
            {
                "code": FAVORITES_SKIPPED,
```

### `u126.P3_gate_fact`

Rename the content link fact on the gate screen, so the value and its count are not where the person reads them

- File: `src/cratekit/intake/land_native.py`
- Source: `u126.json`, row `P3_gate_fact`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 438 against a baseline of 438
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_link_its_count_the_playlist_and_each_file_move_the_digest`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
        "content link": (
```

New text:

```
        "link": (
```

### `u127.L1_screen_line_blind`

The native screen counts no tagged row

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L1_screen_line_blind`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_the_screen_counts_the_tagged_rows_against_the_cut, were folded by the trim into test_the_screen_counts_the_tagged_rows_and_the_digest_moves_with_a_tag_and_the_cut, its check of the vox line counting the tagged rows against the cut, with the rescore across the cut added
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_screen_counts_the_tagged_rows_and_the_digest_moves_with_a_tag_and_the_cut`

Old text:

```
        f"{len(rows.vox_tagged())} of {len(adding)} added row(s), each whose voxlevel "
```

New text:

```
        f"{len(adding)} of {len(adding)} added row(s), each whose voxlevel "
```

### `u127.L2_items_carry_no_vox`

The gate items carry no score and no answer

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L2_items_carry_no_vox`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[above]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[below]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[zero]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`
  - `tests/test_intake_land_vox_native.py::test_the_screen_counts_the_tagged_rows_and_the_digest_moves_with_a_tag_and_the_cut`

Old text:

```
        if row.action == native.ADD and rows.vox_cut is not None and not rows.vox_blocked:
```

New text:

```
        if False:
```

### `u127.L3_totals_from_writer`

Count the written associations as tagged instead of what adoption reads back

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L3_totals_from_writer`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`

Old text:

```
    voxed = sum(1 for row in landed.collection.added if row.vox)
```

New text:

```
    voxed = landed.collection.vox_written
```

### `u127.L4_missing_unsaid`

Say nothing when a planned tag does not read back

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L4_missing_unsaid`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`

Old text:

```
    if collection.vox_missing:
```

New text:

```
    if False:
```

### `u127.L5_unscored_unsaid`

Say nothing about a file with no score

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L5_unscored_unsaid`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_a_file_with_no_score_gets_no_tag_and_is_named, were folded by the trim into test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named, its check that the screen names the file with no score and tags the scored one
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`

Old text:

```
    if not collection.vox_unscored:
```

New text:

```
    if True:
```

### `u127.L7_land_warnings_unsaid`

intake land gives no vox warning

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L7_land_warnings_unsaid`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_no_category]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_uncalibrated]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_unreadable]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
    warnings.extend(vox_warnings(landed.collection))
```

New text:

```
    warnings.extend([])
```

### `u128-b.N3_native_owned_not_found`

The native verb asks no candidate row for the owned tracks, so every one is left

- File: `src/cratekit/intake/land_native.py`
- Source: `u128-b.json`, row `N3_native_owned_not_found`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
        cfg, named, native.candidate_rows(db, names)
```

New text:

```
        cfg, named, ()
```

### `u128.L2_native_warning_unsaid`

The native landing does not put the left rows on its warnings

- File: `src/cratekit/intake/land_native.py`
- Source: `u128.json`, row `L2_native_warning_unsaid`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`

Old text:

```
    warnings.extend(account_playlists.left_warning(landed.collection.left))
```

New text:

```
    warnings.extend(account_playlists.left_warning(()))
```

### `u129-author.A4_archive_raise_fails_landing`

Let an account archive raise escape the landing write after rows are in the library

- File: `src/cratekit/intake/land_native.py`
- Source: `u129-author.json`, row `A4_archive_raise_fails_landing`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[raised]`
  - `tests/test_u129_set_account_playlist.py::test_landing_archive_failure_after_write_is_a_warning[transient]`

Old text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    except Exception as exc:
        message = (
            exc.cause.message if isinstance(exc, CratekitError) else f"{type(exc).__name__}: {exc}"
        )
        return [
            {
                "code": LAND_ARCHIVE_FAILED,
                "message": (
                    f"the account archive could not finish after the landing wrote "
                    f"({message}); the batch is in the library, run crate export "
                    f"archive over the set once the account can be reached"
                ),
            }
        ]
    return list(warnings)

```

New text:

```
    _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    return list(warnings)

```

### `u129-author.A5_archive_return_discarded`

Discard apply_archive warnings so a not-renamed return is silent on the landed envelope

- File: `src/cratekit/intake/land_native.py`
- Source: `u129-author.json`, row `A5_archive_return_discarded`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_a_landing_archive_not_renamed_is_a_warning_on_the_envelope, test_landing_archive_surfaces_changed_since_plan_as_a_warning, were folded by the trim into test_a_landing_archive_failure_is_a_warning_on_the_envelope, test_landing_archive_failure_after_write_is_a_warning, the archive warning checks, now the not renamed case beside the changed since plan one
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[not-renamed]`
  - `tests/test_u129_set_account_playlist.py::test_landing_archive_failure_after_write_is_a_warning[changed]`

Old text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    except Exception as exc:

```

New text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
        warnings = []
    except Exception as exc:

```

### `u135.A3_found_vs_made_collapsed`

The gate screen always says found-or-made when no recorded INBOX playlist is named

- File: `src/cratekit/intake/land_native.py`
- Source: `u135.json`, row `A3_found_vs_made_collapsed`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`, `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
- Collected: 9 against a baseline of 9
- Kills: 6 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined`
  - `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
  - `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`
  - `tests/test_u135_set_inbox_join.py::test_a_recorded_inbox_playlist_removed_before_the_next_landing_is_not_joined`
  - `tests/test_u135_set_inbox_join.py::test_a_removed_set_named_inbox_playlist_is_not_written_into`
  - `tests/test_u135_set_inbox_join.py::test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order`

Old text:

```
        if rows.batch_playlist_id:
            facts["inbox"] = (
                f"adds to the playlist an earlier landing of this set made "
                f"(row {rows.batch_playlist_id})"
            )
        elif rows.inbox_found_by_name:
            facts["inbox"] = "found live by name, not recorded"
        else:
            facts["inbox"] = "made"

```

New text:

```
        facts["inbox"] = (
            f"adds to the playlist an earlier landing of this set made "
            f"(row {rows.batch_playlist_id})"
            if rows.batch_playlist_id
            else "found live by its name under INBOX, or made"
        )

```

### `u146-c.L3_gate_asked_for_nothing`

_place_owned: a pass whose owned hearts are all placed opens the database to write and asks the gate over nothing

- File: `src/cratekit/intake/land_native.py`
- Source: `u146-c.json`, row `L3_gate_asked_for_nothing`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op, test_an_owned_heart_all_favorites_holds_without_a_month_is_no_write_for_an_empty_landing, test_an_owned_heart_whose_file_two_rows_claim_is_not_placed_by_a_guess, test_an_owned_heart_whose_job_froze_no_date_key_is_left_to_the_backfill, were folded by the trim into test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded, test_owned_hearts_an_empty_landing_cannot_place_alone_are_no_write, the four owned heart cases that ask nothing and end no_op, now read through the files' shared _no_op helper
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`
  - `tests/test_intake_land_owned_hearts_native.py::test_owned_hearts_an_empty_landing_cannot_place_alone_are_no_write`

Old text:

```
    if not first.writes:
        return ctx.envelope(data=empty, outcome=Outcome.NO_OP)
```

New text:

```
(empty)
```

### `u146-c.L4_missing_source_refuses`

_place_owned: a library with no All Favorites refuses the empty landing instead of ending NO_OP and saying why

- File: `src/cratekit/intake/land_native.py`
- Source: `u146-c.json`, row `L4_missing_source_refuses`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`

Old text:

```
        if exc.cause.reason != placement.SOURCE_MISSING:
            raise
        return ctx.envelope(
            data=empty,
```

New text:

```
        raise
        return ctx.envelope(
            data=empty,
```

### `u153.L1_facts_colour_count`

land_cli favorites_facts: count only the items, so the owned hearts are left out of the Pink total shown

- File: `src/cratekit/intake/land_native.py`
- Source: `u153.json`, row `L1_facts_colour_count`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit, were folded by the trim into test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one, its check that both hearts take Pink in the one commit, with the count on the screen
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
        facts["rows to colour Pink"] = len(plan.items) + len(plan.colour)
```

New text:

```
        facts["rows to colour Pink"] = len(plan.items)
```

### `u153.L3_notes_colour_skipped`

land_cli favorites_notes: never emit the missing-Pink note, so a landing that coloured nothing says nothing

- File: `src/cratekit/intake/land_native.py`
- Source: `u153.json`, row `L3_notes_colour_skipped`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_with_no_pink_row_the_landing_places_the_heart_and_warns, were folded by the trim into test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made, the no Pink row case, which still places the hearts, leaves them uncoloured and warns with the same code
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made`

Old text:

```
    if placed.colour_skipped:
        notes.append(
            {
                "code": colour_mod.PINK_COLOUR_MISSING,
```

New text:

```
    if False:
        notes.append(
            {
                "code": colour_mod.PINK_COLOUR_MISSING,
```

### `u157.L1_selection_counts`

awaiting_analysis: count no row as carrying dyn

- File: `src/cratekit/intake/land_native.py`
- Source: `u157.json`, row `L1_selection_counts`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_the_warning_names_both_selections_and_counts_each, were folded by the trim into test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection, the warning naming both selections and counting each, now over two rows
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`
- Collected: 186 against a baseline of 186
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection`

Old text:

```
    dyned = sum(1 for row in collection.added if row.dyn)
    normal
```

New text:

```
    dyned = 0
    normal
```

### `u157.L2_blocked_unnamed`

dyn_warnings: a blocked landing names none of its variable rows

- File: `src/cratekit/intake/land_native.py`
- Source: `u157.json`, row `L2_blocked_unnamed`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_library_with_no_category_to_copy_lands_and_names_the_variable_rows`

Old text:

```
    if collection.dyn_blocked:
        untagged.update(collection.dyn_variable)

```

New text:

```
(empty)
```

### `u161.L1_landing_pins_nothing`

ask_then_write: pin nothing, so every native write's answer is free of the file again

- File: `src/cratekit/intake/land_native.py`
- Source: `u161.json`, row `L1_landing_pins_nothing`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another, were folded by the trim into test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path, the continuation over another file refused stale, each screen naming the file it reads and writes
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
            spec, plan=data, context=shown(rows), pinned={DATABASE_PIN: str(opened)}
```

New text:

```
            spec, plan=data, context=shown(rows), pinned={}
```

### `u161.P6_screen_drops_path`

collection_facts: show the root's name where the database path was, so the screen no longer says which file is written

- File: `src/cratekit/intake/land_native.py`
- Source: `u161.json`, row `P6_screen_drops_path`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "reads and writes": str(rows.database),
```

New text:

```
        "reads and writes": str(rows.root_name),
```

### `u165.L1_bridge_skip`

_land_native: predict a filing on a routing tree still on the bridge

- File: `src/cratekit/intake/land_native.py`
- Source: `u165.json`, row `L1_bridge_skip`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_routing_tree_on_the_bridge_files_nothing_and_the_screen_names_it`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`

Old text:

```
            if medium.files_natively
```

New text:

```
            if True
```

### `u165.L2_land_only`

planner: predict and file under --land-only too

- File: `src/cratekit/intake/land_native.py`
- Source: `u165.json`, row `L2_land_only`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_rehearsal_digests_as_the_live_landing_that_files_and_land_only_apart`
  - `tests/test_intake_land_filing.py::test_a_routing_tree_on_the_bridge_files_nothing_and_the_screen_names_it`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`

Old text:

```
            if unfiled:
                return made
```

New text:

```
            if False:
                return made
```

### `u165.L4_files_into`

_native_payload: drop each item's files into

- File: `src/cratekit/intake/land_native.py`
- Source: `u165.json`, row `L4_files_into`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_rehearsal_digests_as_the_live_landing_that_files_and_land_only_apart`
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`

Old text:

```
        if str(row.target) in sorted_into:
```

New text:

```
        if False:
```

### `u166.A11_warning_names_batch`

awaiting_analysis: name the batch playlist again instead of Analyze

- File: `src/cratekit/intake/land_native.py`
- Source: `u166.json`, row `A11_warning_names_batch`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`

Old text:

```
                f"{collection.analyze_name} playlist, which holds every row waiting "
```

New text:

```
                f"{collection.playlist} playlist, which holds every row waiting "
```

### `u177.C4_flag_ignored`

label_plan: ignore --label-from-tags, so the batch lands filed under nothing

- File: `src/cratekit/intake/land_native.py`
- Source: `u177.json`, row `C4_flag_ignored`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_batch_of_two_labels_and_an_unregistered_seller_files_each_under_its_own`
  - `tests/test_intake_land_labels_native.py::test_a_labelled_file_with_no_year_is_named_and_a_decomposed_label_is_the_composed_folder`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_the_label_source_moves_the_digest_and_an_answer_for_one_is_stale_for_another`

Old text:

```
            if label_from_tags:
                return label_filing.plan_for_tags(db, medium, files=files)

```

New text:

```
            if False:
                return label_filing.plan_for_tags(db, medium, files=files)

```

### `u181.L1_half_is_a_warning`

land_cli vox_plan_warnings: warn at exactly half the added rows unscored

- File: `src/cratekit/intake/land_native.py`
- Source: `u181.json`, row `L1_half_is_a_warning`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_half_a_batch_unscored_is_said_on_the_line_and_is_no_warning, were folded by the trim into test_a_batch_mostly_unscored_carries_a_warning_with_its_code_on_the_gate_screen, the bound of more than half unscored, where one in two is the line's alone, beside the warning case
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_batch_mostly_unscored_carries_a_warning_with_its_code_on_the_gate_screen`

Old text:

```
    if not adding or 2 * len(unscored) <= len(adding):
```

New text:

```
    if not adding or 2 * len(unscored) < len(adding):
```

### `u181.L2_coefficient`

land_cli vox_plan_warnings: halve the coefficient, so only an unscored batch above the whole warns

- File: `src/cratekit/intake/land_native.py`
- Source: `u181.json`, row `L2_coefficient`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_batch_mostly_unscored_carries_a_warning_with_its_code_on_the_gate_screen`

Old text:

```
    if not adding or 2 * len(unscored) <= len(adding):
```

New text:

```
    if not adding or 1 * len(unscored) <= len(adding):
```

### `u307.R22_colour_notes_drop_held`

land_native._colour_notes: leave out the note naming the rows that keep a colour a person chose

- File: `src/cratekit/intake/land_native.py`
- Source: `u307.json`, row `R22_colour_notes_drop_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`

Old text:

```
    if placed.held:
```

New text:

```
    if False:
```

### `u319.M8_ok_on_any_field`

land_cli: the short path's OK offered whatever the dialog shows

- File: `src/cratekit/intake/land_native.py`
- Source: `u319.json`, row `M8_ok_on_any_field`
- Moved: the same line of the short path's visit wording, which U307 moved from land_cli.py to land_native.py with the native landing
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_intake_land_dyn_native.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 88 against a baseline of 88
- Kills: 2 (killed)
- Killed:
  - `tests/test_drift.py::test_the_auto_analysis_step_cancels_on_any_other_field_and_leaves_dyn_to_dynamic`
  - `tests/test_drift.py::test_the_sync_stop_offers_the_auto_analysis_path_after_the_selections_it_stands_in_for`

Old text:

```
    "on its Auto Analysis dialog only when it shows every one of those Normal "
```

New text:

```
    "on its Auto Analysis dialog whatever it shows of those Normal "
```

### `u319.M9_warning_drops_the_short_path`

land_cli: the awaiting analysis warning names one path again

- File: `src/cratekit/intake/land_native.py`
- Source: `u319.json`, row `M9_warning_drops_the_short_path`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_the_warning_names_both_selections_and_counts_each, were folded by the trim into test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection, the warning naming both selections and counting each, now over two rows
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_intake_land_native.py`, `tests/test_inbox_analyzed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection`

Old text:

```
                f"for analysis, and {selections}; {AUTO_ANALYSIS_STEP}; then "
```

New text:

```
                f"for analysis, and {selections}; then "
```

### `r1289.M10_warning_ready_filter`

_plan_playlists: the unread warning covers a playlist that was not queued, saying its other tracks are

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M10_warning_ready_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`

Old text:

```
        identity: tracks for identity, tracks in sweep.unread.items() if identity in sweep.ready
```

New text:

```
        identity: tracks for identity, tracks in sweep.unread.items() if True
```

### `r1289.M11_warning_absent`

_plan_playlists: no unread warning at all

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M11_warning_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
    if left:
```

New text:

```
    if False:
```

### `r1289.M12_warning_promise`

_plan_playlists: the warning reworded to promise a later sync offers the playlist again, which is false once its job succeeds

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M12_warning_promise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
                    "playlist's intake job succeeds no later sync offers it again, so "
```

New text:

```
                    "playlist's intake job succeeds the next sync takes it up again, so "
```

### `r1289.M13_warning_names`

_plan_playlists: the warning names each playlist but not its unread tracks

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M13_warning_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
                        + ", ".join(f"{ref} ({one['why']})" for ref, one in tracks.items())
```

New text:

```
                        + "some tracks"
```

### `r227.C6_composed_limit_spelled`

sync all judges against a seven spelled in the shell

- File: `src/cratekit/sync/cli.py`
- Source: `r227.json`, row `C6_composed_limit_spelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_composed_gate_judges_against_the_configured_limit`

Old text:

```
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)
```

New text:

```
    age = source.export_age(exported, limit_days=7)
```

### `r359.M5_unwired`

The playlists planner no longer hands its note to the plan

- File: `src/cratekit/sync/cli.py`
- Source: `r359.json`, row `M5_unwired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
    plan = _Plan(spec=spec, describe=describe, detail=describe([]), note=playlists.said)
```

New text:

```
    plan = _Plan(spec=spec, describe=describe, detail=describe([]))
```

### `r359.M6_no_append`

The check computes the note and never appends it to the detail a person reads

- File: `src/cratekit/sync/cli.py`
- Source: `r359.json`, row `M6_no_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
        check["detail"] += f"; {noted}"
```

New text:

```
        pass
```

### `r359.M7_note_before_describe`

The note reads an empty block instead of the source's own, so it says nothing

- File: `src/cratekit/sync/cli.py`
- Source: `r359.json`, row `M7_note_before_describe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
    noted = plan.note(plan.detail or {}) if plan.note is not None else None
```

New text:

```
    noted = plan.note({}) if plan.note is not None else None
```

### `r504-b.B10_check_no_numbers`

The inbound check fails without naming the three numbers

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B10_check_no_numbers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
            f"; the listing came back short, {short.summary()}, which does not say which"
```

New text:

```
            "; the listing came back short, which does not say which"
```

### `r504-b.B7_sync_drops_short`

sync all lists the hearts and keeps no shortfall

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B7_sync_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
    inbound.shortfall = short
```

New text:

```
    inbound.shortfall = None
```

### `r504-b.B8_check_passes`

A short listing leaves the inbound check at its prior status instead of failing it

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B8_check_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        check["status"] = "fail"
        if inbound.not_queued == playlists.Excluded.EMPTY:
```

New text:

```
        if inbound.not_queued == playlists.Excluded.EMPTY:
```

### `r504-b.B9_all_withheld_says_no_hearts`

Every heart withheld still reads as an account that lists no hearts

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B9_all_withheld_says_no_hearts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`

Old text:

```
            check["detail"] = "not queued: the provider served none of the account's hearts"
```

New text:

```
            pass
```

### `r515-operator.S13_sweep_no_warning`

The sync all sweep says nothing of a short playlist

- File: `src/cratekit/sync/cli.py`
- Source: `r515-operator.json`, row `S13_sweep_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
    if sweep.short:
```

New text:

```
    if False:
```

### `r835-c.S2_sync_hands_the_ledger_to_the_sweep_again`

sync.cli._plan_playlists: the sweep is handed no label built playlists, so every year playlist is swept as intake

- File: `src/cratekit/sync/cli.py`
- Source: `r835-c.json`, row `S2_sync_hands_the_ledger_to_the_sweep_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_intake_writers_native.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`
- Collected: 298 against a baseline of 298
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_the_sync_pass_hands_the_sweep_every_year_playlist_a_build_recorded`

Old text:

```
    label_built = ledger.label_playlist_ids(cfg)
```

New text:

```
    label_built = frozenset()
```

### `r837-a.A17_sweep_hand_off`

sync.cli: the sweep is handed no set playlist, so the exclusion has nothing to exclude

- File: `src/cratekit/sync/cli.py`
- Source: `r837-a.json`, row `A17_sweep_hand_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_export_set.py`, `tests/test_intake_writers_native.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`
- Collected: 361 against a baseline of 361
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_sweep_never_reads_a_set_playlist_as_intake`

Old text:

```
            set_built=set_built,
```

New text:

```
            set_built=frozenset(),
```

### `u109-a.A1_plan_guided`

Plan every enabled source again, guided ones included, so labels is planned as a source with no worker

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A1_plan_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
    plans = [_plan(spec, ctx) for spec in enabled if spec.guided_by is None]
```

New text:

```
    plans = [_plan(spec, ctx) for spec in enabled]
```

### `u109-a.A2_guided_empty`

Collect no guided source, so nothing names crate label sync anywhere

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A2_guided_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
    guided = tuple(spec for spec in enabled if spec.guided_by is not None)
```

New text:

```
    guided = ()
```

### `u109-a.A3_no_check_row`

Drop the guided check row, the one line the human output prints

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A3_no_check_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
    checks.extend(_guided_check(spec) for spec in guided)
```

New text:

```
(empty)
```

### `u109-a.A4_summary_guided`

Drop summary.guided from the pass report

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A4_summary_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_profile_without_the_labels_module_names_no_guided_verb`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`

Old text:

```
        "guided": _guided(guided),
    }
    for plan in plans:
```

New text:

```
    }
    for plan in plans:
```

### `u109-a.A5_gate_guided`

Drop the guided block from what the favourites gate shows

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A5_gate_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`

Old text:

```
            if p.inbound is not None
        },
        "guided": _guided(guided),
    }
```

New text:

```
            if p.inbound is not None
        },
    }
```

### `u109-a.A6_refusal_step_dropped`

A pass that queued nothing refuses without the step naming the guided verb

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A6_refusal_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`

Old text:

```
            steps=(*first.remediation.steps, *(_guided_step(spec) for spec in guided)),
```

New text:

```
            steps=first.remediation.steps,
```

### `u109-a.A7_refusal_step_first`

Prepend the guided step instead of appending it, so it displaces the refusing source's own first step

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A7_refusal_step_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`

Old text:

```
            steps=(*first.remediation.steps, *(_guided_step(spec) for spec in guided)),
```

New text:

```
            steps=(*(_guided_step(spec) for spec in guided), *first.remediation.steps),
```

### `u109-a.A8_row_reworded`

Reword the guided row so it no longer says the source is not swept here

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A8_row_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
            f"not swept by sync all; {spec.command()} takes this source on its "
```

New text:

```
            f"left to another verb; {spec.command()} takes this source on its "
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

### `u73-c.C3_next_only_with_intake_jobs`

Name intake missing --run on every pass, including one that queued no intake job

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C3_next_only_with_intake_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_pass_that_finds_only_debris_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_pass_that_queued_no_intake_job_names_no_run_verb`
  - `tests/test_sync_all.py::test_a_pass_whose_only_playlist_left_every_track_unread_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_playlist_with_no_tracks_queues_nothing_and_is_reported`

Old text:

```
    if not filed:
```

New text:

```
    if False:
```

### `u73-c.C4_next_counts_intake_jobs_only`

Count every filed job as an intake job when deciding to name the run verb

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C4_next_counts_intake_jobs_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`

Old text:

```
if job.handler_key in intake_cli.INTAKE_KEYS]
```

New text:

```
if True]
```

### `u73-c.C5_next_check_row`

Keep the command in the summary and drop the check row the human output prints

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C5_next_check_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_default_output_of_a_pass_that_queued_intake_jobs_names_the_run_verb`

Old text:

```
        checks.append(step["check"])
```

New text:

```
        pass
```

### `u74-b.B10_refused_check_status`

Report a hearts refusal as info rather than fail

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B10_refused_check_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`

Old text:

```
    elif inbound.refused is not None:
        check["status"] = "fail"
```

New text:

```
    elif inbound.refused is not None:
        check["status"] = "info"
```

### `u74-b.B11_gate_screen`

The gate screen says the hearts are queued whatever the answer when the listing refused

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B11_gate_screen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_gate_says_when_the_hearts_could_not_be_listed`

Old text:

```
                "queued_whatever_the_answer": p.inbound.queue is not None,
```

New text:

```
                "queued_whatever_the_answer": True,
```

### `u74-b.B12_next_step_outbound_only`

Name no intake missing --run step when only the hearts filed an intake job

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B12_next_step_outbound_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`

Old text:

```
    filed = [job for p in plans for job in _filed(p) if job.handler_key in intake_cli.INTAKE_KEYS]
```

New text:

```
    filed = [job for p in plans for job in p.filed if job.handler_key in intake_cli.INTAKE_KEYS]
```

### `u74-b.B1_source_id_dropped`

Queue the hearts job with no source_id, so the next pass cannot see it is open

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B1_source_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`

Old text:

```
                run_id=run_id,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
            )
```

New text:

```
                run_id=run_id,
                source_id=None,
            )
```

### `u74-b.B2_compose_skips_inbound`

The composer never queues the read half

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B2_compose_skips_inbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if p.inbound is not None and p.inbound.queue is not None:
            ready.append
```

New text:

```
        if False:
            ready.append
```

### `u74-b.B3_queue_refusal_raised`

Raise a queue time refusal instead of recording it against its half

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B3_queue_refusal_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_refusal_part_way_through_the_playlists_keeps_the_filed_ones_named`
  - `tests/test_sync_all.py::test_a_source_refused_at_queue_time_leaves_the_queued_ones_named`

Old text:

```
                    half.refused, half.not_queued = exc.cause, exc.cause.reason
```

New text:

```
                    raise
```

### `u74-b.B4_filed_outbound_only`

Count only the write half's jobs as filed, so a pass that queued only the hearts refuses or reads as a no-op

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B4_filed_outbound_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
    return [*plan.filed, *(plan.inbound.filed if plan.inbound is not None else ())]
```

New text:

```
    return [*plan.filed]
```

### `u74-b.B5_inbound_refusal_not_counted`

Leave the hearts refusal out of the refusal list, so a declined pass it alone stopped reads as a no-op

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B5_inbound_refusal_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op`

Old text:

```
        for cause in (p.refused, p.inbound.refused if p.inbound else None)
```

New text:

```
        for cause in (p.refused, None)
```

### `u74-b.B6_inbound_warning`

Emit no warning for a hearts refusal

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B6_inbound_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`

Old text:

```
        if plan.inbound is not None and plan.inbound.refused is not None:
            warnings.append(
```

New text:

```
        if False:
            warnings.append(
```

### `u74-b.B7_block_dropped`

Leave the favourites.inbound block out of the summary

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B7_block_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 13 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_half_refused_is_still_a_refusal`

Old text:

```
            plan.detail = {**(plan.detail or {}), "inbound": plan.inbound.block()}
```

New text:

```
            pass
```

### `u74-b.B8_check_dropped`

Leave the sync.favorites.inbound check out, which is all the default output prints

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B8_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
            checks.append(_inbound_check(plan, plan.inbound))
```

New text:

```
            pass
```

### `u74-b.B9_check_wording`

Say the hearts were not listed for a half that was listed and refused at the queue

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B9_check_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`

Old text:

```
            if inbound.hearts is None
```

New text:

```
            if True
```

### `u74.A10_export_refusal_raised`

Raise the write half's export refusal to _plan again, which drops the read half with it

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A10_export_refusal_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_half_refused_is_still_a_refusal`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        plan.refused, plan.not_queued = exc.cause, exc.cause.reason
        return plan
```

New text:

```
        raise
```

### `u74.A11_queue_not_bound`

Never bind the read half's queue callable, so a listed half queues nothing

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A11_queue_not_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 17 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_the_gate_refusal_queues_no_hearts_listing_either`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    inbound.queue = queue
    return inbound
```

New text:

```
    return inbound
```

### `u74.A12_run_id_dropped`

Queue the hearts job without the shared run id, so intake missing --run cannot find it

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A12_run_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`

Old text:

```
                tracks=tracks,
                run_id=run_id,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
```

New text:

```
                tracks=tracks,
                run_id=None,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
```

### `u74.A3_handler_filter`

Drop the handler key filter, so an open outbound favourites job holds the hearts listing

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A3_handler_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`

Old text:

```
        if job.handler_key == handler_key
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
```

New text:

```
        if True
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
```

### `u74.A4_source_filter`

Drop the source_id filter, so an open playlists job holds the hearts listing

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A4_source_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`

Old text:

```
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
        and job.library_id == cfg.library.volume_id
```

New text:

```
        and True
        and job.library_id == cfg.library.volume_id
```

### `u74.A5_library_filter`

Drop the library filter, so another library's open hearts job holds this one

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A5_library_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`

Old text:

```
        and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        and True
    )
```

### `u74.A6_open_filter`

Count a finished hearts job as open, so a failed job holds every later pass

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A6_open_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`

Old text:

```
                if job.is_open()
            )
```

New text:

```
                if True
            )
```

### `u74.A7_in_flight_guard`

Ignore an open hearts job, so every pass queues a second listing beside it

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A7_in_flight_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`

Old text:

```
        if in_flight:
            inbound.not_queued
```

New text:

```
        if False:
            inbound.not_queued
```

### `u74.A8_empty_guard`

Queue an empty hearts listing as a job, rather than reporting no hearts

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A8_empty_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_source_refused_at_queue_time_leaves_the_queued_ones_named`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`

Old text:

```
    if not tracks:
        inbound.not_queued = playlists.Excluded.EMPTY
```

New text:

```
    if False:
        inbound.not_queued = playlists.Excluded.EMPTY
```

### `u74.A9_listing_refusal_raised`

Raise a hearts listing refusal instead of recording it, so it ends the favourites source

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A9_listing_refusal_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op`
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_pass_over_a_recent_export_carries_no_age_warning`
  - `tests/test_sync_all.py::test_a_pass_that_queued_over_an_old_export_warns_and_still_queues`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_half_refused_is_still_a_refusal`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_composed_gate_judges_against_the_configured_limit`
  - `tests/test_sync_all.py::test_the_composed_gate_names_the_exports_date_beside_what_would_queue`
  - `tests/test_sync_all.py::test_the_composed_gate_shows_the_tracks_the_sweeps_digest_covers`
  - `tests/test_sync_all.py::test_the_composed_pass_carries_the_favourites_verb_standing_warning`
  - `tests/test_sync_all.py::test_the_favourites_job_carries_a_gate_run_its_own_verb_owns`
  - `tests/test_sync_all.py::test_the_gate_asks_over_the_digest_sync_favorites_itself_offers`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        inbound.refused, inbound.not_queued = exc.cause, exc.cause.reason
        return inbound
```

New text:

```
        raise
```

### `u210.R16_forecast_line`

sync_pair: warn of the ceiling only at ten times over

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R16_forecast_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_gate_forecast_above_the_hour_names_the_hour_and_its_command_runs`
  - `tests/test_sync_pair_resume.py::test_a_gate_whose_ceiling_is_below_the_expected_calls_says_so_with_the_calls_value`

Old text:

```
        if writing > line:
```

New text:

```
        if writing > line * 10:
```

### `u210.R9_skip_done`

sync_pair: write a pair an earlier command finished

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R9_skip_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_ceiling_stop_after_three_of_five_pairs_is_finished_by_a_continue_of_the_run`

Old text:

```
                    if _steps_of(steps, one).has(STEP_DONE):
```

New text:

```
                    if False:
```

### `u220.P5_no_stop_after_loop`

sync_pair: end OK after the loop though an order did not finish

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u220.json`, row `P5_no_stop_after_loop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_tie.py`
- Collected: 306 against a baseline of 306
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_the_account_still_stands_in_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[refused]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_the_run_puts_the_refused_pair_in_order_and_moves_nothing_else`
  - `tests/test_sync_pair_order.py::test_a_refused_order_stops_its_pair_alone_and_every_other_write_lands`

Old text:

```
    if unordered:
```

New text:

```
    if False:
```

### `u226.M23_totals_no_read_backs`

sync_pair: the run's totals carry no read backs

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u226.json`, row `M23_totals_no_read_backs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 267 against a baseline of 267
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_the_runs_totals_carry_each_read_backs_readings_and_wait`

Old text:

```
        "read_backs": [record for d in done for record in d.read_backs],
```

New text:

```
        "read_backs": [],
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

### `r1372.K22_mark_guard_gone`

stopped_write: a stop that began before the pair was marked is read as the pair's

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K22_mark_guard_gone`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_first_sync_reads_the_stop_on_its_account_playlist_whatever_the_mark`
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`

Old text:

```
        if marked is not None and began < marked:
            return None
```

New text:

```
        if False:
            return None
```

### `r1372.K23_mark_guard_inclusive`

stopped_write: a stop that began at the very moment the pair was marked is refused

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K23_mark_guard_inclusive`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`

Old text:

```
        if marked is not None and began < marked:
```

New text:

```
        if marked is not None and began <= marked:
```

### `r1372.K6_reader_ignores_carried`

reader: the carried records are not read, only the kept steps

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K6_reader_ignores_carried`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
        records = [*records, *(one for one in kept if (one.run_id, one.digest) not in current)]
```

New text:

```
        records = [*records]
```

### `r1372.K7_copy_never_gives_way`

reader: a carried copy is read beside its own run's steps kept under the same plan

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K7_copy_never_gives_way`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`

Old text:

```
        current = {(one.run_id, one.digest) for one in records}
```

New text:

```
        current = set()
```

### `r1372.K8_copy_gives_way_to_any_plan`

reader: a carried copy gives way to its run's steps under any plan, so a replanned run's fresh steps hide it

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K8_copy_gives_way_to_any_plan`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`

Old text:

```
        current = {(one.run_id, one.digest) for one in records}
        records = [*records, *(one for one in kept if (one.run_id, one.digest) not in current)]
```

New text:

```
        current = {one.run_id for one in records}
        records = [*records, *(one for one in kept if one.run_id not in current)]
```

### `r1372.K9_carried_unread_unsaid`

reader: a carried record that cannot be read is not named

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K9_carried_unread_unsaid`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`

Old text:

```
        problems = [*problems, *unread]
```

New text:

```
        problems = [*problems]
```

### `r1376.F13_snapshot_guard_inclusive`

stopped_write (sample, U225): a stop that began after the snapshot by a hair is read as passed

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1376.json`, row `F13_snapshot_guard_inclusive`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 34 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_fresh_sync_orders_the_account_to_rekordbox_and_plans_no_rekordbox_order`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_reading_that_never_settled_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_later_reading_still_on_the_moves_path_is_finished_never_read_as_a_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_later_run_that_failed_before_its_order_began_does_not_hide_the_stopped_write`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_before_the_stop_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_for_another_run_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_on_the_path_is_never_the_baseline_so_the_partial_state_after_it_finishes`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            if synced is None or not began > synced:
```

New text:

```
            if synced is None or True:
```

### `r1376.F1_first_stop_none`

first_stop: a first sync is never handed the stop on its account playlist

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1376.json`, row `F1_first_stop_none`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_first_sync_reads_the_stop_on_its_account_playlist_whatever_the_mark`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`

Old text:

```
        _began, write = self.stopped[0].get(account_id, (None, None))
        return write
```

New text:

```
        _began, write = self.stopped[0].get(account_id, (None, None))
        return None
```

### `r1383.M19_sampled_mirrors_empty`

sampled: _Reader.mirrors answers no INBOX playlist, so every landed track is queued again, the half R-1383 keeps beside it

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1383.json`, row `M19_sampled_mirrors_empty`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 11 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_is_added_and_never_queued`
  - `tests/test_sync_pair.py::test_each_landed_file_is_read_once_per_plan`
  - `tests/test_sync_pair.py::test_one_row_landed_in_two_inbox_playlists_is_one_row`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[torn]`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[unknown-state]`
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`
  - `tests/test_sync_pair.py::test_two_landed_rows_carrying_the_code_are_ambiguous_and_queue_nothing`
  - `tests/test_sync_pair_hold.py::test_a_track_found_by_another_landing_costs_the_plan_no_call[by another account playlist's landing]`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`

Old text:

```
        return self.landings[0]
```

New text:

```
        return {}
```

### `r1383.M1_scan_drops_unread`

landed_inbox_playlists: answer no unread entry, the defect the card closes, so an unreadable landing record is read as no landing and its track queued

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1383.json`, row `M1_scan_drops_unread`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_hold.py`
- Collected: 183 against a baseline of 183
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_held_while_a_record_is_unread`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
    return {account_id: frozenset(ids) for account_id, ids in found.items()}, tuple(unreadable)
```

New text:

```
    return {account_id: frozenset(ids) for account_id, ids in found.items()}, ()
```

### `r1385.M11_name_fallback`

_Reader.held_by_jobs: no fallback to the account playlist for a job naming no playlist, so its reason names nothing

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1385.json`, row `M11_name_fallback`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`

Old text:

```
            name = str(payload.get(intake_cli.PLAYLIST_NAME) or "") or source
```

New text:

```
            name = str(payload.get(intake_cli.PLAYLIST_NAME) or "")
```

### `r1385.M15_failed_jobs_hold`

pair_jobs: read a failed or cancelled job as holding its tracks, so a track whose download failed is never queued again (sampled guard)

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1385.json`, row `M15_failed_jobs_hold`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[cancelled]`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[failed]`

Old text:

```
        and job.state not in (jobs.JobState.FAILED, jobs.JobState.CANCELLED)
    )
```

New text:

```
    )
```

### `r1385.M1_no_job_holds_anything`

_Reader.held_by_jobs: read no job's tracks, so every track a job holds is queued again, a pair's own included

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1385.json`, row `M1_no_job_holds_anything`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 13 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`
  - `tests/test_sync_pair_back.py::test_a_missing_track_is_queued_once_and_then_awaits`
  - `tests/test_sync_pair_discover.py::test_an_unowned_track_added_on_the_account_is_queued_once_and_then_awaiting`
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`

Old text:

```
        return {remote_id: tuple(held) for remote_id, held in found.items()}
```

New text:

```
        return {}
```

### `u225.M14_superseded_unchecked`

stopped_write: a write the pair's snapshot came after is still finished

- File: `src/cratekit/sync/pair_read.py`
- Source: `u225.json`, row `M14_superseded_unchecked`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_a_fresh_sync_finished_is_left_behind_by_the_snapshot`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
            if synced is None or not began > synced:
```

New text:

```
            if synced is None:
```

### `u229.M10_file_isrc_fallback`

mirror_codes: read only the database ISRC, so a landed row whose code is in its file alone is never found

- File: `src/cratekit/sync/pair_read.py`
- Source: `u229.json`, row `M10_file_isrc_fallback`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_is_added_and_never_queued`
  - `tests/test_sync_pair.py::test_each_landed_file_is_read_once_per_plan`
  - `tests/test_sync_pair.py::test_one_row_landed_in_two_inbox_playlists_is_one_row`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[torn]`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[unknown-state]`
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`
  - `tests/test_sync_pair.py::test_two_landed_rows_carrying_the_code_are_ambiguous_and_queue_nothing`
  - `tests/test_sync_pair_hold.py::test_a_track_found_by_another_landing_costs_the_plan_no_call[by another account playlist's landing]`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`

Old text:

```
    for row in playlist_pair.members(db, mirror):
        code = match.isrc_token(row.isrc) or file_identity(cfg, row.path)[0]
        if code:
            found.append((code, row.content_id))
```

New text:

```
    for row in playlist_pair.members(db, mirror):
        code = match.isrc_token(row.isrc)
        if code:
            found.append((code, row.content_id))
```

### `u229.M11_mirror_cache`

_Reader.mirror_codes: read the playlist's files on every ask, so a plan reads a landed file once per step

- File: `src/cratekit/sync/pair_read.py`
- Source: `u229.json`, row `M11_mirror_cache`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_each_landed_file_is_read_once_per_plan`

Old text:

```
        if mirror not in self.landed_codes:
```

New text:

```
        if True:
```

### `u229.M12_own_mirrors_bypass_cache`

_mirror_isrcs: read this pair's landings without the plan's copy, so the widened step reads each own landed file again

- File: `src/cratekit/sync/pair_read.py`
- Source: `u229.json`, row `M12_own_mirrors_bypass_cache`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_each_landed_file_is_read_once_per_plan`

Old text:

```
        reader.cfg, reader.db, reader.mirrors.get(account_id, ()), read=reader.mirror_codes
    )
```

New text:

```
        reader.cfg, reader.db, reader.mirrors.get(account_id, ())
    )
```

### `u229.M2_wide_landed_reads_own_only`

_Reader.landed_anywhere: read only the first account playlist's landings, so most accounts' landed tracks are queued again

- File: `src/cratekit/sync/pair_read.py`
- Source: `u229.json`, row `M2_wide_landed_reads_own_only`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_two_landed_rows_carrying_the_code_are_ambiguous_and_queue_nothing`

Old text:

```
        for ids in self.mirrors.values():
            every.update(ids)
```

New text:

```
        for ids in list(self.mirrors.values())[:1]:
            every.update(ids)
```

### `u229.M6_config_error_not_caught`

_Reader.job_reports: catch only a refusal, so a configuration error from any job's reports escapes

- File: `src/cratekit/sync/pair_read.py`
- Source: `u229.json`, row `M6_config_error_not_caught`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_another_pairs_job_that_no_longer_reads_stops_no_plan`

Old text:

```
            except (CratekitError, config.ConfigError) as error:
```

New text:

```
            except CratekitError as error:
```

### `u229.M9_landed_dedup`

landed_isrcs: append a row once for each INBOX playlist holding it, so one row landed twice reads as ambiguous

- File: `src/cratekit/sync/pair_read.py`
- Source: `u229.json`, row `M9_landed_dedup`
- Moved: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_one_row_landed_in_two_inbox_playlists_is_one_row`

Old text:

```
            if content_id not in found.setdefault(code, []):
                found[code].append(content_id)
```

New text:

```
            found.setdefault(code, []).append(content_id)
```

