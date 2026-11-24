# Mutation table: u335-before-06

Measured by `scripts/mutate.py` on 2026-11-24 05:01 UTC, branch `HEAD` at `b41c698d`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 276.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 05:01 UTC for commit `b41c698da363`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 59, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1056.N9_verb_not_threaded` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 6 | killed |
| `u308.L5_extended_step_dropped` | `src/cratekit/label/review_common.py` | user | 3 file(s) | 247 | 8 | killed |
| `u308.L6_ended_outcome_ignored` | `src/cratekit/label/review_common.py` | user | 4 file(s) | 366 | 20 | killed |
| `u108-a.G01_unsettled_skips_settled` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 4 | killed |
| `u108-c.G19_settle_keeps` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `u108-c.G24_walk_ends_at_gate` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 8 | killed |
| `u108-d.G18_settle_matches_identity_again` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `u108-d.G20_settle_skips_settled_again` | `src/cratekit/label/sync_cli.py` | maintainer | 2 file(s) | 205 | 1 | killed |
| `u189.S2_question_not_saved` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 119 | killed |
| `u240.M24_ascii_fold` | `src/cratekit/label/verify.py` | user | 3 file(s) | 404 | 2 | killed |
| `u192.F1_no_rearm_catch` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 279 | 4 | killed |
| `u192.F2_no_retry` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 279 | 4 | killed |
| `u192.F4_command_dropped` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 279 | 4 | killed |
| `u192.F5_settled_count` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 279 | 1 | killed |
| `u192.F6_queue_only_never` | `src/cratekit/modules/foreground.py` | user | 4 file(s) | 414 | 21 | killed |
| `u192.F7_queue_only_always` | `src/cratekit/modules/foreground.py` | user | 3 file(s) | 343 | 9 | killed |
| `u236.M19_ledger_normalizer_drops` | `src/cratekit/modules/outbound/ledger.py` | user | 8 file(s) | 225 | 8 | killed |
| `u140.B1_ledger_folds_into_a_twin` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B2_ledger_moves_another_id` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 29 | 1 | killed |
| `u309.U4_reserve_recorded_wins` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 9 file(s) | 514 | 15 | killed |
| `u309.U5_reserve_written` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 9 file(s) | 514 | 136 | killed |
| `u201-composites.C4_settle_none` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 5 file(s) | 187 | 5 | killed |
| `u201.L1_agreed_own_playlist` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 5 file(s) | 187 | 1 | killed |
| `u236.M17_ledger_settle_keeps_placement` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 2 file(s) | 25 | 4 | killed |
| `u236.M18_ledger_placement_not_written` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 2 file(s) | 25 | 8 | killed |
| `u236.M20_agreed_never_drops` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 8 file(s) | 225 | 3 | killed |
| `u201.M1_plan_keeps` | `src/cratekit/modules/outbound/mirror.py` | user | 5 file(s) | 187 | 6 | killed |
| `u201.M2_plan_skips` | `src/cratekit/modules/outbound/mirror.py` | user | 5 file(s) | 187 | 5 | killed |
| `u201.E10_unknown_time` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 4 | killed |
| `u201.E13_snapshot_word` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 2 | killed |
| `u201.E3_own_genre_derived_held` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 2 | killed |
| `u201.E6_short_unread` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 187 | 3 | killed |
| `u204.P11_inbox_hold_per_batch` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 224 | 4 | killed |
| `u204.P12_favorites_stay` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.P2_acquire_only_unknown` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 224 | 2 | killed |
| `u230.M13_held_by_dropped` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 212 | 29 | killed |
| `u236.M1_ours_empty` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 10 | killed |
| `u236.M2_unfavourite_counts_ours` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 7 | killed |
| `u236.M3_moved_counts_ours` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 3 | killed |
| `u236.M5_mine_not_left` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 3 | killed |
| `u236.M7_placed_after_keeps_all` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 4 | killed |
| `u236.M8_placed_after_drops_unheld` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 225 | 3 | killed |
| `u198.P2_release_side` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 168 | 3 | killed |
| `u202-composites.P1_reserve_held` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 160 | 1 | killed |
| `u216.M21_reserve_adopt_empty` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 385 | 9 | killed |
| `u216.M22_write_drops_held` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 385 | 12 | killed |
| `u216.M23_read_drops_held` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 385 | 12 | killed |
| `u216.M24_read_unvalidated` | `src/cratekit/modules/outbound/pairs.py` | user | 1 file(s) | 30 | 4 | killed |
| `u221.R12_hold_not_written` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 154 | 18 | killed |
| `u221.R13_hold_not_read` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 154 | 18 | killed |
| `u221.R15_mark_drops_the_hold` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 83 | 14 | killed |
| `u221.R16_release_any_rekordbox_side` | `src/cratekit/modules/outbound/pairs.py` | user | 1 file(s) | 32 | 1 | killed |
| `u221.R18_release_writes_nothing` | `src/cratekit/modules/outbound/pairs.py` | user | 1 file(s) | 32 | 6 | killed |
| `u234.O18_snapshot_keeps_the_reading` | `src/cratekit/modules/outbound/pairs.py` | maintainer | 23 file(s) | 1786 | 4 | killed |
| `u234.O19_reading_not_written` | `src/cratekit/modules/outbound/pairs.py` | user | 23 file(s) | 1786 | 14 | killed |
| `u201.S1_short_undeclared` | `src/cratekit/modules/outbound/service.py` | user | 5 file(s) | 187 | 1 | killed |
| `r1017.M10_older_beats_to` | `src/cratekit/modules/outbound/sets.py` | user | 4 file(s) | 174 | 2 | killed |
| `r1017.M8_first_older_name_only` | `src/cratekit/modules/outbound/sets.py` | user | 4 file(s) | 174 | 2 | killed |
| `r1017.M9_twin_only_beside_to` | `src/cratekit/modules/outbound/sets.py` | user | 4 file(s) | 174 | 2 | killed |
| `u129-author.A17_empty_add_still_writes` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 20 | 3 | killed |
| `u140.A2_new_name_record_ignored` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 6 | killed |
| `u140.A3_refreeze_against_account_spelling` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.A4_rename_always` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 4 | killed |
| `u140.A5_ledger_never_rekeyed` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 9 | killed |
| `u140.A6_refreeze_account_spelling` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 1 | killed |
| `u142.S1_folder_prefix` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 216 | 13 | killed |
| `u142.S5_create_under_the_year` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 216 | 6 | killed |
| `r227.A2_never_stale` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 372 | 13 | killed |
| `r1308.M23_read_back_bypassed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 34 | killed |
| `r1411.A1_agreed_order_always_stands` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 11 | killed |
| `r1411.A3_added_tracks_asked_of_the_agreed_order` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 7 | killed |
| `r836-a.A1_product_made_asked_first` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 112 | 3 | killed |
| `u130-c.C6_pair_not_vouched` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 67 | 5 | killed |
| `u220.A1_front_target` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 12 | killed |
| `u231.M5_positions_not_advanced` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 38 | killed |
| `u206.M17_account_hit_ignored` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 9 file(s) | 1131 | 13 | killed |
| `u208.M19_adapter_never_records_tie` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 134 | 5 | killed |
| `r388-c.M17_slug_respelled` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 723 | 4 | killed |
| `u211.B1_backup_database_portion_refuses_alone` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 3 file(s) | 167 | 1 | killed |
| `u27-restore-cli-independent.X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 3 file(s) | 431 | 3 | killed |
| `r187-a.A10_ambiguous_falls_through` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 1 | killed |
| `r187-a.A11_no_cutoff` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 4 | killed |
| `r187-a.A12_partial_message` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 1 | killed |
| `r187-a.A1_exact_first` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 2 | killed |
| `r187-a.A3_holds_dropped` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 4 | killed |
| `r187-a.A5_word_threshold_high` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 1 | killed |
| `r187-a.A6_first_of_several` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 4 | killed |
| `r187-a.A7_partial_never` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 3 | killed |
| `r187-a.A8_walk_order` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 1 | killed |
| `r187-a.A9_key_discarded` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 1 | killed |
| `r187-b.B12_not_carried_forward` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 1 | killed |
| `u266.M1_seven_opens_again` | `src/cratekit/modules/tools/setbuilder.py` | user | 3 file(s) | 325 | 52 | killed |
| `u279.M12_holder_never_found` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 2 | killed |
| `u279.M1_walk_ignores_exclude` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 10 | killed |
| `u279.M2_excluded_folder_walked` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 10 | killed |
| `u279.M3_ancestor_taken_whole` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 1 | killed |
| `u279.M4_symlink_followed` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 1 | killed |
| `u279.M5_unlistable_raises` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 1 | killed |
| `u279.M6_chain_unresolved` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 1 | killed |
| `u279.M7_outermost_folder_excluded` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 1 | killed |
| `u311.C8_unreadable_number_raises` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 44 | killed |
| `u311.C9_anchor_comes_back` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 13 | killed |
| `u43-author-light.E1_anchor_is_its_own_companion` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 8 | killed |
| `u43-author-light.E3_tempo_serialized_as_bpm` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 4 | killed |
| `u174.O1_native_loop` | `src/cratekit/organize/account.py` | user | 2 file(s) | 166 | 4 | killed |
| `u174.O2_seen_skips_a_filed_pass` | `src/cratekit/organize/account.py` | user | 2 file(s) | 166 | 1 | killed |
| `u174.O3_no_pass_counted` | `src/cratekit/organize/account.py` | user | 2 file(s) | 166 | 1 | killed |
| `u174.O4_no_pass_is_no_step` | `src/cratekit/organize/account.py` | user | 2 file(s) | 166 | 1 | killed |
| `u174.O6_native_refusal_is_a_step` | `src/cratekit/organize/account.py` | user | 2 file(s) | 166 | 2 | killed |
| `u204.A1_adopt_landed` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 224 | 1 | killed |
| `u222.M11_decided_freeze_shown` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 255 | 2 | killed |
| `u222.M12_unshown_not_said` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M19_stale_on_every_run` | `src/cratekit/organize/account_mirror.py` | maintainer | 6 file(s) | 255 | 1 | killed |
| `u222.M1_overlay_not_read` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 255 | 3 | killed |
| `u222.M20_every_step_reworded` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 255 | 2 | killed |
| `u222.M25_steps_not_frozen` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 255 | 6 | killed |
| `u236.M10_reader_no_time_check` | `src/cratekit/organize/account_mirror.py` | user | 8 file(s) | 225 | 3 | killed |
| `u236.M11_reader_never_placed` | `src/cratekit/organize/account_mirror.py` | user | 8 file(s) | 225 | 1 | killed |
| `u236.M12_reader_short_branch` | `src/cratekit/organize/account_mirror.py` | user | 8 file(s) | 225 | 1 | killed |
| `u309-z2.U21_reading_unread_listed` | `src/cratekit/organize/account_mirror.py` | user | 5 file(s) | 118 | 1 | killed |
| `u309-z2.U22_keep_newest_time` | `src/cratekit/organize/account_mirror.py` | user | 4 file(s) | 126 | 1 | killed |
| `u242.M23_filing_dates_a_found_prefix` | `src/cratekit/organize/filing.py` | user | 3 file(s) | 198 | 3 | killed |
| `r1289.M14_mirror_unread_branch` | `src/cratekit/organize/mirror_downloads.py` | user | 3 file(s) | 103 | 1 | killed |
| `r1289.M15_mirror_reads_whole` | `src/cratekit/organize/mirror_downloads.py` | user | 3 file(s) | 103 | 1 | killed |
| `r1289.M16_mirror_why` | `src/cratekit/organize/mirror_downloads.py` | user | 1 file(s) | 37 | 1 | killed |
| `r1289.M17_mirror_listing_refusal` | `src/cratekit/organize/mirror_downloads.py` | user | 1 file(s) | 37 | 1 | killed |
| `u204.D1_one_queue_per_track` | `src/cratekit/organize/mirror_downloads.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.D2_write_rereads_queue` | `src/cratekit/organize/mirror_downloads.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.D3_owned_recording` | `src/cratekit/organize/mirror_downloads.py` | user | 6 file(s) | 224 | 2 | killed |
| `u204.D4_never_lands_named` | `src/cratekit/organize/mirror_downloads.py` | user | 6 file(s) | 224 | 2 | killed |
| `u230.M15_source_blank` | `src/cratekit/organize/mirror_downloads.py` | user | 11 file(s) | 212 | 6 | killed |
| `u230.M16_unread_raises` | `src/cratekit/organize/mirror_downloads.py` | user | 11 file(s) | 212 | 1 | killed |
| `u267.M13_downloads_owned_opens_its_own` | `src/cratekit/organize/mirror_downloads.py` | user | 2 file(s) | 51 | 1 | killed |
| `r1950.M02_identity_drops_second` | `src/cratekit/organize/mirror_edits.py` | user | 2 file(s) | 66 | 1 | killed |
| `r1950.M03_write_skips_second_read_back` | `src/cratekit/organize/mirror_edits.py` | user | 2 file(s) | 66 | 2 | killed |
| `r1950.M04_item_hides_second` | `src/cratekit/organize/mirror_edits.py` | user | 3 file(s) | 71 | 2 | killed |
| `u201-composites.C5_leave_nothing` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 187 | 6 | killed |
| `u201.O1_latch` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 187 | 1 | killed |
| `u201.O2_stale` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 187 | 1 | killed |
| `u201.O3_target_bucket` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 187 | 6 | killed |
| `u204.O2_unfavourite_leaves_months` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.O3_quarter_refused` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.O4_colour` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.O5_batch_live` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.O6_inbox_latch` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u204.O7_restore_detected` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 224 | 1 | killed |
| `u236.M13_write_records_no_month` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 225 | 6 | killed |
| `u236.M14_write_wrong_time` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 225 | 6 | killed |
| `u236.M15_settle_month_title` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 225 | 8 | killed |
| `u236.M16_settle_any_favourite` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 225 | 1 | killed |
| `u340.R17_edit_second_path_off` | `src/cratekit/organize/mirror_edits.py` | user | 3 file(s) | 103 | 1 | killed |
| `u340.R18_edit_off_other` | `src/cratekit/organize/mirror_edits.py` | user | 2 file(s) | 61 | 3 | killed |
| `u340.R19_edit_third_swapped` | `src/cratekit/organize/mirror_edits.py` | user | 3 file(s) | 103 | 2 | killed |
| `u340.R20_edit_write_drops_second` | `src/cratekit/organize/mirror_edits.py` | user | 3 file(s) | 103 | 1 | killed |
| `u340.R29_edit_fallback_taken` | `src/cratekit/organize/mirror_edits.py` | user | 3 file(s) | 103 | 2 | killed |
| `u214.M12_frozen_pairs` | `src/cratekit/organize/mirror_frozen.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u222-zeros.M18_label_no_folder` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222-zeros.M5_agreed_none_lost` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M10_shown_flag_check` | `src/cratekit/organize/mirror_frozen.py` | maintainer | 6 file(s) | 255 | 1 | killed |
| `u222.M13_moved_equal_named` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 5 | killed |
| `u222.M14_moved_new_step_silent` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M15_moved_gone_step_silent` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M16_lines_inverted` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 4 | killed |
| `u222.M17_refused_named_by_every_line` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M2_overlay_never_replaces` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 4 | killed |
| `u222.M3_overlay_any_remote_id` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M6_load_drops_agreed` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 255 | 6 | killed |
| `u222.M8_agreed_list_check` | `src/cratekit/organize/mirror_frozen.py` | maintainer | 6 file(s) | 255 | 1 | killed |
| `u222.M9_text_check` | `src/cratekit/organize/mirror_frozen.py` | maintainer | 6 file(s) | 255 | 1 | killed |
| `u236.M21_frozen_not_overlaid` | `src/cratekit/organize/mirror_frozen.py` | user | 8 file(s) | 225 | 2 | killed |
| `u236.M22_frozen_not_written` | `src/cratekit/organize/mirror_frozen.py` | user | 8 file(s) | 225 | 1 | killed |
| `u236.M23_frozen_reads_malformed` | `src/cratekit/organize/mirror_frozen.py` | user | 8 file(s) | 225 | 1 | killed |
| `r598-b.B1_sweep_before_the_lock` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `r598-b.B3_orphans_not_shown` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `r598-b.B4_abandon_only_reported_as_no_op` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `r598-b.B5_kept_reports_nothing` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 4 | killed |
| `u138.S7_verb_drops_the_answer` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 7 | killed |
| `u184.A10_summary_always_recorded` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A11_wording_swapped` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u184.A1_flag_ignored` | `src/cratekit/session/cli.py` | user | 3 file(s) | 86 | 10 | killed |
| `u184.A2_any_actor_accepted` | `src/cratekit/session/cli.py` | user | 3 file(s) | 86 | 3 | killed |
| `u184.A3_engine_rule_not_selected` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 9 | killed |
| `u184.A4_valid_record_minted_again` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u184.A5_expired_reported_valid` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A6_unreadable_record_refuses` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A7_already_valid_says_ok` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A8_expiry_row_dropped` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A9_expiry_row_names_the_mint` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u311.B2_acknowledgment_hides_what_it_showed` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.A2_the_abort_mints_anyway` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.A3_the_refusal_names_no_ages` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 4 | killed |
| `u49-author.A4_the_record_on_file_is_not_shown` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.A6_the_authorisation_is_not_spent` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.A7_the_check_rows_are_keyed_wrong` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.A8_a_damaged_record_locks_the_verb_out` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.R1_hard_code_the_repair_token` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.R2_hard_code_the_permission_token` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.R3_an_unreadable_file_reads_as_empty` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `r1924.C1_refusal` | `src/cratekit/session/restore_cli.py` | user | 4 file(s) | 411 | 4 | killed |
| `r1924.C2_totals` | `src/cratekit/session/restore_cli.py` | user | 4 file(s) | 411 | 9 | killed |
| `r1924.C3_dry_run_message` | `src/cratekit/session/restore_cli.py` | user | 4 file(s) | 411 | 1 | killed |
| `r187-a.C1_blank_not_key` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `r187-a.C3_mutex` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `r187-a.C4_key_beside_name` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `r187-a.C5_empty_name_scans` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `r187-a.C6_no_cache_path` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 3 | killed |
| `u279.M10_tilde_not_expanded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 340 | 1 | killed |
| `u279.M11_excluded_anchor_not_refused` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 340 | 2 | killed |
| `u279.M13_wrong_folder_named` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 340 | 1 | killed |
| `u279.M8_index_call_unexcluded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 340 | 6 | killed |
| `u279.M9_staging_not_excluded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 340 | 4 | killed |
| `u43-author-light.A1_first_track_wins` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 4 | killed |
| `u43-author-light.A3_containment_not_checked` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `u43-author-light.A4_empty_anchor_defaults` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `u43-author-light.C1_no_lower_bound` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 4 | killed |

## Zero rows and what they owe

- `u214.M12_frozen_pairs` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r1056.N9_verb_not_threaded`

label_mark: prove the pass with sync mark's own wording, so a refusal names sync mark and intake missing

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N9_verb_not_threaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_landing_between_the_plan_and_the_first_rename_renames_nothing`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[abandoned]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[another-pass]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[never-committed]`
  - `tests/test_label_mark_native.py::test_a_pass_no_closed_committed_native_landing_names_is_refused_by_name[no-landing]`
  - `tests/test_label_mark_native.py::test_an_unreachable_library_names_label_mark_as_the_verb_to_run_again`

Old text:

```
        native = native_proof(cfg, str(ctx.args.pass_name), verb=_VERB, named=_NAMED)
```

New text:

```
        native = native_proof(cfg, str(ctx.args.pass_name))
```

### `u308.L5_extended_step_dropped`

review_common.extended: the step the review verbs add to a refusal is dropped

- File: `src/cratekit/label/review_common.py`
- Source: `u308.json`, row `L5_extended_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_artists.py`, `tests/test_label_sync_go.py`
- Collected: 247 against a baseline of 247
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`
  - `tests/test_label_artists.py::test_three_reads_failing_in_a_row_stop_the_run_and_say_what_was_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-held-release]`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-passed-release]`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park`

Old text:

```
    steps = (*cause.remediation.steps, step)
```

New text:

```
    steps = tuple(cause.remediation.steps)
```

### `u308.L6_ended_outcome_ignored`

review_common.ended: every review verb ends OK whatever outcome it reached

- File: `src/cratekit/label/review_common.py`
- Source: `u308.json`, row `L6_ended_outcome_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_artists.py`, `tests/test_label_genre_gate.py`, `tests/test_label_sync_go.py`
- Collected: 366 against a baseline of 366
- Kills: 20 (killed)
- Killed:
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_every_track_owned_is_a_no_op_and_writes_nothing`
  - `tests/test_label_approved.py::test_nothing_accepted_is_a_no_op_that_never_opens_the_catalogue`
  - `tests/test_label_artists.py::test_a_decided_item_reading_an_address_is_left_as_it_is[accepted]`
  - `tests/test_label_artists.py::test_a_decided_item_reading_an_address_is_left_as_it_is[rejected]`
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_a_release_decided_while_it_was_being_read_is_not_rewritten`
  - `tests/test_label_artists.py::test_a_release_the_provider_does_not_serve_is_counted_and_never_blanked`
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[   ]`
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[]`
  - `tests/test_label_artists.py::test_an_artist_put_right_meanwhile_is_not_overwritten`
  - `tests/test_label_artists.py::test_an_empty_queue_is_a_no_op_that_opens_no_catalogue`
  - `tests/test_label_artists.py::test_an_item_whose_artist_is_a_name_is_not_asked_about`
  - `tests/test_label_genre_gate.py::test_a_held_release_returned_to_review_is_filed_and_not_held_again`
  - `tests/test_label_genre_gate.py::test_a_release_filed_before_the_sweep_had_a_gate_is_asked_about_at_approval`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        data={"checks": checks, "summary": summary}, outcome=outcome, warnings=warnings
```

New text:

```
        data={"checks": checks, "summary": summary}, outcome=Outcome.OK, warnings=warnings
```

### `u108-a.G01_unsettled_skips_settled`

sync_cli.unsettled: read every saved answer as unsettled, so a go summarises answers an earlier go already took

- File: `src/cratekit/label/sync_cli.py`
- Source: `u108-a.json`, row `G01_unsettled_skips_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_job_whose_track_was_refused_for_good_is_not_resumed`
  - `tests/test_label_sync_go.py::test_a_job_stopped_halfway_resumes_and_downloads_only_the_rest`
  - `tests/test_label_sync_go.py::test_a_settled_answer_is_not_summarised_again`
  - `tests/test_label_sync_go.py::test_answers_saved_beside_a_finished_go_wait_and_are_not_landed_with_it`

Old text:

```
        if isinstance(entry, Mapping) and not entry.get(SETTLED)
    ]
```

New text:

```
        if isinstance(entry, Mapping)
    ]
```

### `u108-c.G19_settle_keeps`

sync_cli.settle_in: an answer holding a release named in keep is settled anyway

- File: `src/cratekit/label/sync_cli.py`
- Source: `u108-c.json`, row `G19_settle_keeps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`

Old text:

```
        if isinstance(taken, list) and any(one in keep for one in taken):
            continue
```

New text:

```
        if False:
            continue
```

### `u108-c.G24_walk_ends_at_gate`

sync_cli._walk: a walk that answered every label ends without asking the gate

- File: `src/cratekit/label/sync_cli.py`
- Source: `u108-c.json`, row `G24_walk_ends_at_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_label_whose_catalogue_cannot_be_listed_fails_its_line_and_the_walk_goes_on`
  - `tests/test_label_sync.py::test_a_pick_of_a_digit_that_is_not_a_number_is_asked_again`
  - `tests/test_label_sync.py::test_a_pick_outside_the_numbers_is_asked_again`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`
  - `tests/test_label_sync_go.py::test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op`
  - `tests/test_label_sync_go.py::test_the_walk_ends_at_the_gate_and_a_yes_downloads_what_it_answered`
  - `tests/test_label_sync_go.py::test_the_walk_refused_beside_a_download_keeps_what_it_answered`

Old text:

```
    if stopped_at is None:
        # EVERY LABEL WITH SOMETHING NEW IS ANSWERED
```

New text:

```
    if False:
        # EVERY LABEL WITH SOMETHING NEW IS ANSWERED
```

### `u108-d.G18_settle_matches_identity_again`

sync_cli.settle_in: an answer is settled by its place alone, without checking it is the answer the summary covered

- File: `src/cratekit/label/sync_cli.py`
- Source: `u108-d.json`, row `G18_settle_matches_identity_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_settling_leaves_an_answer_whose_place_now_holds_a_different_one`

Old text:

```
        if (
            _text(entry.get("label_id")) != label_id
            or _text(entry.get("answered_at")) != answered_at
        ):
            continue
```

New text:

```
        if False:
            continue
```

### `u108-d.G20_settle_skips_settled_again`

sync_cli.settle_in: an answer already settled is settled again, its first marker overwritten

- File: `src/cratekit/label/sync_cli.py`
- Source: `u108-d.json`, row `G20_settle_skips_settled_again`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_settling_an_answer_already_settled_keeps_its_first_marker`

Old text:

```
        if not isinstance(entry, Mapping) or entry.get(SETTLED):
            continue
        if (
```

New text:

```
        if not isinstance(entry, Mapping):
            continue
        if (
```

### `u189.S2_question_not_saved`

_next, sample of the unit's existing guards: print a new question without saving it, so no answer can apply to it

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `S2_question_not_saved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
- Kills: 119 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv5-goes with --answer pick]`
  - `tests/test_label_sync.py::test_a_label_with_three_new_releases_is_asked_once`
  - `tests/test_label_sync.py::test_a_later_answer_files_its_releases_under_the_run_that_asked`
  - `tests/test_label_sync.py::test_a_pick_naming_a_release_the_question_did_not_offer_is_refused`
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`
  - `tests/test_label_sync.py::test_a_release_answered_not_now_is_not_filed_by_the_labels_sweep`
  - `tests/test_label_sync.py::test_a_release_the_genre_gate_holds_never_appears_in_a_question`
  - `tests/test_label_sync.py::test_a_release_the_sweep_filed_while_its_question_waited_is_settled_by_the_answer`
  - `tests/test_label_sync.py::test_a_saved_question_is_printed_again_with_no_provider_call`
  - `tests/test_label_sync.py::test_a_saved_shortfall_that_withheld_nothing_reads_back_as_no_shortfall`
  - `tests/test_label_sync.py::test_a_superseded_item_is_not_counted_as_waiting_by_label_approved`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[all]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[not-now]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[pick]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[stop]`
  - ... and 104 more, see the JSON sidecar

Old text:

```
                question = listed.question
                _save_pending(cfg, question)
```

New text:

```
                question = listed.question
```

### `u240.M24_ascii_fold`

credit_names: fold as fold_label does, dropping letters outside ASCII (round two's second blocker)

- File: `src/cratekit/label/verify.py`
- Source: `u240.json`, row `M24_ascii_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 404 against a baseline of 404
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_letter_outside_ascii_never_folds_away_from_a_needle[\u6771\u4eac Records-\u2117 2023 Completely Unrelated Records]`
  - `tests/test_tag_folder_copyright.py::test_a_letter_outside_ascii_never_folds_away_from_a_needle[\xc2me-\u2117 2021 Give Me Records]`

Old text:

```
_WORD_BREAK = re.compile(r"[\W_]+")
```

New text:

```
_WORD_BREAK = re.compile(r"[^a-z0-9]+")
```

### `u192.F1_no_rearm_catch`

settle: let the cancelled refusal through untouched, so an interrupted drive leaves the job closed and names job resume

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F1_no_rearm_catch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 279 against a baseline of 279
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`

Old text:

```
    except JobCancelled as exc:
        raise _resumable(exc, job_id, argv, origin) from exc
```

New text:

```
    except ZeroDivisionError as exc:
        raise _resumable(exc, job_id, argv, origin) from exc
```

### `u192.F2_no_retry`

_resumable: read the job instead of re-arming it, so the named --job command meets a closed job

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F2_no_retry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 279 against a baseline of 279
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`

Old text:

```
        job = jobs.retry(store, job_id)
```

New text:

```
        job = jobs.get(store, job_id)
```

### `u192.F4_command_dropped`

_resumable: the first step says to resume the job without naming the command

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F4_command_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 279 against a baseline of 279
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`

Old text:

```
        f"resume it with: {command}",
```

New text:

```
        "resume it with its --job command",
```

### `u192.F5_settled_count`

_resumable: report the total in place of the settled count

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F5_settled_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 279 against a baseline of 279
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`

Old text:

```
        f"the job is queued again with {progress['settled']} of {progress['total']} "
```

New text:

```
        f"the job is queued again with {progress['total']} of {progress['total']} "
```

### `u192.F6_queue_only_never`

queue_only: always False, so --queue-only drives the job anyway

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F6_queue_only_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`, `tests/test_label_genre.py`, `tests/test_sync_land.py`
- Collected: 414 against a baseline of 414
- Kills: 21 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_job_an_older_build_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`
  - `tests/test_analysis_workers.py::test_an_item_an_older_build_renamed_before_its_row_moved_resumes_as_finished`
  - `tests/test_analysis_workers.py::test_an_item_written_before_its_row_moved_resumes_by_its_mark_and_is_measured_once`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[restamp]`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[run]`
  - `tests/test_analysis_workers.py::test_the_shared_tail_step_queues_only_and_drives_its_job_once`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return bool(getattr(args, "queue_only", False))
```

New text:

```
    return False
```

### `u192.F7_queue_only_always`

queue_only: always True, so a verb run by hand queues and returns as before U192

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F7_queue_only_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`, `tests/test_label_genre.py`
- Collected: 343 against a baseline of 343
- Kills: 9 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_analysis_workers.py::test_analyze_restamp_by_hand_drives_its_job_and_says_the_database_note_once`
  - `tests/test_analysis_workers.py::test_analyze_run_by_hand_queues_and_drives_its_job_to_succeeded_in_one_call`
  - `tests/test_label_genre.py::test_a_sweep_driven_at_its_queue_keeps_the_label_warning_and_never_calls_its_label_unapplied`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_tag_folder_by_hand_prints_the_settled_job_and_no_drive_command`
  - `tests/test_tag_workers.py::test_tag_folder_by_hand_queues_and_drives_its_sweep_to_succeeded_in_one_call`

Old text:

```
    return bool(getattr(args, "queue_only", False))
```

New text:

```
    return True
```

### `u236.M19_ledger_normalizer_drops`

ledger load: drop every folder's placements on read and write

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u236.json`, row `M19_ledger_normalizer_drops`
- Moved: the placements kept on load are still in ledger.py, but the mirrored folder normalizer was pulled out of _load into _mirror_document, so the lines sit eight spaces shallower; same placements dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 8 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_survives_the_ledgers_own_read_and_write`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
            {"placed": placed}
            if (placed := _placements(value.get("placed")))
            else {}

```

New text:

```
            {}

```

### `u140.B1_ledger_folds_into_a_twin`

rename_set_playlist drops its refusal when the new name already holds another playlist

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u140.json`, row `B1_ledger_folds_into_a_twin`
- Moved: rename_set_playlist moved from ledger.py to ledger_reserve.py and raises through the shared _refused instead of _unusable with a path; same refusal condition reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_ledger_refuses_to_fold_a_rename_into_another_playlist`

Old text:

```
        if held:
            raise _refused(

```

New text:

```
        if False:
            raise _refused(

```

### `u140.B2_ledger_moves_another_id`

rename_set_playlist drops its refusal when the old name records a different playlist

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u140.json`, row `B2_ledger_moves_another_id`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_ledger_refuses_to_fold_a_rename_into_another_playlist`

Old text:

```
        if recorded != remote_id:

```

New text:

```
        if False:

```

### `u309.U4_reserve_recorded_wins`

A reservation creates again over the playlist the ledger already records

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u309.json`, row `U4_reserve_recorded_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_sync_twins.py`, `tests/test_export_set.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_edits.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 514 against a baseline of 514
- Kills: 15 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_organize_mirror.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run`
  - `tests/test_organize_mirror.py::test_a_removal_the_account_refuses_is_kept_named_and_the_apply_goes_on`
  - `tests/test_organize_mirror.py::test_a_track_added_by_hand_to_a_mirrored_playlist_is_removed_and_named`
  - `tests/test_organize_mirror.py::test_a_track_moved_from_med_to_high_is_added_to_one_and_removed_from_the_other`
  - `tests/test_organize_mirror.py::test_an_apply_stopped_after_the_folder_was_created_resumes_without_a_second_folder`
  - `tests/test_organize_mirror_edits.py::test_a_folder_that_is_not_a_genre_folder_is_mirrored_one_way`
  - `tests/test_organize_mirror_edits.py::test_a_move_in_rekordbox_after_an_edit_was_taken_is_rekordboxs`
  - `tests/test_organize_mirror_edits.py::test_a_short_playlists_snapshot_advances_so_a_rekordbox_move_is_never_read_as_an_edit`
  - `tests/test_organize_mirror_edits.py::test_an_edit_on_a_playlist_never_agreed_is_put_back_and_nothing_in_the_library_changes`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_rekordbox_move`

Old text:

```
        if recorded:
            return recorded, False
        remote_id = create()
```

New text:

```
        if False:
            return recorded, False
        remote_id = create()
```

### `u309.U5_reserve_written`

A reservation's new identifier is never written to the ledger

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u309.json`, row `U5_reserve_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_sync_twins.py`, `tests/test_export_set.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_edits.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 514 against a baseline of 514
- Kills: 136 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_track_settled_twice_on_a_set_playlist_is_recorded_once`
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_name_with_a_slash_finds_the_set_it_named_at_build`
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_export_set.py::test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match`
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_tidal_list_documents_own_identifiers_are_used_without_a_search`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - ... and 121 more, see the JSON sidecar

Old text:

```
        held[key] = record(remote_id)
        ledger._write(cfg, document)
        return remote_id, True
```

New text:

```
        held[key] = record(remote_id)
        return remote_id, True
```

### `u201-composites.C4_settle_none`

settle_mirror_tracks: the library step settles nothing, the thing L2 narrows

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u201-composites.json`, row `C4_settle_none`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_move_in_rekordbox_after_an_edit_was_taken_is_rekordboxs`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_removed_on_the_account_and_added_nowhere_is_unfiled_and_listed`
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
    wanted = list(settled)
```

New text:

```
    wanted = []
```

### `u201.L1_agreed_own_playlist`

record_mirror_agreed: a snapshot lands on a playlist recorded under the title with another identifier

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u201.json`, row `L1_agreed_own_playlist`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`

Old text:

```
            if not entry or str(entry.get("remote_id") or "") != str(remote_id):
                continue
            base =
```

New text:

```
            if not entry:
                continue
            base =
```

### `u236.M17_ledger_settle_keeps_placement`

ledger settle: a settled track keeps its placement on that title

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u236.json`, row `M17_ledger_settle_keeps_placement`
- Moved: settle_mirror_tracks moved from ledger.py to ledger_settle.py and the kept placements are now named before the _place call; same check reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits_u236.py`
- Collected: 25 against a baseline of 25
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`

Old text:

```
                if str(track) in before:
                    kept = {one: at for one, at in before.items() if one != str(track)}
                    _place(record, name, kept)
                    wrote = True
```

New text:

```
                if False:
                    kept = {one: at for one, at in before.items() if one != str(track)}
                    _place(record, name, kept)
                    wrote = True
```

### `u236.M18_ledger_placement_not_written`

ledger settle: never write a placement

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u236.json`, row `M18_ledger_placement_not_written`
- Moved: the placement write in settle_mirror_tracks moved from ledger.py into ledger_settle.settle_mirror_tracks, with record and name now on one line; the same _place call is deleted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits_u236.py`
- Collected: 25 against a baseline of 25
- Kills: 8 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_survives_the_ledgers_own_read_and_write`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
            _place(
                record, name,
                {**_placements(record.get("placed")).get(str(name), {}), str(track): str(at)},
            )
            wrote = True

```

New text:

```
            wrote = True

```

### `u236.M20_agreed_never_drops`

record_mirror_agreed: never drop a placement the account now holds

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u236.json`, row `M20_agreed_never_drops`
- Moved: record_mirror_agreed moved from ledger.py into ledger_settle.py and reads the mirrored folder's record once into record, so the same placed_after call is written shorter there and is bypassed the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_hand_addition_after_the_placement_is_dropped_is_read_as_one`
  - `tests/test_organize_mirror_edits_u236.py::test_the_organize_after_the_favourite_puts_it_in_the_accounts_month`

Old text:

```
            _place(record, name, mirror_edits.placed_after(
                _placements(record.get("placed")).get(name, {}), after, held
            ))
```

New text:

```
            _place(record, name, _placements(record.get("placed")).get(name, {}))
```

### `u201.M1_plan_keeps`

mirror.plan: removes an account track the hold keeps

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u201.json`, row `M1_plan_keeps`
- Moved: the reused playlist's plan left the body of mirror.plan for the helper mirror._reused, so the same line sits eight spaces shallower; same hold.keep test dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_short_listing_changes_nothing_in_the_library_and_undoes_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_to_its_own_genres_with_vox_is_held_and_nothing_is_written`
  - `tests/test_organize_mirror_edits.py::test_a_track_the_library_lacks_added_on_the_account_is_held_there`
  - `tests/test_organize_mirror_edits.py::test_a_track_whose_file_is_gone_is_named_and_nothing_of_it_is_written`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
    remove = tuple(one for one in names if one not in keep and one not in hold.keep)
```

New text:

```
    remove = tuple(one for one in names if one not in keep)
```

### `u201.M2_plan_skips`

mirror.plan: adds back a track the hold skips

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u201.json`, row `M2_plan_skips`
- Moved: the reused playlist's plan left the body of mirror.plan for the helper mirror._reused, where the comprehension is folded onto one line; same hold.skip test dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_short_listing_changes_nothing_in_the_library_and_undoes_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_to_its_own_genres_with_vox_is_held_and_nothing_is_written`
  - `tests/test_organize_mirror_edits.py::test_a_track_removed_on_the_account_and_added_nowhere_is_unfiled_and_listed`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
            one for one in wanted if one not in on and one not in mine.refused and one not in hold.skip
```

New text:

```
            one for one in wanted if one not in on and one not in mine.refused
```

### `u201.E10_unknown_time`

_later: a time unknown lets the account's move win

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E10_unknown_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[-2026-11-04 10:00:00.000 +00:00]`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[2026-11-04T12:00:00+00:00-]`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[2026-11-04T12:00:00-2026-11-04 10:00:00.000 +00:00]`
  - `tests/test_organize_mirror_edits.py::test_two_moves_with_the_account_time_unknown_keep_rekordboxs`

Old text:

```
    if account_at is None or rekordbox_at is None:
```

New text:

```
    if False:
```

### `u201.E13_snapshot_word`

agreed_after: a held track takes the account's word rather than the snapshot's

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E13_snapshot_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_the_snapshot_after_keeps_its_word_on_a_held_track`
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`

Old text:

```
    before = now if base is None else frozenset(base)
```

New text:

```
    before = now
```

### `u201.E3_own_genre_derived_held`

_intent: a track taken off its band and left in its own genre's with vox is decided as a genre change

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E3_own_genre_derived_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_track_taken_off_its_band_and_put_in_its_own_genres_with_vox_is_held`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_to_its_own_genres_with_vox_is_held_and_nothing_is_written`

Old text:

```
    if removed and not now and folders[0] in {place.folder for place in removed}:
```

New text:

```
    if False:
```

### `u201.E6_short_unread`

decide: a short listing marks nothing unread, so a counted, unlisted track reads as taken off

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E6_short_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_short_favorites_listing_holds_what_it_left_out`
  - `tests/test_mirror_edits.py::test_a_short_listing_carries_no_edit_and_holds_what_it_read_differently`
  - `tests/test_organize_mirror_edits.py::test_a_short_listing_changes_nothing_in_the_library_and_undoes_nothing`

Old text:

```
            unread |= one.agreed - one.account
```

New text:

```
            unread |= set()
```

### `u204.P11_inbox_hold_per_batch`

_holds: an INBOX edit holds every batch rather than its own

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P11_inbox_hold_per_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_an_inbox_edit_holds_its_own_batch_and_no_other`
  - `tests/test_mirror_edits.py::test_an_inbox_track_put_in_joins_and_one_taken_off_leaves`
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_an_inbox_batch_joins_it_and_one_taken_off_leaves_it`
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_inbox_or_favorites_that_the_library_lacks_is_queued`

Old text:

```
            key = one.to.title if one.tree == INBOX and one.to is not None else one.tree
```

New text:

```
            key = one.tree
```

### `u204.P12_favorites_stay`

_holds: a Favorites edit keeps no snapshot word on a playlist the plan finds level

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P12_favorites_stay`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_favorites_edit_planned_and_not_applied_is_taken_whole_by_the_next_run`

Old text:

```
        stay = frozenset(mine) if one.place.tree == FAVORITES else frozenset()
```

New text:

```
        stay = frozenset()
```

### `u204.P2_acquire_only_unknown`

_carry: an addition the library lacks is queued whatever the snapshots held

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P2_acquire_only_unknown`
- Moved: _carry's two held Decisions were folded into one whose acquire flag is computed first, so the same condition now assigns acquire instead of opening an if, and is reverted the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_an_addition_the_library_lacks_is_queued_in_favorites_and_inbox_and_a_known_one_never`
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_a_snapshot_once_held_is_never_queued_again`

Old text:

```
        acquire = kind in ADDITIONS and track not in known
```

New text:

```
        acquire = kind in ADDITIONS
```

### `u230.M13_held_by_dropped`

decide: hand the genre rule no per playlist holders, so the lift never reaches the landed check

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M13_held_by_dropped`
- Moved: decide now builds its decisions in one list, so the _decide_genre call in mirror_edits.py sits four spaces shallower; same holders argument dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 29 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_two_moves_at_one_moment_keep_rekordboxs`
  - `tests/test_mirror_edits.py::test_two_moves_follow_the_account_when_its_is_the_later`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[-2026-11-04 10:00:00.000 +00:00]`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[2026-11-04T12:00:00+00:00-]`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[2026-11-04T12:00:00-2026-11-04 10:00:00.000 +00:00]`
  - `tests/test_mirror_edits_u227.py::test_a_folder_edit_for_a_landed_track_takes_the_folder_over_the_landings_band`
  - `tests/test_mirror_edits_u227.py::test_a_hand_move_back_into_the_landings_band_after_the_edit_was_carried_stands`
  - `tests/test_mirror_edits_u227.py::test_a_landings_own_filing_does_not_beat_the_edit_that_queued_it`
  - `tests/test_mirror_edits_u227.py::test_a_move_made_in_rekordbox_after_the_landing_stands`
  - `tests/test_mirror_edits_u227.py::test_a_second_band_added_in_rekordbox_after_the_landing_stands`
  - `tests/test_mirror_edits_u227.py::test_another_genres_band_of_the_landings_name_is_not_the_landings`
  - `tests/test_mirror_edits_u230.py::test_a_folder_edit_on_a_never_agreed_derived_playlist_is_carried_too`
  - `tests/test_mirror_edits_u230.py::test_a_later_account_move_then_a_rekordbox_move_back_into_the_landings_band_stands`
  - `tests/test_mirror_edits_u230.py::test_a_never_agreed_playlist_whose_account_side_holds_the_track_carries_it`
  - `tests/test_mirror_edits_u230.py::test_another_playlist_the_account_still_lists_it_on_counts_too`
  - ... and 14 more, see the JSON sidecar

Old text:

```
            held_by={track: frozenset(titles) for track, titles in held_by.items()},
```

New text:

```
            held_by=None,
```

### `u236.M1_ours_empty`

decide favorites: read no placement, so the library's own month beats the unfavourite again (sitting 88)

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M1_ours_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 10 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_favourite_both_sides_put_in_another_month_leaves_the_placed_one`
  - `tests/test_mirror_edits_u236.py::test_a_favourite_put_in_another_month_leaves_the_placed_one`
  - `tests/test_mirror_edits_u236.py::test_an_unfavourite_over_the_month_the_library_placed_is_carried`
  - `tests/test_mirror_edits_u236.py::test_the_same_over_a_placed_month_never_agreed`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
        ours = frozenset(
            one.place for one in playlists if not one.place.primary and track in one.placed
        )
```

New text:

```
        ours = frozenset()
```

### `u236.M2_unfavourite_counts_ours`

decide favorites: count a placed month as rekordbox's addition against an UNFAVOURITE

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M2_unfavourite_counts_ours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 7 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_an_unfavourite_over_the_month_the_library_placed_is_carried`
  - `tests/test_mirror_edits_u236.py::test_the_same_over_a_placed_month_never_agreed`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
                if (there_s and not was_s) or (there_m - was_m - ours):
```

New text:

```
                if (there_s and not was_s) or (there_m - was_m):
```

### `u236.M3_moved_counts_ours`

decide favorites: count a placed month as a move of rekordbox's against a FAVOURITE

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M3_moved_counts_ours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_favourite_both_sides_put_in_another_month_leaves_the_placed_one`
  - `tests/test_mirror_edits_u236.py::test_a_favourite_put_in_another_month_leaves_the_placed_one`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`

Old text:

```
                moved = there_m - was_m - ours - {to}
```

New text:

```
                moved = there_m - was_m - {to}
```

### `u236.M5_mine_not_left`

decide favorites: a favourite put in another month keeps the placed month

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M5_mine_not_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_favourite_both_sides_put_in_another_month_leaves_the_placed_one`
  - `tests/test_mirror_edits_u236.py::test_a_favourite_put_in_another_month_leaves_the_placed_one`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`

Old text:

```
            mine = ours - now_m
```

New text:

```
            mine = frozenset()
```

### `u236.M7_placed_after_keeps_all`

placed_after: never drop a placement, so a later hand membership could outlast it

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M7_placed_after_keeps_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_is_dropped_once_the_account_holds_its_track_with_no_hold`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_hand_addition_after_the_placement_is_dropped_is_read_as_one`
  - `tests/test_organize_mirror_edits_u236.py::test_the_organize_after_the_favourite_puts_it_in_the_accounts_month`

Old text:

```
    return {track: at for track, at in placed.items() if track in kept or track not in now}
```

New text:

```
    return dict(placed)
```

### `u236.M8_placed_after_drops_unheld`

placed_after: drop every placement no hold covers, round one's finding 1

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M8_placed_after_drops_unheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_is_dropped_once_the_account_holds_its_track_with_no_hold`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`

Old text:

```
    return {track: at for track, at in placed.items() if track in kept or track not in now}
```

New text:

```
    return {track: at for track, at in placed.items() if track in kept}
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

### `u216.M24_read_unvalidated`

_folders: what a folder held is read without checking it is playlist ids

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M24_read_unvalidated`
- Moved: the held check stays in PairStore._folders but now calls the shared pairs._ids helper the other id checks use; same condition reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_adopted.py`
- Collected: 30 against a baseline of 30
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_folder_whose_held_is_not_ids_refuses_the_document[a]`
  - `tests/test_sync_pair_adopted.py::test_a_folder_whose_held_is_not_ids_refuses_the_document[held1]`
  - `tests/test_sync_pair_adopted.py::test_a_folder_whose_held_is_not_ids_refuses_the_document[held2]`
  - `tests/test_sync_pair_adopted.py::test_a_folder_whose_held_is_not_ids_refuses_the_document[held3]`

Old text:

```
            if held is not None and not _ids(held):
```

New text:

```
            if False:
```

### `u221.R12_hold_not_written`

Pair.to_json: write no hold, so the next read finds none and a twin made since U221 falls to the time rule

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R12_hold_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`
- Collected: 154 against a baseline of 154
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_whose_linked_row_left_the_library_is_still_counted_and_released`
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`
  - `tests/test_sync_twins_hold.py::test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned`
  - `tests/test_sync_twins_hold.py::test_a_released_twin_asks_nothing_the_second_time`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_again_since_the_plan_is_left_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_is_released_by_name_and_counted_by_time`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_an_abort_lets_nothing_go`
  - `tests/test_sync_twins_hold.py::test_release_all_lets_every_twin_go`
  - `tests/test_sync_twins_hold.py::test_release_hold_passes_over_a_pair_that_is_no_twin_and_one_holding_nothing`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args0]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        if self.on_hold is not None:
            record["on_hold"] = dict(sorted(self.on_hold.items()))
```

New text:

```
        if False:
            record["on_hold"] = dict(sorted(self.on_hold.items()))
```

### `u221.R13_hold_not_read`

PairStore._pair: read no hold, so every twin falls to the time rule and a released one is held again

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R13_hold_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`
- Collected: 154 against a baseline of 154
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_whose_linked_row_left_the_library_is_still_counted_and_released`
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`
  - `tests/test_sync_twins_hold.py::test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned`
  - `tests/test_sync_twins_hold.py::test_a_released_twin_asks_nothing_the_second_time`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_again_since_the_plan_is_left_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_is_released_by_name_and_counted_by_time`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_an_abort_lets_nothing_go`
  - `tests/test_sync_twins_hold.py::test_release_all_lets_every_twin_go`
  - `tests/test_sync_twins_hold.py::test_release_hold_passes_over_a_pair_that_is_no_twin_and_one_holding_nothing`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args0]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
            on_hold=None if on_hold is None else MappingProxyType(dict(on_hold)),
```

New text:

```
            on_hold=None,
```

### `u221.R15_mark_drops_the_hold`

PairStore.mark: record no hold on a new pair, so a backfilled twin falls to the time rule

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R15_mark_drops_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 83 against a baseline of 83
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_whose_linked_row_left_the_library_is_still_counted_and_released`
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`
  - `tests/test_sync_twins_hold.py::test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_again_since_the_plan_is_left_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_an_abort_lets_nothing_go`
  - `tests/test_sync_twins_hold.py::test_release_hold_passes_over_a_pair_that_is_no_twin_and_one_holding_nothing`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args0]`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args1]`
  - `tests/test_sync_twins_hold.py::test_releasing_the_twin_queues_its_three_at_the_next_sync`
  - `tests/test_sync_twins_hold.py::test_the_hold_survives_a_recorded_snapshot_and_a_mark_of_the_same_pair`

Old text:

```
                on_hold=(
                    None
                    if on_hold is None
                    else MappingProxyType({str(k): str(v) for k, v in on_hold.items() if k})
                ),
```

New text:

```
                on_hold=None,
```

### `u221.R16_release_any_rekordbox_side`

PairStore.release_hold: drop the rekordbox check, so a twin paired again since the plan is released

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R16_release_any_rekordbox_side`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_again_since_the_plan_is_left_held`

Old text:

```
                    or held.rekordbox_id != str(rekordbox_id)
```

New text:

```
                    or False
```

### `u221.R18_release_writes_nothing`

PairStore.release_hold: never write, so an approved release answers released and the next sync still holds

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R18_release_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`
- Collected: 32 against a baseline of 32
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_released_twin_asks_nothing_the_second_time`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_is_released_by_name_and_counted_by_time`
  - `tests/test_sync_twins_hold.py::test_release_all_lets_every_twin_go`
  - `tests/test_sync_twins_hold.py::test_releasing_the_twin_queues_its_three_at_the_next_sync`

Old text:

```
            if released:
                self._write(pairs)
            return released
```

New text:

```
            return released
```

### `u234.O18_snapshot_keeps_the_reading`

a snapshot that moved keeps the reading after the stop, so it outlives the stop it was read after

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u234.json`, row `O18_snapshot_keeps_the_reading`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_intake_land_twins.py`, `tests/test_outbound_order.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 1786 against a baseline of 1786
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_stopped.py::test_a_reading_after_a_stop_round_trips_and_goes_when_the_snapshot_moves`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
                stop_seen=None if moved else held.stop_seen,
```

New text:

```
                stop_seen=held.stop_seen,
```

### `u234.O19_reading_not_written`

the pair's document never writes the reading after the stop, so a later sync never finds it

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u234.json`, row `O19_reading_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_intake_land_twins.py`, `tests/test_outbound_order.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 1786 against a baseline of 1786
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped.py::test_a_reading_after_a_stop_round_trips_and_goes_when_the_snapshot_moves`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`

Old text:

```
        if self.stop_seen is not None:
            record["stop_seen"] = self.stop_seen.to_json()
```

New text:

```
        if False:
            record["stop_seen"] = self.stop_seen.to_json()
```

### `u201.S1_short_undeclared`

PlaylistListing.short: a listing that declares no count is whole

- File: `src/cratekit/modules/outbound/service.py`
- Source: `u201.json`, row `S1_short_undeclared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_listing_with_no_declared_count_is_short`

Old text:

```
        return self.declared is None or self.listed < self.declared
```

New text:

```
        return self.declared is not None and self.listed < self.declared
```

### `r1017.M10_older_beats_to`

Plan: hold an older name's record ahead of the one under the new name

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r1017.json`, row `M10_older_beats_to`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_is_refused_rather_than_adopted`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old`

Old text:

```
    held = recorded_to or (older[0] if older else None)
```

New text:

```
    held = (older[0] if older else None) or recorded_to
```

### `r1017.M8_first_older_name_only`

Plan: stop at the first older name holding a record, the pre review behaviour

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r1017.json`, row `M8_first_older_name_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`
  - `tests/test_export_set_rename.py::test_two_playlists_under_two_older_names_are_a_twin_not_a_choice`

Old text:

```
        if found is not None and all(found.remote_id != one.remote_id for one in older):
```

New text:

```
        if found is not None and not older:
```

### `r1017.M9_twin_only_beside_to`

Plan: call a twin only when a record under the new name exists, the pre review rule

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r1017.json`, row `M9_twin_only_beside_to`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`
  - `tests/test_export_set_rename.py::test_two_playlists_under_two_older_names_are_a_twin_not_a_choice`

Old text:

```
    twin = next((one for one in older if one.remote_id != held.remote_id), None)
```

New text:

```
    twin = next((one for one in older if recorded_to is not None and one.remote_id != held.remote_id), None)
```

### `u129-author.A17_empty_add_still_writes`

Force writes true when every row of the set is unmatched

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u129-author.json`, row `A17_empty_add_still_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 20 against a baseline of 20
- Kills: 3 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_a_rerun_of_export_set_plans_nothing_when_every_matched_track_is_on_it`
  - `tests/test_u129_set_account_playlist.py::test_a_set_intake_plans_and_makes_the_account_playlist`
  - `tests/test_u129_set_account_playlist.py::test_a_set_with_no_matches_makes_nothing_and_says_so`

Old text:

```
        return bool(self.add)

```

New text:

```
        return True

```

### `u140.A2_new_name_record_ignored`

plan_rename does not look under the new name, so a rerun after the rekey finds nothing recorded

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A2_new_name_record_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_is_refused_rather_than_adopted`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old`

Old text:

```
    recorded_to = ledger.set_playlist(cfg, to) if to else None

```

New text:

```
    recorded_to = None

```

### `u140.A3_refreeze_against_account_spelling`

RenamePlan.refreeze compares the frozen name with the account spelling, not the library's

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A3_refreeze_against_account_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`

Old text:

```
        return self.frozen != (self.live or self.to)

```

New text:

```
        return self.frozen != self.to

```

### `u140.A4_rename_always`

RenamePlan.rename is always true, so a second run renames on the account again

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A4_rename_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`

Old text:

```
        return self.playlist.name != self.to

```

New text:

```
        return True

```

### `u140.A5_ledger_never_rekeyed`

apply_rename retitles on the account and leaves the ledger key where it was

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A5_ledger_never_rekeyed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 9 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_backfill_after_the_rename_plans_no_twin_and_a_named_export_adds_to_it`
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_job_with_no_frozen_name_is_found_by_the_queued_day_and_refrozen`
  - `tests/test_export_set_rename.py::test_a_ledger_left_under_the_old_key_is_moved_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_renamed_inspiration_playlist_renames_the_account_playlist_ledger_and_job`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`
  - `tests/test_export_set_rename.py::test_the_backfill_plans_no_twin_after_a_rename_by_the_landing_record`

Old text:

```
        done.rekeyed = ledger.rename_set_playlist(
            cfg, playlist.name, planned.to, playlist.remote_id
        )

```

New text:

```
        done.rekeyed = False

```

### `u140.A6_refreeze_account_spelling`

apply_rename refreezes the account spelling rather than the INSPIRATION playlist's own name

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A6_refreeze_account_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`

Old text:

```
        refreeze(planned.live or planned.to)

```

New text:

```
        refreeze(planned.to)

```

### `u142.S1_folder_prefix`

sets: drop the Downloaded Sets prefix, so a set is filed into the plain year folder the filing owns

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S1_folder_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 216 against a baseline of 216
- Kills: 13 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_export_set.py::test_the_archive_takes_records_and_files_it_in_a_year_folder_made_once`
  - `tests/test_export_set.py::test_two_folders_named_as_the_year_refuse_and_write_nothing`
  - `tests/test_organize.py::test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year`
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`
  - `tests/test_organize.py::test_a_set_found_prefixed_by_the_migration_is_still_filed_by_the_archive`
  - `tests/test_organize.py::test_a_set_in_its_folder_with_its_built_title_is_taken_and_not_moved`
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`
  - `tests/test_organize.py::test_a_year_record_whose_folder_now_carries_the_sets_name_is_not_the_filings`
  - `tests/test_organize.py::test_no_downloaded_sets_folder_is_made_once_and_the_year_folder_beside_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`

Old text:

```
FOLDER_PREFIX = "Downloaded Sets "
```

New text:

```
FOLDER_PREFIX = ""
```

### `u142.S5_create_under_the_year`

apply_archive: create the folder under the plain year, so a set's folder is made with the filing's name

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S5_create_under_the_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 216 against a baseline of 216
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_archive_takes_records_and_files_it_in_a_year_folder_made_once`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`
  - `tests/test_organize.py::test_an_existing_year_folder_on_the_account_is_adopted_not_made_again`
  - `tests/test_organize.py::test_no_downloaded_sets_folder_is_made_once_and_the_year_folder_beside_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`

Old text:

```
        lambda: account.create_folder(planned.folder_name),
```

New text:

```
        lambda: account.create_folder(planned.year),
```

### `r227.A2_never_stale`

No export is ever stale, which is the tree before this unit

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A2_never_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 372 against a baseline of 372
- Kills: 13 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[export.playlist]`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[sync.favorites]`
  - `tests/test_outbound_workers.py::test_old_means_past_the_limit_and_not_at_it`
  - `tests/test_outbound_workers.py::test_the_date_is_the_persons_own_and_not_greenwichs`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_sentence_does_not_say_seven_is_past_seven`
  - `tests/test_sync_all.py::test_a_pass_that_queued_over_an_old_export_warns_and_still_queues`
  - `tests/test_sync_all.py::test_the_composed_gate_names_the_exports_date_beside_what_would_queue`

Old text:

```
        return age is not None and age.total_seconds() > self.limit_days * _SECONDS_PER_DAY
```

New text:

```
        return False
```

### `r1308.M23_read_back_bypassed`

remove_tracks: take the expected list as read back without reading

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M23_read_back_bypassed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 34 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[as-long-as-before]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[then-wrong]`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[count]`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[whole]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_catches_up_on_the_last_reading_is_taken_as_done`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            playlist, before = self._removal_read_back(identifier, before, expected)
```

New text:

```
            playlist, before = self._playlist(identifier), expected
```

### `r1411.A1_agreed_order_always_stands`

the agreed order check passes every reading, so a reading in the order from before the stopped moves is planned from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A1_agreed_order_always_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 11 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_after_an_add_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading1-agreed1-False]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading5-agreed5-False]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading7-agreed7-False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
    return [one for one in dict.fromkeys(reading) if one in named] == [
        one for one in dict.fromkeys(str(one) for one in agreed) if one in held
    ]
```

New text:

```
    return bool(named or held or True)
```

### `r1411.A3_added_tracks_asked_of_the_agreed_order`

the agreed order check reads every track of the reading, so a track this write added refuses the finish

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A3_added_tracks_asked_of_the_agreed_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading10-agreed10-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading2-agreed2-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading3-agreed3-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading4-agreed4-True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`

Old text:

```
    return [one for one in dict.fromkeys(reading) if one in named] == [
```

New text:

```
    return [one for one in dict.fromkeys(reading)] == [
```

### `r836-a.A1_product_made_asked_first`

tidal_account.remove_tracks: the ledger is never asked, so a playlist the product did not create loses tracks

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r836-a.json`, row `A1_product_made_asked_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_organize_root.py`, `tests/test_sync_pair_account.py`
- Collected: 112 against a baseline of 112
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_heard.py::test_the_adapter_refuses_a_playlist_the_ledger_does_not_vouch_for_unasked`
  - `tests/test_organize_root.py::test_the_generic_removal_still_refuses_an_unrecorded_playlist`
  - `tests/test_sync_pair_account.py::test_a_paired_playlist_is_never_removed_whole`

Old text:

```
        if self._cfg is None or not ledger.product_made(self._cfg, identifier):
```

New text:

```
        if False:
```

### `u130-c.C6_pair_not_vouched`

The account seam refuses a removal from a paired playlist

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u130-c.json`, row `C6_pair_not_vouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_account.py`, `tests/test_prune.py`
- Collected: 67 against a baseline of 67
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_account.py::test_a_move_that_landed_elsewhere_is_left_to_the_settle_reading_with_every_track_kept`
  - `tests/test_sync_pair_account.py::test_a_paired_playlist_takes_a_removal`
  - `tests/test_sync_pair_account.py::test_a_track_held_twice_is_not_moved`
  - `tests/test_sync_pair_account.py::test_an_order_already_standing_sends_nothing`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`

Old text:

```
            ledger.product_made(self._cfg, identifier) or pairs.paired(self._cfg, identifier)
```

New text:

```
            ledger.product_made(self._cfg, identifier)
```

### `u220.A1_front_target`

order_tracks: move each track to the playlist's length instead of the front, the move whose landing depends on how the provider counts

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A1_front_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
- Kills: 12 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_every_move_is_to_the_front_where_both_ways_of_counting_agree`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`
  - `tests/test_outbound_order.py::test_the_tracks_before_the_kept_tail_are_moved_last_first`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`

Old text:

```
playlist.move_by_indices([at], 0)
```

New text:

```
playlist.move_by_indices([at], len(before))
```

### `u231.M5_positions_not_advanced`

adapter order: each move's position is read off the reading as it was, not with the moves before it applied

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M5_positions_not_advanced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
- Kills: 38 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading`
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_move_that_lands_anywhere_else_is_not_read_back_and_the_settle_reading_shows_it`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_holding_what_the_adds_left_in_another_order_is_not_stale`
  - `tests/test_outbound_order.py::test_a_reading_that_agrees_with_the_expected_one_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_expected_one_is_read_again`
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before0-order0]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before1-order1]`
  - ... and 23 more, see the JSON sidecar

Old text:

```
            now = _fronted(now, one)
            note["moved"] += 1
```

New text:

```
            note["moved"] += 1
```

### `u206.M17_account_hit_ignored`

TidalAccount._isrc_tracks: never use a remembered answer

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u206.json`, row `M17_account_hit_ignored`
- Moved: Anchored where u309-replay-after-e.json replayed it: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1131 against a baseline of 1131
- Kills: 13 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_choice_among_several_releases_is_made_from_a_remembered_answer_with_no_call`
  - `tests/test_isrc_cache.py::test_a_copy_run_redirecting_installation_state_shares_answers_through_the_override`
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_second_account_over_a_fresh_client_asks_nothing_for_an_answered_isrc`
  - `tests/test_isrc_cache.py::test_a_tie_remembered_is_still_refused_with_its_reason`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_the_catalogue_and_the_account_share_one_answer`
  - `tests/test_isrc_cache.py::test_the_process_counts_say_what_the_cache_settled_and_what_was_asked`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`

Old text:

```
        if held is not None:
            return held if held else _ABSENT
        # What the LAST attempt said
```

New text:

```
        if False:
            return held if held else _ABSENT
        # What the LAST attempt said
```

### `u208.M19_adapter_never_records_tie`

match_track: never record a broken tie

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u208.json`, row `M19_adapter_never_records_tie`
- Moved: Anchored where u309-replay-after-c.json replayed it: match_track moved from tidal_account.py into the Reads mixin in tidal_reads.py and its ISRC lookup lost a level of nesting; same branch reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 134 against a baseline of 134
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - `tests/test_sync_pair_tie.py::test_two_hearted_releases_take_the_lower_hearted_one`

Old text:

```
                elif tied:
                    self._ties.add(key)
```

New text:

```
                elif False:
                    self._ties.add(key)
```

### `r388-c.M17_slug_respelled`

Respell the enum value, so the engine raises a slug nothing reserved

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r388-c.json`, row `M17_slug_respelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-identity]`
  - `tests/modules/test_tools.py::test_every_refusal_cause_has_a_reserved_exit_code`
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
    SNAPSHOT_LISTING_FAILED = "snapshot-listing-failed"
```

New text:

```
    SNAPSHOT_LISTING_FAILED = "snapshot-listing-error"
```

### `u211.B1_backup_database_portion_refuses_alone`

backup _plan_database: let the unconfirmed refusal escape the plan, so the files portion is lost with the database portion

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `u211.json`, row `B1_backup_database_portion_refuses_alone`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_backup_cli.py`, `tests/test_analysis_store.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_backup_refuses_the_database_portion_alone_and_still_mirrors`

Old text:

```
    except AbsenceUnconfirmed as exc:
        return PortionPlan(
```

New text:

```
    except LookupError as exc:
        return PortionPlan(
```

### `u27-restore-cli-independent.X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore`

What the from-backup zeros DO leave held: remove the refusal that stops a restore with no recorded decision, in the backup module the verb calls. Paired with I_A1 and with the whole from-backup family of zeros, which are one hole rather than eleven

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `u27-restore-cli-independent.json`, row `X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 431 against a baseline of 431
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_restore_is_a_named_decision_and_never_a_prompt`
  - `tests/test_write_session.py::test_the_restore_is_the_recovery_and_reaches_its_own_refusals`
  - `tests/test_write_session.py::test_the_restores_own_refusals_survive_the_gates_being_added`

Old text:

```
    if not confirmed:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
            "a restore replaces the live database and is not performed without an "
            "explicit decision naming this library and this snapshot.",
        )
```

New text:

```
(empty)
```

### `r187-a.A10_ambiguous_falls_through`

resolve_anchor: only a partial reach answers unresolved, so an ambiguous name falls through to not in your library

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A10_ambiguous_falls_through`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_engine_says_ambiguous_and_never_not_in_your_library`

Old text:

```
    if matched.track is None and matched.candidates and not (matched.partial and key):
```

New text:

```
    if matched.track is None and matched.partial and not key:
```

### `r187-a.A11_no_cutoff`

match_in_index: score cutoff to zero, so a name nothing answers to reaches the whole index

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A11_no_cutoff`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_web_lookup_is_a_seam_that_is_absent_by_default`
  - `tests/test_setbuilder_cli.py::test_a_name_longer_than_the_owned_title_is_refused_and_not_shortened`
  - `tests/test_setbuilder_cli.py::test_a_name_nothing_answers_to_is_not_indexed_and_not_ambiguous`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[named-not-indexed]`

Old text:

```
        score_cutoff=threshold,
```

New text:

```
        score_cutoff=0,
```

### `r187-a.A12_partial_message`

resolve_anchor: a partial reach uses the several owned tracks sentence, which is false when one was reached

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A12_partial_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_remix_the_library_lacks_is_unowned_once_its_key_is_supplied`

Old text:

```
        if matched.partial:
            why = (
```

New text:

```
        if False:
            why = (
```

### `r187-a.A1_exact_first`

match_in_index: never find an exact hit, so an exact name falls to the fuzzy score that cannot separate it from a longer title

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A1_exact_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_exact_name_is_never_lost_to_a_longer_title_whichever_came_first`
  - `tests/test_setbuilder_cli.py::test_what_plays_after_a_track_is_asked_by_name`

Old text:

```
    exact = [t for t in index if t.match == wanted]
```

New text:

```
    exact = []
```

### `r187-a.A3_holds_dropped`

match_in_index: count every hit at the threshold as holding the name, so one differing word in a long title resolves

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A3_holds_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_file_with_no_artist_tag_is_reachable_by_the_name_the_refusal_lists`
  - `tests/test_setbuilder_cli.py::test_a_name_longer_than_the_owned_title_is_refused_and_not_shortened`
  - `tests/test_setbuilder_cli.py::test_a_remix_the_library_lacks_is_unowned_once_its_key_is_supplied`
  - `tests/test_setbuilder_cli.py::test_one_differing_word_in_a_long_title_is_a_different_version`

Old text:

```
    holding = tuple(t for t in ordered if _holds_every_word(t.match, wanted))
```

New text:

```
    holding = ordered
```

### `r187-a.A5_word_threshold_high`

WORD_THRESHOLD 80 to 95, so a slip of the finger no longer lands

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A5_word_threshold_high`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_typed_short_resolves_when_only_one_track_answers_to_it`

Old text:

```
WORD_THRESHOLD = 80
```

New text:

```
WORD_THRESHOLD = 95
```

### `r187-a.A6_first_of_several`

match_in_index: resolve to the first of several holding hits instead of listing them, the defect itself

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A6_first_of_several`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_that_reaches_two_versions_lists_both_and_picks_neither`
  - `tests/test_setbuilder_cli.py::test_an_ambiguous_name_refuses_through_the_dispatcher_and_lists_the_paths`
  - `tests/test_setbuilder_cli.py::test_the_engine_says_ambiguous_and_never_not_in_your_library`
  - `tests/test_setbuilder_cli.py::test_the_listing_is_capped_and_says_how_many_it_reached`

Old text:

```
    if len(holding) == 1:
        return AnchorMatch(track=holding[0])
```

New text:

```
    if holding:
        return AnchorMatch(track=holding[0])
```

### `r187-a.A7_partial_never`

match_in_index: never report a partial reach, so a different version reads as a choice between owned tracks

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A7_partial_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_longer_than_the_owned_title_is_refused_and_not_shortened`
  - `tests/test_setbuilder_cli.py::test_a_remix_the_library_lacks_is_unowned_once_its_key_is_supplied`
  - `tests/test_setbuilder_cli.py::test_one_differing_word_in_a_long_title_is_a_different_version`

Old text:

```
    return AnchorMatch(candidates=ordered, partial=bool(ordered))
```

New text:

```
    return AnchorMatch(candidates=ordered, partial=False)
```

### `r187-a.A8_walk_order`

match_in_index: order candidates by score alone, so the listing follows the filesystem walk

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A8_walk_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_that_reaches_two_versions_lists_both_and_picks_neither`

Old text:

```
            hits, key=lambda hit: (-hit[1], index[hit[2]].match, index[hit[2]].path)
```

New text:

```
            hits, key=lambda hit: -hit[1]
```

### `r187-a.A9_key_discarded`

resolve_anchor: a partial reach with a supplied key answers unresolved, discarding the key

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A9_key_discarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_remix_the_library_lacks_is_unowned_once_its_key_is_supplied`

Old text:

```
    if matched.track is None and matched.candidates and not (matched.partial and key):
```

New text:

```
    if matched.track is None and matched.candidates:
```

### `r187-b.B12_not_carried_forward`

build_index: a current entry is served and not carried into the next cache, so every other run is a full scan

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B12_not_carried_forward`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_second_run_reads_no_tag_it_already_holds`

Old text:

```
            track = _track_from_cache(entry.get("track"))
            fresh[key] = entry
```

New text:

```
            track = _track_from_cache(entry.get("track"))
```

### `u266.M1_seven_opens_again`

read_index_tags: go back to one read_tag call per field, seven opens a file, the regression the card removes

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u266.json`, row `M1_seven_opens_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_one_open.py`, `tests/test_setbuilder_cli.py`, `tests/modules/test_tools.py`
- Collected: 325 against a baseline of 325
- Kills: 52 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_first_run_opens_each_file_once_and_the_second_none`
  - `tests/test_setbuilder_one_open.py::test_a_file_one_open_cannot_read_reads_all_absent_and_never_raises`
  - `tests/test_setbuilder_one_open.py::test_an_undecodable_field_reads_none_and_its_neighbours_still_read`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.aif]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.aiff]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.flac]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.m4a]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.mp3]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.ogg]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.opus]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.wav]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.aif]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.aiff]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.flac]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.m4a]`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    return tags.read_tags(path, INDEX_FIELDS)
```

New text:

```
    return {name: tags.read_tag(path, name) for name in INDEX_FIELDS}
```

### `u279.M12_holder_never_found`

Exclusion.holder: answer None for every path, so no anchor is placed in an excluded folder

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M12_holder_never_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[state]`

Old text:

```
            if identity in self.folders:
                return self.folders[identity]
```

New text:

```
            if False:
                return self.folders[identity]
```

### `u279.M1_walk_ignores_exclude`

iter_audio: walk the whole root again, sorted(root.rglob), so the excluded folders are indexed (the defect itself)

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M1_walk_ignores_exclude`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 10 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_a_staging_copy_never_takes_the_library_files_place`
  - `tests/test_setbuilder_excluded.py::test_an_earlier_cache_entry_under_an_excluded_folder_is_not_served`
  - `tests/test_setbuilder_excluded.py::test_an_excluded_folder_is_matched_by_location_whatever_its_spelling`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`
  - `tests/test_setbuilder_excluded.py::test_the_excluded_walk_is_todays_walk_less_the_excluded_folders`

Old text:

```
    for candidate in sorted(Exclusion.under(root, exclude).walk(root)):
```

New text:

```
    for candidate in sorted(root.rglob("*")):
```

### `u279.M2_excluded_folder_walked`

Exclusion.walk: drop the skip of an excluded folder, so the hand walk yields it and its contents

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M2_excluded_folder_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 10 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_a_staging_copy_never_takes_the_library_files_place`
  - `tests/test_setbuilder_excluded.py::test_an_earlier_cache_entry_under_an_excluded_folder_is_not_served`
  - `tests/test_setbuilder_excluded.py::test_an_excluded_folder_is_matched_by_location_whatever_its_spelling`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`
  - `tests/test_setbuilder_excluded.py::test_the_excluded_walk_is_todays_walk_less_the_excluded_folders`

Old text:

```
            if identity in self.folders:
                continue
            yield child
```

New text:

```
            yield child
```

### `u279.M3_ancestor_taken_whole`

Exclusion.walk: hand an ancestor of an excluded folder to rglob whole, so a nested excluded folder is walked

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M3_ancestor_taken_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_the_excluded_walk_is_todays_walk_less_the_excluded_folders`

Old text:

```
            if identity in self.ancestors:
```

New text:

```
            if False:
```

### `u279.M4_symlink_followed`

Exclusion.walk: read a symlinked folder on the hand walked path as a directory, so it is descended where rglob does not

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M4_symlink_followed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_the_excluded_walk_is_todays_walk_less_the_excluded_folders`

Old text:

```
                if entry.is_dir(follow_symlinks=False):
```

New text:

```
                if entry.is_dir():
```

### `u279.M5_unlistable_raises`

Exclusion.walk: catch only a missing folder, so one the walk cannot list stops the index where rglob passes it over

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M5_unlistable_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_folder_the_walk_cannot_list_is_passed_over_as_today`

Old text:

```
                entries = list(listing)
        except OSError:
            return
```

New text:

```
                entries = list(listing)
        except FileNotFoundError:
            return
```

### `u279.M6_chain_unresolved`

_chain_to: read the configured folder as spelled, so a staging folder configured through a link outside the root excludes nothing

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M6_chain_unresolved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_excluded_folder_is_matched_by_location_whatever_its_spelling`

Old text:

```
        current = folder.resolve()
```

New text:

```
        current = folder.absolute()
```

### `u279.M7_outermost_folder_excluded`

Exclusion.under: exclude the outermost folder above a configured one rather than the folder itself, so its library siblings are dropped

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M7_outermost_folder_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_the_excluded_walk_is_todays_walk_less_the_excluded_folders`

Old text:

```
                folders.setdefault(chain[0], Path(folder))
```

New text:

```
                folders.setdefault(chain[-1], Path(folder))
```

### `u311.C8_unreadable_number_raises`

A tag that is not a number raises instead of reading as absent

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u311.json`, row `C8_unreadable_number_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_one_open.py`
- Collected: 340 against a baseline of 340
- Kills: 44 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[list]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[text]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[track-missing-fields]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[track-not-a-mapping]`
  - `tests/modules/test_tools.py::test_a_cache_from_another_build_or_with_no_template_stamp_is_discarded[other-build]`
  - `tests/modules/test_tools.py::test_a_cache_from_another_build_or_with_no_template_stamp_is_discarded[unstamped]`
  - `tests/modules/test_tools.py::test_a_cache_parsed_under_another_template_is_discarded`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[bpm-124]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[energy-True]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[title-None]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[vox-value2]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[voxgender-4]`
  - `tests/modules/test_tools.py::test_a_headless_title_takes_the_key_adopt_writes_and_no_tempo`
  - `tests/modules/test_tools.py::test_a_marked_lossy_title_loses_its_marker_along_with_the_head`
  - `tests/modules/test_tools.py::test_a_read_that_returned_nothing_is_never_cached_as_the_files_answer`
  - ... and 29 more, see the JSON sidecar

Old text:

```
    except (TypeError, ValueError):
        return None
```

New text:

```
    except TypeError:
        return None
```

### `u311.C9_anchor_comes_back`

The anchor is no longer excluded from its own pool by match key

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u311.json`, row `C9_anchor_comes_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_one_open.py`
- Collected: 340 against a baseline of 340
- Kills: 13 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_set_builder_produces_a_sequence_from_a_snapshot_index`
  - `tests/test_setbuilder_cli.py::test_a_cache_that_cannot_be_written_does_not_cost_the_set`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_a_path_anchor_is_unchanged_by_the_unowned_form`
  - `tests/test_setbuilder_cli.py::test_every_recommendation_came_out_of_the_index`
  - `tests/test_setbuilder_cli.py::test_one_either_companion_of_an_owned_anchor_is_placed_once`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
        if anchor_match and track.match == anchor_match:
```

New text:

```
        if False:
```

### `u43-author-light.E1_anchor_is_its_own_companion`

build_pool stops excluding the anchor by match key, so the best companion for a track is itself

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u43-author-light.json`, row `E1_anchor_is_its_own_companion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 8 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_set_builder_produces_a_sequence_from_a_snapshot_index`
  - `tests/test_setbuilder_cli.py::test_a_cache_that_cannot_be_written_does_not_cost_the_set`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_a_path_anchor_is_unchanged_by_the_unowned_form`
  - `tests/test_setbuilder_cli.py::test_every_recommendation_came_out_of_the_index`
  - `tests/test_setbuilder_cli.py::test_one_either_companion_of_an_owned_anchor_is_placed_once`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`

Old text:

```
        if anchor_match and track.match == anchor_match:
            continue
```

New text:

```
        if anchor_match and track.match != anchor_match:
            pass
```

### `u43-author-light.E3_tempo_serialized_as_bpm`

as_payload spells the tempo key the way the Vorbis tag dialect does, which is one splat from handing a tempo to a tag writer and seeding a grid at half or double time (R17)

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u43-author-light.json`, row `E3_tempo_serialized_as_bpm`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_structured_payload_carries_a_version`
  - `tests/test_setbuilder_cli.py::test_a_supplied_tempo_narrows_an_unowned_anchor_to_its_band`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_is_ranked_through_the_dispatcher`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`

Old text:

```
            "tempo": plan.anchor.bpm,
```

New text:

```
            "bpm": plan.anchor.bpm,
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

### `u174.O3_no_pass_counted`

_mark_steps: drop the fact counting native landings of no sync pass

- File: `src/cratekit/organize/account.py`
- Source: `u174.json`, row `O3_no_pass_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_landing_of_no_sync_pass_is_counted_and_is_no_step`

Old text:

```
        area.facts["native landings of no sync pass"] = unlanded
```

New text:

```
        pass
```

### `u174.O4_no_pass_is_no_step`

_mark_step: a pass that is no sync pass's is planned as a step with nothing to mark

- File: `src/cratekit/organize/account.py`
- Source: `u174.json`, row `O4_no_pass_is_no_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_landing_of_no_sync_pass_is_counted_and_is_no_step`

Old text:

```
    if not planned.of_a_pass:
        return False
```

New text:

```
    if False:
        return False
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

### `u204.A1_adopt_landed`

_read_edits: a landed row tied by its ISRC is not answered as the track the account holds

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u204.json`, row `A1_adopt_landed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_landed_track_the_provider_ties_to_another_release_is_still_filed`

Old text:

```
            matcher.adopt(content_id, remote)
```

New text:

```
            pass
```

### `u222.M11_decided_freeze_shown`

_record: freeze a decided run's fresh plan as shown by its gate (review round one's BLOCKING)

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M11_decided_freeze_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_decided_run_with_no_frozen_plan_says_it_planned_afresh`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_plan_made_afresh_by_a_decided_run_is_never_read_as_what_the_gate_showed`

Old text:

```
            shown=not run.decided,
```

New text:

```
            shown=True,
```

### `u222.M12_unshown_not_said`

_stale: read a record no gate showed as one it did

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M12_unshown_not_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_plan_made_afresh_by_a_decided_run_is_never_read_as_what_the_gate_showed`

Old text:

```
    if frozen is not None and not frozen.shown:
```

New text:

```
    if False:
```

### `u222.M19_stale_on_every_run`

add_steps: carry stale lines on a gate's own run too

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M19_stale_on_every_run`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_the_gate_run_and_a_report_say_nothing_stale`

Old text:

```
    if run is not None and run.decided:
        area.stale.extend
```

New text:

```
    if run is not None:
        area.stale.extend
```

### `u222.M1_overlay_not_read`

read: never overlay the frozen snapshots, so the decided run reads the ledger's live snapshot as before U222 (sitting 66)

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M1_overlay_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_genre_edit_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_join_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_leave_the_library_took_between_the_acts_applies_the_approved_plan`

Old text:

```
    if frozen is not None:
        # THE GATE'S SNAPSHOTS
```

New text:

```
    if False:
        # THE GATE'S SNAPSHOTS
```

### `u222.M20_every_step_reworded`

_stale: reword the line said when nothing moved

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M20_every_step_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_write_outside_any_mirrored_playlist_between_the_acts_is_not_stale`
  - `tests/test_organize_mirror_frozen_u222.py::test_with_nothing_between_the_acts_the_apply_rebuilds_the_frozen_plan`

Old text:

```
            else "every step plans as the gate showed it"
```

New text:

```
            else "every step plans as its gate showed it"
```

### `u222.M25_steps_not_frozen`

_record: freeze no step, so a stale answer names every step as one the gate did not show

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M25_steps_not_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_the_gate_freezes_every_step_of_the_full_account_area`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_write_outside_any_mirrored_playlist_between_the_acts_is_not_stale`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_account_change_between_the_acts_is_stale_and_names_its_folder_and_playlist`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`
  - `tests/test_organize_mirror_frozen_u222.py::test_with_nothing_between_the_acts_the_apply_rebuilds_the_frozen_plan`

Old text:

```
            steps=area.steps,
```

New text:

```
            steps=(),
```

### `u236.M10_reader_no_time_check`

read edits: hand the rule every recorded placement, whatever membership holds it (round one, finding 2)

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u236.json`, row `M10_reader_no_time_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_membership_a_person_took_off_and_put_back_by_hand_is_theirs`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_deleted_and_made_again_by_hand_is_a_persons_addition[False]`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_deleted_and_made_again_by_hand_is_a_persons_addition[True]`

Old text:

```
                remote for remote, at in recorded_placed.items() if at and added.get(remote) == at
```

New text:

```
                remote for remote, at in recorded_placed.items() if at
```

### `u236.M11_reader_never_placed`

read edits: hand the rule no placement on a playlist never mirrored, the month the write made

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u236.json`, row `M11_reader_never_placed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
                read.append(edits.Mirrored(place=place, rekordbox=frozenset(wanted), placed=ours))
```

New text:

```
                read.append(edits.Mirrored(place=place, rekordbox=frozenset(wanted)))
```

### `u236.M12_reader_short_branch`

read edits: drop the placements of a month whose listing failed (round one, finding 4)

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u236.json`, row `M12_reader_short_branch`
- Moved: the reader's two Mirrored constructions, one for a failed listing and one for a read listing, were merged into one that tests listing is None per field, so dropping the failed listing's placements is now placed left empty only when listing is None
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`

Old text:

```
                rekordbox_added=added,
                placed=ours,
```

New text:

```
                rekordbox_added=added,
                placed=ours if listing is not None else frozenset(),
```

### `u309-z2.U21_reading_unread_listed`

A rekordbox area step over an unread reading is planned instead of listed

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u309-z2.json`, row `U21_reading_unread_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_reading_whose_edits_went_unread_lists_the_step_and_says_why`

Old text:

```
    if reading.unread:
        return Step(key=kind, title=title, state=LISTED, detail=reading.unread)
    return reading
```

New text:

```
    return reading
```

### `u309-z2.U22_keep_newest_time`

The newest of two membership times is replaced by the older

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u309-z2.json`, row `U22_keep_newest_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_of_two_membership_times_for_one_track_the_newest_is_kept`

Old text:

```
    if at is not None and (held is None or at > held):
```

New text:

```
    if at is not None and (held is None or at < held):
```

### `u242.M23_filing_dates_a_found_prefix`

filing: read a taken entry the migration found as a dated mark, filing it by the migration's year

- File: `src/cratekit/organize/filing.py`
- Source: `u242.json`, row `M23_filing_dates_a_found_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_organize_root.py`, `tests/test_organize.py`
- Collected: 198 against a baseline of 198
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_root.py::test_filing_reads_a_stripped_hand_mark_as_it_read_the_prefixed_one`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_filing_reads_a_found_prefix_as_undated_and_a_pass_mark_as_dated`

Old text:

```
        if entry.held and entry.dated:
```

New text:

```
        if entry.held:
```

### `r1289.M14_mirror_unread_branch`

mirror_downloads.plan: drop the unread branch, so an unread wanted track is named as one the provider did not list

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `r1289.json`, row `M14_mirror_unread_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_untitled_track_on_a_mirrored_playlist_is_named_and_the_others_queue`

Old text:

```
            if track in unread:
```

New text:

```
            if False:
```

### `r1289.M15_mirror_reads_whole`

mirror_downloads._catalogue_listing: read the playlist whole again (the declared reader is asked first), so one untitled row names every wanted track on it

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `r1289.json`, row `M15_mirror_reads_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_untitled_track_on_a_mirrored_playlist_is_named_and_the_others_queue`

Old text:

```
        return intake_cli.list_playlist_readable(found[0], playlist_id)
```

New text:

```
        intake_cli.list_playlist_declared(found[0], playlist_id)
        return intake_cli.list_playlist_readable(found[0], playlist_id)
```

### `r1289.M16_mirror_why`

mirror_downloads.plan: the unread track's why reworded so it does not carry the reader's words

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `r1289.json`, row `M16_mirror_why`
- Moved: the unread track's line stays in mirror_downloads.plan, whose named entry is now written on fewer lines, so the same words sit eight spaces shallower; same rewording
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_untitled_track_on_a_mirrored_playlist_is_named_and_the_others_queue`

Old text:

```
                    f"added on the account, but {unread[track].why}, so the "
```

New text:

```
                    f"added on the account, but it could not be read, so the "
```

### `r1289.M17_mirror_listing_refusal`

mirror_downloads.plan (existing guard, sample): a playlist the provider cannot list names nothing for its tracks

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `r1289.json`, row `M17_mirror_listing_refusal`
- Moved: the not queued entry mirror_downloads.plan names for a playlist the provider cannot list is now built by the shared _not_queued helper instead of an inline dict; the same loop over its tracks is emptied
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_playlist_the_provider_cannot_list_is_named_and_the_others_queue`

Old text:

```
                _not_queued(track, title, f"the provider could not list the playlist: {exc.cause.message}")
                for track in sorted(set(tracks))

```

New text:

```
                _not_queued(track, title, f"the provider could not list the playlist: {exc.cause.message}")
                for track in ()

```

### `u204.D1_one_queue_per_track`

mirror_downloads.plan: a track two playlists want is queued twice

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u204.json`, row `D1_one_queue_per_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_inbox_or_favorites_that_the_library_lacks_is_queued`

Old text:

```
        if decision.track in taken:
```

New text:

```
        if False:
```

### `u204.D2_write_rereads_queue`

mirror_downloads.write: two plans approved one after the other queue a track twice

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u204.json`, row `D2_write_rereads_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_two_plans_approved_one_after_the_other_queue_a_track_once`

Old text:

```
            fresh = {track: frozen for track, frozen in tracks.items() if track not in already}
```

New text:

```
            fresh = dict(tracks)
```

### `u204.D3_owned_recording`

mirror_downloads.plan: another release of an owned recording is queued

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u204.json`, row `D3_owned_recording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_recording_the_library_holds_in_no_playlist_is_never_queued`
  - `tests/test_organize_mirror_edits_u204.py::test_another_release_of_an_owned_recording_is_never_queued_nor_swapped`

Old text:

```
            rows = owned(frozen[track].get("isrc")) if track in frozen else ()
```

New text:

```
            rows = ()
```

### `u204.D4_never_lands_named`

mirror_downloads.outcomes: a finished download that found the track owned is said to await its landing

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u204.json`, row `D4_never_lands_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_finished_download_that_never_lands_is_never_said_to_await_one[missing-could not be fetched]`
  - `tests/test_organize_mirror_edits_u204.py::test_a_finished_download_that_never_lands_is_never_said_to_await_one[owned-already holds it]`

Old text:

```
                why = _NEVER_LANDS.get(str(report.get("state")))
```

New text:

```
                why = None
```

### `u230.M15_source_blank`

queued_from: name no source for any job

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u230.json`, row `M15_source_blank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 6 (killed)
- Killed:
  - `tests/test_mirror_downloads_queued_from_u230.py::test_a_cancelled_job_another_source_and_another_library_name_nothing`
  - `tests/test_mirror_downloads_queued_from_u230.py::test_each_track_is_named_with_every_playlist_whose_job_queued_it`
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_job_queued_from_another_playlist_does_not_lift_the_edited_ones_base`
  - `tests/test_organize_mirror_edits_u230.py::test_a_move_in_rekordbox_after_the_carry_still_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it`

Old text:

```
            held.setdefault(str(remote), set()).add(source)
```

New text:

```
            held.setdefault(str(remote), set()).add("")
```

### `u230.M16_unread_raises`

queued_from: a queue that cannot be read raises, stopping the organize

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u230.json`, row `M16_unread_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_downloads_queued_from_u230.py::test_a_queue_that_cannot_be_read_names_nothing`

Old text:

```
    except (CratekitError, OSError, ValueError):
        return {}
    held: dict[str, set[str]] = {}
```

New text:

```
    except (CratekitError, OSError, ValueError):
        raise
    held: dict[str, set[str]] = {}
```

### `u267.M13_downloads_owned_opens_its_own`

mirror_downloads.plan: hand no shared read to the ISRC read, which then opens its own handle in the report

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u267.json`, row `M13_downloads_owned_opens_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_one_read.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_the_downloads_plan_reads_the_library_through_a_reports_one_handle`

Old text:

```
        owned = _owned(cfg, reading, one_read)
```

New text:

```
        owned = _owned(cfg, reading)
```

### `r1950.M02_identity_drops_second`

mirror edits: a change's identity, and so the step digest an approval binds, no longer carries the second genre

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `r1950.json`, row `M02_identity_drops_second`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre_guards_mirror.py`, `tests/test_second_genre.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre_guards_mirror.py::test_two_changes_differing_only_in_the_second_genre_have_different_identities`

Old text:

```
            *([[self.second_was, self.second]] if self.second_was or self.second else []),

```

New text:

```
(empty)
```

### `r1950.M03_write_skips_second_read_back`

mirror edits: the write no longer reads the second genre back, so one that did not take reports success

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `r1950.json`, row `M03_write_skips_second_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre_guards_mirror.py`, `tests/test_second_genre.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_second_genre_guards_mirror.py::test_a_second_genre_the_clearer_skips_fails_the_read_back`
  - `tests/test_second_genre_guards_mirror.py::test_a_second_genre_the_writer_drops_fails_the_read_back`

Old text:

```
        and tags.read_energy_from_file(path) == change.energy
        and (tags.read_tag(path, "secondgenre") or None) == (change.second or None)

```

New text:

```
        and tags.read_energy_from_file(path) == change.energy

```

### `r1950.M04_item_hides_second`

mirror edits: the gate item of a two genre change no longer shows the second genre before and after

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `r1950.json`, row `M04_item_hides_second`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre_guards_mirror.py`, `tests/test_second_genre.py`, `tests/test_organize_mirror_edits_u340.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_second_genre_guards_mirror.py::test_an_unfile_of_a_two_genre_track_clears_its_second_genre`
  - `tests/test_second_genre_guards_mirror.py::test_the_item_of_a_two_genre_change_shows_both_second_genres`

Old text:

```
            if self.second_was or self.second:
                shown["second genre"] = [self.second_was, self.second]

```

New text:

```
(empty)
```

### `u201-composites.C5_leave_nothing`

plan: a move leaves no tree playlist, the thing O4 narrows

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201-composites.json`, row `C5_leave_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_library_moved_since_the_plan_writes_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_mirror_made_before_u201_is_agreed_by_its_first_run_and_an_edit_after_it_is_taken`
  - `tests/test_organize_mirror_edits.py::test_a_move_to_unsorted_clears_the_energy`
  - `tests/test_organize_mirror_edits.py::test_a_move_within_a_genre_keeps_the_genre_and_moves_the_energy_to_the_nearest`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
            leave_ids = [pid for pid in held if pid not in wanted and routed(tree.names[pid])]
```

New text:

```
            leave_ids = []
```

### `u201.O1_latch`

write: the tree's convergence latch is not asked

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O1_latch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_tree_the_product_latched_refuses_the_write_before_any_file_is_tagged`

Old text:

```
        convergence.assert_tree_writable(cfg, db, tree_id, registry)
```

New text:

```
        pass
```

### `u201.O2_stale`

_stale: a library moved since the plan is written

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O2_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_library_moved_since_the_plan_writes_nothing`

Old text:

```
    if approved.identity() != now.identity():
```

New text:

```
    if False:
```

### `u201.O3_target_bucket`

target_tags: a genre word filing into another bucket is taken

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O3_target_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 187 against a baseline of 187
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_mirror_made_before_u201_is_agreed_by_its_first_run_and_an_edit_after_it_is_taken`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_the_tags_are_the_nearest_pair_routing_files_into_the_place[Minimal / Deep Tech-Low Energy-Deep House-9-expected6]`
  - `tests/test_organize_mirror_edits.py::test_the_tags_are_the_nearest_pair_routing_files_into_the_place[Tech House-Med-Deep House-2-expected0]`
  - `tests/test_organize_mirror_edits.py::test_the_tags_are_the_nearest_pair_routing_files_into_the_place[Tech House-None-Deep House-5-expected4]`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
        if routing.resolve_bucket(declared, word).bucket_id != bucket_id:
```

New text:

```
        if False:
```

### `u204.O2_unfavourite_leaves_months`

_plan_favourites: an unfavourite leaves All Favorites alone and stays in its months

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O2_unfavourite_leaves_months`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_removed_from_all_favorites_leaves_the_favorites_folder`

Old text:

```
            leave += [(pid, folder, name) for name, pid in filing if pid in held]
```

New text:

```
            leave += []
```

### `u204.O3_quarter_refused`

_plan_favourites: a favourite put in a quarter is filed into it

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O3_quarter_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_put_in_a_quarter_is_named_and_not_filed`

Old text:

```
            if placeholders.MONTH_LABEL.fullmatch(month) is None and month != placeholders.UNDATED:
```

New text:

```
            if False:
```

### `u204.O4_colour`

_plan_favourites: a favourite with no colour is not coloured Pink

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O4_colour`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_all_favorites_is_favourited_in_its_month_and_coloured`

Old text:

```
        takes = bool(pink) and decision.content_id in colour.sort_rows(db, pink, [decision.content_id]).to_colour
```

New text:

```
        takes = False
```

### `u204.O5_batch_live`

_plan_inbox: a batch no longer directly under INBOX is written as if it were

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O5_batch_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_batch_moved_into_old_since_the_plan_is_never_touched`

Old text:

```
        if len(found) != 1:
```

New text:

```
        if False:
```

### `u204.O6_inbox_latch`

write: an INBOX edit asks no intake tree latch

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O6_inbox_latch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_inbox_edit_over_a_latched_intake_tree_writes_nothing`

Old text:

```
    if edits.INBOX in touched:
```

New text:

```
    if False:
```

### `u204.O7_restore_detected`

write: a favourites only write detects no out of band restore

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O7_restore_detected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_favourites_only_write_detects_an_out_of_band_restore_and_asks_no_tree_latch`

Old text:

```
    if touched and not touched & {edits.GENRE, edits.INBOX}:
```

New text:

```
    if False:
```

### `u236.M13_write_records_no_month`

write: record no month placement, so settle records none

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M13_write_records_no_month`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
        if at:
            done.months.append((one.content_id, one.month, at))
```

New text:

```
        if False:
            done.months.append((one.content_id, one.month, at))
```

### `u236.M14_write_wrong_time`

write: record a time no membership carries

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M14_write_wrong_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
            done.months.append((one.content_id, one.month, at))
```

New text:

```
            done.months.append((one.content_id, one.month, at + "x"))
```

### `u236.M15_settle_month_title`

settle: record the placement under the month's bare name, not its account title

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M15_settle_month_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 8 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_hand_addition_after_the_placement_is_dropped_is_read_as_one`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_organize_after_the_favourite_puts_it_in_the_accounts_month`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
                mirror.title(decision.to.folder, month_of[decision.content_id][0]),
```

New text:

```
                month_of[decision.content_id][0],
```

### `u236.M16_settle_any_favourite`

settle: record a placement for a favourite put in a month on the account too

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M16_settle_any_favourite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`

Old text:

```
            and decision.to.primary
            and month_of.get(decision.content_id)
```

New text:

```
            and month_of.get(decision.content_id)
```

### `u340.R17_edit_second_path_off`

_plan_genre: read a track with two genres as one, so an account edit in one folder is taken as today

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u340.json`, row `R17_edit_second_path_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_organize_mirror_edits_u340.py`, `tests/test_organize_mirror_edits.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u340.py::test_a_band_move_in_one_folder_moves_the_energy_in_both_and_keeps_the_second_genre`

Old text:

```
        elif two is not None:
```

New text:

```
        elif False:
```

### `u340.R18_edit_off_other`

_second_genre_tags: drop the check that the edit left the other folder, so a take off of one folder is read as a no op

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u340.json`, row `R18_edit_off_other`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_organize_mirror_edits_u340.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u340.py::test_taking_it_off_one_folder_alone_is_listed_and_not_taken`
  - `tests/test_second_genre.py::test_an_edit_that_does_not_say_which_genre_changed_is_not_taken[off-first]`
  - `tests/test_second_genre.py::test_an_edit_that_does_not_say_which_genre_changed_is_not_taken[off-second]`

Old text:

```
        if other in left:
```

New text:

```
        if False:
```

### `u340.R19_edit_third_swapped`

_second_genre_tags: replace the second genre whichever folder the move left

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u340.json`, row `R19_edit_third_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_organize_mirror_edits_u340.py`, `tests/test_organize_mirror_edits.py`
- Collected: 103 against a baseline of 103
- Kills: 2 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_move_into_the_fallback_folder_is_not_taken[first]`
  - `tests/test_second_genre.py::test_a_move_out_of_one_folder_into_a_third_replaces_that_folders_genre_only`

Old text:

```
    found = (word, energy, truth.second_genre) if left == {one} else (truth.genre, energy, word)
```

New text:

```
    found = (truth.genre, energy, word)
```

### `u340.R20_edit_write_drops_second`

_write_tags: never write the second genre, so an edit that replaces it writes nothing

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u340.json`, row `R20_edit_write_drops_second`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_organize_mirror_edits_u340.py`, `tests/test_organize_mirror_edits.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre.py::test_the_write_reads_back_the_second_genre_and_leaves_a_one_genre_file_as_before`

Old text:

```
    if change.second_was or change.second:
        pairs.append(("secondgenre", change.second))
```

New text:

```
    if False:
        pairs.append(("secondgenre", change.second))
```

### `u340.R29_edit_fallback_taken`

_second_genre_tags: take a move whose genres file the track elsewhere, so a move into Electronica / Other loses a folder (B2)

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u340.json`, row `R29_edit_fallback_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_organize_mirror_edits_u340.py`, `tests/test_organize_mirror_edits.py`
- Collected: 103 against a baseline of 103
- Kills: 2 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_move_into_the_fallback_folder_is_not_taken[first]`
  - `tests/test_second_genre.py::test_a_move_into_the_fallback_folder_is_not_taken[second]`

Old text:

```
    if filed != {kept, to}:
```

New text:

```
    if False:
```

### `u214.M12_frozen_pairs`

_unmirrored: accept a frozen node of any length

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u214.json`, row `M12_frozen_pairs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        isinstance(one, list) and len(one) == 2 and all(isinstance(part, str) for part in one)
```

New text:

```
        isinstance(one, list) and all(isinstance(part, str) for part in one)
```

### `u222-zeros.M18_label_no_folder`

_label: read no folder line, so a folder that moved is never named

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222-zeros.json`, row `M18_label_no_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_label_step_that_moved_is_named_by_its_folder_line`

Old text:

```
    for key in ("playlist", "folder"):
```

New text:

```
    for key in ("playlist",):
```

### `u222-zeros.M5_agreed_none_lost`

_agreed_json: freeze a never agreed snapshot as an empty one

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222-zeros.json`, row `M5_agreed_none_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_never_agreed_snapshot_is_frozen_and_read_back_as_never_agreed`

Old text:

```
            title: [one.remote_id, None if one.agreed is None else sorted(one.agreed)]
```

New text:

```
            title: [one.remote_id, sorted(one.agreed or ())]
```

### `u222.M10_shown_flag_check`

load: accept a shown flag that is not true or false

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M10_shown_flag_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`

Old text:

```
        if not isinstance(shown, bool):
```

New text:

```
        if False:
```

### `u222.M13_moved_equal_named`

moved: name every step, moved or not

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M13_moved_equal_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_write_outside_any_mirrored_playlist_between_the_acts_is_not_stale`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_account_change_between_the_acts_is_stale_and_names_its_folder_and_playlist`
  - `tests/test_organize_mirror_frozen_u222.py::test_with_nothing_between_the_acts_the_apply_rebuilds_the_frozen_plan`

Old text:

```
        if digest_of(step.identity()) == then.digest:
            continue

```

New text:

```
(empty)
```

### `u222.M14_moved_new_step_silent`

moved: say nothing of a step the gate did not show

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M14_moved_new_step_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`

Old text:

```
            said.append(f"{step.title}, which the gate did not show")
            continue
```

New text:

```
            continue
```

### `u222.M15_moved_gone_step_silent`

moved: say nothing of a step the gate showed and this run did not plan

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M15_moved_gone_step_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`

Old text:

```
            said.append(f"{then.title}, which the gate showed and this run did not plan")
```

New text:

```
            pass
```

### `u222.M16_lines_inverted`

moved: name the lines that did NOT move

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M16_lines_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_label_step_that_moved_is_named_by_its_folder_line`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_account_change_between_the_acts_is_stale_and_names_its_folder_and_playlist`

Old text:

```
                if lines.get(label) != then.lines.get(label)
```

New text:

```
                if lines.get(label) == then.lines.get(label)
```

### `u222.M17_refused_named_by_every_line`

moved: name a refused step by every line the gate showed (review round one)

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M17_refused_named_by_every_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`

Old text:

```
            if lines and then.lines
            else []
```

New text:

```
            if lines or then.lines
            else []
```

### `u222.M2_overlay_never_replaces`

overlay: keep the live snapshot of every playlist, the frozen one never taken

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M2_overlay_never_replaces`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_genre_edit_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_playlist_made_again_between_the_acts_reads_its_snapshot_now`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_join_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_leave_the_library_took_between_the_acts_applies_the_approved_plan`

Old text:

```
                one = replace(one, agreed=held[1])
```

New text:

```
                one = one
```

### `u222.M3_overlay_any_remote_id`

overlay: take the frozen snapshot for a playlist made again under another remote id

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M3_overlay_any_remote_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_playlist_made_again_between_the_acts_reads_its_snapshot_now`

Old text:

```
            if held is not None and held[0] == one.remote_id:
```

New text:

```
            if held is not None:
```

### `u222.M6_load_drops_agreed`

load: read no frozen snapshot, so the overlay has nothing to take

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M6_load_drops_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_genre_edit_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_never_agreed_snapshot_is_frozen_and_read_back_as_never_agreed`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_join_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_leave_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`
  - `tests/test_organize_mirror_frozen_u222.py::test_the_frozen_snapshot_is_the_one_the_gates_plan_read_not_the_one_it_recorded`

Old text:

```
        agreed = _agreed_of(data["agreed"])
```

New text:

```
        agreed = {}
```

### `u222.M8_agreed_list_check`

_agreed_of: accept a snapshot that is not a list of text

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M8_agreed_list_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`

Old text:

```
            if agreed is not None and (
```

New text:

```
            if False and (
```

### `u222.M9_text_check`

_text: accept anything as text

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M9_text_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`

Old text:

```
    if not isinstance(value, str):
        raise ValueError(f"{what} is {value!r}, not text")
```

New text:

```
    if False:
        raise ValueError(f"{what} is {value!r}, not text")
```

### `u236.M21_frozen_not_overlaid`

overlay: read the ledger's placements now beside the gate's snapshot

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u236.json`, row `M21_frozen_not_overlaid`
- Moved: the overlay of the gate's placements is still in mirror_frozen.overlay, the replace call now written on one line instead of two; same snapshot read dropped for the ledger's own
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_frozen_folder_with_no_placements_reads_none_and_one_unread_reads_the_ledgers`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`

Old text:

```
placed=frozen.placed.get(name, folder.placed))
```

New text:

```
placed=folder.placed)
```

### `u236.M22_frozen_not_written`

freeze: freeze no placements

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u236.json`, row `M22_frozen_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`

Old text:

```
            name: {title: dict(sorted(tracks.items())) for title, tracks in sorted(folder.placed.items())}
```

New text:

```
            name: {}
```

### `u236.M23_frozen_reads_malformed`

load: accept placements that are not tracks to times

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u236.json`, row `M23_frozen_reads_malformed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 225 against a baseline of 225
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`

Old text:

```
            if not isinstance(tracks, dict) or not all(
                isinstance(track, str) and isinstance(at, str) for track, at in tracks.items()
            ):
```

New text:

```
            if False:
```

### `r598-b.B1_sweep_before_the_lock`

release_lock: abandon the orphans before releasing the lock, so a live holder's refusal arrives after records were already ended

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B1_sweep_before_the_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_refused_or_aborted_release_abandons_nothing[live-lock-holder]`

Old text:

```
    cleared = session.release_stale_lock(cfg)
    abandoned = [
```

New text:

```
    abandoned_first = session.abandon_orphaned_sessions(cfg)
    cleared = session.release_stale_lock(cfg)
    abandoned = [record.session_id for record in abandoned_first] + [
```

### `r598-b.B3_orphans_not_shown`

release_lock: show an empty orphan list at the gate, so the person decides without seeing what will be ended

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B3_orphans_not_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`

Old text:

```
                for record in orphans
            ],
```

New text:

```
                for record in orphans[:0]
            ],
```

### `r598-b.B4_abandon_only_reported_as_no_op`

release_lock: report a release that only abandoned records as a no-op, telling a person nothing changed

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B4_abandon_only_reported_as_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_release_that_only_abandons_is_a_change_and_passes_the_contract`

Old text:

```
            outcome=Outcome.OK if abandoned else Outcome.NO_OP,
```

New text:

```
            outcome=Outcome.NO_OP,
```

### `r598-b.B5_kept_reports_nothing`

release_lock: report no kept records, hiding an open record the verb deliberately left

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B5_kept_reports_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[alive]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_session_cli.py::test_an_open_record_that_names_no_holder_is_never_abandoned`

Old text:

```
    kept = [record.session_id for record in session.records(cfg) if not record.terminal]
```

New text:

```
    kept = []
```

### `u138.S7_verb_drops_the_answer`

The verb never hands down who answered the gate

- File: `src/cratekit/session/cli.py`
- Source: `u138.json`, row `S7_verb_drops_the_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 7 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        cfg, now=now, decided_by=answered.actor if answered is not None else None

```

New text:

```
        cfg, now=now, decided_by=None

```

### `u184.A10_summary_always_recorded`

_summary: say recorded whether or not this call minted

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A10_summary_always_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
        "recorded": minted,
```

New text:

```
        "recorded": True,
```

### `u184.A11_wording_swapped`

_expiry_row: swap the two phrasings, so a mint reads as already on record

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A11_wording_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
    said = "recorded now" if minted else "already on record, not minted again"
```

New text:

```
    said = "already on record, not minted again" if minted else "recorded now"
```

### `u184.A1_flag_ignored`

record_ack: never take the session road, so --as session falls to the gate and leaves a run waiting

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A1_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`, `tests/test_crate_sync_skill.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 86 against a baseline of 86
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
    if getattr(ctx.args, "as_actor", None) == session.SESSION_ACTOR:
```

New text:

```
    if False:
```

### `u184.A2_any_actor_accepted`

build_ack: drop the one value restriction, so --as names any actor and is parsed

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A2_any_actor_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`, `tests/test_crate_sync_skill.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 86 against a baseline of 86
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[Session]`
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[a-person]`
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[cli]`

Old text:

```
        choices=(session.SESSION_ACTOR,),
```

New text:

```
        choices=None,
```

### `u184.A3_engine_rule_not_selected`

_mint_as_session: hand no actor to the engine, so the terminal rule decides and the ages are not judged

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A3_engine_rule_not_selected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 9 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
        cfg, now=now, decided_by=session.SESSION_ACTOR
    )
```

New text:

```
        cfg, now=now, decided_by=None
    )
```

### `u184.A4_valid_record_minted_again`

_mint_as_session: never report a valid acknowledgment, so every call mints a fresh one

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A4_valid_record_minted_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
    if recorded is not None and recorded.valid_at(now):
```

New text:

```
    if False:
```

### `u184.A5_expired_reported_valid`

_mint_as_session: drop the window check, so an expired acknowledgment is reported as on record

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A5_expired_reported_valid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`

Old text:

```
    if recorded is not None and recorded.valid_at(now):
```

New text:

```
    if recorded is not None:
```

### `u184.A6_unreadable_record_refuses`

_mint_as_session: let an unreadable record raise, so a damaged file can never be replaced by the session

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A6_unreadable_record_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`

Old text:

```
    except CratekitError:
        recorded = None
```

New text:

```
    except CratekitError:
        raise
```

### `u184.A7_already_valid_says_ok`

_mint_as_session: report an existing acknowledgment as an ok run rather than a no op

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A7_already_valid_says_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
                "summary": _summary(recorded, minted=False),
            },
            outcome=Outcome.NO_OP,
```

New text:

```
                "summary": _summary(recorded, minted=False),
            },
            outcome=Outcome.OK,
```

### `u184.A8_expiry_row_dropped`

_mint_as_session: leave the expiry row out of a mint, so a person at a terminal is never shown it

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A8_expiry_row_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`

Old text:

```
                _expiry_row(acknowledgment, minted=True),
```

New text:

```
(empty)
```

### `u184.A9_expiry_row_names_the_mint`

_expiry_row: name the moment recorded where the expiry belongs

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A9_expiry_row_names_the_mint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`

Old text:

```
            f"{acknowledgment.expires_at.isoformat()}"
```

New text:

```
            f"{acknowledgment.recorded_at.isoformat()}"
```

### `u311.B2_acknowledgment_hides_what_it_showed`

Both mints report an acknowledgment without the ages it was shown

- File: `src/cratekit/session/cli.py`
- Source: `u311.json`, row `B2_acknowledgment_hides_what_it_showed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_second_mint_replaces_the_record_and_moves_the_window`

Old text:

```
        "shown": [entry.to_json() for entry in acknowledgment.shown],
```

New text:

```
        "shown": [],
```

### `u49-author.A2_the_abort_mints_anyway`

Drop the abort branch in record_ack, so a person who declines gets an acknowledgment

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A2_the_abort_mints_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_inline_answer_cannot_overturn_a_recorded_abort`
  - `tests/test_session_cli.py::test_answering_abort_records_nothing_and_says_so`

Old text:

```
    if option == "abort":
        return ctx.envelope(
            data={"checks": [], "summary": {"recorded": False, "ages": shown}},
            outcome=Outcome.NO_OP,
        )

```

New text:

```
(empty)
```

### `u49-author.A3_the_refusal_names_no_ages`

Drop the context argument from the ack gate, so the refusal asks the question over nothing

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A3_the_refusal_names_no_ages`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_person_at_a_terminal_reads_the_ages_and_not_only_a_json_consumer`
  - `tests/test_session_cli.py::test_the_refusal_before_acknowledging_names_the_ages_it_consulted`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
    option = ctx.gate.require(
        spec, context={"ages": shown, "acknowledgment": _on_record(cfg, now)}
    )
```

New text:

```
    option = ctx.gate.require(spec)
```

### `u49-author.A4_the_record_on_file_is_not_shown`

Show the ages but not the acknowledgment already on record, so a person cannot see whether they are covered

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A4_the_record_on_file_is_not_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
        spec, context={"ages": shown, "acknowledgment": _on_record(cfg, now)}
```

New text:

```
        spec, context={"ages": shown}
```

### `u49-author.A6_the_authorisation_is_not_spent`

Leave the recorded decision in place after the mint, so one run id re-mints the acknowledgment forever (R-217's defect restored)

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A6_the_authorisation_is_not_spent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`

Old text:

```
    ctx.run.decisions.pop(spec.name, None)
```

New text:

```
(empty)
```

### `u49-author.A7_the_check_rows_are_keyed_wrong`

Key the ack check rows by name rather than key, so the human check table prints a question mark where the portion should be

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A7_the_check_rows_are_keyed_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`

Old text:

```
                    "key": f"backup.age.{entry['portion']}",
```

New text:

```
                    "name": f"backup.age.{entry['portion']}",
```

### `u49-author.A8_a_damaged_record_locks_the_verb_out`

Let the display read of the acknowledgment raise, so a corrupt record makes the one verb that replaces it refuse

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A8_a_damaged_record_locks_the_verb_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`

Old text:

```
    try:
        recorded = session.read_acknowledgment(cfg)
    except CratekitError as exc:
        return {"unreadable": exc.cause.message}
```

New text:

```
    recorded = session.read_acknowledgment(cfg)
```

### `u49-author.R1_hard_code_the_repair_token`

Name repair-backup-facts over every unreadable condition, which is R-201's defect reproduced on the new consumer

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `R1_hard_code_the_repair_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[newer-upgrade-cratekit]`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
```

New text:

```
            remedy=Remedy.REPAIR_BACKUP_FACTS,
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
```

### `u49-author.R2_hard_code_the_permission_token`

The same defect mirrored: name grant-path-access over every condition. Both directions are driven because a carry measured one way leaves the other unasserted

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `R2_hard_code_the_permission_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[corrupt-repair-backup-facts]`
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[newer-upgrade-cratekit]`

Old text:

```
            remedy=Remedy(str(exc.remedy)),
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
```

New text:

```
            remedy=Remedy.GRANT_PATH_ACCESS,
            origin=("session", "cli"),
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
```

### `u49-author.R3_an_unreadable_file_reads_as_empty`

Swallow BackupFactsUnreadable and show no ages, collapsing could-not-read into never-backed-up

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `R3_an_unreadable_file_reads_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[corrupt-repair-backup-facts]`
  - `tests/test_session_cli.py::test_an_unreadable_fact_file_refuses_and_the_remedy_the_raiser_chose_travels[newer-upgrade-cratekit]`

Old text:

```
    except backup_facts.BackupFactsUnreadable as exc:
        raise refuse(
```

New text:

```
    except backup_facts.BackupFactsUnreadable:
        return []
    except NotImplementedError as exc:
        raise refuse(
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

### `r187-a.C1_blank_not_key`

names_something: ask the text and not the comparison key, so a name of punctuation alone is searched for

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C1_blank_not_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_with_nothing_in_it_is_an_unknown_anchor[ - ]`
  - `tests/test_setbuilder_cli.py::test_an_empty_name_refuses_before_any_scan`

Old text:

```
    return bool(setbuilder.match_key("", text))
```

New text:

```
    return bool(text.strip())
```

### `r187-a.C3_mutex`

build: declare --named on the parser and not in the exclusive group, so it can sit beside a path or a label

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C3_mutex`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_invocation_the_flags_cannot_take_is_the_parsers_verdict[name-and-path]`
  - `tests/test_setbuilder_cli.py::test_an_invocation_the_flags_cannot_take_is_the_parsers_verdict[name-and-unowned]`

Old text:

```
    anchor.add_argument(
        "--named",
```

New text:

```
    parser.add_argument(
        "--named",
```

### `r187-a.C4_key_beside_name`

set_build: a key beside --named is let through and silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C4_key_beside_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[key-beside-name]`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if ctx.args.named is None and (ctx.args.key is not None or ctx.args.tempo is not None):
```

### `r187-a.C5_empty_name_scans`

set_build: an empty name pays for the library walk before it is refused

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C5_empty_name_scans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_empty_name_refuses_before_any_scan`

Old text:

```
        index = _index(cfg, root) if names_something(ctx.args.named) else ()
```

New text:

```
        index = _index(cfg, root)
```

### `r187-a.C6_no_cache_path`

_index: pass no cache path, which is R-188 itself, every set a full scan

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C6_no_cache_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_second_run_reads_no_tag_it_already_holds`
  - `tests/test_setbuilder_cli.py::test_the_first_run_opens_each_file_once_and_the_second_none`
  - `tests/test_setbuilder_cli.py::test_the_verb_writes_its_declared_cache_and_nothing_of_the_librarys`

Old text:

```
        cache_path=config.state_path("setbuilder_index_cache", cfg),
```

New text:

```
        cache_path=None,
```

### `u279.M10_tilde_not_expanded`

excluded_folders: read the staging path without expanding a tilde, round one's finding

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M10_tilde_not_expanded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
Path(cfg.paths.download_staging).expanduser())
```

New text:

```
Path(cfg.paths.download_staging))
```

### `u279.M11_excluded_anchor_not_refused`

set_build: drop the excluded anchor refusal, so an anchor in staging gets the generic not indexed wording

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M11_excluded_anchor_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[state]`

Old text:

```
    _refuse_if_excluded(candidate, cfg, root)

```

New text:

```
(empty)
```

### `u279.M13_wrong_folder_named`

_refuse_if_excluded: say the state folder whichever folder holds the anchor

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M13_wrong_folder_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`

Old text:

```
    if holder == folders[0]:
```

New text:

```
    if True:
```

### `u279.M8_index_call_unexcluded`

setbuild _index: drop exclude, so the verb's index walks the state and staging folders again

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M8_index_call_unexcluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 6 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
        exclude=excluded_folders(cfg),

```

New text:

```
(empty)
```

### `u279.M9_staging_not_excluded`

excluded_folders: leave download staging out of the exclusion, the state folder only

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M9_staging_not_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 340 against a baseline of 340
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
    return (config.library_state_dir(cfg), Path(cfg.paths.download_staging).expanduser())
```

New text:

```
    return (config.library_state_dir(cfg), config.library_state_dir(cfg))
```

### `u43-author-light.A1_first_track_wins`

anchor_in_index returns the first indexed track instead of the one at the path, which is exactly what the fuzzy lookup this design replaces does when a version suffix is present

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A1_first_track_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[path-not-indexed]`
  - `tests/test_setbuilder_cli.py::test_an_anchor_spelled_through_a_symlink_still_resolves`
  - `tests/test_setbuilder_cli.py::test_an_exact_name_is_never_lost_to_a_longer_title_whichever_came_first`
  - `tests/test_setbuilder_cli.py::test_what_plays_after_a_track_is_asked_by_name`

Old text:

```
    wanted = str(path)
    for track in index:
        if track.path == wanted:
            return track
```

New text:

```
    wanted = str(path)
    for track in index:
        if track.path or wanted:
            return track
```

### `u43-author-light.A3_containment_not_checked`

anchor_path stops checking that the anchor is inside the library, so a path walking out with .. is scanned for and refused as unindexed rather than refused as outside

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A3_containment_not_checked`
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
    if _within(candidate, root) and False:
```

### `u43-author-light.A4_empty_anchor_defaults`

anchor_path stops refusing an empty anchor, which turns it into the library root and asks the index for a directory

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A4_empty_anchor_defaults`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[empty-anchor]`
  - `tests/test_setbuilder_cli.py::test_an_anchor_path_is_taken_against_the_library_and_never_walks_out_or_defaults`

Old text:

```
    if not anchor:
        raise refuse(
```

New text:

```
    if anchor and not anchor:
        raise refuse(
```

### `u43-author-light.C1_no_lower_bound`

positive_count stops refusing zero and negatives, so build_plan's pool[: count or DEFAULT_POOL] silently turns 0 into 8 and -1 into a dropped last companion

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `C1_no_lower_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_value_the_flag_cannot_take_is_refused_at_the_parser[positive_count--1]`
  - `tests/test_setbuilder_cli.py::test_a_value_the_flag_cannot_take_is_refused_at_the_parser[positive_count--8]`
  - `tests/test_setbuilder_cli.py::test_a_value_the_flag_cannot_take_is_refused_at_the_parser[positive_count-0]`
  - `tests/test_setbuilder_cli.py::test_an_invocation_the_flags_cannot_take_is_the_parsers_verdict[count-below-one]`

Old text:

```
    value = int(text)
    if value < 1:
        raise ValueError(f"{text!r} is not a positive count")
    return value
```

New text:

```
    return int(text)
```

