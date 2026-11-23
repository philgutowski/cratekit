# Mutation table: u304-replay-before-p2

Measured by `scripts/mutate.py` on 2026-11-22 23:38 UTC, branch `HEAD` at `c9192091`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 247.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 30, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/cc6c934b-9743-5b0a-bc60-d462f78fd3d6/scratchpad/u304-replay-known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1446-c.F3_readable_ids_weighed_as_unread` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 264 | 3 | killed |
| `r1446.M10_kept_order_with_unread` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r1446.M14_plan_flag_dropped` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1446.M1_no_readable_check` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 394 | 6 | killed |
| `r1446.M4_unread_moved_not_set` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 394 | 7 | killed |
| `r1446.M8_no_settled_reading_reads_no_move` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1446.M9_unsettled_reading_compared` | `src/cratekit/sync/pair_cli.py` | maintainer | 10 file(s) | 394 | 1 | killed |
| `r1446.S1_u234_settled_reorder_never_leads` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 394 | 10 | killed |
| `r1446.S3_u225_finish_whatever_was_read` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 394 | 12 | killed |
| `r1453.S4_unread_keys_keep_a_readable_release` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 394 | 2 | killed |
| `r1453.U1_unread_keys_unaliased` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1453.U2_base_keeps_unread_keys` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 394 | 4 | killed |
| `r1453.U4_removal_takes_only_the_linked_release` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1453.U5_account_keys_take_unread_only_rows` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 394 | 30 | killed |
| `u130-b.B1_short_base_unnarrowed` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 75 | 1 | killed |
| `u130-b.B3_account_isrc_not_first` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u130-b.B4_no_isrc_still_asked` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 75 | 1 | killed |
| `u130-b.B5_readd_old_rule` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 75 | 1 | killed |
| `u130-b.B6_requeue` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 75 | 3 | killed |
| `u130-b.B7_set_playlist_in_scope` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 75 | 1 | killed |
| `u130-b.B8_tree_name_in_scope` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 75 | 1 | killed |
| `u130-b.B9_stale_pair_blocks_all` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 75 | 1 | killed |
| `u130-c.C1_half_written_snapshot` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 75 | 6 | killed |
| `u147-c.M20_pair_scope` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u198.C10_unpair_account_gone` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.C11_unpair_rekordbox_gone` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 166 | 2 | killed |
| `u198.C12_archive_move` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 166 | 3 | killed |
| `u198.C1_miss_reuse` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 166 | 2 | killed |
| `u198.C2_miss_isrc` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.C3_unread_remembered` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.C4_tie_remembered` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.C5_folder_twice` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.C6_folder_others` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.C7_title_taken` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.C8_folder_gone` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.C9_account_only` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 166 | 1 | killed |
| `u202-composites.C10_reads_account` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 158 | 1 | killed |
| `u202-composites.C3_composite` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 158 | 3 | killed |
| `u202-composites.C8_scope` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 158 | 1 | killed |
| `u202.C1_after_synced` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 158 | 1 | killed |
| `u202.C4_dates_recorded` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 158 | 6 | killed |
| `u202.C5_released` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 158 | 2 | killed |
| `u202.C7_twice` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 158 | 1 | killed |
| `u207.P1_pair_screens_remembered_miss` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 152 | 1 | killed |
| `u207.P2_pair_never_screens` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 152 | 2 | killed |
| `u208.M10_here_database_only` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 141 | 2 | killed |
| `u208.M11_alias_off` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 141 | 5 | killed |
| `u208.M18_held_there_asks_provider` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `u208.M1_ask_any_agreeing` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 141 | 16 | killed |
| `u208.M24_alias_unfrozen` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 141 | 2 | killed |
| `u208.M2_old_tie_miss_reused` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `u208.M4_tie_flag_dropped` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 96 | 2 | killed |
| `u208.M5_tied_rows_not_gathered` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 96 | 2 | killed |
| `u208.M6_facts_line_dropped` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 96 | 1 | killed |
| `u208.M7_totals_tied_zero` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 96 | 2 | killed |
| `u208.M8_item_flag_dropped` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 96 | 1 | killed |
| `u208.M9_here_lookup_dropped` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 141 | 2 | killed |
| `u209.C10_reverse_recheck` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 206 | 2 | killed |
| `u209.C11_home_of` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 206 | 1 | killed |
| `u209.C12_brought_folder` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 206 | 1 | killed |
| `u209.C13_jobs_queued` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 206 | 2 | killed |
| `u209.C3_withheld` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 206 | 1 | killed |
| `u209.C4_rekordbox_gone` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 206 | 1 | killed |
| `u209.C5_memberships` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 206 | 5 | killed |
| `u209.C6_discovered_place` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 206 | 5 | killed |
| `u209.C7_made_left_behind` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 206 | 1 | killed |
| `u209.C8_rows_gone` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 206 | 1 | killed |
| `u209.C9_unpaired_back` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 206 | 1 | killed |
| `u209.H1_offer_mismatch_ignored` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 206 | 1 | killed |
| `u210.R10_check_todo` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 1 | killed |
| `u210.R11_part_written` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 6 | killed |
| `u210.R12_our_folders` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 5 | killed |
| `u210.R14_asked_before` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 9 | killed |
| `u210.R16_forecast_line` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 2 | killed |
| `u210.R18_beyond_order` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 1 | killed |
| `u210.R19_beyond_gained` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 1 | killed |
| `u210.R1_made_step_read` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 1 | killed |
| `u210.R20_beyond_lost` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 1 | killed |
| `u210.R21_check_queued` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 1 | killed |
| `u210.R22_landed_read` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 1 | killed |
| `u210.R2_resumed_move` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 1 | killed |
| `u210.R3_made_here_folder` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 1 | killed |
| `u210.R4_rekordbox_landed` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 2 | killed |
| `u210.R5_queue_once` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 1 | killed |
| `u210.R8_done_step` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 3 | killed |
| `u210.R9_skip_done` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 263 | 1 | killed |
| `u216-m14.M14_moment_any_folder` | `src/cratekit/sync/pair_cli.py` | user | 12 file(s) | 383 | 1 | killed |
| `u216.M13_unrecorded_off` | `src/cratekit/sync/pair_cli.py` | user | 12 file(s) | 383 | 3 | killed |
| `u216.M15_before_rule_off` | `src/cratekit/sync/pair_cli.py` | user | 12 file(s) | 383 | 10 | killed |
| `u216.M16_copy_rule_off` | `src/cratekit/sync/pair_cli.py` | user | 12 file(s) | 383 | 5 | killed |
| `u216.M18_copy_all_titles` | `src/cratekit/sync/pair_cli.py` | user | 12 file(s) | 383 | 2 | killed |
| `u216.M19_place_held_empty` | `src/cratekit/sync/pair_cli.py` | user | 12 file(s) | 383 | 7 | killed |
| `u216.M20_made_drops_held` | `src/cratekit/sync/pair_cli.py` | user | 12 file(s) | 383 | 9 | killed |
| `u220.P2_session_tolerated` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 304 | 2 | killed |
| `u220.P5_no_stop_after_loop` | `src/cratekit/sync/pair_cli.py` | user | 10 file(s) | 304 | 9 | killed |
| `u221.R10_digest_without_the_hold` | `src/cratekit/sync/pair_cli.py` | user | 3 file(s) | 153 | 1 | killed |
| `u221.R11_no_warning_per_twin` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 78 | 1 | killed |
| `u221.R1_hold_only_a_twin` | `src/cratekit/sync/pair_cli.py` | user | 4 file(s) | 173 | 21 | killed |
| `u221.R2_recorded_hold_never_holds` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 78 | 9 | killed |
| `u221.R3_recorded_hold_holds_everything` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 78 | 8 | killed |
| `u221.R4_undated_not_held` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 78 | 2 | killed |
| `u221.R5_time_rule_never_holds` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 78 | 2 | killed |
| `u221.R6_time_rule_always_holds` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 78 | 2 | killed |
| `u221.R7_plan_ignores_the_hold` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 78 | 10 | killed |
| `u221.R8_hold_before_awaiting` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 78 | 1 | killed |
| `u221.R9_gate_names_no_held_track` | `src/cratekit/sync/pair_cli.py` | user | 2 file(s) | 78 | 10 | killed |
| `u225.M14_superseded_unchecked` | `src/cratekit/sync/pair_cli.py` | user | 19 file(s) | 665 | 4 | killed |
| `u225.M15_fold_despite_skip` | `src/cratekit/sync/pair_cli.py` | user | 19 file(s) | 665 | 1 | killed |
| `u225.M16_account_base_unfolded` | `src/cratekit/sync/pair_cli.py` | user | 19 file(s) | 665 | 1 | killed |
| `u225.M17_rekordbox_base_unfolded` | `src/cratekit/sync/pair_cli.py` | user | 19 file(s) | 665 | 1 | killed |
| `u225.M20_stopped_not_passed` | `src/cratekit/sync/pair_cli.py` | user | 19 file(s) | 665 | 3 | killed |
| `u225.M21_start_from_asked` | `src/cratekit/sync/pair_cli.py` | user | 19 file(s) | 665 | 1 | killed |
| `u225.M22_written_always` | `src/cratekit/sync/pair_cli.py` | user | 19 file(s) | 665 | 1 | killed |
| `u225.M23_links_dropped` | `src/cratekit/sync/pair_cli.py` | user | 19 file(s) | 665 | 1 | killed |
| `u225.M24_unread_unsaid` | `src/cratekit/sync/pair_cli.py` | user | 19 file(s) | 665 | 2 | killed |
| `u226.M19_plan_no_hold` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 2 | killed |
| `u226.M20_check_no_lag` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 1 | killed |
| `u226.M21_plan_window_only` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 4 | killed |
| `u226.M22_lagging_not_per_pair` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 1 | killed |
| `u226.M23_totals_no_read_backs` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 265 | 1 | killed |
| `u229.M10_file_isrc_fallback` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 291 | 10 | killed |
| `u229.M11_mirror_cache` | `src/cratekit/sync/pair_cli.py` | maintainer | 8 file(s) | 291 | 1 | killed |
| `u229.M12_own_mirrors_bypass_cache` | `src/cratekit/sync/pair_cli.py` | maintainer | 8 file(s) | 291 | 1 | killed |
| `u229.M15_wide_landed_needs_rest` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 291 | 1 | killed |
| `u229.M1_wide_landed_step` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 291 | 7 | killed |
| `u229.M2_wide_landed_reads_own_only` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 291 | 1 | killed |
| `u229.M3_wide_jobs_step` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 291 | 1 | killed |
| `u229.M4_wide_jobs_own_only` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 291 | 1 | killed |
| `u229.M5_wide_jobs_strict` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 291 | 1 | killed |
| `u229.M6_config_error_not_caught` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 291 | 1 | killed |
| `u229.M8_own_landing_first` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 291 | 1 | killed |
| `u229.M9_landed_dedup` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 291 | 1 | killed |
| `u229.S1_ambiguous_count` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 291 | 2 | killed |
| `u229.S2_own_landed_step` | `src/cratekit/sync/pair_cli.py` | user | 8 file(s) | 291 | 1 | killed |
| `u231.M10_moved_unrecorded` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 1 | killed |
| `u231.M11_snapshot_from_the_order_sent` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 15 | killed |
| `u231.M12_settle_takes_any_reading` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 12 | killed |
| `u231.M13_settle_sleeps_the_whole_window` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 2 | killed |
| `u231.M14_settle_reading_not_kept` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 2 | killed |
| `u231.M15_pending_not_read` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 26 | killed |
| `u231.M16_shown_order_not_finished` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 3 | killed |
| `u231.M17_agreement_gap_ignored` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 1 | killed |
| `u231.M18_reading_before_the_moves_kept` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 1 | killed |
| `u231.M20_every_reading_kept` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 1 | killed |
| `u231.M22_root_playlist_named_gig_ready` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 1 | killed |
| `u231.M23_carried_moving_unread` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 2 | killed |
| `u231.M7_continue_resends` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 6 | killed |
| `u231.M8_no_record_sends_blind` | `src/cratekit/sync/pair_cli.py` | user | 20 file(s) | 753 | 1 | killed |
| `u234.O10_after_not_compared` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 1 | killed |
| `u234.O11_after_not_replaced` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 1 | killed |
| `u234.O12_kept_reading_of_any_run` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 2 | killed |
| `u234.O13_kept_reading_before_the_stop` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 2 | killed |
| `u234.O1_off_path_dropped_from_the_finish` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 21 | killed |
| `u234.O21_gate_says_on_path` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 2 | killed |
| `u234.O22_finishing_note_silent` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 3 | killed |
| `u234.O23_off_path_flag_on_every_finish` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 1 | killed |
| `u234.O25_on_path_reading_kept` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 5 | killed |
| `u234.O26_on_path_reading_keeps_the_order_after` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 1 | killed |
| `u234.O27_settled_order_keeps_the_order_after` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 1 | killed |
| `u234.O3_person_never_leads` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 10 | killed |
| `u234.O4_settled_order_read_as_moved` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 3 | killed |
| `u234.O5_unsettled_reading_read_as_settled` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 10 | killed |
| `u234.O6_reading_never_kept` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 13 | killed |
| `u234.O8_moved_reading_not_kept_afresh` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 1 | killed |
| `u234.O9_after_without_the_window` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 1 | killed |
| `u234.S1_sample_finish_held_to_the_plans_reading` | `src/cratekit/sync/pair_cli.py` | user | 21 file(s) | 765 | 10 | killed |
| `u246.S10_pair_cli_started_empty` | `src/cratekit/sync/pair_cli.py` | user | 5 file(s) | 236 | 1 | killed |
| `u246.S11_pair_cli_served_empty` | `src/cratekit/sync/pair_cli.py` | user | 4 file(s) | 131 | 1 | killed |
| `u246.S12_pair_cli_made_here_empty` | `src/cratekit/sync/pair_cli.py` | user | 1 file(s) | 14 | 1 | killed |
| `u246.S13_pair_cli_per_element` | `src/cratekit/sync/pair_cli.py` | maintainer | 2 file(s) | 78 | 1 | killed |
| `u198.D10_twins` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.D11_two_homes` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.D2_favorites_home` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 166 | 3 | killed |
| `u198.D3_held` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.D4_skip` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 166 | 3 | killed |
| `u198.D5_smart` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.D6_released` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.D7_twice` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.D8_top_names` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 166 | 1 | killed |
| `u198.D9_foreign` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 166 | 2 | killed |
| `u202.D1_skip` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 83 | 1 | killed |
| `u202.D2_two_tops` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 83 | 1 | killed |
| `u202.D3_longest` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 83 | 1 | killed |
| `u202.D5_name_taken` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 83 | 1 | killed |
| `u202.D6_favourites` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 83 | 1 | killed |
| `u216.M11_paired_raw` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 383 | 6 | killed |
| `u216.M12_empty_rest` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 383 | 1 | killed |
| `u216.M1_held_record_ignored` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 383 | 7 | killed |
| `u216.M2_created_folder_by_time` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 383 | 2 | killed |
| `u216.M3_no_moment_reads_new` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 383 | 1 | killed |
| `u216.M4_no_time_reads_new` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 383 | 3 | killed |
| `u216.M5_naive_time_trusted` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 383 | 2 | killed |
| `u216.M6_equal_moment_new` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 383 | 1 | killed |
| `u216.M7_time_rule_off` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 383 | 3 | killed |
| `u216.M8_moment_latest` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 383 | 1 | killed |
| `u216.M9_moment_naive_kept` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 383 | 1 | killed |
| `u242.M25_copy_needs_the_prefix` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 76 | 1 | killed |
| `u242.M27_copy_pool_reads_no_taken` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 76 | 1 | killed |
| `r1404.M1_disagreeing_base_ignored` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 3 | killed |
| `r1404.M2_rekordbox_move_ignored` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 3 | killed |
| `r1404.M3_account_move_not_guarded` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 4 | killed |
| `r1404.M4_always_rekordbox` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 4 | killed |
| `r1404.M5_disagreement_read_now` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 2 | killed |
| `r1404.M6_disagreement_read_against_the_account_now` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 1 | killed |
| `r1404.S1_default_leader` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 16 | killed |
| `r1404.S2_stopped_leader_again` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 2 | killed |
| `r1416.M1_rekordbox_does_not_lead` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 2 | killed |
| `r1416.M2_order_kept_ignored` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 2 | killed |
| `r1416.M3_empty_rekordbox_leads` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 1 | killed |
| `r1416.M4_first_sync_unguarded` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 1 | killed |
| `r1416.M5_stopped_write_yields` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 1 | killed |
| `r1416.M6_default_not_kept` | `src/cratekit/sync/pair_merge.py` | maintainer | 5 file(s) | 224 | 2 | killed |
| `r1416.S2_placed_after_neighbour` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 224 | 22 | killed |

## Zero rows and what they owe

- `r1446.M10_kept_order_with_unread` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u130-b.B3_account_isrc_not_first` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r1446-c.F3_readable_ids_weighed_as_unread`

the shared run unweighted, so it may keep unread ids in place of a readable one and read the wrong unread track as moved

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1446-c.json`, row `F3_readable_ids_weighed_as_unread`
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

### `r1446.M10_kept_order_with_unread`

the settled reading compared with its unread ids in place, so a move of an unread track alone still reads as a reorder

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1446.json`, row `M10_kept_order_with_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        [one for one in kept.order if one not in left_out], readable
```

New text:

```
        list(kept.order), readable
```

### `r1446.M14_plan_flag_dropped`

the plan never carries the flag, so the gate says the stopped order takes the unread track where it was taking it and never that only unread tracks moved

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1446.json`, row `M14_plan_flag_dropped`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1446.json`, row `M1_no_readable_check`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1446.json`, row `M4_unread_moved_not_set`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1446.json`, row `M8_no_settled_reading_reads_no_move`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1446.json`, row `M9_unsettled_reading_compared`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1446.json`, row `S1_u234_settled_reorder_never_leads`
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
        and _now() - since >= AGREE_AFTER
    ):
        return True
```

New text:

```
        and _now() - since >= AGREE_AFTER
    ):
        return False
```

### `r1446.S3_u225_finish_whatever_was_read`

sample, U225: the stop finished even when a reorder was read

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1446.json`, row `S3_u225_finish_whatever_was_read`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1453.json`, row `S4_unread_keys_keep_a_readable_release`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1453.json`, row `U1_unread_keys_unaliased`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1453.json`, row `U2_base_keeps_unread_keys`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1453.json`, row `U4_removal_takes_only_the_linked_release`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `r1453.json`, row `U5_account_keys_take_unread_only_rows`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u130-b.json`, row `B1_short_base_unnarrowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 75 against a baseline of 75
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

### `u130-b.B3_account_isrc_not_first`

Ask the provider even when exactly one account track carries the row's ISRC

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u130-b.json`, row `B3_account_isrc_not_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            if isrc and len(held_there) == 1:
```

New text:

```
            if False:
```

### `u130-b.B4_no_isrc_still_asked`

A row with no ISRC anywhere is still matched through the provider

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u130-b.json`, row `B4_no_isrc_still_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 75 against a baseline of 75
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u130-b.json`, row `B5_readd_old_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 75 against a baseline of 75
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u130-b.json`, row `B6_requeue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 75 against a baseline of 75
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

### `u130-b.B7_set_playlist_in_scope`

A set's playlist may be paired

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u130-b.json`, row `B7_set_playlist_in_scope`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 75 against a baseline of 75
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u130-b.json`, row `B8_tree_name_in_scope`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 75 against a baseline of 75
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

### `u130-b.B9_stale_pair_blocks_all`

With no argument, one pair whose playlist is gone refuses every pair

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u130-b.json`, row `B9_stale_pair_blocks_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 75 against a baseline of 75
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

### `u130-c.C1_half_written_snapshot`

Record the snapshot when either side was written, not both

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u130-c.json`, row `C1_half_written_snapshot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 75 against a baseline of 75
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_skipped_account_side_is_finished_by_the_next_sync`
  - `tests/test_sync_pair.py::test_a_skipped_rekordbox_side_is_finished_by_the_next_sync`
  - `tests/test_sync_pair.py::test_a_whole_sync_after_a_skipped_one_finishes_both_sides_from_the_old_base`
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_skipping_the_only_side_with_changes_answers_no_op`

Old text:

```
    whole = rekordbox_after is not None and account_after is not None and not one.withheld
```

New text:

```
    whole = (rekordbox_after is not None or account_after is not None) and not one.withheld
```

### `u147-c.M20_pair_scope`

sync.pair_cli._scope_account: a mirrored playlist may be paired

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u147-c.json`, row `M20_pair_scope`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
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

### `u198.C10_unpair_account_gone`

plan: a made pair whose account playlist is gone is planned, not unpaired

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u198.json`, row `C10_unpair_account_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u198.json`, row `C11_unpair_rekordbox_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u198.json`, row `C12_archive_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
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

### `u198.C1_miss_reuse`

pair_cli._ask: a remembered miss is never reused

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u198.json`, row `C1_miss_reuse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u198.json`, row `C2_miss_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u198.json`, row `C3_unread_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u198.json`, row `C4_tie_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
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

### `u198.C5_folder_twice`

pair_cli._discovered: two root folders of the name adopt the first

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u198.json`, row `C5_folder_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u198.json`, row `C6_folder_others`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u198.json`, row `C7_title_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u198.json`, row `C8_folder_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
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

### `u198.C9_account_only`

apply_pair: a new pair is made when only rekordbox was approved

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u198.json`, row `C9_account_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_skipping_the_account_gate_makes_and_marks_nothing`

Old text:

```
        if not account:
            return done
```

New text:

```
        if False:
            return done
```

### `u202-composites.C10_reads_account`

plan: a sync of every pair with no marked pair never lists the account, so nothing comes back

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u202-composites.json`, row `C10_reads_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 158 against a baseline of 158
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

### `u202-composites.C3_composite`

composite for C3_removed_only in u202.md: plan_pair never dates a rekordbox removal, so a removal later than the account's put back reads as no moment

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u202-composites.json`, row `C3_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 158 against a baseline of 158
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

### `u202-composites.C8_scope`

_discovered_back: an account playlist a pair may not hold is brought over

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u202-composites.json`, row `C8_scope`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 158 against a baseline of 158
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

### `u202.C1_after_synced`

plan_pair: an account date not after the base's sync still reads the track as put back

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u202.json`, row `C1_after_synced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 158 against a baseline of 158
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

### `u202.C4_dates_recorded`

_record: the account's added dates are never recorded with the snapshot

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u202.json`, row `C4_dates_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 158 against a baseline of 158
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_back.py::test_a_removal_rekordbox_kept_no_moment_for_keeps_the_track_and_names_the_call`
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`
  - `tests/test_sync_pair_back.py::test_the_snapshot_records_each_account_tracks_added_date`

Old text:

```
            if whole
            else None
        ),
        rekordbox=(
```

New text:

```
            if False
            else None
        ),
        rekordbox=(
```

### `u202.C5_released`

_discovered_back: a released account playlist is made in rekordbox again

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u202.json`, row `C5_released`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 158 against a baseline of 158
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u202.json`, row `C7_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 158 against a baseline of 158
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

### `u207.P1_pair_screens_remembered_miss`

sync pair: a remembered miss's code is screened though it is never asked

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u207.json`, row `P1_pair_screens_remembered_miss`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_isrc_screen.py`
- Collected: 152 against a baseline of 152
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u207.json`, row `P2_pair_never_screens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_isrc_screen.py`
- Collected: 152 against a baseline of 152
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u208.json`, row `M10_here_database_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 141 against a baseline of 141
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_tie.py::test_a_row_removed_in_rekordbox_takes_every_release_of_it_off_the_account[file-isrc]`
  - `tests/test_sync_pair_tie.py::test_a_sibling_release_added_on_the_account_finds_the_row_and_is_not_queued[file-isrc]`

Old text:

```
            if code is None:
                code = match.isrc_token(row.isrc) or file_identity(cfg, row.path)[0]
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u208.json`, row `M11_alias_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 141 against a baseline of 141
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u208.json`, row `M18_held_there_asks_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 141 against a baseline of 141
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u208.json`, row `M1_ask_any_agreeing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 141 against a baseline of 141
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u208.json`, row `M24_alias_unfrozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 141 against a baseline of 141
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u208.json`, row `M2_old_tie_miss_reused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 141 against a baseline of 141
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u208.json`, row `M4_tie_flag_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 96 against a baseline of 96
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u208.json`, row `M5_tied_rows_not_gathered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 96 against a baseline of 96
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

### `u208.M6_facts_line_dropped`

facts: leave the broken tie count off the pair's line on the gate

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u208.json`, row `M6_facts_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 96 against a baseline of 96
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u208.json`, row `M7_totals_tied_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 96 against a baseline of 96
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u208.json`, row `M8_item_flag_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`
- Collected: 96 against a baseline of 96
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

### `u208.M9_here_lookup_dropped`

_owned: never look among the pair's own rows, so a sibling of a file ISRC row is queued for acquisition

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u208.json`, row `M9_here_lookup_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_tie.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 141 against a baseline of 141
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

### `u209.C10_reverse_recheck`

check: run no recheck of a made rekordbox side's home before the write

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u209.json`, row `C10_reverse_recheck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 206 against a baseline of 206
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u209.json`, row `C11_home_of`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 206 against a baseline of 206
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u209.json`, row `C12_brought_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 206 against a baseline of 206
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u209.json`, row `C13_jobs_queued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 206 against a baseline of 206
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u209.json`, row `C3_withheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 206 against a baseline of 206
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u209.json`, row `C4_rekordbox_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 206 against a baseline of 206
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u209.json`, row `C5_memberships`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 206 against a baseline of 206
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u209.json`, row `C6_discovered_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 206 against a baseline of 206
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u209.json`, row `C7_made_left_behind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 206 against a baseline of 206
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u209.json`, row `C8_rows_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 206 against a baseline of 206
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u209.json`, row `C9_unpaired_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 206 against a baseline of 206
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u209.json`, row `H1_offer_mismatch_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 206 against a baseline of 206
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R10_check_todo`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R11_part_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R12_our_folders`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R14_asked_before`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
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

### `u210.R16_forecast_line`

sync_pair: warn of the ceiling only at ten times over

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R16_forecast_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
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

### `u210.R18_beyond_order`

_beyond: read no order on a part written playlist

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R18_beyond_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R19_beyond_gained`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
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

### `u210.R1_made_step_read`

apply_pair: never read a made side recorded by an earlier command, so a continue makes it again

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R1_made_step_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[3-the move and the fill]`

Old text:

```
        if isinstance(made, str) and made:
```

New text:

```
        if False:
```

### `u210.R20_beyond_lost`

_beyond: read no track lost

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R20_beyond_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R21_check_queued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R22_landed_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
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

### `u210.R2_resumed_move`

_made: move only a playlist this call made, so a stop between the make and the move leaves it at the root

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R2_resumed_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[2-the make and the move]`

Old text:

```
    if made or (resumed and _made_here(store.get(account_id), one)):
```

New text:

```
    if made:
```

### `u210.R3_made_here_folder`

_made_here: read a reservation in any folder as made here

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R3_made_here_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_made_here_reads_only_a_pair_made_for_this_playlist_in_this_folder`

Old text:

```
        and held.folder == place.folder
```

New text:

```
        and True
```

### `u210.R4_rekordbox_landed`

apply_pair: write rekordbox again on a continue whose commit already landed

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R4_rekordbox_landed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_first_sync_named_by_hand_that_failed_after_its_mark_is_continued_on_its_plan`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_inside_the_account_write_is_finished_without_writing_rekordbox_twice`

Old text:

```
        if isinstance(landed, dict):
```

New text:

```
        if False:
```

### `u210.R5_queue_once`

_queue_once: queue again a job an earlier command of the run queued

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R5_queue_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_job_queued_before_a_stop_is_not_queued_again_by_the_continue`

Old text:

```
    if steps.has(STEP_QUEUED):
```

New text:

```
    if False:
```

### `u210.R8_done_step`

apply_pair: record no done step, so a continue redoes a finished pair

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R8_done_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_ceiling_stop_after_three_of_five_pairs_is_finished_by_a_continue_of_the_run`
  - `tests/test_sync_pair_resume.py::test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue`
  - `tests/test_sync_pair_resume.py::test_the_stop_names_the_run_and_the_calls_its_continue_needs`

Old text:

```
    steps.mark(STEP_DONE, done.account_id or one.target.key)
```

New text:

```
    pass
```

### `u210.R9_skip_done`

sync_pair: write a pair an earlier command finished

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u210.json`, row `R9_skip_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 263 against a baseline of 263
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

### `u216-m14.M14_moment_any_folder`

_discovered_back: the adoption moment reads made pairs in every folder, not only this one

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u216-m14.json`, row `M14_moment_any_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u216.json`, row `M13_unrecorded_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u216.json`, row `M15_before_rule_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u216.json`, row `M16_copy_rule_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u216.json`, row `M18_copy_all_titles`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u216.json`, row `M19_place_held_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
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

### `u216.M20_made_drops_held`

_made: the plan's listing is not passed to the folder's reservation

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u216.json`, row `M20_made_drops_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_playlist_no_pair_names_still_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_the_adopted_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
        stale=place.stale,
        held=place.held,
    )
```

New text:

```
        stale=place.stale,
    )
```

### `u220.P2_session_tolerated`

ORDER_REFUSALS: tolerate a rejected session too, so every later pair meets it

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u220.json`, row `P2_session_tolerated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_tie.py`
- Collected: 304 against a baseline of 304
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

### `u220.P5_no_stop_after_loop`

sync_pair: end OK after the loop though an order did not finish

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u220.json`, row `P5_no_stop_after_loop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_tie.py`
- Collected: 304 against a baseline of 304
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

### `u221.R10_digest_without_the_hold`

PairPlan.identity: leave the held tracks out of the digest, so an approval over one hold is read as approving another

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u221.json`, row `R10_digest_without_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`
- Collected: 153 against a baseline of 153
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

### `u221.R11_no_warning_per_twin`

_warnings: drop the on hold warning, so the answer never counts the held tracks per twin or names the release command

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u221.json`, row `R11_no_warning_per_twin`
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

### `u221.R1_hold_only_a_twin`

held_for_choice: drop the twin test, so a pair that is no twin reads by time and holds every undated track the library lacks

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u221.json`, row `R1_hold_only_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_unread.py`
- Collected: 173 against a baseline of 173
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u221.json`, row `R2_recorded_hold_never_holds`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u221.json`, row `R3_recorded_hold_holds_everything`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u221.json`, row `R4_undated_not_held`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u221.json`, row `R5_time_rule_never_holds`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u221.json`, row `R6_time_rule_always_holds`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u221.json`, row `R7_plan_ignores_the_hold`
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u221.json`, row `R8_hold_before_awaiting`
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

### `u221.R9_gate_names_no_held_track`

_items: drop the on-hold rows, so the gate names no held track

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u221.json`, row `R9_gate_names_no_held_track`
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

### `u225.M14_superseded_unchecked`

stopped_write: a write the pair's snapshot came after is still finished

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u225.json`, row `M14_superseded_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 665 against a baseline of 665
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

### `u225.M15_fold_despite_skip`

plan_pair: both bases move to the stopped write's though it skipped rekordbox

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u225.json`, row `M15_fold_despite_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 665 against a baseline of 665
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u225.json`, row `M16_account_base_unfolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 665 against a baseline of 665
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u225.json`, row `M17_rekordbox_base_unfolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 665 against a baseline of 665
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u225.json`, row `M20_stopped_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 665 against a baseline of 665
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

### `u225.M21_start_from_asked`

_write_account: the start is built from the asked removals and additions, not the adapter's answer

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u225.json`, row `M21_start_from_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 665 against a baseline of 665
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_an_addition_the_provider_left_out_is_never_read_as_taken_off`

Old text:

```
                    one.account_before or one.account_now, removed, added
```

New text:

```
                    one.account_before or one.account_now, one.account_removes, one.account_adds
```

### `u225.M22_written_always`

_write_account: the step says rekordbox was committed though its gate was skipped

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u225.json`, row `M22_written_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 665 against a baseline of 665
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_that_skipped_rekordbox_leaves_the_accounts_removal_to_be_made`

Old text:

```
                written=rekordbox_after is not None,
```

New text:

```
                written=True,
```

### `u225.M23_links_dropped`

_write_account: the step records none of the write's links

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u225.json`, row `M23_links_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 665 against a baseline of 665
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_the_stopped_write_added_then_taken_off_in_rekordbox_comes_off_the_account`

Old text:

```
                written=rekordbox_after is not None,
                links=one.links,
```

New text:

```
                written=rekordbox_after is not None,
                links={},
```

### `u225.M24_unread_unsaid`

_warnings: runs' steps that could not be read are not named

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u225.json`, row `M24_unread_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 665 against a baseline of 665
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

### `u226.M19_plan_no_hold`

plan_pair: a lagging pair is planned from its window rather than held

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u226.json`, row `M19_plan_no_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 265 against a baseline of 265
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

### `u226.M20_check_no_lag`

check: a lagging listing is compared as read rather than named as moved

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u226.json`, row `M20_check_no_lag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 265 against a baseline of 265
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

### `u226.M21_plan_window_only`

plan_pair: the account side listed from its window alone

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u226.json`, row `M21_plan_window_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 265 against a baseline of 265
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

### `u226.M22_lagging_not_per_pair`

PER_PAIR_REASONS: a lagging pair refuses the whole sync of every pair

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u226.json`, row `M22_lagging_not_per_pair`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 265 against a baseline of 265
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

### `u226.M23_totals_no_read_backs`

sync_pair: the run's totals carry no read backs

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u226.json`, row `M23_totals_no_read_backs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 265 against a baseline of 265
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

### `u229.M10_file_isrc_fallback`

mirror_codes: read only the database ISRC, so a landed row whose code is in its file alone is never found

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `M10_file_isrc_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `M11_mirror_cache`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `M12_own_mirrors_bypass_cache`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

### `u229.M15_wide_landed_needs_rest`

_owned: the widened landed step answers a track an earlier step already found, overwriting its row

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `M15_wide_landed_needs_rest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `M1_wide_landed_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

### `u229.M2_wide_landed_reads_own_only`

_Reader.landed_anywhere: read only the first account playlist's landings, so most accounts' landed tracks are queued again

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `M2_wide_landed_reads_own_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

### `u229.M3_wide_jobs_step`

_owned: drop the step that reads every other pair's intake jobs, so a track another pair's job found owned is queued

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `M3_wide_jobs_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `M4_wide_jobs_own_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `M5_wide_jobs_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

### `u229.M6_config_error_not_caught`

_Reader.job_reports: catch only a refusal, so a configuration error from any job's reports escapes

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `M6_config_error_not_caught`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

### `u229.M8_own_landing_first`

_owned: this pair's own landing step reads every landing, so another account's row carrying the code makes the pair's own row ambiguous

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `M8_own_landing_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

### `u229.M9_landed_dedup`

landed_isrcs: append a row once for each INBOX playlist holding it, so one row landed twice reads as ambiguous

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `M9_landed_dedup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

### `u229.S1_ambiguous_count`

plan_pair (sample, U130): add the first of several rows carrying the code rather than naming it ambiguous

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `S1_ambiguous_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u229.json`, row `S2_own_landed_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 291 against a baseline of 291
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

### `u231.M10_moved_unrecorded`

write: every move accepted is not recorded, so a later lag on the path is finished from

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M10_moved_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`

Old text:

```
        steps.mark(STEP_MOVED, timestamp())
```

New text:

```
        pass
```

### `u231.M11_snapshot_from_the_order_sent`

write: the order as sent is recorded as the snapshot, with no settle reading

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M11_snapshot_from_the_order_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[gone]`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[unreadable]`
  - `tests/test_sync_pair_settle.py::test_a_pair_that_never_settles_stays_pending_past_the_age_a_plan_is_kept`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_is_held_whole_until_a_later_reading_agrees`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_pending_run_does_not_count_its_pending_pair_as_synced`
  - `tests/test_sync_pair_settle.py::test_a_settle_reading_refused_for_another_reason_stops_the_write`
  - `tests/test_sync_pair_settle.py::test_a_write_that_keeps_no_record_sends_no_order`
  - `tests/test_sync_pair_settle.py::test_an_agreeing_reading_too_soon_after_the_last_is_not_agreement`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_at_once_finishes_in_the_one_run`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`
  - `tests/test_sync_pair_settle.py::test_the_settle_window_counts_the_time_spent_on_other_writes`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`

Old text:

```
        done.settle = Settle(
            one=one, steps=steps, end=sent, moved_at=_now(), rekordbox_after=None
        )
        return None
```

New text:

```
        return sent
```

### `u231.M12_settle_takes_any_reading`

settle: any reading finishes the pair, the order the moves leave or not

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M12_settle_takes_any_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_pair_that_never_settles_stays_pending_past_the_age_a_plan_is_kept`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_is_held_whole_until_a_later_reading_agrees`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_pending_run_does_not_count_its_pending_pair_as_synced`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_write_that_keeps_no_record_sends_no_order`
  - `tests/test_sync_pair_settle.py::test_an_agreeing_reading_too_soon_after_the_last_is_not_agreement`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`

Old text:

```
        if reading is not None and tuple(reading) == tuple(settle.end):
```

New text:

```
        if reading is not None:
```

### `u231.M13_settle_sleeps_the_whole_window`

settle: the whole window is waited, the time spent on other pairs' writes not counted

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M13_settle_sleeps_the_whole_window`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_the_settle_window_counts_the_time_spent_on_other_writes`

Old text:

```
        left = SETTLE_SECONDS - (_now() - settle.moved_at).total_seconds()
```

New text:

```
        left = SETTLE_SECONDS
```

### `u231.M14_settle_reading_not_kept`

settle: a reading short of the order is not kept on the pair for the next plan to agree with

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M14_settle_reading_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok`

Old text:

```
        if reading is not None:
            pairs.PairStore(cfg).see(settle.one.target.account_id, reading, at=timestamp())
```

New text:

```
        if False:
            pairs.PairStore(cfg).see(settle.one.target.account_id, reading, at=timestamp())
```

### `u231.M15_pending_not_read`

plan: a pending order is planned as U225 would, with no agreement asked

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M15_pending_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M16_shown_order_not_finished`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M17_agreement_gap_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_two_readings_agree_only_once_minutes_apart`

Old text:

```
    agreed = kept and _now() - seen_at >= AGREE_AFTER
```

New text:

```
    agreed = kept
```

### `u231.M18_reading_before_the_moves_kept`

plan: a reading kept before the moves began counts toward agreement

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M18_reading_before_the_moves_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M20_every_reading_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M22_root_playlist_named_gig_ready`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
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

### `u231.M23_carried_moving_unread`

continue: the carried record is not read when the run's steps cannot show the moves (round two's row 4)

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M23_carried_moving_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[gone]`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[unreadable]`

Old text:

```
            moving = steps.carried(STEP_MOVING)
```

New text:

```
            moving = None
```

### `u231.M7_continue_resends`

write: a continue whose pair's moves began sends the order again rather than only reading it

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M7_continue_resends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[gone]`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[unreadable]`
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_whose_moves_all_landed_finishes_on_the_continue`

Old text:

```
        if isinstance(moving, Mapping):
```

New text:

```
        if False:
```

### `u231.M8_no_record_sends_blind`

write: a write that keeps no record sends its order's moves anyway (round one's BLOCKING row)

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u231.json`, row `M8_no_record_sends_blind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 753 against a baseline of 753
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_write_that_keeps_no_record_sends_no_order`

Old text:

```
        if steps.steps is None:
            # U231, ROUND ONE'S REVIEW.
```

New text:

```
        if False:
            # U231, ROUND ONE'S REVIEW.
```

### `u234.O10_after_not_compared`

the order after a settled one leads whatever the reading now, so an order that moved again leads unsettled

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O10_after_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`

Old text:

```
        and not pair_stopped.reordered(kept.after, reading)
        and _now() - since
```

New text:

```
        and _now() - since
```

### `u234.O11_after_not_replaced`

an order after a settled one that moves again is not kept afresh, so the order it moved to is held for good

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O11_after_not_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O12_kept_reading_of_any_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O13_kept_reading_before_the_stop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O1_off_path_dropped_from_the_finish`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

### `u234.O21_gate_says_on_path`

the gate line says on the path for an account read off it

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O21_gate_says_on_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O22_finishing_note_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

### `u234.O23_off_path_flag_on_every_finish`

finishing_off_path is set on every finish, so the gate says off the path for one on it

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O23_off_path_flag_on_every_finish`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O25_on_path_reading_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O26_on_path_reading_keeps_the_order_after`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O27_settled_order_keeps_the_order_after`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O3_person_never_leads`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O4_settled_order_read_as_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O5_unsettled_reading_read_as_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O6_reading_never_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O8_moved_reading_not_kept_afresh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `O9_after_without_the_window`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`

Old text:

```
        and _now() - since >= AGREE_AFTER
    ):
        return True
```

New text:

```
    ):
        return True
```

### `u234.S1_sample_finish_held_to_the_plans_reading`

sample, R-1411: the finish is not held to the plan's reading, so the rest of an off path order is moved from whatever the adapter reads

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u234.json`, row `S1_sample_finish_held_to_the_plans_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 765 against a baseline of 765
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            if one.finishing_order and one.account_before
```

New text:

```
            if False and one.finishing_order and one.account_before
```

### `u246.S10_pair_cli_started_empty`

pair: the stopped write's start as an empty set, so a folded base holds nothing it asked for

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u246.json`, row `S10_pair_cli_started_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair.py`
- Collected: 236 against a baseline of 236
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

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u246.json`, row `S11_pair_cli_served_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_hold.py`
- Collected: 131 against a baseline of 131
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

### `u246.S12_pair_cli_made_here_empty`

pair: no account ids made this run, so discovery is told every pair, the ones this run made included, is already paired

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u246.json`, row `S12_pair_cli_made_here_empty`
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

### `u246.S13_pair_cli_per_element`

pair: build the made here set once per pair again (the shape on main)

- File: `src/cratekit/sync/pair_cli.py`
- Source: `u246.json`, row `S13_pair_cli_per_element`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_comprehension_sets.py`, `tests/test_sync_pair_discover.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`

Old text:

```
                        if pair.account_id not in made_here
```

New text:

```
                        if pair.account_id not in set(ours.values())
```

### `u198.D10_twins`

pair_discover: a twins folder is walked

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u198.json`, row `D10_twins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
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
- Collected: 166 against a baseline of 166
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
- Collected: 166 against a baseline of 166
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
- Collected: 166 against a baseline of 166
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
- Collected: 166 against a baseline of 166
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
- Collected: 166 against a baseline of 166
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
- Collected: 166 against a baseline of 166
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
- Collected: 166 against a baseline of 166
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
- Collected: 166 against a baseline of 166
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
- Collected: 166 against a baseline of 166
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
- Collected: 83 against a baseline of 83
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
- Collected: 83 against a baseline of 83
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
- Collected: 83 against a baseline of 83
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
- Collected: 83 against a baseline of 83
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
- Collected: 83 against a baseline of 83
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
- Collected: 383 against a baseline of 383
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

### `u216.M12_empty_rest`

downloaded_copy: a title with nothing left after the prefix copies a playlist titled as the folder alone

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M12_empty_rest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_downloaded_copy_names_the_paired_title_it_copies`

Old text:

```
    if not wanted:
        return ""
    for one in sorted
```

New text:

```
    for one in sorted
```

### `u216.M1_held_record_ignored`

before_adoption: a playlist the record says the folder held reads as new, so it is made in rekordbox

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M1_held_record_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
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
- Collected: 383 against a baseline of 383
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

### `u216.M3_no_moment_reads_new`

before_adoption: an unrecorded folder with no made pair to date it reads every playlist as new

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M3_no_moment_reads_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`

Old text:

```
    if adopted is None:
        return (
```

New text:

```
    if adopted is None:
        return "" if True else (
```

### `u216.M4_no_time_reads_new`

before_adoption: a playlist with no creation time in an unrecorded folder reads as new

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M4_no_time_reads_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
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
- Collected: 383 against a baseline of 383
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

### `u216.M6_equal_moment_new`

before_adoption: a playlist made at the adoption moment itself reads as new

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M6_equal_moment_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_before_adoption_without_a_record_reads_the_time`

Old text:

```
    if made <= adopted:
```

New text:

```
    if made < adopted:
```

### `u216.M7_time_rule_off`

before_adoption: an unrecorded folder's playlist with a time never reads as held

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M7_time_rule_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
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

### `u216.M8_moment_latest`

adoption_moment: the latest mark rather than the earliest, so a playlist made between two marks reads as held before

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M8_moment_latest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_the_adoption_moment_is_the_earliest_readable_mark`

Old text:

```
    return min(found) if found else None
```

New text:

```
    return max(found) if found else None
```

### `u216.M9_moment_naive_kept`

adoption_moment: keep a mark without a zone, which cannot be compared with the account's times

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u216.json`, row `M9_moment_naive_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_the_adoption_moment_is_the_earliest_readable_mark`

Old text:

```
        if moment.tzinfo is not None:
            found.append(moment)
```

New text:

```
        found.append(moment)
```

### `u242.M25_copy_needs_the_prefix`

pair discovery: read a copy only by its prefix, so a stripped copy is made in rekordbox again

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u242.json`, row `M25_copy_needs_the_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_pair_adopted.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_pairing_techno_with_a_stripped_former_downloaded_techno`

Old text:

```
    if not prefixed and not taken:
```

New text:

```
    if not prefixed:
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

### `r1404.M1_disagreeing_base_ignored`

merge: a base whose two sides disagree on order no longer lets rekordbox lead, the defect R-1404 names

- File: `src/cratekit/sync/pair_merge.py`
- Source: `r1404.json`, row `M1_disagreeing_base_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_twins_hold.py`
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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
- Collected: 224 against a baseline of 224
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

