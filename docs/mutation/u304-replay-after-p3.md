# Mutation table: u304-replay-after-p3

Measured by `scripts/mutate.py` on 2026-11-23 01:02 UTC, branch `HEAD` at `fd78d188`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22911 collected. pytest invocations for this batch: 255.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 42, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/9c4fb6d1-21a5-58b2-b145-6b7e9e36fc05/scratchpad/u304-replay-after-known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22911 against 22911. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u130-a.A5_new_tracks_appended` | `src/cratekit/sync/pair_merge.py` | user | 2 file(s) | 126 | 8 | killed |
| `u130-a.A6_order_change_read_inverted` | `src/cratekit/sync/pair_merge.py` | user | 2 file(s) | 126 | 18 | killed |
| `u202.M1_since` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 2 | killed |
| `u202.M2_naive` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 1 | killed |
| `u202.M3_tie` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 1 | killed |
| `u202.M4_unknown` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 9 | killed |
| `u202.M5_adder` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 10 | killed |
| `u202.M6_account_readded` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 12 | killed |
| `u202.M7_removal_kept` | `src/cratekit/sync/pair_merge.py` | user | 3 file(s) | 164 | 2 | killed |
| `u225.M1_stopped_ignored` | `src/cratekit/sync/pair_merge.py` | user | 4 file(s) | 149 | 5 | killed |
| `u225.M2_rekordbox_since_dropped` | `src/cratekit/sync/pair_merge.py` | user | 4 file(s) | 149 | 2 | killed |
| `u225.M3_rekordbox_over_account` | `src/cratekit/sync/pair_merge.py` | user | 4 file(s) | 149 | 1 | killed |
| `u225.M5_leader_over_account` | `src/cratekit/sync/pair_merge.py` | user | 4 file(s) | 149 | 1 | killed |
| `u234.S2_sample_stopped_leader` | `src/cratekit/sync/pair_merge.py` | user | 6 file(s) | 313 | 3 | killed |
| `u202-composites.R2_confined` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202.R1_recheck_name` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202.W1_landed_then_raised` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1372.K19_passed_by_strict` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1372.K20_passed_by_any_pair` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1372.K21_made_pair_unmapped` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 2 | killed |
| `r1376.F14_finished_filter_gone` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `r1394.S10_later_unsent_write_hides_the_pending` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 3 | killed |
| `r1394.S1_counts_beyond_the_moves_trusted` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 1 | killed |
| `r1394.S2_missing_counts_read_as_none_sent` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 7 | killed |
| `r1394.S6_counts_not_wired` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 14 | killed |
| `r1394.S8_positions_first_only` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 2 | killed |
| `r1394.S9_moving_step_counts_dropped` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 19 | killed |
| `r1418.F7_composite_ordering_start_unread` | `src/cratekit/sync/pair_stopped.py` | user | 10 file(s) | 394 | 20 | killed |
| `r1434.S2_positions_compare_every_track_listed` | `src/cratekit/sync/pair_stopped.py` | user | 10 file(s) | 394 | 2 | killed |
| `u225.M6_front_keeps_nothing` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 1 | killed |
| `u225.M8_reached_strict_membership` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 3 | killed |
| `u225.M9_finish_ignored` | `src/cratekit/sync/pair_stopped.py` | user | 1 file(s) | 89 | 3 | killed |
| `u234.O15_reordered_counts_additions` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 1 | killed |
| `r1289.M1_sweep_reads_whole` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 6 | killed |
| `r1289.M2_unread_not_kept` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 5 | killed |
| `r1289.M3_all_unread_branch` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 2 | killed |
| `r1289.M4_unread_why_dropped` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r1289.M5_all_unread_message` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r1289.M6_report_unread_emptied` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r1289.M7_per_playlist_reraise` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r1289.M8_per_playlist_set` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r1289.M9_short_check` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 2 | killed |
| `r358.S10_mark_always_unbound` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 1 | killed |
| `r358.S1_set_is_the_cursor` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 2 | killed |
| `r358.S5_recheck_is_a_second_read` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 3 | killed |
| `r358.S7_lazy_listing` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 1 | killed |
| `r358.S9_mark_always_applied` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 4 | killed |
| `r359.M10_claims_downloaded` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 1 | killed |
| `r359.M1_drop_field` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 3 | killed |
| `r359.M2_token` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 2 | killed |
| `r359.M3_said_silent` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 2 | killed |
| `r359.M4_said_unconditional` | `src/cratekit/sync/playlists.py` | maintainer | 2 file(s) | 146 | 1 | killed |
| `r359.M8_drop_resolved` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 1 | killed |
| `r359.M9_drop_not_acquired` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 2 | killed |
| `r359.S1_record_on_any_state` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 6 | killed |
| `r361-a.A10_enum_value_respelled` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r361-a.A2_case_insensitive` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 3 | killed |
| `r361-a.A3_no_leading_space` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r361-a.A4_substring_not_suffix` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r361-a.D2_drop_the_placeholder` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 2 | killed |
| `r361-a.D3_drop_in_flight` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r382.M11_reconcile_source_jobs` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r382.M12_in_flight_source_jobs` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 2 | killed |
| `r382.M13_marking_source_jobs` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M15_completed_duplicates` | `src/cratekit/sync/playlists.py` | maintainer | 3 file(s) | 215 | 1 | killed |
| `r382.M1_restore_source_filter` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 7 | killed |
| `r382.M2_drop_handler_key` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M3_drop_library` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M4_hearts_recorded` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M5_no_verbatim_for_pass_jobs` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M6_no_parse` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r382.M7_invalid_records_nothing` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 3 | killed |
| `r382.M8_completed_raw` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r382.M9_open_raw` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r835-b.S1_built_year_excluded_from_sweep` | `src/cratekit/sync/playlists.py` | user | 4 file(s) | 271 | 1 | killed |
| `r837-a.A16_sweep_excludes_set` | `src/cratekit/sync/playlists.py` | user | 5 file(s) | 327 | 1 | killed |
| `u113-a.A6_sweep_passes_no_name` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 147 | 1 | killed |
| `u130-c.C9_sweep_takes_paired` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 76 | 2 | killed |
| `u147-c.M18_sweep_exclusion` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 35 | 1 | killed |
| `u242.M1_exclusion_reads_the_ledger` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 230 | 5 | killed |
| `u242.M2_is_taken_drops_the_id` | `src/cratekit/sync/playlists.py` | user | 4 file(s) | 286 | 14 | killed |
| `u242.M3_is_taken_drops_the_prefix` | `src/cratekit/sync/playlists.py` | user | 5 file(s) | 386 | 22 | killed |
| `u242.M4_plan_reads_no_ledger` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 161 | 5 | killed |
| `u242.M5_pending_marks_ignores_the_ledger` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 230 | 1 | killed |
| `u82-a.A5_only_narrows` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 184 | 9 | killed |
| `u82-a.A6_an_empty_only_is_nothing` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 184 | 1 | killed |
| `u82-a.A7_mark_swept_hands_only_through` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 184 | 8 | killed |
| `u221.R21_unknown_name_not_refused` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R22_all_beside_names` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R23_nothing_named` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `u221.R25_released_twin_asks_again` | `src/cratekit/sync/release_cli.py` | user | 2 file(s) | 1029 | 1 | killed |
| `r1830.M18_plan_counts_nothing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `r1830.M19_digest_omits_the_count` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `r1830.M22_applied_message_counts_nothing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287-m11.M11_gone_offers_nothing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `u287.M13_folder_separator` | `src/cratekit/sync/removed.py` | maintainer | 1 file(s) | 74 | 1 | killed |
| `u287.M14_twin_is_own_filing` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 32 | killed |
| `u287.M17_gone_with_no_record_is_not_whole` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M18_set_aside_rows_count` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M19_old_prefix_is_synced` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M1_partial_read_stops_offers` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 8 | killed |
| `u287.M20_unreadable_record_is_not_whole` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M2_held_by_isrc` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `u287.M3_held_by_recording` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M4_held_before_the_pass` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M5_not_this_pass_file` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u287.M6_on_another_synced` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 8 | killed |
| `u287.M7_in_a_playlist_of_yours` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 3 | killed |
| `u287.M8_empty_read_untrusted` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u287.M9_short_read_untrusted` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M16_stale_digest` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 2 | killed |
| `u288.M17_only_the_offered` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 8 | killed |
| `u288.M18_unmeasured_kept` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M19_first_position` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u288.M20_read_back_refusal` | `src/cratekit/sync/removed.py` | user | 1 file(s) | 74 | 1 | killed |
| `u320-m5.M5_retired_holds` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M10_reopened_keeps_its_retirement` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 2 | killed |
| `u320.M13_withheld_bound_widened` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M18_opened_and_refused_is_unopened` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M4_withheld_hearts_hold_nothing` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 2 | killed |
| `u320.M6_any_failure_is_a_sighting` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 4 | killed |
| `u320.M7_outage_forgets_the_record` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M8_retirement_never_applies` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 5 | killed |
| `u320.M9_relisted_keeps_its_retirement` | `src/cratekit/sync/removed.py` | user | 2 file(s) | 123 | 2 | killed |
| `r1830.M20_screen_omits_the_count` | `src/cratekit/sync/removed_cli.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M21_gate_answer` | `src/cratekit/sync/removed_cli.py` | user | 1 file(s) | 74 | 3 | killed |
| `u288.M22_closed_at_open` | `src/cratekit/sync/removed_cli.py` | user | 1 file(s) | 74 | 1 | killed |
| `u320.M20_retirable_without_this_reads_not_found` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 2 | killed |
| `u320.M21_retire_records_before_the_gate` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M22_retire_ignores_its_answer` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M23_reads_never_recorded` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 11 | killed |
| `u320.M24_record_read_as_empty` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 8 | killed |
| `u320.M25_person_retires_nothing` | `src/cratekit/sync/removed_cli.py` | user | 2 file(s) | 123 | 3 | killed |
| `r704-a.R1_increment_ignores_the_flag` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r704-a.R2_rate_limit_not_retryable` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r704-a.R3_remedy_retry_later` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r704-a.R4_detail_unmarked` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r704-a.R5_flag_not_stored` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 2 | killed |
| `r704-a.R6_sentence_reworded` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `u52-item-derivation.A1_acquires_early_return_gone` | `src/cratekit/sync/run.py` | user | 2 file(s) | 211 | 3 | killed |
| `u52-item-derivation.A2_acquires_default_false` | `src/cratekit/sync/run.py` | user | 2 file(s) | 211 | 6 | killed |
| `r259.S1_scope_owned_sample` | `src/cratekit/sync/scope.py` | maintainer | 1 file(s) | 31 | 1 | killed |
| `r263.S2_favorites_reason` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 146 | 1 | killed |
| `u109-b.B1_labels_not_guided` | `src/cratekit/sync/sources.py` | user | 3 file(s) | 228 | 13 | killed |
| `u109-b.B2_command_spelling` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 197 | 9 | killed |
| `u109-b.B3_no_cursor_reworded` | `src/cratekit/sync/sources.py` | user | 1 file(s) | 31 | 3 | killed |
| `u74.A1_no_inbound_key` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 146 | 26 | killed |
| `u74.A2_wrong_inbound_key` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 146 | 14 | killed |
| `u242.M11_strip_skips_the_held_check` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M12_composite` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 11 | killed |
| `u242.M12_strip_skips_the_migration` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 14 | killed |
| `u242.M13_strip_no_collision_with_others` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u242.M14_strip_no_collision_between_strips` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M15_strip_collision_case_exact` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M17_strip_no_recheck` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u242.M18_strip_records_no_old_title` | `src/cratekit/sync/strip_cli.py` | user | 1 file(s) | 46 | 4 | killed |
| `u242.M19_migration_copies_an_unmarked_mark` | `src/cratekit/sync/taken_cli.py` | user | 1 file(s) | 46 | 3 | killed |
| `u149.T10_any_year_folder` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T11_excluded_read` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T13_paired_planned_again` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T15_unplanned_membership` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T16_unplanned_playlist_row` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 2 | killed |
| `u149.T20_short_snapshot` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T21_landing_paired_again` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 6 | 1 | killed |
| `u149.T2_two_folders_not_refused` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u149.T3_folder_names_unread` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 2 | killed |
| `u149.T4_removed_folder_live` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u149.T5_held_name_counted_free` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 3 | killed |
| `u149.T6_taken_name_free` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u149.T7_ambiguous_takes_first` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 2 | killed |
| `u149.T8_mirror_link_skipped` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u149.T9_removed_row_linked` | `src/cratekit/sync/twins.py` | user | 1 file(s) | 46 | 1 | killed |
| `u213.M14_backfill_reason_check` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M15_backfill_left_action` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 4 | killed |
| `u213.M16_backfill_digest_reason` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M17_backfill_unread_tracks` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 2 | killed |
| `u213.M18_backfill_unread_reasons` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M19_matched_ambiguous_first` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M20_backfill_whole` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M2_backfill_refused_reason` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u221.R19_short_listing_records_its_misses` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 78 | 1 | killed |
| `u221.R20_landing_records_no_hold` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 38 | 1 | killed |
| `u242.M8_twins_reads_the_title_alone` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 92 | 1 | killed |
| `u320.M11_apart_halved` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M12_apart_strict` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M14_any_status_is_not_found` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 8 | killed |
| `u320.M15_context_class_counts` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M16_damaged_record_reads_empty` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M17_other_library_read` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 1 | killed |
| `u320.M19_none_drops_nothing` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 5 | killed |
| `u320.M3_any_not_found_name_counts` | `src/cratekit/sync/unavailable.py` | user | 2 file(s) | 123 | 2 | killed |
| `r838-a.U1_refuse_stranger` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U3_pass_filter` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 2 | killed |
| `r838-a.U4_already_unmarked_stamp` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U5_marked_again` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U6_later_order` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U8_title_already_back` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U10_digest_names` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U13_recheck` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U15_rename_target` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 8 | killed |
| `r838-b.U16_part_way_names` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U9_renamed_since` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-c.U7b_not_listed_rerun` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `u242.M22_unmark_releases_nothing` | `src/cratekit/sync/unmark_cli.py` | user | 4 file(s) | 190 | 7 | killed |
| `u242.M26_release_stamps_no_mark` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 78 | 3 | killed |
| `u246.S14_unmark_narrowed_empty` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 47 | 3 | killed |
| `u246.S15_unmark_narrowed_first_only` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `r263.W1_no_unrecorded_state` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 4 | killed |
| `r263.W2_state_word` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 3 | killed |
| `r263.W3_stale_record_as_completion` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 1 | killed |
| `r263.W4_stale_suffix` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 1 | killed |

## Row definitions

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

### `r1394.S1_counts_beyond_the_moves_trusted`

stopped write: counts larger than the write's moves are trusted rather than read as nothing known

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S1_counts_beyond_the_moves_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`

Old text:

```
    if sent is None or landed is None or not landed <= sent <= total:
```

New text:

```
    if sent is None or landed is None or not landed <= sent:
```

### `r1394.S2_missing_counts_read_as_none_sent`

stopped write: a moving step with no counts reads as no move sent, so any agreed path reading finishes it, as before R-1394

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S2_missing_counts_read_as_none_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts0]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts1]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts2]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts4]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`

Old text:

```
        return 0, total
    return landed, sent
```

New text:

```
        return 0, 0
    return landed, sent
```

### `r1394.S6_counts_not_wired`

stopped write: the counts read back never reach the stopped write, which keeps none landed and none sent

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S6_counts_not_wired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`
  - `tests/test_sync_pair_stopped.py::test_a_moving_step_reads_back_its_counts`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts0]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts1]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts2]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts4]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`
  - `tests/test_sync_pair_stopped.py::test_every_move_accepted_reads_as_every_move_landed_whatever_the_counts`

Old text:

```
        landed=landed,
        sent=reached_by,
```

New text:

```
        landed=0,
        sent=0,
```

### `r1394.S8_positions_first_only`

positions: only the first count on the path that leaves the order is answered, so a track taken off since hides a later one

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S8_positions_first_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`

Old text:

```
    return tuple(
        index
        for index, state in enumerate(passed(start, target))
        if [one for one in dict.fromkeys(state) if one in common] == shown
    )
```

New text:

```
    return tuple(
        index
        for index, state in enumerate(passed(start, target))
        if [one for one in dict.fromkeys(state) if one in common] == shown
    )[:1]
```

### `r1394.S9_moving_step_counts_dropped`

moving step: the record written carries a sent count of 0 whatever it is told

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S9_moving_step_counts_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 19 (killed)
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
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_that_move_leaves_it_is_finished`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        SENT: int(sent),
```

New text:

```
        SENT: 0,
```

### `r1418.F7_composite_ordering_start_unread`

what F7 holds: a stopped write with no moving step reads no start from its ordering step, so the start F7 narrows is never read

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1418.json`, row `F7_composite_ordering_start_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 20 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_finish_stopped_before_its_first_send_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_stopped.py::test_a_write_begun_ordered_and_not_finished_is_read_back_whole`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    begin = sent[1] if sent is not None else start
```

New text:

```
    begin = sent[1] if sent is not None else ()
```

### `r1434.S2_positions_compare_every_track_listed`

existing guard, U225: the path compares every track listed now, a track added since included, so an addition reads the account off the path

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1434.json`, row `S2_positions_compare_every_track_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_since_is_left_out_of_the_comparison`
  - `tests/test_sync_pair_stopped.py::test_positions_counts_the_moves_that_leave_each_order_on_the_path`

Old text:

```
    common = set(current) & set(start)
```

New text:

```
    common = set(current)
```

### `u225.M6_front_keeps_nothing`

front_moves: no tail is kept, every asked track is moved

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M6_front_keeps_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`

Old text:

```
            keep += 1
    return list(reversed(wanted[: len(wanted) - keep]))
```

New text:

```
            keep += 0
    return list(reversed(wanted[: len(wanted) - keep]))
```

### `u225.M8_reached_strict_membership`

reached: a track added or taken off since is compared too

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M8_reached_strict_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_since_is_left_out_of_the_comparison`
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`
  - `tests/test_sync_pair_stopped.py::test_positions_counts_the_moves_that_leave_each_order_on_the_path`

Old text:

```
    common = set(current) & set(start)
```

New text:

```
    common = set(current) | set(start)
```

### `u225.M9_finish_ignored`

stopped_writes: a later run that finished the pair does not hide the stopped write

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u225.json`, row `M9_finish_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_stopped.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_finished_or_unordered_write_is_no_stopped_one`
  - `tests/test_sync_pair_stopped.py::test_a_later_run_that_finished_the_pair_hides_the_stopped_write_in_either_order`

Old text:

```
            if done in steps:
                if account_id not in finished
```

New text:

```
            if False:
                if account_id not in finished
```

### `u234.O15_reordered_counts_additions`

reordered compares the readings whole, so a track added between them is read as a reorder

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u234.json`, row `O15_reordered_counts_additions`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_between_two_readings_is_no_reorder`

Old text:

```
    return [one for one in current if one in common] != [
        one for one in dict.fromkeys(kept) if one in common
    ]


__all__
```

New text:

```
    return current != list(dict.fromkeys(kept))


__all__
```

### `r1289.M1_sweep_reads_whole`

plan: read each swept playlist whole again (the declared reader is asked first), so one untitled row leaves the whole playlist out as unreadable

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M1_sweep_reads_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_playlist_with_no_tracks_queues_nothing_and_is_reported`
  - `tests/test_sync_all.py::test_a_queued_playlist_that_left_a_track_unread_is_recorded_when_its_job_succeeds`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
            listing = intake_cli.list_playlist_readable(found, playlist.playlist_id)
```

New text:

```
            intake_cli.list_playlist_declared(found, playlist.playlist_id)
            listing = intake_cli.list_playlist_readable(found, playlist.playlist_id)
```

### `r1289.M2_unread_not_kept`

plan: keep no unread track on the sweep, so the summary names none and a playlist with every track unread reads as empty

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M2_unread_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_whose_only_playlist_left_every_track_unread_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
        if listing.unread:
```

New text:

```
        if False:
```

### `r1289.M3_all_unread_branch`

plan: drop the every track unread branch, so such a playlist is excluded as empty rather than unreadable

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M3_all_unread_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_whose_only_playlist_left_every_track_unread_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`

Old text:

```
            if not tracks:
                # EVERY TRACK UNREAD
```

New text:

```
            if False:
                # EVERY TRACK UNREAD
```

### `r1289.M4_unread_why_dropped`

plan: record an unread track without the reader's why

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M4_unread_why_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_queued_playlist_that_left_a_track_unread_is_recorded_when_its_job_succeeds`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
                ref: {**one.said(), "why": one.why} for ref, one in listing.unread.items()
```

New text:

```
                ref: {**one.said()} for ref, one in listing.unread.items()
```

### `r1289.M5_all_unread_message`

plan: the every track unread playlist's unreadable message reworded so it names no track

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M5_all_unread_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`

Old text:

```
                    "no track on it could be queued: "
                    + ", ".join(f"{ref} ({one.why})" for ref, one in listing.unread.items())
```

New text:

```
                    "the playlist could not be read"
```

### `r1289.M6_report_unread_emptied`

report: the unread block names each playlist with no tracks under it

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M6_report_unread_emptied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
            identity: {"name": names.get(identity, ""), "tracks": dict(tracks)}
```

New text:

```
            identity: {"name": names.get(identity, ""), "tracks": {}}
```

### `r1289.M7_per_playlist_reraise`

plan (existing guard, sample): take any refusal as one playlist's, so an expired session reads as one unreadable playlist and the sweep goes on

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M7_per_playlist_reraise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_refusal_not_about_one_playlist_still_stops_the_sweep`

Old text:

```
            if exc.cause.reason not in PER_PLAYLIST_REASONS:
                raise
            sweep.excluded[playlist.playlist_id] = Excluded.UNREADABLE
```

New text:

```
            if False:
                raise
            sweep.excluded[playlist.playlist_id] = Excluded.UNREADABLE
```

### `r1289.M8_per_playlist_set`

PER_PLAYLIST_REASONS (existing guard, sample): drop the reader's refusal, so a row with no provider id stops the whole sweep

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M8_per_playlist_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_row_with_no_provider_id_still_leaves_its_playlist_out_by_name`

Old text:

```
PER_PLAYLIST_REASONS = frozenset({"label-playlist-unreadable", "intake-list-unusable"})
```

New text:

```
PER_PLAYLIST_REASONS = frozenset({"label-playlist-unreadable"})
```

### `r1289.M9_short_check`

plan (existing guard, sample): drop the declared count check, so a short listing is queued without saying what the provider withheld

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M9_short_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
        if listing.short is not None:
```

New text:

```
        if False:
```

### `r358.S10_mark_always_unbound`

Report the mark unbound whether or not the step ran

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S10_mark_always_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_block_tells_a_mark_that_ran_apart_from_a_mark_that_never_ran`

Old text:

```
        "mark": MARK_UNBOUND if marked is None else MARK_APPLIED,
```

New text:

```
        "mark": MARK_UNBOUND,
```

### `r358.S1_set_is_the_cursor`

Take the mark set from recorded_now again, the review's finding 1

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S1_set_is_the_cursor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_that_did_not_land_is_offered_again_by_the_next_pass`
  - `tests/test_sync_all.py::test_a_recorded_debris_playlist_is_not_pending_at_all`

Old text:

```
        for identity in sorted(sweep.recorded)
```

New text:

```
        for identity in sorted(sweep.recorded_now)
```

### `r358.S5_recheck_is_a_second_read`

Serve the recheck from the plan's own listing instead of a fresh read

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S5_recheck_is_a_second_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_after_a_real_importable_file_takes_the_recorded_playlist`
  - `tests/test_sync_all.py::test_a_playlist_gone_from_the_account_since_the_plan_is_not_marked`
  - `tests/test_sync_all.py::test_a_playlist_renamed_on_the_account_since_the_plan_is_left_alone`

Old text:

```
        name = listed.get(mark.target_id) or ""
        return bool(name) and current().get(mark.target_id) == name
```

New text:

```
        name = listed.get(mark.target_id) or ""
        return bool(name) and listed.get(mark.target_id) == name
```

### `r358.S7_lazy_listing`

Read the account eagerly, so a call with no file still spends a listing

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S7_lazy_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_without_a_real_importable_file_renames_nothing`

Old text:

```
    held: list[dict[str, str]] = []

    def current() -> dict[str, str]:
```

New text:

```
    held: list[dict[str, str]] = [
        {playlist.playlist_id: playlist.name for playlist in _listed_or_refuse(found)}
    ]

    def current() -> dict[str, str]:
```

### `r358.S9_mark_always_applied`

Report the mark applied whether or not the step ran

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S9_mark_always_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_renames_nothing_even_over_a_recorded_playlist_with_its_file_landed`
  - `tests/test_sync_all.py::test_a_slim_pass_queues_each_new_account_playlist_under_the_shared_run`
  - `tests/test_sync_all.py::test_the_block_tells_a_mark_that_ran_apart_from_a_mark_that_never_ran`
  - `tests/test_sync_all.py::test_the_current_intake_path_marks_nothing_and_still_reports_unbound`

Old text:

```
        "mark": MARK_UNBOUND if marked is None else MARK_APPLIED,
```

New text:

```
        "mark": MARK_APPLIED,
```

### `r359.M10_claims_downloaded`

Reword the sentence into the false claim the defect is about, that the files were downloaded

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M10_claims_downloaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
            "the library, crate intake missing lists it, and no later sync offers "
```

New text:

```
            "the library until downloaded, and no later sync offers "
```

### `r359.M1_drop_field`

Drop the swept_means field from the playlists block, the row the brief names

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M1_drop_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_json_its_tracks_were_resolved_not_acquired`
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
        "swept_means": SWEPT_MEANS,

```

New text:

```
(empty)
```

### `r359.M2_token`

Change the machine token to a nearby word that no longer says not acquired

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M2_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_json_its_tracks_were_resolved_not_acquired`
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
SWEPT_MEANS = "resolved-not-acquired"
```

New text:

```
SWEPT_MEANS = "resolved"
```

### `r359.M3_said_silent`

said returns nothing, so the check carries no sentence while the json field stays

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M3_said_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
    return SWEPT_MEANS_SAID.get(str(block.get("swept_means") or ""))
```

New text:

```
    return None
```

### `r359.M4_said_unconditional`

said answers whatever the block carries, decoupling the sentence from the field

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M4_said_unconditional`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
    return SWEPT_MEANS_SAID.get(str(block.get("swept_means") or ""))
```

New text:

```
    return SWEPT_MEANS_SAID[SWEPT_MEANS]
```

### `r359.M8_drop_resolved`

Reword the sentence so it no longer says the tracks were resolved

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M8_drop_resolved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
            "a recorded playlist had its tracks resolved against the library, not "
```

New text:

```
            "a recorded playlist had its tracks checked against the library, not "
```

### `r359.M9_drop_not_acquired`

Reword the sentence so it no longer says the tracks were not acquired

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M9_drop_not_acquired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
            "acquired, so a track its intake job reported missing is still not in "
```

New text:

```
            "fetched, so a track its intake job reported missing is still not in "
```

### `r359.S1_record_on_any_state`

Existing guard sample: the cursor records a playlist whatever state its job ended in

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `S1_record_on_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_failed_job_is_not_recorded_and_its_playlist_is_offered_again`
  - `tests/test_sync_all.py::test_a_playlist_intake_by_hand_that_did_not_succeed_is_not_recorded[cancelled]`
  - `tests/test_sync_all.py::test_a_playlist_intake_by_hand_that_did_not_succeed_is_not_recorded[failed]`
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`
  - `tests/test_sync_all.py::test_the_cursor_records_ids_only_once_a_job_succeeds`

Old text:

```
        if job.state == jobs.JobState.SUCCEEDED and identity and identity not in seen:
```

New text:

```
        if identity and identity not in seen:
```

### `r361-a.A10_enum_value_respelled`

The enum member's kebab value changes, so the report and the check say another word

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A10_enum_value_respelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`
  - `tests/test_sync_all.py::test_a_pass_that_finds_only_debris_says_so_on_the_check`
  - `tests/test_sync_all.py::test_the_label_batch_debris_is_not_queued_as_intake`
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
    LABEL_DEBRIS = "label-debris"
```

New text:

```
    LABEL_DEBRIS = "label-library"
```

### `r361-a.A2_case_insensitive`

The rule widens to any case, so a person's Colorize Library is excluded too

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A2_case_insensitive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`
  - `tests/test_sync_all.py::test_a_recorded_debris_playlist_is_not_pending_at_all`
  - `tests/test_sync_all.py::test_the_label_batch_debris_is_not_queued_as_intake`

Old text:

```
    return str(name or "").endswith(LIBRARY_PLAYLIST_SUFFIX)
```

New text:

```
    return str(name or "").upper().endswith(LIBRARY_PLAYLIST_SUFFIX)
```

### `r361-a.A3_no_leading_space`

The suffix loses its leading space, so ColorizeLIBRARY is debris

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A3_no_leading_space`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`

Old text:

```
LIBRARY_PLAYLIST_SUFFIX = " LIBRARY"
```

New text:

```
LIBRARY_PLAYLIST_SUFFIX = "LIBRARY"
```

### `r361-a.A4_substring_not_suffix`

endswith becomes in, so LIBRARY Colorize and Colorize LIBRARY 2 are debris

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A4_substring_not_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`

Old text:

```
    return str(name or "").endswith(LIBRARY_PLAYLIST_SUFFIX)
```

New text:

```
    return LIBRARY_PLAYLIST_SUFFIX in str(name or "")
```

### `r361-a.D2_drop_the_placeholder`

Existing: the favourites placeholder is queued by the playlists source

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `D2_drop_the_placeholder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_playlist_exclusions_in_the_order_a_person_is_told`
  - `tests/test_sync_all.py::test_the_favourites_placeholders_are_left_to_the_favourites_source`

Old text:

```
    if placeholders.is_placeholder(playlist.name):
        return Excluded.PLACEHOLDER

```

New text:

```
(empty)
```

### `r361-a.D3_drop_in_flight`

Existing: an open job no longer holds its playlist back, so it is queued twice

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `D3_drop_in_flight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_playlist_exclusions_in_the_order_a_person_is_told`
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`
  - `tests/test_sync_all.py::test_the_cursor_records_ids_only_once_a_job_succeeds`

Old text:

```
    if playlist.playlist_id in in_flight:
        return Excluded.IN_FLIGHT

```

New text:

```
(empty)
```

### `r382.M11_reconcile_source_jobs`

reconcile reads source_jobs again instead of playlist_jobs

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M11_reconcile_source_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_ingested_by_hand_is_recorded_on_the_next_pass`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://listen.tidal.com/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1?u]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://tidal.com/browse/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1]`

Old text:

```
        for identity in completed(playlist_jobs(store, cfg, handler_key=handler_key))
```

New text:

```
        for identity in completed(source_jobs(store, cfg, handler_key=handler_key))
```

### `r382.M12_in_flight_source_jobs`

plan's in flight set reads source_jobs again instead of playlist_jobs

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M12_in_flight_source_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`

Old text:

```
    in_flight = open_playlists(playlist_jobs(store, cfg, handler_key=handler_key))
```

New text:

```
    in_flight = open_playlists(source_jobs(store, cfg, handler_key=handler_key))
```

### `r382.M13_marking_source_jobs`

marking_sweep reads source_jobs again instead of playlist_jobs

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M13_marking_source_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_reads_a_playlist_ingested_by_hand_as_recorded`

Old text:

```
    held.update(completed(playlist_jobs(store, cfg, handler_key=handler_key)))
```

New text:

```
    held.update(completed(source_jobs(store, cfg, handler_key=handler_key)))
```

### `r382.M15_completed_duplicates`

Sample of an existing guard: completed records a playlist once per succeeded job

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M15_completed_duplicates`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_two_succeeded_jobs_for_one_playlist_record_it_once`

Old text:

```
        if job.state == jobs.JobState.SUCCEEDED and identity and identity not in seen:
```

New text:

```
        if job.state == jobs.JobState.SUCCEEDED and identity:
```

### `r382.M1_restore_source_filter`

Restore the source_id == playlists filter on playlist_jobs, the brief's named row: a hand queued job is no longer reconciled or in flight

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M1_restore_source_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_reads_a_playlist_ingested_by_hand_as_recorded`
  - `tests/test_sync_all.py::test_a_playlist_ingested_by_hand_is_recorded_on_the_next_pass`
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://listen.tidal.com/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1?u]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://tidal.com/browse/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1]`

Old text:

```
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
        and (job.payload or {}).get("source_id") == SOURCE_ID
    )
```

### `r382.M2_drop_handler_key`

Drop the handler key filter from playlist_jobs, so an intake.set job naming a playlist is reconciled

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M2_drop_handler_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_set_intake_naming_the_playlist_is_not_a_playlist_intake`

Old text:

```
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        if job.library_id == cfg.library.volume_id
    )
```

### `r382.M3_drop_library`

Drop the library filter from playlist_jobs, so another library's finished job records here

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M3_drop_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_another_librarys_finished_job_is_not_this_librarys_sweep`

Old text:

```
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        if job.handler_key == handler_key
    )
```

### `r382.M4_hearts_recorded`

Drop the reserved hearts reference check in recorded_as, so a hearts job records favorites

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M4_hearts_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_intake_is_not_recorded_as_a_playlist`

Old text:

```
    if intake_cli.is_favorites(reference):
        return ""
```

New text:

```
(empty)
```

### `r382.M5_no_verbatim_for_pass_jobs`

Drop the verbatim return for a pass's own job, so its listing id goes through the lowercasing parser

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M5_no_verbatim_for_pass_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_queued_job_records_the_listing_identifier_verbatim`

Old text:

```
    if (job.payload or {}).get("source_id") == SOURCE_ID:
        return reference

```

New text:

```
(empty)
```

### `r382.M6_no_parse`

Record a hand typed reference verbatim instead of parsing it, so a typed URL is recorded as the URL

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M6_no_parse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://listen.tidal.com/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1?u]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://tidal.com/browse/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1]`

Old text:

```
        return typed_playlist_id(reference)
```

New text:

```
        return reference
```

### `r382.M7_invalid_records_nothing`

An unparseable hand reference records nothing instead of itself

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M7_invalid_records_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_reads_a_playlist_ingested_by_hand_as_recorded`
  - `tests/test_sync_all.py::test_a_playlist_ingested_by_hand_is_recorded_on_the_next_pass`
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`

Old text:

```
    except PlaylistReferenceInvalid:
        return reference
```

New text:

```
    except PlaylistReferenceInvalid:
        return ""
```

### `r382.M8_completed_raw`

completed reads the raw payload reference instead of recorded_as

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M8_completed_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_intake_is_not_recorded_as_a_playlist`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://listen.tidal.com/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1?u]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://tidal.com/browse/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1]`

Old text:

```
        identity = recorded_as(job)
        if job.state == jobs.JobState.SUCCEEDED
```

New text:

```
        identity = _playlist_of(job)
        if job.state == jobs.JobState.SUCCEEDED
```

### `r382.M9_open_raw`

open_playlists reads the raw payload reference instead of recorded_as

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M9_open_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`

Old text:

```
    return frozenset(recorded_as(job) for job in found if job.is_open() and recorded_as(job))
```

New text:

```
    return frozenset(_playlist_of(job) for job in found if job.is_open() and _playlist_of(job))
```

### `r835-b.S1_built_year_excluded_from_sweep`

sync.playlists.exclusion: a year playlist a label build recorded is swept as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `r835-b.json`, row `S1_built_year_excluded_from_sweep`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 271 against a baseline of 271
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_the_sweep_never_reads_a_built_year_playlist_as_intake`

Old text:

```
    if playlist.playlist_id in label_built:
        return Excluded.LABEL_FOLDER
```

New text:

```
    if False:
        return Excluded.LABEL_FOLDER
```

### `r837-a.A16_sweep_excludes_set`

sync.playlists.exclusion: a set playlist export set recorded is swept as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `r837-a.json`, row `A16_sweep_excludes_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_incremental_sync.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 327 against a baseline of 327
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_sweep_never_reads_a_set_playlist_as_intake`

Old text:

```
    if playlist.playlist_id in set_built:
        return Excluded.SET_PLAYLIST
```

New text:

```
    if False:
        return Excluded.SET_PLAYLIST
```

### `u113-a.A6_sweep_passes_no_name`

The sweep queues each playlist job without the account's name

- File: `src/cratekit/sync/playlists.py`
- Source: `u113-a.json`, row `A6_sweep_passes_no_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_sync_all.py`
- Collected: 147 against a baseline of 147
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_sync_all_records_the_name_the_account_listed_on_each_playlist_job`

Old text:

```
                name=names.get(playlist_id),
```

New text:

```
                name=None,
```

### `u130-c.C9_sweep_takes_paired`

The playlists sweep offers a paired playlist as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `u130-c.json`, row `C9_sweep_takes_paired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_the_sweep_excludes_a_paired_playlist`
  - `tests/test_sync_pair.py::test_the_sync_pass_hands_the_pairs_to_the_sweep`

Old text:

```
    if playlist.playlist_id in paired:
```

New text:

```
    if False:
```

### `u147-c.M18_sweep_exclusion`

sync.playlists.exclusion: a mirrored playlist is swept as intake

- File: `src/cratekit/sync/playlists.py`
- Source: `u147-c.json`, row `M18_sweep_exclusion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
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

### `u242.M1_exclusion_reads_the_ledger`

exclusion: answer SWEPT from the legacy prefix alone, so a stripped taken playlist is offered as new

- File: `src/cratekit/sync/playlists.py`
- Source: `u242.json`, row `M1_exclusion_reads_the_ledger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 230 against a baseline of 230
- Kills: 5 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_mark_since_u242_writes_no_title_and_the_playlist_is_never_offered`
  - `tests/test_u242_taken.py::test_exclusion_answers_swept_for_a_taken_playlist_with_no_prefix`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    if is_taken(playlist.playlist_id, playlist.name, taken):
        return Excluded.SWEPT
```

New text:

```
    if is_swept_name(playlist.name):
        return Excluded.SWEPT
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
- Collected: 386 against a baseline of 386
- Kills: 22 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mark_put_back_is_no_mark_and_the_playlist_stays`
  - `tests/test_organize.py::test_a_prefixed_but_unmarked_playlist_has_its_own_reason`
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
  - ... and 7 more, see the JSON sidecar

Old text:

```
    return str(playlist_id or "") in taken or is_swept_name(name)
```

New text:

```
    return str(playlist_id or "") in taken
```

### `u242.M4_plan_reads_no_ledger`

plan: hand exclusion an empty ledger, so sync all offers every stripped playlist

- File: `src/cratekit/sync/playlists.py`
- Source: `u242.json`, row `M4_plan_reads_no_ledger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_all.py`
- Collected: 161 against a baseline of 161
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_that_landed_is_not_owed_a_second_time`
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_mark_since_u242_writes_no_title_and_the_playlist_is_never_offered`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    taken = taken_ids(cfg)

    sweep = Sweep(
```

New text:

```
    taken = frozenset()

    sweep = Sweep(
```

### `u242.M5_pending_marks_ignores_the_ledger`

pending_marks: skip only a prefixed title, so a playlist already taken is taken again

- File: `src/cratekit/sync/playlists.py`
- Source: `u242.json`, row `M5_pending_marks_ignores_the_ledger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 230 against a baseline of 230
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_that_landed_is_not_owed_a_second_time`

Old text:

```
        and not is_taken(identity, listed[identity], sweep.taken)
```

New text:

```
        and not is_swept_name(listed[identity])
```

### `u82-a.A5_only_narrows`

pending_marks: drop the only filter, so every recorded playlist is pending whatever the caller named

- File: `src/cratekit/sync/playlists.py`
- Source: `u82-a.json`, row `A5_only_narrows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_debris_playlist_is_not_pending_at_all`
  - `tests/test_sync_mark.py::test_a_native_pass_takes_playlist_as_the_file_does`
  - `tests/test_sync_mark.py::test_a_native_pass_with_one_track_not_held_leaves_that_playlist_alone`
  - `tests/test_sync_mark.py::test_a_playlist_whose_reports_cannot_be_read_is_left_alone`
  - `tests/test_sync_mark.py::test_a_playlist_with_one_row_not_landed_is_not_marked`
  - `tests/test_sync_mark.py::test_a_track_the_pass_offered_for_review_holds_its_playlist_back`
  - `tests/test_sync_mark.py::test_only_narrows_the_pending_set_and_an_empty_set_is_nothing`
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`
  - `tests/test_sync_mark.py::test_the_pass_is_decided_without_its_manifest`

Old text:

```
        and (only is None or identity in only)
```

New text:

```
(empty)
```

### `u82-a.A6_an_empty_only_is_nothing`

pending_marks: read only by truth and not by None, so an empty set, which is no finished playlist, marks every pending one

- File: `src/cratekit/sync/playlists.py`
- Source: `u82-a.json`, row `A6_an_empty_only_is_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_only_narrows_the_pending_set_and_an_empty_set_is_nothing`

Old text:

```
        and (only is None or identity in only)
```

New text:

```
        and (not only or identity in only)
```

### `u82-a.A7_mark_swept_hands_only_through`

mark_swept: stop handing only to pending_marks, so the verb's finished set is ignored at the one place it is applied

- File: `src/cratekit/sync/playlists.py`
- Source: `u82-a.json`, row `A7_mark_swept_hands_only_through`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_takes_playlist_as_the_file_does`
  - `tests/test_sync_mark.py::test_a_native_pass_with_one_track_not_held_leaves_that_playlist_alone`
  - `tests/test_sync_mark.py::test_a_playlist_whose_reports_cannot_be_read_is_left_alone`
  - `tests/test_sync_mark.py::test_a_playlist_with_one_row_not_landed_is_not_marked`
  - `tests/test_sync_mark.py::test_a_track_the_pass_offered_for_review_holds_its_playlist_back`
  - `tests/test_sync_mark.py::test_only_narrows_the_pending_set_and_an_empty_set_is_nothing`
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`
  - `tests/test_sync_mark.py::test_the_pass_is_decided_without_its_manifest`

Old text:

```
        pending_marks(sweep, only=only),
```

New text:

```
        pending_marks(sweep),
```

### `u221.R21_unknown_name_not_refused`

release plan: drop the refusal of a name that is no twin's, so it reaches the lookup

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R21_unknown_name_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned`

Old text:

```
        if missing:
            raise _not_a_twin(missing)
```

New text:

```
        if False:
            raise _not_a_twin(missing)
```

### `u221.R22_all_beside_names`

sync_release: drop the refusal of names beside --all

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R22_all_beside_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args1]`

Old text:

```
    if every and named:
```

New text:

```
    if False:
```

### `u221.R23_nothing_named`

sync_release: drop the refusal of a run naming nothing, so it plans nothing silently

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R23_nothing_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args0]`

Old text:

```
    if not every and not named:
```

New text:

```
    if False:
```

### `u221.R25_released_twin_asks_again`

Planned.action: a twin holding nothing reads as one to release, so a second run asks again over nothing

- File: `src/cratekit/sync/release_cli.py`
- Source: `u221.json`, row `R25_released_twin_asks_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_cli_contract.py`
- Collected: 1029 against a baseline of 1029
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_released_twin_asks_nothing_the_second_time`

Old text:

```
        return NOTHING_HELD if self.held is not None and not self.held else RELEASE
```

New text:

```
        return RELEASE
```

### `r1830.M18_plan_counts_nothing`

plan_removed: count no renumbering, so the screen shows none

- File: `src/cratekit/sync/removed.py`
- Source: `r1830.json`, row `M18_plan_counts_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`

Old text:

```
        renumbered=len(rb_writer.CollectionRemoval.renumbering(db, offered)) if offered else 0,
```

New text:

```
        renumbered=0,
```

### `r1830.M19_digest_omits_the_count`

identity: leave the renumbering count out of the digest

- File: `src/cratekit/sync/removed.py`
- Source: `r1830.json`, row `M19_digest_omits_the_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`

Old text:

```
        "renumbered": plan.renumbered,
    }
```

New text:

```
    }
```

### `r1830.M22_applied_message_counts_nothing`

apply_removed: the result counts no renumbered membership, so the applied message says none

- File: `src/cratekit/sync/removed.py`
- Source: `r1830.json`, row `M22_applied_message_counts_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`

Old text:

```
        renumbered=len(removal.renumbered),
```

New text:

```
        renumbered=0,
```

### `u287-m11.M11_gone_offers_nothing`

removals: read a playlist not read whole as removing every track, measured again after the zero of the first table was given a test

- File: `src/cratekit/sync/removed.py`
- Source: `u287-m11.json`, row `M11_gone_offers_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[empty]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[short]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[unreadable]`

Old text:

```
        if one.account in reads and reads[one.account].state == READ
```

New text:

```
        if one.account in reads
```

### `u287.M13_folder_separator`

_under: compare the folder as a bare prefix, so a sibling folder sharing its name's start reads as the pass's

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M13_folder_separator`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_path_is_under_a_folder_only_past_a_separator_and_in_one_unicode_form`

Old text:

```
        if root and (held.startswith(root + "/") or held.startswith(root + "\\")):
```

New text:

```
        if root and held.startswith(root):
```

### `u287.M14_twin_is_own_filing`

plan_removed: leave the recorded twins out of the pass's own filing, so the landing's own twin keeps a track

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M14_twin_is_own_filing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 32 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[True]`
  - `tests/test_sync_removed.py::test_a_genre_playlist_of_a_native_routing_tree_keeps_nothing`
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before`
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_says_holds_none_is_read_empty_and_every_new_track_offered`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_refused_removal_gives_the_deletion_pass_no_position`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`
  - ... and 17 more, see the JSON sidecar

Old text:

```
            own = own_nodes.union(
                *(made.get(account, frozenset()) for account in held.accounts),
            )
```

New text:

```
            own = own_nodes
```

### `u287.M17_gone_with_no_record_is_not_whole`

read_one: read a playlist neither read finds and nothing records as gone, holding nothing, rather than not read whole

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M17_gone_with_no_record_is_not_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_nothing_records_that_neither_read_finds_offers_nothing`

Old text:

```
            if not known:
                return Listing(
```

New text:

```
            if False:
                return Listing(
```

### `u287.M18_set_aside_rows_count`

read_one: leave the reader's set aside rows out of the identity sets

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M18_set_aside_rows_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc`

Old text:

```
        for one in readable.unread.values()
    )
```

New text:

```
        for one in ()
    )
```

### `u287.M19_old_prefix_is_synced`

synced: leave a playlist still titled with the retired swept prefix out of the synced set

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M19_old_prefix_is_synced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_playlist_still_titled_with_the_old_prefix_is_synced`

Old text:

```
                    if playlists.is_swept_name(one.name)
```

New text:

```
                    if False
```

### `u287.M1_partial_read_stops_offers`

plan_removed: never read a synced listing as partial, so an unreadable, short or empty playlist or hearts no longer stops any offer

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M1_partial_read_stops_offers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[empty]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[short]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[unreadable]`
  - `tests/test_sync_removed.py::test_a_synced_playlist_nothing_records_that_neither_read_finds_offers_nothing`
  - `tests/test_sync_removed.py::test_hearts_not_read_whole_offer_nothing[empty]`
  - `tests/test_sync_removed.py::test_hearts_not_read_whole_offer_nothing[short]`
  - `tests/test_sync_removed.py::test_hearts_not_read_whole_offer_nothing[unreadable]`

Old text:

```
    partial = any(one.state in NOT_WHOLE for one in listings)
```

New text:

```
    partial = False
```

### `u287.M20_unreadable_record_is_not_whole`

recorded_contents: read a gone playlist whose job reports cannot be read as holding nothing recorded, refusing the verb

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M20_unreadable_record_is_not_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_damaged_job_of_another_playlist_never_refuses_the_verb[False]`

Old text:

```
        except CratekitError:
            return None
        return tuple(found) or None
```

New text:

```
        except ZeroDivisionError:
            return None
        return tuple(found) or None
```

### `u287.M2_held_by_isrc`

Listing.holds: drop the ISRC test, so a track relisted under another id with its ISRC reads as removed

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M2_held_by_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_listing_holds_a_track_by_any_of_three_tests_and_only_a_read_or_gone_one_holds`
  - `tests/test_sync_removed.py::test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc`
  - `tests/test_sync_removed.py::test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording`

Old text:

```
        if wanted.isrc and wanted.isrc.strip().upper() in self.isrcs:
```

New text:

```
        if False and wanted.isrc and wanted.isrc.strip().upper() in self.isrcs:
```

### `u287.M3_held_by_recording`

Listing.holds: drop the folded recording test, so a relinked track with its artist and title reads as removed

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M3_held_by_recording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_listing_holds_a_track_by_any_of_three_tests_and_only_a_read_or_gone_one_holds`
  - `tests/test_sync_removed.py::test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording`

Old text:

```
        return recording(wanted) in self.recordings
```

New text:

```
        return False
```

### `u287.M4_held_before_the_pass`

_answer: drop the held before the pass keep, so a track the library owned when the job ran can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M4_held_before_the_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_says_holds_none_is_read_empty_and_every_new_track_offered`

Old text:

```
    if not held.carried:
        return replace(shown, why=HELD_BEFORE)
```

New text:

```
    if False:
        return replace(shown, why=HELD_BEFORE)
```

### `u287.M5_not_this_pass_file`

_answer: drop the filed folder keep, so a hand brought file the match found can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M5_not_this_pass_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_file_another_pass_filed_is_not_this_pass_s_file`
  - `tests/test_sync_removed.py::test_a_match_on_a_file_the_pass_did_not_file_is_kept`

Old text:

```
    if not held.brought:
        return replace(shown, why=NOT_THIS_PASS)
```

New text:

```
    if False:
        return replace(shown, why=NOT_THIS_PASS)
```

### `u287.M6_on_another_synced`

_answer: drop the still on another synced playlist keep

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M6_on_another_synced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_gone_downloaded_playlist_holds_what_its_pass_recorded`
  - `tests/test_sync_removed.py::test_a_gone_playlist_a_pass_swept_and_never_landed_holds_what_it_recorded`
  - `tests/test_sync_removed.py::test_a_playlist_a_later_pass_swept_and_never_landed_still_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_playlist_still_titled_with_the_old_prefix_is_synced`
  - `tests/test_sync_removed.py::test_a_playlist_the_account_list_omits_and_its_id_opens_is_read_and_keeps_its_tracks`
  - `tests/test_sync_removed.py::test_a_row_the_reader_set_aside_keeps_a_track_by_its_isrc`
  - `tests/test_sync_removed.py::test_a_track_hearted_on_the_account_is_kept_by_the_hearts`
  - `tests/test_sync_removed.py::test_a_track_still_on_another_synced_playlist_is_kept_by_id_isrc_and_recording`

Old text:

```
    if still:
        return replace(shown, why=ON_ANOTHER, kept_by=still)
```

New text:

```
    if False:
        return replace(shown, why=ON_ANOTHER, kept_by=still)
```

### `u287.M7_in_a_playlist_of_yours`

_answer: drop the playlist of yours keep, so a track in a hand made playlist or All Favorites can be offered

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M7_in_a_playlist_of_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_genre_playlist_of_a_native_routing_tree_keeps_nothing`
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_track_in_a_playlist_of_yours_is_kept_and_its_own_filing_keeps_nothing`

Old text:

```
    if yours:
        return replace(shown, why=IN_YOURS, kept_by=yours)
```

New text:

```
    if False:
        return replace(shown, why=IN_YOURS, kept_by=yours)
```

### `u287.M8_empty_read_untrusted`

read_one: trust an empty read with an unknown count, so a provider fault reads every track removed

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M8_empty_read_untrusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[empty]`

Old text:

```
    if not readable.order and (shown is None or shown.tracks != 0):
```

New text:

```
    if False:
```

### `u287.M9_short_read_untrusted`

read_one: trust a listing short of its declared count

- File: `src/cratekit/sync/removed.py`
- Source: `u287.json`, row `M9_short_read_untrusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_synced_playlist_not_read_whole_offers_nothing_from_any_playlist[short]`

Old text:

```
    if readable.short is not None:
        block = readable.short.block()
```

New text:

```
    if False:
        block = readable.short.block()
```

### `u288.M16_stale_digest`

apply_removed: never refuse a plan that moved between the gate and the write

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M16_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_plan_that_moved_before_the_write_refuses_with_nothing_written`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u288.M17_only_the_offered`

apply_removed: take out every answered row that has one, kept rows included, not only the offered

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M17_only_the_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`

Old text:

```
    offered = plan.offered
    if not offered:
```

New text:

```
    offered = tuple(one for one in plan.answers if one.content_id)
    if not offered:
```

### `u288.M18_unmeasured_kept`

_answer: drop the keep of a row an unmeasured table names, so a vox tagged track is offered and then refuses the apply

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M18_unmeasured_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_row_a_my_tag_names_is_kept_and_never_offered_and_the_rest_is_removed`

Old text:

```
    if unmeasured:
        return replace(shown, why=UNMEASURED, kept_by=tuple(sorted(unmeasured)))
```

New text:

```
    if False:
        return replace(shown, why=UNMEASURED, kept_by=tuple(sorted(unmeasured)))
```

### `u288.M19_first_position`

apply_removed: give the deletion pass no first position, so a first delete review accepts the removal as history

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M19_first_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`

Old text:

```
        first = _first_deletion_position(cfg, db)
```

New text:

```
        first = None
```

### `u288.M20_read_back_refusal`

apply_removed: report a read back that disagrees as success

- File: `src/cratekit/sync/removed.py`
- Source: `u288.json`, row `M20_read_back_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`

Old text:

```
        violations = removal.read_back()
        if violations:
```

New text:

```
        violations = removal.read_back()
        if False:
```

### `u320-m5.M5_retired_holds`

Listing.holds: count a retired playlist among the holding states

- File: `src/cratekit/sync/removed.py`
- Source: `u320-m5.json`, row `M5_retired_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_retired_listing_holds_nothing_whatever_it_carries`

Old text:

```
HOLDING = frozenset({READ, GONE, WITHHELD})
```

New text:

```
HOLDING = frozenset({READ, GONE, WITHHELD, RETIRED})
```

### `u320.M10_reopened_keeps_its_retirement`

read_one: a playlist that opens again keeps its entry, so its retirement survives

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M10_reopened_keeps_its_retirement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_that_opens_again_is_read_again_and_the_retirement_cleared`
  - `tests/test_sync_removed_gone.py::test_retire_writes_every_reads_answer_with_the_retirement`

Old text:

```
        state=READ,
        refs=frozenset(str(one) for one in readable.order),
```

New text:

```
        state=READ,
        noted=prior,
        refs=frozenset(str(one) for one in readable.order),
```

### `u320.M13_withheld_bound_widened`

WITHHELD_AT_MOST: read the hearts whole when short by up to half their count, so a dropped window reads as withheld

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M13_withheld_bound_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_hearts_short_by_more_than_a_tenth_of_their_count_stay_partial[over-a-tenth]`

Old text:

```
WITHHELD_AT_MOST = 0.10
```

New text:

```
WITHHELD_AT_MOST = 0.5
```

### `u320.M18_opened_and_refused_is_unopened`

read_one: read a playlist that opened and whose rows the reader refused as unlisted and unopened, so it keeps its retirement

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M18_opened_and_refused_is_unopened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_opens_and_whose_rows_are_refused_is_cleared`

Old text:

```
        if shown is None and exc.cause.reason != SERVED_UNREADABLE:
```

New text:

```
        if shown is None:
```

### `u320.M4_withheld_hearts_hold_nothing`

Listing.holds: leave the withheld hearts out of the holding states, so a hearted track they served is offered

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M4_withheld_hearts_hold_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_hearts_short_by_the_withheld_count_hold_every_heart_served`
  - `tests/test_sync_removed_gone.py::test_hearts_short_only_by_what_the_provider_withholds_read_whole_and_still_keep_a_heart`

Old text:

```
HOLDING = frozenset({READ, GONE, WITHHELD})
```

New text:

```
HOLDING = frozenset({READ, GONE})
```

### `u320.M6_any_failure_is_a_sighting`

read_one: record a sighting for any failure of an unlisted playlist, an outage included

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M6_any_failure_is_a_sighting`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_downloaded_playlist_gone_from_the_account_is_named_and_offers_nothing`
  - `tests/test_sync_removed_gone.py::test_a_playlist_that_failed_any_other_way_twice_a_day_apart_is_never_retired`
  - `tests/test_sync_removed_gone.py::test_pythons_own_not_found_classes_are_no_sighting_and_never_retire[file-not-found]`
  - `tests/test_sync_removed_gone.py::test_pythons_own_not_found_classes_are_no_sighting_and_never_retire[module-not-found]`

Old text:

```
                if said_none
                else prior
```

New text:

```
                if True
                else prior
```

### `u320.M7_outage_forgets_the_record`

read_one: an unlisted playlist whose id failed some other way drops its entry, a retirement included

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M7_outage_forgets_the_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_now_fails_another_way_stops_offers_this_run_and_stays_retired`

Old text:

```
                if said_none
                else prior
```

New text:

```
                if said_none
                else None
```

### `u320.M8_retirement_never_applies`

read_one: never read a retired entry as retired

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M8_retirement_never_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a179s_shape_offers_the_track_once_the_gone_playlist_answers_not_found_a_day_apart`
  - `tests/test_sync_removed_gone.py::test_a_retired_downloaded_playlist_offers_none_of_its_tracks_and_holds_none_of_them`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_now_fails_another_way_stops_offers_this_run_and_stays_retired`
  - `tests/test_sync_removed_gone.py::test_retire_answered_retire_records_the_playlist_and_the_next_run_offers_past_it`
  - `tests/test_sync_removed_gone.py::test_the_control_taken_off_one_of_two_synced_playlists_is_kept_naming_the_other`

Old text:

```
            if said_none and noted is not None and noted.is_retired:
```

New text:

```
            if False:
```

### `u320.M9_relisted_keeps_its_retirement`

read_one: a playlist the account lists again keeps its entry, so its retirement survives

- File: `src/cratekit/sync/removed.py`
- Source: `u320.json`, row `M9_relisted_keeps_its_retirement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_the_account_lists_again_stops_every_offer_again`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_opens_and_whose_rows_are_refused_is_cleared`

Old text:

```
        return Listing(account=account, name=name, state=UNREADABLE, why=exc.cause.message)
```

New text:

```
        return Listing(account=account, name=name, state=UNREADABLE, why=exc.cause.message, noted=prior)
```

### `r1830.M20_screen_omits_the_count`

facts: the gate's screen shows no renumbering

- File: `src/cratekit/sync/removed_cli.py`
- Source: `r1830.json`, row `M20_screen_omits_the_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`

Old text:

```
        "kept or left": len(plan.answers) - len(plan.offered),
        "memberships renumbered": plan.renumbered,
```

New text:

```
        "kept or left": len(plan.answers) - len(plan.offered),
        "memberships renumbered": 0,
```

### `u288.M21_gate_answer`

sync_removed: apply whatever the gate is answered, abort included

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u288.json`, row `M21_gate_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_a_new_track_taken_off_is_offered_and_an_owned_one_is_kept_as_held_before`
  - `tests/test_sync_removed.py::test_abort_writes_nothing`
  - `tests/test_sync_removed.py::test_nothing_is_written_and_the_digest_holds_until_an_answer_moves`

Old text:

```
    if ctx.gate.require(_gate(ctx.entry), plan=data, context=facts(plan)) != "apply":
```

New text:

```
    if ctx.gate.require(_gate(ctx.entry), plan=data, context=facts(plan)) == "never":
```

### `u288.M22_closed_at_open`

written: open the write handle without refusing a running rekordbox

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u288.json`, row `M22_closed_at_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_rekordbox_running_at_the_write_refuses_before_any_session_opens`

Old text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
```

New text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=False, cfg=cfg)
```

### `u320.M20_retirable_without_this_reads_not_found`

retirable: offer a playlist for retirement on its record alone, whatever its id answered now

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u320.json`, row `M20_retirable_without_this_reads_not_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_retire_names_a_gone_playlist_whose_id_now_fails_another_way`
  - `tests/test_sync_removed_gone.py::test_retire_offers_no_playlist_seen_before_whose_id_now_fails_another_way_and_says_so`

Old text:

```
        if one.not_found and one.noted is not None and not one.noted.is_retired
```

New text:

```
        if one.noted is not None and not one.noted.is_retired
```

### `u320.M21_retire_records_before_the_gate`

retire: record the reads before the gate, so its abort writes

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u320.json`, row `M21_retire_records_before_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_retire_lists_each_playlist_behind_its_gate_and_its_abort_writes_nothing`

Old text:

```
    reads = _read_synced(cfg, found, every=True, record_now=False)
```

New text:

```
    reads = _read_synced(cfg, found, every=True, record_now=True)
```

### `u320.M22_retire_ignores_its_answer`

retire: retire whatever the gate was answered

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u320.json`, row `M22_retire_ignores_its_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_retire_lists_each_playlist_behind_its_gate_and_its_abort_writes_nothing`

Old text:

```
    if ctx.gate.require(_gate(ctx.entry, RETIRE_GATE), plan=data, context=context) != "retire":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=warnings)
```

New text:

```
    ctx.gate.require(_gate(ctx.entry, RETIRE_GATE), plan=data, context=context)
```

### `u320.M23_reads_never_recorded`

_read_synced: never write the record after the reads

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u320.json`, row `M23_reads_never_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 11 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a179s_shape_offers_the_track_once_the_gone_playlist_answers_not_found_a_day_apart`
  - `tests/test_sync_removed_gone.py::test_a_gone_downloaded_playlist_is_named_by_what_cratekit_calls_it`
  - `tests/test_sync_removed_gone.py::test_a_retired_downloaded_playlist_offers_none_of_its_tracks_and_holds_none_of_them`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_that_opens_again_is_read_again_and_the_retirement_cleared`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_the_account_lists_again_stops_every_offer_again`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_now_fails_another_way_stops_offers_this_run_and_stays_retired`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_opens_and_whose_rows_are_refused_is_cleared`
  - `tests/test_sync_removed_gone.py::test_a_sighting_on_a_later_date_but_under_a_day_after_the_first_retires_nothing`
  - `tests/test_sync_removed_gone.py::test_retire_offers_no_playlist_seen_before_whose_id_now_fails_another_way_and_says_so`
  - `tests/test_sync_removed_gone.py::test_retire_writes_every_reads_answer_with_the_retirement`
  - `tests/test_sync_removed_gone.py::test_the_control_taken_off_one_of_two_synced_playlists_is_kept_naming_the_other`

Old text:

```
    if record_now:
        record.update(removed.noted(reads))
```

New text:

```
    if False:
        record.update(removed.noted(reads))
```

### `u320.M24_record_read_as_empty`

_read_synced: plan over an empty record whatever it holds

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u320.json`, row `M24_record_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a179s_shape_offers_the_track_once_the_gone_playlist_answers_not_found_a_day_apart`
  - `tests/test_sync_removed_gone.py::test_a_retired_downloaded_playlist_offers_none_of_its_tracks_and_holds_none_of_them`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_that_opens_again_is_read_again_and_the_retirement_cleared`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_the_account_lists_again_stops_every_offer_again`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_now_fails_another_way_stops_offers_this_run_and_stays_retired`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_opens_and_whose_rows_are_refused_is_cleared`
  - `tests/test_sync_removed_gone.py::test_retire_answered_retire_records_the_playlist_and_the_next_run_offers_past_it`
  - `tests/test_sync_removed_gone.py::test_the_control_taken_off_one_of_two_synced_playlists_is_kept_naming_the_other`

Old text:

```
    sightings = record.read()
```

New text:

```
    sightings = record.read() and {}
```

### `u320.M25_person_retires_nothing`

retire: record the named playlists as sighted, never retired

- File: `src/cratekit/sync/removed_cli.py`
- Source: `u320.json`, row `M25_person_retires_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_retire_answered_retire_records_the_playlist_and_the_next_run_offers_past_it`
  - `tests/test_sync_removed_gone.py::test_retire_writes_every_reads_answer_with_the_retirement`
  - `tests/test_sync_removed_gone.py::test_the_retire_gate_binds_across_midnight`

Old text:

```
                one.account: unavailable.retired_by_person(one.noted, moment)
```

New text:

```
                one.account: one.noted
```

### `r704-a.R1_increment_ignores_the_flag`

the increment never takes the rate limited branch, every lookup failure is permanent as before R-704

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R1_increment_ignores_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
            if exc.rate_limited:
```

New text:

```
            if False:
```

### `r704-a.R2_rate_limit_not_retryable`

the rate limited refusal says resume and records the item permanent, so the job verdict and jobs.retry still refuse

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R2_rate_limit_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    retryable=True,
                    origin=("sync.run",),
```

New text:

```
                    retryable=False,
                    origin=("sync.run",),
```

### `r704-a.R3_remedy_retry_later`

the rate limited refusal names retry later rather than resuming the job

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R3_remedy_retry_later`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    remedy=Remedy.RESUME_JOB,
```

New text:

```
                    remedy=Remedy.RETRY_LATER,
```

### `r704-a.R4_detail_unmarked`

the refusal's detail no longer says rate limited, so a machine reader cannot tell it from an outage

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R4_detail_unmarked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    detail={"source_id": source.id, "rate_limited": True},
```

New text:

```
                    detail={"source_id": source.id},
```

### `r704-a.R5_flag_not_stored`

LookupFailure drops the flag it was handed

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R5_flag_not_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
        self.rate_limited = rate_limited
```

New text:

```
        self.rate_limited = False
```

### `r704-a.R6_sentence_reworded`

the refusal no longer says the provider rate limited the lookup

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R6_sentence_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    f"the provider rate limited a lookup {source.id} needed "
```

New text:

```
                    f"the provider throttled a lookup {source.id} needed "
```

### `u52-item-derivation.A1_acquires_early_return_gone`

R-140: an offering source writes the intake row, registers the artifact and moves the watermark over releases nobody accepted

- File: `src/cratekit/sync/run.py`
- Source: `u52-item-derivation.json`, row `A1_acquires_early_return_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`
- Collected: 211 against a baseline of 211
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_an_offering_run_leaves_the_source_watermark_unset`
  - `tests/test_incremental_sync.py::test_an_offering_source_writes_no_intake_file`
  - `tests/test_incremental_sync.py::test_one_run_records_only_the_acquiring_source_of_a_mixed_pair`

Old text:

```
        if not getattr(source, "acquires", True):
```

New text:

```
        if False:
```

### `u52-item-derivation.A2_acquires_default_false`

MUTATE THE COEFFICIENT: flip the getattr default, so every source written before the attribute existed stops recording what it acquired

- File: `src/cratekit/sync/run.py`
- Source: `u52-item-derivation.json`, row `A2_acquires_default_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`
- Collected: 211 against a baseline of 211
- Kills: 6 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_rerun_after_a_clean_sync_processes_only_unowned_items`
  - `tests/test_incremental_sync.py::test_a_watermark_does_not_empty_the_scope_of_unowned_items`
  - `tests/test_incremental_sync.py::test_an_acquiring_source_still_writes_the_intake_file_and_advances`
  - `tests/test_incremental_sync.py::test_one_run_records_only_the_acquiring_source_of_a_mixed_pair`
  - `tests/test_incremental_sync.py::test_one_source_failing_does_not_block_the_other`
  - `tests/test_incremental_sync.py::test_two_sources_in_one_run_share_one_importable_file`

Old text:

```
        if not getattr(source, "acquires", True):
```

New text:

```
        if not getattr(source, "acquires", False):
```

### `r259.S1_scope_owned_sample`

Existing guard sample: scope.scoped no longer drops owned identities

- File: `src/cratekit/sync/scope.py`
- Source: `r259.json`, row `S1_scope_owned_sample`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_rerun_after_a_clean_sync_processes_only_unowned_items`

Old text:

```
        if item.identity in owned:
```

New text:

```
        if False:
```

### `r263.S2_favorites_reason`

Favorites declares no reason, so its absent record reads as never again

- File: `src/cratekit/sync/sources.py`
- Source: `r263.json`, row `S2_favorites_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
        no_cursor="no favorites worker records a cursor, so a completed sync "
```

New text:

```
        no_cursor="" and "no favorites worker records a cursor, so a completed sync "
```

### `u109-b.B1_labels_not_guided`

Drop guided_by from the labels spec, so labels is an ordinary source with no worker

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B1_labels_not_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 228 against a baseline of 228
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
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
- Collected: 197 against a baseline of 197
- Kills: 9 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
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

### `u109-b.B3_no_cursor_reworded`

Reword the labels no_cursor sentence so it no longer names the guided verb

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B3_no_cursor_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_doctor_prints_the_labels_row_it_is_given`

Old text:

```
        no_cursor="label releases are taken by crate label sync, which keeps "
```

New text:

```
        no_cursor="label releases are taken by the guided verb, which keeps "
```

### `u74.A1_no_inbound_key`

The favourites spec declares no read half, so sync all never lists the hearts

- File: `src/cratekit/sync/sources.py`
- Source: `u74.json`, row `A1_no_inbound_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 26 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - ... and 11 more, see the JSON sidecar

Old text:

```
        inbound_key="intake.playlist",
```

New text:

```
        inbound_key=None,
```

### `u74.A2_wrong_inbound_key`

The read half is queued under intake.set, a key whose worker reads a tracklist, not a listing

- File: `src/cratekit/sync/sources.py`
- Source: `u74.json`, row `A2_wrong_inbound_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_only_favourites_declares_a_read_half_and_its_key_is_a_bound_intake_key`

Old text:

```
        inbound_key="intake.playlist",
```

New text:

```
        inbound_key="intake.set",
```

### `u242.M11_strip_skips_the_held_check`

strip: rename without confirming the record holds each planned playlist

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M11_strip_skips_the_held_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_no_rename_is_made_for_a_playlist_the_record_does_not_hold`

Old text:

```
    unheld = [identity for identity in planned if identity not in held]
```

New text:

```
    unheld = []
```

### `u242.M12_composite`

strip: neither record first nor confirm the hold, so a stripped playlist is in no record

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M12_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 11 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_ceiling_stop_names_what_landed_and_a_second_run_resumes`
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_a_stripped_playlist_named_like_a_followed_label_is_still_filed_by_its_mark`
  - `tests/test_u242_taken.py::test_every_old_title_is_restored_by_unmark_of_the_strip`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_no_rename_is_made_for_a_playlist_the_record_does_not_hold`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    taken_cli.migrate(cfg, listed)
    held = record.taken_ids()
    unheld = [identity for identity in planned if identity not in held]
```

New text:

```
    held = record.taken_ids()
    unheld = []
```

### `u242.M12_strip_skips_the_migration`

strip: rename without recording the prefixed playlists as taken first

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M12_strip_skips_the_migration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 14 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_ceiling_stop_names_what_landed_and_a_second_run_resumes`
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`
  - `tests/test_u242_taken.py::test_a_cratekit_marked_playlist_is_never_offered_once_stripped`
  - `tests/test_u242_taken.py::test_a_hand_prefixed_playlist_is_recorded_stripped_and_never_offered`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_a_stripped_playlist_named_like_a_followed_label_is_still_filed_by_its_mark`
  - `tests/test_u242_taken.py::test_a_title_changed_since_the_plan_is_not_renamed`
  - `tests/test_u242_taken.py::test_every_old_title_is_restored_by_unmark_of_the_strip`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_playlist_narrows_and_refuses_a_playlist_with_no_prefix`
  - `tests/test_u242_taken.py::test_the_strip_records_each_old_title_before_its_rename`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_is_put_back_renames_back`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`
  - `tests/test_u242_taken.py::test_unmark_of_the_migration_lets_nothing_go_and_nothing_is_offered`

Old text:

```
    taken_cli.migrate(cfg, listed)
    held = record.taken_ids()
```

New text:

```
    held = record.taken_ids()
```

### `u242.M13_strip_no_collision_with_others`

strip plan: never refuse a stripped title another playlist already carries

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M13_strip_no_collision_with_others`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`
  - `tests/test_u242_taken.py::test_the_gate_screen_lists_every_rename_and_every_refusal`

Old text:

```
        clash = others.get(to.casefold())
```

New text:

```
        clash = None
```

### `u242.M14_strip_no_collision_between_strips`

strip plan: never refuse two prefixed playlists stripped to one title

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M14_strip_no_collision_between_strips`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_collision_is_refused_and_named_and_the_rest_strip`

Old text:

```
        twins = sorted(prefixed[one] for one in writes[to.casefold()] if one != identity)
```

New text:

```
        twins = []
```

### `u242.M15_strip_collision_case_exact`

strip plan: compare titles case exactly, so Techno beside techno is renamed

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M15_strip_collision_case_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_the_gate_screen_lists_every_rename_and_every_refusal`

Old text:

```
            others.setdefault(name.strip().casefold(), name)
```

New text:

```
            others.setdefault(name.strip(), name)
```

### `u242.M17_strip_no_recheck`

strip apply: rename a playlist retitled since the plan was shown

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M17_strip_no_recheck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_title_changed_since_the_plan_is_not_renamed`

Old text:

```
            if now.get(identity) != item["name"]:
                changed.append(identity)
                continue
            # RECORDED BEFORE THE RENAME
```

New text:

```
            if False:
                changed.append(identity)
                continue
            # RECORDED BEFORE THE RENAME
```

### `u242.M18_strip_records_no_old_title`

strip apply: rename without recording the old title, so unmark cannot put it back

- File: `src/cratekit/sync/strip_cli.py`
- Source: `u242.json`, row `M18_strip_records_no_old_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_every_old_title_is_restored_by_unmark_of_the_strip`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_the_strip_records_each_old_title_before_its_rename`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_is_put_back_renames_back`

Old text:

```
            record.record_marked(PASS, {identity: (item["name"], item["to"])})
            remote.rename_playlist(identity, item["to"])
```

New text:

```
            remote.rename_playlist(identity, item["to"])
```

### `u242.M19_migration_copies_an_unmarked_mark`

migration: copy a mark sync unmark already put back

- File: `src/cratekit/sync/taken_cli.py`
- Source: `u242.json`, row `M19_migration_copies_an_unmarked_mark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_the_migration_records_every_prefix_and_standing_mark_once_and_says_how_many`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`

Old text:

```
        if mark.unmarked or not playlists.is_swept_name(mark.to):
```

New text:

```
        if not playlists.is_swept_name(mark.to):
```

### `u149.T10_any_year_folder`

candidates: read every root folder, not only one titled as a year

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T10_any_year_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_only_downloaded_own_playlists_in_a_year_folder_are_read`

Old text:

```
        if not YEAR.fullmatch(year):
            continue
```

New text:

```
        if False:
            continue
```

### `u149.T11_excluded_read`

candidates: drop the label, set and mirror exclusion

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T11_excluded_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_set_playlist_in_a_year_folder_gets_no_twin`

Old text:

```
            if name is None or playlist_id in kept or playlist_id in seen:
```

New text:

```
            if name is None or playlist_id in seen:
```

### `u149.T13_paired_planned_again`

plan_backfill: plan a twin for an already paired playlist, so a second run plans again

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T13_paired_planned_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_existing_folder_is_reused_and_two_of_one_year_place_nothing`

Old text:

```
    wanted = [one for one in listed if one[1] not in held]
```

New text:

```
    wanted = list(listed)
```

### `u149.T15_unplanned_membership`

addition_violations: admit a membership no twin planned

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T15_unplanned_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_confinement_refuses_what_no_twin_explains[changes4]`

Old text:

```
        if row[m_marker] or wanted is None or content_id not in wanted[2]:
```

New text:

```
        if row[m_marker] or wanted is None:
```

### `u149.T16_unplanned_playlist_row`

addition_violations: admit a playlist row no twin made

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T16_unplanned_playlist_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_confinement_refuses_an_unplanned_playlist_read_from_sql`
  - `tests/test_sync_twins.py::test_the_confinement_refuses_what_no_twin_explains[changes0]`

Old text:

```
    for key in sorted(set(after.playlists) - set(before.playlists) - set(made)):
```

New text:

```
    for key in sorted(set()):
```

### `u149.T20_short_snapshot`

pair_backfilled: record the account snapshot when the listing was short

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T20_short_snapshot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_short_listing_pairs_the_twin_with_no_snapshot`

Old text:

```
            account=list(one.account) if one.whole else None,
```

New text:

```
            account=list(one.account),
```

### `u149.T21_landing_paired_again`

plan_landing: plan a twin for an account playlist already paired

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T21_landing_paired_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_twins.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_an_account_playlist_already_paired_gets_no_second_twin`

Old text:

```
    wanted = [(account_id, name) for account_id, name in accounts if account_id not in held]
```

New text:

```
    wanted = list(accounts)
```

### `u149.T2_two_folders_not_refused`

find_folder: drop the refusal of two live top level folders of one year, so the first is written to

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T2_two_folders_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_existing_folder_is_reused_and_two_of_one_year_place_nothing`

Old text:

```
    if len(found) > 1:
```

New text:

```
    if len(found) > 2:
```

### `u149.T3_folder_names_unread`

find_folder: read no names inside a live folder, so a held name is not seen

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T3_folder_names_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_a_twin_name_the_folder_holds_is_left_and_named_and_the_landing_still_lands`
  - `tests/test_sync_twins.py::test_a_name_the_folder_already_holds_is_refused_by_name_never_counted`

Old text:

```
held=_live_children(db, found[0]))
```

New text:

```
held=frozenset())
```

### `u149.T4_removed_folder_live`

_live_top_folders: drop the soft delete filter, so a removed folder is reused

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T4_removed_folder_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_removed_year_folder_is_not_reused_and_a_live_one_is_made`

Old text:

```
        f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0 ORDER BY ID"
```

New text:

```
        f"ORDER BY ID"
```

### `u149.T5_held_name_counted_free`

place: drop the refusal of a name the folder holds, so a second twin of one name is made

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T5_held_name_counted_free`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_a_twin_name_the_folder_holds_is_left_and_named_and_the_landing_still_lands`
  - `tests/test_sync_twins.py::test_a_name_the_folder_already_holds_is_refused_by_name_never_counted`
  - `tests/test_sync_twins.py::test_place_refuses_a_held_name_a_taken_name_an_empty_name_and_an_unplaced_year`

Old text:

```
    if name in folder.held:
```

New text:

```
    if False:
```

### `u149.T6_taken_name_free`

place: drop the refusal of a name this run already gave, so two twins share one name

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T6_taken_name_free`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_place_refuses_a_held_name_a_taken_name_an_empty_name_and_an_unplaced_year`

Old text:

```
    if name in taken:
```

New text:

```
    if False:
```

### `u149.T7_ambiguous_takes_first`

matched: take the first of several library rows, so an ambiguous track is guessed

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T7_ambiguous_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_account_track_two_library_rows_carry_is_named_and_neither_is_guessed`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
        if len(found) == 1:
```

New text:

```
        if found:
```

### `u149.T8_mirror_link_skipped`

Library.find: skip the mirror's link to the very track, so the database ISRC decides

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T8_mirror_link_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_mirrors_link_to_a_track_wins_and_a_link_to_a_removed_row_falls_through`

Old text:

```
            self.by_remote.get(remote_id, ()),
```

New text:

```
            (),
```

### `u149.T9_removed_row_linked`

_grouped: drop the live filter, so a mirror link to a removed row is an answer

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T9_removed_row_linked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_the_mirrors_link_to_a_track_wins_and_a_link_to_a_removed_row_falls_through`

Old text:

```
        if key and content_id in alive and content_id not in found.setdefault(key, []):
```

New text:

```
        if key and content_id not in found.setdefault(key, []):
```

### `u213.M14_backfill_reason_check`

plan_backfill: leave a playlist for any refusal, so an expired session leaves every playlist instead of naming its act

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M14_backfill_reason_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_refusal_that_is_not_about_one_playlist_still_stops_the_run`

Old text:

```
            if exc.cause.reason not in PER_PLAYLIST_REASONS:
                raise
            twins.append(
```

New text:

```
            if False:
                raise
            twins.append(
```

### `u213.M15_backfill_left_action`

plan_backfill: plan a playlist whose listing was refused as a twin to make, with no rows

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M15_backfill_left_action`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`
  - `tests/test_sync_twins.py::test_a_playlist_the_provider_cannot_list_is_left_named_and_the_other_is_made`
  - `tests/test_sync_twins.py::test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned`
  - `tests/test_sync_twins.py::test_every_playlist_left_writes_nothing_and_opens_no_gate`

Old text:

```
                    action=LEFT,
                    why=f"the account playlist could not be read: {exc.cause.message}",
```

New text:

```
                    action=CREATE,
                    why=f"the account playlist could not be read: {exc.cause.message}",
```

### `u213.M16_backfill_digest_reason`

Twin.identity: put the provider's words in the digest again, so a varying message makes the approved run stale

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M16_backfill_digest_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`

Old text:

```
            "why": self.refused or self.why,
```

New text:

```
            "why": self.why,
```

### `u213.M17_backfill_unread_tracks`

plan_backfill: plan from the read tracks alone, so an unread track is in neither the twin's misses nor its snapshot

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M17_backfill_unread_tracks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
            ref: listing.tracks[ref] if ref in listing.tracks else listing.unread[ref].said()
            for ref in listing.order
```

New text:

```
            ref: listing.tracks[ref]
            for ref in listing.order
            if ref in listing.tracks
```

### `u213.M18_backfill_unread_reasons`

plan_backfill: hand matched no unread reasons, so an unread track the library lacks reads as merely not owned

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M18_backfill_unread_reasons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`

Old text:

```
            {ref: one.why for ref, one in listing.unread.items()},
```

New text:

```
            {},
```

### `u213.M19_matched_ambiguous_first`

matched: say an unread track two rows carry is unreadable rather than ambiguous

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M19_matched_ambiguous_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
                    AMBIGUOUS
                    if found
                    else f"{unread[remote_id]}, {UNREAD_NOT_FOUND}"
                    if remote_id in unread
                    else NOT_OWNED
```

New text:

```
                    f"{unread[remote_id]}, {UNREAD_NOT_FOUND}"
                    if remote_id in unread
                    else AMBIGUOUS
                    if found
                    else NOT_OWNED
```

### `u213.M20_backfill_whole`

plan_backfill: read every listing as whole, so a short one is paired with a snapshot it does not have

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M20_backfill_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_short_listing_pairs_the_twin_with_no_snapshot`

Old text:

```
                whole=listing.short is None,
```

New text:

```
                whole=True,
```

### `u213.M2_backfill_refused_reason`

plan_backfill: record no refusal reason on a left playlist, so its digest carries the provider's words

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M2_backfill_refused_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`

Old text:

```
                    refused=exc.cause.reason,
```

New text:

```
                    refused="",
```

### `u221.R19_short_listing_records_its_misses`

pair_backfilled: record a short listing's misses as its hold, so a track the account withheld and serves later is queued with no choice

- File: `src/cratekit/sync/twins.py`
- Source: `u221.json`, row `R19_short_listing_records_its_misses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_short_listings_twin_records_no_hold_and_holds_a_track_served_later`

Old text:

```
                {miss.remote_id: miss.held_as() for miss in one.misses} if one.whole else None
```

New text:

```
                {miss.remote_id: miss.held_as() for miss in one.misses}
```

### `u221.R20_landing_records_no_hold`

pair_landed: mark a landing's twin with no hold, so it is read by time and its misses are held

- File: `src/cratekit/sync/twins.py`
- Source: `u221.json`, row `R20_landing_records_no_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_intake_land_twins.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`

Old text:

```
                one.account_id, one.playlist_id, name=one.account_name, twin=True, on_hold={}
```

New text:

```
                one.account_id, one.playlist_id, name=one.account_name, twin=True, on_hold=None
```

### `u242.M8_twins_reads_the_title_alone`

twins backfill: read a downloaded custom playlist by its prefix alone, so a stripped one gets no twin

- File: `src/cratekit/sync/twins.py`
- Source: `u242.json`, row `M8_twins_reads_the_title_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_twins.py`
- Collected: 92 against a baseline of 92
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_twins_reads_a_stripped_custom_playlist_as_downloaded`

Old text:

```
            if not is_taken(playlist_id, name, held):
```

New text:

```
            if not name.startswith("DOWNLOADED "):
```

### `u320.M11_apart_halved`

APART: retire twelve hours after the first sighting rather than a day

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M11_apart_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_sighting_retires_only_a_day_after_the_first_and_a_retirement_stands`

Old text:

```
APART = timedelta(hours=24)
```

New text:

```
APART = timedelta(hours=12)
```

### `u320.M12_apart_strict`

sighted: retire only past a day, not at a day

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M12_apart_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_sighting_retires_only_a_day_after_the_first_and_a_retirement_stands`

Old text:

```
    if latest - datetime.fromisoformat(held.first) >= APART:
```

New text:

```
    if latest - datetime.fromisoformat(held.first) > APART:
```

### `u320.M14_any_status_is_not_found`

answered_unavailable: read any status as a not found

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M14_any_status_is_not_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_not_found_met_only_while_handling_another_failure_is_not_one`
  - `tests/test_sync_removed_gone.py::test_a_playlist_that_failed_any_other_way_twice_a_day_apart_is_never_retired`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_now_fails_another_way_stops_offers_this_run_and_stays_retired`
  - `tests/test_sync_removed_gone.py::test_only_a_not_found_answer_is_read_as_unavailable`
  - `tests/test_sync_removed_gone.py::test_retire_names_a_gone_playlist_whose_id_now_fails_another_way`
  - `tests/test_sync_removed_gone.py::test_retire_offers_no_playlist_seen_before_whose_id_now_fails_another_way_and_says_so`
  - `tests/test_sync_removed_gone.py::test_retire_offers_no_playlist_whose_id_failed_any_other_way`
  - `tests/test_sync_removed_gone.py::test_the_real_adapter_reads_a_404_as_unavailable_and_a_server_error_not`

Old text:

```
            return answered_not_found(link)
```

New text:

```
            return True
```

### `u320.M15_context_class_counts`

answered_unavailable: read the not found class off a link met only while handling another failure

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M15_context_class_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_not_found_met_only_while_handling_another_failure_is_not_one`

Old text:

```
        if declared and type(link).__name__ == CLIENT_NOT_FOUND:
```

New text:

```
        if type(link).__name__ == CLIENT_NOT_FOUND:
```

### `u320.M16_damaged_record_reads_empty`

UnavailableRecord.read: read a record that is not JSON as holding nothing

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M16_damaged_record_reads_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_an_unreadable_record_refuses_before_the_account_is_asked`

Old text:

```
            # Not UTF-8 is a ``ValueError`` too, and as unreadable.
            raise self._unusable("it is not JSON") from exc
```

New text:

```
            return {}
```

### `u320.M17_other_library_read`

UnavailableRecord: read a record written for another library

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M17_other_library_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_damaged_record_refuses_and_is_never_read_as_empty[library]`

Old text:

```
        if raw.get("library_id") != self.cfg.library.volume_id:
```

New text:

```
        if False:
```

### `u320.M19_none_drops_nothing`

UnavailableRecord._apply: a change of None drops nothing, so a reopened playlist stays retired

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M19_none_drops_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_that_opens_again_is_read_again_and_the_retirement_cleared`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_the_account_lists_again_stops_every_offer_again`
  - `tests/test_sync_removed_gone.py::test_a_retired_playlist_whose_id_opens_and_whose_rows_are_refused_is_cleared`
  - `tests/test_sync_removed_gone.py::test_retire_writes_every_reads_answer_with_the_retirement`
  - `tests/test_sync_removed_gone.py::test_the_record_reads_back_what_it_wrote_and_drops_an_entry_given_none`

Old text:

```
        after = {key: value for key, value in entries.items() if key not in changes}
```

New text:

```
        after = dict(entries)
```

### `u320.M3_any_not_found_name_counts`

answered_unavailable: read any class whose name holds not found, Python's FileNotFoundError included, round one's BLOCKING finding

- File: `src/cratekit/sync/unavailable.py`
- Source: `u320.json`, row `M3_any_not_found_name_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_removed_gone.py`, `tests/test_sync_removed.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_removed_gone.py::test_pythons_own_not_found_classes_are_no_sighting_and_never_retire[file-not-found]`
  - `tests/test_sync_removed_gone.py::test_pythons_own_not_found_classes_are_no_sighting_and_never_retire[module-not-found]`

Old text:

```
        if declared and type(link).__name__ == CLIENT_NOT_FOUND:
```

New text:

```
        if declared and "notfound" in type(link).__name__.lower():
```

### `r838-a.U1_refuse_stranger`

unmark._narrowed: drop the refusal, so a playlist the pass never marked is silently passed over rather than refused

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U1_refuse_stranger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_the_pass_never_marked_is_refused_whatever_its_title`

Old text:

```
    if strangers:
        raise _blocked(
```

New text:

```
    if False:
        raise _blocked(
```

### `r838-a.U3_pass_filter`

unmark: take every pass's marks as the named pass's, so a playlist the pass never marked is planned

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U3_pass_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`
  - `tests/test_sync_unmark.py::test_a_pass_the_record_holds_nothing_for_is_a_gated_plan_of_nothing`

Old text:

```
        tuple(entry for entry in every if entry.pass_name == name),
```

New text:

```
        tuple(entry for entry in every),
```

### `r838-a.U4_already_unmarked_stamp`

unmark._item: ignore the unmarked stamp, so a second run is decided by the title alone

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U4_already_unmarked_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_second_run_plans_nothing_and_still_asks`

Old text:

```
    if entry.unmarked:
        return {
```

New text:

```
    if False:
        return {
```

### `r838-a.U5_marked_again`

unmark._item: ignore a later mark by another pass, so this pass's unmark takes off that pass's prefix

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U5_marked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`

Old text:

```
    later = _later(entry, every)
    if later:
```

New text:

```
    later = _later(entry, every)
    if False:
```

### `r838-a.U6_later_order`

unmark._later: an EARLIER mark by another pass also supersedes, so the latest pass's own unmark is refused

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U6_later_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`

Old text:

```
        and other.marked > entry.marked
```

New text:

```
        and other.marked != entry.marked
```

### `r838-a.U8_title_already_back`

unmark._item: no already-put-back branch, so a title already restored is reported as retitled by hand

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U8_title_already_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_title_already_put_back_is_skipped_without_a_stamp`

Old text:

```
    if current == entry.name:
```

New text:

```
    if False:
```

### `r838-b.U10_digest_names`

unmark._payload: the digest omits the planned renames, so an answer to one plan carries out another

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U10_digest_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_an_answer_is_stale_once_the_account_moves`

Old text:

```
            (item["id"], item["marked_as"], item["to"])
            for item in items
            if item["action"] == UNMARK
```

New text:

```
            (item["id"], item["marked_as"], item["to"])
            for item in items
            if False
```

### `r838-b.U13_recheck`

unmark: no recheck against the second listing, so a title changed after the answer is renamed anyway

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U13_recheck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_that_changes_between_the_plan_and_the_rename_is_said`

Old text:

```
            if now.get(identity) != entry.to:
```

New text:

```
            if False:
```

### `r838-b.U15_rename_target`

unmark: rename to the title the mark wrote rather than the one before it

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U15_rename_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`
  - `tests/test_sync_unmark.py::test_a_pass_that_marked_three_plans_three_renames_back_and_applies_them`
  - `tests/test_sync_unmark.py::test_a_playlist_retitled_by_hand_since_the_mark_is_listed_and_left`
  - `tests/test_sync_unmark.py::test_a_playlist_that_changes_between_the_plan_and_the_rename_is_said`
  - `tests/test_sync_unmark.py::test_a_playlist_the_account_no_longer_lists_is_said_and_left`
  - `tests/test_sync_unmark.py::test_a_title_already_put_back_is_skipped_without_a_stamp`
  - `tests/test_sync_unmark.py::test_playlist_given_twice_narrows_to_both_marks_named`
  - `tests/test_sync_unmark.py::test_playlist_narrows_to_the_marks_named`

Old text:

```
            remote.rename_playlist(identity, entry.name)
```

New text:

```
            remote.rename_playlist(identity, entry.to)
```

### `r838-b.U16_part_way_names`

unmark._failed_part_way: report nothing put back, so a partial failure loses what landed

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U16_part_way_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_failure_part_way_names_what_was_put_back`

Old text:

```
        "unmarked": list(landed),
```

New text:

```
        "unmarked": [],
```

### `r838-b.U9_renamed_since`

unmark._item: plan any title carrying the prefix, so a playlist retitled by hand with the prefix kept is renamed

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U9_renamed_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_retitled_by_hand_since_the_mark_is_listed_and_left`

Old text:

```
    if current != entry.to:
        how =
```

New text:

```
    if not playlists.is_swept_name(current):
        how =
```

### `r838-c.U7b_not_listed_rerun`

U7 measured again after the not-listed test was added: no NOT_LISTED branch, so a playlist the account dropped falls through to the title comparison

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-c.json`, row `U7b_not_listed_rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_the_account_no_longer_lists_is_said_and_left`

Old text:

```
    if current is None:
        return {
            **base,
            "action": SKIP,
            "reason": NOT_LISTED,
```

New text:

```
    if current is None and False:
        return {
            **base,
            "action": SKIP,
            "reason": NOT_LISTED,
```

### `u242.M22_unmark_releases_nothing`

sync unmark: never plan a release, so a pass's taken playlists cannot be let go

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u242.json`, row `M22_unmark_releases_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_unmark.py`, `tests/test_label_playlists.py`, `tests/test_export_set.py`
- Collected: 190 against a baseline of 190
- Kills: 7 (killed)
- Killed:
  - `tests/test_export_set.py::test_sync_unmark_takes_the_archive_mark_off_again`
  - `tests/test_label_playlists.py::test_sync_unmark_takes_the_label_mark_off_again`
  - `tests/test_u242_taken.py::test_a_release_that_fails_part_way_names_what_was_let_go`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_unmark_lets_go_a_pass_mark_with_no_write_to_the_account`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`
  - `tests/test_u242_taken.py::test_unmark_playlist_narrows_the_releases`

Old text:

```
    taken_held = held is not None and held.held
```

New text:

```
    taken_held = False
```

### `u242.M26_release_stamps_no_mark`

sync unmark: a release leaves the pass's legacy mark unstamped, so the next migration or strip takes it again

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u242.json`, row `M26_release_stamps_no_mark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_sync_unmark.py`
- Collected: 78 against a baseline of 78
- Kills: 3 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_a_release_that_fails_part_way_names_what_was_let_go`
  - `tests/test_u242_taken.py::test_a_release_whose_title_was_retitled_since_stamps_the_pass_mark`
  - `tests/test_u242_taken.py::test_unmark_of_a_legacy_pass_after_the_strip_releases_and_stamps_it`

Old text:

```
            if identity in by_id and not by_id[identity].unmarked:
                record.record_unmarked(name, identity)
```

New text:

```
            if False:
                record.record_unmarked(name, identity)
```

### `u246.S14_unmark_narrowed_empty`

unmark: an empty narrowed set, so --playlist narrows every mark away and the verb puts nothing back

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u246.json`, row `S14_unmark_narrowed_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`, `tests/test_gate_shown_plan.py`
- Collected: 47 against a baseline of 47
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_playlist_given_twice_narrows_to_both_marks_named`
  - `tests/test_sync_unmark.py::test_playlist_narrows_to_the_marks_named`
  - `tests/test_sync_unmark.py::test_the_mark_screen_says_a_playlist_was_put_back`

Old text:

```
    narrowed = set(named)
```

New text:

```
    narrowed = set()
```

### `u246.S15_unmark_narrowed_first_only`

unmark: narrow to the first playlist named alone, so a second --playlist is dropped

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `u246.json`, row `S15_unmark_narrowed_first_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`, `tests/test_gate_shown_plan.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_playlist_given_twice_narrows_to_both_marks_named`

Old text:

```
    narrowed = set(named)
```

New text:

```
    narrowed = set(named[:1])
```

### `r263.W1_no_unrecorded_state`

status_rows ignores the declared no_cursor reason, so every absent record reads as never

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W1_no_unrecorded_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 4 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_doctor_prints_the_labels_row_it_is_given`
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
        reason = no_cursor.get(source_id)
```

New text:

```
        reason = None
```

### `r263.W2_state_word`

A cursorless source is reported with state never, detail unchanged

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W2_state_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
"state": "unrecorded"
```

New text:

```
"state": "never"
```

### `r263.W3_stale_record_as_completion`

A stale record on a cursorless source is reported as its last completion again

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W3_stale_record_as_completion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`

Old text:

```
        if reason is not None:
```

New text:

```
        if reason is not None and mark is None:
```

### `r263.W4_stale_suffix`

Drop the note that an earlier build's cursor no longer moves

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W4_stale_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`

Old text:

```
            if mark is not None:
                detail += (
```

New text:

```
            if False:
                detail += (
```

