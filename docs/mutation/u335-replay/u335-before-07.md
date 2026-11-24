# Mutation table: u335-before-07

Measured by `scripts/mutate.py` on 2026-11-24 05:00 UTC, branch `HEAD` at `b41c698d`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 252.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 05:00 UTC for commit `b41c698da363`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 35, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u43-author-light.C2_bound_off_by_one` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `u43-author-light.P4_no_positions_at_all` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 4 | killed |
| `u43-author-light.P5_role_ignored` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `u43-author-round-2.H2_empty_is_a_no_op` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `u43-author-round-2.H3_missing_root_not_refused` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `u43-author-round-2.H4_template_loses_the_marker` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `u43-author-round-2.V2_marker_position_moved` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `u43-author-round-2.V3_root_check_reports_instead_of_refusing` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `u98-a.K1_key_off_wheel` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 7 | killed |
| `u98-a.U2_key_missing` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `u98-a.U3_reported_owned` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 5 | killed |
| `u98-a.U4_tempo_dropped` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 3 | killed |
| `u98-a.X1_mutex` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 3 | killed |
| `u98-b.E1_existing_containment` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `u98-b.S1_supplied_beside_path` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 3 | killed |
| `u98-b.S2_tempo_half` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `u28-skills-independent.K1_composite` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 11 | killed |
| `u28-skills-independent.S11_typed_cause_lost` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 2 | killed |
| `u28-skills-independent.S12_reason_slug` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 2 | killed |
| `u28-skills-independent.S14_into_ignored` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 10 | killed |
| `u28-skills-independent.S15_drift_never_warns` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `u28-skills-independent.S16_counts_miscounted` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 5 | killed |
| `u28-skills-independent.S18_detail_reworded` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `u28-skills-independent.S5_stamp_quote_strip` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 7 | killed |
| `u28-skills-independent.S9_previous_always_none` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 5 | killed |
| `u311.D1_stamp_name_unstripped` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 8 | killed |
| `r1289.M10_warning_ready_filter` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 147 | 1 | killed |
| `r1289.M11_warning_absent` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 147 | 2 | killed |
| `r1289.M12_warning_promise` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 147 | 2 | killed |
| `r1289.M13_warning_names` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 147 | 2 | killed |
| `r227.C6_composed_limit_spelled` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `r359.M5_unwired` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `r359.M6_no_append` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `r359.M7_note_before_describe` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `r504-b.B10_check_no_numbers` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 3 | killed |
| `r504-b.B7_sync_drops_short` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 3 | killed |
| `r504-b.B8_check_passes` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 3 | killed |
| `r504-b.B9_all_withheld_says_no_hearts` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `r515-operator.S13_sweep_no_warning` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u109-a.A1_plan_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 9 | killed |
| `u109-a.A2_guided_empty` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 7 | killed |
| `u109-a.A3_no_check_row` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 3 | killed |
| `u109-a.A4_summary_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 4 | killed |
| `u109-a.A5_gate_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u109-a.A6_refusal_step_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 2 | killed |
| `u109-a.A7_refusal_step_first` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u109-a.A8_row_reworded` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u73-c.C3_next_only_with_intake_jobs` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 5 | killed |
| `u73-c.C4_next_counts_intake_jobs_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u73-c.C5_next_check_row` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u74-b.B10_refused_check_status` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 3 | killed |
| `u74-b.B11_gate_screen` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u74-b.B12_next_step_outbound_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u74-b.B1_source_id_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 9 | killed |
| `u74-b.B2_compose_skips_inbound` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 16 | killed |
| `u74-b.B3_queue_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 3 | killed |
| `u74-b.B4_filed_outbound_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 10 | killed |
| `u74-b.B5_inbound_refusal_not_counted` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u74-b.B6_inbound_warning` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u74-b.B7_block_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 13 | killed |
| `u74-b.B8_check_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 10 | killed |
| `u74-b.B9_check_wording` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u74.A10_export_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 15 | killed |
| `u74.A11_queue_not_bound` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 17 | killed |
| `u74.A12_run_id_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 2 | killed |
| `u74.A3_handler_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u74.A4_source_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u74.A5_library_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 1 | killed |
| `u74.A6_open_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 3 | killed |
| `u74.A7_in_flight_guard` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 2 | killed |
| `u74.A8_empty_guard` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 4 | killed |
| `u74.A9_listing_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 116 | 19 | killed |
| `r1056.S1_no_landing_step_names_intake_missing` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 102 | 4 | killed |
| `r1056.S2_unreachable_step_names_sync` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 102 | 1 | killed |
| `r361-a.A7_mark_verb_forgets_debris` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 103 | 1 | killed |
| `r361-a.A8_mark_verb_respells_the_word` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 103 | 1 | killed |
| `r361-a.A9_reword_the_why` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 103 | 1 | killed |
| `r777-confirm.N4_plain_name` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `r777-confirm.N7_digest_marks` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `r777.N10_screen_says_pass` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `r777.N11_exclusive` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `r777.N12_no_landing_required` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 4 | killed |
| `r777.N18_unreachable_called_bridge` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `r777.N19_digest_landings` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `r777.N5_bridge_accepted` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 2 | killed |
| `r777.N6_no_reread` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 2 | killed |
| `r777.N9_proof_is_file` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 4 | killed |
| `u174.M10_dedupe` | `src/cratekit/sync/mark_cli.py` | maintainer | 3 file(s) | 188 | 1 | killed |
| `u174.M11_stranger_before_no_jobs` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 188 | 1 | killed |
| `u174.M1_stranger_refusal` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 188 | 2 | killed |
| `u174.M2_narrowing` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 188 | 4 | killed |
| `u174.M3_unfinished_refusal` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 188 | 3 | killed |
| `u174.M4_unfinished_rows_outstanding` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 188 | 1 | killed |
| `u174.M5_unfinished_job` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 188 | 1 | killed |
| `u174.M6_unfinished_reports` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 188 | 1 | killed |
| `u174.M7_digest_names_the_narrowing` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 188 | 2 | killed |
| `u174.M8_screen_names_the_narrowing` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 188 | 1 | killed |
| `u174.M9_verb_passes_the_flag` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 188 | 5 | killed |
| `u174.P1_bridge_plans_no_native_pass` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 188 | 1 | killed |
| `u174.P2_unreachable_is_refused` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 188 | 1 | killed |
| `u242.M21_mark_cli_already_marked_by_title` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 115 | 1 | killed |
| `u82-b.B5_not_listed_is_skipped` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-b.B6_a_failed_job_is_skipped` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 2 | killed |
| `u82-b.B7_unread_reports_hold_the_playlist` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 2 | killed |
| `u82-b.B8_an_offered_track_is_owed` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-c.C1_a_tombstoned_track_is_settled` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-c.C2_one_outstanding_track_holds_the_playlist` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 9 | killed |
| `u82-c.C3_landed_is_told_from_owned` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 2 | killed |
| `u82-c.C9_the_accounts_reason_is_kept` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-d.B2_paths_compared_resolved_again` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `r838-c.R1_library_bound` | `src/cratekit/sync/mark_record.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-c.R2_remark_clears` | `src/cratekit/sync/mark_record.py` | maintainer | 1 file(s) | 32 | 1 | killed |
| `r838-d.R3b_stamp_target` | `src/cratekit/sync/mark_record.py` | user | 1 file(s) | 32 | 1 | killed |
| `u242.M6_record_v1_reads_a_taken_key` | `src/cratekit/sync/mark_record.py` | user | 2 file(s) | 78 | 1 | killed |
| `u242.M9_take_overwrites_a_held_entry` | `src/cratekit/sync/mark_record.py` | user | 2 file(s) | 115 | 1 | killed |
| `r777.N1_empty_proof` | `src/cratekit/sync/marks.py` | maintainer | 2 file(s) | 100 | 1 | killed |
| `r777.N2_neither_proof` | `src/cratekit/sync/marks.py` | maintainer | 2 file(s) | 100 | 1 | killed |
| `r777.N3_engine_unchecked` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 100 | 3 | killed |
| `u82-a.A1_stat_oserror_is_the_refusal` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 185 | 4 | killed |
| `u82-a.A2_a_folder_is_not_a_file` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 185 | 1 | killed |
| `u82-a.A3_an_empty_file_is_not_proof` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 185 | 2 | killed |
| `r1360.F1_walk_uncounted` | `src/cratekit/sync/pair_calls.py` | user | 15 file(s) | 828 | 8 | killed |
| `r1360.F2_step_a_page` | `src/cratekit/sync/pair_calls.py` | user | 15 file(s) | 828 | 3 | killed |
| `r1360.F3_judged_without_walk` | `src/cratekit/sync/pair_calls.py` | user | 15 file(s) | 828 | 4 | killed |
| `u220.C1_moves_head_rule` | `src/cratekit/sync/pair_calls.py` | user | 10 file(s) | 306 | 5 | killed |
| `u226.M24_estimate_no_unpaged` | `src/cratekit/sync/pair_calls.py` | user | 3 file(s) | 137 | 16 | killed |
| `u231.M24_forecast_without_the_settle_reading` | `src/cratekit/sync/pair_calls.py` | user | 2 file(s) | 46 | 4 | killed |
| `u246.S7_pair_calls_before_empty` | `src/cratekit/sync/pair_calls.py` | user | 2 file(s) | 46 | 5 | killed |
| `r1264.M14_check_unread_moved` | `src/cratekit/sync/pair_check.py` | user | 2 file(s) | 49 | 1 | killed |
| `r1264.M15_check_unread_as_tuple` | `src/cratekit/sync/pair_check.py` | user | 1 file(s) | 20 | 1 | killed |
| `r1385.M12_check_reads_no_job` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 292 | 2 | killed |
| `r1420-b.B2_beyond_tail_unread_pinned` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 1 | killed |
| `r1420.B1_beyond_order_unread` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 8 | killed |
| `r1420.B3_beyond_removals_asked` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 3 | killed |
| `r1420.N1_fix_reverted` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 7 | killed |
| `r1420.N2_moves_begun_ignored` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 4 | killed |
| `r1420.N3_finish_read_too` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 2 | killed |
| `r1420.N5_order_always_read` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 6 | killed |
| `r1420.N6_call_site_never_reads_order` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 8 | killed |
| `u209.C10_reverse_recheck` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 2 | killed |
| `u209.C11_home_of` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C12_brought_folder` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C13_jobs_queued` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 2 | killed |
| `u209.C3_withheld` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C4_rekordbox_gone` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C5_memberships` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 5 | killed |
| `u209.C6_discovered_place` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 5 | killed |
| `u209.C7_made_left_behind` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C8_rows_gone` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C9_unpaired_back` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.H1_offer_mismatch_ignored` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u210.R10_check_todo` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R11_part_written` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 6 | killed |
| `u210.R12_our_folders` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 5 | killed |
| `u210.R14_asked_before` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 9 | killed |
| `u210.R18_beyond_order` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R19_beyond_gained` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R20_beyond_lost` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R21_check_queued` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R22_landed_read` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u226.M20_check_no_lag` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 267 | 1 | killed |
| `u246.S12_pair_cli_made_here_empty` | `src/cratekit/sync/pair_check.py` | user | 1 file(s) | 14 | 1 | killed |
| `u210.R16_forecast_line` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 2 | killed |
| `u210.R9_skip_done` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 1 | killed |
| `u220.P5_no_stop_after_loop` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 306 | 9 | killed |
| `u226.M23_totals_no_read_backs` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 267 | 1 | killed |
| `u198.D10_twins` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D11_two_homes` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D2_favorites_home` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 3 | killed |
| `u198.D3_held` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D4_skip` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 3 | killed |
| `u198.D5_smart` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D6_released` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D7_twice` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D8_top_names` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.D9_foreign` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 168 | 2 | killed |
| `u202.D1_skip` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D2_two_tops` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D3_longest` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D5_name_taken` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D6_favourites` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u216.M11_paired_raw` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 6 | killed |
| `u216.M1_held_record_ignored` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 7 | killed |
| `u216.M2_created_folder_by_time` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 2 | killed |
| `u216.M4_no_time_reads_new` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 3 | killed |
| `u216.M5_naive_time_trusted` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 2 | killed |
| `u216.M7_time_rule_off` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 3 | killed |
| `u242.M27_copy_pool_reads_no_taken` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 76 | 1 | killed |
| `u304-b.S7_walk_keeps_removed_nodes` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 114 | 1 | killed |
| `u304.S8_walk_root_sentinel` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 114 | 87 | killed |
| `r1404.M1_disagreeing_base_ignored` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 3 | killed |
| `r1404.M2_rekordbox_move_ignored` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 3 | killed |
| `r1404.M3_account_move_not_guarded` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 4 | killed |
| `r1404.M4_always_rekordbox` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 4 | killed |
| `r1404.M5_disagreement_read_now` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 2 | killed |
| `r1404.M6_disagreement_read_against_the_account_now` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 1 | killed |
| `r1404.S1_default_leader` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 16 | killed |
| `r1404.S2_stopped_leader_again` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 2 | killed |
| `r1416.M1_rekordbox_does_not_lead` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 2 | killed |
| `r1416.M2_order_kept_ignored` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 2 | killed |
| `r1416.M3_empty_rekordbox_leads` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 1 | killed |
| `r1416.M4_first_sync_unguarded` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 1 | killed |
| `r1416.M5_stopped_write_yields` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 1 | killed |
| `r1416.M6_default_not_kept` | `src/cratekit/sync/pair_merge.py` | maintainer | 5 file(s) | 225 | 2 | killed |
| `r1416.S2_placed_after_neighbour` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 22 | killed |
| `u130-a.A1_removal_beats_addition` | `src/cratekit/sync/pair_merge.py` | user | 2 file(s) | 23216 | 0 (promoted) | zero |
| `u130-a.A5_new_tracks_appended` | `src/cratekit/sync/pair_merge.py` | user | 2 file(s) | 126 | 8 | killed |
| `u130-a.A6_order_change_read_inverted` | `src/cratekit/sync/pair_merge.py` | user | 2 file(s) | 126 | 18 | killed |
| `u202.M1_since` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 2 | killed |
| `u202.M2_naive` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 1 | killed |
| `u202.M3_tie` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 1 | killed |
| `u202.M4_unknown` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 9 | killed |
| `u202.M5_adder` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 10 | killed |
| `u202.M6_account_readded` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 12 | killed |
| `u202.M7_removal_kept` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 2 | killed |

## Zero rows and what they owe

- `u130-a.A1_removal_beats_addition` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u43-author-light.C2_bound_off_by_one`

The bound is loosened by one rather than removed, so zero passes and negatives do not. A guard whose constant can be moved without a death is a guard that pins nothing.

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `C2_bound_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_value_the_flag_cannot_take_is_refused_at_the_parser[positive_count-0]`
  - `tests/test_setbuilder_cli.py::test_an_invocation_the_flags_cannot_take_is_the_parsers_verdict[count-below-one]`

Old text:

```
    if value < 1:
```

New text:

```
    if value < 0:
```

### `u43-author-light.P4_no_positions_at_all`

Every item reports position null, so the suggested sequence is not recoverable from the payload

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P4_no_positions_at_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unowned_sequence_places_each_companion_once`
  - `tests/test_setbuilder_cli.py::test_one_either_companion_of_an_owned_anchor_is_placed_once`
  - `tests/test_setbuilder_cli.py::test_plan_for_composes_the_engine_exactly_as_build_set_does`
  - `tests/test_setbuilder_cli.py::test_the_sequence_leads_the_items_and_carries_its_own_order`

Old text:

```
        {**entry, "position": placed.get(id(scored))}
```

New text:

```
        {**entry, "position": None}
```

### `u43-author-light.P5_role_ignored`

The role flag is dropped on the way to the engine, so --role before answers with both sides

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `P5_role_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_role_narrows_the_answer_to_one_side`
  - `tests/test_setbuilder_cli.py::test_the_role_flag_reaches_the_engine`

Old text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=role)
```

New text:

```
    plan = setbuilder.build_plan(ranked, resolved, count=count, role=None)
```

### `u43-author-round-2.H2_empty_is_a_no_op`

ROUND ONE: zero. A plan with no companions reports NO_OP rather than OK, which tells a consumer nothing happened when the question was answered

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H2_empty_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`

Old text:

```
    return ctx.envelope(data=plan, outcome=Outcome.OK)
```

New text:

```
    return ctx.envelope(
        data=plan, outcome=Outcome.OK if plan["items"] else Outcome.NO_OP
    )
```

### `u43-author-round-2.H3_missing_root_not_refused`

ROUND ONE: zero. The configured library root is no longer checked before the scan, so an unmounted volume scans zero files and every anchor comes back unindexed

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H3_missing_root_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`

Old text:

```
    if not root.is_dir():
```

New text:

```
    if root.is_dir() and False:
```

### `u43-author-round-2.H4_template_loses_the_marker`

ROUND ONE: zero. The name template stops declaring the lossy marker, so a marked file's clean title keeps the marker and its match key gains a token

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H4_template_loses_the_marker`
- Moved: Same template function; U298 spelled its marker rule as naming.NameTemplate.lossy, which builds the same lossy MarkerRule, so the plain template drops it as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_lossy_marked_companion_comes_back_with_a_clean_title`

Old text:

```
    return NameTemplate.lossy(cfg.naming.lossy_marker)
```

New text:

```
    return NameTemplate()
```

### `u43-author-round-2.V2_marker_position_moved`

The marker rule is declared with a separator that puts it somewhere the head parser does not strip. If the lossy guard passes this, its fixture is in a position where the declaration cannot matter, which is the mistake the first attempt at it made

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `V2_marker_position_moved`
- Moved: Same template function; U298 spelled its marker rule as naming.NameTemplate.lossy, so the wrong literal is passed to it in place of the configured marker, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_lossy_marked_companion_comes_back_with_a_clean_title`

Old text:

```
    return NameTemplate.lossy(cfg.naming.lossy_marker)
```

New text:

```
    return NameTemplate.lossy("[NOTAMARKER]")
```

### `u43-author-round-2.V3_root_check_reports_instead_of_refusing`

The missing root produces an empty plan and an OK exit rather than a refusal, which is the clean-report-over-unreadable-state shape rather than the crash shape. A guard that only catches the crash is not the guard this row needs

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `V3_root_check_reports_instead_of_refusing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`

Old text:

```
    if not root.is_dir():
        raise refuse(
```

New text:

```
    if not root.is_dir():
        return ctx.envelope(
            data=plan_for(
                setbuilder.Track(
                    artist="", title="", key="", bpm=None, genre="",
                    energy=None, vox=None, voxgender=None, match="",
                ),
                (),
                declared=taxonomy.default_taxonomy(),
            ),
            outcome=Outcome.OK,
        )
    if False:
        raise refuse(
```

### `u98-a.K1_key_off_wheel`

camelot_key: drop the refusal, so a code off the wheel parses to the empty string

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `K1_key_off_wheel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 7 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_value_the_flag_cannot_take_is_refused_at_the_parser[camelot_key-0A]`
  - `tests/test_setbuilder_cli.py::test_a_value_the_flag_cannot_take_is_refused_at_the_parser[camelot_key-13A]`
  - `tests/test_setbuilder_cli.py::test_a_value_the_flag_cannot_take_is_refused_at_the_parser[camelot_key-13C]`
  - `tests/test_setbuilder_cli.py::test_a_value_the_flag_cannot_take_is_refused_at_the_parser[camelot_key-8C]`
  - `tests/test_setbuilder_cli.py::test_a_value_the_flag_cannot_take_is_refused_at_the_parser[camelot_key-]`
  - `tests/test_setbuilder_cli.py::test_a_value_the_flag_cannot_take_is_refused_at_the_parser[camelot_key-eight]`
  - `tests/test_setbuilder_cli.py::test_an_invocation_the_flags_cannot_take_is_the_parsers_verdict[key-off-the-wheel]`

Old text:

```
    if not canonical:
        raise ValueError(f"{text!r} is not a Camelot code between 1A and 12B")

```

New text:

```
(empty)
```

### `u98-a.U2_key_missing`

unowned_anchor: drop the key missing refusal, so an unresolved anchor reaches the engine

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U2_key_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[unowned-no-key]`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_with_no_key_or_no_label_refuses`

Old text:

```
    if resolved.key is None:
```

New text:

```
    if False:
```

### `u98-a.U3_reported_owned`

unowned_anchor: return the anchor marked owned and confirmed, the envelope's honesty flags

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U3_reported_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 5 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_in_8a_ranks_the_library_against_it`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_is_ranked_through_the_dispatcher`
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_naming_an_owned_track_exactly_is_held_and_not_ranked`
  - `tests/test_setbuilder_cli.py::test_an_unowned_label_that_names_an_owned_title_is_never_matched_to_it`

Old text:

```
            detail={"label": label, "unresolved": resolved.unresolved},
        )
    return resolved
```

New text:

```
            detail={"label": label, "unresolved": resolved.unresolved},
        )
    return setbuilder.Anchor(
        key=resolved.key, bpm=resolved.bpm, owned=True, display=resolved.display
    )
```

### `u98-a.U4_tempo_dropped`

unowned_anchor: pass no tempo to the engine, so --bpm is silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U4_tempo_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_supplied_tempo_narrows_an_unowned_anchor_to_its_band`
  - `tests/test_setbuilder_cli.py::test_an_owned_and_an_unowned_anchor_in_one_key_digest_apart`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_is_ranked_through_the_dispatcher`

Old text:

```
resolve_anchor(label, (), key=key, bpm=tempo)
```

New text:

```
resolve_anchor(label, (), key=key, bpm=None)
```

### `u98-a.X1_mutex`

build: declare the anchor and --unowned on the parser, not in an exclusive group

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `X1_mutex`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_invocation_the_flags_cannot_take_is_the_parsers_verdict[name-and-path]`
  - `tests/test_setbuilder_cli.py::test_an_invocation_the_flags_cannot_take_is_the_parsers_verdict[name-and-unowned]`
  - `tests/test_setbuilder_cli.py::test_an_invocation_the_flags_cannot_take_is_the_parsers_verdict[path-and-unowned]`

Old text:

```
    anchor = parser.add_mutually_exclusive_group()
```

New text:

```
    anchor = parser
```

### `u98-b.E1_existing_containment`

existing sample: anchor_path drops the library containment refusal

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `E1_existing_containment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_outside_the_library_refuses_before_any_scan`
  - `tests/test_setbuilder_cli.py::test_an_anchor_path_is_taken_against_the_library_and_never_walks_out_or_defaults`

Old text:

```
    if not _within(candidate, root):
```

New text:

```
    if False:
```

### `u98-b.S1_supplied_beside_path`

set_build: drop the refusal of --key or --bpm beside a path anchor, so both are silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `S1_supplied_beside_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[key-beside-name]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[key-beside-path]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[tempo-beside-path]`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if False:
```

### `u98-b.S2_tempo_half`

set_build: drop only the tempo half of that refusal

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `S2_tempo_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[tempo-beside-path]`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if ctx.args.key is not None:
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

### `u311.D1_stamp_name_unstripped`

A stamp line's name is not stripped, so a spaced version line is not found

- File: `src/cratekit/skills/cli.py`
- Source: `u311.json`, row `D1_stamp_name_unstripped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 8 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_clean_directory_gets_every_shipped_skill_with_a_stamp`
  - `tests/test_skills_install.py::test_a_file_a_previous_install_wrote_and_this_build_withdrew_disappears`
  - `tests/test_skills_install.py::test_a_file_the_product_never_wrote_survives_a_refresh`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_an_up_to_date_install_writes_nothing_at_all`
  - `tests/test_skills_install.py::test_install_one_reports_which_of_the_three_things_happened`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`

Old text:

```
            yield name.strip(), value
```

New text:

```
            yield name, value
```

### `r1289.M10_warning_ready_filter`

_plan_playlists: the unread warning covers a playlist that was not queued, saying its other tracks are

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M10_warning_ready_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 147 against a baseline of 147
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
- Collected: 147 against a baseline of 147
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
- Collected: 147 against a baseline of 147
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
- Collected: 147 against a baseline of 147
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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

### `u109-a.A1_plan_guided`

Plan every enabled source again, guided ones included, so labels is planned as a source with no worker

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A1_plan_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_an_explicit_toggle_puts_back_the_source_its_profile_leaves_out`
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
- Collected: 116 against a baseline of 116
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_explicit_toggle_puts_back_the_source_its_profile_leaves_out`
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
- Collected: 116 against a baseline of 116
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_profile_without_the_labels_module_names_no_guided_verb`
  - `tests/test_sync_all.py::test_an_explicit_toggle_puts_back_the_source_its_profile_leaves_out`
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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

### `u73-c.C3_next_only_with_intake_jobs`

Name intake missing --run on every pass, including one that queued no intake job

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C3_next_only_with_intake_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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

### `r1056.S1_no_landing_step_names_intake_missing`

_native_proof: drop the named source from the no landing step, so a label batch is told intake missing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r1056.json`, row `S1_no_landing_step_names_intake_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_sync_mark.py`
- Collected: 102 against a baseline of 102
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[abandoned]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[another-pass]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[never-committed]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[no-landing]`

Old text:

```
            f"land the pass with crate intake land --pass and {named}, then run {verb} "
```

New text:

```
            f"land the pass with crate intake land --pass and {SYNC_PASS_NAMED}, then run {verb} "
```

### `r1056.S2_unreachable_step_names_sync`

_native_proof: name sync mark in the unreachable library step whatever verb asked

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r1056.json`, row `S2_unreachable_step_names_sync`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_sync_mark.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_an_unreachable_library_names_label_mark_as_the_verb_to_run_again`

Old text:

```
            f"mount the library volume, then run {verb} again",
```

New text:

```
            "mount the library volume, then run crate sync mark again",
```

### `r361-a.A7_mark_verb_forgets_debris`

The mark verb's plan no longer decides label-debris, so the playlist falls through to the reports

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A7_mark_verb_forgets_debris`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
        elif playlists.is_library_debris(entry.name):
            entry.reason = LABEL_DEBRIS
        elif job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
        elif job.state is not jobs.JobState.SUCCEEDED:
```

### `r361-a.A8_mark_verb_respells_the_word`

The mark verb spells its own word for the reason instead of reading the enum

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A8_mark_verb_respells_the_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
LABEL_DEBRIS = str(playlists.Excluded.LABEL_DEBRIS)
```

New text:

```
LABEL_DEBRIS = "label-library"
```

### `r361-a.A9_reword_the_why`

The why sentence is reworded, never appended to, since the suite asserts with in

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A9_reword_the_why`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
        "its name is the source system's label run debris, which a sync never "
        "offers and never renames"
```

New text:

```
        "its name is a throwaway the other system left, which a sync never "
        "offers and never renames"
```

### `r777-confirm.N4_plain_name`

Confirm: _native_proof takes a pass name no landing could have been given, after the test that pins its message

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777-confirm.json`, row `N4_plain_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_pass_name_no_landing_could_have_been_given_is_refused`

Old text:

```
    if not landing.plain_name(name):
```

New text:

```
    if False:
```

### `r777-confirm.N7_digest_marks`

Confirm, the first table's old text was moved by the fix round: the native digest no longer covers the planned marks

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777-confirm.json`, row `N7_digest_marks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_answer_is_stale_once_another_playlist_becomes_whole`

Old text:

```
            "landings": list(proof.landings),
            "marks": planned,
```

New text:

```
            "landings": list(proof.landings),
```

### `r777.N10_screen_says_pass`

The gate screen on a native pass shows an intake file line instead of the pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N10_screen_says_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_whose_tracks_the_library_holds_is_marked_after_the_answer`

Old text:

```
        if isinstance(proof, marks.NativeLanding)
        else {"intake file": str(proof)}
```

New text:

```
        if False
        else {"intake file": str(proof)}
```

### `r777.N11_exclusive`

--xml and --pass are no longer one or the other

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N11_exclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_file_and_the_pass_are_one_or_the_other`

Old text:

```
    proof = parser.add_mutually_exclusive_group(required=True)
```

New text:

```
    proof = parser
```

### `r777.N12_no_landing_required`

_native_proof makes a proof when no closed landing of the pass committed

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N12_no_landing_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[abandoned]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[another-pass]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[never-committed]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[no-landing]`

Old text:

```
    if not landings:
        raise _blocked(
```

New text:

```
    if False:
        raise _blocked(
```

### `r777.N18_unreachable_called_bridge`

An unreachable library falls through to the bridge refusal

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N18_unreachable_called_bridge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_unreachable_library_is_named_and_never_called_the_bridge`

Old text:

```
    if medium.declared is None:
        # AN UNREACHABLE ROOT
```

New text:

```
    if False:
        # AN UNREACHABLE ROOT
```

### `r777.N19_digest_landings`

The native digest no longer covers the landings that prove the pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N19_digest_landings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_second_landing_of_the_pass_since_the_plan_makes_the_answer_stale`

Old text:

```
            "landings": list(proof.landings),

```

New text:

```
(empty)
```

### `r777.N5_bridge_accepted`

_native_proof accepts --pass on an intake tree still on the xml bridge

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N5_bridge_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_pass_named_on_a_tree_still_on_the_bridge_is_refused_naming_the_file`
  - `tests/test_sync_mark.py::test_a_tree_put_back_on_the_bridge_after_the_plan_renames_nothing`

Old text:

```
    if not medium.native:
        raise _blocked(
```

New text:

```
    if False:
        raise _blocked(
```

### `r777.N6_no_reread`

apply_pass no longer reads the proof again before the first rename

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N6_no_reread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_landing_recorded_between_the_plan_and_the_apply_renames_nothing`
  - `tests/test_sync_mark.py::test_a_tree_put_back_on_the_bridge_after_the_plan_renames_nothing`

Old text:

```
        if _native_proof(cfg, planned.name) != planned.native:
```

New text:

```
        if False:
```

### `r777.N9_proof_is_file`

PassPlan.proof hands the engine the absent file on a native pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N9_proof_is_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_takes_playlist_as_the_file_does`
  - `tests/test_sync_mark.py::test_a_native_pass_whose_tracks_the_library_holds_is_marked_after_the_answer`
  - `tests/test_sync_mark.py::test_a_native_pass_with_one_track_not_held_leaves_that_playlist_alone`
  - `tests/test_sync_mark.py::test_organize_marks_a_native_pass_through_its_gate`

Old text:

```
        return self.native if self.native is not None else self.xml
```

New text:

```
        return self.xml
```

### `u174.M10_dedupe`

plan_pass: keep a playlist named twice twice in the narrowing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M10_dedupe`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_playlist_repeated_takes_each_named_and_no_playlist_is_the_whole_pass`

Old text:

```
    named = tuple(dict.fromkeys(str(one) for one in playlists_named))
```

New text:

```
    named = tuple(str(one) for one in playlists_named)
```

### `u174.M11_stranger_before_no_jobs`

plan_pass: refuse a stranger only after the no jobs return, so a file of no pass given --playlist asks a gate

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M11_stranger_before_no_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate`

Old text:

```
    _refuse_strangers(named, found, name)
    if not found:
```

New text:

```
    if found:
        _refuse_strangers(named, found, name)
    if not found:
```

### `u174.M1_stranger_refusal`

plan_pass: drop the refusal of a named playlist that is not the pass's, so it plans nothing and says nothing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M1_stranger_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_playlist_of_no_pass_of_this_name_is_refused_before_the_account_is_listed`
  - `tests/test_sync_mark.py::test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate`

Old text:

```
    strangers = [identity for identity in named if identity not in held]
    if strangers:
```

New text:

```
    strangers = [identity for identity in named if identity not in held]
    if False:
```

### `u174.M2_narrowing`

plan_pass: drop the narrowing of the decided playlists, so --playlist plans the whole pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M2_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_already_marked_is_a_skip_and_not_a_refusal`
  - `tests/test_sync_mark.py::test_a_native_pass_takes_playlist_as_the_file_does`
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`
  - `tests/test_sync_mark.py::test_the_library_is_walked_only_for_the_named_playlist`

Old text:

```
        decided = [entry for entry in decided if entry.identity in named]
```

New text:

```
        decided = list(decided)
```

### `u174.M3_unfinished_refusal`

plan_pass: drop the refusal of a named playlist the pass did not complete, so it is shown as a skip

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M3_unfinished_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_job_failed_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_reports_cannot_be_read_is_refused_by_name`

Old text:

```
    unfinished = [entry for entry in decided if entry.reason in UNFINISHED]
    if unfinished:
```

New text:

```
    unfinished = [entry for entry in decided if entry.reason in UNFINISHED]
    if False:
```

### `u174.M4_unfinished_rows_outstanding`

UNFINISHED: leave out rows-outstanding, so a playlist with a missing track is a skip when named

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M4_unfinished_rows_outstanding`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`

Old text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

New text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE})
```

### `u174.M5_unfinished_job`

UNFINISHED: leave out job-unfinished, so a playlist whose job failed is a skip when named

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M5_unfinished_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_job_failed_is_refused_by_name`

Old text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

New text:

```
UNFINISHED = frozenset({REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

### `u174.M6_unfinished_reports`

UNFINISHED: leave out reports-unreadable, so a playlist whose reports cannot be read is a skip when named

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M6_unfinished_reports`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_reports_cannot_be_read_is_refused_by_name`

Old text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

New text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, ROWS_OUTSTANDING})
```

### `u174.M7_digest_names_the_narrowing`

_payload: leave the narrowing out of the digest, so an answer to one playlist's screen carries out the whole pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M7_digest_names_the_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_answer_to_the_narrowed_plan_does_not_carry_out_the_whole_pass`
  - `tests/test_sync_mark.py::test_playlist_repeated_takes_each_named_and_no_playlist_is_the_whole_pass`

Old text:

```
        identity["only"] = sorted(named)
```

New text:

```
        pass
```

### `u174.M8_screen_names_the_narrowing`

_shown: drop the gate screen's line naming the playlists the plan was narrowed to

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M8_screen_names_the_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`

Old text:

```
        shown[ONLY_SAID] = list(named)
```

New text:

```
        pass
```

### `u174.M9_verb_passes_the_flag`

sync_mark: hand plan_pass no playlists, so --playlist is parsed and ignored

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M9_verb_passes_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_playlist_of_no_pass_of_this_name_is_refused_before_the_account_is_listed`
  - `tests/test_sync_mark.py::test_an_answer_to_the_narrowed_plan_does_not_carry_out_the_whole_pass`
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`
  - `tests/test_sync_mark.py::test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate`

Old text:

```
        playlists_named=list(getattr(ctx.args, "playlist", None) or ()),
```

New text:

```
        playlists_named=(),
```

### `u174.P1_bridge_plans_no_native_pass`

native_passes: read native records on a tree on the bridge too, so every old record is planned as a refusal

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `P1_bridge_plans_no_native_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_tree_on_the_bridge_plans_no_native_record`

Old text:

```
    if not medium.native:
        return ()
    return native.landed_passes(cfg)
```

New text:

```
    return native.landed_passes(cfg)
```

### `u174.P2_unreachable_is_refused`

native_passes: read an unreachable root as no pass, so organize asks over a clean plan

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `P2_unreachable_is_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_unreachable_root_is_a_refused_step_and_never_no_pass`

Old text:

```
    if medium.declared is None:
        raise _blocked(
```

New text:

```
    if medium.declared is None:
        return ()
        raise _blocked(
```

### `u242.M21_mark_cli_already_marked_by_title`

sync mark: decide already marked by the title alone, so a taken playlist is planned again

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u242.json`, row `M21_mark_cli_already_marked_by_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_u242_taken.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_partial_failure_names_what_was_marked`

Old text:

```
        elif playlists.is_taken(identity, entry.name, sweep.taken):
```

New text:

```
        elif playlists.is_swept_name(entry.name):
```

### `u82-b.B5_not_listed_is_skipped`

_decided: drop the not listed reason, so the plan declares a rename of a playlist the account no longer has

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-b.json`, row `B5_not_listed_is_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_playlist_the_account_no_longer_lists_is_said_and_not_planned`

Old text:

```
        if not entry.name:
            entry.reason = NOT_LISTED
```

New text:

```
        if False:
            entry.reason = NOT_LISTED
```

### `u82-b.B6_a_failed_job_is_skipped`

_decided: drop the unfinished job reason, so a playlist whose tracks were never all resolved is read from whatever reports it has

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-b.json`, row `B6_a_failed_job_is_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_job_failed_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_playlist_whose_job_failed_is_said_and_not_planned`

Old text:

```
        elif job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
        elif False:
```

### `u82-b.B7_unread_reports_hold_the_playlist`

_decided: stop catching the report reader's refusal, so one damaged report refuses the whole verb and the whole playlists beside it are never marked

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-b.json`, row `B7_unread_reports_hold_the_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_reports_cannot_be_read_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_playlist_whose_reports_cannot_be_read_is_left_alone`

Old text:

```
        except CratekitError as exc:
            # UNREAD IS NOT NOTHING OWED.
```

New text:

```
        except ZeroDivisionError as exc:
            # UNREAD IS NOT NOTHING OWED.
```

### `u82-b.B8_an_offered_track_is_owed`

_NOT_FOUND: count only missing reports, which is what the manifest carried, so a playlist holding a track the pass offered for review is marked over it

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-b.json`, row `B8_an_offered_track_is_owed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_track_the_pass_offered_for_review_holds_its_playlist_back`

Old text:

```
_NOT_FOUND = frozenset({"missing", "offered"})
```

New text:

```
_NOT_FOUND = frozenset({"missing"})
```

### `u82-c.C1_a_tombstoned_track_is_settled`

_settle: drop the suppressed branch, so a track deleted on purpose since the pass holds its playlist back for ever

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-c.json`, row `C1_a_tombstoned_track_is_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_track_deleted_on_purpose_since_the_pass_is_not_owed`

Old text:

```
            elif found.state is match.MatchState.SUPPRESSED:
```

New text:

```
            elif False:
```

### `u82-c.C2_one_outstanding_track_holds_the_playlist`

_settle: never set the outstanding reason, so a playlist with a track still not in the library is planned for the prefix

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-c.json`, row `C2_one_outstanding_track_holds_the_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_native_answer_is_stale_once_another_playlist_becomes_whole`
  - `tests/test_sync_mark.py::test_a_native_pass_with_one_track_not_held_leaves_that_playlist_alone`
  - `tests/test_sync_mark.py::test_a_playlist_with_one_row_not_landed_is_not_marked`
  - `tests/test_sync_mark.py::test_a_track_deleted_on_purpose_since_the_pass_is_not_owed`
  - `tests/test_sync_mark.py::test_a_track_the_pass_offered_for_review_holds_its_playlist_back`
  - `tests/test_sync_mark.py::test_a_track_two_playlists_share_holds_both_back_until_it_lands`
  - `tests/test_sync_mark.py::test_an_answer_to_one_plan_does_not_carry_out_another`
  - `tests/test_sync_mark.py::test_the_pass_is_decided_without_its_manifest`

Old text:

```
        if entry.outstanding:
            entry.reason = ROWS_OUTSTANDING
```

New text:

```
        if False:
            entry.reason = ROWS_OUTSTANDING
```

### `u82-c.C3_landed_is_told_from_owned`

_settle: call every matched track landed, so the screen credits this landing with files it did not bring

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-c.json`, row `C3_landed_is_told_from_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_whose_tracks_the_library_holds_is_marked_after_the_answer`
  - `tests/test_sync_mark.py::test_a_row_the_library_holds_and_the_file_does_not_name_is_owned`

Old text:

```
                entry.settled[LANDED if held & named else OWNED] += 1
```

New text:

```
                entry.settled[LANDED] += 1
```

### `u82-c.C9_the_accounts_reason_is_kept`

_failed_part_way: treat a refusal the account raised as a defect, so a provider timeout is reported as internal-error

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-c.json`, row `C9_the_accounts_reason_is_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_refusal_the_record_raised_keeps_its_reason_and_names_what_was_marked`

Old text:

```
    if isinstance(exc, CratekitError):
        cause = exc.cause
```

New text:

```
    if False:
        cause = exc.cause
```

### `u82-d.B2_paths_compared_resolved_again`

The zero of u82-b re-measured after test_a_library_reached_through_a_link_still_reads_its_files_as_landed. _comparable: compare the spelled path and not the resolved one

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u82-d.json`, row `B2_paths_compared_resolved_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_library_reached_through_a_link_still_reads_its_files_as_landed`

Old text:

```
    return locations.norm_for_compare(str(Path(path).resolve()))
```

New text:

```
    return locations.norm_for_compare(str(path))
```

### `r838-c.R1_library_bound`

mark_record._recognize: accept a record written for another library

- File: `src/cratekit/sync/mark_record.py`
- Source: `r838-c.json`, row `R1_library_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_an_unreadable_record_refuses_rather_than_reading_as_empty[{"version": 1, "library_id": "another-library", "marks": []}]`

Old text:

```
        if library_id != self.cfg.library.volume_id:
```

New text:

```
        if False:
```

### `r838-c.R2_remark_clears`

mark_record.record_marked: append a second entry for a re-mark by the same pass rather than replacing the first

- File: `src/cratekit/sync/mark_record.py`
- Source: `r838-c.json`, row `R2_remark_clears`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_mark_after_an_unmark_clears_the_stamp`

Old text:

```
                    if (entry.pass_name, entry.playlist_id) == (pass_name, playlist_id):
                        entries[index] = fresh
                        break
```

New text:

```
                    if False:
                        entries[index] = fresh
                        break
```

### `r838-d.R3b_stamp_target`

mark_record.record_unmarked: stamp the playlist's mark under any pass, so another pass's mark reads as put back

- File: `src/cratekit/sync/mark_record.py`
- Source: `r838-d.json`, row `R3b_stamp_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`

Old text:

```
                if (entry.pass_name, entry.playlist_id) == (pass_name, playlist_id):
                    entries[index] = replace(entry, unmarked=when)
```

New text:

```
                if entry.playlist_id == playlist_id:
                    entries[index] = replace(entry, unmarked=when)
```

### `u242.M6_record_v1_reads_a_taken_key`

mark record: drop the version 1 branch, so a record written before U242 is refused for having no taken list

- File: `src/cratekit/sync/mark_record.py`
- Source: `u242.json`, row `M6_record_v1_reads_a_taken_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_unmark.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_version_one_record_reads_as_one_with_nothing_taken`

Old text:

```
        if version == 1:
            # BEFORE U242 NOTHING WAS TAKEN HERE. A version 1 record that
            # somehow carries the key is still read as it was written.
            return []
```

New text:

```
        if False:
            return []
```

### `u242.M9_take_overwrites_a_held_entry`

take: replace an entry still held, so a second taker's stamp replaces the first and the migration is not idempotent

- File: `src/cratekit/sync/mark_record.py`
- Source: `u242.json`, row `M9_take_overwrites_a_held_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_mark.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_take_is_idempotent_and_a_released_entry_is_taken_afresh`

Old text:

```
                elif not taken[at].held:
```

New text:

```
                elif True:
```

### `r777.N1_empty_proof`

marks.require_proof accepts a NativeLanding naming no tree, no pass or no landing

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N1_empty_proof`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_mark.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_engine_refuses_a_mark_with_neither_proof`

Old text:

```
        if not local_output.tree_id or not local_output.pass_name or not local_output.landings:
```

New text:

```
        if False:
```

### `r777.N2_neither_proof`

marks.require_proof hands anything that is not a NativeLanding to require_output, so None is no longer refused by name

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N2_neither_proof`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_mark.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_engine_refuses_a_mark_with_neither_proof`

Old text:

```
    if not isinstance(local_output, Path):
```

New text:

```
    if False:
```

### `r777.N3_engine_unchecked`

apply_deferred no longer checks its proof before renaming

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N3_engine_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_mark.py`
- Collected: 100 against a baseline of 100
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_external_marks_wait_for_local_output_and_recheck`
  - `tests/test_sync_mark.py::test_the_engine_refuses_a_mark_with_neither_proof`
  - `tests/test_sync_mark.py::test_the_file_check_makes_one_stat_and_refuses_whatever_it_raises`

Old text:

```
    require_proof(local_output)
    applied: list[str] = []
```

New text:

```
    applied: list[str] = []
```

### `u82-a.A1_stat_oserror_is_the_refusal`

require_output: stop turning an OSError out of the one stat into sync-marks-blocked, so a file gone at that moment is a bare FileNotFoundError again, which is R-398

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A1_stat_oserror_is_the_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 185 against a baseline of 185
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_that_did_not_land_is_offered_again_by_the_next_pass`
  - `tests/test_sync_all.py::test_a_mark_without_a_real_importable_file_renames_nothing`
  - `tests/test_sync_mark.py::test_a_missing_intake_file_refuses_the_verb_before_anything_is_listed`
  - `tests/test_sync_mark.py::test_the_file_check_makes_one_stat_and_refuses_whatever_it_raises`

Old text:

```
    except OSError as exc:
        raise _blocked(local_output, exc.strerror or type(exc).__name__) from exc
```

New text:

```
    except ZeroDivisionError as exc:
        raise _blocked(local_output, exc.strerror or type(exc).__name__) from exc
```

### `u82-a.A2_a_folder_is_not_a_file`

require_output: drop the regular file check, so a folder named like the intake file counts as the importable file

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A2_a_folder_is_not_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_folder_and_an_empty_file_are_not_an_importable_file`

Old text:

```
    if not stat.S_ISREG(found.st_mode):
```

New text:

```
    if False:
```

### `u82-a.A3_an_empty_file_is_not_proof`

require_output: drop the empty file check, so a zero byte file lets the renames through

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A3_an_empty_file_is_not_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 185 against a baseline of 185
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_without_a_real_importable_file_renames_nothing`
  - `tests/test_sync_mark.py::test_a_folder_and_an_empty_file_are_not_an_importable_file`

Old text:

```
    if found.st_size == 0:
```

New text:

```
    if False:
```

### `r1360.F1_walk_uncounted`

unpaged_calls: the walk past a first page is not counted

- File: `src/cratekit/sync/pair_calls.py`
- Source: `r1360.json`, row `F1_walk_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before3-order3]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[101-2]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[199-2]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[200-3]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[250-3]`

Old text:

```
    return UNPAGED_READ + math.ceil(beyond / (PLAYLIST_PAGE - 1))
```

New text:

```
    return UNPAGED_READ
```

### `r1360.F2_step_a_page`

unpaged_calls: each later request is counted as a whole new page

- File: `src/cratekit/sync/pair_calls.py`
- Source: `r1360.json`, row `F2_step_a_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[200-3]`

Old text:

```
math.ceil(beyond / (PLAYLIST_PAGE - 1))
```

New text:

```
math.ceil(beyond / PLAYLIST_PAGE)
```

### `r1360.F3_judged_without_walk`

judged_calls: a judged reading counts one unpaged request whatever its length

- File: `src/cratekit/sync/pair_calls.py`
- Source: `r1360.json`, row `F3_judged_without_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before3-order3]`

Old text:

```
    return listing_calls(count) + unpaged_calls(count)
```

New text:

```
    return listing_calls(count) + UNPAGED_READ
```

### `u220.C1_moves_head_rule`

pair_calls._moves: count the moves by the old head rule

- File: `src/cratekit/sync/pair_calls.py`
- Source: `u220.json`, row `C1_moves_head_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_tie.py`
- Collected: 306 against a baseline of 306
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before0-order0]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before1-order1]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before2-order2]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before3-order3]`

Old text:

```
    for one in reversed(before):
```

New text:

```
    for one in before:
```

### `u226.M24_estimate_no_unpaged`

pair_calls: a judged reading forecast at a listing's cost

- File: `src/cratekit/sync/pair_calls.py`
- Source: `u226.json`, row `M24_estimate_no_unpaged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair.py`
- Collected: 137 against a baseline of 137
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_add_is_counted_against_what_the_playlist_holds_after_its_removals[removes1-adds1]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[40-5-0]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before0-order0]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before1-order1]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before2-order2]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before3-order3]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[0-1]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[1-1]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[100-1]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[101-2]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[199-2]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[200-3]`
  - ... and 1 more, see the JSON sidecar

Old text:

```
UNPAGED_READ = 1

```

New text:

```
UNPAGED_READ = 0

```

### `u231.M24_forecast_without_the_settle_reading`

forecast: an order's settle reading is not counted

- File: `src/cratekit/sync/pair_calls.py`
- Source: `u231.json`, row `M24_forecast_without_the_settle_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_resume.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before1-order1]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before2-order2]`
  - `tests/test_sync_pair_calls.py::test_an_order_costs_its_reading_its_moves_and_one_settle_reading[before3-order3]`

Old text:

```
            calls += moves * (1 + REPARSE) + judged_calls(len(now))
```

New text:

```
            calls += moves * (1 + REPARSE)
```

### `u246.S7_pair_calls_before_empty`

account_write: an empty set of what the playlist held, so no removal is counted as taking anything

- File: `src/cratekit/sync/pair_calls.py`
- Source: `u246.json`, row `S7_pair_calls_before_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_resume.py`
- Collected: 46 against a baseline of 46
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_add_is_counted_against_what_the_playlist_holds_after_its_removals[removes1-adds1]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[40-5-0]`

Old text:

```
    held_before = set(now)
```

New text:

```
    held_before = set()
```

### `r1264.M14_check_unread_moved`

check: never read the unread tracks as moved, so a new unread track after the plan is written over

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1264.json`, row `M14_check_unread_moved`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_hold.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_track_turning_unreadable_between_the_plan_and_the_write_refuses_stale`

Old text:

```
            unread_moved = set(listing.unread) != {named.remote_id for named in one.unread}
```

New text:

```
            unread_moved = False
```

### `r1264.M15_check_unread_as_tuple`

check: compare the unread tracks by place, so tracks trading places refuses stale

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1264.json`, row `M15_check_unread_as_tuple`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_unread_tracks_trading_places_after_the_plan_is_not_stale`

Old text:

```
            unread_moved = set(listing.unread) != {named.remote_id for named in one.unread}
```

New text:

```
            unread_moved = tuple(listing.unread) != tuple(named.remote_id for named in one.unread)
```

### `r1385.M12_check_reads_no_job`

check: read no job at apply time, so a job another sync queued since the plan is queued again beside it

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1385.json`, row `M12_check_reads_no_job`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale`
  - `tests/test_sync_pair_hold.py::test_tracks_another_sync_queued_before_the_write_refuse_stale_not_twice`

Old text:

```
            for job in pair_jobs(cfg, store)
            for item in (job.payload or {}).get(intake_cli.TRACKS) or {}
        }
```

New text:

```
            for job in ()
            for item in (job.payload or {}).get(intake_cli.TRACKS) or {}
        }
```

### `r1420-b.B2_beyond_tail_unread_pinned`

sample: the part written check reads the kept tracks' order but not that this write's additions stand after them, measured again once a test pins it

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420-b.json`, row `B2_beyond_tail_unread_pinned`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`

Old text:

```
        if kept != [track for track in one.account_now if track in held] or (
            list(now) != kept + tail
        ):
```

New text:

```
        if kept != [track for track in one.account_now if track in held] or (
            list(now) != list(now)
        ):
```

### `r1420.B1_beyond_order_unread`

sample: the part written check never reads the order, whatever ordering says

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `B1_beyond_order_unread`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
    if not parts and not ordering:
```

New text:

```
    if not parts and ordering is None:
```

### `r1420.B3_beyond_removals_asked`

sample: the kept order is compared to the whole plan's reading, so a track this write took off reads as a reorder

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `B3_beyond_removals_asked`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_rekordbox_playlist_changed_after_this_run_wrote_it_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_inside_the_account_write_is_finished_without_writing_rekordbox_twice`
  - `tests/test_sync_pair_resume_one.py::test_a_track_withheld_on_the_part_written_playlist_refuses_stale`

Old text:

```
        if kept != [track for track in one.account_now if track in held] or (
```

New text:

```
        if kept != [track for track in one.account_now] or (
```

### `r1420.N1_fix_reverted`

the check leaves the order unread once ordering is marked, as before R-1420, so a person's reorder after an order that moved nothing is written over

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N1_fix_reverted`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return steps.has(STEP_ORDERING)
```

### `r1420.N2_moves_begun_ignored`

a pair whose moves began has its order read, so a continue of a stop part way through the moves refuses the moves' own order as moved

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N2_moves_begun_ignored`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_whose_moves_all_landed_finishes_on_the_continue`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return steps.has(STEP_ORDERING) and one.finishing_order
```

### `r1420.N3_finish_read_too`

a finish of a stopped order has its order read by the check, so a continue of a refused finish whose check lists the lag is held as moved rather than refused at the adapter

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N3_finish_read_too`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return steps.has(STEP_ORDERING) and steps.has(STEP_MOVING)
```

### `r1420.N5_order_always_read`

every part written pair has its order read, the moves' own included

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N5_order_always_read`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_whose_moves_all_landed_finishes_on_the_continue`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return False and steps.has(STEP_ORDERING)
```

### `r1420.N6_call_site_never_reads_order`

the check passes ordering as true for every part written pair, so no order is read once an account write began

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N6_call_site_never_reads_order`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
                why = _beyond(one, now, ordering=_ordered_by_this_run(one, of(one)))
```

New text:

```
                why = _beyond(one, now, ordering=True)
```

### `u209.C10_reverse_recheck`

check: run no recheck of a made rekordbox side's home before the write

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C10_reverse_recheck`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_brought_playlists_folder_gone_reads_as_one_sentence`
  - `tests/test_sync_pair_hold_every.py::test_a_rekordbox_name_taken_before_the_write_stops_every_pair_before_any_is_written`

Old text:

```
                    pair_reverse.recheck(db, one.home, one.change.order)
```

New text:

```
                    pass
```

### `u209.C11_home_of`

check: compare no home a made rekordbox side goes to with the plan's

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C11_home_of`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_brought_playlists_rekordbox_folder_archived_before_the_write_refuses_stale`

Old text:

```
                if now != one.home:
```

New text:

```
                if False:
```

### `u209.C12_brought_folder`

check: read no brought playlist taken out of its account folder

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C12_brought_folder`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_brought_playlist_taken_out_of_its_account_folder_before_the_write_refuses_stale`

Old text:

```
            if listing.get(one.target.account_id) != one.target.title:
```

New text:

```
            if False:
```

### `u209.C13_jobs_queued`

check: read no acquisitions another sync queued since the plan

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C13_jobs_queued`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale`
  - `tests/test_sync_pair_hold.py::test_tracks_another_sync_queued_before_the_write_refuse_stale_not_twice`

Old text:

```
            again = sorted(set(one.acquire) & now)
```

New text:

```
            again = []
```

### `u209.C3_withheld`

check: read no change in the account's withheld count

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C3_withheld`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_withheld_count_changed_before_the_write_refuses_stale`

Old text:

```
            elif withheld != one.withheld:
```

New text:

```
            elif False:
```

### `u209.C4_rekordbox_gone`

check: read no rekordbox playlist deleted or turned into a folder

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C4_rekordbox_gone`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_rekordbox_playlist_deleted_before_the_write_refuses_stale`

Old text:

```
            if there is None or there.removed or not there.plain:
                moved.append(
                    Moved(
                        REKORDBOX_SIDE,
                        one.target.rekordbox_id,
```

New text:

```
            if there is None:
                moved.append(
                    Moved(
                        REKORDBOX_SIDE,
                        one.target.rekordbox_id,
```

### `u209.C5_memberships`

check: read no moved rekordbox membership

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C5_memberships`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale`
  - `tests/test_sync_pair_hold.py::test_a_moved_list_is_checked_whichever_side_was_skipped`
  - `tests/test_sync_pair_hold.py::test_a_rekordbox_membership_changed_before_the_write_refuses_stale_and_names_it`
  - `tests/test_sync_pair_hold.py::test_both_sides_moved_are_both_named`
  - `tests/test_sync_pair_hold_every.py::test_a_made_pair_whose_rekordbox_side_moved_before_the_write_refuses_stale`

Old text:

```
            if there.memberships() != tuple(tuple(row) for row in one.rekordbox_before):
```

New text:

```
            if False:
```

### `u209.C6_discovered_place`

check: read no move of a discovered playlist's place

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C6_discovered_place`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_dragged_into_archive_before_the_write_refuses_stale`
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_moved_into_a_subfolder_before_the_write_refuses_stale`
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_moved_to_another_folder_before_the_write_refuses_stale`
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_moved_to_the_root_before_the_write_refuses_stale`
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_moved_where_discovery_never_pairs_refuses_stale`

Old text:

```
                if now_found is None or (now_found.folder, now_found.title) != (
```

New text:

```
                if False and (now_found.folder, now_found.title) != (
```

### `u209.C7_made_left_behind`

check: read no made pair dragged where no pair is kept

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C7_made_left_behind`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_made_pair_dragged_into_archive_before_the_write_refuses_stale`

Old text:

```
                why = pair_discover.left_behind(db, there, favorites=favorites, skip=skip)
                if why:
```

New text:

```
                why = pair_discover.left_behind(db, there, favorites=favorites, skip=skip)
                if False:
```

### `u209.C8_rows_gone`

check: read no row the plan adds gone from the collection

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C8_rows_gone`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_row_the_plan_adds_gone_before_the_write_stops_every_pair`

Old text:

```
            gone = sorted(set(one.change.adds) - set(playlist_pair.content(db, one.change.adds)))
```

New text:

```
            gone = []
```

### `u209.C9_unpaired_back`

check: read no let go playlist back where its pair is kept

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C9_unpaired_back`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_made_pair_let_go_in_archive_and_dragged_back_before_the_write_refuses_stale`

Old text:

```
            if not pair_discover.left_behind(db, there, favorites=favorites, skip=skip):
```

New text:

```
            if False:
```

### `u209.H1_offer_mismatch_ignored`

_held_plan: read back a held plan whatever offer the run recorded

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `H1_offer_mismatch_ignored`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_held_plan_other_than_the_offer_is_planned_again`

Old text:

```
    if moved:
        return None, 0, f"the held plan is not the plan {', '.join(moved)} showed"
```

New text:

```
    if False:
        return None, 0, f"the held plan is not the plan {', '.join(moved)} showed"
```

### `u210.R10_check_todo`

check: read every pair, a finished one included

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R10_check_todo`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue`

Old text:

```
    todo = [one for one in planned.pairs if not of(one).has(STEP_DONE)]
```

New text:

```
    todo = list(planned.pairs)
```

### `u210.R11_part_written`

check: read a part written existing pair exactly, as one not started

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R11_part_written`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_rekordbox_playlist_changed_after_this_run_wrote_it_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_inside_the_account_write_is_finished_without_writing_rekordbox_twice`
  - `tests/test_sync_pair_resume_one.py::test_a_track_lost_from_the_part_written_account_playlist_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_track_withheld_on_the_part_written_playlist_refuses_stale`

Old text:

```
            if one.target.new or of(one).has(STEP_ACCOUNT):
```

New text:

```
            if one.target.new:
```

### `u210.R12_our_folders`

check: read a folder this run made as not there for the pairs still to make in it

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R12_our_folders`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_ceiling_continue_above_the_hour_names_the_hour_and_finishes_the_run`
  - `tests/test_sync_pair_resume.py::test_a_ceiling_stop_after_three_of_five_pairs_is_finished_by_a_continue_of_the_run`
  - `tests/test_sync_pair_resume.py::test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue`
  - `tests/test_sync_pair_resume.py::test_a_title_taken_in_the_folder_before_the_continue_refuses_stale_naming_it`
  - `tests/test_sync_pair_resume.py::test_the_stop_names_the_run_and_the_calls_its_continue_needs`

Old text:

```
            folder_id = place.folder_id or our_folders.get(place.folder, "")
```

New text:

```
            folder_id = place.folder_id
```

### `u210.R14_asked_before`

_asked_before: compare what is asked now unchanged, so a continue after the run's own marks plans again

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R14_asked_before`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_ceiling_continue_above_the_hour_names_the_hour_and_finishes_the_run`
  - `tests/test_sync_pair_resume.py::test_a_ceiling_stop_after_three_of_five_pairs_is_finished_by_a_continue_of_the_run`
  - `tests/test_sync_pair_resume.py::test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue`
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[2-the make and the move]`
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[3-the move and the fill]`
  - `tests/test_sync_pair_resume.py::test_a_title_taken_in_the_folder_before_the_continue_refuses_stale_naming_it`
  - `tests/test_sync_pair_resume.py::test_a_track_put_on_a_part_made_playlist_before_the_continue_refuses_stale_naming_it`
  - `tests/test_sync_pair_resume.py::test_the_stop_names_the_run_and_the_calls_its_continue_needs`
  - `tests/test_sync_pair_resume_one.py::test_a_first_sync_named_by_hand_that_failed_after_its_mark_is_continued_on_its_plan`

Old text:

```
    return {**dict(asked), "targets": targets}
```

New text:

```
    return dict(asked)
```

### `u210.R18_beyond_order`

_beyond: read no order on a part written playlist

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R18_beyond_order`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`

Old text:

```
    if not parts and not ordering:
```

New text:

```
    if False:
```

### `u210.R19_beyond_gained`

_beyond: read no track gained

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R19_beyond_gained`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_track_put_on_a_part_made_playlist_before_the_continue_refuses_stale_naming_it`

Old text:

```
    gained = held - before - added
```

New text:

```
    gained = set()
```

### `u210.R20_beyond_lost`

_beyond: read no track lost

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R20_beyond_lost`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_track_lost_from_the_part_written_account_playlist_refuses_stale`

Old text:

```
    lost = (before - set(one.account_removes)) - held
```

New text:

```
    lost = set()
```

### `u210.R21_check_queued`

check: read the run's own queued job as another sync's

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R21_check_queued`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_job_queued_before_a_stop_is_not_queued_again_by_the_continue`

Old text:

```
    asking = [one for one in todo if one.acquire and not of(one).has(STEP_QUEUED)]
```

New text:

```
    asking = [one for one in todo if one.acquire]
```

### `u210.R22_landed_read`

check: read no rekordbox playlist this run's commit landed

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R22_landed_read`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_rekordbox_playlist_changed_after_this_run_wrote_it_refuses_stale`

Old text:

```
                _landed_moved(db, one, landed, moved)
```

New text:

```
                pass
```

### `u226.M20_check_no_lag`

check: a lagging listing is compared as read rather than named as moved

- File: `src/cratekit/sync/pair_check.py`
- Source: `u226.json`, row `M20_check_no_lag`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 267 against a baseline of 267
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved`

Old text:

```
            if listing.window == provider_listing.WINDOW_LAGS:
                # U226. Neither read
```

New text:

```
            if False:
                # U226. Neither read
```

### `u246.S12_pair_cli_made_here_empty`

pair: no account ids made this run, so discovery is told every pair, the ones this run made included, is already paired

- File: `src/cratekit/sync/pair_check.py`
- Source: `u246.json`, row `S12_pair_cli_made_here_empty`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[2-the make and the move]`

Old text:

```
            made_here = set(ours.values())
```

New text:

```
            made_here = set()
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

### `u198.D10_twins`

pair_discover: a twins folder is walked

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D10_twins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_cratekits_own_trees_and_the_favorites_folder_are_never_discovered`

Old text:

```
        if _attribute(top) == FOLDER and TWIN_FOLDER.fullmatch(top_name):
```

New text:

```
        if False:
```

### `u198.D11_two_homes`

pair_discover: two favourites playlists read as one home, hidden

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D11_two_homes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_two_favourites_playlists_leave_both_folders_out_and_say_so`

Old text:

```
        if len(named) > 1
```

New text:

```
        if len(named) > 2
```

### `u198.D2_favorites_home`

pair_discover: the one favourites home is walked like any folder

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D2_favorites_home`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_favourites_name_inside_another_apps_folder_does_not_unsettle_the_home`
  - `tests/test_sync_pair_discover.py::test_a_favourites_playlist_at_the_root_is_not_discovered`
  - `tests/test_sync_pair_discover.py::test_cratekits_own_trees_and_the_favorites_folder_are_never_discovered`

Old text:

```
            if not unsure:
                return
```

New text:

```
            if False:
                return
```

### `u198.D3_held`

pair_discover: a playlist a pair holds is found again

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D3_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_paired_playlist_is_not_listed_on_a_later_run`

Old text:

```
        if node_id in held:
            return
```

New text:

```
        if False:
            return
```

### `u198.D4_skip`

pair_discover: a playlist under a skipped folder is found

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D4_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_an_archive_playlist_is_listed_and_never_written`
  - `tests/test_sync_pair_discover.py::test_the_skip_list_is_the_configurations`
  - `tests/test_sync_pair_discover.py::test_two_favourites_playlists_leave_both_folders_out_and_say_so`

Old text:

```
        if skip_why:
```

New text:

```
        if False:
```

### `u198.D5_smart`

pair_discover: a smart playlist is found as a plain one

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D5_smart`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_smart_playlist_is_listed_not_paired`

Old text:

```
        if attribute != PLAIN:
```

New text:

```
        if False:
```

### `u198.D6_released`

pair_discover: a released playlist is found again

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D6_released`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_on_the_account_unpairs_stays_and_is_not_made_again`

Old text:

```
        if node_id in gone:
```

New text:

```
        if False:
```

### `u198.D7_twice`

pair_discover: two playlists of one title are both found

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D7_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_two_playlists_taking_one_title_refuse_that_title_only`

Old text:

```
        if counted[one.title] > 1:
```

New text:

```
        if counted[one.title] > 2:
```

### `u198.D8_top_names`

pair_discover: a top folder the taxonomy names is walked

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D8_top_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_cratekits_own_trees_and_the_favorites_folder_are_never_discovered`

Old text:

```
        if top_id in roots or top_name in names or top_id in foreign:
```

New text:

```
        if top_id in roots or top_id in foreign:
```

### `u198.D9_foreign`

pair_discover: another app's top folder is walked

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D9_foreign`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_favourites_name_inside_another_apps_folder_does_not_unsettle_the_home`
  - `tests/test_sync_pair_discover.py::test_another_apps_top_folder_is_never_discovered`

Old text:

```
        if top_id in roots or top_name in names or top_id in foreign:
```

New text:

```
        if top_id in roots or top_name in names:
```

### `u202.D1_skip`

home_of: a folder the skip list names is made in

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D1_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_home_of_refuses_each_place_it_cannot_decide`

Old text:

```
        if folder in set(str(one) for one in skip):
```

New text:

```
        if False:
```

### `u202.D2_two_tops`

home_of: two top folders of the name, the first is taken

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D2_two_tops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_home_of_refuses_each_place_it_cannot_decide`

Old text:

```
        if len(top) > 1:
```

New text:

```
        if len(top) > 2:
```

### `u202.D3_longest`

home_of: the shortest subfolder name is read first

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D3_longest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_home_of_reads_the_longest_subfolder_and_strips_the_prefix`

Old text:

```
            longest = max(len(named(row)) for row in fits)
```

New text:

```
            longest = min(len(named(row)) for row in fits)
```

### `u202.D5_name_taken`

home_of: a name the folder already holds is made again beside it

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D5_name_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_playlist_of_the_name_no_pair_holds_is_left_and_named`

Old text:

```
    if here:
        where = " / ".join(path) or "the rekordbox root"
```

New text:

```
    if False:
        where = " / ".join(path) or "the rekordbox root"
```

### `u202.D6_favourites`

home_of: the folder holding the favourites is made in

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u202.json`, row `D6_favourites`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_home_of_refuses_the_folder_holding_the_favourites`

Old text:

```
            _attribute(row) == PLAIN
            and named(row) == favorites
            and str(getattr(row, "ParentID", "") or "") in above
```

New text:

```
            False
```

### `u216.M11_paired_raw`

downloaded_copy: compare the paired title as it stands, its folder prefix kept

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M11_paired_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_in_a_created_folder_is_named_a_copy`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_downloaded_copy_names_the_paired_title_it_copies`

Old text:

```
        if name_of(folder, one).casefold() == wanted:
```

New text:

```
        if one.casefold() == wanted:
```

### `u216.M1_held_record_ignored`

before_adoption: a playlist the record says the folder held reads as new, so it is made in rekordbox

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M1_held_record_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_before_adoption_reads_the_record_first`

Old text:

```
        if account_id in held:
            return (
```

New text:

```
        if False:
            return (
```

### `u216.M2_created_folder_by_time`

before_adoption: drop the created folder answer, so an unrecorded created folder is read by time and its new playlists named

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M2_created_folder_by_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_created_folder_without_a_record_still_brings_in`
  - `tests/test_sync_pair_adopted.py::test_before_adoption_reads_the_record_first`

Old text:

```
    if created:
        return ""
    unrecorded = (
```

New text:

```
    unrecorded = (
```

### `u216.M4_no_time_reads_new`

before_adoption: a playlist with no creation time in an unrecorded folder reads as new

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M4_no_time_reads_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_a_creation_time_without_a_zone_is_no_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_or_a_creation_time_every_unpaired_playlist_is_named`

Old text:

```
    if made is None or made.tzinfo is None:
        return (
```

New text:

```
    if made is None or made.tzinfo is None:
        return "" if True else (
```

### `u216.M5_naive_time_trusted`

before_adoption: a creation time without a zone is compared as given

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M5_naive_time_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_a_creation_time_without_a_zone_is_no_time`

Old text:

```
    if made is None or made.tzinfo is None:
```

New text:

```
    if made is None:
```

### `u216.M7_time_rule_off`

before_adoption: an unrecorded folder's playlist with a time never reads as held

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M7_time_rule_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_creation_time_decides`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_moment_is_read_from_this_folders_own_pairs`

Old text:

```
    if made <= adopted:
```

New text:

```
    if False:
```

### `u242.M27_copy_pool_reads_no_taken`

pair discovery: a taken title with no prefix reads every taken playlist beside it, so two of one name are each the other's copy

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u242.json`, row `M27_copy_pool_reads_no_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_pair_adopted.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_prefixed_copy_beside_a_taken_original_is_still_its_copy`

Old text:

```
        if other_id != account_id and not (plain_taken and other_id in held)
```

New text:

```
        if other_id != account_id
```

### `u304-b.S7_walk_keeps_removed_nodes`

pair_discover._live_children: a removed playlist is read as live (again, with test_a_playlist_deleted_in_rekordbox_is_never_found)

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u304-b.json`, row `S7_walk_keeps_removed_nodes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_adopted.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_in_rekordbox_is_never_found`

Old text:

```
    live = [row for row in every if not rb_writer.node_removed(row)]
    children: dict[str, list[Any]] = {}
```

New text:

```
    live = list(every)
    children: dict[str, list[Any]] = {}
```

### `u304.S8_walk_root_sentinel`

pair_discover._live_children: a node under the root sentinel is not filed under the root

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u304.json`, row `S8_walk_root_sentinel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_adopted.py`
- Collected: 114 against a baseline of 114
- Kills: 87 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_created_folder_without_a_record_still_brings_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_in_a_created_folder_is_named_a_copy`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_playlist_no_pair_names_still_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_a_created_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_the_adopted_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_a_creation_time_without_a_zone_is_no_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_or_a_creation_time_every_unpaired_playlist_is_named`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_creation_time_decides`
  - ... and 72 more, see the JSON sidecar

Old text:

```
        if parent in rb_writer.ROOT_PARENT_SENTINELS:
            parent = ""
        children.setdefault(parent, []).append(row)
    return every, live, children
```

New text:

```
        children.setdefault(parent, []).append(row)
    return every, live, children
```

### `r1404.M1_disagreeing_base_ignored`

merge: a base whose two sides disagree on order no longer lets rekordbox lead, the defect R-1404 names

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M1_disagreeing_base_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_track_the_account_adds_is_placed_in_the_order_rekordbox_holds`
  - `tests/test_sync_pair_merge.py::test_only_the_tracks_both_sides_held_at_the_base_are_read_for_their_order`
  - `tests/test_sync_pair_merge.py::test_with_no_change_since_a_base_whose_sides_disagree_rekordbox_leads`

Old text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, base.account
        ):
```

New text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or False:
```

### `r1404.M2_rekordbox_move_ignored`

merge: rekordbox's own reorder since the base no longer leads, only a disagreeing base does

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M2_rekordbox_move_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_whole_sync_after_a_skipped_one_finishes_both_sides_from_the_old_base`
  - `tests/test_sync_pair.py::test_when_rekordbox_alone_reorders_the_account_follows`
  - `tests/test_sync_pair_merge.py::test_when_rekordbox_alone_reordered_its_order_wins`

Old text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, base.account
        ):
```

New text:

```
        if False or order_changed(
            base.rekordbox, base.account
        ):
```

### `r1404.M3_account_move_not_guarded`

merge: rekordbox leads over a disagreeing base even when the account changed order since it, so an account reorder no longer reaches rekordbox

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M3_account_move_not_guarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_when_both_sides_reorder_the_account_order_wins`
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_a_base_whose_sides_disagree_still_leads`
  - `tests/test_sync_pair_merge.py::test_the_stopped_writes_order_is_not_read_against_the_base`
  - `tests/test_sync_pair_merge.py::test_when_both_sides_reordered_the_account_order_wins`

Old text:

```
    elif base is not None and not order_changed(account.keys, base.account):
```

New text:

```
    elif base is not None:
```

### `r1404.M4_always_rekordbox`

merge: with neither side changed, rekordbox leads whatever the base, so a base whose sides agree takes the other tie between two additions

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M4_always_rekordbox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_base_whose_sides_agree_leaves_the_account_leading_when_neither_side_moved`
  - `tests/test_sync_pair_merge.py::test_only_the_tracks_both_sides_held_at_the_base_are_read_for_their_order`
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_against_the_account_s_base_not_the_account_now`
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_at_the_base_not_between_the_sides_now`

Old text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, base.account
        ):
```

New text:

```
        if True:
```

### `r1404.M5_disagreement_read_now`

merge: the disagreement is read between the sides as they stand now rather than at the base

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M5_disagreement_read_now`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_against_the_account_s_base_not_the_account_now`
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_at_the_base_not_between_the_sides_now`

Old text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, base.account
        ):
```

New text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            rekordbox.keys, account.keys
        ):
```

### `r1404.M6_disagreement_read_against_the_account_now`

merge: the base's rekordbox order is compared with the account as it stands, not the account's base

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M6_disagreement_read_against_the_account_now`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_against_the_account_s_base_not_the_account_now`

Old text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, base.account
        ):
```

New text:

```
        if order_changed(rekordbox.keys, base.rekordbox) or order_changed(
            base.rekordbox, account.keys
        ):
```

### `r1404.S1_default_leader`

sample: the account no longer leads by default, so a first sync and a both reordered pair take rekordbox's order

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `S1_default_leader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_when_both_sides_reorder_the_account_order_wins`
  - `tests/test_sync_pair_merge.py::test_a_base_is_read_as_before_whatever_the_order`
  - `tests/test_sync_pair_merge.py::test_a_base_whose_sides_agree_leaves_the_account_leading_when_neither_side_moved`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_reads_its_order_against_it_whatever_the_order`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_into_an_empty_rekordbox_side_is_led_by_the_account_whatever_the_order`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_whose_order_is_kept_leads_with_the_account`
  - `tests/test_sync_pair_merge.py::test_only_the_tracks_both_sides_held_at_the_base_are_read_for_their_order`
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_a_base_whose_sides_disagree_still_leads`
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_the_stopped_write_leads_whatever_else_moved`
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_against_the_account_s_base_not_the_account_now`
  - `tests/test_sync_pair_merge.py::test_the_base_s_disagreement_is_read_at_the_base_not_between_the_sides_now`
  - `tests/test_sync_pair_merge.py::test_the_stopped_writes_order_is_not_read_against_the_base`
  - `tests/test_sync_pair_merge.py::test_when_both_sides_reordered_the_account_order_wins`
  - `tests/test_sync_pair_merge.py::test_when_the_account_alone_reordered_its_order_wins`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    leader = ACCOUNT
    if stopped is not None:
```

New text:

```
    leader = REKORDBOX
    if stopped is not None:
```

### `r1404.S2_stopped_leader_again`

sample, U225: with no change since a stopped write, the side that led it no longer leads again

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `S2_stopped_leader_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_the_stopped_writes_order_is_not_read_against_the_base`
  - `tests/test_sync_pair_merge.py::test_with_no_change_since_the_stopped_write_the_side_that_led_it_leads_again`

Old text:

```
        elif not account_moved and stopped.leader == REKORDBOX:
```

New text:

```
        elif False:
```

### `r1416.M1_rekordbox_does_not_lead`

merge: a first sync whose account order is not kept is led by the account again, the defect R-1416 names

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `M1_rekordbox_does_not_lead`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_led_by_rekordbox_places_the_accounts_tracks_after_their_neighbours`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_whose_order_is_not_kept_leads_with_rekordbox`

Old text:

```
        # order rekordbox stands in, or the DJ's arrangement is lost for good.
        leader = REKORDBOX
```

New text:

```
        # order rekordbox stands in, or the DJ's arrangement is lost for good.
        leader = ACCOUNT
```

### `r1416.M2_order_kept_ignored`

merge: the flag is ignored, so a first sync under GIG READY or with every pair's order kept is led by rekordbox

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `M2_order_kept_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_whose_order_is_kept_leads_with_the_account`

Old text:

```
    elif base is None and not order_kept and rekordbox.keys:
```

New text:

```
    elif base is None and rekordbox.keys:
```

### `r1416.M3_empty_rekordbox_leads`

merge: an empty rekordbox side leads its first sync, so the gate says the order follows rekordbox's where it takes the account's

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `M3_empty_rekordbox_leads`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_into_an_empty_rekordbox_side_is_led_by_the_account_whatever_the_order`

Old text:

```
    elif base is None and not order_kept and rekordbox.keys:
```

New text:

```
    elif base is None and not order_kept:
```

### `r1416.M4_first_sync_unguarded`

merge: a pair whose order is not kept is led by rekordbox whatever its base, so an account reorder after the first sync no longer reaches rekordbox

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `M4_first_sync_unguarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_base_is_read_as_before_whatever_the_order`

Old text:

```
    elif base is None and not order_kept and rekordbox.keys:
```

New text:

```
    elif not order_kept and rekordbox.keys:
```

### `r1416.M5_stopped_write_yields`

merge: outside the scope a stopped write no longer decides the order, so the new first sync rule takes its place

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `M5_stopped_write_yields`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_reads_its_order_against_it_whatever_the_order`

Old text:

```
    if stopped is not None:
        # U225.
```

New text:

```
    if stopped is not None and order_kept:
        # U225.
```

### `r1416.M6_default_not_kept`

merge: the keyword's default reads the order as not kept, so a caller that says nothing is led by rekordbox on a first sync

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `M6_default_not_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_whose_order_is_kept_leads_with_the_account`

Old text:

```
    order_kept: bool = True,
```

New text:

```
    order_kept: bool = False,
```

### `r1416.S2_placed_after_neighbour`

sample, U130: a track only the following side holds goes to the start rather than after its neighbour

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1416.json`, row `S2_placed_after_neighbour`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 225 against a baseline of 225
- Kills: 22 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_short_account_listing_reads_nothing_as_removed`
  - `tests/test_sync_pair.py::test_a_skipped_account_side_is_finished_by_the_next_sync`
  - `tests/test_sync_pair.py::test_a_track_added_in_rekordbox_only_lands_on_the_account`
  - `tests/test_sync_pair.py::test_an_unmatched_rekordbox_track_is_named_and_stays_in_rekordbox`
  - `tests/test_sync_pair.py::test_the_first_sync_marks_the_pair_and_adds_only`
  - `tests/test_sync_pair_back.py::test_a_removal_rekordbox_kept_no_moment_for_keeps_the_track_and_names_the_call`
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_hold.py::test_a_held_plan_other_than_the_offer_is_planned_again`
  - `tests/test_sync_pair_hold.py::test_a_no_change_sync_of_a_linked_pair_makes_no_isrc_lookup`
  - `tests/test_sync_pair_hold.py::test_a_two_gate_sync_makes_one_plans_lookups`
  - `tests/test_sync_pair_hold.py::test_an_unreadable_held_plan_is_planned_again_and_says_why`
  - `tests/test_sync_pair_hold.py::test_answers_continued_in_later_commands_ask_nothing_when_nothing_moved`
  - `tests/test_sync_pair_merge.py::test_a_base_whose_sides_agree_leaves_the_account_leading_when_neither_side_moved`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_reads_its_order_against_it_whatever_the_order`
  - ... and 7 more, see the JSON sidecar

Old text:

```
        anchor += 1
        result.insert(anchor, key)
```

New text:

```
        result.insert(0, key)
```

### `u130-a.A1_removal_beats_addition`

A removal wins over an addition, so a track removed on one side and re-added on the other is dropped

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u130-a.json`, row `A1_removal_beats_addition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if added or not removed:
```

New text:

```
        if not removed:
```

### `u130-a.A5_new_tracks_appended`

A track only the other side holds goes to the end instead of after its predecessor

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u130-a.json`, row `A5_new_tracks_appended`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair.py`
- Collected: 126 against a baseline of 126
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_base_whose_sides_agree_leaves_the_account_leading_when_neither_side_moved`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_reads_its_order_against_it_whatever_the_order`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_led_by_rekordbox_places_the_accounts_tracks_after_their_neighbours`
  - `tests/test_sync_pair_merge.py::test_a_run_of_new_tracks_at_the_head_of_the_other_side_keeps_its_own_order`
  - `tests/test_sync_pair_merge.py::test_a_track_added_mid_list_on_the_other_side_keeps_its_place`
  - `tests/test_sync_pair_merge.py::test_a_track_the_account_adds_is_placed_in_the_order_rekordbox_holds`
  - `tests/test_sync_pair_merge.py::test_an_addition_is_kept_when_the_other_side_dropped_its_neighbour`

Old text:

```
        anchor += 1
        result.insert(anchor, key)
```

New text:

```
        result.append(key)
```

### `u130-a.A6_order_change_read_inverted`

Read an unchanged order as changed and a changed one as unchanged

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u130-a.json`, row `A6_order_change_read_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair.py`
- Collected: 126 against a baseline of 126
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_whole_sync_after_a_skipped_one_finishes_both_sides_from_the_old_base`
  - `tests/test_sync_pair.py::test_when_both_sides_reorder_the_account_order_wins`
  - `tests/test_sync_pair.py::test_when_rekordbox_alone_reorders_the_account_follows`
  - `tests/test_sync_pair_merge.py::test_a_base_is_read_as_before_whatever_the_order`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_a_track_the_account_adds_is_placed_in_the_order_rekordbox_holds`
  - `tests/test_sync_pair_merge.py::test_only_the_tracks_both_sides_held_at_the_base_are_read_for_their_order`
  - `tests/test_sync_pair_merge.py::test_order_changed_reads_only_the_tracks_both_held`
  - `tests/test_sync_pair_merge.py::test_rekordbox_reordered_since_a_base_whose_sides_disagree_leads`
  - `tests/test_sync_pair_merge.py::test_rekordbox_reordered_since_the_stopped_write_leads`
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_a_base_whose_sides_disagree_still_leads`
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_the_stopped_write_leads_whatever_else_moved`
  - `tests/test_sync_pair_merge.py::test_the_stopped_writes_order_is_not_read_against_the_base`
  - `tests/test_sync_pair_merge.py::test_when_both_sides_reordered_the_account_order_wins`
  - `tests/test_sync_pair_merge.py::test_when_rekordbox_alone_reordered_its_order_wins`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    return [key for key in now if key in held_then] != [key for key in base if key in held_now]
```

New text:

```
    return [key for key in now if key in held_then] == [key for key in base if key in held_now]
```

### `u202.M1_since`

pair_merge.merge: a moment at or before the base's sync is read as a known moment

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M1_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_merge.py::test_a_moment_at_or_before_the_base_sync_is_no_moment`

Old text:

```
        if since is not None and (since.tzinfo is None or not at > since):
            return None
```

New text:

```
        if False:
            return None
```

### `u202.M2_naive`

pair_merge.merge: a moment with no zone is read as a known moment

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M2_naive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_moment_with_no_zone_is_no_moment`

Old text:

```
        if not isinstance(at, datetime) or at.tzinfo is None:
```

New text:

```
        if not isinstance(at, datetime):
```

### `u202.M3_tie`

Call.outcome: a tie goes to the removal, so a track is lost on equal moments

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M3_tie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_tie_keeps_the_track`

Old text:

```
        return REMOVAL_LATER if self.removed_at > self.added_at else ADDITION_LATER
```

New text:

```
        return REMOVAL_LATER if self.removed_at >= self.added_at else ADDITION_LATER
```

### `u202.M4_unknown`

Call.outcome: an unknown moment lets the removal win

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M4_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_removed_on_the_account_and_put_back_in_rekordbox_is_kept`
  - `tests/test_sync_pair_back.py::test_a_removal_rekordbox_kept_no_moment_for_keeps_the_track_and_names_the_call`
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_in_rekordbox_after_the_account_took_it_out_stays_and_is_named`
  - `tests/test_sync_pair_merge.py::test_a_moment_at_or_before_the_base_sync_is_no_moment`
  - `tests/test_sync_pair_merge.py::test_a_moment_with_no_zone_is_no_moment`
  - `tests/test_sync_pair_merge.py::test_a_removal_on_one_side_and_a_re_add_on_the_other_keeps_the_track`
  - `tests/test_sync_pair_merge.py::test_a_removal_with_no_moment_never_beats_an_addition_and_is_called_unknown`
  - `tests/test_sync_pair_merge.py::test_an_account_removal_never_beats_a_rekordbox_addition`

Old text:

```
        if self.added_at is None or self.removed_at is None:
            return TIME_UNKNOWN
```

New text:

```
        if self.added_at is None or self.removed_at is None:
            return REMOVAL_LATER
```

### `u202.M5_adder`

pair_merge.merge: the adding side is mistaken for the removing one, so the moments are read off the wrong sides

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M5_adder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_in_rekordbox_after_the_account_took_it_out_stays_and_is_named`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`
  - `tests/test_sync_pair_merge.py::test_a_base_with_no_sync_moment_still_orders_two_known_moments`
  - `tests/test_sync_pair_merge.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_merge.py::test_a_tie_keeps_the_track`
  - `tests/test_sync_pair_merge.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`
  - `tests/test_sync_pair_merge.py::test_an_account_addition_later_than_a_rekordbox_removal_is_added_back_there`
  - `tests/test_sync_pair_merge.py::test_an_account_removal_never_beats_a_rekordbox_addition`

Old text:

```
                (ACCOUNT, account, rekordbox) if added_account else (REKORDBOX, rekordbox, account)
```

New text:

```
                (ACCOUNT, account, rekordbox) if not added_account else (REKORDBOX, rekordbox, account)
```

### `u202.M6_account_readded`

pair_merge.merge: a track the account put back is not read as added there (R-990 reopened)

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M6_account_readded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_back.py::test_a_removal_rekordbox_kept_no_moment_for_keeps_the_track_and_names_the_call`
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`
  - `tests/test_sync_pair_merge.py::test_a_base_with_no_sync_moment_still_orders_two_known_moments`
  - `tests/test_sync_pair_merge.py::test_a_moment_at_or_before_the_base_sync_is_no_moment`
  - `tests/test_sync_pair_merge.py::test_a_moment_with_no_zone_is_no_moment`
  - `tests/test_sync_pair_merge.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_merge.py::test_a_removal_with_no_moment_never_beats_an_addition_and_is_called_unknown`
  - `tests/test_sync_pair_merge.py::test_a_tie_keeps_the_track`
  - `tests/test_sync_pair_merge.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`

Old text:

```
            key not in then_account or key in account.readded
```

New text:

```
            key not in then_account
```

### `u202.M7_removal_kept`

pair_merge.merge: a call the removal won still keeps the track

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u202.json`, row `M7_removal_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`
- Collected: 164 against a baseline of 164
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_merge.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`

Old text:

```
            if call.kept:
                kept.add(key)
```

New text:

```
            if True:
                kept.add(key)
```

