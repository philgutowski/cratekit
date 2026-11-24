# Mutation table: u335-before-10

Measured by `scripts/mutate.py` on 2026-11-24 05:01 UTC, branch `HEAD` at `b41c698d`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 262.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 05:01 UTC for commit `b41c698da363`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 45, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r838-b.U9_renamed_since` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-c.U7b_not_listed_rerun` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `u242.M22_unmark_releases_nothing` | `src/cratekit/sync/unmark_cli.py` | user | 4 file(s) | 197 | 7 | killed |
| `u242.M26_release_stamps_no_mark` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 78 | 3 | killed |
| `u246.S14_unmark_narrowed_empty` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 47 | 3 | killed |
| `u246.S15_unmark_narrowed_first_only` | `src/cratekit/sync/unmark_cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u306.C4_reports_reversed` | `src/cratekit/tagging/artifacts.py` | user | 3 file(s) | 252 | 5 | killed |
| `u292.M01_floor` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1082 | 1 | killed |
| `u292.M02_proposed_needs_a_write` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1082 | 3 | killed |
| `u292.M03_served_needs_a_write` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1082 | 3 | killed |
| `u292.M04_file_word_routes_first` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1082 | 8 | killed |
| `u292.M05_coarse_never_hides_specific` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1082 | 7 | killed |
| `u292.M08_alias_rows_need_an_entry` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1082 | 3 | killed |
| `u292.M09_folder_counts_by_the_row` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1082 | 2 | killed |
| `u292.M10_unread_counted` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1082 | 1 | killed |
| `u292.M11_joining_files_nowhere` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1082 | 1 | killed |
| `u292.M15_settled_rows_reached` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1082 | 2 | killed |
| `u294.M26_needing_disposition` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 118 | 5 | killed |
| `u292.M16_outcome_over_unread` | `src/cratekit/tagging/backlog_cli.py` | user | 2 file(s) | 1082 | 1 | killed |
| `u322.M22_backlog_partly_clause_gone` | `src/cratekit/tagging/backlog_cli.py` | user | 6 file(s) | 392 | 1 | killed |
| `u322.M24_backlog_line_gone` | `src/cratekit/tagging/backlog_cli.py` | user | 6 file(s) | 392 | 2 | killed |
| `r791-a.S1_403_blocks` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 239 | 11 | killed |
| `r791-a.S3_client_challenge_title` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 239 | 8 | killed |
| `u281.R1_stop_after_four` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 11 | killed |
| `u281.R2_limit_two` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 12 | killed |
| `u281.R3_stopped_reads_miss` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 8 | killed |
| `u281.R4_stopped_note_unmarked` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 3 | killed |
| `u281.R7_one_count_for_every_catalogue` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 3 | killed |
| `u281.S6_every_title_named_cloudflare` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 205 | 2 | killed |
| `u282.W1_walk_beatport_first` | `src/cratekit/tagging/catalogues.py` | user | 9 file(s) | 1470 | 43 | killed |
| `u282.W2_sources_beatport_first` | `src/cratekit/tagging/catalogues.py` | user | 9 file(s) | 1470 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R7_pacer_does_not_sleep` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 189 | 6 | killed |
| `r1184.M19_tag_folder_wiring` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 289 | 1 | killed |
| `r1184.M20_tag_folder_fallback` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 289 | 1 | killed |
| `r650-a.B5_artifact_drops_the_key` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 3 | killed |
| `r650-a.C4_warning_fires_on_a_clean_sweep` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r650-a.C6_warning_names_no_strings` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r650-a.C7_warning_order_is_the_walk_order` | `src/cratekit/tagging/cli.py` | maintainer | 1 file(s) | 102 | 1 | killed |
| `r650-a.C8_warning_code_reworded` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r650-a.C9_warning_counts_the_wrong_total` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r791-b.C1_artifact_answers` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 239 | 15 | killed |
| `r791-b.C2_artifact_unread` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 239 | 6 | killed |
| `r791-b.C6_not_asked_excluded` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 239 | 1 | killed |
| `r791-b.C7_parse_break_said` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 239 | 1 | killed |
| `r796-c.V1_the_worker_hands_the_seam_over` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 380 | 10 | killed |
| `r796-c.V2_blocked_warning_is_the_shops_only` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 380 | 1 | killed |
| `r796-c.V3_some_unread_is_said` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 380 | 1 | killed |
| `r796-c.V4_no_isrc_is_warned_about` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 380 | 1 | killed |
| `r796-c.V5_parse_break_sentence_said_once` | `src/cratekit/tagging/cli.py` | maintainer | 4 file(s) | 380 | 1 | killed |
| `u192.T4_tag_queue_only_ignored` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 221 | 7 | killed |
| `u240.M11_needle_is_the_name` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 2 | killed |
| `u240.M12_raw_line_matched` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 2 | killed |
| `u240.M13_two_way_match` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 7 | killed |
| `u240.M16_genres_joined_by_name` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 1 | killed |
| `u240.M17_worker_hands_no_seam` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 8 | killed |
| `u240.M20_warning_dropped` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 1 | killed |
| `u240.M21_failed_sweep_unreported` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 3 | killed |
| `u240.M23_cap_lowered` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 1 | killed |
| `u281.C1_refusal_said_as_blocked` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 138 | 5 | killed |
| `u281.C4_source_blocked_counts_unsent_as_sent` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u281.C5_partial_challenge_called_whole` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u281.W7_worker_run_key_without_attempt` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 138 | 1 | killed |
| `u282.C2_refused_token_not_warned` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 443 | 1 | killed |
| `u284.C5_sweep_stop_unsaid` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 1 | killed |
| `u289.C1_record_drops_asked` | `src/cratekit/tagging/cli.py` | user | 8 file(s) | 1437 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R19_folder_queues_no_items` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 41 | killed |
| `u56-catalogue-searcher-and-tag-workers.R20_unnamed_folder_sweeps_cwd` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R21_two_zeroes_read_as_one` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R22_vanished_file_reports_done` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u84-b.C1_artifact_carries_status` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u85-a.A15_worker_hands_in_the_fetch` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 102 | 3 | killed |
| `u244.M01_no_token_not_asked` | `src/cratekit/tagging/discogs.py` | user | 5 file(s) | 470 | 11 | killed |
| `u244.M02_rejection_remembered` | `src/cratekit/tagging/discogs.py` | user | 3 file(s) | 262 | 2 | killed |
| `u289.S4_discogs_asked_head` | `src/cratekit/tagging/discogs.py` | user | 8 file(s) | 1437 | 27 | killed |
| `u318.S01_track_needs_the_mix` | `src/cratekit/tagging/discogs.py` | user | 8 file(s) | 1728 | 32 | killed |
| `r1967.M01_mint_with_a_row` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 27 | killed |
| `r1967.M02_mint_for_a_file_alone` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 1 | killed |
| `r1967.M03_never_mint` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 7 | killed |
| `r1967.M04_gate_hides_mint` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 2 | killed |
| `r1967.M05_stale_count_takes_the_lookup_row` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 1 | killed |
| `r1967.M06_stale_names_no_lookup_row` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 1 | killed |
| `r1967.M07_no_check_before_files` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 1 | killed |
| `r1967.M08_check_passes_a_found_row` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 1 | killed |
| `r1967.M09_mint_always` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 1 | killed |
| `r1967.M10_mint_never_at_the_write` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 2 | killed |
| `r1967.M11_creations_always` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 1 | killed |
| `r1967.M12_creations_never` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 2 | killed |
| `r1967.M14_uuid_constant` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 1 | killed |
| `r1967.M15_minted_unreported` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 2 | killed |
| `r1967.M16_minted_name_lowered` | `src/cratekit/tagging/genre_set.py` | user | 3 file(s) | 291 | 2 | killed |
| `u339.M11_file_writes` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 2 | killed |
| `u339.M12_leaves_held` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 2 | killed |
| `u339.M13_digest_leaves` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 1 | killed |
| `u339.M14_stale_check` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 3 | killed |
| `u339.M15_file_reread` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 1 | killed |
| `u339.M16_record_before` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 3 | killed |
| `u339.M17_row_needs_file` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 3 | killed |
| `u339.M1_genre_declared` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 1 | killed |
| `u339.M2_path_whole_name` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 6 | killed |
| `u339.M3_path_two_nodes` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 1 | killed |
| `u339.M4_path_folder` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 2 | killed |
| `u339.M5_removed_member` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 2 | killed |
| `u339.M7_multi_valued` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 1 | killed |
| `u339.M8_held_out` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 2 | killed |
| `u339.M9_already` | `src/cratekit/tagging/genre_set.py` | user | 2 file(s) | 78 | 2 | killed |
| `r1967.C01_never_say_to_make` | `src/cratekit/tagging/genre_set_cli.py` | user | 3 file(s) | 291 | 1 | killed |
| `r1967.C03_payload_hides_mint` | `src/cratekit/tagging/genre_set_cli.py` | user | 3 file(s) | 291 | 1 | killed |
| `r1967.C04_written_hides_the_row_made` | `src/cratekit/tagging/genre_set_cli.py` | user | 3 file(s) | 291 | 1 | killed |
| `u172-b.A14_write_false_trusted` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172-b.A16_tombstone_votes` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A10_tie_not_broken_by_artist` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A11_split_not_written` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.A12_fraction_into_weigh` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 2 | killed |
| `u172.A13_report_writes` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A15_read_back_skipped` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A17_bound_read_as_float` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.A2_tagged_file_is_a_candidate` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 7 | killed |
| `u172.A3_off_taxonomy_never_named` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.A5_same_artist_votes_twice` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A6_vote_per_member` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 5 | killed |
| `u172.A7_playlist_weight_halved` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 6 | killed |
| `u172.A8_artist_weight_halved` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 6 | killed |
| `u172.A9_folder_artist_ignored` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 5 | killed |
| `r1184.M21_guess_wiring` | `src/cratekit/tagging/guess_cli.py` | user | 3 file(s) | 289 | 1 | killed |
| `u172.B1_library_read_for_nothing` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.B2_unknown_pass_silent` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.B3_pass_ignored` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.B4_outcome_ok_always` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 4 | killed |
| `r816-d.C2_empty_plan` | `src/cratekit/tagging/plan_verbs.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-d.C3_majority_unmapped` | `src/cratekit/tagging/plan_verbs.py` | user | 1 file(s) | 72 | 1 | killed |
| `u306.C3_applied_written_zero` | `src/cratekit/tagging/plan_verbs.py` | user | 3 file(s) | 224 | 4 | killed |
| `u306.P1_named_cap` | `src/cratekit/tagging/plan_verbs.py` | user | 6 file(s) | 489 | 2 | killed |
| `u306.P3_counted_zeros` | `src/cratekit/tagging/plan_verbs.py` | user | 3 file(s) | 224 | 1 | killed |
| `u306.P6_payload_count` | `src/cratekit/tagging/plan_verbs.py` | user | 3 file(s) | 224 | 1 | killed |
| `u306.P7_applied_noop` | `src/cratekit/tagging/plan_verbs.py` | user | 3 file(s) | 224 | 2 | killed |
| `u306.P9_applied_advisories` | `src/cratekit/tagging/plan_verbs.py` | user | 3 file(s) | 224 | 7 | killed |
| `u322.M20_backlog_uses_folder_binder` | `src/cratekit/tagging/plan_verbs.py` | user | 6 file(s) | 392 | 2 | killed |
| `r796-a.L1_no_data_is_a_miss` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 6 | killed |
| `r796-a.L7_a_refusal_is_remembered` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 4 | killed |
| `r796-b.O3_a_usable_answer_is_never_replaced` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 2 | killed |
| `r796-b.O5_a_declined_beatport_match_is_asked_about` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 5 | killed |
| `r796-b.O6_unread_joins_the_unread_names` | `src/cratekit/tagging/published.py` | user | 4 file(s) | 380 | 7 | killed |
| `u322.M19_suggest_binder_flag_off` | `src/cratekit/tagging/published.py` | user | 6 file(s) | 392 | 3 | killed |
| `u284.R1_since_moves_every_refusal` | `src/cratekit/tagging/refused.py` | user | 1 file(s) | 35 | 3 | killed |
| `u284.R4_empty_since_read` | `src/cratekit/tagging/refused.py` | maintainer | 1 file(s) | 35 | 1 | killed |
| `u284.R5_count_never_grows` | `src/cratekit/tagging/refused.py` | maintainer | 1 file(s) | 35 | 2 | killed |
| `u284.R7_deep_record_raises` | `src/cratekit/tagging/refused.py` | user | 1 file(s) | 35 | 1 | killed |
| `r799-b.P1_a_file_is_planned_only_while_it_carries_what_a_record_wrote` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 15 | killed |
| `r799-b.P2_two_explanations_are_ambiguous` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 4 | killed |
| `r799-b.P3_a_shops_genre_is_the_shops` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-b.P4_a_rewrite_retires_the_record_it_replaced` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 2 | killed |
| `r799-b.P5_only_a_file_under_the_library_is_opened` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 4 | killed |
| `r799-b.P6_one_file_is_one_group` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `r799-b.W1_a_file_is_read_again_before_it_is_written` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-b.W2_the_writers_answer_is_kept` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 3 | killed |
| `r799-b.W3_a_write_is_read_back` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-c.P11_blank_is_not_agreement` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-c.V3_an_unrecorded_rewrite_is_not_clean` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 2 | killed |
| `r799-c.W4_a_rewrite_is_recorded` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 5 | killed |
| `r799-c.W5_a_rewrites_record_is_one_generation_on` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 4 | killed |
| `r799-c.V1_the_gate_is_asked_before_the_write` | `src/cratekit/tagging/remap_cli.py` | user | 1 file(s) | 93 | 15 | killed |
| `r799-c.V2_a_file_that_did_not_take_refuses` | `src/cratekit/tagging/remap_cli.py` | user | 1 file(s) | 93 | 7 | killed |
| `r1103.S1_answer_too_coarse` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 4 | killed |
| `r1103.W1_writer_answer_ignored` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 6 | killed |
| `r1103.W2_unwritten_reason_blank` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 5 | killed |
| `r1103.W3_unwritten_reason_wrong` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 5 | killed |
| `r1103.W4_unwritten_proposed_dropped` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 4 | killed |
| `r1103.W6_unwritten_current_swapped` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 2 | killed |
| `r1103.H1_item_not_failed` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 3 | killed |
| `r1103.H2_refusal_slug` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 331 | 4 | killed |
| `r1103.H3_message_names_no_file` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r1103.H4_detail_path` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `r1103.H5_detail_genre` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r1103.H6_detail_current` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r185-r246-author.E3_empty_plan_queues_anyway` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 2 | killed |
| `r185-r246-author.M1_folder_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 5 | killed |
| `r185-r246-author.W1_queue_warning_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.W2_resume_warning_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.W3_resume_warning_unconditional` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 1 | killed |
| `r185-r246-author.W4_refusal_step_dropped` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 3 | killed |
| `r185-r246-author.W5_refusal_step_unconditional` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 2 | killed |
| `r185-r246-author.W6_refusal_counts_the_plan` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 2 | killed |
| `r290-author.R1_retag_rebuild_drops_the_type` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 228 | 2 | killed |
| `r816-e.E1_retag_names_the_verb` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R26_retag_queues_no_items` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 122 | 20 | killed |
| `u56-catalogue-searcher-and-tag-workers.R28_worker_trusts_the_frozen_row` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R29_blank_genre_is_corrected` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R30_specific_genre_is_overwritten` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R31_artifact_drops_the_previous_value` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 102 | 1 | killed |
| `r816-a.A1_too_coarse_protection` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 6 | killed |
| `r816-a.A2_held_out` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-a.A3_multi_valued` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-a.A4_agreement` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 12 | killed |
| `r816-a.A5_unreadable_is_blank` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-a.A6_first_value` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-a.A7_digest_counts` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-a.A8_leave_unmatched` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-b.B1_stale_check` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-b.B2_stale_tombstone` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 5 | killed |
| `r816-b.B4_restore_detection` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-b.B5_commit_recorded` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-c.B6_bookkeeping_exempt` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 10 | killed |
| `r816-c.B9_cache_reset` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `u114.M18_narrow_called` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 131 | 21 | killed |
| `u294.M01_rows_narrowed_keeps_all` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 128 | 11 | killed |
| `u294.M02_rows_narrowed_changes_unfiltered` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 128 | 21 | killed |
| `u306.T1_tallied_writes` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 131 | 31 | killed |
| `u306.T2_tallied_unread` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 131 | 4 | killed |
| `u306.T3_scanned_root` | `src/cratekit/tagging/rows.py` | user | 3 file(s) | 193 | 3 | killed |
| `r816-d.C1_acknowledgment` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C4_only_apply_writes` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C5_leave_reaches_the_plan` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `u294.M23_rows_read_back` | `src/cratekit/tagging/rows_cli.py` | user | 2 file(s) | 128 | 1 | killed |
| `u244.M21_passed_over_rides_unread` | `src/cratekit/tagging/searchers.py` | user | 5 file(s) | 470 | 6 | killed |
| `u260.F11_reset_images_forgets_nothing` | `src/cratekit/tagging/searchers.py` | maintainer | 4 file(s) | 263 | 9 | killed |

## Zero rows and what they owe

- `r799-b.P6_one_file_is_one_group` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

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
- Collected: 197 against a baseline of 197
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

### `u306.C4_reports_reversed`

What R1 does hold: tagging.artifacts.committed reads the reports last item first, so the sweep's summary lists its files out of item order

- File: `src/cratekit/tagging/artifacts.py`
- Source: `u306.json`, row `C4_reports_reversed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_shared_homes.py`
- Collected: 252 against a baseline of 252
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_report_that_cannot_be_parsed_is_skipped_rather_than_raised_on`
  - `tests/test_tag_workers.py::test_reports_past_the_four_digit_name_come_back_in_item_order`
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_report_names_each_unresolved_source_genre_with_its_count`

Old text:

```
    return _REPORTS.committed(cfg, job_id, ordered=_in_item_order)
```

New text:

```
    return _REPORTS.committed(cfg, job_id, ordered=lambda paths: _in_item_order(paths)[::-1])
```

### `u292.M01_floor`

FLOOR: propose at medium rather than high

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M01_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1082 against a baseline of 1082
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_row_below_the_floor_is_never_proposed_and_is_left_with_its_band`

Old text:

```
FLOOR = suggest.HIGH
```

New text:

```
FLOOR = suggest.MEDIUM
```

### `u292.M02_proposed_needs_a_write`

a row with no genre is proposed whatever tag suggest's action, a row below the floor included

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M02_proposed_needs_a_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1082 against a baseline of 1082
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_row_below_the_floor_is_never_proposed_and_is_left_with_its_band`
  - `tests/test_tag_backlog.py::test_a_row_with_nothing_beside_it_is_left_with_no_votes`
  - `tests/test_tag_backlog.py::test_the_campaign_lists_the_existing_verbs_in_order_and_the_projection`

Old text:

```
            if offered is not None and offered.action == suggest.WRITE:
```

New text:

```
            if offered is not None:
```

### `u292.M03_served_needs_a_write`

a row lagging its file is served whatever tag rows' action, a left row included

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M03_served_needs_a_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1082 against a baseline of 1082
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_person_reads_the_backlog`
  - `tests/test_tag_backlog.py::test_a_row_lagging_its_file_is_served_exactly_when_tag_rows_would_write_it`
  - `tests/test_tag_backlog.py::test_the_campaign_lists_the_existing_verbs_in_order_and_the_projection`

Old text:

```
            if item is not None and item.action == rows.WRITE:
```

New text:

```
            if item is not None:
```

### `u292.M04_file_word_routes_first`

cause_of: drop the test that a routing file word is the row lagging its file

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M04_file_word_routes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1082 against a baseline of 1082
- Kills: 8 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_person_reads_the_backlog`
  - `tests/test_tag_backlog.py::test_a_row_lagging_its_file_is_served_exactly_when_tag_rows_would_write_it`
  - `tests/test_tag_backlog.py::test_every_needs_genre_row_lands_in_exactly_one_cause_and_a_routed_row_in_none`
  - `tests/test_tag_backlog.py::test_off_taxonomy_words_are_grouped_across_spellings_and_ranked_by_rows`
  - `tests/test_tag_backlog.py::test_the_campaign_lists_the_existing_verbs_in_order_and_the_projection`
  - `tests/test_tag_backlog.py::test_the_cause_of_a_row_is_tested_in_order[-Melodic House-row-lags-file-Melodic House]`
  - `tests/test_tag_backlog.py::test_the_cause_of_a_row_is_tested_in_order[Indie Tech-Melodic House-row-lags-file-Melodic House]`
  - `tests/test_tag_backlog.py::test_the_verb_reports_the_backlog_and_asks_no_gate`

Old text:

```
        if disposition is adopt_scan.Disposition.ROUTE:
            return ROW_LAGS_FILE, file_word
```

New text:

```
        if False:
            return ROW_LAGS_FILE, file_word
```

### `u292.M05_coarse_never_hides_specific`

cause_of: a catch all can be the word over a specific word

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M05_coarse_never_hides_specific`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1082 against a baseline of 1082
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_catch_all_is_left_to_tag_retag`
  - `tests/test_tag_backlog.py::test_every_needs_genre_row_lands_in_exactly_one_cause_and_a_routed_row_in_none`
  - `tests/test_tag_backlog.py::test_off_taxonomy_words_are_grouped_across_spellings_and_ranked_by_rows`
  - `tests/test_tag_backlog.py::test_the_cause_of_a_row_is_tested_in_order[-Electronica-too-coarse-Electronica]`
  - `tests/test_tag_backlog.py::test_the_cause_of_a_row_is_tested_in_order[Electronica--too-coarse-Electronica]`
  - `tests/test_tag_backlog.py::test_the_cause_of_a_row_is_tested_in_order[Indie Tech-Electronica-off-taxonomy-Indie Tech]`
  - `tests/test_tag_backlog.py::test_the_verb_reports_the_backlog_and_asks_no_gate`

Old text:

```
    specific = [word for word in present if not declared.is_too_coarse_as_source(word)]
```

New text:

```
    specific = list(present)
```

### `u292.M08_alias_rows_need_an_entry`

word_of: an alias's rows follow with no genre entry for its genre

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M08_alias_rows_need_an_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1082 against a baseline of 1082
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_word_with_one_answer_moves_only_the_rows_it_reaches`
  - `tests/test_tag_backlog.py::test_an_alias_to_a_genre_the_library_has_no_entry_for_moves_nothing`
  - `tests/test_tag_backlog.py::test_the_campaign_lists_the_existing_verbs_in_order_and_the_projection`

Old text:

```
        return frozenset(row.content_id for row in alone) if known(genre) else frozenset()
```

New text:

```
        return frozenset(row.content_id for row in alone)
```

### `u292.M09_folder_counts_by_the_row`

word_of: a folder counts the rows whose FILE carries the spelling, round one's defect

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M09_folder_counts_by_the_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1082 against a baseline of 1082
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_folder_counts_a_row_only_where_tag_rows_would_write_its_word`
  - `tests/test_tag_backlog.py::test_off_taxonomy_words_are_grouped_across_spellings_and_ranked_by_rows`

Old text:

```
        if row.row_word == spelling or writes.get(row.content_id) == spelling

```

New text:

```
        if row.file_word == spelling

```

### `u292.M10_unread_counted`

plan_backlog: a row whose file is not here is dropped uncounted, round one's defect

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M10_unread_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1082 against a baseline of 1082
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_rows_whose_file_is_not_here_are_counted_and_said`

Old text:

```
            unread[rows._PROBED.get(track.readability, rows.FILE_UNREADABLE)] += 1

```

New text:

```
            pass

```

### `u292.M11_joining_files_nowhere`

plan_backlog: joining names rows tag rows gives a genre adoption files, the opposite

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M11_joining_files_nowhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1082 against a baseline of 1082
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_row_tag_rows_would_move_into_needs_genre_is_counted_back`

Old text:

```
            is not adopt_scan.Disposition.ROUTE

```

New text:

```
            is adopt_scan.Disposition.ROUTE

```

### `u292.M15_settled_rows_reached`

plan_backlog: every row of a settled word read as settled, reached or not

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M15_settled_rows_reached`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1082 against a baseline of 1082
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_word_with_one_answer_moves_only_the_rows_it_reaches`
  - `tests/test_tag_backlog.py::test_the_campaign_lists_the_existing_verbs_in_order_and_the_projection`

Old text:

```
                    if row.content_id in word.reached

```

New text:

```
                    if True

```

### `u294.M26_needing_disposition`

the census after a step counts every row it scanned, not only the needs genre ones: the one filter needing keeps once its dead checks were taken out

- File: `src/cratekit/tagging/backlog.py`
- Source: `u294.json`, row `M26_needing_disposition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_backlog.py`
- Collected: 118 against a baseline of 118
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`
  - `tests/test_tag_campaign.py::test_a_person_reads_the_campaign_and_the_resort_it_leaves`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_after_part_of_it_landed_reports_what_the_census_reads`
  - `tests/test_tag_campaign.py::test_needing_counts_only_live_rows_with_a_readable_file`
  - `tests/test_tag_campaign.py::test_the_whole_campaign_lands_and_needs_genre_falls_as_measured`

Old text:

```
        if track.disposition is adopt_scan.Disposition.NEEDS_GENRE
    )
```

New text:

```
        if True
    )
```

### `u292.M16_outcome_over_unread`

the verb: a backlog of unread rows alone ends no_op, round one's clean report

- File: `src/cratekit/tagging/backlog_cli.py`
- Source: `u292.json`, row `M16_outcome_over_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1082 against a baseline of 1082
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_rows_whose_file_is_not_here_are_counted_and_said`

Old text:

```
        outcome=Outcome.OK if plan.rows or plan.unread or plan.joining else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if plan.rows else Outcome.NO_OP,
```

### `u322.M22_backlog_partly_clause_gone`

backlog_cli.advisories: the partly read clause is dropped, so the campaign's gate says nothing of Beatport

- File: `src/cratekit/tagging/backlog_cli.py`
- Source: `u322.json`, row `M22_backlog_partly_clause_gone`
- Moved: Same clause in advisories; U298 renamed _named to the public named
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`

Old text:

```
    if unread.partly:
        parts.append(
            f"{unread.partly_by} could not be read for {len(unread.partly)} row(s) "
            f"another catalogue answered, {named(list(unread.partly))}, so those were "
```

New text:

```
    if False:
        parts.append(
            f"{unread.partly_by} could not be read for {len(unread.partly)} row(s) "
            f"another catalogue answered, {named(list(unread.partly))}, so those were "
```

### `u322.M24_backlog_line_gone`

backlog_cli.checks: no catalogue line

- File: `src/cratekit/tagging/backlog_cli.py`
- Source: `u322.json`, row `M24_backlog_line_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`
  - `tests/test_tag_backlog.py::test_the_catalogue_line_names_the_rows_the_walk_stopped_before`

Old text:

```
    if plan.catalogue:
        found.append(_check("backlog.catalogue"
```

New text:

```
    if False:
        found.append(_check("backlog.catalogue"
```

### `r791-a.S1_403_blocks`

_BLOCK_STATUSES: drop 403, so Traxsource's Cloudflare 403 reads as unreachable again

- File: `src/cratekit/tagging/catalogues.py`
- Source: `r791-a.json`, row `S1_403_blocks`
- Moved: Anchored where u306-replay-after-d.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 239 against a baseline of 239
- Kills: 11 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_beatport_miss_beside_two_blocked_fallbacks_is_not_a_no_hit`
  - `tests/test_catalogue_searcher.py::test_a_fallbacks_refusal_is_blocked_and_its_outage_unreachable[403 interstitial]`
  - `tests/test_catalogue_searcher.py::test_beatport_answering_403_is_blocked_like_the_fallbacks`
  - `tests/test_catalogue_searcher.py::test_three_refusals_raise_unreachable_and_say_the_fallbacks_were_blocked`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
_BLOCK_STATUSES = frozenset({403, 429})
```

New text:

```
_BLOCK_STATUSES = frozenset({429})
```

### `r791-a.S3_client_challenge_title`

_CHALLENGE_TITLE: forget Bandcamp's Client Challenge title, the measured 200 that read as a miss

- File: `src/cratekit/tagging/catalogues.py`
- Source: `r791-a.json`, row `S3_client_challenge_title`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 239 against a baseline of 239
- Kills: 8 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_client_challenge_page_is_blocked_rather_than_a_miss`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_track_page_unread_is_not_a_miss[challenge]`
  - `tests/test_catalogue_searcher.py::test_a_beatport_miss_beside_two_blocked_fallbacks_is_not_a_no_hit`
  - `tests/test_catalogue_searcher.py::test_a_blocked_bandcamp_track_page_stops_the_walk_over_further_listings`
  - `tests/test_catalogue_searcher.py::test_three_refusals_raise_unreachable_and_say_the_fallbacks_were_blocked`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`

Old text:

```
|client challenge|attention required!)",
```

New text:

```
|attention required!)",
```

### `u281.R1_stop_after_four`

Refusals.stopped: stop only once the count passes the limit, so four refusals are sent, not three

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R1_stop_after_four`
- Moved: Anchored where u306-replay-after-a.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 11 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_a_new_run_asks_again_from_its_first_file`
  - `tests/test_beatport_refusal.py::test_a_searcher_given_no_count_keeps_its_own_for_its_life`
  - `tests/test_beatport_refusal.py::test_a_stopped_beatport_and_a_discogs_with_no_token_refuse_rather_than_decline`
  - `tests/test_beatport_refusal.py::test_a_stopped_catalogue_is_answered_without_a_wait`
  - `tests/test_beatport_refusal.py::test_the_binder_hands_the_run_count_to_the_searcher`
  - `tests/test_beatport_refusal.py::test_the_count_is_per_catalogue_so_a_refusing_one_never_stops_an_answering_one`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
        if self.running.get(source, 0) < self.limit:
```

New text:

```
        if self.running.get(source, 0) <= self.limit:
```

### `u281.R2_limit_two`

REFUSALS_BEFORE_STOP: two rather than three, a moment's challenge stops the run

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R2_limit_two`
- Moved: Anchored where u306-replay-after-a.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 12 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_match_resets_the_count_as_a_miss_does`
  - `tests/test_beatport_refusal.py::test_a_new_run_asks_again_from_its_first_file`
  - `tests/test_beatport_refusal.py::test_a_searcher_given_no_count_keeps_its_own_for_its_life`
  - `tests/test_beatport_refusal.py::test_an_outage_between_refusals_ends_the_run_of_them`
  - `tests/test_beatport_refusal.py::test_blocked_miss_blocked_blocked_does_not_stop_the_run`
  - `tests/test_beatport_refusal.py::test_the_binder_hands_the_run_count_to_the_searcher`
  - `tests/test_beatport_refusal.py::test_the_count_is_per_catalogue_so_a_refusing_one_never_stops_an_answering_one`
  - `tests/test_beatport_refusal.py::test_the_limit_is_three`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
REFUSALS_BEFORE_STOP = 3
```

New text:

```
REFUSALS_BEFORE_STOP = 2
```

### `u281.R3_stopped_reads_miss`

Refusals.stopped: answer a stopped catalogue MISS, the card's merge blocker, a refused file recorded as one no catalogue carries

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R3_stopped_reads_miss`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 8 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_a_stopped_beatport_and_a_discogs_with_no_token_refuse_rather_than_decline`
  - `tests/test_beatport_refusal.py::test_a_stopped_beatport_never_reads_as_a_miss_or_a_clean_no_hit`
  - `tests/test_beatport_refusal.py::test_a_stopped_catalogue_is_answered_without_a_wait`
  - `tests/test_beatport_refusal.py::test_deezer_is_still_not_asked_beside_a_blocked_beatport[not-sent]`
  - `tests/test_beatport_refusal.py::test_the_count_is_per_catalogue_so_a_refusing_one_never_stops_an_answering_one`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
        return SourceOutcome(
            source,
            Answer.BLOCKED,
            note=(
                f"{NOT_SENT}{source} refused
```

New text:

```
        return SourceOutcome(
            source,
            Answer.MISS,
            note=(
                f"{NOT_SENT}{source} refused
```

### `u281.R4_stopped_note_unmarked`

Refusals.stopped: the note loses its not sent head, so the summary counts the unsent files as sent

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R4_stopped_note_unmarked`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 3 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
                f"{NOT_SENT}{source} refused this client on its last {self.limit} "
```

New text:

```
                f"{source} refused this client on its last {self.limit} "
```

### `u281.R7_one_count_for_every_catalogue`

Refusals.heard: count every catalogue's refusals under one key, so a refusing fallback stops Beatport too

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R7_one_count_for_every_catalogue`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 3 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_discogs_is_never_under_the_count`
  - `tests/test_beatport_refusal.py::test_the_count_is_per_catalogue_so_a_refusing_one_never_stops_an_answering_one`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`

Old text:

```
        if self.running.get(source, 0) < self.limit:
```

New text:

```
        if sum(self.running.values()) < self.limit:
```

### `u281.S6_every_title_named_cloudflare`

unread_outcome: name every challenge title Cloudflare's, Bandcamp's own Client Challenge included

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `S6_every_title_named_cloudflare`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 205 against a baseline of 205
- Kills: 2 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_bandcamp_client_challenge_title_is_blocked_and_not_called_cloudflare`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`

Old text:

```
        named = f", a {CLOUDFLARE_CHALLENGE}" if _CLOUDFLARE_TITLE.match(title) else ""
```

New text:

```
        named = f", a {CLOUDFLARE_CHALLENGE}"
```

### `u282.W1_walk_beatport_first`

WALK: Beatport first again, the order before the card

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u282.json`, row `W1_walk_beatport_first`
- Moved: Anchored where u306-replay-after-d.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 43 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_200_challenge_beside_an_unread_discogs_refuses_as_unreachable_not_parse_broken`
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_discogs_first.py::test_a_401_is_sent_once_and_beatport_decides_every_file`
  - `tests/test_discogs_first.py::test_a_beatport_decline_beside_a_refused_token_is_a_decline_and_never_raises`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_a_beatport_miss_keeps_discogs_word_and_is_not_no_hit`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[outage]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[refused]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[reshaped]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[both]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[fallback-only]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[styleless]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[unmapped]`
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_discogs_match_decides_and_beatport_is_not_asked`
  - `tests/test_discogs_first.py::test_a_discogs_miss_asks_beatport_and_beatport_decides`
  - ... and 28 more, see the JSON sidecar

Old text:

```
WALK: tuple[str, ...] = (DISCOGS, BEATPORT)
```

New text:

```
WALK: tuple[str, ...] = (BEATPORT, DISCOGS)
```

### `u282.W2_sources_beatport_first`

SOURCES: Beatport first again, so the summary and its sentences count Beatport first

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u282.json`, row `W2_sources_beatport_first`
- Moved: Anchored where u306-replay-after-d.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_record_and_a_summary_list_discogs_first`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
SOURCES: tuple[str, ...] = (DISCOGS, BEATPORT, TRAXSOURCE, BANDCAMP)
```

New text:

```
SOURCES: tuple[str, ...] = (BEATPORT, DISCOGS, TRAXSOURCE, BANDCAMP)
```

### `u56-catalogue-searcher-and-tag-workers.R7_pacer_does_not_sleep`

The pacer reports an interval it never took, so a headless worker hammers a catalogue at full speed

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R7_pacer_does_not_sleep`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 6 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_no_genre_spends_a_second_fetch_on_the_track_page`
  - `tests/test_catalogue_searcher.py::test_jitter_is_drawn_from_the_injected_random_source`
  - `tests/test_catalogue_searcher.py::test_the_image_fetch_is_paced_and_answers_the_bytes`
  - `tests/test_catalogue_searcher.py::test_the_pacer_sleeps_before_every_fetch_including_the_first`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
        delay = self.minimum_s * (1.0 + self.entropy.random() * self.jitter_fraction)
        self.sleep(delay)
        return delay
```

New text:

```
        delay = self.minimum_s * (1.0 + self.entropy.random() * self.jitter_fraction)
        return delay
```

### `r1184.M19_tag_folder_wiring`

tag folder report: never hand the warning the taxonomy, so the own name answer is dropped

- File: `src/cratekit/tagging/cli.py`
- Source: `r1184.json`, row `M19_tag_folder_wiring`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 289 against a baseline of 289
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
_off_taxonomy_warning(summary, _declared(cfg) if summary.get("off_taxonomy") else None)
```

New text:

```
_off_taxonomy_warning(summary, None)
```

### `r1184.M20_tag_folder_fallback`

tag folder report: drop the catch of an unreadable copy, so the report is refused over a sentence

- File: `src/cratekit/tagging/cli.py`
- Source: `r1184.json`, row `M20_tag_folder_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 289 against a baseline of 289
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
    try:
        return active_taxonomy.load(cfg)
    except CratekitError:
        return None
```

New text:

```
    return active_taxonomy.load(cfg)
```

### `r650-a.B5_artifact_drops_the_key`

The committed item report stops carrying the flag, so the summary reads it back as absent

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `B5_artifact_drops_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
            "off_taxonomy": result.off_taxonomy,
```

New text:

```
(empty)
```

### `r650-a.C4_warning_fires_on_a_clean_sweep`

The empty check goes, so an ordinary folder is warned about a gap it does not have

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C4_warning_fires_on_a_clean_sweep`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_with_nothing_off_taxonomy_carries_no_such_warning`

Old text:

```
    if not counted:
        return ()
```

New text:

```
(empty)
```

### `r650-a.C6_warning_names_no_strings`

The warning says a gap exists and not which word, which is the R24 mistake one verb over

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C6_warning_names_no_strings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
                f"these catalogue answers: {words}. Each word was written onto "
```

New text:

```
                f"these catalogue answers. Each word was written onto "
```

### `r650-a.C7_warning_order_is_the_walk_order`

The strings are listed in commit order, so two runs over one folder disagree

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C7_warning_order_is_the_walk_order`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
    words = ", ".join(sorted(counted))
```

New text:

```
    words = ", ".join(counted)
```

### `r650-a.C8_warning_code_reworded`

The code a log filter reads is reworded, never appended to

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C8_warning_code_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
OFF_TAXONOMY = "tag-folder-off-taxonomy"
```

New text:

```
OFF_TAXONOMY = "tag-folder-unknown-word"
```

### `r650-a.C9_warning_counts_the_wrong_total`

The warning names the file count as the sweep's whole tagged total

- File: `src/cratekit/tagging/cli.py`
- Source: `r650-a.json`, row `C9_warning_counts_the_wrong_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
    files = sum(counted.values())
```

New text:

```
    files = summary.get("tagged", 0)
```

### `r791-b.C1_artifact_answers`

handle: the artifact records only the first source's answer

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C1_artifact_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_four_real_misses_are_no_hit_and_carry_no_unread_warning`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
                for said in result.answers
            ],
```

New text:

```
                for said in result.answers[:1]
            ],
```

### `r791-b.C2_artifact_unread`

handle: the artifact's unread map is always empty

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C2_artifact_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
                if said.source in result.unread
```

New text:

```
                if False
```

### `r791-b.C6_not_asked_excluded`

_unread_warnings: count not-asked as asked, so a Beatport match hides a blocked fallback

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C6_not_asked_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`

Old text:

```
        asked = sum(count for word, count in counted.items() if word != searchers.NOT_ASKED)
```

New text:

```
        asked = sum(count for word, count in counted.items())
```

### `r791-b.C7_parse_break_said`

_unread_warnings: never say a parse break is a defect a rerun will not move

- File: `src/cratekit/tagging/cli.py`
- Source: `r791-b.json`, row `C7_parse_break_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`

Old text:

```
                        if broken
                        else ""
```

New text:

```
                        if False
                        else ""
```

### `r796-c.V1_the_worker_hands_the_seam_over`

handle: stop passing the general catalogue's seam to tag_one, so the verb never asks it

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V1_the_worker_hands_the_seam_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 10 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_four_real_misses_are_no_hit_and_carry_no_unread_warning`

Old text:

```
        published=published.for_taxonomy(declared),
```

New text:

```
        published=None,
```

### `r796-c.V2_blocked_warning_is_the_shops_only`

_unread_warnings: name every source blocked throughout, the general catalogue included, so one refusal is said under two codes

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V2_blocked_warning_is_the_shops_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`

Old text:

```
    for source in searchers.SOURCES:
        counted = answers.get(source) or {}
```

New text:

```
    for source in answers:
        counted = answers.get(source) or {}
```

### `r796-c.V3_some_unread_is_said`

_published_warnings: warn only when the catalogue was unread on every file asked about, so a partial block is counts and no sentence

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V3_some_unread_is_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`

Old text:

```
    if failed:
        seen = "; ".join(f"{word} on {count}" for word, count in unread.items() if count)
```

New text:

```
    if failed and failed == asked:
        seen = "; ".join(f"{word} on {count}" for word, count in unread.items() if count)
```

### `r796-c.V4_no_isrc_is_warned_about`

_published_warnings: never warn about files with no ISRC

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V4_no_isrc_is_warned_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`

Old text:

```
    if bare:
```

New text:

```
    if False:
```

### `r796-c.V5_parse_break_sentence_said_once`

_unread_warnings: read the general catalogue's parse break into the shops' sentence too

- File: `src/cratekit/tagging/cli.py`
- Source: `r796-c.json`, row `V5_parse_break_sentence_said_once`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`

Old text:

```
            for source in searchers.SOURCES
        )
```

New text:

```
            for source in answers
        )
```

### `u192.T4_tag_queue_only_ignored`

tag_folder: ignore --queue-only and drive the sweep

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T4_tag_queue_only_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_label_genre.py`, `tests/test_render_payloads.py`
- Collected: 221 against a baseline of 221
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_genre.py::test_an_unreadable_registry_warns_and_refuses_only_a_sweep_that_named_a_label`
  - `tests/test_label_genre.py::test_the_remedy_names_the_label_by_its_identifier`
  - `tests/test_render_payloads.py::test_a_builder_that_raises_leaves_the_queued_verb_a_success`
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`
  - `tests/test_tag_workers.py::test_a_real_track_beside_the_staging_tree_is_still_queued`
  - `tests/test_tag_workers.py::test_queueing_a_folder_names_the_job_and_the_command_that_drives_it`
  - `tests/test_tag_workers.py::test_tag_folder_queue_only_returns_the_sweep_queued_with_nothing_asked`

Old text:

```
        if foreground.queue_only(ctx.args):
```

New text:

```
        if False:
```

### `u240.M11_needle_is_the_name`

_label_payload: freeze the label's name as its needle, ignoring --match

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M11_needle_is_the_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_the_needles_are_frozen_with_the_genres_when_the_sweep_is_queued`
  - `tests/test_tag_folder_copyright.py::test_two_labels_sharing_a_display_name_never_lend_each_other_a_genre`

Old text:

```
            entry.label_id: {"name": entry.name, "needle": entry.match or entry.name}
```

New text:

```
            entry.label_id: {"name": entry.name, "needle": entry.name}
```

### `u240.M12_raw_line_matched`

copyright_matcher: match the needle against the raw line, mark and year included (round two's first blocker)

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M12_raw_line_matched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_lines_year_never_completes_a_needle[1985 Music-(P) 1985 Music For Nations]`
  - `tests/test_tag_folder_copyright.py::test_a_lines_year_never_completes_a_needle[2020 Vision-\u2117 2020 Vision Quest]`

Old text:

```
        credit = credits[0]
```

New text:

```
        credit = line
```

### `u240.M13_two_way_match`

copyright_matcher: match either way, so a short line inside a long needle names it

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M13_two_way_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_letter_outside_ascii_never_folds_away_from_a_needle[\u6771\u4eac Records-\u2117 2023 Completely Unrelated Records]`
  - `tests/test_tag_folder_copyright.py::test_a_letter_outside_ascii_never_folds_away_from_a_needle[\xc2me-\u2117 2021 Give Me Records]`
  - `tests/test_tag_folder_copyright.py::test_a_line_carrying_only_part_of_a_needle_names_no_label[(P) 2024 Cronos]`
  - `tests/test_tag_folder_copyright.py::test_a_line_carrying_only_part_of_a_needle_names_no_label[\u2117 2023 Barac]`
  - `tests/test_tag_folder_copyright.py::test_a_line_carrying_only_part_of_a_needle_names_no_label[\u2117 2023 Records]`
  - `tests/test_tag_folder_copyright.py::test_a_line_carrying_only_part_of_a_needle_names_no_label[\u2117 2024 Music]`
  - `tests/test_tag_folder_copyright.py::test_a_sublabels_own_line_names_the_sublabel_and_the_parents_names_the_parent`

Old text:

```
        named = [row for row in rows if label_verify.credit_names(row[1], credit)]
```

New text:

```
        named = [row for row in rows if label_verify.labels_match(row[1], credit)]
```

### `u240.M16_genres_joined_by_name`

_copyright_seam: join a label's genre by its display name, round one's second blocker

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M16_genres_joined_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_two_labels_sharing_a_display_name_never_lend_each_other_a_genre`

Old text:

```
        held = genres.get(label_id)
```

New text:

```
        held = next((row for row in genres.values() if isinstance(row, Mapping) and row.get("name") == name), None)
```

### `u240.M17_worker_hands_no_seam`

handle: the worker never builds the copyright seam

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M17_worker_hands_no_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 8 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_label_batch_with_every_catalogue_blocked_lands_tagged_by_label`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_an_unregistered_file_in_the_batch_is_left_untagged_and_its_item_fails`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`
  - `tests/test_tag_folder_copyright.py::test_the_needles_are_frozen_with_the_genres_when_the_sweep_is_queued`
  - `tests/test_tag_folder_copyright.py::test_the_report_names_each_file_by_label_by_catalogue_or_not_at_all`
  - `tests/test_tag_folder_copyright.py::test_the_tails_tag_step_lands_a_label_batch_with_every_catalogue_blocked`
  - `tests/test_tag_folder_copyright.py::test_two_labels_sharing_a_display_name_never_lend_each_other_a_genre`

Old text:

```
        copyright_labels=_copyright_seam(payload),
```

New text:

```
        copyright_labels=None,
```

### `u240.M20_warning_dropped`

_resume: the two label warning never reaches the envelope

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M20_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`

Old text:

```
            + _ambiguous_warnings(summary)

```

New text:

```
(empty)
```

### `u240.M21_failed_sweep_unreported`

_with_report: no ending carries the report, so a failed sweep says nothing of its files

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M21_failed_sweep_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_cancelled_sweep_carries_its_report_too`
  - `tests/test_tag_folder_copyright.py::test_a_refusal_names_ten_failed_files_and_counts_the_rest`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`

Old text:

```
    if job.state not in _REPORTED_ENDINGS:
```

New text:

```
    if True:
```

### `u240.M23_cap_lowered`

_with_report: name three failed files rather than ten

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M23_cap_lowered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_refusal_names_ten_failed_files_and_counts_the_rest`

Old text:

```
_FAILED_NAMED = 10
```

New text:

```
_FAILED_NAMED = 3
```

### `u281.C1_refusal_said_as_blocked`

_unread_phrase: say a refusal as 'blocked on N' again, the wording the card replaces

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C1_refusal_said_as_blocked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_beatport_refusal.py`
- Collected: 138 against a baseline of 138
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_some_of_whose_refusals_were_a_challenge_says_how_many`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`

Old text:

```
    if word != searchers.Answer.BLOCKED.value:
        return f"{source} {word} on {count}"
```

New text:

```
    if True:
        return f"{source} {word} on {count}"
```

### `u281.C4_source_blocked_counts_unsent_as_sent`

_unread_warnings: count the unsent files among the searches sent, so the warning claims searches never made

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C4_source_blocked_counts_unsent_as_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
        sent = asked - held
```

New text:

```
        sent = asked
```

### `u281.C5_partial_challenge_called_whole`

_unread_phrase: call every refusal a challenge when any one was

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C5_partial_challenge_called_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_some_of_whose_refusals_were_a_challenge_says_how_many`

Old text:

```
    if challenged >= count:
```

New text:

```
    if challenged:
```

### `u281.W7_worker_run_key_without_attempt`

tagging.cli.handle: name the run by the job alone, so a resumed run inherits the last run's stop

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `W7_worker_run_key_without_attempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_beatport_refusal.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
            declared, refusals=searchers.for_run(f"{job.job_id}@{job.attempts}")
```

New text:

```
            declared, refusals=searchers.for_run(f"{job.job_id}")
```

### `u282.C2_refused_token_not_warned`

_discogs_warnings: the refused token's warning is never raised

- File: `src/cratekit/tagging/cli.py`
- Source: `u282.json`, row `C2_refused_token_not_warned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tag_suggest.py`
- Collected: 443 against a baseline of 443
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
    if refused:
        warnings.append(
```

New text:

```
    if False:
        warnings.append(
```

### `u284.C5_sweep_stop_unsaid`

tagging.cli._with_report: the sweep's own refusal says nothing of who refused

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C5_sweep_stop_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token`

Old text:

```
    if stop:
        # WHO REFUSED
```

New text:

```
    if False:
        # WHO REFUSED
```

### `u289.C1_record_drops_asked`

the sweep's record leaves the question's read out

- File: `src/cratekit/tagging/cli.py`
- Source: `u289.json`, row `C1_record_drops_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_the_sweeps_record_names_the_question_each_file_was_asked`

Old text:

```
                "read": result.asked_read,
```

New text:

```
                "read": "",
```

### `u56-catalogue-searcher-and-tag-workers.R19_folder_queues_no_items`

The zero item rule broken at its source: a job with nothing to claim drives straight to SUCCEEDED over a folder nothing walked

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R19_folder_queues_no_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 41 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_real_track_beside_the_staging_tree_is_still_queued`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_retried_job_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_a_searcher_that_raises_part_way_fails_only_its_own_item`
  - ... and 26 more, see the JSON sidecar

Old text:

```
            item_ids=tuple(str(path.relative_to(folder)) for path in files),
```

New text:

```
            item_ids=(),
```

### `u56-catalogue-searcher-and-tag-workers.R20_unnamed_folder_sweeps_cwd`

Path("") is the current directory, so an unnamed folder writes genres into whatever the person is standing in

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R20_unnamed_folder_sweeps_cwd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_empty_folder_argument_never_sweeps_the_working_directory`

Old text:

```
    named = str(ctx.args.folder or "")
    if not named.strip():
```

New text:

```
    named = str(ctx.args.folder or "")
    if False:
```

### `u56-catalogue-searcher-and-tag-workers.R21_two_zeroes_read_as_one`

A mistyped path reports as a folder with nothing to tag, which is the answer most likely to stop somebody looking

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R21_two_zeroes_read_as_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`

Old text:

```
            if folder.is_dir()
            else _empty(
                "tag-folder-absent",
```

New text:

```
            if True
            else _empty(
                "tag-folder-absent",
```

### `u56-catalogue-searcher-and-tag-workers.R22_vanished_file_reports_done`

An item whose file is gone reports done having tagged nothing, which is the clean report over unreadable state the merge bar names

- File: `src/cratekit/tagging/cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R22_vanished_file_reports_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`

Old text:

```
    path = folder / item.item_id
    if not path.is_file():
```

New text:

```
    path = folder / item.item_id
    if False:
```

### `u84-b.C1_artifact_carries_status`

The item artifact drops the repair status, so nothing on disk records what the repair did

- File: `src/cratekit/tagging/cli.py`
- Source: `u84-b.json`, row `C1_artifact_carries_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`

Old text:

```
            "art_repair": result.art_repair,

```

New text:

```
(empty)
```

### `u85-a.A15_worker_hands_in_the_fetch`

The worker passes no image fetch, so the verb never embeds art

- File: `src/cratekit/tagging/cli.py`
- Source: `u85-a.json`, row `A15_worker_hands_in_the_fetch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`

Old text:

```
        fetch_image=searchers.for_images(),

```

New text:

```
(empty)
```

### `u244.M01_no_token_not_asked`

DiscogsAsker.ask: answer MISS for a searcher with no token instead of not-asked, so a sweep with no token records no-hit

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M01_no_token_not_asked`
- Moved: Anchored where u306-replay-after-c2.json replayed it: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tag_suggest.py`, `tests/test_catalogue_searcher.py`, `tests/test_published_genre.py`
- Collected: 470 against a baseline of 470
- Kills: 11 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_file_swept_without_a_token_is_sources_unread_not_no_hit`
  - `tests/test_discogs_searcher.py::test_a_recorded_token_the_keychain_lost_is_not_asked_and_says_so`
  - `tests/test_discogs_searcher.py::test_a_searcher_built_with_no_asker_has_no_token_and_reads_no_keychain`
  - `tests/test_discogs_searcher.py::test_a_walk_that_asked_nothing_is_a_decline_naming_what_it_passed_over`
  - `tests/test_discogs_searcher.py::test_beatport_unreachable_and_discogs_unasked_refuse_as_an_outage_naming_the_token`
  - `tests/test_discogs_searcher.py::test_no_recorded_token_reads_no_keychain_and_is_not_asked`
  - `tests/test_discogs_searcher.py::test_no_token_is_not_asked_with_how_to_record_one_and_never_no_hit`
  - `tests/test_discogs_searcher.py::test_the_general_catalogue_is_still_asked_beside_an_unasked_discogs`
  - `tests/test_tag_suggest.py::test_rows_unread_only_by_a_catalogue_nobody_asked_do_not_stop_the_walk`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`

Old text:

```
        if self.token is None:
            return NotAsked(DISCOGS, self.unasked)
```

New text:

```
        if self.token is None:
            return SourceOutcome(DISCOGS, Answer.MISS)
```

### `u244.M02_rejection_remembered`

DiscogsAsker.ask: forget a rejected token, so it is resent on every later file

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M02_rejection_remembered`
- Moved: Anchored where u306-replay-after-d.json replayed it: DiscogsAsker moved verbatim from tagging/searchers.py to tagging/discogs.py, where the text occurs once, in DiscogsAsker.ask; the identical line in tagging/cyanite.py is Cyanite's own guard and not this one
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tag_suggest.py`
- Collected: 262 against a baseline of 262
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_rejected_token_is_not_sent_again_in_the_run`
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
        if self.rejected is not None:
```

New text:

```
        if False:
```

### `u289.S4_discogs_asked_head`

DiscogsAsker._search: ask the track field with the file's own text

- File: `src/cratekit/tagging/discogs.py`
- Source: `u289.json`, row `S4_discogs_asked_head`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 27 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_headed_title_tag_asks_discogs_past_its_head_and_takes_its_match`
  - `tests/test_discogs_question.py::test_a_name_that_reads_to_no_one_split_is_asked_with_no_artist_and_says_so`
  - `tests/test_discogs_question.py::test_a_title_tag_with_no_artist_tag_is_never_split_by_its_name`
  - `tests/test_discogs_question.py::test_an_mp3_marked_title_tag_carries_no_marker_into_the_question`
  - `tests/test_discogs_question.py::test_an_mp3_named_untagged_file_carries_no_marker_into_the_question`
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_discogs_question.py::test_an_untagged_file_named_artist_and_title_takes_the_release_that_names_both`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[04A - 126 - Burning (Extended Mix)-04A]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[04A - 126 - Burning (Extended Mix)-126]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[04A - 126 - Burning (Extended Mix)-Burning (Original Mix)]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[04A - 126 - Burning (Extended Mix)-Burning]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[04A - 126 - Dub-Dub (Original Mix)]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[08A - 124 - (Intro)-Intro]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[08A - 124 - (Not Just) Knee Deep (Part 1)-Knee Deep]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[08A - 124 - 1998 (Original Mix)-1998]`
  - ... and 12 more, see the JSON sidecar

Old text:

```
        bare = _last_group_stripped(track.strip()) or track.strip()
```

New text:

```
        bare = _last_group_stripped(title.strip()) or title.strip()
```

### `u318.S01_track_needs_the_mix`

_release_carries: a track matching title and artist counts whatever its mix, the sitting's defect

- File: `src/cratekit/tagging/discogs.py`
- Source: `u318.json`, row `S01_track_needs_the_mix`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 32 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[Sunrise Mood (Mike's (Dub) Mix)-Sunrise Mood]`
  - `tests/test_discogs_version.py::test_a_different_spelling_is_still_another_maker[Stra\xdfe-Strase]`
  - `tests/test_discogs_version.py::test_a_different_spelling_is_still_another_maker[Trentem\xf8ller-Trentemoeller]`
  - `tests/test_discogs_version.py::test_a_different_spelling_is_still_another_maker[\u0110or\u0111e-Dorje]`
  - `tests/test_discogs_version.py::test_a_different_spelling_is_still_another_maker[\xc6ther-Ather]`
  - `tests/test_discogs_version.py::test_a_different_spelling_is_still_another_maker[\xde\xf3r-Tor]`
  - `tests/test_discogs_version.py::test_a_mix_named_by_a_word_no_list_holds_is_read_as_its_makers`
  - `tests/test_discogs_version.py::test_a_named_mix_after_a_description_still_names_its_maker`
  - `tests/test_discogs_version.py::test_a_refused_release_gives_way_to_a_later_one_that_carries_the_mix`
  - `tests/test_discogs_version.py::test_a_remix_takes_nothing_from_a_release_of_the_plain_title_and_another_remix`
  - `tests/test_discogs_version.py::test_a_title_naming_two_mixes_lists_them_in_order_in_the_note`
  - `tests/test_discogs_version.py::test_an_article_is_folded_out_of_a_makers_name_on_both_sides`
  - `tests/test_discogs_version.py::test_an_unread_release_beside_a_version_refusal_is_unread_not_a_miss`
  - `tests/test_discogs_version.py::test_another_maker_is_still_a_version_miss_with_the_note`
  - `tests/test_discogs_version.py::test_another_version_or_none_takes_nothing[08A - 124 - X (A Remix)-X (Original Mix)]`
  - ... and 17 more, see the JSON sidecar

Old text:

```
                if not named or titles.writes_version(track_title, named, titled=True):
```

New text:

```
                if True:
```

### `r1967.M01_mint_with_a_row`

plan_set: drop the no row condition, so a plan mints beside an active row of the name

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M01_mint_with_a_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 27 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_file_that_moved_since_the_plan_is_named_and_its_row_left`
  - `tests/test_tag_set.py::test_a_file_that_will_not_take_the_genre_refuses_after_the_rest_landed`
  - `tests/test_tag_set.py::test_a_genre_with_no_lookup_row_is_planned_to_be_made_and_a_tombstone_is_not_its_row`
  - `tests/test_tag_set.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_set.py::test_a_second_run_plans_nothing_and_writes_nothing`
  - `tests/test_tag_set.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_set.py::test_the_apply_writes_the_genre_on_file_and_row_and_nothing_else`
  - `tests/test_tag_set.py::test_the_policy_registered_is_the_retag_genres_and_no_creation_is_asked_for`
  - `tests/test_tag_set.py::test_the_restore_puts_the_files_and_rows_back`
  - `tests/test_tag_set.py::test_the_session_record_keeps_each_written_files_old_genre`
  - `tests/test_tag_set_move.py::test_a_candy_membership_added_after_the_approval_keeps_the_favorites_and_the_job_finishes`
  - `tests/test_tag_set_move.py::test_a_derived_membership_added_after_the_approval_refuses_the_move_stale`
  - `tests/test_tag_set_move.py::test_a_favourite_with_no_vocal_sub_leaves_the_old_favorites`
  - `tests/test_tag_set_move.py::test_a_genre_given_again_after_the_approval_refuses_the_move_stale`
  - `tests/test_tag_set_move.py::test_a_genre_move_is_spent_only_when_every_move_of_its_track_finished`
  - ... and 12 more, see the JSON sidecar

Old text:

```
        mint=genre_row is None and any(item.row_writes for item in items),
```

New text:

```
        mint=any(item.row_writes for item in items),
```

### `r1967.M02_mint_for_a_file_alone`

plan_set: mint for any written item, so a file written alone makes a row nothing links

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M02_mint_for_a_file_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_nothing_is_made_for_a_file_alone`

Old text:

```
        mint=genre_row is None and any(item.row_writes for item in items),
```

New text:

```
        mint=genre_row is None and any(item.action == WRITE for item in items),
```

### `r1967.M03_never_mint`

plan_set: never mint, so a genre with no row is planned as written and the apply cannot link it

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M03_never_mint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_declined_gate_says_the_row_would_be_made_and_makes_none`
  - `tests/test_tag_set.py::test_a_genre_with_no_lookup_row_is_planned_to_be_made_and_a_tombstone_is_not_its_row`
  - `tests/test_tag_set.py::test_a_row_made_between_the_gate_and_the_apply_refuses_stale`
  - `tests/test_tag_set.py::test_a_row_made_by_another_hand_after_the_plan_refuses_before_any_file`
  - `tests/test_tag_set.py::test_nothing_is_made_when_no_file_takes_the_genre`
  - `tests/test_tag_set.py::test_one_row_is_made_for_many_rows_beside_a_tombstone_and_the_commit_names_the_genre_table`
  - `tests/test_tag_set.py::test_the_restore_takes_the_made_row_back`

Old text:

```
        mint=genre_row is None and any(item.row_writes for item in items),
```

New text:

```
        mint=False,
```

### `r1967.M04_gate_hides_mint`

SetPlan.shown_row: show none for a mint, so the gate and the digest say no row is made

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M04_gate_hides_mint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_genre_with_no_lookup_row_is_planned_to_be_made_and_a_tombstone_is_not_its_row`
  - `tests/test_tag_set.py::test_a_row_made_between_the_gate_and_the_apply_refuses_stale`

Old text:

```
        return self.genre_row or (MINT if self.mint else NO_ROW)
```

New text:

```
        return self.genre_row or NO_ROW
```

### `r1967.M05_stale_count_takes_the_lookup_row`

assert_plan_unchanged: count the lookup row among the named rows moved, so the refusal says a row moved that did not

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M05_stale_count_takes_the_lookup_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_row_made_after_the_gate_refuses_stale_on_the_write_handle`

Old text:

```
        f"the plan taken again is not the approved plan ({rows_moved} named row(s) "
```

New text:

```
        f"the plan taken again is not the approved plan ({len(moved)} named row(s) "
```

### `r1967.M06_stale_names_no_lookup_row`

assert_plan_unchanged: leave the lookup row out of what moved, so the refusal names nothing

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M06_stale_names_no_lookup_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_row_made_after_the_gate_refuses_stale_on_the_write_handle`

Old text:

```
    if approved.shown_row != again.shown_row:
        moved.append
```

New text:

```
    if False:
        moved.append
```

### `r1967.M07_no_check_before_files`

apply_set: drop the check before any file, so a row made since the plan is duplicated

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M07_no_check_before_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_row_made_by_another_hand_after_the_plan_refuses_before_any_file`

Old text:

```
    if plan.mint:
        _assert_none_active(db, plan.genre)

```

New text:

```
(empty)
```

### `r1967.M08_check_passes_a_found_row`

_assert_none_active: answer as if no row were found, so a second row of the name is made

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M08_check_passes_a_found_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_row_made_by_another_hand_after_the_plan_refuses_before_any_file`

Old text:

```
    if found is None:
        return
    raise refuse(
```

New text:

```
    if True:
        return
    raise refuse(
```

### `r1967.M09_mint_always`

_write_rows: mint whatever the plan says, so a genre with an active row gets a second

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M09_mint_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_the_policy_registered_is_the_retag_genres_and_no_creation_is_asked_for`

Old text:

```
    done["minted"] = _mint_genre(db, plan.genre) if plan.mint else ""
```

New text:

```
    done["minted"] = _mint_genre(db, plan.genre)
```

### `r1967.M10_mint_never_at_the_write`

_write_rows: make no row when the plan mints, so the rows cannot be linked

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M10_mint_never_at_the_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set.py::test_one_row_is_made_for_many_rows_beside_a_tombstone_and_the_commit_names_the_genre_table`
  - `tests/test_tag_set.py::test_the_restore_takes_the_made_row_back`

Old text:

```
    done["minted"] = _mint_genre(db, plan.genre) if plan.mint else ""
```

New text:

```
    done["minted"] = ""
```

### `r1967.M11_creations_always`

_write_rows: ask for the genre table on every commit, made or not

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M11_creations_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_the_policy_registered_is_the_retag_genres_and_no_creation_is_asked_for`

Old text:

```
    rb_writer.commit_guarded(db, creations=(rb_writer.GENRE_TABLE,) if done["minted"] else ())
```

New text:

```
    rb_writer.commit_guarded(db, creations=(rb_writer.GENRE_TABLE,))
```

### `r1967.M12_creations_never`

_write_rows: ask for nothing when a row was made, so the guard must refuse the commit

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M12_creations_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set.py::test_one_row_is_made_for_many_rows_beside_a_tombstone_and_the_commit_names_the_genre_table`
  - `tests/test_tag_set.py::test_the_restore_takes_the_made_row_back`

Old text:

```
    rb_writer.commit_guarded(db, creations=(rb_writer.GENRE_TABLE,) if done["minted"] else ())
```

New text:

```
    rb_writer.commit_guarded(db, creations=())
```

### `r1967.M14_uuid_constant`

_mint_genre: give every minted row one UUID

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M14_uuid_constant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_one_row_is_made_for_many_rows_beside_a_tombstone_and_the_commit_names_the_genre_table`

Old text:

```
        ID=str(db.generate_unused_id(tables.DjmdGenre)), Name=genre, UUID=str(uuid4())
```

New text:

```
        ID=str(db.generate_unused_id(tables.DjmdGenre)), Name=genre, UUID="u"
```

### `r1967.M15_minted_unreported`

apply_set: leave the minted row out of what the apply answers

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M15_minted_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set.py::test_one_row_is_made_for_many_rows_beside_a_tombstone_and_the_commit_names_the_genre_table`
  - `tests/test_tag_set.py::test_the_restore_takes_the_made_row_back`

Old text:

```
        minted=str(done["minted"]),

```

New text:

```
(empty)
```

### `r1967.M16_minted_name_lowered`

_mint_genre: make the row under another spelling of the genre, so the rows link a word no folder files by

- File: `src/cratekit/tagging/genre_set.py`
- Source: `r1967.json`, row `M16_minted_name_lowered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set.py::test_one_row_is_made_for_many_rows_beside_a_tombstone_and_the_commit_names_the_genre_table`
  - `tests/test_tag_set.py::test_the_restore_takes_the_made_row_back`

Old text:

```
Name=genre, UUID=str(uuid4())
```

New text:

```
Name=genre.lower(), UUID=str(uuid4())
```

### `u339.M11_file_writes`

plan_set: every write rewrites the file, an agreeing one too

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M11_file_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set.py::test_only_the_surface_that_differs_is_planned`
  - `tests/test_tag_set.py::test_the_session_record_keeps_each_written_files_old_genre`

Old text:

```
                file_writes=file_word != genre, row_writes=row_word != genre,
```

New text:

```
                file_writes=True, row_writes=row_word != genre,
```

### `u339.M12_leaves_held`

_leaves: a row the tree does not hold in its old folder still leaves it

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M12_leaves_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_row_leaves_the_folder_its_old_genre_filed_it_in_only_where_the_tree_holds_it`
  - `tests/test_tag_set_move.py::test_a_genre_moved_back_asks_nothing_of_the_old_folder`

Old text:

```
    return was if held.holds(was, content_id) else ""
```

New text:

```
    return was
```

### `u339.M13_digest_leaves`

Item.digested: the folder a row leaves is not digested

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M13_digest_leaves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_row_leaves_the_folder_its_old_genre_filed_it_in_only_where_the_tree_holds_it`

Old text:

```
            "leaves": self.leaves,
        }
```

New text:

```
        }
```

### `u339.M14_stale_check`

assert_plan_unchanged: a plan that moved is applied

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M14_stale_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_file_changed_after_the_gate_refuses_stale_on_the_write_handle`
  - `tests/test_tag_set.py::test_a_file_gone_between_the_plan_and_the_apply_writes_nothing`
  - `tests/test_tag_set.py::test_a_row_made_after_the_gate_refuses_stale_on_the_write_handle`

Old text:

```
    if again.digest == approved.digest:
        return
```

New text:

```
    if True:
        return
```

### `u339.M15_file_reread`

write_files: a file changed since the plan is written over

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M15_file_reread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_file_that_moved_since_the_plan_is_named_and_its_row_left`

Old text:

```
        if word != item.file or outcome == rows.FILE_UNREADABLE:
            moved.append
```

New text:

```
        if False:
            moved.append
```

### `u339.M16_record_before`

apply_set: the record keeps no file's old genre, so a restore puts none back

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M16_record_before`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_set.py::test_the_restore_puts_the_files_and_rows_back`
  - `tests/test_tag_set.py::test_the_restore_takes_the_made_row_back`
  - `tests/test_tag_set.py::test_the_session_record_keeps_each_written_files_old_genre`

Old text:

```
[item.before() for item in writes if item.file_writes]
```

New text:

```
[]
```

### `u339.M17_row_needs_file`

apply_set: a row is written though its file did not take the genre

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M17_row_needs_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_file_that_moved_since_the_plan_is_named_and_its_row_left`
  - `tests/test_tag_set.py::test_a_file_that_will_not_take_the_genre_refuses_after_the_rest_landed`
  - `tests/test_tag_set.py::test_nothing_is_made_when_no_file_takes_the_genre`

Old text:

```
if item.content_id in landed and item.row_writes]
```

New text:

```
if item.row_writes]
```

### `u339.M1_genre_declared`

assert_declared: accept any genre, so an undeclared word reaches the plan

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M1_genre_declared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_an_undeclared_genre_refuses_before_the_acknowledgment_and_any_read`

Old text:

```
    if suggest.suggestable(declared, word):
        return word
```

New text:

```
    if True:
        return word
```

### `u339.M2_path_whole_name`

_nodes_at: a node whose name is only a prefix of the rest counts as the whole path

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M2_path_whole_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_playlist_names_its_live_rows_in_its_order`
  - `tests/test_tag_set.py::test_a_playlist_path_naming_no_plain_playlist_refuses[absent]`
  - `tests/test_tag_set.py::test_a_playlist_path_naming_no_plain_playlist_refuses[smart]`
  - `tests/test_tag_set.py::test_a_playlist_under_a_folder_whose_name_holds_the_separator_is_found`
  - `tests/test_tag_set.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_set.py::test_two_nodes_of_one_name_refuse`

Old text:

```
        if rest == name:
            found.append((node, here))
```

New text:

```
        if rest.startswith(name):
            found.append((node, here))
```

### `u339.M3_path_two_nodes`

playlist_members: two nodes at one path no longer refuse

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M3_path_two_nodes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_two_nodes_of_one_name_refuse`

Old text:

```
    if len(matches) > 1:
```

New text:

```
    if len(matches) > 2:
```

### `u339.M4_path_folder`

playlist_members: a folder or a smart playlist is taken as a playlist

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M4_path_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_playlist_path_naming_no_plain_playlist_refuses[a-folder]`
  - `tests/test_tag_set.py::test_a_playlist_path_naming_no_plain_playlist_refuses[smart]`

Old text:

```
    if attribute != 0:
```

New text:

```
    if attribute == 9:
```

### `u339.M5_removed_member`

playlist_members: a removed membership is read as a member

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M5_removed_member`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_playlist_names_its_live_rows_in_its_order`
  - `tests/test_tag_set.py::test_planned_written_and_read_back_through_the_two_acts`

Old text:

```
        if not rb_writer.membership_removed(song)
    ]
    songs.sort
```

New text:

```
        if True
    ]
    songs.sort
```

### `u339.M7_multi_valued`

plan_set: a file holding two genres is written over

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M7_multi_valued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_file_holding_two_genres_is_left_and_both_are_shown`

Old text:

```
        elif rows._file_words(Path(path)):
```

New text:

```
        elif False:
```

### `u339.M8_held_out`

plan_set: --leave holds nothing out

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M8_held_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_row_held_out_is_listed_and_a_held_identifier_naming_none_is_carried`
  - `tests/test_tag_set.py::test_nothing_is_to_be_made_when_no_row_is_to_link_it`

Old text:

```
        elif content_id in held_out:
            reason = HELD_OUT
```

New text:

```
        elif False:
            reason = HELD_OUT
```

### `u339.M9_already`

plan_set: a row agreeing on one surface only reads as already that genre

- File: `src/cratekit/tagging/genre_set.py`
- Source: `u339.json`, row `M9_already`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set.py::test_nothing_is_made_for_a_file_alone`
  - `tests/test_tag_set.py::test_only_the_surface_that_differs_is_planned`

Old text:

```
        elif file_word == genre and row_word == genre:
```

New text:

```
        elif file_word == genre or row_word == genre:
```

### `r1967.C01_never_say_to_make`

_to_make: never warn, so a declined gate does not say a row would be made

- File: `src/cratekit/tagging/genre_set_cli.py`
- Source: `r1967.json`, row `C01_never_say_to_make`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_declined_gate_says_the_row_would_be_made_and_makes_none`

Old text:

```
    if not plan.mint:
        return []
    return [warning(
        GENRE_ROW_TO_MAKE,
```

New text:

```
    if True:
        return []
    return [warning(
        GENRE_ROW_TO_MAKE,
```

### `r1967.C03_payload_hides_mint`

_payload: show none for a mint in the plan's totals

- File: `src/cratekit/tagging/genre_set_cli.py`
- Source: `r1967.json`, row `C03_payload_hides_mint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_a_genre_with_no_lookup_row_is_planned_to_be_made_and_a_tombstone_is_not_its_row`

Old text:

```
        genre_row=plan.shown_row,
        playlist=plan.playlist,
```

New text:

```
        genre_row=plan.genre_row or gs.NO_ROW,
        playlist=plan.playlist,
```

### `r1967.C04_written_hides_the_row_made`

_written: never name the row made, so the answer and the restore line omit it

- File: `src/cratekit/tagging/genre_set_cli.py`
- Source: `r1967.json`, row `C04_written_hides_the_row_made`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`, `tests/test_rb_writer_guard.py`
- Collected: 291 against a baseline of 291
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set.py::test_the_restore_takes_the_made_row_back`

Old text:

```
        if written.minted
        else ""
    )
    taken
```

New text:

```
        if False
        else ""
    )
    taken
```

### `u172-b.A14_write_false_trusted`

write: trust the writer's answer, so a file that would not take the genre is reported guessed

- File: `src/cratekit/tagging/guess.py`
- Source: `u172-b.json`, row `A14_write_false_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_that_will_not_take_its_genre_is_never_reported_guessed`

Old text:

```
        if not tags.write_genre(item.path, item.genre):
```

New text:

```
        if tags.write_genre(item.path, item.genre) and False:
```

### `u172-b.A16_tombstone_votes`

library_by_artist: a soft deleted row votes

- File: `src/cratekit/tagging/guess.py`
- Source: `u172-b.json`, row `A16_tombstone_votes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_soft_deleted_row_is_no_neighbour`

Old text:

```
        if trees.soft_delete_marker(row):
            continue
```

New text:

```
        if False:
            continue
```

### `u172.A10_tie_not_broken_by_artist`

_broken: a split goes to the first by name only, ignoring the artist's weight

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A10_tie_not_broken_by_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_three_way_tie_goes_to_the_artist_then_to_the_name`

Old text:

```
    return sorted(tied, key=lambda word: (-artist.get(word, 0), word))[0]
```

New text:

```
    return sorted(tied)[0]
```

### `u172.A11_split_not_written`

plan: a split writes no genre, contrary to Phillip's write every guess

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A11_split_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_three_way_tie_goes_to_the_artist_then_to_the_name`
  - `tests/test_tag_guess.py::test_a_tie_is_warned_with_the_genre_it_was_written_as`
  - `tests/test_tag_guess.py::test_a_tie_no_artist_breaks_goes_to_the_first_by_name`

Old text:

```
        if band == suggest.SPLIT:
            genre = _broken(tied, artist)
```

New text:

```
        if band == suggest.SPLIT:
            genre = ''
```

### `u172.A12_fraction_into_weigh`

plan: drop the exact band, so tag suggest's float band_of decides, the rounds 1 and 2 defect

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A12_fraction_into_weigh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_an_exact_bound_over_a_playlist_and_an_artist_is_banded_exactly`
  - `tests/test_tag_guess.py::test_an_exact_eighty_percent_share_is_high_as_tag_suggest_says`

Old text:

```
        if band in suggest.BANDS:
```

New text:

```
        if False:
```

### `u172.A13_report_writes`

write: drop the report's early return, so --report writes

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A13_report_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_report_writes_nothing_and_says_what_a_run_would`

Old text:

```
    if found.report:
        return found
```

New text:

```
    if False:
        return found
```

### `u172.A15_read_back_skipped`

write: skip the read back, so a file reading back another genre is reported guessed

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A15_read_back_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_that_reads_back_another_genre_is_unwritten`

Old text:

```
        if back != item.genre:
```

New text:

```
        if False:
```

### `u172.A17_bound_read_as_float`

band_of: compare the exact share with the float bound, so an exact eighty percent reads medium

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A17_bound_read_as_float`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_an_exact_bound_over_a_playlist_and_an_artist_is_banded_exactly`
  - `tests/test_tag_guess.py::test_an_exact_eighty_percent_share_is_high_as_tag_suggest_says`
  - `tests/test_tag_guess.py::test_the_exact_band_agrees_with_tag_suggests_on_every_whole_vote[8-10]`

Old text:

```
        if share >= Fraction(str(least)) and total >= votes:
```

New text:

```
        if share >= least and total >= votes:
```

### `u172.A2_tagged_file_is_a_candidate`

plan: drop the fill if empty branch, so a file carrying a genre is guessed and overwritten

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A2_tagged_file_is_a_candidate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_with_a_genre_is_never_a_candidate_and_its_off_taxonomy_word_is_named`
  - `tests/test_tag_guess.py::test_a_folder_that_needs_no_guess_opens_no_library`
  - `tests/test_tag_guess.py::test_a_folders_own_name_in_another_case_is_named_with_its_one_answer`
  - `tests/test_tag_guess.py::test_an_off_taxonomy_word_is_named_with_both_offers`
  - `tests/test_tag_guess.py::test_the_artists_tracks_in_the_folder_vote_too`
  - `tests/test_tag_guess.py::test_the_share_before_and_after_counts_the_files_carrying_a_genre`
  - `tests/test_tag_guess.py::test_the_verb_writes_each_guess_and_never_touches_a_tagged_file`

Old text:

```
        if one.genre:
            if off_taxonomy
```

New text:

```
        if False:
            if off_taxonomy
```

### `u172.A3_off_taxonomy_never_named`

plan: never name an off taxonomy word on a staged file, so the review offers nothing

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A3_off_taxonomy_never_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_with_a_genre_is_never_a_candidate_and_its_off_taxonomy_word_is_named`
  - `tests/test_tag_guess.py::test_a_folders_own_name_in_another_case_is_named_with_its_one_answer`
  - `tests/test_tag_guess.py::test_an_off_taxonomy_word_is_named_with_both_offers`

Old text:

```
            if off_taxonomy(declared, one.genre):
```

New text:

```
            if False:
```

### `u172.A5_same_artist_votes_twice`

_share: keep the artist's own tracks in the playlist's share, so they vote twice

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A5_same_artist_votes_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_track_by_the_same_artist_votes_once_as_the_artists`

Old text:

```
        if not member.genre or (own and artist_key(member.artist) == own):
```

New text:

```
        if not member.genre:
```

### `u172.A6_vote_per_member`

_share: a vote per member rather than one shared voice, so a long playlist drowns the artist

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A6_vote_per_member`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_long_playlist_does_not_drown_three_tracks_by_the_artist`
  - `tests/test_tag_guess.py::test_a_playlist_share_on_an_exact_bound_is_banded_as_the_ints_would_be`
  - `tests/test_tag_guess.py::test_a_three_way_tie_goes_to_the_artist_then_to_the_name`
  - `tests/test_tag_guess.py::test_a_track_by_the_same_artist_votes_once_as_the_artists`
  - `tests/test_tag_guess.py::test_an_exact_bound_over_a_playlist_and_an_artist_is_banded_exactly`

Old text:

```
Fraction(PLAYLIST_WEIGHT * count, total)
```

New text:

```
Fraction(count)
```

### `u172.A7_playlist_weight_halved`

PLAYLIST_WEIGHT: halve the playlist's voice, from four to two

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A7_playlist_weight_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_long_playlist_does_not_drown_three_tracks_by_the_artist`
  - `tests/test_tag_guess.py::test_a_playlist_mostly_of_one_genre_gives_it_to_a_track_no_artist_knows`
  - `tests/test_tag_guess.py::test_a_playlist_share_on_an_exact_bound_is_banded_as_the_ints_would_be`
  - `tests/test_tag_guess.py::test_a_three_way_tie_goes_to_the_artist_then_to_the_name`
  - `tests/test_tag_guess.py::test_a_track_by_the_same_artist_votes_once_as_the_artists`
  - `tests/test_tag_guess.py::test_an_exact_bound_over_a_playlist_and_an_artist_is_banded_exactly`

Old text:

```
PLAYLIST_WEIGHT = 4
```

New text:

```
PLAYLIST_WEIGHT = 2
```

### `u172.A8_artist_weight_halved`

_artist_votes: an artist neighbour weighs one rather than two

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A8_artist_weight_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_long_playlist_does_not_drown_three_tracks_by_the_artist`
  - `tests/test_tag_guess.py::test_a_three_way_tie_goes_to_the_artist_then_to_the_name`
  - `tests/test_tag_guess.py::test_a_track_by_the_same_artist_votes_once_as_the_artists`
  - `tests/test_tag_guess.py::test_an_exact_bound_over_a_playlist_and_an_artist_is_banded_exactly`
  - `tests/test_tag_guess.py::test_an_exact_eighty_percent_share_is_high_as_tag_suggest_says`
  - `tests/test_tag_guess.py::test_the_artists_tracks_in_the_library_give_the_genre`

Old text:

```
        votes[word] += ARTIST_WEIGHT
```

New text:

```
        votes[word] += 1
```

### `u172.A9_folder_artist_ignored`

_artist_votes: the folder's own tracks by the artist give no vote

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A9_folder_artist_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_track_by_the_same_artist_votes_once_as_the_artists`
  - `tests/test_tag_guess.py::test_an_unreadable_library_is_said_and_the_folder_still_votes`
  - `tests/test_tag_guess.py::test_the_artists_tracks_in_the_folder_vote_too`
  - `tests/test_tag_guess.py::test_the_share_before_and_after_counts_the_files_carrying_a_genre`
  - `tests/test_tag_guess.py::test_the_verb_writes_each_guess_and_never_touches_a_tagged_file`

Old text:

```
        if one.path != candidate.path and one.genre and artist_key(one.artist) == own
```

New text:

```
        if False
```

### `r1184.M21_guess_wiring`

tag guess: drop the own name sentence from the off taxonomy warning

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `r1184.json`, row `M21_guess_wiring`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 289 against a baseline of 289
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_folders_own_name_in_another_case_is_named_with_its_one_answer`

Old text:

```
                    + taxonomy_word.own_names(declared, found.off_taxonomy)

```

New text:

```
(empty)
```

### `u172.B1_library_read_for_nothing`

signals: read the library and the pass even when no file needs a genre

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B1_library_read_for_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_folder_that_needs_no_guess_opens_no_library`

Old text:

```
    if not any(one.readable and not one.genre for one in staged):
```

New text:

```
    if False:
```

### `u172.B2_unknown_pass_silent`

_playlists: read a pass no job carries as no playlists, the round 1 defect

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B2_unknown_pass_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_pass_no_job_carries_is_said_and_never_read_as_no_playlists`

Old text:

```
        if not batch_name.pass_jobs(cfg, pass_name):
```

New text:

```
        if False:
```

### `u172.B3_pass_ignored`

signals: never read the pass's playlists

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B3_pass_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_pass_no_job_carries_is_said_and_never_read_as_no_playlists`
  - `tests/test_tag_guess.py::test_a_pass_that_cannot_be_read_is_said_and_the_artist_still_votes`
  - `tests/test_tag_guess.py::test_the_pass_names_the_playlists_that_vote`

Old text:

```
    if pass_name:
        playlists, playlists_unread
```

New text:

```
    if False:
        playlists, playlists_unread
```

### `u172.B4_outcome_ok_always`

tag_guess: answer OK when nothing was written

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B4_outcome_ok_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_that_will_not_take_its_genre_is_never_reported_guessed`
  - `tests/test_tag_guess.py::test_a_folder_that_needs_no_guess_opens_no_library`
  - `tests/test_tag_guess.py::test_a_report_writes_nothing_and_says_what_a_run_would`
  - `tests/test_tag_guess.py::test_no_pass_reads_no_playlist`

Old text:

```
        outcome=Outcome.OK if written else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `r816-d.C2_empty_plan`

tag_rows: open the database to write for a plan that writes nothing

- File: `src/cratekit/tagging/plan_verbs.py`
- Source: `r816-d.json`, row `C2_empty_plan`
- Moved: the check rows_cli.tag_rows made before writing now stands in plan_verbs.applied, which tag_rows returns through, and the text occurs once in plan_verbs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_an_empty_plan_still_asks_and_opens_nothing_to_write`

Old text:

```
    if not plan.writes:
```

New text:

```
    if False:
```

### `r816-d.C3_majority_unmapped`

_plan: plan over a library most of whose rows are under no prefix rule

- File: `src/cratekit/tagging/plan_verbs.py`
- Source: `r816-d.json`, row `C3_majority_unmapped`
- Moved: the refusal rows_cli._plan and two other plan verbs each held now stands once in plan_verbs.reading, which rows_cli._plan opens its handle through
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_library_most_of_whose_rows_are_unmapped_refuses_before_the_gate`

Old text:

```
        if totals.majority_unmapped:
```

New text:

```
        if False:
```

### `u306.C3_applied_written_zero`

What P8 does hold: plan_verbs.applied reports nothing written after a write, so a whole write reads as none

- File: `src/cratekit/tagging/plan_verbs.py`
- Source: `u306.json`, row `C3_applied_written_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`, `tests/test_tag_remap.py`, `tests/test_tag_suggest.py`
- Collected: 224 against a baseline of 224
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_an_approved_plan_is_written_and_the_run_names_the_verb_the_rows_follow_by`
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_suggest.py::test_the_file_and_the_row_carry_the_genre_and_nothing_else_moved`

Old text:

```
    data["totals"] = {**data["totals"], "written": written.written, "read_back": written.read_back}
```

New text:

```
    data["totals"] = {**data["totals"], "written": 0, "read_back": written.read_back}
```

### `u306.P1_named_cap`

plan_verbs.NAMED: a sentence names four rather than five, so every refusal and warning that lists names says one fewer and counts one more

- File: `src/cratekit/tagging/plan_verbs.py`
- Source: `u306.json`, row `P1_named_cap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`, `tests/test_tag_suggest.py`, `tests/test_tag_guess.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_shared_homes.py`
- Collected: 489 against a baseline of 489
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_token_discogs_refused_is_said_and_beatport_is_asked_on_every_row`
  - `tests/test_tag_remap.py::test_the_refusal_names_a_few_files_and_carries_them_all`

Old text:

```
NAMED = 5

```

New text:

```
NAMED = 4

```

### `u306.P3_counted_zeros`

plan_verbs.counted: name every outcome, the ones that did not happen with a zero, in each verb's summary line

- File: `src/cratekit/tagging/plan_verbs.py`
- Source: `u306.json`, row `P3_counted_zeros`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`, `tests/test_tag_remap.py`, `tests/test_tag_suggest.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`

Old text:

```
    return ", ".join(f"{counts[name]} {name}" for name in names if counts[name])
```

New text:

```
    return ", ".join(f"{counts[name]} {name}" for name in names)
```

### `u306.P6_payload_count`

plan_verbs.payload: count the writes rather than every item, so the totals the gate digests and the envelope carries undercount the plan

- File: `src/cratekit/tagging/plan_verbs.py`
- Source: `u306.json`, row `P6_payload_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`, `tests/test_tag_remap.py`, `tests/test_tag_suggest.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`

Old text:

```
        "totals": {"count": len(plan.items), **totals, "written": 0, "read_back": 0},
```

New text:

```
        "totals": {"count": len(plan.writes), **totals, "written": 0, "read_back": 0},
```

### `u306.P7_applied_noop`

plan_verbs.applied: take the no op path only for a plan with no items, so an answered plan of rows to leave alone reaches the write

- File: `src/cratekit/tagging/plan_verbs.py`
- Source: `u306.json`, row `P7_applied_noop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`, `tests/test_tag_remap.py`, `tests/test_tag_suggest.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_run_that_leaves_a_file_says_how_many_and_why_on_every_path`
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`

Old text:

```
    if not plan.writes:
        return ctx.envelope(
```

New text:

```
    if not plan.items:
        return ctx.envelope(
```

### `u306.P9_applied_advisories`

plan_verbs.applied: drop the advisories after a write, so what the plan left alone is told only when nothing was written

- File: `src/cratekit/tagging/plan_verbs.py`
- Source: `u306.json`, row `P9_applied_advisories`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`, `tests/test_tag_remap.py`, `tests/test_tag_suggest.py`
- Collected: 224 against a baseline of 224
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_run_that_wrote_still_says_what_it_left`
  - `tests/test_tag_rows.py::test_a_file_on_a_volume_that_is_not_mounted_is_counted_and_the_run_does_not_fail`
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`
  - `tests/test_tag_rows.py::test_a_word_the_library_has_no_row_for_names_the_act_on_a_run_that_wrote`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_suggest.py::test_the_file_and_the_row_carry_the_genre_and_nothing_else_moved`

Old text:

```
    return ctx.envelope(data=data, warnings=[said(written), *advisories(plan)])
```

New text:

```
    return ctx.envelope(data=data, warnings=[said(written)])
```

### `u322.M20_backlog_uses_folder_binder`

backlog_cli.read_plan: the backlog asks through tag folder's binder, so Deezer is held behind a refusing Beatport

- File: `src/cratekit/tagging/plan_verbs.py`
- Source: `u322.json`, row `M20_backlog_uses_folder_binder`
- Moved: the line backlog_cli.read_plan copied now stands once in plan_verbs.kept, which both tag backlog and tag suggest call, so this row and its twin mutate the one line both copies became
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`
  - `tests/test_tag_suggest.py::test_tag_suggest_asks_deezer_past_a_refusing_beatport_by_each_files_isrc`

Old text:

```
            searchers.for_taxonomy(declared), published.for_suggestions(declared)
```

New text:

```
            searchers.for_taxonomy(declared), published.for_taxonomy(declared)
```

### `r796-a.L1_no_data_is_a_miss`

_error: stop reading the catalogue's 'no data' as a miss, so an ISRC it does not know is an error nobody recognises

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L1_no_data_is_a_miss`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 6 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_track_no_catalogue_knows_with_every_source_read_is_still_no_hit`
  - `tests/test_published_genre.py::test_a_track_whose_album_the_catalogue_does_not_list_is_not_a_miss`
  - `tests/test_published_genre.py::test_an_isrc_the_catalogue_does_not_know_is_a_miss_and_asks_for_no_album`
  - `tests/test_published_genre.py::test_the_request_names_this_tool_and_not_a_browser`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_four_real_misses_are_no_hit_and_carry_no_unread_warning`

Old text:

```
    if code == _NO_DATA:
```

New text:

```
    if False:
```

### `r796-a.L7_a_refusal_is_remembered`

genre_lookup: forget a BLOCKED answer, so the next file asks a catalogue that said stop

- File: `src/cratekit/tagging/published.py`
- Source: `r796-a.json`, row `L7_a_refusal_is_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 4 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_block_on_the_album_is_remembered_too`
  - `tests/test_published_genre.py::test_a_refusal_is_remembered_and_nothing_more_is_asked_in_the_run`
  - `tests/test_published_genre.py::test_a_refusal_on_one_file_reaches_the_next_files_seam`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`

Old text:

```
        if said.answer == Answer.BLOCKED.value:
            refusals.append(said)
```

New text:

```
        if False:
            refusals.append(said)
```

### `r796-b.O3_a_usable_answer_is_never_replaced`

second_opinion: ask the general catalogue about a hit that already has a genre (R4)

- File: `src/cratekit/tagging/published.py`
- Source: `r796-b.json`, row `O3_a_usable_answer_is_never_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 2 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_file_with_no_isrc_whose_genre_a_shop_settled_is_still_not_asked`
  - `tests/test_published_genre.py::test_a_usable_answer_is_never_replaced_and_the_record_says_not_asked`

Old text:

```
        if hit.genre or isrc is None:
```

New text:

```
        if isrc is None:
```

### `r796-b.O5_a_declined_beatport_match_is_asked_about`

_BEATPORT_ANSWERED: count only a miss, so a track Beatport calls by a catch-all is never asked about (R1, AE2)

- File: `src/cratekit/tagging/published.py`
- Source: `r796-b.json`, row `O5_a_declined_beatport_match_is_asked_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 5 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_declined_answer_beside_beatports_own_declined_word_keeps_beatports`
  - `tests/test_published_genre.py::test_a_published_genre_over_beatports_declined_word_is_written_and_keeps_beatports_picture`
  - `tests/test_published_genre.py::test_ae2_two_coarse_answers_write_nothing_and_the_record_shows_both`
  - `tests/test_published_genre.py::test_beatports_picture_is_embedded_under_a_published_genre_and_says_whose_it_is`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`

Old text:

```
_BEATPORT_ANSWERED = (Answer.MATCHED.value, Answer.MISS.value)
```

New text:

```
_BEATPORT_ANSWERED = (Answer.MISS.value,)
```

### `r796-b.O6_unread_joins_the_unread_names`

second_opinion: leave the general catalogue out of the hit's unread names when it could not be read

- File: `src/cratekit/tagging/published.py`
- Source: `r796-b.json`, row `O6_unread_joins_the_unread_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 7 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_blocked_general_catalogue_leaves_the_file_untagged_and_askable`
  - `tests/test_published_genre.py::test_an_unread_general_catalogue_joins_the_unread_names[blocked]`
  - `tests/test_published_genre.py::test_an_unread_general_catalogue_joins_the_unread_names[parse-break]`
  - `tests/test_published_genre.py::test_an_unread_general_catalogue_joins_the_unread_names[unreachable]`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`

Old text:

```
            unread = (*hit.unread, SOURCE) if said.answer in UNREAD else hit.unread
```

New text:

```
            unread = hit.unread
```

### `u322.M19_suggest_binder_flag_off`

for_suggestions: the binder does not ask past a refusing Beatport, so Deezer is asked about no row

- File: `src/cratekit/tagging/published.py`
- Source: `u322.json`, row `M19_suggest_binder_flag_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_the_suggest_binder_is_built_over_the_one_lookup`
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`
  - `tests/test_tag_suggest.py::test_tag_suggest_asks_deezer_past_a_refusing_beatport_by_each_files_isrc`

Old text:

```
    return second_opinion(declared, lookup=for_lookup(), past_a_refusing_shop=True)
```

New text:

```
    return second_opinion(declared, lookup=for_lookup(), past_a_refusing_shop=False)
```

### `u284.R1_since_moves_every_refusal`

refused._change: a later refusal resets since to now, so the date says the latest refusal rather than when it began

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R1_since_moves_every_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_first_refusal_sets_since_and_a_later_one_keeps_it`
  - `tests/test_sync_refused.py::test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token`
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
                    since=before.since if before is not None else now,
```

New text:

```
                    since=now,
```

### `u284.R4_empty_since_read`

refused._parse: an entry with an empty since is read as refusing

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R4_empty_since_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_an_entry_of_the_wrong_shape_is_skipped_and_the_rest_read`

Old text:

```
        if isinstance(since, str) and since and isinstance(last, str)
```

New text:

```
        if isinstance(since, str) and isinstance(last, str)
```

### `u284.R5_count_never_grows`

refused._change: the refusal count stays where it was

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R5_count_never_grows`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_first_refusal_sets_since_and_a_later_one_keeps_it`
  - `tests/test_sync_refused.py::test_a_sweeps_run_count_records_a_refusal_sent_and_not_one_unsent`

Old text:

```
                    count=(before.count if before is not None else 0) + 1,
```

New text:

```
                    count=(before.count if before is not None else 0) + 0,
```

### `u284.R7_deep_record_raises`

refused._parse: a record nested past the parser's depth raises out of every read

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R7_deep_record_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_record_nested_past_the_parsers_depth_reads_as_none_and_is_written_over`

Old text:

```
    except (ValueError, RecursionError):
        # A RECORD NESTED
```

New text:

```
    except ValueError:
        # A RECORD NESTED
```

### `r799-b.P1_a_file_is_planned_only_while_it_carries_what_a_record_wrote`

plan: take every record in force as explaining the file, whatever the file carries

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P1_a_file_is_planned_only_while_it_carries_what_a_record_wrote`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_blank_file_whose_word_is_now_declined_is_not_read_as_agreeing`
  - `tests/test_tag_remap.py::test_a_file_holding_a_second_genre_is_left_alone_and_both_are_shown`
  - `tests/test_tag_remap.py::test_a_file_whose_genre_was_cleared_is_left_alone_and_not_read_as_agreeing`
  - `tests/test_tag_remap.py::test_a_genre_a_record_shop_wrote_later_on_a_path_the_catalogue_once_wrote_agrees`
  - `tests/test_tag_remap.py::test_a_genre_frame_holding_two_values_is_two_values_on_an_id3_container`
  - `tests/test_tag_remap.py::test_a_genre_nobody_recorded_writing_is_left_alone_and_listed[Deep House]`
  - `tests/test_tag_remap.py::test_a_genre_nobody_recorded_writing_is_left_alone_and_listed[Pop]`
  - `tests/test_tag_remap.py::test_a_genre_nobody_recorded_writing_is_left_alone_and_listed[dance / pop]`
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_record_shops_genre_is_never_resolved_as_the_catalogues_word`
  - `tests/test_tag_remap.py::test_a_run_that_leaves_a_file_says_how_many_and_why_on_every_path`
  - `tests/test_tag_remap.py::test_a_run_that_wrote_still_says_what_it_left`
  - `tests/test_tag_remap.py::test_every_file_is_counted_once_and_the_items_are_in_path_order`
  - `tests/test_tag_remap.py::test_only_a_planned_write_is_written`
  - `tests/test_tag_remap.py::test_the_apply_writes_the_planned_genre_and_no_other_file`

Old text:

```
    explaining = [record for record in in_force if values == (record.written,)]
```

New text:

```
    explaining = list(in_force)
```

### `r799-b.P2_two_explanations_are_ambiguous`

plan: settle a genre two records explain differently by the first of them

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P2_two_explanations_are_ambiguous`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_reached_through_a_link_is_the_file`
  - `tests/test_tag_remap.py::test_a_genre_two_records_explain_with_different_sources_is_left`
  - `tests/test_tag_remap.py::test_a_genre_two_records_explain_with_different_words_is_left`
  - `tests/test_tag_remap.py::test_one_file_recorded_under_two_spellings_is_one_file`

Old text:

```
    if len({(record.source, record.word) for record in explaining}) > 1:
```

New text:

```
    if False:
```

### `r799-b.P3_a_shops_genre_is_the_shops`

plan: resolve a record shop's word as the general catalogue's

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P3_a_shops_genre_is_the_shops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_record_shops_genre_is_never_resolved_as_the_catalogues_word`

Old text:

```
    if wrote.source != SOURCE:
```

New text:

```
    if False:
```

### `r799-b.P4_a_rewrite_retires_the_record_it_replaced`

plan: keep every record of the source in force, whatever its generation

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P4_a_rewrite_retires_the_record_it_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_word_given_its_first_genre_back_is_still_followed`

Old text:

```
        if record.source == SOURCE and record.generation == newest
    ]
```

New text:

```
        if record.source == SOURCE
    ]
```

### `r799-b.P5_only_a_file_under_the_library_is_opened`

plan: settle a recorded path wherever it is

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P5_only_a_file_under_the_library_is_opened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_outside_the_library_is_said_and_not_listed`
  - `tests/test_tag_remap.py::test_a_file_outside_this_librarys_root_is_counted_and_never_opened`
  - `tests/test_tag_remap.py::test_a_folder_named_in_another_case_on_a_volume_that_folds_case_is_inside`
  - `tests/test_tag_remap.py::test_a_path_that_climbs_out_of_the_library_is_outside_it`

Old text:

```
        if resolved is None or not _inside(resolved, library):
```

New text:

```
        if resolved is None:
```

### `r799-b.P6_one_file_is_one_group`

plan: key a file under the library by its resolved name and not by the file itself

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `P6_one_file_is_one_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        stat = resolved.stat()
    except OSError:
        return ("name", str(resolved))
    return ("file", stat.st_dev, stat.st_ino)
```

New text:

```
    return ("name", str(resolved))
```

### `r799-b.W1_a_file_is_read_again_before_it_is_written`

apply: write over whatever the file carries by now

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `W1_a_file_is_read_again_before_it_is_written`
- Moved: Same read before the write in apply; U298 replaced the local _file_genres with tagging.tag.file_genres, the identical exact reader
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_that_moved_since_the_plan_is_named_and_not_written`

Old text:

```
        if file_genres(target) != (item.current,):
            moved.append(item.path)
            continue
```

New text:

```
(empty)
```

### `r799-b.W2_the_writers_answer_is_kept`

apply: count a file the writer could not write as written

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `W2_the_writers_answer_is_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_the_writer_could_not_write_is_named_as_untouched_and_the_rest_are_written`
  - `tests/test_tag_remap.py::test_a_refusal_that_rewrote_nothing_does_not_send_a_person_to_the_row_verb`
  - `tests/test_tag_remap.py::test_a_write_that_does_not_take_refuses_after_the_rest_were_written`

Old text:

```
        if not tags.write_genre(target, item.wanted):
            failed.append(item.path)
            continue
```

New text:

```
        tags.write_genre(target, item.wanted)
```

### `r799-b.W3_a_write_is_read_back`

apply: take the writer's word that the genre is on the file

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-b.json`, row `W3_a_write_is_read_back`
- Moved: Same read back in apply; U298 replaced the local _file_genres with tagging.tag.file_genres, the identical exact reader
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_written_that_does_not_read_back_is_named_as_wrong`

Old text:

```
        if file_genres(target) != (item.wanted,):
            wrong.append(item.path)
            continue
```

New text:

```
(empty)
```

### `r799-c.P11_blank_is_not_agreement`

plan: read a blank file whose word is given nothing as agreeing

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-c.json`, row `P11_blank_is_not_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_blank_file_whose_word_is_now_declined_is_not_read_as_agreeing`

Old text:

```
        if any(current and current == _wanted(declared, record.word) for record in mine):
```

New text:

```
        if any(current == _wanted(declared, record.word) for record in mine):
```

### `r799-c.V3_an_unrecorded_rewrite_is_not_clean`

verb: call a run clean whose rewrite could not be recorded

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-c.json`, row `V3_an_unrecorded_rewrite_is_not_clean`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_record_that_cannot_be_committed_is_named_and_the_file_stays_rewritten`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[unrecorded-no record of the rewrite could be committed]`

Old text:

```
        return not (self.wrong or self.moved or self.failed or self.unrecorded)
```

New text:

```
        return not (self.wrong or self.moved or self.failed)
```

### `r799-c.W4_a_rewrite_is_recorded`

apply: commit no record of a rewrite, so the verb's own write reads as a hand edit

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-c.json`, row `W4_a_rewrite_is_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_this_verb_rewrote_is_corrected_again_when_the_word_moves_again`
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_record_that_cannot_be_committed_is_named_and_the_file_stays_rewritten`
  - `tests/test_tag_remap.py::test_a_rewrite_is_recorded_as_a_tagging_record_of_its_own`
  - `tests/test_tag_remap.py::test_a_word_given_its_first_genre_back_is_still_followed`

Old text:

```
        if not _record(cfg, name, ordinal, item):
            unrecorded.append(item.path)
```

New text:

```
(empty)
```

### `r799-c.W5_a_rewrites_record_is_one_generation_on`

apply: record a rewrite at the generation of the record it replaced

- File: `src/cratekit/tagging/remap.py`
- Source: `r799-c.json`, row `W5_a_rewrites_record_is_one_generation_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_this_verb_rewrote_is_corrected_again_when_the_word_moves_again`
  - `tests/test_tag_remap.py::test_a_genre_put_back_by_hand_after_a_rewrite_is_left_alone`
  - `tests/test_tag_remap.py::test_a_rewrite_is_recorded_as_a_tagging_record_of_its_own`
  - `tests/test_tag_remap.py::test_a_word_given_its_first_genre_back_is_still_followed`

Old text:

```
                "generation": item.generation + 1,
```

New text:

```
                "generation": item.generation,
```

### `r799-c.V1_the_gate_is_asked_before_the_write`

verb: apply the plan whatever the gate answers

- File: `src/cratekit/tagging/remap_cli.py`
- Source: `r799-c.json`, row `V1_the_gate_is_asked_before_the_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_file_changed_after_the_answer_makes_the_decision_stale`
  - `tests/test_tag_remap.py::test_a_file_outside_the_library_is_said_and_not_listed`
  - `tests/test_tag_remap.py::test_a_person_reads_the_counts_and_the_pairs_at_the_gate`
  - `tests/test_tag_remap.py::test_a_record_that_could_not_be_parsed_is_said`
  - `tests/test_tag_remap.py::test_a_refusal_that_rewrote_nothing_does_not_send_a_person_to_the_row_verb`
  - `tests/test_tag_remap.py::test_a_run_that_leaves_a_file_says_how_many_and_why_on_every_path`
  - `tests/test_tag_remap.py::test_a_run_that_wrote_still_says_what_it_left`
  - `tests/test_tag_remap.py::test_a_write_that_does_not_take_refuses_after_the_rest_were_written`
  - `tests/test_tag_remap.py::test_an_abort_writes_nothing`
  - `tests/test_tag_remap.py::test_an_active_taxonomy_with_no_table_says_so_and_plans_nothing`
  - `tests/test_tag_remap.py::test_an_approved_plan_is_written_and_the_run_names_the_verb_the_rows_follow_by`
  - `tests/test_tag_remap.py::test_an_empty_plan_still_asks_and_then_writes_nothing`
  - `tests/test_tag_remap.py::test_the_gate_takes_no_inline_answer`
  - `tests/test_tag_remap.py::test_the_shipped_template_declares_the_table_so_the_warning_is_not_given`
  - `tests/test_tag_remap.py::test_the_verb_asks_before_it_writes_and_the_gate_shows_the_plan`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=_advisories(plan))
```

New text:

```
(empty)
```

### `r799-c.V2_a_file_that_did_not_take_refuses`

verb: answer a clean run over a file that did not take its genre

- File: `src/cratekit/tagging/remap_cli.py`
- Source: `r799-c.json`, row `V2_a_file_that_did_not_take_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_remap.py`
- Collected: 93 against a baseline of 93
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_remap.py::test_a_refusal_that_rewrote_nothing_does_not_send_a_person_to_the_row_verb`
  - `tests/test_tag_remap.py::test_a_write_that_does_not_take_refuses_after_the_rest_were_written`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[failed-could not be written and are untouched]`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[moved-carried something else]`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[unrecorded-no record of the rewrite could be committed]`
  - `tests/test_tag_remap.py::test_each_way_a_file_did_not_take_its_genre_refuses_and_says_which[wrong-do not read back]`
  - `tests/test_tag_remap.py::test_the_refusal_names_a_few_files_and_carries_them_all`

Old text:

```
    if written.clean:
        return
    parts = []
```

New text:

```
    if True:
        return
    parts = []
```

### `r1103.S1_answer_too_coarse`

Sample of the unit's existing guards: retag_one writes an answer the taxonomy calls too coarse

- File: `src/cratekit/tagging/retag.py`
- Source: `r1103.json`, row `S1_answer_too_coarse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 222 against a baseline of 222
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_accepted_answer_that_is_itself_a_catch_all_is_still_refused`
  - `tests/test_genre_retag.py::test_an_answer_that_is_itself_a_catch_all_is_refused_and_the_file_is_untouched`
  - `tests/test_tag_workers.py::test_an_answer_that_is_itself_too_coarse_reaches_the_review_queue`
  - `tests/test_tagging_engine.py::test_a_candidate_whose_answer_is_itself_too_coarse_is_refused_per_candidate`

Old text:

```
    if declared.is_too_coarse_as_source(answer):
```

New text:

```
    if False:
```

### `r1103.W1_writer_answer_ignored`

retag_one: drop the check of the writer's answer, so a file that refused reports the genre as written (the defect R-1103 records)

- File: `src/cratekit/tagging/retag.py`
- Source: `r1103.json`, row `W1_writer_answer_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 222 against a baseline of 222
- Kills: 6 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`
  - `tests/test_genre_retag.py::test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run`
  - `tests/test_genre_retag.py::test_an_unwritten_file_never_reaches_the_library_plan`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
    if not tags.write_genre(candidate.path, answer):
```

New text:

```
    if tags.write_genre(candidate.path, answer) and False:
```

### `r1103.W2_unwritten_reason_blank`

retag_one: the unwritten result carries no reason, so it reads as neither written nor refused and the worker commits a report for it

- File: `src/cratekit/tagging/retag.py`
- Source: `r1103.json`, row `W2_unwritten_reason_blank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 222 against a baseline of 222
- Kills: 5 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`
  - `tests/test_genre_retag.py::test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
            reason=UNWRITTEN_REASON,
```

New text:

```
            reason="",
```

### `r1103.W3_unwritten_reason_wrong`

retag_one: the unwritten result carries another selection reason, no-answer, a realistic neighbour that sends it to the asked count

- File: `src/cratekit/tagging/retag.py`
- Source: `r1103.json`, row `W3_unwritten_reason_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 222 against a baseline of 222
- Kills: 5 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`
  - `tests/test_genre_retag.py::test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
            reason=UNWRITTEN_REASON,
```

New text:

```
            reason=NO_ANSWER,
```

### `r1103.W4_unwritten_proposed_dropped`

retag_one: the unwritten result loses the answer it could not write, so the refusal names no genre

- File: `src/cratekit/tagging/retag.py`
- Source: `r1103.json`, row `W4_unwritten_proposed_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 222 against a baseline of 222
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`
  - `tests/test_genre_retag.py::test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`

Old text:

```
            reason=UNWRITTEN_REASON,
            proposed=answer,
```

New text:

```
            reason=UNWRITTEN_REASON,
            proposed="",
```

### `r1103.W6_unwritten_current_swapped`

retag_one: the unwritten result reports the answer as the genre the file still carries

- File: `src/cratekit/tagging/retag.py`
- Source: `r1103.json`, row `W6_unwritten_current_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 222 against a baseline of 222
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`

Old text:

```
    if not tags.write_genre(candidate.path, answer):
        # THE WRITER'S FALSE IS AN UNWRITTEN FILE, NEVER A CORRECTION (R-1103).
        # ``written`` stays None, so :attr:`RetagOutcome.written` leaves the file
        # out and :func:`plan_library` plans no row for it, and the answer it
        # could not take rides as ``proposed`` so the report can name it. A
        # verdict the answer came from stays as it is: the next run reads it
        # again and tries the write again, rather than asking a person twice.
        return RetagResult(
            path=candidate.path,
            current=candidate.current,
```

New text:

```
    if not tags.write_genre(candidate.path, answer):
        # THE WRITER'S FALSE IS AN UNWRITTEN FILE, NEVER A CORRECTION (R-1103).
        # ``written`` stays None, so :attr:`RetagOutcome.written` leaves the file
        # out and :func:`plan_library` plans no row for it, and the answer it
        # could not take rides as ``proposed`` so the report can name it. A
        # verdict the answer came from stays as it is: the next run reads it
        # again and tries the write again, rather than asking a person twice.
        return RetagResult(
            path=candidate.path,
            current=answer,
```

### `r1103.H1_item_not_failed`

handle: drop the refusal for an unwritten result, so the item ends done with a report and the job succeeds over a file that kept its catch-all

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H1_item_not_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_genre_retag.py`
- Collected: 152 against a baseline of 152
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
    if result.reason == retag.UNWRITTEN_REASON:
```

New text:

```
    if False:
```

### `r1103.H2_refusal_slug`

handle: the item fails under the general analysis-write-failed slug instead of retag's own

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H2_refusal_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_reserved_causes.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
        raise refuse(
            retag.UNWRITTEN_REASON,
```

New text:

```
        raise refuse(
            "analysis-write-failed",
```

### `r1103.H3_message_names_no_file`

handle: reword the refusal so it names no file

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H3_message_names_no_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`

Old text:

```
            f"{path} would not take the genre {result.proposed!r}, so it still "
```

New text:

```
            f"the file would not take the genre {result.proposed!r}, so it still "
```

### `r1103.H4_detail_path`

handle: the refusal's detail loses the file's path

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H4_detail_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
                "path": str(path),
```

New text:

```
                "path": "",
```

### `r1103.H5_detail_genre`

handle: the refusal's detail names the genre the file still carries as the one it would not take

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H5_detail_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`

Old text:

```
                "genre": result.proposed,
```

New text:

```
                "genre": result.current,
```

### `r1103.H6_detail_current`

handle: the refusal's detail loses the genre the file still carries

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r1103.json`, row `H6_detail_current`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`

Old text:

```
                "current": result.current,
```

New text:

```
                "current": "",
```

### `r185-r246-author.E3_empty_plan_queues_anyway`

Queue a job over an empty selection, which core.jobs drives straight to SUCCEEDED over a folder nothing touched

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `E3_empty_plan_queues_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_empty_plan_is_still_asked_about_and_queues_nothing_and_says_which_zero[False]`
  - `tests/test_tag_workers.py::test_an_empty_plan_is_still_asked_about_and_queues_nothing_and_says_which_zero[True]`

Old text:

```
    if not plan["items"]:
        payload, warnings = (
```

New text:

```
    if False:
        payload, warnings = (
```

### `r185-r246-author.M1_folder_dropped`

Drop the folder from the instruction, so a person reading one envelope beside others cannot tell which sweep it names

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `M1_folder_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_the_queueing_envelope_names_the_reload_before_the_person_walks_away`

Old text:

```
            f"this correction writes the genre onto the files under {folder} and "
            f"does not update the library rows, which go on carrying the old "
```

New text:

```
            f"this correction writes the genre onto the files it selected and "
            f"does not update the library rows, which go on carrying the old "
```

### `r185-r246-author.W1_queue_warning_dropped`

The queueing envelope stops naming the reload, so the person walks away told nothing

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W1_queue_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_queueing_envelope_names_the_reload_before_the_person_walks_away`

Old text:

```
            warnings=(library_row_warning(folder),),

```

New text:

```
(empty)
```

### `r185-r246-author.W2_resume_warning_dropped`

A successful resume stops naming the reload

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W2_resume_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`

Old text:

```
        if summary["corrected"]:
            warnings = (*warnings, library_row_warning(folder))

```

New text:

```
(empty)
```

### `r185-r246-author.W3_resume_warning_unconditional`

Name the reload on every resume, including one that corrected nothing and made no row stale

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W3_resume_warning_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_that_corrected_nothing_does_not_send_a_person_to_rekordbox`

Old text:

```
        if summary["corrected"]:
            warnings = (*warnings, library_row_warning(folder))
```

New text:

```
        warnings = (*warnings, library_row_warning(folder))
```

### `r185-r246-author.W4_refusal_step_dropped`

A half corrected sweep leaves through its cause with nothing said about the rows it made stale

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W4_refusal_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`

Old text:

```
        try:
            job, warnings = shell.advance(
                ctx,
                store,
                queued,
                origin=("tagging", "retag_cli"),
                nothing_to_run="report a correction over files it never looked at",
            )
        except CratekitError as failed:
            # THE REFUSAL CARRIES THE RELOAD WHEN ANYTHING WAS CORRECTED. The
            # artifacts are committed per item before the failure, so this
            # counts what actually landed rather than what was confirmed, and a
            # sweep that refused on its first item adds nothing to a refusal it
            # has no reload to name. See ``with_reload_step``.
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
            raise with_reload_step(failed, folder) from failed
```

New text:

```
        job, warnings = shell.advance(
            ctx,
            store,
            queued,
            origin=("tagging", "retag_cli"),
            nothing_to_run="report a correction over files it never looked at",
        )
```

### `r185-r246-author.W5_refusal_step_unconditional`

Append the reload to every refusal, including one that corrected nothing

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W5_refusal_step_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_that_failed_before_correcting_anything_names_no_reload`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
            raise with_reload_step(failed, folder) from failed
```

New text:

```
            raise with_reload_step(failed, folder) from failed
```

### `r185-r246-author.W6_refusal_counts_the_plan`

Count the confirmed items instead of the committed artifacts, so a sweep that wrote nothing still reports a correction

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `W6_refusal_counts_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_that_failed_before_correcting_anything_names_no_reload`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`

Old text:

```
            if not _summary(cfg, ctx.args.job)["corrected"]:
                raise
```

New text:

```
            if not payload.get(ITEMS_KEY):
                raise
```

### `r290-author.R1_retag_rebuild_drops_the_type`

Rebuild the retag refusal as a plain CratekitError again, so a retag parked after correcting a file says failed

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r290-author.json`, row `R1_retag_rebuild_drops_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`
- Collected: 228 against a baseline of 228
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`

Old text:

```
    return rebuilt(
        error,
        replace(
```

New text:

```
    return CratekitError(
        replace(
```

### `r816-e.E1_retag_names_the_verb`

library_row_warning: name no verb, reworded

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r816-e.json`, row `E1_retag_names_the_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`

Old text:

```
because this verb writes the file half only; run `crate tag "
            f"rows` so the rows catch up
```

New text:

```
because this verb writes the file half only; run the row "
            f"verb so the rows catch up
```

### `u56-catalogue-searcher-and-tag-workers.R26_retag_queues_no_items`

The zero item rule broken on the second verb, over work somebody explicitly confirmed

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R26_retag_queues_no_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 20 (killed)
- Killed:
  - `tests/test_queued_resume_contract.py::test_the_resume_the_job_driver_spawns_can_actually_proceed[tag.retag]`
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_rather_than_reported_done`
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[-read_back1-no-genre]`
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[Ambient-read_back0-genre-specific]`
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_parses_the_active_taxonomy_once_however_many_files_it_corrects`
  - `tests/test_tag_workers.py::test_a_retag_that_corrected_nothing_does_not_send_a_person_to_rekordbox`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`
  - `tests/test_tag_workers.py::test_a_retried_retag_drives_only_the_item_that_failed`
  - ... and 5 more, see the JSON sidecar

Old text:

```
            item_ids=tuple(str(row["path"]) for row in plan["items"]),
```

New text:

```
            item_ids=(),
```

### `u56-catalogue-searcher-and-tag-workers.R28_worker_trusts_the_frozen_row`

The genre is not re-read at drive time, so a file somebody corrected by hand between the confirmation and the drive is corrected again

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R28_worker_trusts_the_frozen_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[-read_back1-no-genre]`

Old text:

```
    current = tags.read_genre_from_file(path) or ""
    if not current:
```

New text:

```
    current = tags.read_genre_from_file(path) or ""
    if False:
```

### `u56-catalogue-searcher-and-tag-workers.R29_blank_genre_is_corrected`

The retag writes into a field tag.folder owns under fill if empty, which is one field under two policies

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R29_blank_genre_is_corrected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[-read_back1-no-genre]`

Old text:

```
    if not current:
        result = retag.RetagResult(path=path, current=current, reason=retag.NO_GENRE)
```

New text:

```
    if current == "\\u0000":
        result = retag.RetagResult(path=path, current=current, reason=retag.NO_GENRE)
```

### `u56-catalogue-searcher-and-tag-workers.R30_specific_genre_is_overwritten`

A queued job overwrites somebody's own curation, which is the write this verb exists to avoid making

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R30_specific_genre_is_overwritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[Ambient-read_back0-genre-specific]`
  - `tests/test_tag_workers.py::test_the_report_is_derived_from_what_ran_rather_than_from_what_was_planned`

Old text:

```
    elif not declared.is_too_coarse_as_source(current):
```

New text:

```
    elif False:
```

### `u56-catalogue-searcher-and-tag-workers.R31_artifact_drops_the_previous_value`

R-185's only record: without the previous genre the artifacts stop naming which library rows went stale, so the deferred database half has no population to read

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R31_artifact_drops_the_previous_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_an_interrupted_retag_leaves_a_library_row_stale_and_the_artifact_recovers_it`

Old text:

```
            "current": result.current,
            "written": result.written,
```

New text:

```
            "written": result.written,
```

### `r816-a.A1_too_coarse_protection`

plan_rows: drop the rule that a too coarse file word does not replace a specific row word

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A1_too_coarse_protection`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 6 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_a_too_coarse_file_does_not_replace_a_specific_row`
  - `tests/test_tag_rows.py::test_every_live_row_is_counted_exactly_once_and_items_are_in_identifier_order`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_writes_the_genre_and_no_other_column_of_any_row`
  - `tests/test_tag_rows.py::test_the_pairs_are_the_writes_counted_largest_first`

Old text:

```
        elif _protected(declared, row_word, file_word):
```

New text:

```
        elif False:
```

### `r816-a.A2_held_out`

plan_rows: ignore the rows a person held out, so a hand set genre is planned as a write

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A2_held_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_row_a_person_holds_out_is_listed_and_left`

Old text:

```
        if content_id in held_out:
```

New text:

```
        if False:
```

### `r816-a.A3_multi_valued`

plan_rows: write a row from a file holding more than one genre

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A3_multi_valued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_holding_two_genres_is_left_alone_and_both_are_shown`
  - `tests/test_tag_rows.py::test_two_genres_in_an_id3_frame_read_as_they_do_in_a_list_container`

Old text:

```
            if several:
```

New text:

```
            if False:
```

### `r816-a.A4_agreement`

plan_rows: stop reading equal words as agreement, so every row with a file genre is a write

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A4_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 12 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_holding_two_genres_is_left_alone_and_both_are_shown`
  - `tests/test_tag_rows.py::test_a_row_and_file_that_agree_are_not_in_the_plan`
  - `tests/test_tag_rows.py::test_a_second_apply_plans_nothing_and_writes_nothing`
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_an_empty_plan_still_asks_and_opens_nothing_to_write`
  - `tests/test_tag_rows.py::test_an_empty_second_value_is_not_a_second_genre_and_not_an_unknown_word`
  - `tests/test_tag_rows.py::test_an_identifier_held_out_that_names_no_differing_row_is_carried_and_digested`
  - `tests/test_tag_rows.py::test_every_live_row_is_counted_exactly_once_and_items_are_in_identifier_order`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_writes_the_genre_and_no_other_column_of_any_row`
  - `tests/test_tag_rows.py::test_the_digest_moves_when_only_a_count_moves`
  - `tests/test_tag_rows.py::test_two_genres_in_an_id3_frame_read_as_they_do_in_a_list_container`

Old text:

```
        if row_word == file_word:
```

New text:

```
        if False:
```

### `r816-a.A5_unreadable_is_blank`

_file_word: count a file whose tags would not open as a file with no genre

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A5_unreadable_is_blank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_no_tag_library_opens_is_unreadable_and_not_blank`
  - `tests/test_tag_rows.py::test_every_live_row_is_counted_exactly_once_and_items_are_in_identifier_order`

Old text:

```
        return "", FILE_UNREADABLE
```

New text:

```
        return "", FILE_BLANK
```

### `r816-a.A6_first_value`

_file_word: compare the checked reader's text as it came, null bytes and all

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A6_first_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_an_empty_second_value_is_not_a_second_genre_and_not_an_unknown_word`
  - `tests/test_tag_rows.py::test_two_genres_in_an_id3_frame_read_as_they_do_in_a_list_container`

Old text:

```
    word = next((part.strip() for part in text.split("\x00") if part.strip()), "")
```

New text:

```
    word = text.strip()
```

### `r816-a.A7_digest_counts`

RowsPlan.digest: leave the outcome counts out of the digest

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A7_digest_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_digest_moves_when_only_a_count_moves`

Old text:

```
                "counts": dict(self.counts),

```

New text:

```
(empty)
```

### `r816-a.A8_leave_unmatched`

plan_rows: drop the identifiers held out that name no differing row

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-a.json`, row `A8_leave_unmatched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`
  - `tests/test_tag_rows.py::test_an_identifier_held_out_that_names_no_differing_row_is_carried_and_digested`

Old text:

```
        leave_unmatched=tuple(sorted(held_out - listed)),
```

New text:

```
        leave_unmatched=(),
```

### `r816-b.B1_stale_check`

apply_rows: write without asking whether each row is still as the plan read it

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B1_stale_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_row_removed_since_the_plan_refuses_and_nothing_is_written`
  - `tests/test_tag_rows.py::test_a_row_whose_genre_moved_since_the_plan_refuses_and_nothing_is_written`

Old text:

```
    assert_rows_as_planned(plan, mapped)

```

New text:

```
(empty)
```

### `r816-b.B2_stale_tombstone`

assert_rows_as_planned: write a row removed since the plan

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B2_stale_tombstone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[0_0]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[0_1]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[None]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[]`
  - `tests/test_tag_rows.py::test_a_row_removed_since_the_plan_refuses_and_nothing_is_written`

Old text:

```
        if row is None or trees.soft_delete_marker(row):
```

New text:

```
        if row is None:
```

### `r816-b.B4_restore_detection`

apply_rows: record a fingerprint without first looking for an out of band restore

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B4_restore_detection`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_restore_out_of_band_is_marked_before_this_write_replaces_the_evidence`

Old text:

```
    convergence.detect_out_of_band_restore(cfg, db, tree_registry.read(cfg))

```

New text:

```
(empty)
```

### `r816-b.B5_commit_recorded`

apply_rows: leave the landed commit off the session record

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B5_commit_recorded`
- Moved: Same call site in apply_rows; U298 replaced the module's _record_commit with write.row_defaults.record_commit, so the deleted line is reworded and still the record of the landed commit
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_apply_is_a_recorded_session_a_restore_can_undo`

Old text:

```
        # RECORDED THE INSTANT THE COMMIT RETURNS.
        row_defaults.record_commit(record, CHANGE_KEY, written, cfg)

```

New text:

```
        # RECORDED THE INSTANT THE COMMIT RETURNS.

```

### `r816-c.B6_bookkeeping_exempt`

judge: stop exempting the binding's bookkeeping columns, so every clean write reads as moved

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-c.json`, row `B6_bookkeeping_exempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 10 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_on_a_volume_that_is_not_mounted_is_counted_and_the_run_does_not_fail`
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`
  - `tests/test_tag_rows.py::test_a_person_reads_the_counts_and_the_pairs_at_the_gate_and_after_the_write`
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_a_word_the_library_has_no_row_for_names_the_act_on_a_run_that_wrote`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_writes_the_genre_and_no_other_column_of_any_row`
  - `tests/test_tag_rows.py::test_the_genre_report_stops_naming_the_old_word_after_the_run`
  - `tests/test_tag_rows.py::test_the_read_back_passes_a_row_whose_genre_and_bookkeeping_alone_moved`

Old text:

```
            and column not in rb_writer.BOOKKEEPING_COLUMNS

```

New text:

```
(empty)
```

### `r816-c.B9_cache_reset`

apply_rows: leave the collection cache holding the words as they were

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-c.json`, row `B9_cache_reset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_genre_report_stops_naming_the_old_word_after_the_run`

Old text:

```
    collection.reset_cache()

```

New text:

```
(empty)
```

### `u114.M18_narrow_called`

The row engine never calls the narrow step, so no file is written and every row is

- File: `src/cratekit/tagging/rows.py`
- Source: `u114.json`, row `M18_narrow_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`, `tests/test_tag_rows.py`
- Collected: 131 against a baseline of 131
- Kills: 21 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_commit_that_refuses_leaves_the_row_as_it_was_and_claims_no_commit`
  - `tests/test_tag_rows.py::test_a_file_on_a_volume_that_is_not_mounted_is_counted_and_the_run_does_not_fail`
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`
  - `tests/test_tag_rows.py::test_a_person_reads_the_counts_and_the_pairs_at_the_gate_and_after_the_write`
  - `tests/test_tag_rows.py::test_a_restore_out_of_band_is_marked_before_this_write_replaces_the_evidence`
  - `tests/test_tag_rows.py::test_a_second_apply_plans_nothing_and_writes_nothing`
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_a_word_the_library_has_no_row_for_names_the_act_on_a_run_that_wrote`
  - `tests/test_tag_rows.py::test_an_unregistered_policy_would_write_nothing_and_the_apply_registers_it`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_is_a_recorded_session_a_restore_can_undo`
  - `tests/test_tag_rows.py::test_the_apply_writes_the_genre_and_no_other_column_of_any_row`
  - `tests/test_tag_rows.py::test_the_genre_report_stops_naming_the_old_word_after_the_run`
  - `tests/test_tag_rows.py::test_with_no_regression_the_write_marks_nothing_and_records_where_it_left_off`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        if narrow is not None:
            plan = narrow(plan)
```

New text:

```
        if narrow is None:
            plan = narrow(plan)
```

### `u294.M01_rows_narrowed_keeps_all`

rows.narrowed: hold out no write, so the campaign's tag rows step writes every row the verb would, joining and other routed rows included

- File: `src/cratekit/tagging/rows.py`
- Source: `u294.json`, row `M01_rows_narrowed_keeps_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_rows.py`
- Collected: 128 against a baseline of 128
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_file_that_comes_to_carry_the_word_after_the_gate_stops_the_words_as_stale`
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`
  - `tests/test_tag_campaign.py::test_a_follower_whose_file_carries_another_spelling_is_held_out`
  - `tests/test_tag_campaign.py::test_a_rows_plan_narrowed_to_nothing_writes_nothing`
  - `tests/test_tag_campaign.py::test_a_rows_plan_narrowed_writes_only_the_rows_kept_and_holds_the_rest_out`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_stops_the_campaign_with_the_earlier_writes_named`
  - `tests/test_tag_campaign.py::test_a_word_left_or_unanswered_is_named_and_nothing_retags_it`
  - `tests/test_tag_campaign.py::test_an_unexpected_failure_in_a_step_is_this_builds_defect_with_what_landed`
  - `tests/test_tag_campaign.py::test_only_the_genre_column_moves_on_a_written_row`
  - `tests/test_tag_campaign.py::test_rows_joining_needs_genre_and_any_other_routed_row_are_never_written`
  - `tests/test_tag_campaign.py::test_the_whole_campaign_lands_and_needs_genre_falls_as_measured`

Old text:

```
    held = {item.content_id for item in plan.writes if item.content_id not in kept}
```

New text:

```
    held = set()
```

### `u294.M02_rows_narrowed_changes_unfiltered`

rows.narrowed: leave every change in the write, so a held row is written though its item says held

- File: `src/cratekit/tagging/rows.py`
- Source: `u294.json`, row `M02_rows_narrowed_changes_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_rows.py`
- Collected: 128 against a baseline of 128
- Kills: 21 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_file_that_comes_to_carry_the_word_after_the_gate_stops_the_words_as_stale`
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`
  - `tests/test_tag_campaign.py::test_a_folder_that_would_copy_another_bucket_after_the_gate_stops_the_words_as_stale`
  - `tests/test_tag_campaign.py::test_a_follower_whose_file_carries_another_spelling_is_held_out`
  - `tests/test_tag_campaign.py::test_a_person_reads_the_campaign_and_the_resort_it_leaves`
  - `tests/test_tag_campaign.py::test_a_rows_plan_narrowed_to_nothing_writes_nothing`
  - `tests/test_tag_campaign.py::test_a_rows_plan_narrowed_writes_only_the_rows_kept_and_holds_the_rest_out`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_after_part_of_it_landed_reports_what_the_census_reads`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_stops_the_campaign_with_the_earlier_writes_named`
  - `tests/test_tag_campaign.py::test_a_word_left_or_unanswered_is_named_and_nothing_retags_it`
  - `tests/test_tag_campaign.py::test_an_alias_to_the_folder_another_answer_makes_is_planned_on_that_folder`
  - `tests/test_tag_campaign.py::test_an_unexpected_failure_in_a_step_is_this_builds_defect_with_what_landed`
  - `tests/test_tag_campaign.py::test_every_file_an_alias_retags_is_on_the_gate_and_in_the_digest`
  - `tests/test_tag_campaign.py::test_only_the_genre_column_moves_on_a_written_row`
  - `tests/test_tag_campaign.py::test_rows_joining_needs_genre_and_any_other_routed_row_are_never_written`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        changes=tuple(change for change in plan.changes.changes if change.content_id not in held),
```

New text:

```
        changes=tuple(plan.changes.changes),
```

### `u306.T1_tallied_writes`

rows.Tallied.writes: read the items left alone as the writes, for tag rows and tag suggest both

- File: `src/cratekit/tagging/rows.py`
- Source: `u306.json`, row `T1_tallied_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`
- Collected: 131 against a baseline of 131
- Kills: 31 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_commit_that_refuses_leaves_the_row_as_it_was_and_claims_no_commit`
  - `tests/test_tag_rows.py::test_a_file_on_a_volume_that_is_not_mounted_is_counted_and_the_run_does_not_fail`
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`
  - `tests/test_tag_rows.py::test_a_person_reads_the_counts_and_the_pairs_at_the_gate_and_after_the_write`
  - `tests/test_tag_rows.py::test_a_restore_out_of_band_is_marked_before_this_write_replaces_the_evidence`
  - `tests/test_tag_rows.py::test_a_row_whose_genre_moved_since_the_plan_refuses_and_nothing_is_written`
  - `tests/test_tag_rows.py::test_a_second_apply_plans_nothing_and_writes_nothing`
  - `tests/test_tag_rows.py::test_a_second_run_after_a_clean_one_asks_and_is_a_no_op`
  - `tests/test_tag_rows.py::test_a_too_coarse_file_does_not_replace_a_specific_row`
  - `tests/test_tag_rows.py::test_a_word_the_library_has_no_row_for_names_the_act_on_a_run_that_wrote`
  - `tests/test_tag_rows.py::test_an_unregistered_policy_would_write_nothing_and_the_apply_registers_it`
  - `tests/test_tag_rows.py::test_every_live_row_is_counted_exactly_once_and_items_are_in_identifier_order`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`
  - `tests/test_tag_rows.py::test_the_apply_is_a_recorded_session_a_restore_can_undo`
  - ... and 16 more, see the JSON sidecar

Old text:

```
        return tuple(item for item in self.items if item.action == WRITE)
```

New text:

```
        return tuple(item for item in self.items if item.action != WRITE)
```

### `u306.T2_tallied_unread`

rows.Tallied.unread: count no row as unread, so a plan over files whose genre was never learned reads as complete

- File: `src/cratekit/tagging/rows.py`
- Source: `u306.json`, row `T2_tallied_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`
- Collected: 131 against a baseline of 131
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_on_a_volume_that_is_not_mounted_is_counted_and_the_run_does_not_fail`
  - `tests/test_tag_rows.py::test_a_file_whose_bytes_are_not_here_is_counted_and_never_opened`
  - `tests/test_tag_rows.py::test_every_live_row_is_counted_exactly_once_and_items_are_in_identifier_order`
  - `tests/test_tag_rows.py::test_planned_written_and_read_back_through_the_two_acts`

Old text:

```
        return sum(self.counts[name] for name in UNREAD)
```

New text:

```
        return 0
```

### `u306.T3_scanned_root`

rows.scanned: hand adoption's census the library root's parent, so the walk tag rows, suggest and backlog share resolves rows under the wrong root

- File: `src/cratekit/tagging/rows.py`
- Source: `u306.json`, row `T3_scanned_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`
- Collected: 193 against a baseline of 193
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_file_on_a_volume_that_is_not_mounted_is_counted_and_the_run_does_not_fail`
  - `tests/test_tag_rows.py::test_a_row_recorded_under_no_prefix_rule_is_counted_unmapped`
  - `tests/test_tag_rows.py::test_exactly_half_unmapped_is_not_a_majority_and_the_verb_plans`

Old text:

```
        root=Path(cfg.library.root),
        prefix_map=locations.prefix_rules(cfg.resolved_prefix_map()),
```

New text:

```
        root=Path(cfg.library.root).parent,
        prefix_map=locations.prefix_rules(cfg.resolved_prefix_map()),
```

### `r816-d.C1_acknowledgment`

tag_rows: ask the gate without reading the backup acknowledgment first

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C1_acknowledgment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `r816-d.C4_only_apply_writes`

tag_rows: write on any answer

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C4_only_apply_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_plan_refusal_writes_nothing_and_a_declined_gate_writes_nothing`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
```

New text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) == "never":
```

### `r816-d.C5_leave_reaches_the_plan`

_plan: drop the rows held out on the command line

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `r816-d.json`, row `C5_leave_reaches_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_held_row_survives_the_write_and_the_apply_must_name_it_again`
  - `tests/test_tag_rows.py::test_a_mistyped_identifier_is_shown_at_the_gate_and_warned_about`

Old text:

```
        return rows.plan_rows(cfg, db, declared, leave=leave)
```

New text:

```
        return rows.plan_rows(cfg, db, declared, leave=())
```

### `u294.M23_rows_read_back`

tag rows' apply path no longer refuses over a row that does not read back

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `u294.json`, row `M23_rows_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_rows.py`
- Collected: 128 against a baseline of 128
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_row_that_does_not_read_back_refuses_the_rows_step`

Old text:

```
    rows.assert_read_back(written)
    return written
```

New text:

```
    return written
```

### `u244.M21_passed_over_rides_unread`

_unread_sources: leave a source passed over for want of a token out of unread, so the file reads no-hit

- File: `src/cratekit/tagging/searchers.py`
- Source: `u244.json`, row `M21_passed_over_rides_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tag_suggest.py`, `tests/test_catalogue_searcher.py`, `tests/test_published_genre.py`
- Collected: 470 against a baseline of 470
- Kills: 6 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_file_swept_without_a_token_is_sources_unread_not_no_hit`
  - `tests/test_discogs_searcher.py::test_a_walk_that_asked_nothing_is_a_decline_naming_what_it_passed_over`
  - `tests/test_discogs_searcher.py::test_no_token_is_not_asked_with_how_to_record_one_and_never_no_hit`
  - `tests/test_discogs_searcher.py::test_the_general_catalogue_is_still_asked_beside_an_unasked_discogs`
  - `tests/test_tag_suggest.py::test_rows_unread_only_by_a_catalogue_nobody_asked_do_not_stop_the_walk`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`

Old text:

```
    ) + tuple(skipped.source for skipped in passed)
```

New text:

```
    )
```

### `u260.F11_reset_images_forgets_nothing`

reset_images: drop nothing, so a shared fetch built in one test outlives it

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F11_reset_images_forgets_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 9 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_bytes_that_are_not_a_picture_are_asked_again_and_fail_as_they_did`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_the_binder_hands_back_one_fetch_per_process_and_the_reset_drops_it`
  - `tests/test_album_cover_once.py::test_two_addresses_serving_the_same_bytes_make_two_requests_and_one_encode`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
    """Forget the shared image fetch and every picture it remembered."""
    _images.clear()
```

New text:

```
    """Forget the shared image fetch and every picture it remembered."""
```

