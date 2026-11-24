# Mutation table: u335-before-08

Measured by `scripts/mutate.py` on 2026-11-24 04:59 UTC, branch `HEAD` at `b41c698d`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 257.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:59 UTC for commit `b41c698da363`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 41, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u225.M1_stopped_ignored` | `src/cratekit/sync/pair_merge.py` | user | 4 file(s) | 149 | 5 | killed |
| `u225.M2_rekordbox_since_dropped` | `src/cratekit/sync/pair_merge.py` | user | 4 file(s) | 149 | 2 | killed |
| `u225.M3_rekordbox_over_account` | `src/cratekit/sync/pair_merge.py` | user | 4 file(s) | 149 | 1 | killed |
| `u225.M5_leader_over_account` | `src/cratekit/sync/pair_merge.py` | user | 4 file(s) | 149 | 1 | killed |
| `u234.S2_sample_stopped_leader` | `src/cratekit/sync/pair_merge.py` | user | 6 file(s) | 313 | 3 | killed |
| `r1264.M18_identity_unread` | `src/cratekit/sync/pair_model.py` | user | 2 file(s) | 49 | 1 | killed |
| `r1394.P7_unknown_named_as_landed` | `src/cratekit/sync/pair_model.py` | user | 20 file(s) | 750 | 1 | killed |
| `r1394.P8_every_move_named_as_a_stop` | `src/cratekit/sync/pair_model.py` | user | 20 file(s) | 750 | 1 | killed |
| `u130-b.B7_set_playlist_in_scope` | `src/cratekit/sync/pair_model.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B8_tree_name_in_scope` | `src/cratekit/sync/pair_model.py` | user | 1 file(s) | 76 | 1 | killed |
| `u220.P2_session_tolerated` | `src/cratekit/sync/pair_model.py` | user | 10 file(s) | 306 | 2 | killed |
| `u221.R10_digest_without_the_hold` | `src/cratekit/sync/pair_model.py` | user | 3 file(s) | 154 | 1 | killed |
| `u226.M22_lagging_not_per_pair` | `src/cratekit/sync/pair_model.py` | user | 8 file(s) | 267 | 1 | killed |
| `r1264-composites.M7_account_add_filter` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 20 | 1 | killed |
| `r1264.M1_unread_dropped` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 95 | 17 | killed |
| `r1264.M2_unread_isrc_on_account` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 87 | 1 | killed |
| `r1264.M3_account_keys_listing_order` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 117 | 3 | killed |
| `r1264.M4_account_keys_filter` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 96 | 12 | killed |
| `r1264.M5_unread_keys_empty` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 66 | 4 | killed |
| `r1264.M6_base_strip` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 66 | 3 | killed |
| `r1264.M8_order_after_listing` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 117 | 3 | killed |
| `r1376.F11_leader_lost` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 4 | killed |
| `r1376.F3_call_site_gone` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 6 | killed |
| `r1376.F4_first_sync_unrecorded_only` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 1 | killed |
| `r1376.F5_first_sync_marked_only` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 318 | killed |
| `r1376.F6_every_sync_first` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 4 | killed |
| `r1383.M14_hold_before_awaiting` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 2 | killed |
| `r1383.M15_hold_before_twin` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 1 | killed |
| `r1383.M18_sampled_own_landed_step` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 1 | killed |
| `r1383.M2_hold_branch_removed` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 4 | killed |
| `r1383.M3_hold_without_isrc` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 1 | killed |
| `r1383.M4_hold_while_readable` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 27 | killed |
| `r1383.M5_hold_dropped_from_plan` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 2 | killed |
| `r1385.M10_reason_dropped` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 7 | killed |
| `r1385.M2_other_jobs_not_asked` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 6 | killed |
| `r1385.M4_plan_not_asked` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 3 | killed |
| `r1385.M6_ask_not_registered` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 3 | killed |
| `r1385.M8_own_reads_every_job` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 6 | killed |
| `r1385.M9_own_reads_no_job` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 8 | killed |
| `r1394.P4_finish_from_landed` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 2 | killed |
| `r1394.P5_finish_from_any_path_reading` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 6 | killed |
| `r1404.S3_scope_every_pair` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 13 | killed |
| `r1416.M10_cli_account_write_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 12 | killed |
| `r1416.M7_cli_tells_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 4 | killed |
| `r1416.M8_cli_tells_not_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 2 | killed |
| `r1416.M9_cli_scope_key_only` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 119 | killed |
| `r1416.S3_scope_under_the_folder` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 119 | killed |
| `r1418.F5_plans_reading_without_unread_ids` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1432-composites.C4_finish_reads_the_listing_unfinished` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 61 | killed |
| `r1432.E1_listed_rule_puts_it_first` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 18 | killed |
| `r1432.P3_target_id_no_longer_listed_put_back` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 3 | killed |
| `r1432.P4_target_id_already_held_put_twice` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 8 | killed |
| `r1432.P5_target_placed_by_the_listing` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 11 | killed |
| `r1432.P6_target_behind_the_first_held` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 19 | killed |
| `r1432.P8_placed_in_front_of_its_neighbour` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 22 | killed |
| `r1434.M1_write_that_sent_nothing_read_on_its_whole_path` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 2 | killed |
| `r1434.M2_plan_reads_a_write_that_sent_nothing_on_its_whole_path` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.M3_readable_move_after_a_write_that_sent_nothing_read_on_its_whole_path` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.M4_hold_promises_the_accounts_order_for_an_unread_move` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.M5_hold_withholds_the_lead_from_a_readable_reorder` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1434.S1_sent_nothing_off_path_waits_for_settled_readings` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 7 | killed |
| `r1434.S3_unread_track_placed_at_the_front` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 22 | killed |
| `r1434.S5_folded_base_keeps_unread_keys` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1446-b.C1_composite_no_unread_left_out` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 155 | 6 | killed |
| `r1446-c.F1_every_unread_kept_its_place` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 264 | 2 | killed |
| `r1446-c.F2_no_unread_id_read_as_moved` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 264 | 3 | killed |
| `r1446-c.F3_readable_ids_weighed_as_unread` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 264 | 3 | killed |
| `r1446.M14_plan_flag_dropped` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1446.M1_no_readable_check` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 6 | killed |
| `r1446.M4_unread_moved_not_set` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 7 | killed |
| `r1446.M8_no_settled_reading_reads_no_move` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1446.M9_unsettled_reading_compared` | `src/cratekit/sync/pair_plan.py` | maintainer | 10 file(s) | 394 | 1 | killed |
| `r1446.S1_u234_settled_reorder_never_leads` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 10 | killed |
| `r1446.S3_u225_finish_whatever_was_read` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 12 | killed |
| `r1453.S4_unread_keys_keep_a_readable_release` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 2 | killed |
| `r1453.U1_unread_keys_unaliased` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1453.U2_base_keeps_unread_keys` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1453.U4_removal_takes_only_the_linked_release` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1453.U5_account_keys_take_unread_only_rows` | `src/cratekit/sync/pair_plan.py` | user | 10 file(s) | 394 | 30 | killed |
| `u130-b.B1_short_base_unnarrowed` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B4_no_isrc_still_asked` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B5_readd_old_rule` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B6_requeue` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 76 | 3 | killed |
| `u198.C1_miss_reuse` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 168 | 2 | killed |
| `u198.C2_miss_isrc` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C3_unread_remembered` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C4_tie_remembered` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 168 | 1 | killed |
| `u202-composites.C3_composite` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 160 | 3 | killed |
| `u202.C1_after_synced` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 160 | 1 | killed |
| `u207.P1_pair_screens_remembered_miss` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 154 | 1 | killed |
| `u207.P2_pair_never_screens` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 154 | 2 | killed |
| `u208.M10_here_database_only` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 2 | killed |
| `u208.M11_alias_off` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 5 | killed |
| `u208.M18_held_there_asks_provider` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 1 | killed |
| `u208.M1_ask_any_agreeing` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 16 | killed |
| `u208.M24_alias_unfrozen` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 2 | killed |
| `u208.M2_old_tie_miss_reused` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 1 | killed |
| `u208.M4_tie_flag_dropped` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 97 | 2 | killed |
| `u208.M5_tied_rows_not_gathered` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 97 | 2 | killed |
| `u208.M9_here_lookup_dropped` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 143 | 2 | killed |
| `u221.R1_hold_only_a_twin` | `src/cratekit/sync/pair_plan.py` | user | 4 file(s) | 174 | 21 | killed |
| `u221.R2_recorded_hold_never_holds` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 9 | killed |
| `u221.R3_recorded_hold_holds_everything` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 8 | killed |
| `u221.R4_undated_not_held` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 2 | killed |
| `u221.R5_time_rule_never_holds` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 2 | killed |
| `u221.R6_time_rule_always_holds` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 2 | killed |
| `u221.R7_plan_ignores_the_hold` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 10 | killed |
| `u221.R8_hold_before_awaiting` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 78 | 1 | killed |
| `u225.M15_fold_despite_skip` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 1 | killed |
| `u225.M16_account_base_unfolded` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 1 | killed |
| `u225.M17_rekordbox_base_unfolded` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 1 | killed |
| `u225.M20_stopped_not_passed` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 3 | killed |
| `u226.M19_plan_no_hold` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 267 | 2 | killed |
| `u226.M21_plan_window_only` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 267 | 4 | killed |
| `u229.M15_wide_landed_needs_rest` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.M1_wide_landed_step` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 7 | killed |
| `u229.M3_wide_jobs_step` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.M4_wide_jobs_own_only` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.M5_wide_jobs_strict` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.M8_own_landing_first` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.S1_ambiguous_count` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 2 | killed |
| `u229.S2_own_landed_step` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 1 | killed |
| `u231.M15_pending_not_read` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 26 | killed |
| `u231.M16_shown_order_not_finished` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 3 | killed |
| `u231.M17_agreement_gap_ignored` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 1 | killed |
| `u231.M18_reading_before_the_moves_kept` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 1 | killed |
| `u231.M20_every_reading_kept` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 1 | killed |
| `u231.M22_root_playlist_named_gig_ready` | `src/cratekit/sync/pair_plan.py` | user | 20 file(s) | 750 | 1 | killed |
| `u234.O10_after_not_compared` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O11_after_not_replaced` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O12_kept_reading_of_any_run` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 2 | killed |
| `u234.O13_kept_reading_before_the_stop` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 2 | killed |
| `u234.O1_off_path_dropped_from_the_finish` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 21 | killed |
| `u234.O23_off_path_flag_on_every_finish` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O25_on_path_reading_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 5 | killed |
| `u234.O26_on_path_reading_keeps_the_order_after` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O27_settled_order_keeps_the_order_after` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O3_person_never_leads` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 10 | killed |
| `u234.O4_settled_order_read_as_moved` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 3 | killed |
| `u234.O5_unsettled_reading_read_as_settled` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 10 | killed |
| `u234.O6_reading_never_kept` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 13 | killed |
| `u234.O8_moved_reading_not_kept_afresh` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u234.O9_after_without_the_window` | `src/cratekit/sync/pair_plan.py` | user | 21 file(s) | 762 | 1 | killed |
| `u246.S10_pair_cli_started_empty` | `src/cratekit/sync/pair_plan.py` | user | 5 file(s) | 237 | 1 | killed |
| `u246.S11_pair_cli_served_empty` | `src/cratekit/sync/pair_plan.py` | user | 4 file(s) | 132 | 1 | killed |
| `u304.S1_file_code_read_through_its_module` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 97 | 5 | killed |
| `u304.S2_file_code_for_an_agreement` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 117 | 2 | killed |
| `u304.S4_pending_agreement_clock` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 135 | 1 | killed |
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
| `u202-composites.R2_confined` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202.R1_recheck_name` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202.W1_landed_then_raised` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1264.M19_warning` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 20 | 1 | killed |
| `r1264.M20_item` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 20 | 7 | killed |
| `r1383.M10_warning_never_said` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 137 | 5 | killed |
| `r1383.M12_unlisted_said_as_records` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 1 | killed |
| `r1383.M13_records_unnamed` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 2 | killed |
| `r1383.M16_zero_said_as_count` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 1 | killed |
| `r1383.M17_total_uncounted` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 108 | 2 | killed |
| `r1383.M6_gate_item_dropped` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 137 | 2 | killed |
| `r1383.M7_gate_item_side` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 108 | 2 | killed |
| `r1385.M13_warning_unsplit` | `src/cratekit/sync/pair_screen.py` | user | 8 file(s) | 292 | 1 | killed |
| `r1385.M14_warning_here_dropped` | `src/cratekit/sync/pair_screen.py` | user | 8 file(s) | 292 | 2 | killed |
| `r1432.P10_warning_says_it_stays` | `src/cratekit/sync/pair_screen.py` | user | 10 file(s) | 394 | 2 | killed |
| `u130-b.B9_stale_pair_blocks_all` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 1 | killed |
| `u198.C10_unpair_account_gone` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C11_unpair_rekordbox_gone` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 2 | killed |
| `u198.C12_archive_move` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 3 | killed |
| `u198.C5_folder_twice` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C6_folder_others` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C7_title_taken` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C8_folder_gone` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u202-composites.C10_reads_account` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 160 | 1 | killed |
| `u202-composites.C8_scope` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 160 | 1 | killed |
| `u202.C5_released` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 160 | 2 | killed |
| `u202.C7_twice` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 160 | 1 | killed |
| `u208.M6_facts_line_dropped` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 97 | 1 | killed |
| `u208.M7_totals_tied_zero` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 97 | 2 | killed |
| `u208.M8_item_flag_dropped` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 97 | 1 | killed |
| `u216-m14.M14_moment_any_folder` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 1 | killed |
| `u216.M13_unrecorded_off` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 3 | killed |
| `u216.M15_before_rule_off` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 10 | killed |
| `u216.M16_copy_rule_off` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 5 | killed |
| `u216.M18_copy_all_titles` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 2 | killed |
| `u216.M19_place_held_empty` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 7 | killed |
| `u221.R11_no_warning_per_twin` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 78 | 1 | killed |
| `u221.R9_gate_names_no_held_track` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 78 | 10 | killed |
| `u225.M24_unread_unsaid` | `src/cratekit/sync/pair_screen.py` | user | 19 file(s) | 662 | 2 | killed |
| `u234.O21_gate_says_on_path` | `src/cratekit/sync/pair_screen.py` | user | 21 file(s) | 762 | 2 | killed |
| `u234.O22_finishing_note_silent` | `src/cratekit/sync/pair_screen.py` | user | 21 file(s) | 762 | 3 | killed |
| `u304.S10_unpaired_default_side` | `src/cratekit/sync/pair_screen.py` | user | 4 file(s) | 189 | 2 | killed |
| `r1372.K19_passed_by_strict` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1372.K20_passed_by_any_pair` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1372.K21_made_pair_unmapped` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 2 | killed |
| `r1376.F14_finished_filter_gone` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1394.S10_later_unsent_write_hides_the_pending` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 3 | killed |

## Row definitions

### `u225.M1_stopped_ignored`

merge: a stopped write handed in is ignored and the order is read against the base

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u225.json`, row `M1_stopped_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 149 against a baseline of 149
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_reads_its_order_against_it_whatever_the_order`
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_rekordbox_reordered_since_the_stopped_write_leads`
  - `tests/test_sync_pair_merge.py::test_the_stopped_writes_order_is_not_read_against_the_base`
  - `tests/test_sync_pair_merge.py::test_with_no_change_since_the_stopped_write_the_side_that_led_it_leads_again`

Old text:

```
    if stopped is not None:
        # U225.
```

New text:

```
    if False:
        # U225.
```

### `u225.M2_rekordbox_since_dropped`

merge: rekordbox reordered since the stopped write does not lead

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u225.json`, row `M2_rekordbox_since_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 149 against a baseline of 149
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_a_first_sync_after_a_stopped_write_still_adds_only_and_reads_order_against_it`
  - `tests/test_sync_pair_merge.py::test_rekordbox_reordered_since_the_stopped_write_leads`

Old text:

```
        if order_changed(rekordbox.keys, stopped.rekordbox) and not account_moved:
```

New text:

```
        if False and not account_moved:
```

### `u225.M3_rekordbox_over_account`

merge: rekordbox reordered since leads even when the account was reordered since

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u225.json`, row `M3_rekordbox_over_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_the_stopped_write_leads_whatever_else_moved`

Old text:

```
        if order_changed(rekordbox.keys, stopped.rekordbox) and not account_moved:
```

New text:

```
        if order_changed(rekordbox.keys, stopped.rekordbox):
```

### `u225.M5_leader_over_account`

merge: the stopped write's leader leads even when the account was reordered since

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u225.json`, row `M5_leader_over_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_the_account_reordered_since_the_stopped_write_leads_whatever_else_moved`

Old text:

```
        elif not account_moved and stopped.leader == REKORDBOX:
```

New text:

```
        elif stopped.leader == REKORDBOX:
```

### `u234.S2_sample_stopped_leader`

sample, U225: the side that led the stopped write is not followed, so the account leads a finish

- File: `src/cratekit/sync/pair_merge.py`
- Source: `u234.json`, row `S2_sample_stopped_leader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_twins_hold.py`
- Collected: 313 against a baseline of 313
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_merge.py::test_the_stopped_writes_order_is_not_read_against_the_base`
  - `tests/test_sync_pair_merge.py::test_with_no_change_since_the_stopped_write_the_side_that_led_it_leads_again`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`

Old text:

```
        elif not account_moved and stopped.leader == REKORDBOX:
```

New text:

```
        elif False and not account_moved and stopped.leader == REKORDBOX:
```

### `r1264.M18_identity_unread`

PairPlan.identity: leave the unread ids out of the digest

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1264.json`, row `M18_identity_unread`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_hold.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_plan_whose_unread_tracks_differ_digests_differently`

Old text:

```
                {"unread": [named.remote_id for named in self.unread]} if self.unread else {}
```

New text:

```
                {} if self.unread else {}
```

### `r1394.P7_unknown_named_as_landed`

held message: a reading at a move whose landing is not known is named as before the moves accepted

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1394.json`, row `P7_unknown_named_as_landed`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`

Old text:

```
    elif at < write.landed:
```

New text:

```
    elif at <= write.landed:
```

### `r1394.P8_every_move_named_as_a_stop`

held message: every move accepted is named as a write that stopped part way

- File: `src/cratekit/sync/pair_model.py`
- Source: `r1394.json`, row `P8_every_move_named_as_a_stop`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`

Old text:

```
    elif write is None or write.moved:
```

New text:

```
    elif write is None:
```

### `u130-b.B7_set_playlist_in_scope`

A set's playlist may be paired

- File: `src/cratekit/sync/pair_model.py`
- Source: `u130-b.json`, row `B7_set_playlist_in_scope`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_label_playlist_is_not_a_pair`

Old text:

```
    if account_id in set_built:
```

New text:

```
    if False:
```

### `u130-b.B8_tree_name_in_scope`

A playlist under a top level node the taxonomy names is in scope

- File: `src/cratekit/sync/pair_model.py`
- Source: `u130-b.json`, row `B8_tree_name_in_scope`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_playlist_under_one_of_cratekits_trees_is_not_a_pair`

Old text:

```
    if any(node_id in roots for node_id, _name in chain) or top_name in names:
```

New text:

```
    if any(node_id in roots for node_id, _name in chain):
```

### `u220.P2_session_tolerated`

ORDER_REFUSALS: tolerate a rejected session too, so every later pair meets it

- File: `src/cratekit/sync/pair_model.py`
- Source: `u220.json`, row `P2_session_tolerated`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_tie.py`
- Collected: 306 against a baseline of 306
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_rejected_session_on_the_order_still_stops_the_whole_write`
  - `tests/test_sync_pair_order.py::test_the_order_refusals_that_stop_one_pair_are_the_two_an_order_raises`

Old text:

```
ORDER_REFUSALS = frozenset({"outbound-remove-refused", "unavailable-transient"})
```

New text:

```
ORDER_REFUSALS = frozenset({"outbound-remove-refused", "unavailable-transient", "credential-missing"})
```

### `u221.R10_digest_without_the_hold`

PairPlan.identity: leave the held tracks out of the digest, so an approval over one hold is read as approving another

- File: `src/cratekit/sync/pair_model.py`
- Source: `u221.json`, row `R10_digest_without_the_hold`
- Moved: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_the_plans_digest_moves_with_the_hold`

Old text:

```
                {"on_hold": sorted(named.remote_id for named in self.on_hold)}
                if self.on_hold
                else {}
```

New text:

```
                {}
```

### `u226.M22_lagging_not_per_pair`

PER_PAIR_REASONS: a lagging pair refuses the whole sync of every pair

- File: `src/cratekit/sync/pair_model.py`
- Source: `u226.json`, row `M22_lagging_not_per_pair`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_model.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 267 against a baseline of 267
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_lags_beside_a_partial_unpaged_read_holds_the_pair_and_says_why`

Old text:

```
        # U226. Its account playlist's window read lags its unpaged read.
        LAGGING,

```

New text:

```
(empty)
```

### `r1264-composites.M7_account_add_filter`

plan_pair: offer an unread track to the account as an addition, which already lists it; reached on a first sync, where no base strips the unread key

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264-composites.json`, row `M7_account_add_filter`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists`

Old text:

```
        if remote_of(key) and key not in unseen and key not in unread_keys
```

New text:

```
        if remote_of(key) and key not in unseen
```

### `r1264.M1_unread_dropped`

plan_pair: read no unread tracks off the listing, so an untitled track the base holds reads as taken off the account and its linked row is removed from rekordbox

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M1_unread_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_hold.py`
- Collected: 95 against a baseline of 95
- Kills: 17 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists`
  - `tests/test_sync_pair_unread.py::test_a_plan_whose_unread_tracks_differ_digests_differently`
  - `tests/test_sync_pair_unread.py::test_a_rekordbox_reorder_while_a_track_is_unread_reaches_the_account_and_stands`
  - `tests/test_sync_pair_unread.py::test_a_rekordbox_row_carrying_an_unread_tracks_isrc_is_not_added_to_the_account`
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing0-t4]`
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing1-t24]`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_track_naming_no_artist_is_unread_the_same_way`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_in_rekordbox_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_on_the_account_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            listing.unread,
            listing.order,
```

New text:

```
            {},
            listing.order,
```

### `r1264.M2_unread_isrc_on_account`

plan_pair: do not join an unread track's ISRC to the account's codes, so a rekordbox row carrying it asks the provider, which may name another release

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M2_unread_isrc_on_account`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_twins.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_rekordbox_row_carrying_an_unread_tracks_isrc_is_not_added_to_the_account`

Old text:

```
        code = match.isrc_token(one.isrc)
        if code:
```

New text:

```
        code = match.isrc_token(one.isrc)
        if False:
```

### `r1264.M3_account_keys_listing_order`

plan_pair: read the account's keys in the readable tracks' order, so a row's key sits at its readable release's place

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M3_account_keys_listing_order`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing0-t4]`
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing1-t24]`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`

Old text:

```
            for remote_id in (listed_order or account_now)
            if alias(remote_id) in readable_keys
```

New text:

```
            for remote_id in account_now
            if alias(remote_id) in readable_keys
```

### `r1264.M4_account_keys_filter`

plan_pair: keep an unread track's own key among the account's keys, so it reads as held on the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M4_account_keys_filter`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair.py`
- Collected: 96 against a baseline of 96
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_plan_whose_unread_tracks_differ_digests_differently`
  - `tests/test_sync_pair_unread.py::test_a_rekordbox_reorder_while_a_track_is_unread_reaches_the_account_and_stands`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_track_naming_no_artist_is_unread_the_same_way`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_in_rekordbox_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_on_the_account_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_a_track_turning_unreadable_between_the_plan_and_the_write_refuses_stale`
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`
  - `tests/test_sync_pair_unread.py::test_unread_tracks_trading_places_after_the_plan_is_not_stale`
  - `tests/test_sync_pair_unread.py::test_while_a_track_is_unread_a_rekordbox_removal_still_lands_on_the_account`

Old text:

```
            for remote_id in (listed_order or account_now)
            if alias(remote_id) in readable_keys
```

New text:

```
            for remote_id in (listed_order or account_now)
            if True
```

### `r1264.M5_unread_keys_empty`

plan_pair: no unread keys, so nothing is stripped from the base or kept from the account's additions

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M5_unread_keys_empty`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_twins.py`
- Collected: 66 against a baseline of 66
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`

Old text:

```
    unread_keys = {alias(remote_id) for remote_id in unread} - readable_keys
```

New text:

```
    unread_keys: set[str] = set()
```

### `r1264.M6_base_strip`

plan_pair: leave unread keys in the base account, so a row linked to an unread track reads as removed on the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M6_base_strip`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_twins.py`
- Collected: 66 against a baseline of 66
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`

Old text:

```
        if unread_keys:
            unseen |=
```

New text:

```
        if False:
            unseen |=
```

### `r1264.M8_order_after_listing`

plan_pair: compute the account order over the readable tracks only

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1264.json`, row `M8_order_after_listing`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing0-t4]`
  - `tests/test_sync_pair_unread.py::test_a_release_turning_unread_beside_a_readable_one_moves_nothing[listing1-t24]`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`

Old text:

```
        after = pair_merge.appended(listed_order or account_now, account_removes, account_adds)
```

New text:

```
        after = pair_merge.appended(account_now, account_removes, account_adds)
```

### `r1376.F11_leader_lost`

plan_pair: the stop is read as led by the account whatever side led it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F11_leader_lost`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_names_the_pair_as_finishing_the_stopped_run`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_says_the_account_was_read_off_the_moves_path`

Old text:

```
            leader=stopped_write.leader,
```

New text:

```
            leader=pair_merge.ACCOUNT,
```

### `r1376.F3_call_site_gone`

plan_pair: a first sync never asks for the stop on its account playlist

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F3_call_site_gone`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`

Old text:

```
    if stopped_write is None and first_sync:
        stopped_write = reader.first_stop(target.account_id)
```

New text:

```
    if False:
        stopped_write = reader.first_stop(target.account_id)
```

### `r1376.F4_first_sync_unrecorded_only`

plan_pair: a pair marked with no snapshot is not read as a first sync, so its earlier stop is kept out by the mark

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F4_first_sync_unrecorded_only`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble`

Old text:

```
    first_sync = held is None or held.first
```

New text:

```
    first_sync = held is None
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

### `r1376.F6_every_sync_first`

plan_pair: every sync reads the stop whatever its snapshot, so a stop the snapshot passed is finished again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F6_every_sync_first`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_a_fresh_sync_finished_is_left_behind_by_the_snapshot`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
    if stopped_write is None and first_sync:
```

New text:

```
    if stopped_write is None:
```

### `r1383.M14_hold_before_awaiting`

plan_pair: decide the landing hold before awaiting, so a track an earlier sync queued is shown held with the wrong remedy

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M14_hold_before_awaiting`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record`

Old text:

```
        if remote_id in queued_before:
            awaiting.append(names[key])
```

New text:

```
        if match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]:
            landing_unread.append(names[key])
        elif remote_id in queued_before:
            awaiting.append(names[key])
```

### `r1383.M15_hold_before_twin`

plan_pair: decide the landing hold before a twin's hold, so a twin's held track loses its sync release remedy

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M15_hold_before_twin`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record`

Old text:

```
        elif held_for_choice(held, remote_id, dates):
```

New text:

```
        elif match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]:
            landing_unread.append(names[key])
        elif held_for_choice(held, remote_id, dates):
```

### `r1383.M18_sampled_own_landed_step`

sampled U128 guard: _owned asks no landing made for this account playlist, so its own landed track is found only by the widened step

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M18_sampled_own_landed_step`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`

Old text:

```
        landed = _mirror_isrcs(reader, account_id)
```

New text:

```
        landed = {}
```

### `r1383.M2_hold_branch_removed`

plan_pair: never hold, so a track an unreadable landing record may have brought in is queued with the warning beside it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M2_hold_branch_removed`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_held_while_a_record_is_unread`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]
        ):
```

New text:

```
            False
        ):
```

### `r1383.M3_hold_without_isrc`

plan_pair: hold a track carrying no ISRC as well, so a track no landing could name waits on the record forever

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M3_hold_without_isrc`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_carrying_no_isrc_is_still_queued_beside_an_unreadable_record`

Old text:

```
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]
        ):
```

New text:

```
            reader.landings[1]
        ):
```

### `r1383.M4_hold_while_readable`

plan_pair: hold whenever the track carries an ISRC, so every new track waits though every record reads

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M4_hold_while_readable`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 27 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_still_queued`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[cancelled]`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[failed]`
  - `tests/test_sync_pair.py::test_a_track_this_pair_alone_lists_is_queued_once_beside_anothers_job`
  - `tests/test_sync_pair.py::test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row`
  - `tests/test_sync_pair.py::test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale`
  - `tests/test_sync_pair.py::test_another_pairs_job_that_no_longer_reads_stops_no_plan`
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - ... and 12 more, see the JSON sidecar

Old text:

```
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc")) and reader.landings[1]
        ):
```

New text:

```
            match.isrc_token((tracks.get(remote_id) or {}).get("isrc"))
        ):
```

### `r1383.M5_hold_dropped_from_plan`

plan_pair: build the pair with no held tracks, so the gate names none and the total counts none

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1383.json`, row `M5_hold_dropped_from_plan`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
        landing_unread=tuple(landing_unread),
```

New text:

```
        landing_unread=(),
```

### `r1385.M10_reason_dropped`

plan_pair: name a track another pair holds awaiting with no reason, so the gate never says which pair holds it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M10_reason_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
            awaiting.append(_with_reason(names[key], why))
```

New text:

```
            awaiting.append(names[key])
```

### `r1385.M2_other_jobs_not_asked`

_queued_elsewhere: ask no other pair's job, so a track another pair's pending job holds is queued again (the card's second scenario)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M2_other_jobs_not_asked`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
    for source, name in reader.held_by_jobs.get(remote_id, ()):
```

New text:

```
    for source, name in ():
```

### `r1385.M4_plan_not_asked`

_queued_elsewhere: ask nothing of this plan, so two pairs listing one lacking track queue it twice (the card's first scenario)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M4_plan_not_asked`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_the_runs_own_job_for_an_earlier_pair_stops_no_later_command`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
    asked = reader.asked.get(remote_id)
```

New text:

```
    asked = None
```

### `r1385.M6_ask_not_registered`

plan_pair: register nothing this pair asks to acquire, so a later pair of the plan queues it again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M6_ask_not_registered`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_the_runs_own_job_for_an_earlier_pair_stops_no_later_command`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
        reader.asked.setdefault(remote_id, (target.key, name))
```

New text:

```
        pass
```

### `r1385.M8_own_reads_every_job`

_queued: read every pair's job as this pair's own, so another pair's job is named with no pair and asked before a twin's hold

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M8_own_reads_every_job`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`

Old text:

```
        if any(source == account_id for source, _name in held)
```

New text:

```
        if held
```

### `r1385.M9_own_reads_no_job`

_queued: read none of this pair's own jobs, so its own queued track is named for no pair or held on a twin

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1385.json`, row `M9_own_reads_no_job`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`
  - `tests/test_sync_pair_back.py::test_a_missing_track_is_queued_once_and_then_awaits`
  - `tests/test_sync_pair_discover.py::test_an_unowned_track_added_on_the_account_is_queued_once_and_then_awaiting`
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`

Old text:

```
        if any(source == account_id for source, _name in held)
```

New text:

```
        if False
```

### `r1394.P4_finish_from_landed`

pending order: an agreed reading at the moves the provider accepted is finished from even with a move whose landing is not known after it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1394.json`, row `P4_finish_from_landed`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`

Old text:

```
        if not at or max(at) >= write.sent:
```

New text:

```
        if not at or max(at) >= write.landed:
```

### `r1394.P5_finish_from_any_path_reading`

pending order: any agreed reading on the moves' path is finished from, R-1394's own defect

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1394.json`, row `P5_finish_from_any_path_reading`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`

Old text:

```
        if not at or max(at) >= write.sent:
```

New text:

```
        if not at or max(at) >= 0:
```

### `r1404.S3_scope_every_pair`

sample, U231: every pair keeps the account's order, so a root pair's account is written rekordbox's order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1404.json`, row `S3_scope_every_pair`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 13 (killed)
- Killed:
  - `tests/test_sync_pair_root_order.py::test_a_hand_pairs_first_sync_outside_gig_ready_keeps_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_rekordbox_reorder_outside_gig_ready_stays_sync_after_sync`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_rekordbox_holds_is_appended_to_the_account_and_nothing_else_moves`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_tidal_holds_lands_after_its_neighbour_in_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_track_placed_in_rekordbox_outside_gig_ready_keeps_its_place`
  - `tests/test_sync_pair_root_order.py::test_after_the_first_sync_a_tidal_reorder_still_leads_and_a_rekordbox_reorder_stands`
  - `tests/test_sync_pair_root_order.py::test_an_account_addition_outside_gig_ready_is_placed_in_rekordbox_s_order`
  - `tests/test_sync_pair_settle.py::test_a_pair_outside_gig_ready_gets_no_order_write_and_its_membership_still_syncs`
  - `tests/test_sync_pair_settle.py::test_a_rekordbox_side_to_be_made_is_under_gig_ready_only_inside_the_folder`
  - `tests/test_sync_pair_settle.py::test_a_root_playlist_named_gig_ready_is_not_under_gig_ready`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_of_an_account_playlist_with_no_stop_is_planned_as_before`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_left_off_its_path_outside_gig_ready_leaves_rekordbox_untouched`

Old text:

```
    if cfg.outbound.pair_order_every_pair:
        return True
```

New text:

```
    if True:
        return True
```

### `r1416.M10_cli_account_write_kept`

pair_cli: the account write reads the order as always kept, so a root pair's first sync writes rekordbox's order onto the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M10_cli_account_write_kept`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_root_order.py::test_a_hand_pairs_first_sync_outside_gig_ready_keeps_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_rekordbox_reorder_outside_gig_ready_stays_sync_after_sync`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_rekordbox_holds_is_appended_to_the_account_and_nothing_else_moves`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_tidal_holds_lands_after_its_neighbour_in_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_track_placed_in_rekordbox_outside_gig_ready_keeps_its_place`
  - `tests/test_sync_pair_root_order.py::test_after_the_first_sync_a_tidal_reorder_still_leads_and_a_rekordbox_reorder_stands`
  - `tests/test_sync_pair_root_order.py::test_an_account_addition_outside_gig_ready_is_placed_in_rekordbox_s_order`
  - `tests/test_sync_pair_settle.py::test_a_pair_outside_gig_ready_gets_no_order_write_and_its_membership_still_syncs`
  - `tests/test_sync_pair_settle.py::test_a_root_playlist_named_gig_ready_is_not_under_gig_ready`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_of_an_account_playlist_with_no_stop_is_planned_as_before`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_left_off_its_path_outside_gig_ready_leaves_rekordbox_untouched`

Old text:

```
        order_unkept = wanted_keys != firsts and not order_kept
```

New text:

```
        order_unkept = False
```

### `r1416.M7_cli_tells_kept`

pair_cli: the merge is always told the order is kept, so a root pair's first sync puts rekordbox in the account's order again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M7_cli_tells_kept`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_root_order.py::test_a_hand_pairs_first_sync_outside_gig_ready_keeps_rekordbox_s_order`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_rekordbox_holds_is_appended_to_the_account_and_nothing_else_moves`
  - `tests/test_sync_pair_root_order.py::test_a_track_only_tidal_holds_lands_after_its_neighbour_in_rekordbox_s_order`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_of_an_account_playlist_with_no_stop_is_planned_as_before`

Old text:

```
        order_kept=order_kept,
```

New text:

```
        order_kept=True,
```

### `r1416.M8_cli_tells_not_kept`

pair_cli: the merge is always told the order is not kept, so a GIG READY pair's first sync keeps rekordbox's order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M8_cli_tells_not_kept`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_root_order.py::test_a_hand_pairs_first_sync_with_every_pairs_order_kept_follows_tidal`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_of_an_account_playlist_with_no_stop_under_gig_ready_follows_the_account`

Old text:

```
        order_kept=order_kept,
```

New text:

```
        order_kept=False,
```

### `r1416.M9_cli_scope_key_only`

pair_cli: the flag read before the merge is the config key alone, so a GIG READY pair reads as not kept

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `M9_cli_scope_key_only`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 119 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_the_account_still_stands_in_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[refused]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_the_run_puts_the_refused_pair_in_order_and_moves_nothing_else`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`
  - `tests/test_sync_pair_order.py::test_a_first_order_is_asked_with_nothing_to_agree_with_but_what_the_adapter_wrote`
  - ... and 104 more, see the JSON sidecar

Old text:

```
    order_kept = _keeps_order(cfg, rekordbox, home)
```

New text:

```
    order_kept = cfg.outbound.pair_order_every_pair
```

### `r1416.S3_scope_under_the_folder`

sample, U231: a playlist under GIG READY is no longer read as kept, so its first sync is led by rekordbox

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1416.json`, row `S3_scope_under_the_folder`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 119 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_the_account_still_stands_in_finishes_it`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[refused]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_the_run_puts_the_refused_pair_in_order_and_moves_nothing_else`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`
  - `tests/test_sync_pair_order.py::test_a_first_order_is_asked_with_nothing_to_agree_with_but_what_the_adapter_wrote`
  - ... and 104 more, see the JSON sidecar

Old text:

```
        return bool(rekordbox.ancestors) and rekordbox.top[1] == ORDER_FOLDER
```

New text:

```
        return False
```

### `r1418.F5_plans_reading_without_unread_ids`

existing guard, R-1264: the plan's reading of an account it orders is the readable tracks alone, unread ids left out of it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1418.json`, row `F5_plans_reading_without_unread_ids`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`

Old text:

```
            account_before = tuple(listed_order or account_now)
```

New text:

```
            account_before = tuple(account_now)
```

### `r1432-composites.C4_finish_reads_the_listing_unfinished`

what E4 holds: at a finish the readable tracks are read as the account lists them, with the stopped write's remaining moves not applied, so its half done order is read as the account's

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432-composites.json`, row `C4_finish_reads_the_listing_unfinished`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 61 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_with_no_unread_track_is_put_in_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_first_move_refused_on_its_412s_is_sent_again_from_the_start_once`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - ... and 46 more, see the JSON sidecar

Old text:

```
                for one in pair_stopped.finished(
                    listed_order or account_now, stopped_write.target
                )
```

New text:

```
                for one in (listed_order or account_now)
```

### `r1432.E1_listed_rule_puts_it_first`

existing guard, R-1264: an unread track not named by a target goes to the front rather than behind the track listed before it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `E1_listed_rule_puts_it_first`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered5-listed5-target5-expected5]`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        placed.insert(behind(listed[:index]), one)
```

New text:

```
        placed.insert(0, one)
```

### `r1432.P3_target_id_no_longer_listed_put_back`

an unread id the target names and the account no longer lists is put back into the asked order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P3_target_id_no_longer_listed_put_back`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered3-listed3-target3-expected3]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered6-listed6-target6-expected6]`

Old text:

```
        if one in held or one not in holding:
```

New text:

```
        if one in held:
```

### `r1432.P4_target_id_already_held_put_twice`

a target id the order already holds, a readable track, is inserted again, so the asked order holds it twice

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P4_target_id_already_held_put_twice`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered3-listed3-target3-expected3]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered4-listed4-target4-expected4]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered5-listed5-target5-expected5]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered6-listed6-target6-expected6]`
  - `tests/test_sync_pair_stopped_order.py::test_rekordbox_reordered_since_the_stop_leads`

Old text:

```
        if one in held or one not in holding:
```

New text:

```
        if one not in holding:
```

### `r1432.P5_target_placed_by_the_listing`

each unread id the target names is placed behind the track the listing shows before it, not the one the target puts before it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P5_target_placed_by_the_listing`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 11 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered3-listed3-target3-expected3]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered4-listed4-target4-expected4]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered5-listed5-target5-expected5]`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
        placed.insert(behind(target[:index]), one)
```

New text:

```
        placed.insert(behind(listed[: list(listed).index(one)]), one)
```

### `r1432.P6_target_behind_the_first_held`

an unread id is placed behind the first track the target puts before it that the order holds, not the nearest

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P6_target_behind_the_first_held`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        for one in reversed(before):
```

New text:

```
        for one in before:
```

### `r1432.P8_placed_in_front_of_its_neighbour`

an unread id is put in front of the track it follows rather than behind it, the target's and the listing's alike (R-1418's F6, in this unit's shape)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1432.json`, row `P8_placed_in_front_of_its_neighbour`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 22 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
                return placed.index(one) + 1
```

New text:

```
                return placed.index(one)
```

### `r1434.M1_write_that_sent_nothing_read_on_its_whole_path`

round two's shape: a write known to have sent no move is read against its whole path, so a person's drag of one track to the top, where its first move would have put it, is finished over

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M1_write_that_sent_nothing_read_on_its_whole_path`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`

Old text:

```
    return tuple(write.start) if write.sent_nothing else tuple(write.target)
```

New text:

```
    return tuple(write.target)
```

### `r1434.M2_plan_reads_a_write_that_sent_nothing_on_its_whole_path`

the plan's path read alone back on the whole path for a write that sent no move, R-1446's check of a readable move keeping the start

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M2_plan_reads_a_write_that_sent_nothing_on_its_whole_path`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`

Old text:

```
            stopped_write.start, _toward(stopped_write), reading
```

New text:

```
            stopped_write.start, stopped_write.target, reading
```

### `r1434.M3_readable_move_after_a_write_that_sent_nothing_read_on_its_whole_path`

R-1446's check of a readable move alone back on the whole path for a write that sent no move, so a drag of a readable track to the top with an unread track listed reads as an unread move

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M3_readable_move_after_a_write_that_sent_nothing_read_on_its_whole_path`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`

Old text:

```
        return not pair_stopped.reached(write.start, _toward(write), readable)
```

New text:

```
        return not pair_stopped.reached(write.start, write.target, readable)
```

### `r1434.M4_hold_promises_the_accounts_order_for_an_unread_move`

the hold while a move of unread tracks alone settles says the account's order is then read as the person's, though the others are finished in the stopped order

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M4_hold_promises_the_accounts_order_for_an_unread_move`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`

Old text:

```
            if unread and not _readable_moved(write, kept, reading, unread, moved_nothing=False)
```

New text:

```
            if False
```

### `r1434.M5_hold_withholds_the_lead_from_a_readable_reorder`

the hold while a reorder of readable tracks settles says the others are finished in the stopped order, though the account's order then leads

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `M5_hold_withholds_the_lead_from_a_readable_reorder`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`

Old text:

```
            if unread and not _readable_moved(write, kept, reading, unread, moved_nothing=False)
```

New text:

```
            if True
```

### `r1434.S1_sent_nothing_off_path_waits_for_settled_readings`

existing guard, U234: an order off the path of a write known to have sent no move no longer leads at once

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `S1_sent_nothing_off_path_waits_for_settled_readings`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_finish_stopped_before_its_first_send_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_this_version_recorded_with_no_move_sent_leaves_a_reorder_the_persons`

Old text:

```
        moved_nothing = off_path and stopped_write.sent_nothing
```

New text:

```
        moved_nothing = False
```

### `r1434.S3_unread_track_placed_at_the_front`

existing guard, R-1264: an unread track a reorder does not move is put at the front rather than behind the track listed before it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `S3_unread_track_placed_at_the_front`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 22 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered0-listed0-target0-expected0]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered1-listed1-target1-expected1]`
  - `tests/test_sync_pair_settle.py::test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target[ordered2-listed2-target2-expected2]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
                return placed.index(one) + 1
```

New text:

```
                return 0
```

### `r1434.S5_folded_base_keeps_unread_keys`

existing guard, R-1264: the base keeps an unread track's key, so it is read as taken off the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1434.json`, row `S5_folded_base_keeps_unread_keys`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`

Old text:

```
            base_account = tuple(key for key in base_account if key not in unread_keys)
```

New text:

```
            base_account = tuple(base_account)
```

### `r1446-b.C1_composite_no_unread_left_out`

the composite of r1446 rows M10 and M11, what they hold together: the settled reading and the reading now both compared with their unread ids in place, so a move of an unread track alone reads as a reorder again; either filter alone is equivalent, since reordered reads only the tracks both readings hold

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446-b.json`, row `C1_composite_no_unread_left_out`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 155 against a baseline of 155
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_settled_reorder_moved_a_readable_track_only_when_one_moved[kept0-reading0-unread0-False]`
  - `tests/test_sync_pair_settle.py::test_a_settled_reorder_moved_a_readable_track_only_when_one_moved[kept4-reading4-unread4-False]`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
        [one for one in kept.order if one not in left_out], readable
```

New text:

```
        list(kept.order), list(reading)
```

### `r1446-c.F1_every_unread_kept_its_place`

round one's BLOCKING reverted: once only unread tracks moved, no target at all, so an unread track nobody moved keeps the interrupted move's place

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446-c.json`, row `F1_every_unread_kept_its_place`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`
- Collected: 264 against a baseline of 264
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
                    else tuple(one for one in stopped_write.target if one not in moved_unread)
```

New text:

```
                    else ()
```

### `r1446-c.F2_no_unread_id_read_as_moved`

every unread id read as unmoved, so the one the person moved is put where the stopped order was taking it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446-c.json`, row `F2_no_unread_id_read_as_moved`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`
- Collected: 264 against a baseline of 264
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_the_unread_tracks_moved_since_the_stop_are_those_off_the_order_both_readings_share`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
    return frozenset(one for one in now if one in left_out and one not in held)
```

New text:

```
    return frozenset()
```

### `r1446-c.F3_readable_ids_weighed_as_unread`

the shared run unweighted, so it may keep unread ids in place of a readable one and read the wrong unread track as moved

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446-c.json`, row `F3_readable_ids_weighed_as_unread`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`
- Collected: 264 against a baseline of 264
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_the_unread_tracks_moved_since_the_stop_are_those_off_the_order_both_readings_share`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
        value = top[0] + (1 if one in left_out else heavy)
```

New text:

```
        value = top[0] + 1
```

### `r1446.M14_plan_flag_dropped`

the plan never carries the flag, so the gate says the stopped order takes the unread track where it was taking it and never that only unread tracks moved

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `M14_plan_flag_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`

Old text:

```
        stop_unread_moved=unread_moved,
```

New text:

```
        stop_unread_moved=False,
```

### `r1446.M1_no_readable_check`

the card's row: a reorder read after a stop stands whatever it moved, so a settled move of an unread track alone lets the account lead and undoes rekordbox's reorder

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `M1_no_readable_check`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
            reordered_since_stop
            and unread
            and not _readable_moved(
```

New text:

```
            False
            and unread
            and not _readable_moved(
```

### `r1446.M4_unread_moved_not_set`

the flag never set, so the finish places the moved unread track by the stopped write's target, over the person's place, and the gate says the stopped order takes it there

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `M4_unread_moved_not_set`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`

Old text:

```
            moved_nothing = False
            unread_moved = True
```

New text:

```
            moved_nothing = False
```

### `r1446.M8_no_settled_reading_reads_no_move`

with no settled reading kept, the reorder is read as moving no readable track, so a reorder U234 read is dropped

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `M8_no_settled_reading_reads_no_move`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_with_no_settled_reading_a_reorder_stands_as_read`

Old text:

```
    if kept is None or not kept.settled:
        return True
```

New text:

```
    if kept is None or not kept.settled:
        return False
```

### `r1446.M9_unsettled_reading_compared`

an unsettled kept reading compared as though settled; unreachable while U234 reads a reorder only from a settled one

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `M9_unsettled_reading_compared`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_with_no_settled_reading_a_reorder_stands_as_read`

Old text:

```
    if kept is None or not kept.settled:
```

New text:

```
    if kept is None:
```

### `r1446.S1_u234_settled_reorder_never_leads`

sample, U234: a reorder settled readings show never leads

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `S1_u234_settled_reorder_never_leads`
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`

Old text:

```
        and pair_model._now() - since >= AGREE_AFTER
    ):
        return True
```

New text:

```
        and pair_model._now() - since >= AGREE_AFTER
    ):
        return False
```

### `r1446.S3_u225_finish_whatever_was_read`

sample, U225: the stop finished even when a reorder was read

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1446.json`, row `S3_u225_finish_whatever_was_read`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_finish_stopped_before_its_first_send_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_this_version_recorded_with_no_move_sent_leaves_a_reorder_the_persons`

Old text:

```
    if stopped_write is not None and not reordered_since_stop:
```

New text:

```
    if stopped_write is not None:
```

### `r1453.S4_unread_keys_keep_a_readable_release`

the brief's row, R-1434's S4: the unread keys keep a key a readable release carries, so a row held as an unread release and a readable one is unread, left out of the order and its removal not read

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1453.json`, row `S4_unread_keys_keep_a_readable_release`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`

Old text:

```
    unread_keys = {alias(remote_id) for remote_id in unread} - readable_keys
```

New text:

```
    unread_keys = {alias(remote_id) for remote_id in unread}
```

### `r1453.U1_unread_keys_unaliased`

a nearby value: the unread keys read by each release's own key rather than its row's, so an unread release of a row held twice never meets the readable release's key

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1453.json`, row `U1_unread_keys_unaliased`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`

Old text:

```
    unread_keys = {alias(remote_id) for remote_id in unread} - readable_keys
```

New text:

```
    unread_keys = {remote_key(remote_id) for remote_id in unread} - readable_keys
```

### `r1453.U2_base_keeps_unread_keys`

R-1264's base strip gone: the base keeps an unread key, so an unread track is read as taken off the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1453.json`, row `U2_base_keeps_unread_keys`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_an_unread_track_the_twin_holds_is_never_removed_or_added_again`

Old text:

```
        if unread_keys:
            unseen |= {key for key in base_account if key in unread_keys}
```

New text:

```
        if False:
            unseen |= {key for key in base_account if key in unread_keys}
```

### `r1453.U4_removal_takes_only_the_linked_release`

U208's every release of a removed track goes, narrowed to the key's own release, so the readable release of a row held twice stays on the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1453.json`, row `U4_removal_takes_only_the_linked_release`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`

Old text:

```
                    [held for held in account_now if alias(held) == key] or [remote_of(key)]
```

New text:

```
                    [remote_of(key)]
```

### `r1453.U5_account_keys_take_unread_only_rows`

the account's keys read every listed id, an unread only row included, so it is placed by the merge as a readable row

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1453.json`, row `U5_account_keys_take_unread_only_rows`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 30 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_finish_stopped_before_its_first_send_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - ... and 15 more, see the JSON sidecar

Old text:

```
            for remote_id in (listed_order or account_now)
            if alias(remote_id) in readable_keys
```

New text:

```
            for remote_id in (listed_order or account_now)
```

### `u130-b.B1_short_base_unnarrowed`

A short listing's withheld tracks read as removed on the account

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u130-b.json`, row `B1_short_base_unnarrowed`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_short_account_listing_reads_nothing_as_removed`

Old text:

```
        if short is not None:
            # A WITHHELD TRACK IS NOT A REMOVED ONE.
```

New text:

```
        if False:
            # A WITHHELD TRACK IS NOT A REMOVED ONE.
```

### `u130-b.B4_no_isrc_still_asked`

A row with no ISRC anywhere is still matched through the provider

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u130-b.json`, row `B4_no_isrc_still_asked`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_row_with_no_isrc_anywhere_is_named_and_the_provider_is_not_asked`

Old text:

```
            elif not isrc:
                reason = NO_ISRC
```

New text:

```
            elif False:
                reason = NO_ISRC
```

### `u130-b.B5_readd_old_rule`

A re-add is any change of the first row, so a duplicate losing one copy reads as put back

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u130-b.json`, row `B5_readd_old_rule`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_held_twice_that_lost_one_copy_is_not_read_as_put_back`

Old text:

```
            if content_id in base_rows and not (row_ids & base_rows[content_id])
```

New text:

```
            if content_id in base_rows and row_ids != base_rows[content_id]
```

### `u130-b.B6_requeue`

A track an earlier sync queued is queued again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u130-b.json`, row `B6_requeue`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_an_account_track_the_library_lacks_is_queued_once_and_never_written_as_a_row`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
        if remote_id in queued_before:
```

New text:

```
        if False:
```

### `u198.C1_miss_reuse`

pair_cli._ask: a remembered miss is never reused

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u198.json`, row `C1_miss_reuse`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_sync_screens_every_code_it_will_ask_and_never_a_linked_row_or_a_remembered_miss`
  - `tests/test_sync_pair_discover.py::test_rows_the_account_cannot_carry_are_counted_skipped_and_never_asked_again`

Old text:

```
    if held is not None and held.isrc == isrc and AGREEING_RELEASES not in held.reason:
```

New text:

```
    if False:
```

### `u198.C2_miss_isrc`

pair_cli._ask: a remembered miss is reused whatever the row's ISRC

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u198.json`, row `C2_miss_isrc`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_remembered_miss_is_asked_again_when_the_rows_isrc_changes`

Old text:

```
    if held is not None and held.isrc == isrc and AGREEING_RELEASES not in held.reason:
```

New text:

```
    if held is not None and AGREEING_RELEASES not in held.reason:
```

### `u198.C3_unread_remembered`

pair_cli._ask: an unreadable candidate is remembered

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u198.json`, row `C3_unread_remembered`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_an_unreadable_candidate_is_never_remembered`

Old text:

```
    if UNREADABLE_CANDIDATE not in reason and AGREEING_RELEASES not in reason:
```

New text:

```
    if AGREEING_RELEASES not in reason:
```

### `u198.C4_tie_remembered`

pair_cli._ask: a tie is remembered

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u198.json`, row `C4_tie_remembered`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_tie_is_never_remembered_and_is_asked_again`

Old text:

```
    if UNREADABLE_CANDIDATE not in reason and AGREEING_RELEASES not in reason:
```

New text:

```
    if UNREADABLE_CANDIDATE not in reason:
```

### `u202-composites.C3_composite`

composite for C3_removed_only in u202.md: plan_pair never dates a rekordbox removal, so a removal later than the account's put back reads as no moment

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u202-composites.json`, row `C3_composite`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`

Old text:

```
                rekordbox_removed[as_key(content_id)] = max(
```

New text:

```
                _undated = max(
```

### `u202.C1_after_synced`

plan_pair: an account date not after the base's sync still reads the track as put back

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u202.json`, row `C1_after_synced`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_put_back_dated_before_the_last_sync_is_no_put_back`

Old text:

```
                    and now > was
                    and now > synced
```

New text:

```
                    and now > was
```

### `u207.P1_pair_screens_remembered_miss`

sync pair: a remembered miss's code is screened though it is never asked

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u207.json`, row `P1_pair_screens_remembered_miss`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_isrc_screen.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_sync_screens_every_code_it_will_ask_and_never_a_linked_row_or_a_remembered_miss`

Old text:

```
        and _remembered_miss(reader, content_id, code) is None

```

New text:

```
(empty)
```

### `u207.P2_pair_never_screens`

sync pair: the plan never screens, so every code is asked alone

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u207.json`, row `P2_pair_never_screens`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_isrc_screen.py`
- Collected: 154 against a baseline of 154
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_code_the_account_playlist_already_holds_is_never_screened`
  - `tests/test_sync_pair_discover.py::test_a_sync_screens_every_code_it_will_ask_and_never_a_linked_row_or_a_remembered_miss`

Old text:

```
    if asked:
        reader.remote.screen_isrcs(asked)
```

New text:

```
    if False:
        reader.remote.screen_isrcs(asked)
```

### `u208.M10_here_database_only`

here: read only the database ISRC, never the row's file

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M10_here_database_only`
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; file_identity is read through pair_read, its home since the split
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued[file-isrc]`

Old text:

```
            if code is None:
                code = match.isrc_token(row.isrc) or pair_read.file_identity(cfg, row.path)[0]
            if code:
                codes.setdefault(code, []).append(row.content_id)
```

New text:

```
            if code is None:
                code = match.isrc_token(row.isrc)
            if code:
                codes.setdefault(code, []).append(row.content_id)
```

### `u208.M11_alias_off`

alias: read every account track as its own key, so two releases of one row are two keys again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M11_alias_off`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_release_added_on_the_account_as_the_row_leaves_rekordbox_is_never_taken_off`
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[database-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_sibling_placed_at_the_top_of_the_account_is_left_where_the_person_put_it`
  - `tests/test_sync_pair_tie.py::test_the_first_release_taken_off_while_a_later_one_stays_keeps_the_row`

Old text:

```
        return aliased.get(remote_id) or remote_key(remote_id)
```

New text:

```
        return remote_key(remote_id)
```

### `u208.M18_held_there_asks_provider`

plan_pair: with several releases of the row on the account, ask the provider as round one did

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M18_held_there_asks_provider`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_two_releases_already_on_the_account_take_the_lower_and_add_no_third`

Old text:

```
            elif isrc and held_there:
```

New text:

```
            elif False:
```

### `u208.M1_ask_any_agreeing`

_ask: ask the account without any_agreeing, so a tie between agreeing releases is refused as before U208

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M1_ask_any_agreeing`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_release_added_on_the_account_as_the_row_leaves_rekordbox_is_never_taken_off`
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[database-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_second_sync_asks_the_provider_nothing_about_a_linked_tie`
  - `tests/test_sync_pair_tie.py::test_a_sibling_placed_at_the_top_of_the_account_is_left_where_the_person_put_it`
  - `tests/test_sync_pair_tie.py::test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued[database-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_tie_remembered_as_a_miss_before_this_unit_is_asked_once_and_linked`
  - `tests/test_sync_pair_tie.py::test_a_tie_with_none_hearted_is_linked_to_the_lowest_release`
  - `tests/test_sync_pair_tie.py::test_both_releases_taken_off_the_account_take_the_row_out_of_rekordbox`
  - `tests/test_sync_pair_tie.py::test_one_release_taken_off_the_account_while_another_stays_changes_nothing[database-isrc]`
  - `tests/test_sync_pair_tie.py::test_one_release_taken_off_the_account_while_another_stays_changes_nothing[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_the_files_album_narrows_the_tie_before_the_lowest_is_taken`
  - `tests/test_sync_pair_tie.py::test_the_first_release_taken_off_while_a_later_one_stays_keeps_the_row`
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - ... and 1 more, see the JSON sidecar

Old text:

```
            album=album,
            any_agreeing=True,
        )
        or ""
```

New text:

```
            album=album,
            any_agreeing=False,
        )
        or ""
```

### `u208.M24_alias_unfrozen`

alias: read the links live, as the first fix round did, so a link the library lookup makes after the merge changes the key space

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M24_alias_unfrozen`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_release_added_on_the_account_as_the_row_leaves_rekordbox_is_never_taken_off`
  - `tests/test_sync_pair_tie.py::test_a_sibling_placed_at_the_top_of_the_account_is_left_where_the_person_put_it`

Old text:

```
        return aliased.get(remote_id) or remote_key(remote_id)
```

New text:

```
        return remote_key(canon[known[remote_id]]) if known.get(remote_id) in canon else remote_key(remote_id)
```

### `u208.M2_old_tie_miss_reused`

_ask: reuse a miss remembered with the tie's words, so a tie remembered before U208 is never asked again nor linked

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M2_old_tie_miss_reused`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_tie_remembered_as_a_miss_before_this_unit_is_asked_once_and_linked`

Old text:

```
    if held is not None and held.isrc == isrc and AGREEING_RELEASES not in held.reason:
```

New text:

```
    if held is not None and held.isrc == isrc:
```

### `u208.M4_tie_flag_dropped`

_ask: never say a tie was broken, so the gate counts none

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M4_tie_flag_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - `tests/test_sync_pair_tie.py::test_two_hearted_releases_take_the_lower_hearted_one`

Old text:

```
        return remote_id, "", bool(remote.tie_broken(row.content_id))
```

New text:

```
        return remote_id, "", False
```

### `u208.M5_tied_rows_not_gathered`

plan_pair: gather no tied rows, so the facts line, the totals and the item flag say nothing

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M5_tied_rows_not_gathered`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - `tests/test_sync_pair_tie.py::test_two_hearted_releases_take_the_lower_hearted_one`

Old text:

```
        elif broke:
            tied.append(names[key])
```

New text:

```
        elif False:
            tied.append(names[key])
```

### `u208.M9_here_lookup_dropped`

_owned: never look among the pair's own rows, so a sibling of a file ISRC row is queued for acquisition

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u208.json`, row `M9_here_lookup_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued[file-isrc]`

Old text:

```
    if rest and here is not None:
```

New text:

```
    if False:
```

### `u221.R1_hold_only_a_twin`

held_for_choice: drop the twin test, so a pair that is no twin reads by time and holds every undated track the library lacks

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R1_hold_only_a_twin`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_unread.py`
- Collected: 174 against a baseline of 174
- Kills: 21 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[blocked]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[queued]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[running]`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_job_still_holds_is_awaiting_and_not_queued[succeeded]`
  - `tests/test_sync_pair.py::test_a_track_carrying_no_isrc_is_still_queued_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_still_queued`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[cancelled]`
  - `tests/test_sync_pair.py::test_a_track_only_a_failed_or_cancelled_job_held_is_queued[failed]`
  - `tests/test_sync_pair.py::test_a_track_this_pair_alone_lists_is_queued_once_beside_anothers_job`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`
  - `tests/test_sync_pair.py::test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale`
  - `tests/test_sync_pair.py::test_another_pairs_job_that_no_longer_reads_stops_no_plan`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    if pair is None or not getattr(pair, "twin", False):
        return False
```

New text:

```
    if pair is None:
        return False
```

### `u221.R2_recorded_hold_never_holds`

held_for_choice: a recorded hold holds nothing, so a twin made since U221 queues its missing tracks

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R2_recorded_hold_never_holds`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_pair_that_is_no_twin_never_holds`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_a_plain_pair_lists_is_queued_once_and_still_held`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record`

Old text:

```
    if recorded is not None:
        return remote_id in recorded
```

New text:

```
    if recorded is not None:
        return False
```

### `u221.R3_recorded_hold_holds_everything`

held_for_choice: a recorded hold holds every track, so a track added later and a released twin's tracks are never queued

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R3_recorded_hold_holds_everything`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_pair_that_is_no_twin_never_holds`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_is_released_by_name_and_counted_by_time`
  - `tests/test_sync_twins_hold.py::test_release_all_lets_every_twin_go`
  - `tests/test_sync_twins_hold.py::test_releasing_the_twin_queues_its_three_at_the_next_sync`

Old text:

```
    if recorded is not None:
        return remote_id in recorded
```

New text:

```
    if recorded is not None:
        return True
```

### `u221.R4_undated_not_held`

held_for_choice: a pre U221 twin's undated track is read as added after the mark and queued

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R4_undated_not_held`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_short_listings_twin_records_no_hold_and_holds_a_track_served_later`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_holds_what_the_account_dates_before_its_mark`

Old text:

```
    if marked is None or added is None:
        return True
```

New text:

```
    if marked is None or added is None:
        return False
```

### `u221.R5_time_rule_never_holds`

held_for_choice: a pre U221 twin's dated track is never held, so a track dated before the mark is queued

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R5_time_rule_never_holds`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_track_dated_at_the_very_mark_is_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_holds_what_the_account_dates_before_its_mark`

Old text:

```
    return not added > marked
```

New text:

```
    return False
```

### `u221.R6_time_rule_always_holds`

held_for_choice: a pre U221 twin holds a track dated after the mark, so one put on by hand since is never queued

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R6_time_rule_always_holds`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_track_dated_at_the_very_mark_is_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_holds_what_the_account_dates_before_its_mark`

Old text:

```
    return not added > marked
```

New text:

```
    return True
```

### `u221.R7_plan_ignores_the_hold`

plan_pair: drop the hold branch, so every held track is queued as before U221

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R7_plan_ignores_the_hold`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_short_listings_twin_records_no_hold_and_holds_a_track_served_later`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_holds_what_the_account_dates_before_its_mark`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_a_plain_pair_lists_is_queued_once_and_still_held`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record`

Old text:

```
        elif held_for_choice(held, remote_id, dates):
```

New text:

```
        elif False:
```

### `u221.R8_hold_before_awaiting`

plan_pair: read the hold before the queued before check, so a track an earlier sync queued is named on hold rather than awaiting

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u221.json`, row `R8_hold_before_awaiting`
- Moved: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`

Old text:

```
        if remote_id in queued_before:
            awaiting.append(names[key])
        elif held_for_choice(held, remote_id, dates):
```

New text:

```
        if held_for_choice(held, remote_id, dates):
            on_hold.append(names[key])
        elif remote_id in queued_before:
            awaiting.append(names[key])
        elif held_for_choice(held, remote_id, dates):
```

### `u225.M15_fold_despite_skip`

plan_pair: both bases move to the stopped write's though it skipped rekordbox

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u225.json`, row `M15_fold_despite_skip`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_that_skipped_rekordbox_leaves_the_accounts_removal_to_be_made`

Old text:

```
    folded = stopped_write is not None and stopped_write.written
```

New text:

```
    folded = stopped_write is not None
```

### `u225.M16_account_base_unfolded`

plan_pair: the account base is the snapshot's, not what the stopped write left

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u225.json`, row `M16_account_base_unfolded`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_the_stopped_write_added_then_taken_off_in_rekordbox_comes_off_the_account`

Old text:

```
                if folded
                else held.account or ()
```

New text:

```
                if False
                else held.account or ()
```

### `u225.M17_rekordbox_base_unfolded`

plan_pair: the rekordbox base is the snapshot's, not what the stopped write left

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u225.json`, row `M17_rekordbox_base_unfolded`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_the_stopped_write_added_then_taken_off_in_rekordbox_comes_off_the_account`

Old text:

```
            if folded
            else tuple(held.rekordbox or ())
```

New text:

```
            if False
            else tuple(held.rekordbox or ())
```

### `u225.M20_stopped_not_passed`

plan_pair: the stopped write is not handed to the merge

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u225.json`, row `M20_stopped_not_passed`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_names_the_pair_as_finishing_the_stopped_run`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_says_the_account_was_read_off_the_moves_path`

Old text:

```
        stopped=stopped,
```

New text:

```
        stopped=None,
```

### `u226.M19_plan_no_hold`

plan_pair: a lagging pair is planned from its window rather than held

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u226.json`, row `M19_plan_no_hold`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 267 against a baseline of 267
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_a_named_pair_whose_window_lags_refuses_as_itself`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_lags_beside_a_partial_unpaged_read_holds_the_pair_and_says_why`

Old text:

```
        if listing.window == provider_listing.WINDOW_LAGS:
            raise _lagging(target.account_id, name)
```

New text:

```
        if False:
            raise _lagging(target.account_id, name)
```

### `u226.M21_plan_window_only`

plan_pair: the account side listed from its window alone

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u226.json`, row `M21_plan_window_only`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 267 against a baseline of 267
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_a_named_pair_whose_window_lags_refuses_as_itself`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_lags_an_order_past_the_unpaged_reads_first_page_plans_no_order`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_lags_beside_a_partial_unpaged_read_holds_the_pair_and_says_why`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_serves_an_old_order_plans_no_rekordbox_order`

Old text:

```
            reader.found, target.account_id, current=True

```

New text:

```
            reader.found, target.account_id, current=False

```

### `u229.M15_wide_landed_needs_rest`

_owned: the widened landed step answers a track an earlier step already found, overwriting its row

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `M15_wide_landed_needs_rest`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`

Old text:

```
    if rest:
        landed = reader.landed_anywhere
        for remote_id in rest:
```

New text:

```
    if rest:
        landed = reader.landed_anywhere
        for remote_id in [one for one in lacking if codes.get(one)]:
```

### `u229.M1_wide_landed_step`

_owned: drop the step that reads every landed INBOX playlist, so a track another account playlist landed is queued again (sitting 86)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `M1_wide_landed_step`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_is_added_and_never_queued`
  - `tests/test_sync_pair.py::test_one_row_landed_in_two_inbox_playlists_is_one_row`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[torn]`
  - `tests/test_sync_pair.py::test_the_same_plan_with_the_record_readable_adds_the_row[unknown-state]`
  - `tests/test_sync_pair.py::test_two_landed_rows_carrying_the_code_are_ambiguous_and_queue_nothing`
  - `tests/test_sync_pair_hold.py::test_a_track_found_by_another_landing_costs_the_plan_no_call[by another account playlist's landing]`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`

Old text:

```
        landed = reader.landed_anywhere
```

New text:

```
        landed = {}
```

### `u229.M3_wide_jobs_step`

_owned: drop the step that reads every other pair's intake jobs, so a track another pair's job found owned is queued

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `M3_wide_jobs_step`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_another_pairs_intake_job_found_owned_is_added`

Old text:

```
        for remote_id, content_id in _owned_by_jobs(reader, others, rest, own=False).items():
```

New text:

```
        for remote_id, content_id in {}.items():
```

### `u229.M4_wide_jobs_own_only`

_owned: the widened job step reads this pair's own jobs again, never another pair's

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `M4_wide_jobs_own_only`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_another_pairs_intake_job_found_owned_is_added`

Old text:

```
        others = tuple(job for job in reader.pair_jobs if job.job_id not in mine)
```

New text:

```
        others = tuple(job for job in reader.pair_jobs if job.job_id in mine)
```

### `u229.M5_wide_jobs_strict`

_owned: read other pairs' jobs as the pair's own, so one pair's job whose configuration no longer reads refuses every plan

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `M5_wide_jobs_strict`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_another_pairs_job_that_no_longer_reads_stops_no_plan`

Old text:

```
_owned_by_jobs(reader, others, rest, own=False)
```

New text:

```
_owned_by_jobs(reader, others, rest, own=True)
```

### `u229.M8_own_landing_first`

_owned: this pair's own landing step reads every landing, so another account's row carrying the code makes the pair's own row ambiguous

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `M8_own_landing_first`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`

Old text:

```
        landed = _mirror_isrcs(reader, account_id)
```

New text:

```
        landed = reader.landed_anywhere
```

### `u229.S1_ambiguous_count`

plan_pair (sample, U130): add the first of several rows carrying the code rather than naming it ambiguous

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `S1_ambiguous_count`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_two_landed_rows_carrying_the_code_are_ambiguous_and_queue_nothing`
  - `tests/test_sync_pair.py::test_two_rows_carrying_one_isrc_add_neither_and_say_so`

Old text:

```
            if len(answer) == 1:
                content_id = answer[0]
```

New text:

```
            if len(answer) >= 1:
                content_id = answer[0]
```

### `u229.S2_own_landed_step`

_owned (sample, U128): drop this pair's own landed step, so a track its own landing brought is answered only by the widened step

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u229.json`, row `S2_own_landed_step`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_this_account_playlists_own_landing_wins_over_anothers`

Old text:

```
        landed = _mirror_isrcs(reader, account_id)
        for remote_id in rest:
```

New text:

```
        landed = {}
        for remote_id in rest:
```

### `u231.M15_pending_not_read`

plan: a pending order is planned as U225 would, with no agreement asked

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M15_pending_not_read`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 26 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_pair_that_never_settles_stays_pending_past_the_age_a_plan_is_kept`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_is_held_whole_until_a_later_reading_agrees`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_settle.py::test_a_reading_kept_from_before_the_moves_is_no_agreement`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    if stopped_write is not None and stopped_write.pending:
```

New text:

```
    if False:
```

### `u231.M16_shown_order_not_finished`

plan: a reading showing the order the moves leave still waits for agreement

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M16_shown_order_not_finished`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_late_order_finishes_in_the_next_run_with_no_rekordbox_write_between`
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`

Old text:

```
    if pair_stopped.shows(write.end, now):
        return
```

New text:

```
    if False:
        return
```

### `u231.M17_agreement_gap_ignored`

plan: a reading equal to the one kept agrees however soon after it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M17_agreement_gap_ignored`
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_two_readings_agree_only_once_minutes_apart`

Old text:

```
    agreed = kept and pair_model._now() - seen_at >= AGREE_AFTER
```

New text:

```
    agreed = kept
```

### `u231.M18_reading_before_the_moves_kept`

plan: a reading kept before the moves began counts toward agreement

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M18_reading_before_the_moves_kept`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_reading_kept_from_before_the_moves_is_no_agreement`

Old text:

```
    kept = seen_at is not None and seen_at >= write.moving_at and tuple(held.seen) == now
```

New text:

```
    kept = seen_at is not None and tuple(held.seen) == now
```

### `u231.M20_every_reading_kept`

plan: every reading replaces the one kept, so one too soon resets the wait

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M20_every_reading_kept`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_two_readings_agree_only_once_minutes_apart`

Old text:

```
    if not kept:
        reader.see(target.account_id, now)
```

New text:

```
    if True:
        reader.see(target.account_id, now)
```

### `u231.M22_root_playlist_named_gig_ready`

scope: a root playlist named GIG READY is read as under the folder (round one's row 6)

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u231.json`, row `M22_root_playlist_named_gig_ready`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_root_playlist_named_gig_ready_is_not_under_gig_ready`

Old text:

```
        return bool(rekordbox.ancestors) and rekordbox.top[1] == ORDER_FOLDER
```

New text:

```
        return rekordbox.top[1] == ORDER_FOLDER
```

### `u234.O10_after_not_compared`

the order after a settled one leads whatever the reading now, so an order that moved again leads unsettled

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O10_after_not_compared`
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`

Old text:

```
        and not pair_stopped.reordered(kept.after, reading)
        and pair_model._now() - since
```

New text:

```
        and pair_model._now() - since
```

### `u234.O11_after_not_replaced`

an order after a settled one that moves again is not kept afresh, so the order it moved to is held for good

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O11_after_not_replaced`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`

Old text:

```
    if kept.after is None or since is None or pair_stopped.reordered(kept.after, reading):
```

New text:

```
    if kept.after is None or since is None:
```

### `u234.O12_kept_reading_of_any_run`

_kept_after takes a reading kept for another run as this stop's

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O12_kept_reading_of_any_run`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_kept_reading_counts_only_for_its_run_at_or_after_its_moves`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_for_another_run_shows_no_reorder`

Old text:

```
    if kept is None or kept.run != write.run_id:
```

New text:

```
    if kept is None:
```

### `u234.O13_kept_reading_before_the_stop`

_kept_after takes a reading kept before the stop as one after it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O13_kept_reading_before_the_stop`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_kept_reading_counts_only_for_its_run_at_or_after_its_moves`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_before_the_stop_shows_no_reorder`

Old text:

```
    if seen_at is None or seen_at < began:
```

New text:

```
    if seen_at is None:
```

### `u234.O1_off_path_dropped_from_the_finish`

the defect back: an account off the stopped write's path is left out of the finish, so the folded base reads it as reordered and it is written into rekordbox

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O1_off_path_dropped_from_the_finish`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 21 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_reading_that_never_settled_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_before_the_stop_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_for_another_run_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_on_the_path_is_never_the_baseline_so_the_partial_state_after_it_finishes`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    if stopped_write is not None and not reordered_since_stop:
```

New text:

```
    if stopped_write is not None and not reordered_since_stop and not off_path:
```

### `u234.O23_off_path_flag_on_every_finish`

finishing_off_path is set on every finish, so the gate says off the path for one on it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O23_off_path_flag_on_every_finish`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_names_the_pair_as_finishing_the_stopped_run`

Old text:

```
        finishing_off_path=stopped is not None and off_path,
```

New text:

```
        finishing_off_path=stopped is not None,
```

### `u234.O25_on_path_reading_kept`

round two's fix undone: a reading on the moves' path is kept and settled as the baseline, so a lag of the whole write then the partial state is read as a reorder

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O25_on_path_reading_kept`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_reading_that_never_settled_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_later_reading_still_on_the_moves_path_is_finished_never_read_as_a_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_on_the_path_is_never_the_baseline_so_the_partial_state_after_it_finishes`
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`

Old text:

```
    kept = _kept_after(held, write)
    if not off_path:
```

New text:

```
    kept = _kept_after(held, write)
    if False:
```

### `u234.O26_on_path_reading_keeps_the_order_after`

a reading on the path leaves an order held as the one after on its old clock, so read again it leads at once

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O26_on_path_reading_keeps_the_order_after`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`

Old text:

```
        # any order held as the one after, so that order waits afresh.
        if kept is not None and kept.after is not None:
```

New text:

```
        # any order held as the one after, so that order waits afresh.
        if False:
```

### `u234.O27_settled_order_keeps_the_order_after`

a reading back at the settled order leaves an order held as the one after on its old clock, so read again it leads at once

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O27_settled_order_keeps_the_order_after`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`

Old text:

```
        # as the one after waits afresh if it is read again.
        if kept.after is not None:
```

New text:

```
        # as the one after waits afresh if it is read again.
        if False:
```

### `u234.O3_person_never_leads`

an order after a settled one that agrees over the window never leads, so a person's reorder is held for good

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O3_person_never_leads`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`

Old text:

```
        return True
    if kept.after is None or since is None
```

New text:

```
        return False
    if kept.after is None or since is None
```

### `u234.O4_settled_order_read_as_moved`

a reading back at the settled order is read as differing from it, so the order after is held for it and the stop is never finished

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O4_settled_order_read_as_moved`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_added_on_the_account_between_two_readings_is_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`
  - `tests/test_sync_pair_stopped_order.py::test_two_syncs_reading_the_same_order_off_the_path_are_no_reorder`

Old text:

```
    if not pair_stopped.reordered(kept.order, reading):
        # BACK AT THE SETTLED ORDER
```

New text:

```
    if False:
        # BACK AT THE SETTLED ORDER
```

### `u234.O5_unsettled_reading_read_as_settled`

round one's defect back: a kept reading counts before it settles, so the provider moving between two plans is read as the person

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O5_unsettled_reading_read_as_settled`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`

Old text:

```
    if not kept.settled:
```

New text:

```
    if False:
```

### `u234.O6_reading_never_kept`

the plan keeps no reading after the stop, so no later sync can show a person's reorder

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O6_reading_never_kept`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 13 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`

Old text:

```
    if kept is None:
        reader.see_stop(target.account_id, pairs.StopReading(write.run_id, reading, stamp))
        return False
```

New text:

```
    if kept is None:
        return False
```

### `u234.O8_moved_reading_not_kept_afresh`

a reading in another order before the kept one settles does not replace it, so a lag is settled as the first reading

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O8_moved_reading_not_kept_afresh`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`

Old text:

```
        if pair_stopped.reordered(kept.order, reading):
            reader.see_stop(target.account_id, pairs.StopReading(write.run_id, reading, stamp))
        elif
```

New text:

```
        if False:
            pass
        elif
```

### `u234.O9_after_without_the_window`

the order after a settled one leads on its next reading however soon

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u234.json`, row `O9_after_without_the_window`
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`

Old text:

```
        and pair_model._now() - since >= AGREE_AFTER
    ):
        return True
```

New text:

```
    ):
        return True
```

### `u246.S10_pair_cli_started_empty`

pair: the stopped write's start as an empty set, so a folded base holds nothing it asked for

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u246.json`, row `S10_pair_cli_started_empty`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair.py`
- Collected: 237 against a baseline of 237
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_the_stopped_write_added_then_taken_off_in_rekordbox_comes_off_the_account`

Old text:

```
        started = set(stopped_write.start) if folded else set()
```

New text:

```
        started = set()
```

### `u246.S11_pair_cli_served_empty`

pair: the served keys as an empty set, so under a short listing every base key reads as withheld

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u246.json`, row `S11_pair_cli_served_empty`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_hold.py`
- Collected: 132 against a baseline of 132
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_short_listing_removes_nothing_from_the_account`

Old text:

```
            served = set(account_keys)
```

New text:

```
            served = set()
```

### `u304.S1_file_code_read_through_its_module`

pair_plan: the file's ISRC and album, read through pair_read so a patch reaches it, answer nothing

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u304.json`, row `S1_file_code_read_through_its_module`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_tie.py`
- Collected: 97 against a baseline of 97
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_rekordbox_row_with_no_isrc_column_is_matched_on_its_files_isrc`
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_one_release_taken_off_the_account_while_another_stays_changes_nothing[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_the_files_album_narrows_the_tie_before_the_lowest_is_taken`

Old text:

```
            code, album = pair_read.file_identity(cfg, row.path)
```

New text:

```
            code, album = "", ""
```

### `u304.S2_file_code_for_an_agreement`

pair_plan: a row with no database code never asks its file for one before the account is asked to agree

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u304.json`, row `S2_file_code_for_an_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`
- Collected: 117 against a baseline of 117
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued[file-isrc]`

Old text:

```
or pair_read.file_identity(cfg, row.path)[0]
```

New text:

```
or ""
```

### `u304.S4_pending_agreement_clock`

pair_plan._pending: a pending pair's agreement read off the wall clock, not pair_model._now

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u304.json`, row `S4_pending_agreement_clock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 135 against a baseline of 135
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_two_readings_agree_only_once_minutes_apart`

Old text:

```
    agreed = kept and pair_model._now() - seen_at >= AGREE_AFTER
```

New text:

```
    agreed = kept and __import__("datetime").datetime.now(__import__("datetime").UTC) - seen_at >= AGREE_AFTER
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
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

### `u202-composites.R2_confined`

pair_reverse.create: the twins' confinement check is not run before the commit

- File: `src/cratekit/sync/pair_reverse.py`
- Source: `u202-composites.json`, row `R2_confined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_write_outside_the_playlist_made_is_refused_with_nothing_written`

Old text:

```
                twins.assert_confined(
                    db,
```

New text:

```
                (lambda *a, **k: None)(
                    db,
```

### `u202.R1_recheck_name`

pair_reverse.recheck: a name taken since the plan is made again

- File: `src/cratekit/sync/pair_reverse.py`
- Source: `u202.json`, row `R1_recheck_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_the_write_refuses_a_name_taken_since_the_plan`

Old text:

```
    if taken:
        raise _stale(
```

New text:

```
    if False:
        raise _stale(
```

### `u202.W1_landed_then_raised`

pair_reverse.create: a commit that lands and then raises no longer tells the caller, so the playlist made stays unpaired (the second review's BLOCKING finding)

- File: `src/cratekit/sync/pair_reverse.py`
- Source: `u202.json`, row `W1_landed_then_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_commit_that_lands_and_then_raises_still_pairs_the_playlist`

Old text:

```
                    if on_commit is not None and playlist_id:
                        on_commit(playlist_id)
                raise
```

New text:

```
                raise
```

### `r1264.M19_warning`

_warnings: say nothing of the unread tracks

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1264.json`, row `M19_warning`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`

Old text:

```
    unread = [(one, named) for one in planned.pairs for named in one.unread]
    if unread:
```

New text:

```
    unread = [(one, named) for one in planned.pairs for named in one.unread]
    if False:
```

### `r1264.M20_item`

_items: list no unread track among the gate's items

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1264.json`, row `M20_item`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`
- Collected: 20 against a baseline of 20
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists`
  - `tests/test_sync_pair_unread.py::test_a_row_held_only_as_an_unread_release_stays_where_the_account_lists_it`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_removed_in_rekordbox_leaves_the_account`
  - `tests/test_sync_pair_unread.py::test_a_row_whose_listed_release_is_its_unread_second_stays_in_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_track_naming_no_artist_is_unread_the_same_way`
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`

Old text:

```
        items.append(row("account", "unread", named))
```

New text:

```
        pass
```

### `r1383.M10_warning_never_said`

plan: carry no unread entry to the warning, so the hold is silent

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M10_warning_never_said`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`
  - `tests/test_sync_pair.py::test_a_track_no_landing_brought_in_is_held_while_a_record_is_unread`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
                _landings_said(cfg, reader.landings[1]) if "landings" in reader.__dict__ else ()
```

New text:

```
                ()
```

### `r1383.M12_unlisted_said_as_records`

_landings_said: never say the log is unlisted, so a refused listing is named as a record to repair

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M12_unlisted_said_as_records`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`

Old text:

```
    if session.log_unlisted(unread, cfg):
        return (
```

New text:

```
    if False:
        return (
```

### `r1383.M13_records_unnamed`

_landings_said: name no record, so the warning cannot say which record to look at

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M13_records_unnamed`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
        f"the record {Path(path).name} in {Path(path).parent}, which reads under the "
```

New text:

```
        f"a record in {Path(path).parent}, which reads under the "
```

### `r1383.M16_zero_said_as_count`

_warnings: say a scan nothing waited on as zero tracks held, round one's finding 7

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M16_zero_said_as_count`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_an_earlier_sync_queued_is_awaiting_beside_an_unreadable_record`

Old text:

```
                        if waiting
                        # THE SCAN
```

New text:

```
                        if True
                        # THE SCAN
```

### `r1383.M17_total_uncounted`

payload: count no held track in the totals

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M17_total_uncounted`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
            "landing_unread": count("library", LANDING_UNREAD_ACTION),
```

New text:

```
            "landing_unread": 0,
```

### `r1383.M6_gate_item_dropped`

_items: name no held track on the gate, so a person approving sees nothing of what waits

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M6_gate_item_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_hold.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
    for named in one.landing_unread:
        items.append(row("library", LANDING_UNREAD_ACTION, named))
```

New text:

```
    for named in ():
        items.append(row("library", LANDING_UNREAD_ACTION, named))
```

### `r1383.M7_gate_item_side`

_items: name a held track on the rekordbox side rather than the library's

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1383.json`, row `M7_gate_item_side`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_twins_hold.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[torn]`
  - `tests/test_sync_pair.py::test_an_unreadable_landing_record_holds_the_track_it_may_have_brought_in[unknown-state]`

Old text:

```
        items.append(row("library", LANDING_UNREAD_ACTION, named))
```

New text:

```
        items.append(row("rekordbox", LANDING_UNREAD_ACTION, named))
```

### `r1385.M13_warning_unsplit`

_warnings: say every awaited track was queued, so a skip that queued nothing is reported as queued (round one's finding)

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1385.json`, row `M13_warning_unsplit`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`

Old text:

```
        before = [row for row in awaiting if not row.reason.startswith(QUEUED_HERE)]
```

New text:

```
        before = awaiting
```

### `r1385.M14_warning_here_dropped`

_warnings: never say a track another pair of this sync is to queue

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1385.json`, row `M14_warning_here_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_two_pairs_listing_one_lacking_track_queue_it_once`

Old text:

```
        if here:
            parts.append(
```

New text:

```
        if False:
            parts.append(
```

### `r1432.P10_warning_says_it_stays`

the sync-pair-unread warning at a finish says only that each stays where it is

- File: `src/cratekit/sync/pair_screen.py`
- Source: `r1432.json`, row `P10_warning_says_it_stays`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`

Old text:

```
                        if finished_unread
```

New text:

```
                        if False
```

### `u130-b.B9_stale_pair_blocks_all`

With no argument, one pair whose playlist is gone refuses every pair

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u130-b.json`, row `B9_stale_pair_blocks_all`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`

Old text:

```
                if not every or exc.cause.reason not in PER_PAIR_REASONS:
```

New text:

```
                if True:
```

### `u198.C10_unpair_account_gone`

plan: a made pair whose account playlist is gone is planned, not unpaired

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C10_unpair_account_gone`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_on_the_account_unpairs_stays_and_is_not_made_again`

Old text:

```
            if pair is not None and (pair.twin or pair.made) and target.account_id not in listed:
```

New text:

```
            if pair is not None and pair.twin and target.account_id not in listed:
```

### `u198.C11_unpair_rekordbox_gone`

plan: a made pair whose rekordbox playlist is gone is left out, not released

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C11_unpair_rekordbox_gone`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_made_pair_deleted_inside_archive_is_said_to_be_gone`
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_in_rekordbox_unpairs_and_leaves_the_account_playlist`

Old text:

```
                if there is None or there.removed:
```

New text:

```
                if False:
```

### `u198.C12_archive_move`

plan: a made pair moved under a skipped folder keeps syncing

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C12_archive_move`
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py; the line also stands in favorites/order.py, another package's own guard, so rows --after would not choose
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_made_pair_moved_into_another_apps_or_the_favorites_folder_is_let_go[favorites]`
  - `tests/test_sync_pair_discover.py::test_a_made_pair_moved_into_another_apps_or_the_favorites_folder_is_let_go[foreign]`
  - `tests/test_sync_pair_discover.py::test_a_made_pair_moved_into_archive_is_let_go_and_never_written_again`

Old text:

```
                if moved:
```

New text:

```
                if False:
```

### `u198.C5_folder_twice`

pair_cli._discovered: two root folders of the name adopt the first

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C5_folder_twice`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_two_root_folders_of_the_name_leave_that_folder_out`

Old text:

```
            if len(named) > 1:
```

New text:

```
            if len(named) > 2:
```

### `u198.C6_folder_others`

pair_cli._discovered: a folder another list keeps is adopted

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C6_folder_others`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_root_folder_another_list_of_cratekits_keeps_is_not_adopted`

Old text:

```
            elif named and named[0] in others:
```

New text:

```
            elif False:
```

### `u198.C7_title_taken`

pair_cli._discovered: a person's playlist of the title gets a second beside it

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C7_title_taken`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_an_existing_root_folder_of_the_name_is_reused_and_a_persons_title_is_left`

Old text:

```
            if one.title in taken:
```

New text:

```
            if False:
```

### `u198.C8_folder_gone`

pair_cli._discovered: a recorded folder is reused though the account deleted it

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u198.json`, row `C8_folder_gone`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_recorded_folder_deleted_on_the_account_is_made_again`

Old text:

```
        if recorded is not None and recorded.folder_id in root:
```

New text:

```
        if recorded is not None:
```

### `u202-composites.C10_reads_account`

plan: a sync of every pair with no marked pair never lists the account, so nothing comes back

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u202-composites.json`, row `C10_reads_account`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_with_every_pair_released_a_new_playlist_in_a_recorded_folder_still_comes`

Old text:

```
    reads_account = bool(wanted) or (every and bool(document.folders))
```

New text:

```
    reads_account = bool(wanted)
```

### `u202-composites.C8_scope`

_discovered_back: an account playlist a pair may not hold is brought over

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u202-composites.json`, row `C8_scope`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_set_playlist_sharing_a_name_does_not_stop_the_authors_own`

Old text:

```
            try:
                _scope_account(
                    account_id, reader.listed, reader.label_owned, reader.set_built, reader.mirrored
                )
            except CratekitError as exc:
```

New text:

```
            try:
                pass
            except CratekitError as exc:
```

### `u202.C5_released`

_discovered_back: a released account playlist is made in rekordbox again

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u202.json`, row `C5_released`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_made_pair_whose_rekordbox_playlist_is_deleted_releases_its_account_playlist`
  - `tests/test_sync_pair_back.py::test_a_released_account_playlist_is_never_made_again`

Old text:

```
            if account_id in released:
```

New text:

```
            if False:
```

### `u202.C7_twice`

_discovered_back: two account playlists of one rekordbox name are both made

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u202.json`, row `C7_twice`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_two_account_playlists_of_one_rekordbox_name_refuse_that_name_only`

Old text:

```
        if many > 1:
```

New text:

```
        if many > 2:
```

### `u208.M6_facts_line_dropped`

facts: leave the broken tie count off the pair's line on the gate

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u208.json`, row `M6_facts_line_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`

Old text:

```
                if one.tied
                else ""
```

New text:

```
                if False
                else ""
```

### `u208.M7_totals_tied_zero`

payload: report totals.tied as zero whatever the plan broke

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u208.json`, row `M7_totals_tied_zero`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - `tests/test_sync_pair_tie.py::test_two_hearted_releases_take_the_lower_hearted_one`

Old text:

```
            "tied": sum(len(one.tied) for one in planned.pairs),
```

New text:

```
            "tied": 0,
```

### `u208.M8_item_flag_dropped`

_items: mark no account add as chosen by a broken tie

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u208.json`, row `M8_item_flag_dropped`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`

Old text:

```
                **({"tied": True} if remote_id in broken else {}),
```

New text:

```
                **({}),
```

### `u216-m14.M14_moment_any_folder`

_discovered_back: the adoption moment reads made pairs in every folder, not only this one

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u216-m14.json`, row `M14_moment_any_folder`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_moment_is_read_from_this_folders_own_pairs`

Old text:

```
                if pair.made and pair.folder == folder
```

New text:

```
                if pair.made
```

### `u216.M13_unrecorded_off`

_discovered_back: no folder reads as unrecorded, so a pre U216 adoption is read as a created folder

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u216.json`, row `M13_unrecorded_off`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_without_a_record_or_a_creation_time_every_unpaired_playlist_is_named`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_creation_time_decides`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_moment_is_read_from_this_folders_own_pairs`

Old text:

```
        unrecorded = recorded.held is None and not recorded.created
```

New text:

```
        unrecorded = False
```

### `u216.M15_before_rule_off`

_discovered_back: the before adoption rule is not applied

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u216.json`, row `M15_before_rule_off`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_a_creation_time_without_a_zone_is_no_time`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_or_a_creation_time_every_unpaired_playlist_is_named`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_creation_time_decides`
  - `tests/test_sync_pair_adopted.py::test_without_a_record_the_moment_is_read_from_this_folders_own_pairs`

Old text:

```
            if before:
                left(account_id, title, folder, pair_discover.BEFORE, before)
```

New text:

```
            if False:
                left(account_id, title, folder, pair_discover.BEFORE, before)
```

### `u216.M16_copy_rule_off`

_discovered_back: the DOWNLOADED copy rule is not applied

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u216.json`, row `M16_copy_rule_off`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_in_a_created_folder_is_named_a_copy`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`

Old text:

```
            if copied:
                whose = (
```

New text:

```
            if False:
                whose = (
```

### `u216.M18_copy_all_titles`

_discovered_back: the paired titles are every title in the folder, paired or not

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u216.json`, row `M18_copy_all_titles`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`

Old text:

```
            title for account_id, title in inside.items() if account_id in paired_ids
        ]
```

New text:

```
            title for account_id, title in inside.items()
        ]
```

### `u216.M19_place_held_empty`

_discovered: an adopted folder's plan carries an empty listing, so the adoption records it held nothing

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u216.json`, row `M19_place_held_empty`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
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
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
                        held=frozenset(inside) if action == FOLDER_ADOPT else None,
```

New text:

```
                        held=frozenset() if action == FOLDER_ADOPT else None,
```

### `u221.R11_no_warning_per_twin`

_warnings: drop the on hold warning, so the answer never counts the held tracks per twin or names the release command

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u221.json`, row `R11_no_warning_per_twin`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`

Old text:

```
    holding = [one for one in planned.pairs if one.on_hold]
```

New text:

```
    holding = []
```

### `u221.R9_gate_names_no_held_track`

_items: drop the on-hold rows, so the gate names no held track

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u221.json`, row `R9_gate_names_no_held_track`
- Moved: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_another_account_playlist_landed_is_added_and_the_rest_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_short_listings_twin_records_no_hold_and_holds_a_track_served_later`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_holds_what_the_account_dates_before_its_mark`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_a_plain_pair_lists_is_queued_once_and_still_held`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_another_pairs_job_holds_is_still_held`
  - `tests/test_sync_twins_hold.py::test_a_twins_held_track_stays_on_hold_beside_an_unreadable_landing_record`

Old text:

```
    for named in one.on_hold:
        items.append(row("library", ON_HOLD_ACTION, named))
```

New text:

```
    for named in ():
        items.append(row("library", ON_HOLD_ACTION, named))
```

### `u225.M24_unread_unsaid`

_warnings: runs' steps that could not be read are not named

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u225.json`, row `M24_unread_unsaid`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`
  - `tests/test_sync_pair_stopped_order.py::test_a_runs_steps_that_cannot_be_read_are_named_never_read_as_no_write`

Old text:

```
    if planned.stopped_unread:
```

New text:

```
    if False:
```

### `u234.O21_gate_says_on_path`

the gate line says on the path for an account read off it

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u234.json`, row `O21_gate_says_on_path`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_says_the_account_was_read_off_the_moves_path`

Old text:

```
                    if one.finishing_off_path
                    else "so its moves are not read as anybody's; "
```

New text:

```
                    if False
                    else "so its moves are not read as anybody's; "
```

### `u234.O22_finishing_note_silent`

the sync-pair-finishing note leaves out that the account was read off the path

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u234.json`, row `O22_finishing_note_silent`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_says_the_account_was_read_off_the_moves_path`

Old text:

```
                            "it is not read as a reorder; "
                            if one.finishing_off_path
```

New text:

```
                            "it is not read as a reorder; "
                            if False
```

### `u304.S10_unpaired_default_side`

pair_screen.Unpaired: the side gone by default is rekordbox's, not the account's

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u304.json`, row `S10_unpaired_default_side`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_hold.py`
- Collected: 189 against a baseline of 189
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_an_unpaired_pair_names_the_account_side_gone_unless_told_otherwise`
  - `tests/test_sync_twins.py::test_a_twin_whose_account_playlist_is_deleted_is_unpaired_and_left_named`

Old text:

```
    gone: str = "account"
```

New text:

```
    gone: str = "rekordbox"
```

### `r1372.K19_passed_by_strict`

passed_by: a write that began at the snapshot's very moment is not passed

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K19_passed_by_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
            if began is not None and not began > moment:
```

New text:

```
            if began is not None and began < moment:
```

### `r1372.K20_passed_by_any_pair`

passed_by: a snapshot lets go of every pair's carried records, not its own

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K20_passed_by_any_pair`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
            if _account_of(key, steps, new=new, made=made) != account_id:
                continue
            began = placeholders.parse_hearted(steps.get(account))
            if began is not None
```

New text:

```
            began = placeholders.parse_hearted(steps.get(account))
            if began is not None
```

### `r1372.K21_made_pair_unmapped`

_account_of: a made pair is read under its key, not the account playlist it was made as

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1372.json`, row `K21_made_pair_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_made_pair_is_read_under_the_account_playlist_it_was_made_as`
  - `tests/test_sync_pair_stopped.py::test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it`

Old text:

```
    if key.startswith(new):
        return steps.get(made) if isinstance(steps.get(made), str) else ""
    return key
```

New text:

```
    return key
```

### `r1376.F14_finished_filter_gone`

stopped_writes (sample, U225): a stop a later run finished is still read, by a first sync among others

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1376.json`, row `F14_finished_filter_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_later_run_that_finished_the_pair_hides_the_stopped_write_in_either_order`

Old text:

```
        if account_id not in finished or not finished[account_id] > began
```

New text:

```
        if True
```

### `r1394.S10_later_unsent_write_hides_the_pending`

stopped writes: the latest record is read whether or not it sent a move, so a refused finish hides the pending write it was finishing, round two's BLOCKING row

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S10_later_unsent_write_hides_the_pending`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_stopped.py::test_a_later_write_that_sent_no_move_does_not_hide_a_pending_one`

Old text:

```
            if held is None or (write.pending, write.at) > (held[1].pending, held[1].at):
```

New text:

```
            if held is None or write.at > held[1].at:
```

