# Mutation table: u312-replay-before-7

Measured by `scripts/mutate.py` on 2026-11-23 10:19 UTC, branch `HEAD` at `bece470e`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22479 collected. pytest invocations for this batch: 217.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `269cecd96b22`, and this tree is at `bece470ea56f`).

Subset baselines: 30, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22479 against 22479. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u227.R25_way_on_state` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `r1499.S01_download_reading` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 12 | killed |
| `r1499.S02_tail_reading` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.S03_arrival_after_tail` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 2 | killed |
| `r1499.S04_arrival_after_plan` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.S05_keep_after_arrival` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 2 | killed |
| `r1499.S06_keep_called` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 7 | killed |
| `r1499.S07_kept_read` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 4 | killed |
| `r1499.S08_own_pass_proof` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 2 | killed |
| `r1499.S10_own_by_list` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 66 | killed |
| `r1499.S11_unreadable_refuses` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.S12_warnings_in_refusal` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.S13_own_unnamed_step` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.B03_pass_step` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 6 | killed |
| `r1499.B04_pass_maybe_renamed` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.B05_arrived_items` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 4 | killed |
| `r1499.B06_arrived_count` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.B08_kept_identity` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 5 | killed |
| `r1499.B10_plain_step_moves_out` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 325 | 2 | killed |
| `u227.R16_join_state` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 130 | 5 | killed |
| `u227.R17_join_held` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 130 | 1 | killed |
| `u227.R18_join_blank` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 130 | 1 | killed |
| `u82-b.B5_not_listed_is_skipped` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-b.B6_a_failed_job_is_skipped` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 2 | killed |
| `u82-b.B7_unread_reports_hold_the_playlist` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 2 | killed |
| `u82-b.B8_an_offered_track_is_owed` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-c.C1_a_tombstoned_track_is_settled` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-c.C2_one_outstanding_track_holds_the_playlist` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 9 | killed |
| `u82-c.C3_landed_is_told_from_owned` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 2 | killed |
| `u82-c.C9_the_accounts_reason_is_kept` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u82-d.B2_paths_compared_resolved_again` | `src/cratekit/sync/mark_cli.py` | user | 1 file(s) | 69 | 1 | killed |
| `u174.O1_native_loop` | `src/cratekit/organize/account.py` | user | 2 file(s) | 166 | 4 | killed |
| `u174.O2_seen_skips_a_filed_pass` | `src/cratekit/organize/account.py` | user | 2 file(s) | 166 | 1 | killed |
| `u174.O6_native_refusal_is_a_step` | `src/cratekit/organize/account.py` | user | 2 file(s) | 166 | 2 | killed |
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
| `u82-a.A1_stat_oserror_is_the_refusal` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 184 | 4 | killed |
| `u82-a.A3_an_empty_file_is_not_proof` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 184 | 2 | killed |
| `u82-a.A5_only_narrows` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 184 | 9 | killed |
| `u82-a.A6_an_empty_only_is_nothing` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 184 | 1 | killed |
| `u82-a.A7_mark_swept_hands_only_through` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 184 | 8 | killed |
| `u242.M21_mark_cli_already_marked_by_title` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 115 | 1 | killed |
| `u293.N1_no_answer` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1069 | 4 | killed |
| `u293.N2_rekordbox_refused` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1069 | 3 | killed |
| `u293.N4_occupied_refused` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1069 | 4 | killed |
| `u293.N5_owed_kept` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1069 | 3 | killed |
| `u293.N6_settled_by_landing` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1069 | 1 | killed |
| `u293.S3_sync_land_holds` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 144 | 1 | killed |
| `u130-b.B7_set_playlist_in_scope` | `src/cratekit/sync/pair_model.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B8_tree_name_in_scope` | `src/cratekit/sync/pair_model.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B1_short_base_unnarrowed` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B4_no_isrc_still_asked` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B5_readd_old_rule` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B6_requeue` | `src/cratekit/sync/pair_plan.py` | user | 1 file(s) | 76 | 3 | killed |
| `r1383.M12_unlisted_said_as_records` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 1 | killed |
| `r1383.M13_records_unnamed` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 2 | killed |
| `r1383.M16_zero_said_as_count` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-b.B9_stale_pair_blocks_all` | `src/cratekit/sync/pair_screen.py` | user | 1 file(s) | 76 | 1 | killed |
| `u130-c.C1_half_written_snapshot` | `src/cratekit/sync/pair_write.py` | user | 1 file(s) | 76 | 6 | killed |
| `u130-c.C9_sweep_takes_paired` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 76 | 2 | killed |
| `u130-c.C5_no_renumber` | `src/cratekit/write/playlist_pair.py` | user | 1 file(s) | 76 | 3 | killed |
| `u216.M21_reserve_adopt_empty` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 385 | 9 | killed |
| `u216.M22_write_drops_held` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 385 | 12 | killed |
| `u216.M23_read_drops_held` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 385 | 12 | killed |
| `u216.M11_paired_raw` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 6 | killed |
| `u216.M1_held_record_ignored` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 7 | killed |
| `u216.M2_created_folder_by_time` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 2 | killed |
| `u216.M4_no_time_reads_new` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 3 | killed |
| `u216.M5_naive_time_trusted` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 2 | killed |
| `u216.M7_time_rule_off` | `src/cratekit/sync/pair_discover.py` | user | 12 file(s) | 385 | 3 | killed |
| `u216-m14.M14_moment_any_folder` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 1 | killed |
| `u216.M13_unrecorded_off` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 3 | killed |
| `u216.M15_before_rule_off` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 10 | killed |
| `u216.M16_copy_rule_off` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 5 | killed |
| `u216.M18_copy_all_titles` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 2 | killed |
| `u216.M19_place_held_empty` | `src/cratekit/sync/pair_screen.py` | user | 12 file(s) | 385 | 7 | killed |
| `u216.M20_made_drops_held` | `src/cratekit/sync/pair_write.py` | user | 12 file(s) | 385 | 9 | killed |
| `r1264.M22_readable_dates` | `src/cratekit/intake/cli.py` | user | 4 file(s) | 183 | 6 | killed |
| `u234.S2_sample_stopped_leader` | `src/cratekit/sync/pair_merge.py` | user | 6 file(s) | 313 | 3 | killed |
| `r1404.M2_rekordbox_move_ignored` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 3 | killed |
| `r1404.M3_account_move_not_guarded` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 4 | killed |
| `r1404.S1_default_leader` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 16 | killed |
| `r1416.S2_placed_after_neighbour` | `src/cratekit/sync/pair_merge.py` | user | 5 file(s) | 225 | 22 | killed |
| `r1385.M12_check_reads_no_job` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 292 | 2 | killed |
| `r1385.M10_reason_dropped` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 7 | killed |
| `r1385.M2_other_jobs_not_asked` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 6 | killed |
| `r1385.M4_plan_not_asked` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 3 | killed |
| `r1385.M6_ask_not_registered` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 3 | killed |
| `r1385.M8_own_reads_every_job` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 6 | killed |
| `r1385.M9_own_reads_no_job` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 8 | killed |
| `u229.M15_wide_landed_needs_rest` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.M1_wide_landed_step` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 7 | killed |
| `u229.M3_wide_jobs_step` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.M4_wide_jobs_own_only` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.M5_wide_jobs_strict` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.M8_own_landing_first` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.S1_ambiguous_count` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 2 | killed |
| `u229.S2_own_landed_step` | `src/cratekit/sync/pair_plan.py` | user | 8 file(s) | 292 | 1 | killed |
| `r1385.M11_name_fallback` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 1 | killed |
| `r1385.M15_failed_jobs_hold` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 2 | killed |
| `r1385.M1_no_job_holds_anything` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 13 | killed |
| `u229.M10_file_isrc_fallback` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 10 | killed |
| `u229.M11_mirror_cache` | `src/cratekit/sync/pair_read.py` | maintainer | 8 file(s) | 292 | 1 | killed |
| `u229.M12_own_mirrors_bypass_cache` | `src/cratekit/sync/pair_read.py` | maintainer | 8 file(s) | 292 | 1 | killed |
| `u229.M2_wide_landed_reads_own_only` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.M6_config_error_not_caught` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 1 | killed |
| `u229.M9_landed_dedup` | `src/cratekit/sync/pair_read.py` | user | 8 file(s) | 292 | 1 | killed |
| `r1385.M13_warning_unsplit` | `src/cratekit/sync/pair_screen.py` | user | 8 file(s) | 292 | 1 | killed |
| `r1385.M14_warning_here_dropped` | `src/cratekit/sync/pair_screen.py` | user | 8 file(s) | 292 | 2 | killed |
| `u304.S1_file_code_read_through_its_module` | `src/cratekit/sync/pair_plan.py` | user | 2 file(s) | 97 | 5 | killed |
| `u304.S2_file_code_for_an_agreement` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 117 | 2 | killed |
| `u246.S11_pair_cli_served_empty` | `src/cratekit/sync/pair_plan.py` | user | 4 file(s) | 132 | 1 | killed |
| `r1383.M17_total_uncounted` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 108 | 2 | killed |
| `r1383.M7_gate_item_side` | `src/cratekit/sync/pair_screen.py` | user | 2 file(s) | 108 | 2 | killed |
| `r1383.M14_hold_before_awaiting` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 2 | killed |
| `r1383.M18_sampled_own_landed_step` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 1 | killed |
| `r1383.M2_hold_branch_removed` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 4 | killed |
| `r1383.M3_hold_without_isrc` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 1 | killed |
| `r1383.M4_hold_while_readable` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 27 | killed |
| `r1383.M5_hold_dropped_from_plan` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 137 | 2 | killed |
| `r1383.M19_sampled_mirrors_empty` | `src/cratekit/sync/pair_read.py` | user | 3 file(s) | 137 | 11 | killed |
| `r1383.M10_warning_never_said` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 137 | 5 | killed |
| `r1383.M6_gate_item_dropped` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 137 | 2 | killed |
| `r1383.M1_scan_drops_unread` | `src/cratekit/sync/pair_read.py` | user | 4 file(s) | 183 | 5 | killed |
| `u209.H7_hold_equality_unchecked` | `src/cratekit/core/held_plan.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `u202-composites.R2_confined` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202.R1_recheck_name` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202.W1_landed_then_raised` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202-composites.C3_composite` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 160 | 3 | killed |
| `u202.C1_after_synced` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 160 | 1 | killed |
| `u202-composites.C10_reads_account` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 160 | 1 | killed |
| `u202-composites.C8_scope` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 160 | 1 | killed |
| `u202.C5_released` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 160 | 2 | killed |
| `u202.C7_twice` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 160 | 1 | killed |
| `u202.C4_dates_recorded` | `src/cratekit/sync/pair_write.py` | user | 3 file(s) | 160 | 6 | killed |
| `u202.D1_skip` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D2_two_tops` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D3_longest` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D5_name_taken` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202.D6_favourites` | `src/cratekit/sync/pair_discover.py` | user | 2 file(s) | 84 | 1 | killed |
| `u202-composites.P1_reserve_held` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 160 | 1 | killed |
| `u207.P1_pair_screens_remembered_miss` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 154 | 1 | killed |
| `u207.P2_pair_never_screens` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 154 | 2 | killed |
| `u198.P2_release_side` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 168 | 3 | killed |
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
| `u198.C1_miss_reuse` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 168 | 2 | killed |
| `u198.C2_miss_isrc` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C3_unread_remembered` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C4_tie_remembered` | `src/cratekit/sync/pair_plan.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C10_unpair_account_gone` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C11_unpair_rekordbox_gone` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 2 | killed |
| `u198.C12_archive_move` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 3 | killed |
| `u198.C5_folder_twice` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C6_folder_others` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C7_title_taken` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C8_folder_gone` | `src/cratekit/sync/pair_screen.py` | user | 3 file(s) | 168 | 1 | killed |
| `u198.C9_account_only` | `src/cratekit/sync/pair_write.py` | user | 3 file(s) | 168 | 1 | killed |
| `u304-b.S15_favourites_home_judged_without_the_foreign_check` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 114 | 1 | killed |
| `u304-b.S7_walk_keeps_removed_nodes` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 114 | 1 | killed |
| `u304.S8_walk_root_sentinel` | `src/cratekit/sync/pair_discover.py` | user | 3 file(s) | 114 | 87 | killed |
| `u209.H6_load_age_unchecked` | `src/cratekit/core/held_plan.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C10_reverse_recheck` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 2 | killed |
| `u209.C11_home_of` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C12_brought_folder` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C13_jobs_queued` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 2 | killed |

## Zero rows and what they owe

- `u209.H7_hold_equality_unchecked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u227.R25_way_on_state`

_way_on: name a blocked mirror download as the next pass's, which takes queued jobs only (round two's R3)

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R25_way_on_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_mirror_download_a_pass_cannot_take_keeps_the_command_that_settles_it`

Old text:

```
    elif _mirror_download(job) and job.state is jobs.JobState.QUEUED:
```

New text:

```
    elif _mirror_download(job):
```

### `r1499.S01_download_reading`

sync land: the reading before the download never refuses, so a pass downloads beside a go's download at its gate

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S01_download_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_file_the_passes_tail_left_and_then_changed_is_not_its_own`
  - `tests/test_sync_land_beside.py::test_a_label_gos_download_at_its_landings_gate_renamed_refuses_the_pass_before_it_downloads`
  - `tests/test_sync_land_beside.py::test_a_pass_whose_landing_is_proven_is_not_named`
  - `tests/test_sync_land_beside.py::test_a_plain_download_beside_the_pass_refuses_naming_it`
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`
  - `tests/test_sync_land_beside.py::test_an_earlier_pass_renamed_at_its_gate_is_named_by_its_pass`
  - `tests/test_sync_land_beside.py::test_an_earlier_passes_unlanded_download_refuses_a_new_pass_naming_how_it_lands`
  - `tests/test_sync_land_beside.py::test_once_the_passes_landing_is_proven_its_record_reads_nothing_as_its_own`
  - `tests/test_sync_land_staged.py::test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_an_unlanded_first_refuses_before_any_download_is_refused`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses`

Old text:

```
    if not found:
        return settled

```

New text:

```
    if not found or step == DOWNLOAD:
        return settled

```

### `r1499.S02_tail_reading`

sync land: the reading before the tail never refuses, so a download finished during the pass's download is tailed and landed with it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S02_tail_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_gos_download_arriving_while_the_pass_downloads_refuses_its_tail`

Old text:

```
    if not found:
        return settled

```

New text:

```
    if not found or step == TAG:
        return settled

```

### `r1499.S03_arrival_after_tail`

sync land: no check after name apply, so a download finished during the tail is renamed and planned into the landing

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S03_arrival_after_tail`
- Moved: Anchored where u303-replay-after-c.json replayed it: U303 shortened the comment under the check to a sentence; the arrival check after the name apply, the guard this row disables, is unchanged in the same place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_file_a_person_put_there_while_the_tail_ran_refuses_its_landing`

Old text:

```
            if changed is not None:
                # Not continued, since no record was kept; the steps name the landing.
```

New text:

```
            if False:
                # Not continued, since no record was kept; the steps name the landing.
```

### `r1499.S04_arrival_after_plan`

sync land: a landing planned over an arrival is handed on at its gate

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S04_arrival_after_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`

Old text:

```
                changed = _arrived(cfg, staging, name, before)
                if changed is None:
                    raise

```

New text:

```
                changed = None
                if changed is None:
                    raise

```

### `r1499.S05_keep_after_arrival`

_keep: keep the record although something arrived, so the arrival reads as the pass's own on its next run

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S05_keep_after_arrival`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`

Old text:

```
    if why is not None:
        report.warnings.append(
```

New text:

```
    if False:
        report.warnings.append(
```

### `r1499.S06_keep_called`

sync land: keep no record at the tail's stop, so the pass continued refuses beside its own renamed tracks

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S06_keep_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[failed]`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[gate]`
  - `tests/test_sync_land_beside.py::test_the_record_is_kept_under_the_pass_at_each_tail_stop`

Old text:

```
            _keep(report, cfg, staging, name, before)
```

New text:

```
            pass
```

### `r1499.S07_kept_read`

_alone: read no kept record, so the pass's own renamed tracks are beside it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S07_kept_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[failed]`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[gate]`

Old text:

```
                kept=staged.kept(staged.pass_record(cfg, name)),
```

New text:

```
                kept=frozenset(),
```

### `r1499.S08_own_pass_proof`

_alone: never read the pass's landing proof, so a landed pass's record still reads files as its own

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S08_own_pass_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_once_the_passes_landing_is_proven_its_record_reads_nothing_as_its_own`

Old text:

```
                own_pass=name,
                origin=_ORIGIN,
```

New text:

```
                own_pass=None,
                origin=_ORIGIN,
```

### `r1499.S10_own_by_list`

_own_downloads: no download is the pass's own, so its own fresh tracks refuse it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S10_own_by_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 66 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_failed_tail_step_plans_no_landing_and_names_the_continuation`
  - `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_a_job_command_that_stops_at_a_gate_is_that_commands_gate`
  - `tests/test_sync_land.py::test_a_landing_that_needs_the_backup_acknowledgment_stops_without_minting_one`
  - `tests/test_sync_land.py::test_a_name_apply_refusal_ends_the_pass_before_the_landing`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes`
  - `tests/test_sync_land.py::test_a_pass_whose_vocal_model_can_score_says_so_and_asks_nothing`
  - ... and 51 more, see the JSON sidecar

Old text:

```
        if staged.pass_of(job) == name and job.library_id == cfg.library.volume_id
```

New text:

```
        if staged.pass_of(job) == name + '-' and job.library_id == cfg.library.volume_id
```

### `r1499.S11_unreadable_refuses`

_alone: a refusal of the reading (an unlistable folder, an unreadable root) reads as nothing beside

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S11_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`

Old text:

```
    except CratekitError as exc:
        raise _Stop(step, exc) from None
    except OSError
```

New text:

```
    except CratekitError:
        return staged.Settled(frozenset(), 0)
    except OSError
```

### `r1499.S12_warnings_in_refusal`

_with_warnings: a refusal drops the pass's warnings

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S12_warnings_in_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`

Old text:

```
    if report.warnings:
        data["warnings"]
```

New text:

```
    if False:
        data["warnings"]
```

### `r1499.S13_own_unnamed_step`

_own_unnamed: never name the landing under the pass for files no download names

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S13_own_unnamed_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`

Old text:

```
    if not (found.unnamed and own):
        return ()
```

New text:

```
    if True:
        return ()
```

### `r1499.B03_pass_step`

Waiting.step: a sync pass's download is named as a plain one, with no continue command

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B03_pass_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_fresh_go_beside_a_sync_passes_download_names_its_continue_command`
  - `tests/test_sync_land_beside.py::test_an_earlier_pass_renamed_at_its_gate_is_named_by_its_pass`
  - `tests/test_sync_land_beside.py::test_an_earlier_passes_unlanded_download_refuses_a_new_pass_naming_how_it_lands`
  - `tests/test_sync_land_staged.py::test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_an_unlanded_first_refuses_before_any_download_is_refused`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses`

Old text:

```
        if self.pass_name is not None and self.pass_run is not None:
```

New text:

```
        if False:
```

### `r1499.B04_pass_maybe_renamed`

beside: a sync pass whose tail may have renamed files no download names is never named

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B04_pass_maybe_renamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_earlier_pass_renamed_at_its_gate_is_named_by_its_pass`

Old text:

```
            name = pass_of(job) if run is None else None
```

New text:

```
            name = None
```

### `r1499.B05_arrived_items`

arrived: a new finished item of another download is not read

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B05_arrived_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_a_gos_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_gos_tail_that_fails_while_a_download_arrives_says_its_record_was_not_kept`

Old text:

```
    new = sorted({job_id for job_id, _item in after.items - before.items})
```

New text:

```
    new = []
```

### `r1499.B06_arrived_count`

arrived: a change in the count of files a landing takes is not read

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B06_arrived_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_a_person_put_there_while_the_tail_ran_refuses_its_landing`

Old text:

```
    if not new and after.count == before.count:
        return None
```

New text:

```
    if not new:
        return None
```

### `r1499.B08_kept_identity`

beside (sample of the lifted guards): files no download names are all read as own when a record exists

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B08_kept_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_ran_still_refuses_a_file_more_than_its_own_renamed`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_left_reads_no_file_put_there_since_as_its_own`
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_file_the_passes_tail_left_and_then_changed_is_not_its_own`

Old text:

```
        unnamed = [path for path in unnamed if identity(path) not in kept]
```

New text:

```
        unnamed = []
```

### `r1499.B10_plain_step_moves_out`

Waiting.step: a plain download's step says to land it in place, which lands the batch with it

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B10_plain_step_moves_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_plain_download_in_the_folder_refuses_a_fresh_go_before_the_gate`
  - `tests/test_sync_land_beside.py::test_a_plain_download_beside_the_pass_refuses_naming_it`

Old text:

```
f"move the tracks of job {self.job_id} out of {folder}, and land them on "
```

New text:

```
f"land the tracks of job {self.job_id} in {folder}, and land them on "
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

### `u174.O1_native_loop`

_mark_steps: plan no native pass, R-915 as it was

- File: `src/cratekit/organize/account.py`
- Source: `u174.json`, row `O1_native_loop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`
- Collected: 166 against a baseline of 166
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_landing_of_no_sync_pass_is_counted_and_is_no_step`
  - `tests/test_sync_mark.py::test_a_native_pass_whose_plan_refuses_is_a_refused_step_and_not_dropped`
  - `tests/test_sync_mark.py::test_organize_marks_a_native_pass_through_its_gate`
  - `tests/test_sync_mark.py::test_organize_plans_every_native_pass_not_only_the_latest`

Old text:

```
    for name in native_names:
```

New text:

```
    for name in ():
```

### `u174.O2_seen_skips_a_filed_pass`

_mark_steps: plan a pass with an intake file a second time by its native record

- File: `src/cratekit/organize/account.py`
- Source: `u174.json`, row `O2_seen_skips_a_filed_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_pass_with_an_intake_file_is_planned_once_by_its_file`

Old text:

```
        if name in seen:
            continue
```

New text:

```
        if False:
            continue
```

### `u174.O6_native_refusal_is_a_step`

_mark_steps: let native_passes' refusal escape, so the whole organize refuses and the file proven passes are not planned

- File: `src/cratekit/organize/account.py`
- Source: `u174.json`, row `O6_native_refusal_is_a_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`
- Collected: 166 against a baseline of 166
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_unreachable_root_is_a_refused_step_and_never_no_pass`
  - `tests/test_sync_mark.py::test_an_unreadable_tree_registry_refuses_the_native_step_alone`

Old text:

```
    try:
        native_names = mark_cli.native_passes(cfg)
    except CratekitError as exc:
```

New text:

```
    try:
        native_names = mark_cli.native_passes(cfg)
    except ZeroDivisionError as exc:
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

### `u82-a.A1_stat_oserror_is_the_refusal`

require_output: stop turning an OSError out of the one stat into sync-marks-blocked, so a file gone at that moment is a bare FileNotFoundError again, which is R-398

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A1_stat_oserror_is_the_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
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

### `u82-a.A3_an_empty_file_is_not_proof`

require_output: drop the empty file check, so a zero byte file lets the renames through

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A3_an_empty_file_is_not_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
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

### `u293.N1_no_answer`

_no_answer: an answer or a raised line given to the night is taken

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N1_no_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1069 against a baseline of 1069
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv0]`
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv1]`
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv2]`
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv3]`

Old text:

```
    if given:
```

New text:

```
    if False:
```

### `u293.N2_rekordbox_refused`

sync_night: the night runs beside rekordbox or its agent

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N2_rekordbox_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1069 against a baseline of 1069
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_refused_night_writes_its_record_even_when_its_line_cannot_be_kept`
  - `tests/test_sync_night.py::test_rekordbox_or_its_agent_up_refuses_before_any_call[running0]`
  - `tests/test_sync_night.py::test_rekordbox_or_its_agent_up_refuses_before_any_call[running1]`

Old text:

```
            rb_writer.assert_rekordbox_closed("crate sync night")
```

New text:

```
            pass
```

### `u293.N4_occupied_refused`

sync_night: a new pass runs beside what the staging folder holds

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N4_occupied_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1069 against a baseline of 1069
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_landed_pass_reads_settled_everywhere_whatever_is_staged_since`
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_waiting_at_its_gate`
  - `tests/test_sync_night.py::test_a_staging_folder_holding_what_a_landing_takes_refuses_a_new_pass`
  - `tests/test_sync_night.py::test_an_answered_gate_over_tracks_still_staged_stays_owed`

Old text:

```
                _nothing_waits(cfg, last)
```

New text:

```
                pass
```

### `u293.N5_owed_kept`

_refused: a refusal writes a fresh record over a pass still owed

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N5_owed_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1069 against a baseline of 1069
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_the_next_night_continues`
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_waiting_at_its_gate`
  - `tests/test_sync_night.py::test_an_answered_gate_over_tracks_still_staged_stays_owed`

Old text:

```
    if _owed(last) and last is not None:
```

New text:

```
    if False:
```

### `u293.N6_settled_by_landing`

settle: the pass's own landing never ends a wait, so a landed pass reads as waiting

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N6_settled_by_landing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1069 against a baseline of 1069
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_landed_pass_reads_settled_everywhere_whatever_is_staged_since`

Old text:

```
    if _landed(cfg, record.get("land_name")):
```

New text:

```
    if False:
```

### `u293.S3_sync_land_holds`

sync_land: a pass by hand takes no staging lock

- File: `src/cratekit/cli/sync_land.py`
- Source: `u293.json`, row `S3_sync_land_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_sync_land.py`, `tests/test_sync_land_beside.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_pass_by_hand_refuses_while_the_night_holds_the_lock`

Old text:

```
    with staging_lock.held("crate sync land", run_id=ctx.run.run_id):
```

New text:

```
    if True:
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

### `u130-c.C1_half_written_snapshot`

Record the snapshot when either side was written, not both

- File: `src/cratekit/sync/pair_write.py`
- Source: `u130-c.json`, row `C1_half_written_snapshot`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
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

### `u130-c.C5_no_renumber`

Leave rekordbox's order as the adds and removals left it

- File: `src/cratekit/write/playlist_pair.py`
- Source: `u130-c.json`, row `C5_no_renumber`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_added_on_the_account_only_lands_in_rekordbox_in_place`
  - `tests/test_sync_pair.py::test_the_first_sync_marks_the_pair_and_adds_only`
  - `tests/test_sync_pair.py::test_when_both_sides_reorder_the_account_order_wins`

Old text:

```
            moved = renumber(db, change.playlist_id, change.order)
```

New text:

```
            moved = 0
```

### `u216.M21_reserve_adopt_empty`

reserve_folder: an adoption records an empty set whatever the plan listed

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M21_reserve_adopt_empty`
- Moved: Anchored where u309-replay-after-b.json replayed it: PairStore.reserve_folder's adoption in pairs.py writes the same expression on one line without the parentheses; same record of what it held emptied
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_an_adoption_whose_plan_did_not_say_what_it_held_is_recorded_as_unknown`
  - `tests/test_sync_pair_adopted.py::test_reserving_an_adopted_folder_records_what_it_held_and_a_created_one_nothing`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
                before = None if held is None else frozenset(str(one) for one in held if str(one))
```

New text:

```
                before = frozenset()
```

### `u216.M22_write_drops_held`

_write: the folder record is written without what it held

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M22_write_drops_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_playlist_no_pair_names_still_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_folder_record_keeps_what_it_held_through_another_write`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_a_created_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_the_adopted_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_reserving_an_adopted_folder_records_what_it_held_and_a_created_one_nothing`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
                    **({"held": sorted(one.held)} if one.held is not None else {}),
```

New text:

```
                    **({}),
```

### `u216.M23_read_drops_held`

_folders: what a folder held is never read back

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M23_read_drops_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_playlist_no_pair_names_still_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_folder_record_keeps_what_it_held_through_another_write`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_a_created_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_the_adopted_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_reserving_an_adopted_folder_records_what_it_held_and_a_created_one_nothing`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
                None if held is None else frozenset(held),
            )
```

New text:

```
                None,
            )
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

### `u216.M20_made_drops_held`

_made: the plan's listing is not passed to the folder's reservation

- File: `src/cratekit/sync/pair_write.py`
- Source: `u216.json`, row `M20_made_drops_held`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
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

### `r1264.M22_readable_dates`

list_playlist_readable: give no added dates, so a pair's later change calls read every time as unknown

- File: `src/cratekit/intake/cli.py`
- Source: `r1264.json`, row `M22_readable_dates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_merge.py`
- Collected: 183 against a baseline of 183
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
        dates=_added_dates(rows, tracks),
```

New text:

```
        dates={},
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

### `u209.H7_hold_equality_unchecked`

held_plan.hold: hold a plan that does not read back equal to itself

- File: `src/cratekit/core/held_plan.py`
- Source: `u209.json`, row `H7_hold_equality_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 22479 against a baseline of 22479
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

### `u202.C4_dates_recorded`

_record: the account's added dates are never recorded with the snapshot

- File: `src/cratekit/sync/pair_write.py`
- Source: `u202.json`, row `C4_dates_recorded`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
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

### `u202-composites.P1_reserve_held`

reserve_made_rekordbox: an account playlist a pair already holds is made a second rekordbox playlist

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u202-composites.json`, row `P1_reserve_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`
- Collected: 160 against a baseline of 160
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_reserving_an_account_playlist_a_pair_holds_answers_that_pair_and_makes_nothing`

Old text:

```
            held = document.pairs.get(account_id)
            if held is not None:
                return held.rekordbox_id, False
            rekordbox_id = str(create())
```

New text:

```
            rekordbox_id = str(create())
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

### `u198.P2_release_side`

pairs.release: the survivor is recorded on the wrong side

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u198.json`, row `P2_release_side`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_in_rekordbox_unpairs_and_leaves_the_account_playlist`
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_on_the_account_unpairs_stays_and_is_not_made_again`
  - `tests/test_sync_pair_discover.py::test_a_write_of_the_pairs_alone_keeps_the_folders_misses_and_released`

Old text:

```
            if side == ACCOUNT_SIDE:
```

New text:

```
            if side != ACCOUNT_SIDE:
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

### `u198.C9_account_only`

apply_pair: a new pair is made when only rekordbox was approved

- File: `src/cratekit/sync/pair_write.py`
- Source: `u198.json`, row `C9_account_only`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
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

### `u304-b.S15_favourites_home_judged_without_the_foreign_check`

pair_discover.discover: a playlist named as the favourites one inside another app's folder counts as the Favorites home; S9's composite, the foreign check S9 hands every node to, removed

- File: `src/cratekit/sync/pair_discover.py`
- Source: `u304-b.json`, row `S15_favourites_home_judged_without_the_foreign_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_adopted.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_favourites_name_inside_another_apps_folder_does_not_unsettle_the_home`

Old text:

```
        for row in foreign_tree.outside(
            [r for r in live if _attribute(r) == PLAIN and str(getattr(r, "Name", "") or "") == favorites],
            every,
        )
```

New text:

```
        for row in [r for r in live if _attribute(r) == PLAIN and str(getattr(r, "Name", "") or "") == favorites]
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

