# Mutation table: u335-after-11

Measured by `scripts/mutate.py` on 2026-11-24 06:51 UTC, branch `HEAD` at `1a401a39`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23223 collected. pytest invocations for this batch: 253.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 06:51 UTC for commit `1a401a39247d`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 37, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23223 against 23223. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u260.F1_fetch_never_answers_from_memory` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 10 | killed |
| `u260.F5_binder_builds_per_call` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 8 | killed |
| `u281.W2_searcher_ignores_the_handed_count` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 10 | killed |
| `u281.W5_run_never_changes` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 4 | killed |
| `u282.D2_shop_decline_gives_way` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 3 | killed |
| `u282.P1_no_picture_question` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 8 | killed |
| `u282.P3_answer_not_folded` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 5 | killed |
| `u282.P5_match_names_no_picture` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 4 | killed |
| `u282.R1_rejection_raised_at_once` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 5 | killed |
| `u282.R4_rejection_reads_as_no_token` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 3 | killed |
| `u284.S1_sweep_keeps_no_record` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 381 | 4 | killed |
| `u284.S5_refusal_said_as_outage` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 381 | 5 | killed |
| `u284.S7_token_step_dropped` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 381 | 1 | killed |
| `u284.S8_refusal_not_retryable` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 381 | 2 | killed |
| `u284.S9_rejected_token_names_any_shop` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 381 | 1 | killed |
| `u289.S1_question_unused` | `src/cratekit/tagging/searchers.py` | user | 8 file(s) | 1437 | 28 | killed |
| `u289.S2_asked_not_carried` | `src/cratekit/tagging/searchers.py` | user | 8 file(s) | 1437 | 127 | killed |
| `u289.S5_shop_asked_head` | `src/cratekit/tagging/searchers.py` | user | 8 file(s) | 1437 | 4 | killed |
| `u289.S6_picture_asked_head` | `src/cratekit/tagging/searchers.py` | user | 8 file(s) | 1437 | 2 | killed |
| `u306.S1_shop_query` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 205 | 14 | killed |
| `u56-catalogue-searcher-and-tag-workers.R13_query_unescaped` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 189 | 5 | killed |
| `u56-catalogue-searcher-and-tag-workers.R5_bare_alias_lookup` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 189 | 29 | killed |
| `u85-b.B9_image_fetch_paced` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 189 | 2 | killed |
| `r1950.S01_apply_read_back_unchecked` | `src/cratekit/tagging/second.py` | user | 2 file(s) | 27 | 3 | killed |
| `r1950.S03_removed_membership_chosen` | `src/cratekit/tagging/second.py` | user | 2 file(s) | 27 | 2 | killed |
| `r1950.S04_removed_node_in_tree` | `src/cratekit/tagging/second.py` | user | 2 file(s) | 27 | 2 | killed |
| `r1950.S05_two_nodes_first_taken` | `src/cratekit/tagging/second.py` | user | 2 file(s) | 27 | 1 | killed |
| `r1950.S06_parent_cycle_unguarded` | `src/cratekit/tagging/second.py` | user | 2 file(s) | 27 | 1 | killed |
| `r1950.S07_plan_genre_unchecked` | `src/cratekit/tagging/second.py` | user | 2 file(s) | 27 | 1 | killed |
| `u340.R21_verb_same_folder` | `src/cratekit/tagging/second.py` | user | 1 file(s) | 15 | 1 | killed |
| `u340.R23_verb_moved` | `src/cratekit/tagging/second.py` | user | 1 file(s) | 15 | 1 | killed |
| `u281.S1_beatport_reads_no_refusal` | `src/cratekit/tagging/shops.py` | user | 5 file(s) | 447 | 22 | killed |
| `u114.M10_file_has_genre` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 4 | killed |
| `u114.M11_file_word_votes` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M12_below_band` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M13_band_order` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M14_genre_unknown` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M15_file_moved` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M16_file_read_back` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M17_rows_follow_files` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 3 | killed |
| `u114.M1_suggestable_routes_only` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 5 | killed |
| `u114.M24_retry_unread` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 2 | killed |
| `u114.M25_settled_not_asked` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M4_split` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 3 | killed |
| `u114.M6_folder_weight` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M7_votes_once` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M9_catalogue_declared` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u244.M03_kept_passed_over_reasked` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 59 | 1 | killed |
| `u306.C2_kept_ignores_unasked` | `src/cratekit/tagging/suggest.py` | user | 3 file(s) | 177 | 1 | killed |
| `u322.M01_stop_counts_partly_read` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 7 | killed |
| `u322.M02_stop_counts_passed_over` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 5 | killed |
| `u322.M05_not_sent_read_as_sent` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 3 | killed |
| `u322.M06_refused_row_drops_words` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 5 | killed |
| `u322.M08_credential_counts` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 3 | killed |
| `u322.M14_token_rows_said_no_token` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 4 | killed |
| `u322.M15_counts_not_sent_as_asked` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 2 | killed |
| `u322.M16_counts_stopped_zero` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 2 | killed |
| `u114.M19_write_intent` | `src/cratekit/tagging/suggest_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `u114.M20_pick_declared` | `src/cratekit/tagging/suggest_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `r650-a.C1_summary_counts_nothing` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 2 | killed |
| `r650-a.C3_summary_drops_the_key` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 4 | killed |
| `r650-a.D3_unresolved_is_fed_by_declines` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 1 | killed |
| `r791-b.C3_summary_counts_answers` | `src/cratekit/tagging/summary.py` | user | 3 file(s) | 239 | 15 | killed |
| `r791-b.C8_one_file` | `src/cratekit/tagging/summary.py` | maintainer | 3 file(s) | 239 | 1 | killed |
| `r791-b.C9_unread_skip_zero_filled` | `src/cratekit/tagging/summary.py` | user | 3 file(s) | 239 | 11 | killed |
| `u240.M18_way_inverted` | `src/cratekit/tagging/summary.py` | user | 5 file(s) | 338 | 3 | killed |
| `u240.M19_one_name_ambiguous` | `src/cratekit/tagging/summary.py` | user | 5 file(s) | 338 | 2 | killed |
| `u240.M22_failed_items_left_out` | `src/cratekit/tagging/summary.py` | user | 5 file(s) | 338 | 3 | killed |
| `u281.C2_challenge_never_named` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 1 | killed |
| `u281.C3_unsent_never_counted` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 2 | killed |
| `u282.C1_refused_token_not_counted` | `src/cratekit/tagging/summary.py` | user | 5 file(s) | 443 | 1 | killed |
| `u284-composite.C3x_unread_discogs_and_outage_named` | `src/cratekit/tagging/summary.py` | user | 4 file(s) | 227 | 2 | killed |
| `u284.C1_tagged_file_named_refused` | `src/cratekit/tagging/summary.py` | user | 4 file(s) | 227 | 1 | killed |
| `u284.C2_outage_named_refused` | `src/cratekit/tagging/summary.py` | user | 4 file(s) | 227 | 2 | killed |
| `u284.C4_stop_never_collected` | `src/cratekit/tagging/summary.py` | user | 4 file(s) | 227 | 2 | killed |
| `u284.C6_token_unsaid` | `src/cratekit/tagging/summary.py` | user | 4 file(s) | 227 | 3 | killed |
| `u284.C7_rejected_token_told_to_wait` | `src/cratekit/tagging/summary.py` | user | 4 file(s) | 227 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R23_summary_from_the_queue` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 27 | killed |
| `u84-b.C2_summary_zero_filled` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 2 | killed |
| `u84-b.C3_old_reports_uncounted` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 1 | killed |
| `u85-a.A16_summary_counts_art` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 102 | 1 | killed |
| `r1724.N11_tag_one_raw_stem` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1679 | 5 | killed |
| `r289-a.A1_appledouble_gone` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r289-a.A2_appledouble_one_dot` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r289-a.A3_staging_dirs_gone` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 4 | killed |
| `r289-a.A4_staging_dirs_acquire_only` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 2 | killed |
| `r289-a.A5_staging_dirs_absolute` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r650-a.B3_engine_drops_the_flag_on_the_write` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 3 | killed |
| `r650-a.B4_engine_leaks_the_flag_onto_a_skip` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r791-b.T1_sources_unread_disposition` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 239 | 12 | killed |
| `r791-b.T2_art_names_unread` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 239 | 1 | killed |
| `r796-b.O9_no_isrc_is_not_no_hit` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 380 | 3 | killed |
| `u240.M1_two_names_take_the_first` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 338 | 4 | killed |
| `u240.M2_no_genre_label_named` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 338 | 4 | killed |
| `u240.M3_tag_no_longer_outranks_the_line` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 338 | 17 | killed |
| `u240.M4_folder_label_no_longer_outranks_the_line` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 338 | 9 | killed |
| `u240.M5_wrong_field_read` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 338 | 11 | killed |
| `u240.M6_named_by_lost` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 338 | 5 | killed |
| `u240.M7_line_labels_dropped_from_result` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 338 | 3 | killed |
| `u240.M8_failed_files_line_dropped` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 338 | 1 | killed |
| `u240.M9_park_flattened` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 338 | 1 | killed |
| `u260.E1_engine_encodes_per_file` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 196 | 8 | killed |
| `u282.T1_question_asked_with_a_picture` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1470 | 2 | killed |
| `u282.T2_question_never_asked` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1470 | 5 | killed |
| `u289.T1_title_tag_split` | `src/cratekit/tagging/tag.py` | user | 8 file(s) | 1437 | 1 | killed |
| `u289.T2_split_artist_dropped` | `src/cratekit/tagging/tag.py` | user | 8 file(s) | 1437 | 4 | killed |
| `u289.T3_record_read_from_title` | `src/cratekit/tagging/tag.py` | user | 8 file(s) | 1437 | 3 | killed |
| `u56-catalogue-searcher-and-tag-workers.R14_walk_unsorted` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 7 | killed |
| `u56-catalogue-searcher-and-tag-workers.R15_walk_not_recursive` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 4 | killed |
| `u85-a.A11_failed_write_is_error` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u85-a.A1_search_skipped_only_with_both` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 11 | killed |
| `u85-a.A2_any_picture_settles` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 8 | killed |
| `u85-a.A5_no_url_guard` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 141 | 1 | killed |
| `u85-a.A6_no_fetch_guard` | `src/cratekit/tagging/tag.py` | maintainer | 4 file(s) | 242 | 1 | killed |
| `u85-a.A7_fetch_raise_is_a_decline` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u85-a.A9_not_a_picture_is_a_decline` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r1724.N6_tail_never_dropped` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 81 | killed |
| `r1724.N7_tail_word` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 82 | killed |
| `r1724.S1_u289_head_needs_a_key` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 3 | killed |
| `r1724.S2_u289_version_part` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 1 | killed |
| `u280-pinned.M06_marker_read_anywhere` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 1 | killed |
| `u280-pinned.M11_ambiguity_featured_credits` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 1 | killed |
| `u280-pinned.M29_marker_number_from_all_words` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 1 | killed |
| `u280.M01_ambiguous_read_as_titled` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 32 | killed |
| `u280.M04_bare_meets_bare` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 6 | killed |
| `u280.M05_marker_not_read_past` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 2 | killed |
| `u280.M07_version_alone_after_title` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 2 | killed |
| `u280.M09_ambiguity_ignores_feature` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 7 | killed |
| `u280.M10_ambiguity_one_credit_only` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 12 | killed |
| `u280.M12_ambiguity_version_alone` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 5 | killed |
| `u280.M17_featured_part_never` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 6 | killed |
| `u280.M18_featured_part_own_credit` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 16 | killed |
| `u280.M19_tempo_never_title` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 2 | killed |
| `u280.M22_whole_name_shed` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 13 | killed |
| `u280.M24_track_number_past_marker` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 2 | killed |
| `u280.M26_brackets_shed_across_a_dash` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 6 | killed |
| `u280.M27_leading_groups_across_a_dash` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 2 | killed |
| `u280.M28_any_number_read_past` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 3 | killed |
| `u280.M30_featured_after_a_head` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 1 | killed |
| `u289.N2_head_alone_ambiguous` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 1 | killed |
| `u289.N3_three_parts_split` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 3 | killed |
| `u289.N4_version_title_split` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 1 | killed |
| `u289.N5_numbered_title_split` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 1 | killed |
| `u289.N6_track_number_artist_split` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 1 | killed |
| `u289.N7_numbered_artist_split` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 1 | killed |
| `u289.Q2_head_alone_two_parts` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 2 | killed |
| `u289.Q3_marker_kept` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 10 | killed |
| `u289.Q4_artist_part_kept` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 13 | killed |
| `u289.Q5_artist_part_needs_title` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 1 | killed |
| `u289.Q6_same_name_any_overlap` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 2 | killed |
| `u289.Q7_empty_title_asked` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 3 | killed |
| `u289.Q8_headless_read_past` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1437 | 1 | killed |
| `u318.T09_ends_in_version_word` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 6 | killed |
| `u324-pinned.F20_initial_prefix_dropped_pinned` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 2 | killed |
| `u324.F14_o_as_oe` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 16 | killed |
| `u324.F18_written_length_initial` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u324.F19_no_initials` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 7 | killed |
| `u118-d.T2_named_word` | `src/cratekit/templates/taxonomy.default.toml` | user | 2 file(s) | 928 | collection error | collect-error |
| `u133-b.T1_keyword_back` | `src/cratekit/templates/taxonomy.default.toml` | user | 3 file(s) | 946 | collection error | collect-error |
| `u133-b.T2_alias_gone` | `src/cratekit/templates/taxonomy.default.toml` | user | 4 file(s) | 1222 | 2 | killed |
| `u133-b.T5_former_display` | `src/cratekit/templates/taxonomy.default.toml` | user | 3 file(s) | 1038 | 2 | killed |
| `u133-b.T7_former_gone` | `src/cratekit/templates/taxonomy.default.toml` | user | 3 file(s) | 1014 | collection error | collect-error |
| `u133-b.T9_energy_off` | `src/cratekit/templates/taxonomy.default.toml` | user | 3 file(s) | 1038 | 13 | killed |
| `u88-b.X6_template_bound` | `src/cratekit/templates/taxonomy.default.toml` | user | 2 file(s) | 341 | 3 | killed |
| `sitting3.G8_queue_skips_readiness` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 36 | 2 | killed |
| `u181.C3_unscored_flag_ignored` | `src/cratekit/vocals/cli.py` | user | 2 file(s) | 107 | 5 | killed |
| `u25.G6_always_rewrite` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 36 | 1 | killed |
| `u331.S12_vocal_module_imported_before_the_bound_loader` | `src/cratekit/vocals/cli.py` | user | 2 file(s) | 54 | 1 | killed |
| `u343.M12_unscored_reads_the_name_alone` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 36 | 1 | killed |
| `r745-a.E10_text_not_cleaned` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 7 | killed |
| `r745-a.E11_any_path_encoded` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-a.E12_three_stars_moved` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-a.E13_siblings_by_identifier` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-a.E1_tombstone_row_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 16 | killed |
| `r745-a.E3_tombstone_playlist_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r745-a.E4_dangling_member_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 6 | killed |
| `r745-a.E5_empty_folder_self_closed` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 34 | killed |
| `r745-a.E6_tempo_constant_moved` | `src/cratekit/write/collection_export.py` | user | 2 file(s) | 141 | 2 | killed |
| `r745-a.E7_identifier_not_held_to_digits` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-a.E8_duplicate_identifier_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 1 | killed |
| `r745-a.E9_smart_playlist_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 3 | killed |
| `r745-b.E14_members_as_they_arrive` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 1 | killed |
| `r745-b.E15_unreadable_kind_is_a_playlist` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 3 | killed |
| `r745-b.E16_lookups_not_primed` | `src/cratekit/write/collection_export.py` | maintainer | 1 file(s) | 94 | 1 | killed |
| `r745-b.E17_provenance_read_anywhere` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 1 | killed |
| `r745-c.E2_tombstone_membership_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r773-a.M10_unmapped_rows_not_collected` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r773-a.M11_prefixes_least_rows_first` | `src/cratekit/write/collection_export.py` | maintainer | 1 file(s) | 94 | 1 | killed |
| `r773-a.M1_read_back_not_asked` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r773-a.M2_unmapped_not_told_apart` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r773-a.M3_placed_row_written_as_recorded` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 5 | killed |
| `r773-a.M4_emitter_handed_the_rows_as_read` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 5 | killed |
| `r773-a.M5_another_host_not_caught` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 1 | killed |
| `r773-a.M6_left_row_counted_as_under_no_rule` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r773-a.M7_prefixes_not_carried` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r773-a.M8_placed_rows_not_counted` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r773-a.M9_left_rows_not_collected` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r773-a.S1_streamed_row_encoded_as_a_file` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 5 | killed |
| `r773-a.S2_tombstoned_row_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 16 | killed |
| `r773-a.S3_not_a_file_count_inverted` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r1949.E1_missing_never` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 25 | killed |
| `r1949.N10_no_classes` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 1 | killed |
| `r1949.N11_no_bands` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 9 | killed |
| `r1949.N12_undeclared_pair_raises` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 110 | killed |
| `r1949.N14_namesake_names_swapped` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 1 | killed |
| `r1949.N15_vocal_half_dropped` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 2 | killed |
| `r1949.N16_favorites_half_dropped` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 1 | killed |
| `r1949.N1_no_namesakes` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 9 | killed |
| `r1949.N2_removed_compared` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 1 | killed |
| `r1949.N3_resolved_compared_again` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 2 | killed |
| `r1949.N4_covered_compared` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 1 | killed |
| `r1949.N5_uncompared_dimension_compared` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 2 | killed |
| `r1949.N6_folder_by_display_only` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 1 | killed |
| `r1949.N8_manual_class_compared` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 1 | killed |
| `r1949.N9_no_genre_subs` | `src/cratekit/write/convergence_check.py` | user | 8 file(s) | 535 | 1 | killed |

## Row definitions

### `u260.F1_fetch_never_answers_from_memory`

remembering: never look the address up, so every file asks the host again, the behaviour before the unit

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F1_fetch_never_answers_from_memory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 10 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_raises_is_not_remembered`
  - `tests/test_album_cover_once.py::test_an_albums_files_naming_one_address_make_one_request_one_wait_and_one_encode`
  - `tests/test_album_cover_once.py::test_an_empty_answer_handed_straight_in_is_not_remembered`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_the_fetch_memory_keeps_a_few_addresses_and_forgets_the_oldest`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
            data = held.get(url)
            if data is not None:
                held.move_to_end(url)
                return data
        data = fetch_image(url)
```

New text:

```
            data = None
            if data is not None:
                held.move_to_end(url)
                return data
        data = fetch_image(url)
```

### `u260.F5_binder_builds_per_call`

for_images: build a fresh remembering fetch on every call, so the worker's per item binder call forgets every picture

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F5_binder_builds_per_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 8 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_an_albums_files_naming_one_address_make_one_request_one_wait_and_one_encode`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_the_binder_hands_back_one_fetch_per_process_and_the_reset_drops_it`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
    if not _images:
        _images.append(remembering(default_image_fetch(), admit=art.decodes))
    return _images[0]
```

New text:

```
    return remembering(default_image_fetch(), admit=art.decodes)
```

### `u281.W2_searcher_ignores_the_handed_count`

catalogue_searcher: build its own count whatever it is handed, so a worker's per file searcher starts again every file

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `W2_searcher_ignores_the_handed_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 10 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_a_new_run_asks_again_from_its_first_file`
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
    counted = Refusals() if refusals is None else refusals
```

New text:

```
    counted = Refusals()
```

### `u281.W5_run_never_changes`

for_run: keep the first run's count for every later run, so the next sweep never asks a stopped catalogue

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `W5_run_never_changes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 4 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_run_met_again_after_another_starts_afresh`
  - `tests/test_beatport_refusal.py::test_one_run_name_is_one_count_and_another_name_a_fresh_one`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
    if not _run_refusals or _run_refusals[0][0] != run:
```

New text:

```
    if not _run_refusals:
```

### `u282.D2_shop_decline_gives_way`

search: a record shop's decline gives way too, so an explicit Beatport first walk asks Discogs after Beatport's unmapped genre

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `D2_shop_decline_gives_way`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_record_shop_decline_still_ends_an_explicit_walk`
  - `tests/test_published_genre.py::test_ae2_two_coarse_answers_write_nothing_and_the_record_shows_both`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`

Old text:

```
            if resolved.genre is None and source not in _SEARCHES:
```

New text:

```
            if resolved.genre is None:
```

### `u282.P1_no_picture_question`

_pictured: no picture question is carried, so a file Discogs tagged gets no cover (merge blocker 5)

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `P1_no_picture_question`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 8 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_misses_names_no_picture_and_no_unread`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_refuses_is_unread_and_counts_toward_the_stop`
  - `tests/test_discogs_first.py::test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread`
  - `tests/test_discogs_first.py::test_a_tagged_file_with_no_picture_keeps_its_genre_and_gets_the_cover`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
    if not later:
        return lent
```

New text:

```
    if True:
        return lent
```

### `u282.P3_answer_not_folded`

_pictured: the picture's answer is not folded into the record, so Beatport stays not-asked after it was asked

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `P3_answer_not_folded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_misses_names_no_picture_and_no_unread`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_refuses_is_unread_and_counts_toward_the_stop`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
            answers = [entry if said.source == source else said for said in answers]
```

New text:

```
            answers = [said for said in answers]
```

### `u282.P5_match_names_no_picture`

_pictured: a matched row's cover is not taken

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `P5_match_names_no_picture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_tagged_file_with_no_picture_keeps_its_genre_and_gets_the_cover`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
                    art_url=outcome.art_url,
                    art_source=source,
```

New text:

```
                    art_url="",
                    art_source="",
```

### `u282.R1_rejection_raised_at_once`

search: a rejected token is raised at once, so Beatport is never asked (round one's BLOCKING)

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `R1_rejection_raised_at_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_401_is_sent_once_and_beatport_decides_every_file`
  - `tests/test_discogs_first.py::test_a_beatport_decline_beside_a_refused_token_is_a_decline_and_never_raises`
  - `tests/test_discogs_first.py::test_a_tagged_file_still_gets_its_cover_when_the_token_is_refused`
  - `tests/test_discogs_first.py::test_a_token_refused_on_its_shape_still_lets_beatport_decide_and_lend_its_cover`
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
                    rejected = refusal
                    passed.append
```

New text:

```
                    raise refusal
                    passed.append
```

### `u282.R4_rejection_reads_as_no_token`

search: a rejected token is recorded with the no token note, so the sweep counts it as never recorded

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `R4_rejection_reads_as_no_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_beatport_decline_beside_a_refused_token_is_a_decline_and_never_raises`
  - `tests/test_discogs_first.py::test_a_token_refused_on_its_shape_still_lets_beatport_decide_and_lend_its_cover`
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
                        NotAsked(DISCOGS, f"{DISCOGS_TOKEN_REFUSED}{refusal.cause.message}")
```

New text:

```
                        NotAsked(DISCOGS, DISCOGS_NO_TOKEN)
```

### `u284.S1_sweep_keeps_no_record`

searchers.for_run: the sweep's run count keeps no record, so no date is ever known

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S1_sweep_keeps_no_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 381 against a baseline of 381
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_miss_from_the_refusing_catalogue_clears_it_and_an_outage_does_not`
  - `tests/test_sync_refused.py::test_a_sweep_with_a_token_names_each_file_beatport_refused_and_writes_no_genre`
  - `tests/test_sync_refused.py::test_a_sweeps_run_count_records_a_refusal_sent_and_not_one_unsent`
  - `tests/test_sync_refused.py::test_with_a_token_the_pass_reaches_its_landing_and_names_the_refused_files`

Old text:

```
        _run_refusals[:] = [(run, Refusals(record=True))]
```

New text:

```
        _run_refusals[:] = [(run, Refusals())]
```

### `u284.S5_refusal_said_as_outage`

searchers._decide: a refusal by every catalogue raises the outage refusal, network step first and no token step

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S5_refusal_said_as_outage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 381 against a baseline of 381
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_refusal_with_no_date_recorded_still_names_the_catalogue`
  - `tests/test_sync_refused.py::test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token`
  - `tests/test_sync_refused.py::test_with_a_token_discogs_refusing_too_stops_and_names_both`
  - `tests/test_sync_refused.py::test_with_no_token_a_refusing_beatport_names_itself_its_date_and_the_token`
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
    if len(blocked) == len(outcomes):
        raise _refused_by_all
```

New text:

```
    if False:
        raise _refused_by_all
```

### `u284.S7_token_step_dropped`

searchers._refused_by_all: no token step when Discogs went unasked

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S7_token_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_with_no_token_a_refusing_beatport_names_itself_its_date_and_the_token`

Old text:

```
    if unasked:
        steps.append(
            f"record a Discogs token
```

New text:

```
    if False:
        steps.append(
            f"record a Discogs token
```

### `u284.S8_refusal_not_retryable`

searchers._refused_by_all: the refusal is not retryable, so a resumed sweep cannot ask again

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S8_refusal_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 381 against a baseline of 381
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_with_no_token_a_refusing_beatport_names_itself_its_date_and_the_token`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
        retryable=True,
        origin=("tagging", "searchers"),
        detail={
            "sources": [outcome.source for outcome in outcomes],
            "answers": [outcome.answer.value for outcome in outcomes],
            "notes": [outcome.note for outcome in outcomes],
            REFUSED_DETAIL: since,
```

New text:

```
        retryable=False,
        origin=("tagging", "searchers"),
        detail={
            "sources": [outcome.source for outcome in outcomes],
            "answers": [outcome.answer.value for outcome in outcomes],
            "notes": [outcome.note for outcome in outcomes],
            REFUSED_DETAIL: since,
```

### `u284.S9_rejected_token_names_any_shop`

searchers._beside_refusals: a rejected token names the shops as refusing whatever they answered

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S9_rejected_token_names_any_shop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_rejected_token_beside_a_beatport_miss_names_no_refusing_shop`

Old text:

```
    if not outcomes or any(outcome.answer is not Answer.BLOCKED for outcome in outcomes):
```

New text:

```
    if not outcomes:
```

### `u289.S1_question_unused`

catalogue_searcher: ask every source the file's own text, the head included, as main did

- File: `src/cratekit/tagging/searchers.py`
- Source: `u289.json`, row `S1_question_unused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 28 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_beatport_query_for_a_headed_title_carries_no_head`
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
  - ... and 13 more, see the JSON sidecar

Old text:

```
        hit = answer(asked.artist, title, asked.title)
```

New text:

```
        hit = answer(asked.artist, title, title)
```

### `u289.S2_asked_not_carried`

catalogue_searcher: the hit does not carry the question, so the record names nothing

- File: `src/cratekit/tagging/searchers.py`
- Source: `u289.json`, row `S2_asked_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 127 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_head_and_a_marker_alone_are_never_an_empty_track_field`
  - `tests/test_discogs_question.py::test_a_headed_title_tag_asks_discogs_past_its_head_and_takes_its_match`
  - `tests/test_discogs_question.py::test_a_name_that_reads_to_no_one_split_is_asked_with_no_artist_and_says_so`
  - `tests/test_discogs_question.py::test_a_staged_download_is_asked_and_tagged_as_before`
  - `tests/test_discogs_question.py::test_a_title_of_a_head_alone_is_asked_as_written_and_the_record_says_so`
  - `tests/test_discogs_question.py::test_a_title_tag_with_no_artist_tag_is_never_split_by_its_name`
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_discogs_question.py::test_an_untagged_name_with_no_head_is_asked_as_before`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[(Foo) Bar (feat. X) (Extended Mix)-(Foo) Bar]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[(Hate) Is The Message-(Love) Is The Message]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[(Intro) (Extended Mix)-(Intro)]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[(Intro) (Extended Mix)-Sunrise Mood]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[(Intro)-(Intro)]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[(Intro)-Intro (Original Mix)]`
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[(Intro)-Intro Theme]`
  - ... and 112 more, see the JSON sidecar

Old text:

```
        return None if hit is None else replace(hit, asked=asked)
```

New text:

```
        return hit
```

### `u289.S5_shop_asked_head`

shop: the record shops are sent no question, so their free text carries the head

- File: `src/cratekit/tagging/searchers.py`
- Source: `u289.json`, row `S5_shop_asked_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_beatport_query_for_a_headed_title_carries_no_head`
  - `tests/test_discogs_question.py::test_an_mp3_named_untagged_file_carries_no_marker_into_the_question`
  - `tests/test_discogs_question.py::test_the_pictures_question_after_a_discogs_genre_carries_no_head`
  - `tests/test_discogs_question.py::test_the_record_shops_free_text_query_carries_no_head`

Old text:

```
            artist, title, fetch=touch, pacer=pacer, declared=declared, track=track
```

New text:

```
            artist, title, fetch=touch, pacer=pacer, declared=declared
```

### `u289.S6_picture_asked_head`

_pictured: the picture's question to a record shop after a Discogs genre carries the head

- File: `src/cratekit/tagging/searchers.py`
- Source: `u289.json`, row `S6_picture_asked_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_mp3_named_untagged_file_carries_no_marker_into_the_question`
  - `tests/test_discogs_question.py::test_the_pictures_question_after_a_discogs_genre_carries_no_head`

Old text:

```
        for source in later:
            outcome = shop(source, artist, title, track)
```

New text:

```
        for source in later:
            outcome = shop(source, artist, title, title)
```

### `u306.S1_shop_query`

searchers.catalogue_searcher: hand the shops a query builder that does not escape, so every Beatport, Traxsource and Bandcamp URL carries raw spaces and ampersands

- File: `src/cratekit/tagging/searchers.py`
- Source: `u306.json`, row `S1_shop_query`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 205 against a baseline of 205
- Kills: 14 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_an_artist_and_title_that_need_escaping_reach_the_seam_as_a_quoted_url`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_four_real_misses_are_no_hit_and_carry_no_unread_warning`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
            artist, title, fetch=touch, pacer=pacer, declared=declared, track=track, query=_query
```

New text:

```
            artist, title, fetch=touch, pacer=pacer, declared=declared, track=track, query=lambda *parts: " ".join(parts)
```

### `u56-catalogue-searcher-and-tag-workers.R13_query_unescaped`

An unescaped query truncates at the first ampersand, so a different search is reported as this track's miss

- File: `src/cratekit/tagging/searchers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R13_query_unescaped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 5 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_an_artist_and_title_that_need_escaping_reach_the_seam_as_a_quoted_url`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`

Old text:

```
    return quote_plus(f"{artist} {title}".strip())
```

New text:

```
    return f"{artist} {title}".strip()
```

### `u56-catalogue-searcher-and-tag-workers.R5_bare_alias_lookup`

The defect the document review found: hand roll the resolution out of tagging_alias instead of routing.suggest_tag, which loses the sub display and every declared refusal

- File: `src/cratekit/tagging/searchers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R5_bare_alias_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 29 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_genre_costs_one_fetch_and_its_picture_is_the_original`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_no_genre_spends_a_second_fetch_on_the_track_page`
  - `tests/test_catalogue_searcher.py::test_a_beatport_hit_carries_its_release_picture_resized_to_the_source_edge`
  - `tests/test_catalogue_searcher.py::test_a_beatport_match_carries_the_tag_the_source_name_and_the_raw_genre`
  - `tests/test_catalogue_searcher.py::test_a_beatport_miss_or_silence_falls_through_to_traxsource_which_names_itself[miss]`
  - `tests/test_catalogue_searcher.py::test_a_beatport_miss_or_silence_falls_through_to_traxsource_which_names_itself[unreachable]`
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[acapella]`
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[electronic]`
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[electronica]`
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[techno]`
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[declared tag with no bucket]`
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[padded genre]`
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[unknown word]`
  - `tests/test_catalogue_searcher.py::test_a_match_after_an_unreachable_source_names_it_in_unread_too`
  - ... and 14 more, see the JSON sidecar

Old text:

```
    suggestion = routing.suggest_tag(declared, outcome.source_genre)
    tag = suggestion.tag
    if suggestion.declined or not tag or declared.is_too_coarse_as_source(tag):
        tag = None
```

New text:

```
    hit = declared.tagging_alias(outcome.source_genre.casefold())
    tag = declared.bucket(hit[0]).display if hit is not None else None
```

### `u85-b.B9_image_fetch_paced`

The image fetch skips the pace wait, so a folder opens with a burst of picture requests

- File: `src/cratekit/tagging/searchers.py`
- Source: `u85-b.json`, row `B9_image_fetch_paced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`
- Collected: 189 against a baseline of 189
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_the_image_fetch_is_paced_and_answers_the_bytes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
    def fetch_image(url: str) -> bytes | None:
        pacer.wait()

```

New text:

```
    def fetch_image(url: str) -> bytes | None:

```

### `r1950.S01_apply_read_back_unchecked`

second.apply: drop the read back compare, so a write that did not take is counted read back and the verb reports a clean run

- File: `src/cratekit/tagging/second.py`
- Source: `r1950.json`, row `S01_apply_read_back_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_second_guards.py`, `tests/test_tag_second.py`
- Collected: 27 against a baseline of 27
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_second_guards.py::test_a_clear_that_does_not_read_back_is_named_wrong`
  - `tests/test_tag_second_guards.py::test_a_write_that_changes_the_genre_beside_it_is_named_wrong`
  - `tests/test_tag_second_guards.py::test_a_write_that_does_not_read_back_is_named_wrong_and_refused`

Old text:

```
        if after is None or after != (item.genre, item.wanted):
```

New text:

```
        if after is None:
```

### `r1950.S03_removed_membership_chosen`

playlist_members: count a removed membership, so a track rekordbox took out of the playlist is written

- File: `src/cratekit/tagging/second.py`
- Source: `r1950.json`, row `S03_removed_membership_chosen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_second_guards.py`, `tests/test_tag_second.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_second_guards.py::test_a_parent_cycle_in_the_tree_names_nothing_and_breaks_no_lookup`
  - `tests/test_tag_second_guards.py::test_a_removed_membership_is_not_a_chosen_row`

Old text:

```
                for song in db.get_playlist_songs(PlaylistID=str(found[0].ID))
                if not rb_writer.membership_removed(song)

```

New text:

```
                for song in db.get_playlist_songs(PlaylistID=str(found[0].ID))

```

### `r1950.S04_removed_node_in_tree`

playlist_members: read removed playlists as the tree, so a deleted playlist's tracks are chosen

- File: `src/cratekit/tagging/second.py`
- Source: `r1950.json`, row `S04_removed_node_in_tree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_second_guards.py`, `tests/test_tag_second.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_second_guards.py::test_a_live_playlist_under_a_removed_folder_is_at_no_path`
  - `tests/test_tag_second_guards.py::test_a_removed_playlist_is_not_in_the_tree`

Old text:

```
    nodes = {str(node.ID): node for node in db.get_playlist() if not rb_writer.node_removed(node)}
```

New text:

```
    nodes = {str(node.ID): node for node in db.get_playlist()}
```

### `r1950.S05_two_nodes_first_taken`

playlist_members: drop the refusal of two playlists at one path, so the first is chosen and rows nobody named are written

- File: `src/cratekit/tagging/second.py`
- Source: `r1950.json`, row `S05_two_nodes_first_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_second_guards.py`, `tests/test_tag_second.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_second_guards.py::test_two_playlists_at_one_path_refuse_rather_than_choose`

Old text:

```
    if len(found) > 1:
        raise _no_playlist(path, f"{len(found)} nodes answer to it")
```

New text:

```
    if False:
        raise _no_playlist(path, f"{len(found)} nodes answer to it")
```

### `r1950.S06_parent_cycle_unguarded`

playlist_members: drop the parent cycle guard, so a cycle in the tree recurses until Python stops it

- File: `src/cratekit/tagging/second.py`
- Source: `r1950.json`, row `S06_parent_cycle_unguarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_second_guards.py`, `tests/test_tag_second.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_second_guards.py::test_a_parent_cycle_in_the_tree_names_nothing_and_breaks_no_lookup`

Old text:

```
        if above is None or parent in seen:
```

New text:

```
        if above is None:
```

### `r1950.S07_plan_genre_unchecked`

second.plan: drop its own genre check, so a direct caller plans a second genre that files nowhere

- File: `src/cratekit/tagging/second.py`
- Source: `r1950.json`, row `S07_plan_genre_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_second_guards.py`, `tests/test_tag_second.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_second_guards.py::test_the_engine_refuses_a_genre_that_files_nowhere_itself`

Old text:

```
    if wanted:
        assert_genre_files(declared, wanted)
```

New text:

```
    if False:
        assert_genre_files(declared, wanted)
```

### `u340.R21_verb_same_folder`

tag second _reason: drop the same folder outcome, so a second genre naming the file's own folder is written

- File: `src/cratekit/tagging/second.py`
- Source: `u340.json`, row `R21_verb_same_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_second.py`
- Collected: 15 against a baseline of 15
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_second.py::test_each_chosen_row_lands_in_one_outcome`

Old text:

```
    if routing.second_bucket(declared, file_genre, wanted) is None:
        return SAME_FOLDER
```

New text:

```
    if False:
        return SAME_FOLDER
```

### `u340.R23_verb_moved`

tag second apply: write a file that changed since the plan

- File: `src/cratekit/tagging/second.py`
- Source: `u340.json`, row `R23_verb_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_second.py`
- Collected: 15 against a baseline of 15
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_second.py::test_a_file_that_moved_since_the_plan_is_not_written`

Old text:

```
        if now is None or now != (item.genre, item.current):
```

New text:

```
        if now is None:
```

### `u281.S1_beatport_reads_no_refusal`

_search_beatport: drop the shared refusal check, so a 403 is unreachable and a 200 challenge a parse break, as before the card

- File: `src/cratekit/tagging/shops.py`
- Source: `u281.json`, row `S1_beatport_reads_no_refusal`
- Moved: Anchored where u306-replay-after-a.json replayed it: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`
- Collected: 447 against a baseline of 447
- Kills: 22 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_200_challenge_beside_an_unread_discogs_refuses_as_unreachable_not_parse_broken`
  - `tests/test_beatport_refusal.py::test_a_200_just_a_moment_page_is_blocked_not_a_parse_break`
  - `tests/test_beatport_refusal.py::test_a_200_page_carrying_only_cloudflares_script_is_blocked`
  - `tests/test_beatport_refusal.py::test_a_403_carrying_cloudflares_challenge_header_is_blocked_and_named`
  - `tests/test_beatport_refusal.py::test_a_403_without_the_header_is_blocked_and_says_only_the_status`
  - `tests/test_beatport_refusal.py::test_a_429_that_outlasts_the_backoff_is_blocked_as_the_fallbacks_read_it`
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_a_new_run_asks_again_from_its_first_file`
  - `tests/test_beatport_refusal.py::test_a_searcher_given_no_count_keeps_its_own_for_its_life`
  - `tests/test_beatport_refusal.py::test_a_stopped_beatport_and_a_discogs_with_no_token_refuse_rather_than_decline`
  - `tests/test_beatport_refusal.py::test_a_stopped_catalogue_is_answered_without_a_wait`
  - `tests/test_beatport_refusal.py::test_another_mitigation_is_not_called_a_challenge`
  - `tests/test_beatport_refusal.py::test_blocked_miss_blocked_blocked_does_not_stop_the_run`
  - `tests/test_beatport_refusal.py::test_deezer_is_still_not_asked_beside_a_blocked_beatport[not-sent]`
  - `tests/test_beatport_refusal.py::test_deezer_is_still_not_asked_beside_a_blocked_beatport[refused]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
    tracks = None if page.text is None else _beatport_tracks(page.text)
    if tracks is None:
        refused = unread_outcome(BEATPORT, page)
        if refused is not None:
            return refused
        return SourceOutcome(
```

New text:

```
    if page.text is None:
        return SourceOutcome(BEATPORT, Answer.UNREACHABLE, note=page.note)
    tracks = _beatport_tracks(page.text)
    if tracks is None:
        return SourceOutcome(
```

### `u114.M10_file_has_genre`

A row whose file carries a genre is offered a suggestion instead of being left to tag rows

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M10_file_has_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_row_whose_file_carries_a_genre_its_row_lacks_votes_with_the_files_word`
  - `tests/test_tag_suggest.py::test_a_row_with_a_genre_on_the_file_and_not_the_row_is_left_to_tag_rows`
  - `tests/test_tag_suggest.py::test_every_live_row_lands_in_exactly_one_outcome`
  - `tests/test_tag_suggest.py::test_the_gate_refuses_a_plan_that_changed`

Old text:

```
        if word:
            counts[FILE_HAS_GENRE] += 1
            # IT VOTES WITH ITS FILE'S WORD. The row lags its file, which is
            # what ``tag rows`` repairs, and the file is the newer of the two.
            live[track.content_id].genre = word
            continue

```

New text:

```
(empty)
```

### `u114.M11_file_word_votes`

A row whose file carries a genre its row lacks no longer votes with the file's word

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M11_file_word_votes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_row_whose_file_carries_a_genre_its_row_lacks_votes_with_the_files_word`

Old text:

```
            live[track.content_id].genre = word

```

New text:

```
(empty)
```

### `u114.M12_below_band`

The band threshold is ignored and every suggestion with a band is written

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M12_below_band`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_suggestion_below_the_band_is_offered_and_written_only_when_widened`

Old text:

```
        elif not _at_or_above(earned, band):
```

New text:

```
        elif not _at_or_above(earned, LOW):
```

### `u114.M13_band_order`

The band comparison is reversed, so a weaker band passes a stronger threshold

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M13_band_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_suggestion_below_the_band_is_offered_and_written_only_when_widened`

Old text:

```
    return BANDS.index(band) <= BANDS.index(least)
```

New text:

```
    return BANDS.index(band) >= BANDS.index(least)
```

### `u114.M14_genre_unknown`

A genre with no lookup row is planned as a write with an empty identifier

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M14_genre_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_declared_genre_the_library_has_no_lookup_row_for_is_left`

Old text:

```
                replace(item, action=LEAVE, reason=GENRE_UNKNOWN)
                if genre_id is None
                else replace(item, genre_id=genre_id)
```

New text:

```
                replace(item, genre_id=genre_id or "")
```

### `u114.M15_file_moved`

A file that carries a genre by the time the write reaches it is written over

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M15_file_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_file_given_a_genre_after_the_gate_is_left_and_named`

Old text:

```
        if word or outcome != rows.FILE_BLANK:
```

New text:

```
        if outcome == rows.FILE_UNREADABLE:
```

### `u114.M16_file_read_back`

A file is not read back after the write, so its row is written whatever the file holds

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M16_file_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_file_the_writer_says_it_wrote_and_that_does_not_read_back_leaves_its_row`

Old text:

```
        if rows._file_word(target)[0] != item.genre:
            wrong.append(item.content_id)
            continue

```

New text:

```
(empty)
```

### `u114.M17_rows_follow_files`

Every planned row is written, the ones whose file did not take the genre included

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M17_rows_follow_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_file_given_a_genre_after_the_gate_is_left_and_named`
  - `tests/test_tag_suggest.py::test_a_file_that_will_not_take_its_genre_leaves_its_row_and_the_rest_land`
  - `tests/test_tag_suggest.py::test_a_file_the_writer_says_it_wrote_and_that_does_not_read_back_leaves_its_row`

Old text:

```
        if item.content_id in wanted

```

New text:

```
(empty)
```

### `u114.M1_suggestable_routes_only`

suggestable accepts any word adoption routes, a keyword or catch all placement included, so Dance is suggested

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M1_suggestable_routes_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_catalogue_answer_outside_the_taxonomy_is_never_suggested`
  - `tests/test_tag_suggest.py::test_a_pick_outside_the_taxonomy_is_refused_before_any_row_is_read`
  - `tests/test_tag_suggest.py::test_a_tie_between_declared_genres_is_a_split_with_no_default`
  - `tests/test_tag_suggest.py::test_an_undeclared_word_lowers_the_agreement_and_is_never_suggested`
  - `tests/test_tag_suggest.py::test_only_a_genre_adoption_files_by_its_exact_name_is_suggestable`

Old text:

```
    return disposition is adopt_scan.Disposition.ROUTE and declared.named_folder(word) is not None
```

New text:

```
    return disposition is adopt_scan.Disposition.ROUTE
```

### `u114.M24_retry_unread`

A catalogue that could not be read is asked again, the behaviour before the review

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M24_retry_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_catalogue_that_cannot_be_read_is_this_rows_answer_and_is_not_asked_twice`
  - `tests/test_tag_suggest.py::test_tag_suggest_asks_deezer_past_a_refusing_beatport_by_each_files_isrc`

Old text:

```
        if first.said != DECLINED or first.source_genre:
```

New text:

```
        if first.said == MATCHED or first.source_genre:
```

### `u114.M25_settled_not_asked`

A row held out or picked is looked up anyway

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M25_settled_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_row_held_out_or_picked_is_not_looked_up`

Old text:

```
        if catalogue is not None and not settled_by_person:
```

New text:

```
        if catalogue is not None:
```

### `u114.M4_split`

A two way tie at the top is no longer a split and the first tied genre becomes the default

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M4_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_folder_that_splits_evenly_offers_both_genres_and_no_default`
  - `tests/test_tag_suggest.py::test_a_person_picks_a_genre_for_a_split`
  - `tests/test_tag_suggest.py::test_a_tie_between_declared_genres_is_a_split_with_no_default`

Old text:

```
    if len(tied) > 1:
```

New text:

```
    if len(tied) > 2:
```

### `u114.M6_folder_weight`

A folder neighbour votes at the artist's weight

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M6_folder_weight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_the_artist_outweighs_the_folder`

Old text:

```
        weights[other] = FOLDER_WEIGHT
```

New text:

```
        weights[other] = ARTIST_WEIGHT
```

### `u114.M7_votes_once`

A neighbour by the artist in the same folder votes twice, its weights added

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M7_votes_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_neighbour_by_the_artist_in_the_same_folder_votes_once_at_the_artist_weight`

Old text:

```
        weights[other] = max(weights.get(other, 0), ARTIST_WEIGHT)
```

New text:

```
        weights[other] = weights.get(other, 0) + ARTIST_WEIGHT
```

### `u114.M9_catalogue_declared`

A catalogue answer is a vote whether or not the taxonomy declares it

- File: `src/cratekit/tagging/suggest.py`
- Source: `u114.json`, row `M9_catalogue_declared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_catalogue_answer_outside_the_taxonomy_is_never_suggested`

Old text:

```
        and suggestable(declared, asked.genre)

```

New text:

```
(empty)
```

### `u244.M03_kept_passed_over_reasked`

KeptCatalogue.answer: keep the day's answer that passed over Discogs after a token is recorded, round two's B2

- File: `src/cratekit/tagging/suggest.py`
- Source: `u244.json`, row `M03_kept_passed_over_reasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_kept_row_that_passed_over_discogs_is_asked_again_once_a_token_is_recorded`

Old text:

```
        if kept is not None and not self._askable_now(kept):
```

New text:

```
        if kept is not None:
```

### `u306.C2_kept_ignores_unasked`

What P5 does hold: KeptCatalogue never asks again a kept row that passed over a catalogue, so a token recorded later is never used the same day

- File: `src/cratekit/tagging/suggest.py`
- Source: `u306.json`, row `C2_kept_ignores_unasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_kept_row_that_passed_over_discogs_is_asked_again_once_a_token_is_recorded`

Old text:

```
        return not set(kept.passed_over) <= self._unasked
```

New text:

```
        return False
```

### `u322.M01_stop_counts_partly_read`

KeptCatalogue.answer: a partly read row no longer resets the run, the card's defect: a Discogs miss beside a refusing Beatport stops the walk at the third row

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M01_stop_counts_partly_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 7 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_discogs_miss_beside_a_refusing_beatport_does_not_stop_the_walk`
  - `tests/test_catalogue_walk_refusal.py::test_a_partly_read_row_resets_the_run_of_refusals`
  - `tests/test_catalogue_walk_refusal.py::test_a_row_read_beside_a_refusal_stays_unread_and_askable`
  - `tests/test_catalogue_walk_refusal.py::test_deezer_is_asked_on_every_row_with_an_isrc_while_beatport_refuses`
  - `tests/test_catalogue_walk_refusal.py::test_partly_read_rows_never_count_toward_the_stop`
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`
  - `tests/test_tag_suggest.py::test_tag_suggest_asks_deezer_past_a_refusing_beatport_by_each_files_isrc`

Old text:

```
            if answer.said != UNREAD or answer.partly_read:
```

New text:

```
            if answer.said != UNREAD:
```

### `u322.M02_stop_counts_passed_over`

KeptCatalogue.answer: a row unread only by a catalogue nobody asked counts toward the stop, against U244

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M02_stop_counts_passed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 5 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_catalogue_nobody_asked_neither_counts_nor_resets`
  - `tests/test_catalogue_walk_refusal.py::test_a_rejected_discogs_token_beside_a_beatport_that_answers_does_not_stop_the_walk`
  - `tests/test_catalogue_walk_refusal.py::test_a_row_passed_over_for_a_refused_token_is_kept_for_the_day`
  - `tests/test_tag_backlog.py::test_a_token_discogs_refused_is_said_and_beatport_is_asked_on_every_row`
  - `tests/test_tag_suggest.py::test_rows_unread_only_by_a_catalogue_nobody_asked_do_not_stop_the_walk`

Old text:

```
            elif not answer.passed_over:
                self._unread_running += 1
```

New text:

```
            else:
                self._unread_running += 1
```

### `u322.M05_not_sent_read_as_sent`

_word: a refusal never sent is recorded as one sent, so the counts call Beatport asked on every row

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M05_not_sent_read_as_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_row_read_beside_a_refusal_stays_unread_and_askable`
  - `tests/test_catalogue_walk_refusal.py::test_the_words_of_a_refusal_by_every_catalogue_are_read_off_its_detail`
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`

Old text:

```
    if answer == searchers.Answer.BLOCKED.value and note.startswith(searchers.NOT_SENT):
```

New text:

```
    if False:
```

### `u322.M06_refused_row_drops_words`

_asked_from: a row a catalogue refused beside one that answered carries no words, so it counts toward the stop

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M06_refused_row_drops_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 5 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_discogs_miss_beside_a_refusing_beatport_does_not_stop_the_walk`
  - `tests/test_catalogue_walk_refusal.py::test_a_row_read_beside_a_refusal_stays_unread_and_askable`
  - `tests/test_catalogue_walk_refusal.py::test_deezer_is_asked_on_every_row_with_an_isrc_while_beatport_refuses`
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`
  - `tests/test_tag_suggest.py::test_tag_suggest_asks_deezer_past_a_refusing_beatport_by_each_files_isrc`

Old text:

```
            return Asked(UNREAD, note=f"unread: {', '.join(refused)}", answers=words)
```

New text:

```
            return Asked(UNREAD, note=f"unread: {', '.join(refused)}")
```

### `u322.M08_credential_counts`

catalogue_lookup: a token Discogs refused is read as every catalogue refusing, so a Beatport that answers stops the walk at row three

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M08_credential_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_rejected_discogs_token_beside_a_beatport_that_answers_does_not_stop_the_walk`
  - `tests/test_catalogue_walk_refusal.py::test_a_row_passed_over_for_a_refused_token_is_kept_for_the_day`
  - `tests/test_tag_backlog.py::test_a_token_discogs_refused_is_said_and_beatport_is_asked_on_every_row`

Old text:

```
            if exc.cause.reason == searchers.CREDENTIAL_REASON:
```

New text:

```
            if False:
```

### `u322.M14_token_rows_said_no_token`

sort_unread: a row passed over for a refused token is said as no token recorded

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M14_token_rows_said_no_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 4 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_rejected_discogs_token_beside_a_beatport_that_answers_does_not_stop_the_walk`
  - `tests/test_catalogue_walk_refusal.py::test_rows_are_sorted_by_why_they_were_not_read_whole`
  - `tests/test_catalogue_walk_refusal.py::test_the_suggest_verb_says_a_token_that_could_not_be_used`
  - `tests/test_tag_backlog.py::test_a_token_discogs_refused_is_said_and_beatport_is_asked_on_every_row`

Old text:

```
        elif TOKEN_UNUSABLE in asked.note:
```

New text:

```
        elif False:
```

### `u322.M15_counts_not_sent_as_asked`

catalogue_counts: a row a catalogue was passed over on counts as asked

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M15_counts_not_sent_as_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_the_backlogs_catalogue_line_counts_each_catalogues_answers`
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`

Old text:

```
            if word in _ANSWERED or word in searchers.UNREAD_ANSWERS:
```

New text:

```
            if word in _ANSWERED or word in (*searchers.UNREAD_ANSWERS, NOT_SENT):
```

### `u322.M16_counts_stopped_zero`

catalogue_counts: the rows the walk stopped before are not counted

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M16_counts_stopped_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_the_backlogs_catalogue_line_counts_each_catalogues_answers`
  - `tests/test_tag_backlog.py::test_the_catalogue_line_names_the_rows_the_walk_stopped_before`

Old text:

```
        "stopped": sum(asked.note == STOPPED_NOTE for asked in listed),
```

New text:

```
        "stopped": 0,
```

### `u114.M19_write_intent`

The apply opens the database without write intent, so a running rekordbox is not refused by the opener

- File: `src/cratekit/tagging/suggest_cli.py`
- Source: `u114.json`, row `M19_write_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_with_rekordbox_open_the_plan_is_read_and_no_file_is_written`

Old text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
```

New text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=False, cfg=cfg)
```

### `u114.M20_pick_declared`

A --set genre the taxonomy does not declare is accepted

- File: `src/cratekit/tagging/suggest_cli.py`
- Source: `u114.json`, row `M20_pick_declared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_suggest.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_a_pick_outside_the_taxonomy_is_refused_before_any_row_is_read`

Old text:

```
        if not suggest.suggestable(declared, genre):
```

New text:

```
        if not genre.strip():
```

### `r650-a.C1_summary_counts_nothing`

The report stops counting the strings, leaving the map empty on a folder that has them

- File: `src/cratekit/tagging/summary.py`
- Source: `r650-a.json`, row `C1_summary_counts_nothing`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
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
            if report.get("off_taxonomy") and source_genre:
                off_taxonomy[source_genre] = off_taxonomy.get(source_genre, 0) + 1
```

New text:

```
(empty)
```

### `r650-a.C3_summary_drops_the_key`

The payload stops carrying the map at all

- File: `src/cratekit/tagging/summary.py`
- Source: `r650-a.json`, row `C3_summary_drops_the_key`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_sweep_with_nothing_off_taxonomy_carries_no_such_warning`
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`

Old text:

```
        "off_taxonomy": off_taxonomy,
```

New text:

```
(empty)
```

### `r650-a.D3_unresolved_is_fed_by_declines`

Existing: the unresolved map is filled from unmapped-genre and from nothing else

- File: `src/cratekit/tagging/summary.py`
- Source: `r650-a.json`, row `D3_unresolved_is_fed_by_declines`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
        if reason == tag_engine.UNMAPPED_GENRE and source_genre:
```

New text:

```
        if source_genre:
```

### `r791-b.C3_summary_counts_answers`

_summary: count no answers

- File: `src/cratekit/tagging/summary.py`
- Source: `r791-b.json`, row `C3_summary_counts_answers`
- Moved: Anchored where u306-replay-after-d.json replayed it: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 15 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
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
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
                counted[word] += 1
```

New text:

```
                counted[word] += 0
```

### `r791-b.C8_one_file`

_files: say 1 files were

- File: `src/cratekit/tagging/summary.py`
- Source: `r791-b.json`, row `C8_one_file`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`

Old text:

```
    return "1 file was" if count == 1 else f"{count} files were"
```

New text:

```
    return f"{count} files were"
```

### `r791-b.C9_unread_skip_zero_filled`

_summary: count only the three skip reasons that predate R-791

- File: `src/cratekit/tagging/summary.py`
- Source: `r791-b.json`, row `C9_unread_skip_zero_filled`
- Moved: Anchored where u306-replay-after-d.json replayed it: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_skip_reason_reaches_the_report_and_not_only_the_artifact`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`

Old text:

```
    skipped = dict.fromkeys(tag_engine.SKIP_REASONS, 0)
```

New text:

```
    skipped = dict.fromkeys(tag_engine.SKIP_REASONS[:3], 0)
```

### `u240.M18_way_inverted`

_way: a label's genre reported as a catalogue's

- File: `src/cratekit/tagging/summary.py`
- Source: `u240.json`, row `M18_way_inverted`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_label_batch_with_every_catalogue_blocked_lands_tagged_by_label`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_the_report_names_each_file_by_label_by_catalogue_or_not_at_all`

Old text:

```
    if str(report.get("source") or "") == tag_engine.LABEL_GENRE:
```

New text:

```
    if str(report.get("source") or "") != tag_engine.LABEL_GENRE:
```

### `u240.M19_one_name_ambiguous`

_count_ambiguous: count a line naming one label as ambiguous

- File: `src/cratekit/tagging/summary.py`
- Source: `u240.json`, row `M19_one_name_ambiguous`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`
  - `tests/test_tag_folder_copyright.py::test_two_labels_sharing_a_display_name_are_two_in_the_ambiguous_count`

Old text:

```
    if len(names) > 1:
```

New text:

```
    if len(names) > 0:
```

### `u240.M22_failed_items_left_out`

_summary: items with no report are not listed

- File: `src/cratekit/tagging/summary.py`
- Source: `u240.json`, row `M22_failed_items_left_out`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
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
        if item_id in reported:
```

New text:

```
        if True:
```

### `u281.C2_challenge_never_named`

_summary: never count a Cloudflare challenge, so the warning cannot name one

- File: `src/cratekit/tagging/summary.py`
- Source: `u281.json`, row `C2_challenge_never_named`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
                if searchers.CLOUDFLARE_CHALLENGE in note:
                    challenged[source] += 1
```

New text:

```
                if False:
                    challenged[source] += 1
```

### `u281.C3_unsent_never_counted`

_summary: never count a file a catalogue was not sent

- File: `src/cratekit/tagging/summary.py`
- Source: `u281.json`, row `C3_unsent_never_counted`
- Moved: Anchored where u306-replay-after-c.json replayed it: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
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
                if note.startswith(searchers.NOT_SENT):
                    not_sent[source] += 1
```

New text:

```
                if False:
                    not_sent[source] += 1
```

### `u282.C1_refused_token_not_counted`

_summary: a refused token's not-asked is never counted, so the sweep says nothing about it (round two's BLOCKING)

- File: `src/cratekit/tagging/summary.py`
- Source: `u282.json`, row `C1_refused_token_not_counted`
- Moved: Anchored where u306-replay-after-c2.json replayed it: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tag_suggest.py`
- Collected: 443 against a baseline of 443
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`

Old text:

```
                discogs_refused += 1
```

New text:

```
                discogs_refused += 0
```

### `u284-composite.C3x_unread_discogs_and_outage_named`

tagging.cli._refused_out: the composite for C3's zero, both the Discogs was read guard and the every other catalogue refused guard removed, so any file left with no genre is named as one the catalogues refused

- File: `src/cratekit/tagging/summary.py`
- Source: `u284-composite.json`, row `C3x_unread_discogs_and_outage_named`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_pass_whose_catalogues_answered_says_nothing_of_refusals`
  - `tests/test_sync_refused.py::test_a_sweep_beatport_never_refused_names_nothing`

Old text:

```
    if said.get(searchers.DISCOGS) not in (searchers.Answer.MISS.value, searchers.Answer.MATCHED.value):
        return ()
    others = [
        source
        for source in searchers.SOURCES
        if source != searchers.DISCOGS and source in said and said[source] != searchers.NOT_ASKED
    ]
    if not others or any(said[source] != searchers.Answer.BLOCKED.value for source in others):
        return ()
```

New text:

```
    others = [
        source
        for source in searchers.SOURCES
        if source != searchers.DISCOGS and source in said and said[source] != searchers.NOT_ASKED
    ]
    if not others:
        return ()
```

### `u284.C1_tagged_file_named_refused`

tagging.cli._refused_out: a file with a genre written is named among those left with none

- File: `src/cratekit/tagging/summary.py`
- Source: `u284.json`, row `C1_tagged_file_named_refused`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_file_discogs_tagged_while_beatport_refused_its_picture_is_not_named`

Old text:

```
    if reason not in (tag_engine.SOURCES_UNREAD, tag_engine.UNMAPPED_GENRE):
        return ()
```

New text:

```
    if False:
        return ()
```

### `u284.C2_outage_named_refused`

tagging.cli._refused_out: a file another catalogue was down for is named as refused

- File: `src/cratekit/tagging/summary.py`
- Source: `u284.json`, row `C2_outage_named_refused`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_pass_whose_catalogues_answered_says_nothing_of_refusals`
  - `tests/test_sync_refused.py::test_a_sweep_beatport_never_refused_names_nothing`

Old text:

```
    if not others or any(said[source] != searchers.Answer.BLOCKED.value for source in others):
```

New text:

```
    if not others:
```

### `u284.C4_stop_never_collected`

tagging.cli._summary: no failed file is read as one every catalogue refused

- File: `src/cratekit/tagging/summary.py`
- Source: `u284.json`, row `C4_stop_never_collected`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token`
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
        if cause is not None and isinstance((cause.detail or {}).get(searchers.REFUSED_DETAIL), dict):
```

New text:

```
        if False:
```

### `u284.C6_token_unsaid`

tagging.cli._refusal_stop: Discogs unasked is never said and its token step never given

- File: `src/cratekit/tagging/summary.py`
- Source: `u284.json`, row `C6_token_unsaid`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_stop_over_a_token_discogs_refused_never_says_waiting_mends_it`
  - `tests/test_sync_refused.py::test_a_sweep_with_no_token_fails_each_file_and_says_who_refused_and_the_token`
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
    if unasked:
        why = 
```

New text:

```
    if False:
        why = 
```

### `u284.C7_rejected_token_told_to_wait`

tagging.cli._refusal_stop: a stop over a rejected token says waiting mends it

- File: `src/cratekit/tagging/summary.py`
- Source: `u284.json`, row `C7_rejected_token_told_to_wait`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_tag_workers.py`, `tests/test_tag_folder_copyright.py`, `tests/test_discogs_first.py`
- Collected: 227 against a baseline of 227
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_stop_over_a_token_discogs_refused_never_says_waiting_mends_it`

Old text:

```
    if unasked != searchers.DISCOGS_TOKEN_REFUSED:
```

New text:

```
    if True:
```

### `u56-catalogue-searcher-and-tag-workers.R23_summary_from_the_queue`

The report counts what was queued rather than what ran, so a half finished sweep reports every file as handled

- File: `src/cratekit/tagging/summary.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R23_summary_from_the_queue`
- Moved: Anchored where u306-replay-after-c.json replayed it: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 27 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_report_from_before_the_repair_is_counted_under_no_status`
  - `tests/test_tag_workers.py::test_a_sweep_beatport_matched_whole_names_no_fallback_as_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_a_token_discogs_refuses_is_warned_about_even_when_beatport_settles_every_file`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - ... and 12 more, see the JSON sidecar

Old text:

```
    for report in artifacts.committed(cfg, job_id):
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
```

New text:

```
    for report in []:
        reason = str(report.get("skipped") or "")
        source_genre = str(report.get("source_genre") or "")
```

### `u84-b.C2_summary_zero_filled`

The summary lists only the statuses it saw, so none repaired and not counted read the same

- File: `src/cratekit/tagging/summary.py`
- Source: `u84-b.json`, row `C2_summary_zero_filled`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_report_from_before_the_repair_is_counted_under_no_status`
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`

Old text:

```
        "art_repair": art_repair,
```

New text:

```
        "art_repair": {key: value for key, value in art_repair.items() if value},
```

### `u84-b.C3_old_reports_uncounted`

A report committed before the repair existed is counted as ok, a status nobody measured

- File: `src/cratekit/tagging/summary.py`
- Source: `u84-b.json`, row `C3_old_reports_uncounted`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_report_from_before_the_repair_is_counted_under_no_status`

Old text:

```
        status = str(report.get("art_repair") or "")
```

New text:

```
        status = str(report.get("art_repair") or art.REPAIR_OK)
```

### `u85-a.A16_summary_counts_art`

The job summary never counts an art status

- File: `src/cratekit/tagging/summary.py`
- Source: `u85-a.json`, row `A16_summary_counts_art`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`
- Collected: 102 against a baseline of 102
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`

Old text:

```
            art_fetch[fetched] += 1
```

New text:

```
            pass
```

### `r1724.N11_tag_one_raw_stem`

tag_one: hand the searcher the raw stem, so the match reads mix)_pn and the Obiman release is missed

- File: `src/cratekit/tagging/tag.py`
- Source: `r1724.json`, row `N11_tag_one_raw_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_name_tail.py::test_a_file_with_an_artist_tag_and_no_title_tag_is_asked_its_name_past_the_tail`
  - `tests/test_name_tail.py::test_sunshine_hotel_is_asked_by_its_artist_and_title_and_no_source_sees_the_tail`
  - `tests/test_name_tail.py::test_the_obiman_name_is_asked_its_title_and_takes_the_release_a_person_would_type`
  - `tests/test_name_tail.py::test_the_obiman_name_matches_its_release_whatever_discogs_is_asked`

Old text:

```
    title = title_tag or titles.name_title(path.stem)
```

New text:

```
    title = title_tag or path.stem
```

### `r289-a.A1_appledouble_gone`

Drop the AppleDouble skip, so a sidecar is walked as a track

- File: `src/cratekit/tagging/tag.py`
- Source: `r289-a.json`, row `A1_appledouble_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_the_walk_skips_what_is_no_track_and_keeps_every_track[the_walk_skips_the_appledouble_sidecar_beside_a_real_track]`

Old text:

```
        and not path.name.startswith(APPLEDOUBLE_PREFIX)
```

New text:

```
        and True
```

### `r289-a.A2_appledouble_one_dot`

Widen the sidecar prefix to a bare dot, the defect the review caught

- File: `src/cratekit/tagging/tag.py`
- Source: `r289-a.json`, row `A2_appledouble_one_dot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_the_walk_skips_what_is_no_track_and_keeps_every_track[a_title_that_opens_with_dots_is_walked_and_so_is_the_album_holding_it]`

Old text:

```
APPLEDOUBLE_PREFIX = "._"
```

New text:

```
APPLEDOUBLE_PREFIX = "."
```

### `r289-a.A3_staging_dirs_gone`

Drop the staging tree skip, so a partial download is queued as a track

- File: `src/cratekit/tagging/tag.py`
- Source: `r289-a.json`, row `A3_staging_dirs_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_real_track_beside_the_staging_tree_is_still_queued`
  - `tests/test_tag_workers.py::test_tagging_the_download_root_queues_nothing_from_the_acquisition_staging_tree`
  - `tests/test_tagging_engine.py::test_the_walk_skips_what_is_no_track_and_keeps_every_track[the_master_staging_tree_is_skipped_too]`
  - `tests/test_tagging_engine.py::test_the_walk_skips_what_is_no_track_and_keeps_every_track[the_walk_does_not_descend_into_the_acquisition_staging_tree]`

Old text:

```
        and not SKIPPED_DIRNAMES.intersection(path.relative_to(root).parts[:-1])
```

New text:

```
        and True
```

### `r289-a.A4_staging_dirs_acquire_only`

Forget the master staging tree, keeping the acquisition one

- File: `src/cratekit/tagging/tag.py`
- Source: `r289-a.json`, row `A4_staging_dirs_acquire_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 2 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_the_skipped_dirnames_are_the_two_constants_that_own_them`
  - `tests/test_tagging_engine.py::test_the_walk_skips_what_is_no_track_and_keeps_every_track[the_master_staging_tree_is_skipped_too]`

Old text:

```
SKIPPED_DIRNAMES: frozenset[str] = frozenset(
    {".cratekit-acquire-staging", ".cratekit-master-staging"}
)
```

New text:

```
SKIPPED_DIRNAMES: frozenset[str] = frozenset({".cratekit-acquire-staging"})
```

### `r289-a.A5_staging_dirs_absolute`

Match the staging names on the absolute path, not relative to the root

- File: `src/cratekit/tagging/tag.py`
- Source: `r289-a.json`, row `A5_staging_dirs_absolute`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_root_that_is_itself_a_staging_tree_is_still_walked`

Old text:

```
        and not SKIPPED_DIRNAMES.intersection(path.relative_to(root).parts[:-1])
```

New text:

```
        and not SKIPPED_DIRNAMES.intersection(path.parts)
```

### `r650-a.B3_engine_drops_the_flag_on_the_write`

The one branch that wrote a word stops recording where the word came from

- File: `src/cratekit/tagging/tag.py`
- Source: `r650-a.json`, row `B3_engine_drops_the_flag_on_the_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`
  - `tests/test_tagging_engine.py::test_a_file_with_no_genre_takes_what_the_searcher_answered[a_word_the_taxonomy_does_not_know_is_written_and_reported]`

Old text:

```
        off_taxonomy = hit.off_taxonomy
```

New text:

```
        off_taxonomy = False
```

### `r650-a.B4_engine_leaks_the_flag_onto_a_skip`

The flag is read off the hit for every file, so a has-genre skip claims a word this run did not write

- File: `src/cratekit/tagging/tag.py`
- Source: `r650-a.json`, row `B4_engine_leaks_the_flag_onto_a_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_file_this_engine_did_not_tag_is_never_off_taxonomy`

Old text:

```
    written: str | None = None
    off_taxonomy = False
```

New text:

```
    written: str | None = None
    off_taxonomy = bool(hit and hit.off_taxonomy)
```

### `r791-b.T1_sources_unread_disposition`

tag_one: a decline naming unread sources is reported no-hit

- File: `src/cratekit/tagging/tag.py`
- Source: `r791-b.json`, row `T1_sources_unread_disposition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 12 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`
  - `tests/test_tagging_engine.py::test_a_decline_beside_an_unread_catalogue_is_sources_unread_and_not_no_hit`

Old text:

```
        elif hit.unread:
```

New text:

```
        elif False:
```

### `r791-b.T2_art_names_unread`

_art_embedded: the picture decline never names the unread sources

- File: `src/cratekit/tagging/tag.py`
- Source: `r791-b.json`, row `T2_art_names_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_decline_beside_an_unread_catalogue_is_sources_unread_and_not_no_hit`

Old text:

```
        unread = hit.unread if hit is not None else ()
```

New text:

```
        unread = ()
```

### `r796-b.O9_no_isrc_is_not_no_hit`

tag_one: drop the no-isrc skip reason, so a file the general catalogue could not be asked about is no-hit (AE4)

- File: `src/cratekit/tagging/tag.py`
- Source: `r796-b.json`, row `O9_no_isrc_is_not_no_hit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_catalogue_searcher.py`
- Collected: 380 against a baseline of 380
- Kills: 3 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_malformed_isrc_tag_is_reported_with_what_it_held`
  - `tests/test_published_genre.py::test_ae4_a_file_with_no_isrc_is_reported_as_that_and_not_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`

Old text:

```
        elif any(said.answer == NO_ISRC for said in hit.answers):
```

New text:

```
        elif False:
```

### `u240.M1_two_names_take_the_first`

_by_label: a line naming two registered labels gives the file the first one's genre

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M1_two_names_take_the_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_searchers_park_reaches_the_job_as_a_park_on_a_file_its_line_could_not_settle`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_another_act_sharing_a_labels_first_letters_is_never_that_label[two-registered-labels]`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`

Old text:

```
    if len(named) != 1 or not named[0].genre:
```

New text:

```
    if not named or not named[0].genre:
```

### `u240.M2_no_genre_label_named`

_by_label: a line naming one label with no genre is not recorded on the file

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M2_no_genre_label_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_another_act_sharing_a_labels_first_letters_is_never_that_label[one-label-with-no-genre]`
  - `tests/test_tag_folder_copyright.py::test_another_act_sharing_a_labels_first_letters_is_never_that_label[two-registered-labels]`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`

Old text:

```
        return _Labelled(None, own, copyright_labels=tuple(found.label for found in named))
```

New text:

```
        return _Labelled(None, own, copyright_labels=())
```

### `u240.M3_tag_no_longer_outranks_the_line`

_by_label: a file's own label tag no longer comes first, so the line or --label decides a tagged file

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M3_tag_no_longer_outranks_the_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 17 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`
  - `tests/test_label_genre.py::test_a_file_of_a_label_with_no_genre_is_searched_as_today`
  - `tests/test_label_genre.py::test_a_folder_of_mixed_labels_tags_each_by_its_own`
  - `tests/test_label_genre.py::test_a_label_tag_reaches_its_genre_with_no_label_named`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_puls_file_with_no_genre_gets_its_labels_genre_with_no_searcher_called`
  - `tests/test_label_genre.py::test_a_puls_file_with_no_picture_is_searched_for_its_art_only`
  - `tests/test_label_genre.py::test_a_refusal_on_the_art_search_does_not_fail_a_puls_file`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_an_art_search_for_a_labelled_file_never_offers_the_general_catalogue_its_isrc`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_verbs_label_names_the_label_of_a_file_with_no_tag_and_the_tag_wins`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    if own:

```

New text:

```
    if False:

```

### `u240.M4_folder_label_no_longer_outranks_the_line`

_by_label: --label no longer comes before the copyright line

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M4_folder_label_no_longer_outranks_the_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 9 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`
  - `tests/test_label_genre.py::test_the_verbs_label_names_the_label_of_a_file_with_no_tag_and_the_tag_wins`
  - `tests/test_tag_folder_copyright.py::test_the_verbs_label_outranks_the_copyright_line`

Old text:

```
    if typed:

```

New text:

```
    if False:

```

### `u240.M5_wrong_field_read`

_by_label: the label tag read where the copyright line should be

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M5_wrong_field_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_label_batch_with_every_catalogue_blocked_lands_tagged_by_label`
  - `tests/test_tag_folder_copyright.py::test_a_mixed_folder_with_every_catalogue_blocked_tags_each_file_by_its_line`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_an_unregistered_file_in_the_batch_is_left_untagged_and_its_item_fails`
  - `tests/test_tag_folder_copyright.py::test_another_act_sharing_a_labels_first_letters_is_never_that_label[one-label-with-no-genre]`
  - `tests/test_tag_folder_copyright.py::test_another_act_sharing_a_labels_first_letters_is_never_that_label[two-registered-labels]`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`
  - `tests/test_tag_folder_copyright.py::test_the_needles_are_frozen_with_the_genres_when_the_sweep_is_queued`
  - `tests/test_tag_folder_copyright.py::test_the_report_names_each_file_by_label_by_catalogue_or_not_at_all`
  - `tests/test_tag_folder_copyright.py::test_the_tails_tag_step_lands_a_label_batch_with_every_catalogue_blocked`
  - `tests/test_tag_folder_copyright.py::test_two_labels_sharing_a_display_name_never_lend_each_other_a_genre`

Old text:

```
        line = held["copyright"] or ""
```

New text:

```
        line = held["label"] or ""
```

### `u240.M6_named_by_lost`

tag_one: the record says nothing of how the label was named

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M6_named_by_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_label_batch_with_every_catalogue_blocked_lands_tagged_by_label`
  - `tests/test_tag_folder_copyright.py::test_a_label_tag_naming_a_label_with_a_genre_is_named_by_the_tag`
  - `tests/test_tag_folder_copyright.py::test_a_mixed_folder_with_every_catalogue_blocked_tags_each_file_by_its_line`
  - `tests/test_tag_folder_copyright.py::test_the_report_names_each_file_by_label_by_catalogue_or_not_at_all`
  - `tests/test_tag_folder_copyright.py::test_the_verbs_label_outranks_the_copyright_line`

Old text:

```
            "label_from": tier.named_by,
```

New text:

```
            "label_from": "",
```

### `u240.M7_line_labels_dropped_from_result`

tag_one: the labels an unsettled line named never reach the result

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M7_line_labels_dropped_from_result`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_another_act_sharing_a_labels_first_letters_is_never_that_label[one-label-with-no-genre]`
  - `tests/test_tag_folder_copyright.py::test_another_act_sharing_a_labels_first_letters_is_never_that_label[two-registered-labels]`
  - `tests/test_tag_folder_copyright.py::test_files_whose_line_named_two_labels_are_counted_and_warned`

Old text:

```
        copyright_labels=tier.copyright_labels,
```

New text:

```
        copyright_labels=(),
```

### `u240.M8_failed_files_line_dropped`

tag_one: a failed file's refusal no longer carries its line's labels

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M8_failed_files_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`

Old text:

```
        if needs_genre and tier.copyright_labels and type(exc) is CratekitError:
```

New text:

```
        if False:
```

### `u240.M9_park_flattened`

tag_one: a searcher's park on an unsettled line is rebuilt as a plain refusal

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M9_park_flattened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_searchers_park_reaches_the_job_as_a_park_on_a_file_its_line_could_not_settle`

Old text:

```
        if needs_genre and tier.copyright_labels and type(exc) is CratekitError:
```

New text:

```
        if needs_genre and tier.copyright_labels:
```

### `u260.E1_engine_encodes_per_file`

_art_embedded: call the plain encoder again, so every file encodes the same bytes

- File: `src/cratekit/tagging/tag.py`
- Source: `u260.json`, row `E1_engine_encodes_per_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 196 against a baseline of 196
- Kills: 8 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_an_albums_files_naming_one_address_make_one_request_one_wait_and_one_encode`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_two_addresses_serving_the_same_bytes_make_two_requests_and_one_encode`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
        cdj = art.to_cdj_jpeg_remembered(data)
```

New text:

```
        cdj = art.to_cdj_jpeg(data)
```

### `u282.T1_question_asked_with_a_picture`

tag_one: the picture's question is asked whatever the file holds, so a file with a picture spends a Beatport request

- File: `src/cratekit/tagging/tag.py`
- Source: `u282.json`, row `T1_question_asked_with_a_picture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_that_has_a_picture_sends_beatport_nothing`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
    if settled is None and hit is not None and hit.ask_picture is not None:
```

New text:

```
    if hit is not None and hit.ask_picture is not None:
```

### `u282.T2_question_never_asked`

tag_one: the picture's question is never asked (merge blocker 5)

- File: `src/cratekit/tagging/tag.py`
- Source: `u282.json`, row `T2_question_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_picture_ask_that_raises_never_fails_the_file`
  - `tests/test_discogs_first.py::test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread`
  - `tests/test_discogs_first.py::test_a_tagged_file_with_no_picture_keeps_its_genre_and_gets_the_cover`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
    if settled is None and hit is not None and hit.ask_picture is not None:
```

New text:

```
    if False:
```

### `u289.T1_title_tag_split`

tag_one: a file with a title tag and no artist tag is split by its name

- File: `src/cratekit/tagging/tag.py`
- Source: `u289.json`, row `T1_title_tag_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_title_tag_with_no_artist_tag_is_never_split_by_its_name`

Old text:

```
    named = titles.by_name(path.stem) if not artist and not title_tag else None
```

New text:

```
    named = titles.by_name(path.stem) if not artist else None
```

### `u289.T2_split_artist_dropped`

tag_one: the name's artist is read and never handed to the searcher

- File: `src/cratekit/tagging/tag.py`
- Source: `u289.json`, row `T2_split_artist_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_mp3_named_untagged_file_carries_no_marker_into_the_question`
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_discogs_question.py::test_an_untagged_file_named_artist_and_title_takes_the_release_that_names_both`
  - `tests/test_discogs_question.py::test_the_sweeps_record_names_the_question_each_file_was_asked`

Old text:

```
    if named is not None:
        artist = named.artist
```

New text:

```
    if False:
        artist = named.artist
```

### `u289.T3_record_read_from_title`

tag_one: the record says how the title was read for a file asked by its name

- File: `src/cratekit/tagging/tag.py`
- Source: `u289.json`, row `T3_record_read_from_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_name_that_reads_to_no_one_split_is_asked_with_no_artist_and_says_so`
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_discogs_question.py::test_the_sweeps_record_names_the_question_each_file_was_asked`

Old text:

```
        if named is not None and named.read in (titles.Read.BY_NAME, titles.Read.NAME_AMBIGUOUS):
```

New text:

```
        if False:
```

### `u56-catalogue-searcher-and-tag-workers.R14_walk_unsorted`

The walk stops sorting, so an enqueue and a later walk disagree about ordinal order and one file's report is filed under another's name

- File: `src/cratekit/tagging/tag.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R14_walk_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_tag_folder_by_hand_queues_and_drives_its_sweep_to_succeeded_in_one_call`
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
        for path in sorted(root.rglob("*"))
```

New text:

```
        for path in root.rglob("*")
```

### `u56-catalogue-searcher-and-tag-workers.R15_walk_not_recursive`

The walk stops recursing, so a folder of subfolders queues nothing and reports the honest zero over a library

- File: `src/cratekit/tagging/tag.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R15_walk_not_recursive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tagging_engine.py::test_the_walk_recurses_and_comes_back_sorted`
  - `tests/test_tagging_engine.py::test_the_walk_skips_what_is_no_track_and_keeps_every_track[a_title_that_opens_with_dots_is_walked_and_so_is_the_album_holding_it]`
  - `tests/test_tagging_engine.py::test_the_walk_skips_what_is_no_track_and_keeps_every_track[the_skip_does_not_stop_the_walk_recursing]`

Old text:

```
        for path in sorted(root.rglob("*"))
```

New text:

```
        for path in sorted(root.glob("*"))
```

### `u85-a.A11_failed_write_is_error`

A write the file refused is reported embedded

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A11_failed_write_is_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_picture_the_file_will_not_take_is_an_error_and_the_genre_stands`

Old text:

```
    if not written:
```

New text:

```
    if False:
```

### `u85-a.A1_search_skipped_only_with_both`

A tagged file skips the search whatever its art, so a tagged file with no picture is never given one

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A1_search_skipped_only_with_both`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_the_skip_reason_reaches_the_report_and_not_only_the_artifact`
  - `tests/test_tagging_engine.py::test_a_file_this_engine_did_not_tag_is_never_off_taxonomy`
  - `tests/test_tagging_engine.py::test_a_file_with_a_genre_and_no_art_gets_art_and_its_genre_is_untouched`
  - `tests/test_tagging_engine.py::test_a_tagged_file_nobody_carries_is_still_has_genre_and_art_unavailable`
  - `tests/test_tagging_engine.py::test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal[catalogue-parse-broken]`
  - `tests/test_tagging_engine.py::test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal[catalogue-unreachable]`
  - `tests/test_tagging_engine.py::test_a_tagged_file_whose_searcher_breaks_outright_still_raises`
  - `tests/test_tagging_engine.py::test_the_folder_pass_produces_exactly_what_the_per_file_calls_produce`

Old text:

```
if existing and settled is not None:
```

New text:

```
if existing:
```

### `u85-a.A2_any_picture_settles`

A file carrying a picture is treated as needing one, so art it already has is re-downloaded over

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A2_any_picture_settles`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 8 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tagging_engine.py::test_a_file_that_already_carries_a_genre_is_skipped_and_never_overwritten`
  - `tests/test_tagging_engine.py::test_a_file_that_already_has_a_genre_is_still_repaired`
  - `tests/test_tagging_engine.py::test_a_tagged_file_with_zeroed_art_is_repaired_and_never_fetched`
  - `tests/test_tagging_engine.py::test_an_untagged_file_with_zeroed_art_gets_its_genre_and_keeps_its_picture`
  - `tests/test_tagging_engine.py::test_the_folder_pass_asks_once_per_untagged_file`

Old text:

```
    if pictures:
        return {"art_fetch": ART_PRESENT
```

New text:

```
    if False:
        return {"art_fetch": ART_PRESENT
```

### `u85-a.A5_no_url_guard`

A hit naming no picture is still fetched, with an empty URL

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A5_no_url_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_published_genre.py::test_a_picture_from_beatports_row_is_reported_as_beatports`

Old text:

```
    if not hit.art_url:
```

New text:

```
    if False:
```

### `u85-a.A6_no_fetch_guard`

No fetch supplied calls None and reports the TypeError as a fetch failure

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A6_no_fetch_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_picture_that_cannot_be_fetched_is_unavailable_and_the_genre_still_lands[no_fetch_supplied_is_unavailable_rather_than_a_silent_skip]`

Old text:

```
    if fetch_image is None:
```

New text:

```
    if False:
```

### `u85-a.A7_fetch_raise_is_a_decline`

A fetch that raises fails the item instead of reporting art unavailable

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A7_fetch_raise_is_a_decline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_picture_that_cannot_be_fetched_is_unavailable_and_the_genre_still_lands[a_fetch_that_raises_is_unavailable_and_never_fails_the_item]`

Old text:

```
    except Exception as exc:  # noqa: BLE001
        return result(ART_UNAVAILABLE, f"the picture at {url} could not be fetched: {exc}")
```

New text:

```
    except ZeroDivisionError as exc:  # noqa: BLE001
        return result(ART_UNAVAILABLE, f"the picture at {url} could not be fetched: {exc}")
```

### `u85-a.A9_not_a_picture_is_a_decline`

Bytes that are not an image fail the item instead of reporting art unavailable

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A9_not_a_picture_is_a_decline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_picture_that_cannot_be_fetched_is_unavailable_and_the_genre_still_lands[bytes_that_are_not_a_picture_are_unavailable_and_nothing_is_embedded]`

Old text:

```
    except art.ArtError as exc:
        return result(ART_UNAVAILABLE, f"what
```

New text:

```
    except ZeroDivisionError as exc:
        return result(ART_UNAVAILABLE, f"what
```

### `r1724.N6_tail_never_dropped`

name_title: return the stem whatever it ends with, main's reading

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N6_tail_never_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 81 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_name_tail.py::test_a_file_with_an_artist_tag_and_no_title_tag_is_asked_its_name_past_the_tail`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[06A - 126 - Sean Doron - Sunshine Hotel_PN-06A - 126 - Sean Doron - Sunshine Hotel]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[8A - 124 - [MP3] Lane 8 - Aba_PN-8A - 124 - [MP3] Lane 8 - Aba]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)_PN-9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Attention_PN-Attention]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Promise to Stay Here_PN-Promise to Stay Here]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood [Nightwave Remix]_PN-Sunrise Mood [Nightwave Remix]]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood _PN-Sunrise Mood]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood_PN  -Sunrise Mood]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Foo) Bar (feat. X) (Extended Mix)-(Foo) Bar]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro) (Extended Mix)-(Intro)]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro)-(Intro)]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro)-Intro (Original Mix)]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro)-Intro]`
  - ... and 66 more, see the JSON sidecar

Old text:

```
        return stem
    return DASH.join(parts)
```

New text:

```
        return stem
    return stem
```

### `r1724.N7_tail_word`

NAME_TAIL: the tail without its underscore, so Sunrise Mood PN loses a word

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N7_tail_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 82 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_name_tail.py::test_a_file_with_an_artist_tag_and_no_title_tag_is_asked_its_name_past_the_tail`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[06A - 126 - Sean Doron - Sunshine Hotel_PN-06A - 126 - Sean Doron - Sunshine Hotel]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[8A - 124 - [MP3] Lane 8 - Aba_PN-8A - 124 - [MP3] Lane 8 - Aba]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)_PN-9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Attention_PN-Attention]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Promise to Stay Here_PN-Promise to Stay Here]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood [Nightwave Remix]_PN-Sunrise Mood [Nightwave Remix]]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood _PN-Sunrise Mood]`
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood_PN  -Sunrise Mood]`
  - `tests/test_name_tail.py::test_a_name_with_no_tail_is_read_byte_for_byte[Sunrise Mood PN]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Foo) Bar (feat. X) (Extended Mix)-(Foo) Bar]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro) (Extended Mix)-(Intro)]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro)-(Intro)]`
  - `tests/test_name_tail.py::test_every_matching_corpus_name_still_matches_with_the_tail_written_after_it[(Intro)-Intro (Original Mix)]`
  - ... and 67 more, see the JSON sidecar

Old text:

```
NAME_TAIL = "_PN"
```

New text:

```
NAME_TAIL = "PN"
```

### `r1724.S1_u289_head_needs_a_key`

sample, U289: _past_head reads any leading head, a tempo alone included

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `S1_u289_head_needs_a_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[122 - Kerri Chandler - On My Way--Read.AS_WRITTEN]`
  - `tests/test_discogs_question.py::test_a_title_with_no_head_is_asked_exactly_as_before[124 - Sunrise Mood-124 - Sunrise Mood-Bernard+Badie+124+-+Sunrise+Mood]`
  - `tests/test_discogs_question.py::test_a_title_with_no_head_is_asked_exactly_as_before[99 - Luftballons-99 - Luftballons-Bernard+Badie+99+-+Luftballons]`

Old text:

```
    if not body or not _a_head(words(DASH.join(parts[:body]))):
        return None
```

New text:

```
    if not body:
        return None
```

### `r1724.S2_u289_version_part`

sample, U289: by_name splits a name whose second part ends in a version

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `S2_u289_version_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122 - Kerri Chandler - Original Mix--Read.NAME_AMBIGUOUS]`

Old text:

```
            and not _ends_in_version(folded_title)

```

New text:

```
(empty)
```

### `u280-pinned.M06_marker_read_anywhere`

read_title: a square bracketed group is read past at any part, not only where the naming verb writes its marker

- File: `src/cratekit/tagging/titles.py`
- Source: `u280-pinned.json`, row `M06_marker_read_anywhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 1 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-Bernard Badie - [Love] Is The Message-(Hate) Is The Message]`

Old text:

```
    found = _MARKER.match(text) if marker else None

```

New text:

```
    found = _MARKER.match(text)

```

### `u280-pinned.M11_ambiguity_featured_credits`

_only_a_list_reads: a part naming the artist only as featured counts among several credits

- File: `src/cratekit/tagging/titles.py`
- Source: `u280-pinned.json`, row `M11_ambiguity_featured_credits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 1 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_each_way_a_credit_is_written_is_known[Bernard Badie & Tide-08A - 124 - Sunrise Mood (feat. Tide) - Bernard Badie - Vocal Mix-Sunrise Mood]`

Old text:

```
    if len(credits) > 1 and not all(_credits_before_featuring(parts[index], names) for index in credits):

```

New text:

```
    if False:

```

### `u280-pinned.M29_marker_number_from_all_words`

read_title: past the marker a track number is decided from all remaining words, "[MP3] 01 - Artist - (Intro)" (round one's BLOCKING F1, as a row)

- File: `src/cratekit/tagging/titles.py`
- Source: `u280-pinned.json`, row `M29_marker_number_from_all_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 1 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-[MP3] 01 - Original Mix-Original Mix]`

Old text:

```
            numbered=_numbered(words(text[found.end() :].split(DASH)[0])),

```

New text:

```
            numbered=_numbered(words(text[found.end() :])),

```

### `u280.M01_ambiguous_read_as_titled`

matches: an ambiguous name is matched as a titled one, by its whole name only, so no row writing its split confirms it

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M01_ambiguous_read_as_titled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 32 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_featured_artists_name_takes_no_self_titled_genre_on_a_mixed_page[-1-False]`
  - `tests/test_title_matcher.py::test_a_featured_artists_name_takes_no_self_titled_genre_on_a_mixed_page[-1-True]`
  - `tests/test_title_matcher.py::test_a_featured_artists_name_takes_no_self_titled_genre_on_a_mixed_page[1-False]`
  - `tests/test_title_matcher.py::test_a_featured_artists_name_takes_no_self_titled_genre_on_a_mixed_page[1-True]`
  - `tests/test_title_matcher.py::test_a_name_hiding_the_shape_is_ambiguous_too[Bernard Badie & Tide-Bernard Badie - Tide - Sunrise Mood Extended Mix-Bernard Badie-Sunrise Mood (Extended Mix)]`
  - `tests/test_title_matcher.py::test_a_name_hiding_the_shape_is_ambiguous_too[Bernard Badie & Tide-Bernard Badie - Tide - Sunrise Mood Extended Mix-Tide-Sunrise Mood - Extended Mix]`
  - `tests/test_title_matcher.py::test_a_name_hiding_the_shape_is_ambiguous_too[Bernard Badie-08A - 124 - Bernard Badie - Vocal Mix feat. Tide-Vocal Mix-Bernard Badie (Vocal Mix feat. Tide)]`
  - `tests/test_title_matcher.py::test_a_name_hiding_the_shape_is_ambiguous_too[Bernard Badie-Bernard Badie - Bernard Badie - Vocal Mix-Bernard Badie-Bernard Badie (Vocal Mix)]`
  - `tests/test_title_matcher.py::test_a_name_hiding_the_shape_is_ambiguous_too[Bernard Badie-Bernard Badie - Vocal Mix feat. Tide-Vocal-Bernard Badie (Vocal Mix)]`
  - `tests/test_title_matcher.py::test_a_self_titled_tracks_dash_version_the_list_lacks_finds_its_own_row_only_when_it_writes_the_version`
  - `tests/test_title_matcher.py::test_a_split_reads_past_a_feature_credit_and_the_files_own_brackets[Bernard Badie - Sunrise Mood Extended Mix (Tide Edit)-Sunrise Mood (Extended Mix) (Tide Edit)]`
  - `tests/test_title_matcher.py::test_a_split_reads_past_a_feature_credit_and_the_files_own_brackets[Bernard Badie - Sunrise Mood Remix (2014)-Sunrise Mood (Remix) (2014)]`
  - `tests/test_title_matcher.py::test_a_split_reads_past_a_feature_credit_and_the_files_own_brackets[Bernard Badie feat. Tide - Sunrise Mood Extended Mix-Bernard Badie (Sunrise Mood Extended Mix)]`
  - `tests/test_title_matcher.py::test_a_split_reads_past_a_feature_credit_and_the_files_own_brackets[Bernard Badie feat. Tide - Sunrise Mood Extended Mix-Sunrise Mood (Extended Mix)]`
  - `tests/test_title_matcher.py::test_artist_then_a_version_ending_part_matches_a_row_that_writes_the_same_split[08A - 124 - Bernard Badie - Kerri Chandler Remix-Bernard Badie (Kerri Chandler Remix)]`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    if file.outcome is Outcome.AMBIGUOUS:
        return bool(file.splits & row.splits) or _any_same(whole, row.titles)

```

New text:

```
    if file.outcome is Outcome.AMBIGUOUS:
        return _any_same(whole, row.titles)

```

### `u280.M04_bare_meets_bare`

Title.same: two bare names meet, "(Love) Is The Message" meets "(Hate) Is The Message"

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M04_bare_meets_bare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 6 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_title_matches_no_other_recording_either_way_round[(Hate) Is The Message-(Love) Is The Message]`
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-Bernard Badie - [Love] Is The Message-(Hate) Is The Message]`
  - `tests/test_title_matcher.py::test_bandcamp_writes_no_genre_off_another_track_by_the_artist[(Hate) Is The Message-(Love) Is The Message]`
  - `tests/test_title_matcher.py::test_beatport_writes_no_genre_off_another_track_by_the_artist[(Hate) Is The Message-(Love) Is The Message]`
  - `tests/test_title_matcher.py::test_discogs_writes_no_style_off_another_track_by_the_artist[(Hate) Is The Message-(Love) Is The Message]`
  - `tests/test_title_matcher.py::test_traxsource_writes_no_genre_off_another_track_by_the_artist[(Hate) Is The Message-(Love) Is The Message]`

Old text:

```
            self.names & other.names or self.names & other.bare or self.bare & other.names

```

New text:

```
            self.names & other.names or self.names & other.bare or self.bare & other.names or self.bare & other.bare

```

### `u280.M05_marker_not_read_past`

read_title: the naming verb's marker is never read past, "[MP3] (Not Just) Knee Deep" misses its row

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M05_marker_not_read_past`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 2 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_each_way_a_credit_is_written_is_known[Bernard Badie-[MP3] 01 Sunrise Mood-Sunrise Mood]`
  - `tests/test_title_matcher.py::test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other`

Old text:

```
    found = _MARKER.match(text) if marker else None

```

New text:

```
    found = None

```

### `u280.M07_version_alone_after_title`

read_title: a title read after the artist's credit or a track number may be version words alone

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M07_version_alone_after_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 2 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-[MP3] 01 - Original Mix-Original Mix]`
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Bernard Badie-08A - 124 - 05 - Original Mix-05-Original Mix]`

Old text:

```
        return not (after_title and _version_alone(found))

```

New text:

```
        return True

```

### `u280.M09_ambiguity_ignores_feature`

_only_a_list_reads: a feature credit after the version hides the shape again (R-1651's first shape)

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M09_ambiguity_ignores_feature`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 7 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_name_hiding_the_shape_is_ambiguous_too[Bernard Badie-08A - 124 - Bernard Badie - Vocal Mix feat. Tide-Vocal Mix-Bernard Badie (Vocal Mix feat. Tide)]`
  - `tests/test_title_matcher.py::test_a_name_hiding_the_shape_is_ambiguous_too[Bernard Badie-Bernard Badie - Vocal Mix feat. Tide-Vocal-Bernard Badie (Vocal Mix)]`
  - `tests/test_title_matcher.py::test_a_name_is_read_once_into_its_parts[Bernard Badie-Bernard Badie - Vocal Mix feat. Tide-credit title-ambiguous]`
  - `tests/test_title_matcher.py::test_every_ambiguous_shape_writes_no_genre_off_a_row_that_reads_it_one_way[Bernard Badie-08A - 124 - Bernard Badie - Vocal Mix feat. Tide-Vocal Mix-beatport]`
  - `tests/test_title_matcher.py::test_every_ambiguous_shape_writes_no_genre_off_a_row_that_reads_it_one_way[Bernard Badie-08A - 124 - Bernard Badie - Vocal Mix feat. Tide-Vocal Mix-discogs]`
  - `tests/test_title_matcher.py::test_every_ambiguous_shape_writes_no_genre_off_a_row_that_reads_it_one_way[Bernard Badie-Bernard Badie - Vocal Mix feat. Tide-Vocal-beatport]`
  - `tests/test_title_matcher.py::test_every_ambiguous_shape_writes_no_genre_off_a_row_that_reads_it_one_way[Bernard Badie-Bernard Badie - Vocal Mix feat. Tide-Vocal-discogs]`

Old text:

```
    cut = _before_featuring(parts[first])

```

New text:

```
    cut = parts[first]

```

### `u280.M10_ambiguity_one_credit_only`

_only_a_list_reads: more than one credit hides the shape again (R-1651's second shape)

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M10_ambiguity_one_credit_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 12 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_name_hiding_the_shape_is_ambiguous_too[Bernard Badie & Tide-Bernard Badie - Tide - Sunrise Mood Extended Mix-Bernard Badie-Sunrise Mood (Extended Mix)]`
  - `tests/test_title_matcher.py::test_a_name_hiding_the_shape_is_ambiguous_too[Bernard Badie & Tide-Bernard Badie - Tide - Sunrise Mood Extended Mix-Tide-Sunrise Mood - Extended Mix]`
  - `tests/test_title_matcher.py::test_a_name_hiding_the_shape_is_ambiguous_too[Bernard Badie-Bernard Badie - Bernard Badie - Vocal Mix-Bernard Badie-Bernard Badie (Vocal Mix)]`
  - `tests/test_title_matcher.py::test_a_name_is_read_once_into_its_parts[Bernard Badie & Tide-Bernard Badie - Tide - Sunrise Mood Extended Mix-credit credit title-ambiguous]`
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie & Tide-Bernard Badie - Tide feat. Someone - Sunrise Mood Extended Mix-Bernard Badie]`
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie & Tide-Bernard Badie feat. Someone - Tide - Vocal Mix-Bernard Badie]`
  - `tests/test_title_matcher.py::test_every_ambiguous_shape_writes_no_genre_off_a_row_that_reads_it_one_way[Bernard Badie & Tide-Bernard Badie - Tide - Sunrise Mood Extended Mix-Bernard Badie-beatport]`
  - `tests/test_title_matcher.py::test_every_ambiguous_shape_writes_no_genre_off_a_row_that_reads_it_one_way[Bernard Badie & Tide-Bernard Badie - Tide - Sunrise Mood Extended Mix-Bernard Badie-discogs]`
  - `tests/test_title_matcher.py::test_every_ambiguous_shape_writes_no_genre_off_a_row_that_reads_it_one_way[Bernard Badie & Tide-Bernard Badie - Tide - Sunrise Mood Extended Mix-Tide-beatport]`
  - `tests/test_title_matcher.py::test_every_ambiguous_shape_writes_no_genre_off_a_row_that_reads_it_one_way[Bernard Badie & Tide-Bernard Badie - Tide - Sunrise Mood Extended Mix-Tide-discogs]`
  - `tests/test_title_matcher.py::test_every_ambiguous_shape_writes_no_genre_off_a_row_that_reads_it_one_way[Bernard Badie-Bernard Badie - Bernard Badie - Vocal Mix-Bernard Badie-beatport]`
  - `tests/test_title_matcher.py::test_every_ambiguous_shape_writes_no_genre_off_a_row_that_reads_it_one_way[Bernard Badie-Bernard Badie - Bernard Badie - Vocal Mix-Bernard Badie-discogs]`

Old text:

```
    if first >= layout.end or layout.numbered or not credits:

```

New text:

```
    if first >= layout.end or layout.numbered or len(credits) != 1:

```

### `u280.M12_ambiguity_version_alone`

_only_a_list_reads: X of version words alone is ambiguous too, "Artist - Original Mix" no longer the self titled track

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M12_ambiguity_version_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 5 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_name_is_read_once_into_its_parts[Bernard Badie-Bernard Badie - Original Mix-title after-titled]`
  - `tests/test_title_matcher.py::test_artist_then_a_version_ending_part_matches_a_row_that_writes_the_same_split[08A - 124 - Bernard Badie - Original Mix-Bernard Badie (Extended Mix)]`
  - `tests/test_title_matcher.py::test_artist_then_a_version_ending_part_matches_a_row_that_writes_the_same_split[Bernard Badie - Original Mix-Bernard Badie]`
  - `tests/test_title_matcher.py::test_the_artists_part_before_any_other_part_reads_as_it_did[08A - 124 - Bernard Badie - Extended Mix-Bernard Badie (Original Mix)-Extended Mix]`
  - `tests/test_title_matcher.py::test_the_artists_part_before_any_other_part_reads_as_it_did[Bernard Badie - Original Mix-Bernard Badie-Original Mix]`

Old text:

```
    if _version_alone(words(title_core(cut)[0])) or not _ends_in_version(cut):

```

New text:

```
    if not _ends_in_version(cut):

```

### `u280.M17_featured_part_never`

_featured_first_part: a first part naming the artist only as featured is never read as a title

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M17_featured_part_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 6 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_bracketed_title_before_a_feature_is_read_without_the_credit[(Dub Mix) feat. Bernard Badie - Tide-Dub Mix]`
  - `tests/test_title_matcher.py::test_a_bracketed_title_before_a_feature_is_read_without_the_credit[(Intro) feat. Bernard Badie - Tide - Album-(Intro)]`
  - `tests/test_title_matcher.py::test_a_title_crediting_a_featured_artist_is_still_read_without_the_credit[Sunrise Mood (feat. Tide) - Bernard Badie]`
  - `tests/test_title_matcher.py::test_a_title_crediting_a_featured_artist_is_still_read_without_the_credit[Sunrise Mood feat. Tide - Bernard Badie]`
  - `tests/test_title_matcher.py::test_a_title_crediting_a_featured_artist_takes_its_own_genre_listed_first`
  - `tests/test_title_matcher.py::test_each_way_a_credit_is_written_is_known[Tide-Sunrise Mood feat. Tide - Bernard Badie-Sunrise Mood]`

Old text:

```
    if head != 0 or head == layout.title or head not in layout.credits:

```

New text:

```
    if True:

```

### `u280.M18_featured_part_own_credit`

_featured_first_part: the artist's own credit is read as a title too, "Artist feat. Tide" as "artist"

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M18_featured_part_own_credit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 16 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_featured_artists_part_never_reads_the_name_as_the_self_titled_track[Bernard Badie feat. Tide - Sunrise Mood]`
  - `tests/test_title_matcher.py::test_a_files_head_is_never_its_title[Bernard Badie - Sunrise Mood-Bernard Badie]`
  - `tests/test_title_matcher.py::test_a_track_numbered_title_after_a_version_ending_album_is_still_the_title[Bernard Badie - Summer Mix - 01 - Sunrise Mood]`
  - `tests/test_title_matcher.py::test_a_track_numbered_title_after_a_version_ending_album_is_still_the_title[Bernard Badie - Summer Mix - 01 Sunrise Mood Extended Mix]`
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-Bernard Badie - (Intro) (Live)-Bernard Badie]`
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-Bernard Badie - (Intro)-Bernard Badie]`
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-Bernard Badie - Dancing With Bernard Badie-Bernard Badie]`
  - `tests/test_title_matcher.py::test_beatport_ranks_no_row_by_brackets_shed_across_a_dash[Bernard Badie - (Intro) (Live)]`
  - `tests/test_title_matcher.py::test_beatport_ranks_no_row_by_brackets_shed_across_a_dash[Bernard Badie - (Intro)]`
  - `tests/test_title_matcher.py::test_beatport_ranks_no_row_by_brackets_shed_across_a_dash[Bernard Badie - [Intro]]`
  - `tests/test_title_matcher.py::test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other`
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Bernard Badie-Bernard Badie - Bernard Badie Theme-Bernard Badie Theme-Bernard Badie]`
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Tide-Tide - Riding The Tide-Riding The Tide-Tide]`
  - `tests/test_title_matcher.py::test_the_artists_part_before_any_other_part_reads_as_it_did[Bernard Badie - Sunrise Mood (Extended Mix)-Sunrise Mood-Bernard Badie]`
  - `tests/test_title_matcher.py::test_the_artists_part_before_any_other_part_reads_as_it_did[Bernard Badie - Sunrise Mood-Sunrise Mood-Bernard Badie]`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    if _credits_before_featuring(parts[head], names):
        return None

```

New text:

```
(empty)
```

### `u280.M19_tempo_never_title`

_tempo_as_title: a tempo alone before a version alone is never read as a title

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M19_tempo_never_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 2 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_each_way_a_credit_is_written_is_known[Bernard Badie-100 - Original Mix-100]`
  - `tests/test_title_matcher.py::test_each_way_a_credit_is_written_is_known[Bernard Badie-124 - Interlude-124]`

Old text:

```
    if layout.body != 1 or naming.is_camelot(words(parts[0])[0]):

```

New text:

```
    if True:

```

### `u280.M22_whole_name_shed`

read_file: the whole name is shed across its dashes again

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M22_whole_name_shed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 13 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_featured_artists_name_takes_no_self_titled_genre_on_a_mixed_page[-1-False]`
  - `tests/test_title_matcher.py::test_a_featured_artists_name_takes_no_self_titled_genre_on_a_mixed_page[-1-True]`
  - `tests/test_title_matcher.py::test_a_featured_artists_part_never_reads_the_name_as_the_self_titled_track[01 Bernard Badie feat. Tide - Sunrise Mood Extended Mix]`
  - `tests/test_title_matcher.py::test_a_featured_artists_part_never_reads_the_name_as_the_self_titled_track[Bernard Badie (feat. Tide) - Sunrise Mood Extended Mix]`
  - `tests/test_title_matcher.py::test_a_featured_artists_part_never_reads_the_name_as_the_self_titled_track[Bernard Badie feat. Tide - Sunrise Mood Extended Mix]`
  - `tests/test_title_matcher.py::test_a_featured_artists_part_never_reads_the_name_as_the_self_titled_track[Bernard Badie feat. Tide - Sunrise Mood]`
  - `tests/test_title_matcher.py::test_a_featured_artists_part_never_reads_the_name_as_the_self_titled_track[Bernard Badie feat. Tide - Vocal Mix]`
  - `tests/test_title_matcher.py::test_a_featured_artists_part_never_reads_the_name_as_the_self_titled_track[Bernard Badie featuring Tide - Kerri Chandler Remix]`
  - `tests/test_title_matcher.py::test_a_featured_artists_part_never_reads_the_name_as_the_self_titled_track[Bernard Badie ft. Tide - Sunrise Mood Extended Mix]`
  - `tests/test_title_matcher.py::test_a_featured_artists_part_never_reads_the_name_as_the_self_titled_track[[MP3] Bernard Badie feat. Tide - Sunrise Mood Extended Mix]`
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie & Tide-Bernard Badie feat. Someone - Tide - Vocal Mix-Bernard Badie]`
  - `tests/test_title_matcher.py::test_the_self_titled_split_reads_past_a_marker_and_a_feature_credit_together[01 Bernard Badie feat. Tide - Vocal Mix]`
  - `tests/test_title_matcher.py::test_the_self_titled_split_reads_past_a_marker_and_a_feature_credit_together[[MP3] Bernard Badie feat. Tide - Vocal Mix]`

Old text:

```
    whole = read_title(text, shed=False, numbered=_numbered(words(parts[0])))

```

New text:

```
    whole = read_title(text, shed=True, numbered=_numbered(words(parts[0])))

```

### `u280.M24_track_number_past_marker`

_a_track_number: a lone track number is not read past a marker, "[MP3] 01 - Ame - Title" is titled "01"

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M24_track_number_past_marker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 2 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_each_way_a_credit_is_written_is_known[Bernard Badie-[MP3] 01 - Bernard Badie - (Intro)-(Intro)]`
  - `tests/test_title_matcher.py::test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other`

Old text:

```
    return _LONE_TRACK_NUMBER.fullmatch(_LEADING_GROUPS.sub("", part).strip()) is not None

```

New text:

```
    return _LONE_TRACK_NUMBER.fullmatch(part.strip()) is not None

```

### `u280.M26_brackets_shed_across_a_dash`

own_core: a last part of brackets alone is shed across the dash again, "Artist - (Intro)" read as "artist" (round one's F2)

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M26_brackets_shed_across_a_dash`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 6 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-Bernard Badie - (Intro) (Live)-Bernard Badie]`
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-Bernard Badie - (Intro)-Bernard Badie]`
  - `tests/test_title_matcher.py::test_beatport_ranks_no_row_by_brackets_shed_across_a_dash[Bernard Badie - (Intro) (Live)]`
  - `tests/test_title_matcher.py::test_beatport_ranks_no_row_by_brackets_shed_across_a_dash[Bernard Badie - (Intro)]`
  - `tests/test_title_matcher.py::test_beatport_ranks_no_row_by_brackets_shed_across_a_dash[Bernard Badie - [Intro]]`
  - `tests/test_title_matcher.py::test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other`

Old text:

```
    if DASH in text and not identifies(without_trailing_groups(text.split(DASH)[-1])):

```

New text:

```
    if False:

```

### `u280.M27_leading_groups_across_a_dash`

read_title: the groups a stretch opens with are shed when they are its whole first part, "(Intro) - Original Mix" read as "original mix" (F2)

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M27_leading_groups_across_a_dash`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 2 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-01A - 150 - (Intro) - Bernard Badie - Night Shapes-Bernard Badie]`
  - `tests/test_title_matcher.py::test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other`

Old text:

```
        if lead is not None and identifies(core.split(DASH)[0][lead.end() :]):

```

New text:

```
        if lead is not None:

```

### `u280.M28_any_number_read_past`

read_title: any first word flagged as a number is read past before brackets, "007 (Intro)" as "(Intro)" (round two's BLOCKING, as a row)

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M28_any_number_read_past`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 3 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-007 (Intro)-Intro]`
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-010 (Intro)-(Intro)]`
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-08A - 124 - Bernard Badie - 007 (Intro)-Intro]`

Old text:

```
        elif _a_track_number(found[0]):

```

New text:

```
        else:

```

### `u280.M30_featured_after_a_head`

_featured_first_part: fires after a head too, "08A - 124 - Artist feat. Tide - Title" tagged "Tide" (round one's F3)

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M30_featured_after_a_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 1 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Tide-08A - 124 - Bernard Badie feat. Tide - Sunrise Mood-Bernard Badie]`

Old text:

```
    if head != 0 or head == layout.title or head not in layout.credits:

```

New text:

```
    if head == layout.title or head not in layout.credits:

```

### `u289.N2_head_alone_ambiguous`

by_name: a head alone name is recorded ambiguous rather than head alone

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `N2_head_alone_ambiguous`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122--Read.HEAD_ALONE]`

Old text:

```
    if unsplit.read is Read.HEAD_ALONE:
        return unsplit
```

New text:

```
    if False:
        return unsplit
```

### `u289.N3_three_parts_split`

by_name: a name of three or more parts is split at its first dash

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `N3_three_parts_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122 - Kerri Chandler - On My Way - Album--Read.NAME_AMBIGUOUS]`
  - `tests/test_discogs_question.py::test_a_name_that_reads_to_no_one_split_is_asked_with_no_artist_and_says_so`
  - `tests/test_discogs_question.py::test_the_sweeps_record_names_the_question_each_file_was_asked`

Old text:

```
    if len(rest) == 2:
        artist, title = (part.strip() for part in rest)
```

New text:

```
    if len(rest) >= 2:
        artist, title = rest[0].strip(), DASH.join(rest[1:]).strip()
```

### `u289.N4_version_title_split`

by_name: a second part ending in a version is split, Artist - Original Mix

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `N4_version_title_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122 - Kerri Chandler - Original Mix--Read.NAME_AMBIGUOUS]`

Old text:

```
            and not _ends_in_version(folded_title)
```

New text:

```
            and True
```

### `u289.N5_numbered_title_split`

by_name: a second part opening with a track number is split, Album - 01 Title

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `N5_numbered_title_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122 - Kerri Chandler - 01 On My Way--Read.NAME_AMBIGUOUS]`

Old text:

```
            and not _opens_with_a_track_number(folded_title)
```

New text:

```
            and True
```

### `u289.N6_track_number_artist_split`

by_name: a lone track number is taken as the artist

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `N6_track_number_artist_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122 - 01 - On My Way--Read.NAME_AMBIGUOUS]`

Old text:

```
            and not _a_track_number(folded_artist)
```

New text:

```
            and True
```

### `u289.N7_numbered_artist_split`

by_name: a first part opening with a track number is taken as the artist

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `N7_numbered_artist_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122 - 01 Kerri Chandler - On My Way--Read.NAME_AMBIGUOUS]`

Old text:

```
            and not _numbered(words(folded_artist))
```

New text:

```
            and True
```

### `u289.Q2_head_alone_two_parts`

_past_head: drop the head alone check, so a title 08A - 124 is asked as 124

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `Q2_head_alone_two_parts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122--Read.HEAD_ALONE]`
  - `tests/test_discogs_question.py::test_a_title_of_a_head_alone_is_asked_as_written_and_the_record_says_so`

Old text:

```
    if len(parts) <= 2 and _a_head(words(DASH.join(parts))):
        return []
```

New text:

```
    if False:
        return []
```

### `u289.Q3_marker_kept`

_past_head: keep the marker after the head, so [MP3] rides into the question

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `Q3_marker_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 10 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_head_and_a_marker_alone_are_never_an_empty_track_field`
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122 - [MP3] Kerri Chandler - On My Way-Kerri Chandler-Read.BY_NAME]`
  - `tests/test_discogs_question.py::test_a_name_whose_artist_part_names_nobody_is_not_split[8A - 122 - [MP3] - On My Way]`
  - `tests/test_discogs_question.py::test_an_mp3_marked_title_tag_carries_no_marker_into_the_question`
  - `tests/test_discogs_question.py::test_an_mp3_named_untagged_file_carries_no_marker_into_the_question`
  - `tests/test_discogs_question.py::test_the_headed_cases_are_asked_past_their_head`
  - `tests/test_discogs_question.py::test_the_pictures_question_after_a_discogs_genre_carries_no_head`
  - `tests/test_discogs_question.py::test_the_question_reads_past_the_head_the_marker_and_the_artists_own_part[03B - 83 - [MP3] Kerri Chandler - On My Way-kerri chandler-On My Way]`
  - `tests/test_discogs_question.py::test_the_record_shops_free_text_query_carries_no_head`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xc6ther-08A - 124 - [MP3] Aether - Sun Path-Aether-Sun Path]`

Old text:

```
    if marker is not None:
        rest[0] = rest[0][marker.end() :]
```

New text:

```
    if False:
        rest[0] = rest[0][marker.end() :]
```

### `u289.Q4_artist_part_kept`

question: never read the artist's own part off, so an untagged split asks Artist - Title as its track

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `Q4_artist_part_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 13 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122 - Kerri Chandler - On My Way (Extended Mix)-Kerri Chandler-Read.BY_NAME]`
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122 - Kerri Chandler - On My Way-Kerri Chandler-Read.BY_NAME]`
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122 - [MP3] Kerri Chandler - On My Way-Kerri Chandler-Read.BY_NAME]`
  - `tests/test_discogs_question.py::test_an_mp3_named_untagged_file_carries_no_marker_into_the_question`
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`
  - `tests/test_discogs_question.py::test_an_untagged_file_named_artist_and_title_takes_the_release_that_names_both`
  - `tests/test_discogs_question.py::test_the_question_reads_past_the_head_the_marker_and_the_artists_own_part[03B - 83 - Kerri Chandler - On My Way-Kerri Chandler-On My Way]`
  - `tests/test_discogs_question.py::test_the_question_reads_past_the_head_the_marker_and_the_artists_own_part[03B - 83 - [MP3] Kerri Chandler - On My Way-kerri chandler-On My Way]`
  - `tests/test_discogs_question.py::test_the_sweeps_record_names_the_question_each_file_was_asked`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[Stra\xdfe Bloom-08A - 124 - Strasse Bloom - Sun Path-Strasse Bloom-Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[Trentem\xf8ller-08A - 124 - Trentemoller - Sun Path-Trentemoller-Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[Trentemoller-08A - 124 - Trentem\xf8ller - Sun Path-Trentem\xf8ller-Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xc6ther-08A - 124 - [MP3] Aether - Sun Path-Aether-Sun Path]`

Old text:

```
    if len(rest) > 1 and _same_name(rest[0], artist) and identifies(DASH.join(rest[1:])):
```

New text:

```
    if False:
```

### `u289.Q5_artist_part_needs_title`

question: read the artist's part off even when no title follows it

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `Q5_artist_part_needs_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_the_artists_part_is_read_off_only_when_a_title_follows_it`

Old text:

```
    if len(rest) > 1 and _same_name(rest[0], artist) and identifies(DASH.join(rest[1:])):
```

New text:

```
    if len(rest) > 1 and _same_name(rest[0], artist):
```

### `u289.Q6_same_name_any_overlap`

_same_name: any shared first word reads a part as the artist's own

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `Q6_same_name_any_overlap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_the_question_reads_past_the_head_the_marker_and_the_artists_own_part[03B - 83 - Kerri Chandler & Tide - On My Way-Kerri Chandler-Kerri Chandler & Tide - On My Way]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\u0141ukasz Bloom-08A - 124 - Lukasz Bloom & Tide - Sun Path-Lukasz Bloom & Tide-Lukasz Bloom & Tide - Sun Path]`

Old text:

```
    return bool(mine) and mine == tuple(_folded(word) for word in words(normalized(artist)))
```

New text:

```
    return bool(mine) and mine[:1] == tuple(_folded(word) for word in words(normalized(artist)))[:1]
```

### `u289.Q7_empty_title_asked`

question: ask an empty title past the head rather than the text as written

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `Q7_empty_title_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_head_and_a_marker_alone_are_never_an_empty_track_field`
  - `tests/test_discogs_question.py::test_a_name_splits_only_when_it_reads_to_exactly_one_artist_and_title[8A - 122--Read.HEAD_ALONE]`
  - `tests/test_discogs_question.py::test_a_title_of_a_head_alone_is_asked_as_written_and_the_record_says_so`

Old text:

```
    if not identifies(title):
        return Question(artist, value, Read.HEAD_ALONE)
```

New text:

```
    if False:
        return Question(artist, value, Read.HEAD_ALONE)
```

### `u289.Q8_headless_read_past`

question: a text with no head is asked stripped and NFC normalized instead of byte for byte

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `Q8_headless_read_past`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_beatport_refusal.py`
- Collected: 1437 against a baseline of 1437
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_a_title_with_no_head_is_asked_exactly_as_before[  Sunrise Mood  -Sunrise Mood-Bernard+Badie+++Sunrise+Mood]`

Old text:

```
    if rest is None:
        return Question(artist, value, Read.AS_WRITTEN)
```

New text:

```
    if rest is None:
        return Question(artist, value.strip(), Read.AS_WRITTEN)
```

### `u318.T09_ends_in_version_word`

_naming_words: drop the last word test, so (Part 1) or (Tim Green Vocal) is a version

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T09_ends_in_version_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 6 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[08A - 124 - Make Luv - Room 5-Make Luv]`
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Lost And Found Tim Green-False-False]`
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off (Tim Green)-False-False]`
  - `tests/test_discogs_version.py::test_what_a_title_names_as_its_mix[Two Months Off (Tim Green Vocal)-Fixture Artist-named3]`
  - `tests/test_title_matcher.py::test_artist_then_a_version_ending_part_matches_a_row_that_writes_the_same_split[08A - 124 - Make Luv - Room 5-Make Luv]`
  - `tests/test_title_matcher.py::test_discogs_still_matches_a_title_to_its_own_track[08A - 124 - Make Luv - Room 5-Make Luv]`

Old text:

```
    if not found or not _a_kind_word(found, len(found) - 1) or found[0] in _CREDITS:
```

New text:

```
    if not found or found[0] in _CREDITS:
```

### `u324-pinned.F20_initial_prefix_dropped_pinned`

_runs_in: an initial stands for any word, not only one it opens

- File: `src/cratekit/tagging/titles.py`
- Source: `u324-pinned.json`, row `F20_initial_prefix_dropped_pinned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 2 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-08A - 124 - C. Badie - Sun Path-Sun Path]`
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[\xde\xf3r\xf0ur Badie-08A - 124 - \xc6. Badie - Sun Path-Sun Path]`

Old text:

```
        return mine == theirs or (initial(index) and theirs.startswith(mine))
```

New text:

```
        return mine == theirs or initial(index)
```

### `u324.F14_o_as_oe`

_PLAIN_SPELLINGS: read ø as oe, the Danish transliteration, so Trentemoller no longer meets Trentemøller

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F14_o_as_oe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 16 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_different_spelling_is_still_another_maker[Trentem\xf8ller-Trentemoeller]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[TRENTEM\xd8LLER-Trentemoller]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[Trentem\xf8ller-Trentemoller]`
  - `tests/test_discogs_version.py::test_a_letter_that_also_carries_an_accent_is_read_plain`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[TRENTEM\xd8LLER-Trentemoller]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[Trentem\xf8ller-Trentemoller]`
  - `tests/test_discogs_version.py::test_another_maker_is_still_a_version_miss_with_the_note`
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`
  - `tests/test_discogs_version.py::test_the_mix_spelled_with_its_letter_takes_a_release_writing_it_plain`
  - `tests/test_discogs_version.py::test_the_sitting_file_takes_its_genre_through_tag_one`
  - `tests/test_discogs_version.py::test_the_trentemoller_remix_takes_each_release_the_sweep_named[2667673]`
  - `tests/test_discogs_version.py::test_the_trentemoller_remix_takes_each_release_the_sweep_named[589586]`
  - `tests/test_discogs_version.py::test_the_trentemoller_remix_takes_each_release_the_sweep_named[641256]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[Trentem\xf8ller-08A - 124 - Trentemoller - Sun Path-Trentemoller-Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[Trentemoller-08A - 124 - Trentem\xf8ller - Sun Path-Trentem\xf8ller-Sun Path]`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        "ø": "o",

```

New text:

```
        "ø": "oe",

```

### `u324.F18_written_length_initial`

_runs_in: judge an initial by its written length, round one's NIT 4, so Ĳ. becomes an initial main never read

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F18_written_length_initial`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Ijsbrand Badie-08A - 124 - \u0132. Badie - Sun Path-Sun Path]`

Old text:

```
        return written is not None and len(_unaccented(written[index])) == 1
```

New text:

```
        return written is not None and len(written[index]) == 1
```

### `u324.F19_no_initials`

_names_the_artist: pass no written words, so no initial stands for a word

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F19_no_initials`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 7 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\u01e2sir Badie-08A - 124 - \u01e2. Badie - Sun Path-\u01e2 Badie-\u01e2. Badie - Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xc6sir Badie-08A - 124 - \u01fc. Badie - Sun Path-\u01fc Badie-\u01fc. Badie - Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xc6sop Badie-08A - 124 - \xc6. Badie - Sun Path-\xc6 Badie-\xc6. Badie - Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xde\xf3r\xf0ur Badie-08A - 124 - \xde. Badie - Sun Path-\xde Badie-\xde. Badie - Sun Path]`
  - `tests/test_title_matcher.py::test_a_whole_name_is_never_shed_across_its_dashes[Bernard Badie-08A - 124 - B. Badie - Sun Path-B Badie]`
  - `tests/test_title_matcher.py::test_each_way_a_credit_is_written_is_known[Bernard Badie-08A - 124 - B. Badie - Sun Path-Sun Path]`
  - `tests/test_title_matcher.py::test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other`

Old text:

```
    return len(folded) > 1 and any(_runs_in(folded, name, written=written) for name in names)
```

New text:

```
    return len(folded) > 1 and any(_runs_in(folded, name) for name in names)
```

### `u118-d.T2_named_word`

Hip-hop & Rap is no longer a Hip-Hop word

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u118-d.json`, row `T2_named_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_routing_parity.py`
- Collected: 928 against a baseline of 926
- Kills: 5 (collect-error)
- Note: collection changed: 928 collected against a baseline of 926. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_adopt_split_place.py::test_a_hip_hop_track_in_the_old_playlist_moves_into_its_band_and_leaves_it[Hip-hop & Rap]`
  - `tests/test_adopt_split_place.py::test_an_approved_move_files_soul_and_hip_hop_in_their_folders_and_keeps_r_and_b`
  - `tests/test_adopt_split_place.py::test_each_word_routes_to_the_folder_the_author_gave_it[Hip-hop & Rap-Hip-Hop]`
  - `tests/test_adopt_split_place.py::test_the_gate_shows_every_soul_and_hip_hop_track_moving_and_no_r_and_b_track`
  - `tests/test_routing_parity.py::test_the_promoted_buckets_take_exactly_what_the_old_code_filed_in_the_playlists_they_left`

Old text:

```
  "Hip-hop & Rap",

```

New text:

```
(empty)
```

### `u133-b.T1_keyword_back`

The jazz keyword rule sends a partial match to NonElectronic again, as before U133

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b.json`, row `T1_keyword_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 946 against a baseline of 945
- Kills: 13 (collect-error)
- Note: collection changed: 946 collected against a baseline of 945. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_a_partial_jazz_match_already_in_rock_is_filed_in_jazz_and_stays_in_rock`
  - `tests/test_adopt_jazz_folder.py::test_a_partial_jazz_match_routes_to_jazz_by_the_keyword_rule_the_author_moved[Acid Jazz]`
  - `tests/test_adopt_jazz_folder.py::test_a_partial_jazz_match_routes_to_jazz_by_the_keyword_rule_the_author_moved[Jazz Funk]`
  - `tests/test_adopt_jazz_folder.py::test_a_partial_jazz_match_routes_to_jazz_by_the_keyword_rule_the_author_moved[jazz]`
  - `tests/test_routing_parity.py::test_the_one_keyword_rule_the_author_moved_takes_only_what_the_old_code_filed_by_it`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_made_before_u133_takes_the_discogs_table_and_loads_after_the_holds_edits`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_with_no_jazz_keyword_rule_is_told_it_has_none`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_with_the_words_out_and_the_row_left_does_not_load`
  - `tests/test_taxonomy_upgrade.py::test_every_bucket_of_the_copy_filing_a_word_is_named_not_the_first`
  - `tests/test_taxonomy_upgrade.py::test_jazz_is_held_while_non_electronic_still_files_its_words_and_every_place_is_named`
  - `tests/test_taxonomy_upgrade.py::test_one_place_filing_a_word_under_two_spellings_names_both_in_one_sentence`
  - `tests/test_taxonomy_upgrade.py::test_the_hand_edit_the_hold_names_lets_jazz_in_on_the_next_run`
  - `tests/test_taxonomy_upgrade.py::test_the_upgrade_that_adds_jazz_says_the_copys_keyword_rule_is_left`

Old text:

```
keyword = "jazz"
bucket = "jazz"

```

New text:

```
keyword = "jazz"
bucket = "non_electronic"

```

### `u133-b.T2_alias_gone`

Jazz loses its routing alias, so a track tagged Jazz reaches it only by the keyword

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b.json`, row `T2_alias_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`, `tests/test_vocabulary.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 1222 against a baseline of 1222
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_a_track_tagged_jazz_routes_to_the_jazz_folder_by_its_alias`
  - `tests/test_routing_parity.py::test_the_promoted_buckets_take_exactly_what_the_old_code_filed_in_the_playlists_they_left`

Old text:

```
aliases = [
  "Jazz",
]

```

New text:

```
aliases = []

```

### `u133-b.T5_former_display`

The former place names a playlist the library does not hold, so the move finds nothing to leave

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b.json`, row `T5_former_display`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`, `tests/test_taxonomy.py`
- Collected: 1038 against a baseline of 1038
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_jazz_left_the_non_electronic_folder_and_declares_the_playlist_it_left`
  - `tests/test_routing_parity.py::test_the_promoted_buckets_take_exactly_what_the_old_code_filed_in_the_playlists_they_left`

Old text:

```
sub = "jazz"
display = "Jazz"

```

New text:

```
sub = "jazz"
display = "Jazz Archive"

```

### `u133-b.T7_former_gone`

Jazz declares no former place, so its tracks are filed into a band while they still sit in the old playlist

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b.json`, row `T7_former_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`, `tests/test_taxonomy.py`
- Collected: 1014 against a baseline of 1038
- Kills: 5 (collect-error)
- Note: collection changed: 1014 collected against a baseline of 1038. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_routing_parity.py::test_routing_resolves_every_source_string_identically[Jazz]`
  - `tests/test_routing_parity.py::test_routing_resolves_every_source_string_identically[jazz]`
  - `tests/test_routing_parity.py::test_the_one_keyword_rule_the_author_moved_takes_only_what_the_old_code_filed_by_it`
  - `tests/test_routing_parity.py::test_the_source_routed_bucket_matches_for_every_source_string`
  - `tests/test_taxonomy.py::test_the_shipped_template_declares_three_former_places_and_they_load`
- Collection errors: `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_jazz_folder.py`

Old text:

```
[[bucket.formerly]]
id = "non_electronic_jazz"
bucket = "non_electronic"
sub = "jazz"
display = "Jazz"

```

New text:

```
(empty)
```

### `u133-b.T9_energy_off`

Jazz has no energy split

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b.json`, row `T9_energy_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`, `tests/test_taxonomy.py`
- Collected: 1038 against a baseline of 1038
- Kills: 13 (killed)
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_a_jazz_track_in_the_old_playlist_moves_into_its_band_and_leaves_it[2-low]`
  - `tests/test_adopt_jazz_folder.py::test_a_jazz_track_in_the_old_playlist_moves_into_its_band_and_leaves_it[5-med]`
  - `tests/test_adopt_jazz_folder.py::test_a_jazz_track_in_the_old_playlist_moves_into_its_band_and_leaves_it[9-high]`
  - `tests/test_adopt_jazz_folder.py::test_a_jazz_track_in_the_old_playlist_moves_into_its_band_and_leaves_it[None-unsorted]`
  - `tests/test_adopt_jazz_folder.py::test_a_partial_jazz_match_already_in_rock_is_filed_in_jazz_and_stays_in_rock`
  - `tests/test_adopt_jazz_folder.py::test_adoption_withholds_a_jazz_track_still_in_the_old_playlist`
  - `tests/test_adopt_jazz_folder.py::test_an_approved_move_files_jazz_in_its_bands_and_keeps_every_other_membership`
  - `tests/test_adopt_jazz_folder.py::test_jazz_is_shaped_as_hip_hop_is`
  - `tests/test_adopt_jazz_folder.py::test_the_gate_shows_every_jazz_track_moving_and_no_other_track`
  - `tests/test_adopt_jazz_folder.py::test_the_old_jazz_playlist_competes_in_both_buckets_and_is_never_a_destination`
  - `tests/test_routing_parity.py::test_every_bucket_and_level_lands_in_the_same_sub`
  - `tests/test_routing_parity.py::test_the_reserved_and_derived_subs_are_never_returned_by_routing[derived]`
  - `tests/test_routing_parity.py::test_the_reserved_and_derived_subs_are_never_returned_by_routing[reserved]`

Old text:

```
  "jazz",
]
rates = false

```

New text:

```
  "jazz",
]
rates = false
energy = { enabled = false }

```

### `u88-b.X6_template_bound`

the shipped template: a bound of twenty two minutes instead of twenty

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u88-b.json`, row `X6_template_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_routing_workers.py`
- Collected: 341 against a baseline of 341
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_track_of_exactly_the_bound_is_not_a_member`
  - `tests/test_routing_workers.py::test_the_long_track_values_the_tests_expect_are_the_shipped_declaration`
  - `tests/test_taxonomy.py::test_the_long_track_bound_and_the_inspiration_folder_ship_as_the_source_system_had_them`

Old text:

```
over_seconds = 1200
```

New text:

```
over_seconds = 1320
```

### `sitting3.G8_queue_skips_readiness`

File the job whatever is missing, so a restamp scores nothing and reports ok

- File: `src/cratekit/vocals/cli.py`
- Source: `sitting3.json`, row `G8_queue_skips_readiness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 36 against a baseline of 36
- Kills: 2 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_missing_checkpoint_is_refused_at_the_queue_and_named`
  - `tests/test_vocals_cli.py::test_a_slim_worker_refuses_at_the_queue_rather_than_reporting_done`

Old text:

```
    if scoring.loader_bound():
        return
    missing = scoring.missing_requirement()
    if missing is None:
        return

```

New text:

```
    if scoring.loader_bound():
        return
    missing = scoring.missing_requirement()
    if True:
        return

```

### `u181.C3_unscored_flag_ignored`

analyze vocals: ignore --unscored, so the whole folder is queued

- File: `src/cratekit/vocals/cli.py`
- Source: `u181.json`, row `C3_unscored_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`
- Collected: 107 against a baseline of 107
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_analyze_step_rescores_after_analyze_run_and_before_the_restamp`
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_over_a_folder_whose_headed_files_all_carry_a_score_queues_nothing`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_file_the_run_marked_with_no_score_and_leaves_the_rest`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`

Old text:

```
    unscored = bool(getattr(ctx.args, "unscored", False))
```

New text:

```
    unscored = False
```

### `u25.G6_always_rewrite`

Rewrite vocal tags even when the values did not move

- File: `src/cratekit/vocals/cli.py`
- Source: `u25.json`, row `G6_always_rewrite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_an_unchanged_score_is_not_rewritten`

Old text:

```
    if (previous_level, previous_gender, previous_conf) != (level, gender, conf):
        _write_or_refuse(

```

New text:

```
    if True or (previous_level, previous_gender, previous_conf) != (level, gender, conf):
        _write_or_refuse(

```

### `u331.S12_vocal_module_imported_before_the_bound_loader`

vocals/cli._bind_defaults: import the default loader's module before asking whether one is bound, so a machine where it cannot load cannot score through a bound one

- File: `src/cratekit/vocals/cli.py`
- Source: `u331.json`, row `S12_vocal_module_imported_before_the_bound_loader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_analysis.py`
- Collected: 54 against a baseline of 54
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_bound_loader_is_asked_for_before_the_models_module_is_imported`

Old text:

```
    if scoring.loader_bound():
        return
    from cratekit.analysis import vocal

```

New text:

```
    from cratekit.analysis import vocal

    if scoring.loader_bound():
        return

```

### `u343.M12_unscored_reads_the_name_alone`

vocals _unscored: select by the head on the name, so a file the run marked with no score is never rescored

- File: `src/cratekit/vocals/cli.py`
- Source: `u343.json`, row `M12_unscored_reads_the_name_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_unscored_queues_a_file_the_run_marked_with_no_score_and_leaves_the_rest`

Old text:

```
        if analysis_cli.already_measured(path, cfg) and tags.read_vox_from_file(path) is None:
```

New text:

```
        if analysis_cli.run.has_head(path.name, template=analysis_cli._template(cfg)) and tags.read_vox_from_file(path) is None:
```

### `r745-a.E10_text_not_cleaned`

clean_text: write a control character as it is held

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E10_text_not_cleaned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 7 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\n]`
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\r]`
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\t]`
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\ufffe]`
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\x00]`
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\x01]`
  - `tests/test_export_collection.py::test_a_character_no_document_may_carry_is_written_as_a_space_and_counted[\x1f]`

Old text:

```
    return _NOT_ATTRIBUTE_TEXT.sub(" ", value)
```

New text:

```
    return value
```

### `r745-a.E11_any_path_encoded`

is_file_path: encode anything that is not already a location, a streamed reference included

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E11_any_path_encoded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_streamed_track_is_not_dressed_as_a_file_on_this_machine`
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`

Old text:

```
    return recorded.startswith("/") and not locations.looks_like_location(recorded)
```

New text:

```
    return bool(recorded) and not locations.looks_like_location(recorded)
```

### `r745-a.E12_three_stars_moved`

STAR_BYTES: spell three stars 150, a nearby value that is not the export byte

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E12_three_stars_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_row_says_what_the_database_row_says`
  - `tests/test_export_collection.py::test_each_star_count_is_spelled_as_the_export_byte`

Old text:

```
    {0: 0, 1: 51, 2: 102, 3: 153, 4: 204, 5: 255}
```

New text:

```
    {0: 0, 1: 51, 2: 102, 3: 150, 4: 204, 5: 255}
```

### `r745-a.E13_siblings_by_identifier`

_children: order siblings by identifier, ignoring the stored sequence

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E13_siblings_by_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_siblings_come_out_in_their_sequence_and_not_in_identifier_order`
  - `tests/test_export_collection.py::test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted`

Old text:

```
        siblings.sort(key=lambda node: (node.seq, _ordinal(node.node_id), node.node_id))
```

New text:

```
        siblings.sort(key=lambda node: (_ordinal(node.node_id), node.node_id))
```

### `r745-a.E1_tombstone_row_written`

read_tracks: write a tombstoned collection row as a live one

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E1_tombstone_row_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 16 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_a_single_file_intake_splices_into_the_file[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_single_file_intake_splices_into_the_file[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_each_star_count_is_spelled_as_the_export_byte`
  - `tests/test_export_collection.py::test_every_declared_count_equals_what_was_written`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_no_tempo_the_database_holds_reaches_the_file[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_no_tempo_the_database_holds_reaches_the_file[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`
  - `tests/test_export_collection.py::test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_export_collection.py::test_the_strict_reader_takes_the_file_and_sees_the_same_library`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if trees.soft_delete_marker(row):
            continue
        track_id = str(row.ID)
```

New text:

```
        track_id = str(row.ID)
```

### `r745-a.E3_tombstone_playlist_written`

read_nodes: write a tombstoned playlist as a live one

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E3_tombstone_playlist_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_every_declared_count_equals_what_was_written`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted`
  - `tests/test_export_collection.py::test_the_strict_reader_takes_the_file_and_sees_the_same_library`

Old text:

```
        if trees.soft_delete_marker(row):
            continue
        node_id = str(row.ID)
```

New text:

```
        node_id = str(row.ID)
```

### `r745-a.E4_dangling_member_written`

_render_node: write every stored member, whether or not the collection holds it

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E4_dangling_member_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_every_declared_count_equals_what_was_written`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted`
  - `tests/test_export_collection.py::test_the_strict_reader_takes_the_file_and_sees_the_same_library`

Old text:

```
        keys = [member for member in node.members if member in live]
```

New text:

```
        keys = list(node.members)
```

### `r745-a.E5_empty_folder_self_closed`

_render_node: self close a folder with no children, as rekordbox does

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E5_empty_folder_self_closed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 34 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_folder_with_nothing_in_it_has_a_body_a_landing_could_insert_into`
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_a_library_recorded_where_it_is_mounted_has_nothing_to_place`
  - `tests/test_export_collection.py::test_a_playlist_prune_reads_the_file_and_takes_off_only_what_left_it[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_playlist_prune_reads_the_file_and_takes_off_only_what_left_it[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_a_queueing_verb_reads_the_file_and_queues_its_tracks[recorded-under-a-base-drive-favourites-sweep]`
  - `tests/test_export_collection.py::test_a_queueing_verb_reads_the_file_and_queues_its_tracks[recorded-under-a-base-drive-playlist-export]`
  - `tests/test_export_collection.py::test_a_queueing_verb_reads_the_file_and_queues_its_tracks[recorded-under-the-root-favourites-sweep]`
  - `tests/test_export_collection.py::test_a_queueing_verb_reads_the_file_and_queues_its_tracks[recorded-under-the-root-playlist-export]`
  - `tests/test_export_collection.py::test_a_rating_on_neither_scale_is_written_unrated_and_said_so`
  - `tests/test_export_collection.py::test_a_row_says_what_the_database_row_says`
  - `tests/test_export_collection.py::test_a_single_file_intake_splices_into_the_file[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_single_file_intake_splices_into_the_file[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_an_ampersand_a_quote_and_an_accent_survive_the_readers`
  - ... and 19 more, see the JSON sidecar

Old text:

```
    return rbxml.folder_open(name, len(body), indent) + "".join(body) + rbxml.node_close(indent)
```

New text:

```
    if not body:
        return rbxml.folder_open(name, 0, indent).replace(">\\r\\n", "/>\\r\\n")
    return rbxml.folder_open(name, len(body), indent) + "".join(body) + rbxml.node_close(indent)
```

### `r745-a.E6_tempo_constant_moved`

track_element: write a real tempo in place of the gridless constant

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E6_tempo_constant_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 141 against a baseline of 141
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_no_tempo_the_database_holds_reaches_the_file[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_no_tempo_the_database_holds_reaches_the_file[recorded-under-the-root]`

Old text:

```
AverageBpm="0.00"
```

New text:

```
AverageBpm="98.76"
```

### `r745-a.E7_identifier_not_held_to_digits`

refuse_unusable_id: accept any identifier

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E7_identifier_not_held_to_digits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_an_identifier_that_is_not_digits_is_refused_and_nothing_is_written`
  - `tests/test_export_collection.py::test_an_identifier_the_readers_would_lose_is_refused_by_the_emitter[handed-straight-to-the-emitter-not-digits]`

Old text:

```
    if identifier.isascii() and identifier.isdigit():
        return
```

New text:

```
    if True:
        return
```

### `r745-a.E8_duplicate_identifier_written`

render: write one identifier twice

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E8_duplicate_identifier_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_an_identifier_the_readers_would_lose_is_refused_by_the_emitter[held-twice]`

Old text:

```
        if track.track_id in seen:
```

New text:

```
        if False:
```

### `r745-a.E9_smart_playlist_written`

_writable: write a smart playlist, as a node of a kind no reader classifies as a playlist

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-a.json`, row `E9_smart_playlist_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_every_declared_count_equals_what_was_written`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted`

Old text:

```
    return [node for node in nodes if node.attribute in (PLAYLIST_ATTRIBUTE, FOLDER_ATTRIBUTE)]
```

New text:

```
    return [
        node
        for node in nodes
        if node.attribute in (PLAYLIST_ATTRIBUTE, FOLDER_ATTRIBUTE, SMART_ATTRIBUTE)
    ]
```

### `r745-b.E14_members_as_they_arrive`

read_nodes: keep members in the order the rows arrive, not the stored order

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-b.json`, row `E14_members_as_they_arrive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_members_come_out_in_their_stored_order_whatever_order_the_rows_arrive_in`

Old text:

```
sorted(members.get(node_id, ()))
```

New text:

```
members.get(node_id, ())
```

### `r745-b.E15_unreadable_kind_is_a_playlist`

_attribute: answer the playlist code for a kind that cannot be parsed

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-b.json`, row `E15_unreadable_kind_is_a_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_kind_that_cannot_be_read_is_never_written_as_a_playlist[2.5j]`
  - `tests/test_export_collection.py::test_a_kind_that_cannot_be_read_is_never_written_as_a_playlist[]`
  - `tests/test_export_collection.py::test_a_kind_that_cannot_be_read_is_never_written_as_a_playlist[folder]`

Old text:

```
    try:
        return int(value)
    except (TypeError, ValueError):
        return UNREADABLE_ATTRIBUTE
```

New text:

```
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
```

### `r745-b.E16_lookups_not_primed`

read_tracks: read no lookup table ahead of the rows

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-b.json`, row `E16_lookups_not_primed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_lookup_tables_are_read_once_each_and_not_once_per_row`

Old text:

```
    held = _prime_lookups(db)
```

New text:

```
    held = []
```

### `r745-b.E17_provenance_read_anywhere`

provenance_of: read the line anywhere in the file, not only ahead of the document element

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-b.json`, row `E17_provenance_read_anywhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_comment_inside_the_document_does_not_answer_for_the_file`

Old text:

```
    head = content[: max(0, content.find(b"<DJ_PLAYLISTS"))]
```

New text:

```
    head = content
```

### `r745-c.E2_tombstone_membership_written`

read_nodes: keep a tombstoned membership row. Measured again after the test its zero bought

- File: `src/cratekit/write/collection_export.py`
- Source: `r745-c.json`, row `E2_tombstone_membership_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_membership_somebody_removed_is_not_written_back_into_the_playlist`
  - `tests/test_export_collection.py::test_a_membership_that_cannot_say_whether_it_was_removed_refuses`

Old text:

```
        if trees.soft_delete_marker(song):
            continue
```

New text:

```
        if False:
            continue
```

### `r773-a.M10_unmapped_rows_not_collected`

render: collect no row under no rule, the prefix still counted

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M10_unmapped_rows_not_collected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
            unmapped.append(track.track_id)
```

New text:

```
            pass
```

### `r773-a.M11_prefixes_least_rows_first`

render: order the prefixes with the fewest rows first

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M11_prefixes_least_rows_first`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`

Old text:

```
            unmapped_prefixes=tuple(prefixes.most_common()),
```

New text:

```
            unmapped_prefixes=tuple(reversed(prefixes.most_common())),
```

### `r773-a.M1_read_back_not_asked`

mounted_location: rewrite a row wherever a rule sends it, without asking whether the place reads back as itself

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M1_read_back_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_rule_onto_a_second_volume_is_left_to_the_reader_that_follows_it`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[moved-again]`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[target-not-a-path]`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`

Old text:

```
        if read_back.path == resolved.path:
```

New text:

```
        if True:
```

### `r773-a.M2_unmapped_not_told_apart`

mounted_location: answer a row under no rule as recorded, so nothing counts it

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M2_unmapped_not_told_apart`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
        return Mounted(recorded, Mounting.UNDER_NO_RULE, prefix=resolved.prefix)
```

New text:

```
        return Mounted(recorded, Mounting.AS_RECORDED)
```

### `r773-a.M3_placed_row_written_as_recorded`

mounted_location: count a placed row and hand back the recorded spelling, which is the finding itself

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M3_placed_row_written_as_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[onto-itself]`
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_rules_are_walked_in_the_order_they_were_recorded`

Old text:

```
            return Mounted(resolved.path, Mounting.PLACED)
```

New text:

```
            return Mounted(recorded, Mounting.PLACED)
```

### `r773-a.M4_emitter_handed_the_rows_as_read`

render: emit the rows as read and not the rows as placed

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M4_emitter_handed_the_rows_as_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[onto-itself]`
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_rules_are_walked_in_the_order_they_were_recorded`

Old text:

```
        + "".join(track_element(track) for track in placed)
```

New text:

```
        + "".join(track_element(track) for track in tracks)
```

### `r773-a.M5_another_host_not_caught`

mounted_location: catch a different error, so a location naming another host ends the export

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M5_another_host_not_caught`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`

Old text:

```
    except locations.LocationDecodeError:
        return Mounted(recorded, Mounting.AS_RECORDED)
```

New text:

```
    except KeyError:
        return Mounted(recorded, Mounting.AS_RECORDED)
```

### `r773-a.M6_left_row_counted_as_under_no_rule`

mounted_location: answer a row left to its rule as under no rule, which is where doctor and the export disagreed

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M6_left_row_counted_as_under_no_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_rule_onto_a_second_volume_is_left_to_the_reader_that_follows_it`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[moved-again]`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[target-not-a-path]`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`

Old text:

```
        return Mounted(recorded, Mounting.LEFT_TO_ITS_RULE)
```

New text:

```
        return Mounted(recorded, Mounting.UNDER_NO_RULE)
```

### `r773-a.M7_prefixes_not_carried`

render: carry no leading prefix for the rows under no rule

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M7_prefixes_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
            unmapped_prefixes=tuple(prefixes.most_common()),
```

New text:

```
            unmapped_prefixes=(),
```

### `r773-a.M8_placed_rows_not_counted`

render: count no placed row

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M8_placed_rows_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[onto-itself]`
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_rules_are_walked_in_the_order_they_were_recorded`

Old text:

```
            remapped += 1
```

New text:

```
            remapped += 0
```

### `r773-a.M9_left_rows_not_collected`

render: collect no row left to its rule

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `M9_left_rows_not_collected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_rule_onto_a_second_volume_is_left_to_the_reader_that_follows_it`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[moved-again]`
  - `tests/test_export_collection.py::test_a_rule_places_a_row_only_where_it_reads_back_as_itself[target-not-a-path]`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`

Old text:

```
            left.append(track.track_id)
```

New text:

```
            pass
```

### `r773-a.S1_streamed_row_encoded_as_a_file`

is_file_path, existing: take any value that is not a location as a path, a streamed track and an empty one included

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `S1_streamed_row_encoded_as_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_streamed_track_is_not_dressed_as_a_file_on_this_machine`
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
    return recorded.startswith("/") and not locations.looks_like_location(recorded)
```

New text:

```
    return not locations.looks_like_location(recorded)
```

### `r773-a.S2_tombstoned_row_written`

read_tracks, existing: write a tombstoned collection row

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `S2_tombstoned_row_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 16 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_a_single_file_intake_splices_into_the_file[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_single_file_intake_splices_into_the_file[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_each_star_count_is_spelled_as_the_export_byte`
  - `tests/test_export_collection.py::test_every_declared_count_equals_what_was_written`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_no_tempo_the_database_holds_reaches_the_file[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_no_tempo_the_database_holds_reaches_the_file[recorded-under-the-root]`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`
  - `tests/test_export_collection.py::test_the_export_nests_as_the_database_nests_and_omits_what_was_deleted`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_export_collection.py::test_the_strict_reader_takes_the_file_and_sees_the_same_library`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if trees.soft_delete_marker(row):
            continue
        track_id = str(row.ID)
```

New text:

```
        if False:
            continue
        track_id = str(row.ID)
```

### `r773-a.S3_not_a_file_count_inverted`

render, existing: count the rows that do name a file as the ones that do not

- File: `src/cratekit/write/collection_export.py`
- Source: `r773-a.json`, row `S3_not_a_file_count_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_streamed_track_is_not_dressed_as_a_file_on_this_machine`
  - `tests/test_export_collection.py::test_each_recorded_spelling_is_placed_or_left_by_the_one_resolver`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
    unlocated = tuple(track.track_id for track in tracks if not is_located(track.location))
```

New text:

```
    unlocated = tuple(track.track_id for track in tracks if is_located(track.location))
```

### `r1949.E1_missing_never`

check: never report a declared track the playlist lacks, so a short tree reads matching

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `E1_missing_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 25 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`
  - `tests/test_rebuild.py::test_a_tree_stripped_of_its_membership_rebuilds_to_match_the_control`
  - `tests/test_rebuild.py::test_the_check_reports_a_difference_in_both_directions`
  - `tests/test_rebuild.py::test_the_check_walks_down_from_the_adopted_root_and_ignores_a_namesake`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[the library moved]`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[two files swapped]`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`
  - `tests/test_resort_scope.py::test_the_gate_shows_every_add_and_only_the_routing_trees`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_refuses_the_resume_before_any_item_runs[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[resort]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
        if content_id not in held:
```

New text:

```
        if False:
```

### `r1949.N10_no_classes`

declared_names: leave every sub class out, so a cleared track left in with vox alone reads matching

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N10_no_classes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_vocal_playlist_the_run_did_not_compare_is_not_named_through_its_names`

Old text:

```
        subs = set(competing) | {genre.id for genre in bucket.genre_subs} | classes
```

New text:

```
        subs = set(competing) | {genre.id for genre in bucket.genre_subs}
```

### `r1949.N11_no_bands`

declared_names: leave the competing places out, so the band the residual names is never compared

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N11_no_bands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 9 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_cleared_second_genre_alone_in_its_folder_is_named_by_the_check`
  - `tests/test_second_genre.py::test_a_cleared_second_genre_leaves_its_genre_sub_named_as_well`
  - `tests/test_second_genre.py::test_a_cleared_second_genre_under_a_folder_renamed_in_rekordbox_is_named`
  - `tests/test_second_genre.py::test_a_playlist_rekordbox_removed_is_not_compared_through_its_names`
  - `tests/test_second_genre.py::test_a_record_naming_a_bucket_the_taxonomy_dropped_is_reported_not_raised`
  - `tests/test_second_genre.py::test_a_recorded_folder_renamed_to_another_genres_name_is_read_by_that_name`
  - `tests/test_second_genre.py::test_a_soul_tracks_cleared_rnb_alone_in_the_rnb_band_is_named_too`
  - `tests/test_second_genre.py::test_a_vocal_playlist_the_run_did_not_compare_is_not_named_through_its_names`
  - `tests/test_second_genre.py::test_the_converge_verb_says_differing_over_a_cleared_second_genre`

Old text:

```
        subs = set(competing) | {genre.id for genre in bucket.genre_subs} | classes
```

New text:

```
        subs = {genre.id for genre in bucket.genre_subs} | classes
```

### `r1949.N12_undeclared_pair_raises`

declared_names: let a former or split place's KeyError escape, so every check refuses

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N12_undeclared_pair_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 110 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_check_with_no_source_leaves_the_recorded_favorites_out_and_names_the_gap`
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`
  - `tests/test_genre_favorites.py::test_the_rebuild_files_a_favourite_into_the_folder_it_moves_it_to`
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`
  - `tests/test_rebuild.py::test_a_declared_file_the_library_has_no_row_for_is_surfaced_and_is_not_a_difference`
  - `tests/test_rebuild.py::test_a_destination_that_lost_every_track_is_still_compared`
  - `tests/test_rebuild.py::test_a_destination_with_no_recorded_node_falls_back_to_the_declared_name`
  - `tests/test_rebuild.py::test_a_genre_sub_is_created_once_beside_the_band_and_a_second_rebuild_plans_nothing`
  - `tests/test_rebuild.py::test_a_governed_write_records_the_fingerprint_at_its_close`
  - `tests/test_rebuild.py::test_a_library_with_no_vocal_calibration_reports_what_it_did_not_compare`
  - `tests/test_rebuild.py::test_a_membership_pointing_at_a_soft_deleted_row_is_not_a_difference_either`
  - `tests/test_rebuild.py::test_a_playlist_nobody_declared_is_reported_and_is_not_a_difference`
  - `tests/test_rebuild.py::test_a_rebuild_after_a_rename_converges_rather_than_doubling_the_tree`
  - `tests/test_rebuild.py::test_a_rebuild_and_its_check_beside_deadca7s_folder_leave_it_and_report_no_drift[ordinary]`
  - `tests/test_rebuild.py::test_a_rebuild_and_its_check_beside_deadca7s_folder_leave_it_and_report_no_drift[zero-date-west-of-utc]`
  - ... and 95 more, see the JSON sidecar

Old text:

```
            except KeyError:
                continue
            found.setdefault
```

New text:

```
            except ValueError:
                continue
            found.setdefault
```

### `r1949.N14_namesake_names_swapped`

namesakes: name the destination by its playlist and folder swapped, so a leftover names a folder nobody has

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N14_namesake_names_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_cleared_second_genre_alone_in_its_folder_is_named_by_the_check`

Old text:

```
        out.append(Destination(*place, node.folder_display, node.playlist_display, node))
```

New text:

```
        out.append(Destination(*place, node.playlist_display, node.folder_display, node))
```

### `r1949.N15_vocal_half_dropped`

_uncompared_subs: drop the vocal half, so with vox reads left behind and differing on an uncalibrated run

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N15_vocal_half_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 2 (killed)
- Killed:
  - `tests/test_rebuild.py::test_a_vocal_playlist_nothing_compared_is_not_named_as_left_behind`
  - `tests/test_second_genre.py::test_a_vocal_playlist_the_run_did_not_compare_is_not_named_through_its_names`

Old text:

```
    if VOCAL_DIMENSION in tuple(not_compared):
        skipped |=
```

New text:

```
    if False:
        skipped |=
```

### `r1949.N16_favorites_half_dropped`

_uncompared_subs: drop the favourites half, so a Favorites playlist is compared when its source was not read

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N16_favorites_half_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_favorites_playlist_the_run_did_not_compare_stays_foreign`

Old text:

```
    skipped = _uncompared_playlist_subs(declared, not_compared)
    if VOCAL
```

New text:

```
    skipped = set()
    if VOCAL
```

### `r1949.N1_no_namesakes`

check: compare only resolved destinations again, so a playlist nothing derives into is foreign and converge says matching over a cleared second genre (the residual itself)

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N1_no_namesakes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 9 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_cleared_second_genre_alone_in_its_folder_is_named_by_the_check`
  - `tests/test_second_genre.py::test_a_cleared_second_genre_leaves_its_genre_sub_named_as_well`
  - `tests/test_second_genre.py::test_a_cleared_second_genre_under_a_folder_renamed_in_rekordbox_is_named`
  - `tests/test_second_genre.py::test_a_playlist_rekordbox_removed_is_not_compared_through_its_names`
  - `tests/test_second_genre.py::test_a_record_naming_a_bucket_the_taxonomy_dropped_is_reported_not_raised`
  - `tests/test_second_genre.py::test_a_recorded_folder_renamed_to_another_genres_name_is_read_by_that_name`
  - `tests/test_second_genre.py::test_a_soul_tracks_cleared_rnb_alone_in_the_rnb_band_is_named_too`
  - `tests/test_second_genre.py::test_a_vocal_playlist_the_run_did_not_compare_is_not_named_through_its_names`
  - `tests/test_second_genre.py::test_the_converge_verb_says_differing_over_a_cleared_second_genre`

Old text:

```
            *namesakes(declared, nodes, destinations, not_compared, record),

```

New text:

```
(empty)
```

### `r1949.N2_removed_compared`

namesakes: compare a playlist rekordbox removed through its names, so a removed playlist reads differing

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N2_removed_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_playlist_rekordbox_removed_is_not_compared_through_its_names`

Old text:

```
        if node.removed or (node.folder_id, node.playlist_id) in resolved:
```

New text:

```
        if (node.folder_id, node.playlist_id) in resolved:
```

### `r1949.N3_resolved_compared_again`

namesakes: compare a node a record already resolved again under the names it now bears, so a renamed recorded playlist overwrites its own destination

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N3_resolved_compared_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 2 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_recorded_folder_renamed_to_another_genres_name_is_read_by_that_name`
  - `tests/test_second_genre.py::test_a_recorded_playlist_renamed_to_another_bands_names_keeps_its_own_destination`

Old text:

```
        if node.removed or (node.folder_id, node.playlist_id) in resolved:
```

New text:

```
        if node.removed:
```

### `r1949.N4_covered_compared`

namesakes: compare a second node bearing a destination's names that this run derived or a record names, so a namesake beside a renamed folder reads unexpected

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N4_covered_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_namesake_of_a_destination_already_resolved_elsewhere_is_left_as_it_was`

Old text:

```
        if place is None or place in covered or place[1] in skipped:
```

New text:

```
        if place is None or place[1] in skipped:
```

### `r1949.N5_uncompared_dimension_compared`

namesakes: compare a playlist whose dimension this run did not compare, so a with vox playlist on an uncalibrated run reads differing

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N5_uncompared_dimension_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 2 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_favorites_playlist_the_run_did_not_compare_stays_foreign`
  - `tests/test_second_genre.py::test_a_vocal_playlist_the_run_did_not_compare_is_not_named_through_its_names`

Old text:

```
        if place is None or place in covered or place[1] in skipped:
```

New text:

```
        if place is None or place in covered:
```

### `r1949.N6_folder_by_display_only`

namesakes: read a recorded folder by its display name, so a cleared second genre under a folder renamed in rekordbox reads matching

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N6_folder_by_display_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_cleared_second_genre_under_a_folder_renamed_in_rekordbox_is_named`

Old text:

```
            folder = recorded_folder.get(node.folder_id, folder)
```

New text:

```
            folder = folder
```

### `r1949.N8_manual_class_compared`

declared_names: keep the manual classes, so a hand kept Candy playlist reads differing (round one's blocker)

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N8_manual_class_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_hand_filled_candy_playlist_alone_in_its_folder_stays_a_persons_own`

Old text:

```
        if entry.policy is not taxonomy.SubPolicy.MANUAL
```

New text:

```
        if True
```

### `r1949.N9_no_genre_subs`

declared_names: leave the genre subs out, so a cleared second genre's genre sub playlist reads matching

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N9_no_genre_subs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_routing_workers.py`, `tests/test_resort_scope.py`, `tests/test_rebuild_growth.py`, `tests/test_rebuild_one_open.py`
- Collected: 535 against a baseline of 535
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_cleared_second_genre_leaves_its_genre_sub_named_as_well`

Old text:

```
        subs = set(competing) | {genre.id for genre in bucket.genre_subs} | classes
```

New text:

```
        subs = set(competing) | classes
```

