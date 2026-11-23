# Mutation table: u306-replay-after-d

Measured by `scripts/mutate.py` on 2026-11-23 00:42 UTC, branch `HEAD` at `451c6354`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22940 collected. pytest invocations for this batch: 225.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `c919209162e4`, and this tree is at `451c63542812`).

Subset baselines: 22, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/known.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22940 against 22940. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u167.M23_waiting_exit` | `src/cratekit/analysis/check_cli.py` | user | 1 file(s) | 70 | 7 | killed |
| `u167.M24_suspect_exit` | `src/cratekit/analysis/check_cli.py` | user | 1 file(s) | 70 | 5 | killed |
| `u167.M10_wheel_wrap` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 2 | killed |
| `u167.M11_sigmas` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u167.M12_floor_rate` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 21 | killed |
| `u167.M13_suspect_state_guard` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u167.M14_dyn_excuses` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 2 | killed |
| `u167.M15_unread_suspect` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 5 | killed |
| `u167.M16_suspect_outranks` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 3 | killed |
| `u167.M17_gone_counts_as_nothing` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 2 | killed |
| `u167.M19_landing_without_rows` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u167.M1_file_kind` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u167.M21_name_wins` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 7 | killed |
| `u167.M3_tag_fits` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 2 | killed |
| `u167.M4_grid_parse_failure` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u167.M5_short_header` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u167.M6_constant_test` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 5 | killed |
| `u167.M7_missing_folded` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 2 | killed |
| `u167.M8_empty_grid` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u167.M9_relative_key` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u259.M10_chunk_size` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 2 | killed |
| `u259.M11_scope_carries_no_rows` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u259.M13_batch_failure_not_met_again` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u259.M14_batch_failure_reads_nothing` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u259.M15_id_not_text_judged` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u259.M16_id_skip_widened` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u259.M6_unanalysed_reads_by_id` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u259.M7_unanalysed_keeps_no_row` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 6 | killed |
| `u259.M8_check_rows_rereads_scope` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 1 | killed |
| `u259.M9_read_row_per_row` | `src/cratekit/analysis/rekordbox_check.py` | user | 1 file(s) | 70 | 3 | killed |
| `u93-recursive-analysis.D21_restamp_flag` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 18 | killed |
| `u93-recursive-analysis.D22_restamp_resume_warning` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 206 | 2 | killed |
| `u93-recursive-analysis.D24_restamp_join` | `src/cratekit/analysis/cli.py` | maintainer | 2 file(s) | 206 | 1 | killed |
| `u94-a.S1_floor_dropped` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 3 | killed |
| `u94-a.S2_floor_off_by_one` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 2 | killed |
| `u94-a.S3_partial_refusal_dropped` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 6 | killed |
| `u94-a.S4_accept_flag_dead` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 11 | killed |
| `u94-a.S5_recursive_not_required` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 2 | killed |
| `u94-a.S6_music_folder_not_wide` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-a.S7_samefile_to_spelling` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-a.S8_after_walk_never_asked` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-b.W1_after_walk_refusal_dropped` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-b.W3_accepted_reads_ok` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 2 | killed |
| `u94-b.W4_partial_warning_dropped` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 2 | killed |
| `u94-b.W5_warning_without_a_write` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-b.W7_omissions_dropped_from_the_fit` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-b.W8_note_forgets_the_omission` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-c.N1_stride_is_the_first_n` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 2 | killed |
| `u94-c.N2_stride_is_a_fixed_step` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-c.N3_sample_ignored` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 3 | killed |
| `u94-c.N4_vocal_half_sampled` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-c.N5_note_m_is_the_sample` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-c.N6_default_sample_halved` | `src/cratekit/analysis/cli.py` | maintainer | 2 file(s) | 206 | 1 | killed |
| `u94-c.N7_root_not_required_first` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 1 | killed |
| `u94-c.N8_absent_folder_not_told_apart` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 2 | killed |
| `r1631.M25_bandcamp_any_head` | `src/cratekit/tagging/shops.py` | user | 6 file(s) | 1241 | 1 | killed |
| `u280-pinned.M06_marker_read_anywhere` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 1 | killed |
| `u280-pinned.M11_ambiguity_featured_credits` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 1 | killed |
| `u280-pinned.M29_marker_number_from_all_words` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 1 | killed |
| `u280.M01_ambiguous_read_as_titled` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 32 | killed |
| `u280.M03_bare_names_dropped` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 3 | killed |
| `u280.M04_bare_meets_bare` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 6 | killed |
| `u280.M05_marker_not_read_past` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 2 | killed |
| `u280.M07_version_alone_after_title` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 2 | killed |
| `u280.M09_ambiguity_ignores_feature` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 7 | killed |
| `u280.M10_ambiguity_one_credit_only` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 12 | killed |
| `u280.M12_ambiguity_version_alone` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 5 | killed |
| `u280.M13_ambiguity_track_numbered` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 3 | killed |
| `u280.M15_splits_without_feature_cut` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 1 | killed |
| `u280.M17_featured_part_never` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 6 | killed |
| `u280.M18_featured_part_own_credit` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 16 | killed |
| `u280.M19_tempo_never_title` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 2 | killed |
| `u280.M22_whole_name_shed` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 13 | killed |
| `u280.M24_track_number_past_marker` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 2 | killed |
| `u280.M26_brackets_shed_across_a_dash` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 6 | killed |
| `u280.M27_leading_groups_across_a_dash` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 2 | killed |
| `u280.M28_any_number_read_past` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 3 | killed |
| `u280.M30_featured_after_a_head` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 1 | killed |
| `u280.M31_bracketed_later_title_unread` | `src/cratekit/tagging/titles.py` | user | 6 file(s) | 1241 | 1 | killed |
| `u289.C1_record_drops_asked` | `src/cratekit/tagging/cli.py` | user | 8 file(s) | 1437 | 1 | killed |
| `u289.S1_question_unused` | `src/cratekit/tagging/searchers.py` | user | 8 file(s) | 1437 | 28 | killed |
| `u289.S2_asked_not_carried` | `src/cratekit/tagging/searchers.py` | user | 8 file(s) | 1437 | 127 | killed |
| `u289.S4_discogs_asked_head` | `src/cratekit/tagging/discogs.py` | user | 8 file(s) | 1437 | 27 | killed |
| `u289.S5_shop_asked_head` | `src/cratekit/tagging/searchers.py` | user | 8 file(s) | 1437 | 4 | killed |
| `u289.S6_picture_asked_head` | `src/cratekit/tagging/searchers.py` | user | 8 file(s) | 1437 | 2 | killed |
| `u289.T1_title_tag_split` | `src/cratekit/tagging/tag.py` | user | 8 file(s) | 1437 | 1 | killed |
| `u289.T2_split_artist_dropped` | `src/cratekit/tagging/tag.py` | user | 8 file(s) | 1437 | 4 | killed |
| `u289.T3_record_read_from_title` | `src/cratekit/tagging/tag.py` | user | 8 file(s) | 1437 | 3 | killed |
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
| `u282.D1_discogs_decline_ends_the_walk` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 9 | killed |
| `u282.D2_shop_decline_gives_way` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 3 | killed |
| `u282.D3_second_decline_named` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 1 | killed |
| `u282.D5_held_decline_dropped` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 6 | killed |
| `u282.L1_decline_lends_no_picture` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 1 | killed |
| `u282.L2_nobody_named_is_the_source` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 4 | killed |
| `u282.L3_shop_row_not_recorded` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 1 | killed |
| `u282.P1_no_picture_question` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 8 | killed |
| `u282.P3_answer_not_folded` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 5 | killed |
| `u282.P4_refusal_not_unread` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 3 | killed |
| `u282.P5_match_names_no_picture` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 4 | killed |
| `u282.P6_waiting_note_dropped` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 1 | killed |
| `u282.R1_rejection_raised_at_once` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 5 | killed |
| `u282.R2_any_refusal_held` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 1 | killed |
| `u282.R4_rejection_reads_as_no_token` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 3 | killed |
| `u282.W1_walk_beatport_first` | `src/cratekit/tagging/catalogues.py` | user | 9 file(s) | 1470 | 43 | killed |
| `u282.W2_sources_beatport_first` | `src/cratekit/tagging/catalogues.py` | user | 9 file(s) | 1470 | 2 | killed |
| `u282.T1_question_asked_with_a_picture` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1470 | 2 | killed |
| `u282.T2_question_never_asked` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1470 | 5 | killed |
| `u282.T3_failed_question_raises` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1470 | 1 | killed |
| `u282.T4_failed_question_result_dropped` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1470 | 1 | killed |
| `r1724.N13_retag_raw_stem` | `src/cratekit/tagging/retag.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1724.N14_retag_tag_read` | `src/cratekit/tagging/retag.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1724.N11_tag_one_raw_stem` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1679 | 5 | killed |
| `r1724.N12_tag_one_tag_read` | `src/cratekit/tagging/tag.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1724.N10_by_name_unsplit_stem` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 2 | killed |
| `r1724.N1_tail_any_case` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1724.N2_no_trailing_space_read` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1724.N3_space_before_tail_kept` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1724.N4_tail_alone_guard` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 9 | killed |
| `r1724.N5_tail_alone_empty` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 9 | killed |
| `r1724.N6_tail_never_dropped` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 81 | killed |
| `r1724.N7_tail_word` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 82 | killed |
| `r1724.N8_by_name_raw_stem` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 6 | killed |
| `r1724.N9_by_name_headless_stem` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 1 | killed |
| `r1724.S1_u289_head_needs_a_key` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 3 | killed |
| `r1724.S2_u289_version_part` | `src/cratekit/tagging/titles.py` | user | 9 file(s) | 1679 | 1 | killed |
| `u178.S1_summary_counts_labels` | `src/cratekit/tagging/summary.py` | user | 3 file(s) | 236 | 5 | killed |
| `u178.S2_unknown_label_refused` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.S3_unreadable_registry_refuses_label` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.S4_genres_frozen` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 13 | killed |
| `u178.S5_worker_takes_label` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 7 | killed |
| `u178.S6_outranked_needs_label` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 4 | killed |
| `u178-e9.E9_label_tag_reset` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.E2_no_search_with_picture` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 11 | killed |
| `u178.E3_art_refusal_tolerated` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.E4_isrc_withheld` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.E6_label_write_checked` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.E7_catalogue_write_checked` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u244.M04_refusal_remembered` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 1 | killed |
| `u244.M05_401_is_rejection` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 3 | killed |
| `u244.M06_gone_release_passed_over` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 1 | killed |
| `u244.M07_remaining_floor` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 1 | killed |
| `u244.M08_notes_scrubbed` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 1 | killed |
| `u244.M09_results_not_a_list` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 2 | killed |
| `u244.M10_unread_outranks_styleless` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 1 | killed |
| `u244.M11_block_ends_release_walk` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 1 | killed |
| `u244.M13_styleless_gives_way` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 2 | killed |
| `u244.M18_article_first` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 2 | killed |
| `r791-a.S10_track_unread_returned` | `src/cratekit/tagging/shops.py` | user | 3 file(s) | 239 | 2 | killed |
| `r791-a.S14_blocked_step` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 239 | 1 | killed |
| `r791-a.S1_403_blocks` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 239 | 11 | killed |
| `r791-a.S2_429_blocks` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 239 | 3 | killed |
| `r791-a.S3_client_challenge_title` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 239 | 8 | killed |
| `r791-a.S4_ellipsis_character` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 239 | 1 | killed |
| `r791-a.S5_challenge_body` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 239 | 1 | killed |
| `r791-a.S8_blocked_track_page_stops` | `src/cratekit/tagging/shops.py` | maintainer | 3 file(s) | 239 | 1 | killed |
| `r791-a.S9_gone_track_page` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 239 | 1 | killed |
| `u275.M1_base_back_to_linux` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 549 | 6 | killed |
| `u275.M2_slope_back_to_linux` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 549 | 19 | killed |
| `u275.M3_slope_rounded_down` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 549 | 6 | killed |
| `u275.M4_base_rounded_down` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 549 | 5 | killed |
| `u275.M5_decode_line_dropped` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 549 | 29 | killed |
| `u275.M6_unknown_length_shorter` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 549 | 3 | killed |
| `u275.M7_cheapest_track_sets_the_cost` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 549 | 13 | killed |
| `u275.M8_analysis_line_scaled` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 549 | 18 | killed |
| `r791-b.C1_artifact_answers` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 239 | 15 | killed |
| `r791-b.C2_artifact_unread` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 239 | 6 | killed |
| `r791-b.C3_summary_counts_answers` | `src/cratekit/tagging/summary.py` | user | 3 file(s) | 239 | 15 | killed |
| `r791-b.C6_not_asked_excluded` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 239 | 1 | killed |
| `r791-b.C7_parse_break_said` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 239 | 1 | killed |
| `r791-b.C8_one_file` | `src/cratekit/tagging/summary.py` | maintainer | 3 file(s) | 239 | 1 | killed |
| `r791-b.C9_unread_skip_zero_filled` | `src/cratekit/tagging/summary.py` | user | 3 file(s) | 239 | 11 | killed |
| `u263.D18_vocal_reason` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 224 | 1 | killed |
| `u192.T1_typed_label_on_queue` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 166 | 1 | killed |
| `u192.T2_queue_warnings_lost` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 166 | 1 | killed |
| `u192.T3_resume_label_unsaid` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 166 | 2 | killed |
| `u276.K13_record_key_method_dropped` | `src/cratekit/analysis/detect.py` | user | 2 file(s) | 89 | 1 | killed |
| `u276.K14_record_read_with_plain` | `src/cratekit/analysis/detect.py` | user | 2 file(s) | 89 | 1 | killed |
| `u40-author-full.C3_resume_without_run` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 70 | 3 | killed |
| `u40-author-full.C4_resume_always_runs` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 70 | 1 | killed |
| `u294.M03_suggest_narrowed_ignores_genre` | `src/cratekit/tagging/suggest.py` | user | 2 file(s) | 115 | 1 | killed |
| `u294.M04_suggest_narrowed_changes_unfiltered` | `src/cratekit/tagging/suggest.py` | user | 2 file(s) | 115 | 1 | killed |
| `u157.A1_no_level_tag` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 212 | 1 | killed |
| `u276.K1_default_is_whole` | `src/cratekit/analysis/detect.py` | user | 4 file(s) | 119 | 3 | killed |
| `u192.T4_tag_queue_only_ignored` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 221 | 7 | killed |
| `r290-author.R1_retag_rebuild_drops_the_type` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 228 | 2 | killed |
| `u181.C3_unscored_flag_ignored` | `src/cratekit/vocals/cli.py` | user | 2 file(s) | 105 | 4 | killed |
| `u94-b.W6_outcome_energy_only` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 206 | 1 | killed |
| `u244.M02_rejection_remembered` | `src/cratekit/tagging/discogs.py` | user | 3 file(s) | 262 | 2 | killed |

## Row definitions

### `u167.M23_waiting_exit`

analyze_check: waiting ends ok with exit 0 rather than pending

- File: `src/cratekit/analysis/check_cli.py`
- Source: `u167.json`, row `M23_waiting_exit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 7 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_landing_s_session_names_its_rows`
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_an_empty_analyze_playlist_falls_to_every_row_not_analysed`
  - `tests/test_analyze_check.py::test_an_intake_tree_not_cut_over_falls_to_every_row_not_analysed_and_says_why`
  - `tests/test_analyze_check.py::test_rows_landed_and_not_yet_analysed_are_waiting_on_a_pending_action`
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[analyze]`
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[unanalysed]`

Old text:

```
    if verdict == rc.WAITING:
```

New text:

```
    if False:
```

### `u167.M24_suspect_exit`

analyze_check: suspect ends ok with exit 0 rather than refusing

- File: `src/cratekit/analysis/check_cli.py`
- Source: `u167.json`, row `M24_suspect_exit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 5 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_removed_dyn_mark_does_not_excuse_a_variable_grid`
  - `tests/test_analyze_check.py::test_a_variable_grid_on_a_row_not_marked_dyn_is_suspect_and_exits_27`
  - `tests/test_analyze_check.py::test_an_analysed_row_whose_file_is_missing_is_suspect`
  - `tests/test_analyze_check.py::test_no_file_under_the_library_is_opened_for_writing`
  - `tests/test_analyze_check.py::test_suspect_outranks_waiting_through_the_verb`

Old text:

```
    if verdict == rc.SUSPECT:
```

New text:

```
    if False:
```

### `u167.M10_wheel_wrap`

key_relation: forget the wheel wraps, so 12 and 1 read far

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M10_wheel_wrap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_title_key_is_equal_one_step_or_far_from_rekordbox_s[12B-1B-one_step]`
  - `tests/test_analyze_check.py::test_the_title_key_is_equal_one_step_or_far_from_rekordbox_s[1A-12A-one_step]`

Old text:

```
    if letter == other_letter and (number - other_number) % 12 in (1, 11):
```

New text:

```
    if letter == other_letter and abs(number - other_number) == 1:
```

### `u167.M11_sigmas`

KEY_AGREEMENT_SIGMAS: two standard errors rather than three

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M11_sigmas`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_key_floor_is_the_recorded_rate_less_three_standard_errors`

Old text:

```
KEY_AGREEMENT_SIGMAS = 3.0
```

New text:

```
KEY_AGREEMENT_SIGMAS = 2.0
```

### `u167.M12_floor_rate`

key_floor: take the rate over differs alone rather than over every compared key

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M12_floor_rate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 21 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[analyze]`
  - `tests/test_analyze_check.py::test_a_landing_s_session_names_its_rows`
  - `tests/test_analyze_check.py::test_a_pass_names_its_landing_s_rows_over_the_playlist`
  - `tests/test_analyze_check.py::test_a_removed_dyn_mark_does_not_excuse_a_variable_grid`
  - `tests/test_analyze_check.py::test_a_row_gone_from_the_collection_is_named_and_does_not_hold_the_visit`
  - `tests/test_analyze_check.py::test_a_row_not_analysed_is_waiting`
  - `tests/test_analyze_check.py::test_a_row_not_analysed_never_reads_suspect_whatever_grid_it_carries`
  - `tests/test_analyze_check.py::test_a_variable_grid_on_a_row_marked_dyn_is_done`
  - `tests/test_analyze_check.py::test_a_variable_grid_on_a_row_not_marked_dyn_is_suspect_and_exits_27`
  - `tests/test_analyze_check.py::test_an_analysed_row_whose_file_is_missing_is_suspect`
  - `tests/test_analyze_check.py::test_every_row_analysed_on_a_constant_grid_is_done`
  - `tests/test_analyze_check.py::test_every_row_analysed_right_is_done_and_exits_zero`
  - `tests/test_analyze_check.py::test_keys_far_below_the_recorded_agreement_are_suspect_and_near_it_are_not`
  - `tests/test_analyze_check.py::test_no_file_under_the_library_is_opened_for_writing`
  - `tests/test_analyze_check.py::test_rows_landed_and_not_yet_analysed_are_waiting_on_a_pending_action`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    total = measured["equal"] + measured["differs"]
```

New text:

```
    total = measured["differs"]
```

### `u167.M13_suspect_state_guard`

suspect_grid: judge the grid of a row that is not analysed

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M13_suspect_state_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_row_not_analysed_never_reads_suspect_whatever_grid_it_carries`

Old text:

```
        if self.state != ANALYSED:
            return False
        if self.grid.state == VARIABLE:
```

New text:

```
        if self.grid.state == VARIABLE:
```

### `u167.M14_dyn_excuses`

suspect_grid: a dyn mark no longer excuses a variable grid

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M14_dyn_excuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_variable_grid_on_a_row_marked_dyn_is_done`
  - `tests/test_analyze_check.py::test_the_same_variable_grid_on_a_row_marked_dyn_is_done`

Old text:

```
            return not self.dyn
```

New text:

```
            return True
```

### `u167.M15_unread_suspect`

suspect_grid: a missing or unreadable grid on an analysed row is not suspect

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M15_unread_suspect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 5 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_variable_or_unread_grid_is_suspect[absent]`
  - `tests/test_analyze_check.py::test_a_variable_or_unread_grid_is_suspect[missing]`
  - `tests/test_analyze_check.py::test_a_variable_or_unread_grid_is_suspect[unreadable]`
  - `tests/test_analyze_check.py::test_an_analysed_row_whose_file_is_missing_is_suspect`
  - `tests/test_analyze_check.py::test_an_unread_grid_on_a_row_marked_dyn_is_still_suspect`

Old text:

```
        return self.grid.state in (ABSENT, MISSING, UNREADABLE)
```

New text:

```
        return False
```

### `u167.M16_suspect_outranks`

verdict: waiting outranks suspect

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M16_suspect_outranks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_suspect_outranks_waiting`
  - `tests/test_analyze_check.py::test_suspect_outranks_waiting_through_the_verb`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_in_inbox_analyze`

Old text:

```
        if any(row.suspect_grid for row in self.rows) or self.key_suspect:
            return SUSPECT
        if self.counted(NOT_ANALYSED):
            return WAITING
```

New text:

```
        if self.counted(NOT_ANALYSED):
            return WAITING
        if any(row.suspect_grid for row in self.rows) or self.key_suspect:
            return SUSPECT
```

### `u167.M17_gone_counts_as_nothing`

verdict: drop the all gone case, so a scope of removed rows reads done

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M17_gone_counts_as_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_named_landing_whose_every_row_left_the_collection_refuses`
  - `tests/test_analyze_check.py::test_no_row_or_only_gone_rows_is_nothing`

Old text:

```
        if not self.rows or self.counted(GONE) == len(self.rows):
```

New text:

```
        if not self.rows:
```

### `u167.M19_landing_without_rows`

resolve_scope: a named landing whose playlists hold no live row reads as an empty scope

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M19_landing_without_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_pass_whose_playlists_hold_no_live_row_refuses_rather_than_reading_empty`

Old text:

```
        if not members:
            raise refuse(
```

New text:

```
        if False:
            raise refuse(
```

### `u167.M1_file_kind`

grid_ticks: accept any first four bytes, so a file that is not an analysis file is walked

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M1_file_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_damaged_file_reads_unreadable_never_absent[not-an-analysis-file]`

Old text:

```
    if kind != _FILE_KIND:
```

New text:

```
    if False:
```

### `u167.M21_name_wins`

resolve_scope: the playlist wins over a named pass when it holds rows

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M21_name_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 7 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_landing_nothing_recorded_refuses_rather_than_reading_empty[--pass]`
  - `tests/test_analyze_check.py::test_a_landing_nothing_recorded_refuses_rather_than_reading_empty[--session]`
  - `tests/test_analyze_check.py::test_a_landing_s_session_names_its_rows`
  - `tests/test_analyze_check.py::test_a_named_landing_whose_every_row_left_the_collection_refuses`
  - `tests/test_analyze_check.py::test_a_pass_names_its_landing_s_rows_over_the_playlist`
  - `tests/test_analyze_check.py::test_a_pass_whose_playlists_hold_no_live_row_refuses_rather_than_reading_empty`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_for_a_named_landing`

Old text:

```
    if pass_name is not None or session_id is not None:
        kind
```

New text:

```
    if (pass_name is not None or session_id is not None) and not _analyze_members(db, declared, registry)[0]:
        kind
```

### `u167.M3_tag_fits`

grid_ticks: drop the tag fits check, so an overrunning or undersized tag is parsed

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M3_tag_fits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_damaged_file_reads_unreadable_never_absent[a-tag-of-length-zero-before-the-grid]`
  - `tests/test_analyze_check.py::test_a_damaged_file_reads_unreadable_never_absent[a-tag-that-overruns]`

Old text:

```
        if tag_length < _HEADER.size or offset + tag_length > len(data):
```

New text:

```
        if False:
```

### `u167.M4_grid_parse_failure`

grid_ticks: read a grid tag that will not parse as a file with no grid

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M4_grid_parse_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_damaged_file_reads_unreadable_never_absent[a-grid-tag-that-will-not-parse]`

Old text:

```
                raise ValueError(f"the grid tag would not parse: {exc}") from exc
```

New text:

```
                return None
```

### `u167.M5_short_header`

grid_ticks: drop the short file refusal, so ten bytes reach the unpack

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M5_short_header`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_damaged_file_reads_unreadable_never_absent[shorter-than-a-header]`

Old text:

```
    if len(data) < _HEADER.size:
```

New text:

```
    if False:
```

### `u167.M6_constant_test`

read_grid: call a grid constant when its ends are within a whole beat per minute

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M6_constant_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 5 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_removed_dyn_mark_does_not_excuse_a_variable_grid`
  - `tests/test_analyze_check.py::test_a_variable_grid_on_a_row_not_marked_dyn_is_suspect_and_exits_27`
  - `tests/test_analyze_check.py::test_a_variable_grid_reads_variable_with_its_span`
  - `tests/test_analyze_check.py::test_no_file_under_the_library_is_opened_for_writing`
  - `tests/test_analyze_check.py::test_suspect_outranks_waiting_through_the_verb`

Old text:

```
        state=CONSTANT if low == high else VARIABLE, beats=len(ticks), low=low, high=high
```

New text:

```
        state=CONSTANT if high - low < 1000 else VARIABLE, beats=len(ticks), low=low, high=high
```

### `u167.M7_missing_folded`

read_grid: read a missing analysis file as a file with no grid

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M7_missing_folded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_missing_file_reads_missing`
  - `tests/test_analyze_check.py::test_an_analysed_row_whose_file_is_missing_is_suspect`

Old text:

```
        return Grid(state=MISSING, why=f"no analysis file at {path}")
```

New text:

```
        return Grid(state=ABSENT, why=f"no analysis file at {path}")
```

### `u167.M8_empty_grid`

read_grid: read a grid tag with no beats as constant

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M8_empty_grid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_file_with_no_grid_tag_reads_absent_never_constant`

Old text:

```
    if not ticks:
        return Grid(state=ABSENT, why=f"{path} holds no beat grid")
```

New text:

```
    if ticks is None:
        return Grid(state=ABSENT, why=f"{path} holds no beat grid")
    if not ticks:
        return Grid(state=CONSTANT)
```

### `u167.M9_relative_key`

key_relation: the relative major or minor reads far, not one step

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M9_relative_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_title_key_is_equal_one_step_or_far_from_rekordbox_s[8A-8B-one_step]`

Old text:

```
    if number == other_number:
        return KEY_ONE_STEP
```

New text:

```
    if number == other_number:
        return KEY_FAR
```

### `u259.M10_chunk_size`

_CHUNK: read 50 IDs to a statement rather than 500, so a scope's statements grow with it

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u259.json`, row `M10_chunk_size`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[analyze]`

Old text:

```
_CHUNK = 500
```

New text:

```
_CHUNK = 50
```

### `u259.M11_scope_carries_no_rows`

resolve_scope: the unanalysed scope carries none of the rows it read

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u259.json`, row `M11_scope_carries_no_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[unanalysed]`

Old text:

```
        read=waiting,
    )
```

New text:

```
    )
```

### `u259.M13_batch_failure_not_met_again`

check_rows: a batch the binding cannot load fails the check, ahead of an earlier row's refusal

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u259.json`, row `M13_batch_failure_not_met_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_row_the_binding_cannot_load_after_one_that_refuses_still_refuses_as_it_did`

Old text:

```
    except Exception:  # noqa: BLE001 - every failure is met again, in order, below
        held = None
```

New text:

```
    except Exception:  # noqa: BLE001 - every failure is met again, in order, below
        raise
```

### `u259.M14_batch_failure_reads_nothing`

check_rows: after a batch the binding cannot load, judge every row as missing rather than read it

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u259.json`, row `M14_batch_failure_reads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_row_the_binding_cannot_load_after_one_that_refuses_still_refuses_as_it_did`

Old text:

```
            content=_UNREAD if held is None else held.get(content_id),
```

New text:

```
            content=None if held is None else held.get(content_id),
```

### `u259.M15_id_not_text_judged`

_unanalysed: judge a row whose ID is stored as bytes, so it joins a scope the read by ID never put it in

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u259.json`, row `M15_id_not_text_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_row_whose_id_is_not_text_stays_out_of_every_row_as_it_did`

Old text:

```
        if isinstance(content.ID, bytes):
            continue
```

New text:

```
        if False:
            continue
```

### `u259.M16_id_skip_widened`

_unanalysed: leave out every ID that is not text, round one's fix, so integer IDs read as nothing to check

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u259.json`, row `M16_id_skip_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[unanalysed]`

Old text:

```
        if isinstance(content.ID, bytes):
```

New text:

```
        if not isinstance(content.ID, str):
```

### `u259.M6_unanalysed_reads_by_id`

_unanalysed: ask for each collection row again by ID, the per row read U259 removed

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u259.json`, row `M6_unanalysed_reads_by_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[unanalysed]`

Old text:

```
        one = analyzed.judge(content_id, content)
```

New text:

```
        one = analyzed.member(db, content_id)
```

### `u259.M7_unanalysed_keeps_no_row`

_unanalysed: carry no row for a waiting ID, so every row of the scope reads as gone

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u259.json`, row `M7_unanalysed_keeps_no_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 6 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[unanalysed]`
  - `tests/test_analyze_check.py::test_a_row_whose_id_is_not_text_stays_out_of_every_row_as_it_did`
  - `tests/test_analyze_check.py::test_an_empty_analyze_playlist_falls_to_every_row_not_analysed`
  - `tests/test_analyze_check.py::test_an_intake_tree_not_cut_over_falls_to_every_row_not_analysed_and_says_why`
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[unanalysed]`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_over_every_row`

Old text:

```
            waiting[one.content_id] = content
```

New text:

```
            waiting[one.content_id] = None
```

### `u259.M8_check_rows_rereads_scope`

check_rows: ignore the rows the scope already read, so the unanalysed scope is read a second time

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u259.json`, row `M8_check_rows_rereads_scope`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[unanalysed]`

Old text:

```
    held: dict[str, Any] | None = dict(scope.read)
```

New text:

```
    held: dict[str, Any] | None = {}
```

### `u259.M9_read_row_per_row`

check_rows: hand read_row no row, so each row in scope is read by ID again

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u259.json`, row `M9_read_row_per_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 70 against a baseline of 70
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[analyze]`
  - `tests/test_analyze_check.py::test_the_check_reads_the_collection_in_statements_that_do_not_grow_with_it[unanalysed]`

Old text:

```
            content=_UNREAD if held is None else held.get(content_id),
```

New text:

```
            content=_UNREAD,
```

### `u93-recursive-analysis.D21_restamp_flag`

The restamp queue ignores the flag and always scans one level

- File: `src/cratekit/analysis/cli.py`
- Source: `u93-recursive-analysis.json`, row `D21_restamp_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 18 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_nested_appledouble_sidecar_and_a_dot_directory_are_not_items`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_freezes_the_flag_in_the_payload`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_queues_every_nested_file_once_in_sorted_order`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_runs_every_nested_item_to_done_and_writes_the_right_file`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_says_which_linked_folders_it_did_not_walk`
  - `tests/test_analysis_workers.py::test_a_restamp_driven_at_its_queue_names_a_linked_folder_once`
  - `tests/test_analysis_workers.py::test_a_tree_whose_only_folders_are_links_says_so_on_the_zero`
  - `tests/test_analysis_workers.py::test_the_resume_repeats_what_the_walk_left_out_rather_than_only_the_queue`
  - `tests/test_analysis_workers.py::test_two_nested_folders_holding_the_same_filename_are_two_items`
  - `tests/test_vocals_cli.py::test_a_nested_file_deleted_after_the_vocals_queue_refuses_that_item_only`
  - `tests/test_vocals_cli.py::test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_queues_every_nested_file_once_in_sorted_order`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_says_which_linked_folders_it_did_not_walk`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    recursive = bool(getattr(ctx.args, "recursive", False))
    scan = discovery.scan_audio(folder, recursive=recursive)
```

New text:

```
    recursive = bool(getattr(ctx.args, "recursive", False))
    scan = discovery.scan_audio(folder, recursive=False)
```

### `u93-recursive-analysis.D22_restamp_resume_warning`

The restamp resume drops the walk's omissions, leaving them on the queue envelope only

- File: `src/cratekit/analysis/cli.py`
- Source: `u93-recursive-analysis.json`, row `D22_restamp_resume_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_restamp_driven_at_its_queue_names_a_linked_folder_once`
  - `tests/test_analysis_workers.py::test_the_resume_repeats_what_the_walk_left_out_rather_than_only_the_queue`

Old text:

```
        warnings = (*warnings, *discovery.warnings_of(job.payload))
        if job.handler_key == "analyze.restamp":
```

New text:

```
        if job.handler_key == "analyze.restamp":
```

### `u93-recursive-analysis.D24_restamp_join`

The restamp worker joins the item id with the operator instead of the checked rule

- File: `src/cratekit/analysis/cli.py`
- Source: `u93-recursive-analysis.json`, row `D24_restamp_join`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_restamp_item_that_would_leave_the_frozen_folder_is_refused`

Old text:

```
    return folder, discovery.item_path(folder, str(item.item_id))
```

New text:

```
    return folder, folder / item.item_id
```

### `u94-a.S1_floor_dropped`

analyze_calibrate: never refuse a sample below the fit floor, so --sample 3 measures three tracks and fails after the walk instead of before it

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S1_floor_dropped`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_refusal_known_before_the_walk_does_not_make_the_walk`
  - `tests/test_analysis_workers.py::test_a_sample_below_the_fit_floor_is_refused_before_measuring[extra0]`
  - `tests/test_analysis_workers.py::test_a_sample_below_the_fit_floor_is_refused_before_measuring[extra1]`

Old text:

```
    if sample < MIN_CALIBRATION_TRACKS:
        return _calibrate_refusal(
```

New text:

```
    if sample < 0:
        return _calibrate_refusal(
```

### `u94-a.S2_floor_off_by_one`

analyze_calibrate: move the floor one below MIN_CALIBRATION_TRACKS, a nearby value, so a sample of nine is accepted

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S2_floor_off_by_one`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_sample_below_the_fit_floor_is_refused_before_measuring[extra0]`
  - `tests/test_analysis_workers.py::test_a_sample_below_the_fit_floor_is_refused_before_measuring[extra1]`

Old text:

```
    if sample < MIN_CALIBRATION_TRACKS:
        return _calibrate_refusal(
```

New text:

```
    if sample < MIN_CALIBRATION_TRACKS - 1:
        return _calibrate_refusal(
```

### `u94-a.S3_partial_refusal_dropped`

analyze_calibrate: never refuse a walk known to be partial before it is made, which is R-409 itself: one genre folder fits and writes

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S3_partial_refusal_dropped`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_recursive_walk_of_one_genre_is_still_one_genre`
  - `tests/test_analysis_workers.py::test_a_refusal_known_before_the_walk_does_not_make_the_walk`
  - `tests/test_analysis_workers.py::test_a_single_genre_folder_without_the_flag_writes_nothing_and_says_why`
  - `tests/test_analysis_workers.py::test_the_root_read_one_level_deep_is_partial_and_names_the_flag`
  - `tests/test_analysis_workers.py::test_the_root_with_no_loose_tracks_and_no_flag_is_told_about_the_flag`
  - `tests/test_analysis_workers.py::test_the_wrong_folder_is_said_before_the_missing_extra`

Old text:

```
    if partial is not None and not accepted:
        return _calibrate_refusal(ctx, _partial_refused(partial), summary)

```

New text:

```
    if False:
        return _calibrate_refusal(ctx, _partial_refused(partial), summary)

```

### `u94-a.S4_accept_flag_dead`

analyze_calibrate: read --accept-partial as always false, so the flag the refusal names does nothing

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S4_accept_flag_dead`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 11 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_partial_fit_that_wrote_nothing_does_not_warn_about_a_calibration`
  - `tests/test_analysis_workers.py::test_a_single_cluster_is_not_cut_down_the_middle`
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`
  - `tests/test_analysis_workers.py::test_accept_partial_writes_and_warns`
  - `tests/test_analysis_workers.py::test_calibrate_cuts_the_vocal_threshold_between_the_two_clusters`
  - `tests/test_analysis_workers.py::test_calibrate_fits_the_energy_reference_over_a_folder_and_writes_it`
  - `tests/test_analysis_workers.py::test_calibrate_over_an_empty_folder_is_a_failed_check_not_a_traceback`
  - `tests/test_analysis_workers.py::test_calibrate_over_too_few_tracks_writes_nothing_and_says_so`
  - `tests/test_analysis_workers.py::test_calibrate_without_the_extra_refuses_rather_than_fitting_over_nothing`

Old text:

```
    accepted = bool(ctx.args.accept_partial)
```

New text:

```
    accepted = False
```

### `u94-a.S5_recursive_not_required`

_partial_before_walk: treat the root read one level deep as the whole library, so only its loose files are fitted and the check says ok

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S5_recursive_not_required`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_root_read_one_level_deep_is_partial_and_names_the_flag`
  - `tests/test_analysis_workers.py::test_the_root_with_no_loose_tracks_and_no_flag_is_told_about_the_flag`

Old text:

```
    if wide and recursive:
        return None
```

New text:

```
    if wide:
        return None
```

### `u94-a.S6_music_folder_not_wide`

_is_library_wide: accept the root alone, so the music folder every module places tracks under is refused as not the library

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S6_music_folder_not_wide`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_music_folder_walked_recursively_is_the_library_too`

Old text:

```
    for candidate in (root, root / cfg.library.music_dir):
```

New text:

```
    for candidate in (root,):
```

### `u94-a.S7_samefile_to_spelling`

_is_library_wide: compare two spellings instead of asking the filesystem, so the root reached through a link is not the root

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S7_samefile_to_spelling`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_root_reached_through_a_link_is_still_the_root`

Old text:

```
            if os.path.samefile(folder, candidate):
```

New text:

```
            if str(folder) == str(candidate):
```

### `u94-a.S8_after_walk_never_asked`

analyze_calibrate: never ask what the walk left out, so a root missing a linked or unreadable genre reads ok

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S8_after_walk_never_asked`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`

Old text:

```
        partial = _partial_after_walk(scan)
```

New text:

```
        partial = None
```

### `u94-b.W1_after_walk_refusal_dropped`

analyze_calibrate: ask what the walk left out and fit anyway without the flag, so the omission is known and ignored

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W1_after_walk_refusal_dropped`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`

Old text:

```
        if partial is not None and not accepted:
            return _calibrate_refusal(ctx, _partial_refused(partial), summary, omitted)
```

New text:

```
        if False:
            return _calibrate_refusal(ctx, _partial_refused(partial), summary, omitted)
```

### `u94-b.W3_accepted_reads_ok`

_partial_accepted: report an accepted partial as ok, so it reads as the library wide fit on the check row

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W3_accepted_reads_ok`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`
  - `tests/test_analysis_workers.py::test_accept_partial_writes_and_warns`

Old text:

```
        "skipped",
        f"{what}; fitted anyway
```

New text:

```
        "ok",
        f"{what}; fitted anyway
```

### `u94-b.W4_partial_warning_dropped`

analyze_calibrate: never put calibration-partial-sample on the envelope

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W4_partial_warning_dropped`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`
  - `tests/test_analysis_workers.py::test_accept_partial_writes_and_warns`

Old text:

```
if partial is not None and wrote else ())
```

New text:

```
if False else ())
```

### `u94-b.W5_warning_without_a_write`

analyze_calibrate: warn about what was written when neither half wrote anything

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W5_warning_without_a_write`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_partial_fit_that_wrote_nothing_does_not_warn_about_a_calibration`

Old text:

```
if partial is not None and wrote else ())
```

New text:

```
if partial is not None else ())
```

### `u94-b.W7_omissions_dropped_from_the_fit`

analyze_calibrate: leave the walk's omissions off the envelope of a fit that went ahead

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W7_omissions_dropped_from_the_fit`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`

Old text:

```
        + tuple(omitted),
```

New text:

```
        + tuple(()),
```

### `u94-b.W8_note_forgets_the_omission`

fitted_note: never record how many folders were not walked, so the file a later restamp trusts reads as a whole fit

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W8_note_forgets_the_omission`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`

Old text:

```
    if left_out:
        note +=
```

New text:

```
    if False:
        note +=
```

### `u94-c.N1_stride_is_the_first_n`

stride_sample: take the first N of the sorted walk, which is the first few folders of the alphabet

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N1_stride_is_the_first_n`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_same_tree_gives_the_same_sample_twice`
  - `tests/test_analysis_workers.py::test_the_stride_sample_is_even_ordered_and_reaches_the_tail`

Old text:

```
    return [items[index * total // count] for index in range(count)]
```

New text:

```
    return list(items[:count])
```

### `u94-c.N2_stride_is_a_fixed_step`

stride_sample: a fixed step of len // count, which stops short of the tail whenever the division has a remainder

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N2_stride_is_a_fixed_step`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_stride_sample_is_even_ordered_and_reaches_the_tail`

Old text:

```
    return [items[index * total // count] for index in range(count)]
```

New text:

```
    return [items[index * (total // count)] for index in range(count)]
```

### `u94-c.N3_sample_ignored`

analyze_calibrate: measure every walked track whatever --sample says, the unbounded run the brief rules out

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N3_sample_ignored`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_sample_at_the_fit_floor_is_accepted`
  - `tests/test_analysis_workers.py::test_the_same_tree_gives_the_same_sample_twice`
  - `tests/test_analysis_workers.py::test_the_vocal_cut_reads_every_tagged_file_while_energy_reads_the_sample`

Old text:

```
    sampled = stride_sample(paths, sample)
```

New text:

```
    sampled = list(paths)
```

### `u94-c.N4_vocal_half_sampled`

analyze_calibrate: hand the vocal half the sample instead of every file under the walk

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N4_vocal_half_sampled`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_vocal_cut_reads_every_tagged_file_while_energy_reads_the_sample`

Old text:

```
        _calibrate_vocals(cfg, folder, paths, left_out),
```

New text:

```
        _calibrate_vocals(cfg, folder, sampled, left_out),
```

### `u94-c.N5_note_m_is_the_sample`

analyze_calibrate: record the sample size as M, so the note reads N of N and hides how much of the library was fitted

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N5_note_m_is_the_sample`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_same_tree_gives_the_same_sample_twice`

Old text:

```
        _calibrate_energy(cfg, folder, sampled, len(paths), left_out),
```

New text:

```
        _calibrate_energy(cfg, folder, sampled, len(sampled), left_out),
```

### `u94-c.N6_default_sample_halved`

DEFAULT_CALIBRATION_SAMPLE: halve the coefficient, 500 to 250

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-c.json`, row `N6_default_sample_halved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_default_sample_is_what_the_parser_hands_the_verb`

Old text:

```
DEFAULT_CALIBRATION_SAMPLE = 500
```

New text:

```
DEFAULT_CALIBRATION_SAMPLE = 250
```

### `u94-c.N7_root_not_required_first`

analyze_calibrate: ask the folder's standing with the library away, so an unmounted volume is blamed on the folder

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N7_root_not_required_first`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_calibrate_refuses_with_the_library_away_rather_than_writing_beside_the_mount`

Old text:

```
    _require_library_root(cfg)
    partial = _partial_before_walk
```

New text:

```
    partial = _partial_before_walk
```

### `u94-c.N8_absent_folder_not_told_apart`

analyze_calibrate: drop the not a folder answer, so a mistyped path is told it is not the library root

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N8_absent_folder_not_told_apart`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`
  - `tests/test_analysis_workers.py::test_calibrate_over_a_folder_that_is_not_there_says_that_and_not_empty`

Old text:

```
    if not folder.is_dir():
        return _calibrate_refusal(
```

New text:

```
    if False:
        return _calibrate_refusal(
```

### `r1631.M25_bandcamp_any_head`

_bandcamp_heading_matches: drop a heading's head whether or not it names the artist

- File: `src/cratekit/tagging/shops.py`
- Source: `r1631.json`, row `M25_bandcamp_any_head`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 1 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_bandcamp_writes_no_genre_off_another_track_by_the_artist[Original Mix-Sunrise Mood - Original Mix]`

Old text:

```
    if dash and _artist_matches(artist, head):
```

New text:

```
    if dash:
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
  - `tests/test_title_matcher.py::test_what_the_whole_name_found_the_parse_still_reads[Bernard Badie & Tide-08A - 124 - Sunrise Mood (feat. Tide) - Bernard Badie - Vocal Mix-Sunrise Mood]`

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

### `u280.M03_bare_names_dropped`

Title.same: a bare name of one title no longer meets the other's names, "(Not Just) Knee Deep" misses "Knee Deep"

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M03_bare_names_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 3 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_headed_file_title_matches_its_own_row[08A - 124 - (Not Just) Knee Deep (Part 1)-Knee Deep]`
  - `tests/test_title_matcher.py::test_discogs_still_matches_a_title_to_its_own_track[08A - 124 - (Not Just) Knee Deep (Part 1)-Knee Deep]`
  - `tests/test_title_matcher.py::test_the_scraped_parsers_still_match_a_title_to_its_own_row[08A - 124 - (Not Just) Knee Deep (Part 1)-Knee Deep]`

Old text:

```
            self.names & other.names or self.names & other.bare or self.bare & other.names

```

New text:

```
            self.names & other.names or self.names & other.bare

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
  - `tests/test_title_matcher.py::test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other`
  - `tests/test_title_matcher.py::test_what_the_whole_name_found_the_parse_still_reads[Bernard Badie-[MP3] 01 Sunrise Mood-Sunrise Mood]`

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
  - `tests/test_title_matcher.py::test_a_files_title_among_its_dash_parts_still_finds_its_own_row[08A - 124 - Bernard Badie - Original Mix-Bernard Badie (Extended Mix)]`
  - `tests/test_title_matcher.py::test_a_files_title_among_its_dash_parts_still_finds_its_own_row[Bernard Badie - Original Mix-Bernard Badie]`
  - `tests/test_title_matcher.py::test_a_name_is_read_once_into_its_parts[Bernard Badie-Bernard Badie - Original Mix-title after-titled]`
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

### `u280.M13_ambiguity_track_numbered`

_only_a_list_reads: a track numbered later title no longer makes X its album

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M13_ambiguity_track_numbered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 3 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_track_numbered_title_after_a_version_ending_album_is_still_the_title[Bernard Badie - Summer Mix - 01 - Sunrise Mood]`
  - `tests/test_title_matcher.py::test_a_track_numbered_title_after_a_version_ending_album_is_still_the_title[Bernard Badie - Summer Mix - 01 Sunrise Mood Extended Mix]`
  - `tests/test_title_matcher.py::test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other`

Old text:

```
    if first >= layout.end or layout.numbered or not credits:

```

New text:

```
    if first >= layout.end or not credits:

```

### `u280.M15_splits_without_feature_cut`

_name_splits: X is split only as written, never without its feature credit

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M15_splits_without_feature_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 1 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_name_hiding_the_shape_is_ambiguous_too[Bernard Badie-Bernard Badie - Vocal Mix feat. Tide-Vocal-Bernard Badie (Vocal Mix)]`

Old text:

```
    for tail in dict.fromkeys((parts[ambiguous], _before_featuring(parts[ambiguous]).rstrip())):

```

New text:

```
    for tail in (parts[ambiguous],):

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
  - `tests/test_title_matcher.py::test_what_the_whole_name_found_the_parse_still_reads[Tide-Sunrise Mood feat. Tide - Bernard Badie-Sunrise Mood]`

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
  - `tests/test_title_matcher.py::test_beatport_ranks_no_row_by_brackets_shed_across_a_dash[Bernard Badie - (Intro) (Live)]`
  - `tests/test_title_matcher.py::test_beatport_ranks_no_row_by_brackets_shed_across_a_dash[Bernard Badie - (Intro)]`
  - `tests/test_title_matcher.py::test_beatport_ranks_no_row_by_brackets_shed_across_a_dash[Bernard Badie - [Intro]]`
  - `tests/test_title_matcher.py::test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other`
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Bernard Badie-Bernard Badie - Bernard Badie Theme-Bernard Badie Theme-Bernard Badie]`
  - `tests/test_title_matcher.py::test_round_two_a_title_keeps_its_own_row_and_takes_no_other[Tide-Tide - Riding The Tide-Riding The Tide-Tide]`
  - `tests/test_title_matcher.py::test_the_artists_part_before_any_other_part_reads_as_it_did[Bernard Badie - Sunrise Mood (Extended Mix)-Sunrise Mood-Bernard Badie]`
  - `tests/test_title_matcher.py::test_the_artists_part_before_any_other_part_reads_as_it_did[Bernard Badie - Sunrise Mood-Sunrise Mood-Bernard Badie]`
  - `tests/test_title_matcher.py::test_the_artists_part_is_known_as_a_name_writes_it[Bernard Badie-Bernard Badie - Sun Path - 02 - Tide-Tide]`
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
  - `tests/test_title_matcher.py::test_what_the_whole_name_found_the_parse_still_reads[Bernard Badie-100 - Original Mix-100]`
  - `tests/test_title_matcher.py::test_what_the_whole_name_found_the_parse_still_reads[Bernard Badie-124 - Interlude-124]`

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
  - `tests/test_title_matcher.py::test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other`
  - `tests/test_title_matcher.py::test_what_the_whole_name_found_the_parse_still_reads[Bernard Badie-[MP3] 01 - Bernard Badie - (Intro)-(Intro)]`

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

### `u280.M31_bracketed_later_title_unread`

_opens_with_a_track_number: "02 (Intro)" after an album is no later title, and "(Intro)" is never read

- File: `src/cratekit/tagging/titles.py`
- Source: `u280.json`, row `M31_bracketed_later_title_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_title_matcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_bandcamp.py`
- Collected: 1241 against a baseline of 1241
- Kills: 1 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other`

Old text:

```
    return _numbered(core) or (len(core) == 1 and _a_track_number(core[0]) and len(words(part)) > 1)

```

New text:

```
    return _numbered(core)

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

### `u282.D1_discogs_decline_ends_the_walk`

search: a Discogs decline is returned at once, so Beatport is never asked after an unmapped style (merge blocker 2)

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `D1_discogs_decline_ends_the_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 9 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_a_beatport_miss_keeps_discogs_word_and_is_not_no_hit`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[outage]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[refused]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[reshaped]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[both]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[fallback-only]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[styleless]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[unmapped]`
  - `tests/test_discogs_first.py::test_two_declines_keep_discogs_word_and_beatport_s_picture`

Old text:

```
            if resolved.genre is None and source not in _SEARCHES:
```

New text:

```
            if False:
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

### `u282.D3_second_decline_named`

search: the later decline names the file over Discogs' held one

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `D3_second_decline_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_two_declines_keep_discogs_word_and_beatport_s_picture`

Old text:

```
                declined if resolved.genre is None and declined is not None else resolved,
```

New text:

```
                resolved,
```

### `u282.D5_held_decline_dropped`

search: a held Discogs decline is forgotten at the walk's end, so a Discogs decline beside a Beatport miss is a no-hit and beside a refusal an outage (merge blocker 3)

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `D5_held_decline_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 6 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_a_beatport_miss_keeps_discogs_word_and_is_not_no_hit`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[outage]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[refused]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[reshaped]`
  - `tests/test_discogs_searcher.py::test_a_matched_release_with_no_style_declines_with_nothing_to_map`
  - `tests/test_discogs_searcher.py::test_no_style_that_names_a_folder_is_a_decline_naming_the_first_style`

Old text:

```
        if declined is not None:
            return _lent(
```

New text:

```
        if False:
            return _lent(
```

### `u282.L1_decline_lends_no_picture`

_lent: a shop's matched row lends no picture to a Discogs decline

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `L1_decline_lends_no_picture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_two_declines_keep_discogs_word_and_beatport_s_picture`

Old text:

```
    return replace(hit, art_url=shown.art_url, art_source=shown.source)
```

New text:

```
    return replace(hit, art_url="", art_source="")
```

### `u282.L2_nobody_named_is_the_source`

_lent: with no shop's row, art_source stays None, so the picture's report is written about Discogs

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `L2_nobody_named_is_the_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_a_beatport_miss_keeps_discogs_word_and_is_not_no_hit`
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_misses_names_no_picture_and_no_unread`
  - `tests/test_discogs_first.py::test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread`

Old text:

```
        return replace(hit, art_url="", art_source="")
```

New text:

```
        return replace(hit, art_url="")
```

### `u282.L3_shop_row_not_recorded`

search: the matched shop row is never recorded as the picture's

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `L3_shop_row_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_two_declines_keep_discogs_word_and_beatport_s_picture`

Old text:

```
            if source in _SEARCHES:
                shown = outcome
```

New text:

```
            if source in _SEARCHES:
                pass
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

### `u282.P4_refusal_not_unread`

_pictured: a refused or unread picture ask does not join unread

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `P4_refusal_not_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 3 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_refuses_is_unread_and_counts_toward_the_stop`
  - `tests/test_discogs_first.py::test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread`

Old text:

```
            if outcome.answer.value in UNREAD_ANSWERS and source not in unread:
```

New text:

```
            if False:
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

### `u282.P6_waiting_note_dropped`

_pictured: the not-asked entry carries no note saying Beatport waits for a picture

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `P6_waiting_note_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`

Old text:

```
        replace(said, note=note) if said.source in later else said for said in lent.answers
```

New text:

```
        said for said in lent.answers
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

### `u282.R2_any_refusal_held`

search: any refusal from the asker is held, not only a rejected token

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `R2_any_refusal_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_only_a_refused_token_is_held_and_any_other_refusal_from_discogs_propagates`

Old text:

```
                    if refusal.cause.reason != _CREDENTIAL_REASON:
                        raise
```

New text:

```
                    if False:
                        raise
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

### `u282.W1_walk_beatport_first`

WALK: Beatport first again, the order before the card

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u282.json`, row `W1_walk_beatport_first`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
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
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
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

### `u282.T3_failed_question_raises`

_picture_asked: a question that fails raises and fails a file whose genre was written

- File: `src/cratekit/tagging/tag.py`
- Source: `u282.json`, row `T3_failed_question_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_picture_ask_that_raises_never_fails_the_file`

Old text:

```
    except Exception as exc:  # noqa: BLE001
        said = f"{exc.cause.reason}
```

New text:

```
    except ZeroDivisionError as exc:  # noqa: BLE001
        said = f"{exc.cause.reason}
```

### `u282.T4_failed_question_result_dropped`

tag_one: a failed question's art result is dropped, so the picture is fetched off a hit that named none

- File: `src/cratekit/tagging/tag.py`
- Source: `u282.json`, row `T4_failed_question_result_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_picture_ask_that_raises_never_fails_the_file`

Old text:

```
    elif unasked is not None:
        pictured = unasked
```

New text:

```
    elif False:
        pictured = unasked
```

### `r1724.N13_retag_raw_stem`

retag_one: ask the raw stem, so tag retag asks Sunshine Hotel_PN

- File: `src/cratekit/tagging/retag.py`
- Source: `r1724.json`, row `N13_retag_raw_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_retag_asks_a_file_with_no_title_tag_its_name_past_the_tail`

Old text:

```
        title = tags.read_tag(candidate.path, "title") or titles.name_title(candidate.path.stem)
```

New text:

```
        title = tags.read_tag(candidate.path, "title") or candidate.path.stem
```

### `r1724.N14_retag_tag_read`

retag_one: read the tail off a title tag too

- File: `src/cratekit/tagging/retag.py`
- Source: `r1724.json`, row `N14_retag_tag_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_retag_asks_a_title_tag_ending_in_the_tail_as_written`

Old text:

```
        title = tags.read_tag(candidate.path, "title") or titles.name_title(candidate.path.stem)
```

New text:

```
        title = titles.name_title(tags.read_tag(candidate.path, "title") or candidate.path.stem)
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

### `r1724.N12_tag_one_tag_read`

tag_one: read the tail off a title tag too, so a tag ending _PN is not asked as written

- File: `src/cratekit/tagging/tag.py`
- Source: `r1724.json`, row `N12_tag_one_tag_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_title_tag_ending_in_the_tail_is_asked_and_matched_as_written`

Old text:

```
    title = title_tag or titles.name_title(path.stem)
```

New text:

```
    title = titles.name_title(title_tag or path.stem)
```

### `r1724.N10_by_name_unsplit_stem`

by_name: the unsplit question reads the raw stem, so an ambiguous name is asked with its tail

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N10_by_name_unsplit_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 2 (killed)
- Killed:
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[8A - 124 - Make Luv - Room 5 - Album_PN-asked3]`
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[8A - 124_PN-asked5]`

Old text:

```
    unsplit = question(name, "")
```

New text:

```
    unsplit = question(stem, "")
```

### `r1724.N1_tail_any_case`

name_title: read the tail in any letter case, so a name ending _pn loses it too

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N1_tail_any_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_name_with_no_tail_is_read_byte_for_byte[Sunrise Mood_pn]`

Old text:

```
    if not text.endswith(NAME_TAIL):
        return stem
    parts =
```

New text:

```
    if not text.lower().endswith(NAME_TAIL.lower()):
        return stem
    parts =
```

### `r1724.N2_no_trailing_space_read`

name_title: read the stem with its trailing space, so a tail before a space is kept

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N2_no_trailing_space_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood_PN  -Sunrise Mood]`

Old text:

```
    text = stem.rstrip()
    if not text.endswith(NAME_TAIL):
```

New text:

```
    text = stem
    if not text.endswith(NAME_TAIL):
```

### `r1724.N3_space_before_tail_kept`

name_title: keep the space before the tail, so Sunrise Mood _PN is asked with a trailing space

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N3_space_before_tail_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_name_loses_the_tail_after_its_title[Sunrise Mood _PN-Sunrise Mood]`

Old text:

```
    parts[-1] = parts[-1].rstrip()

```

New text:

```
(empty)
```

### `r1724.N4_tail_alone_guard`

name_title: drop the tail alone guard, so 8A - 124 - Artist - _PN reads to a name ending in a dash and loses its ISRC genre

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N4_tail_alone_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 9 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_asked_as_before`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[ _PN-asked1]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - Artist - ?_PN-asked6]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - Artist - Title - _PN-asked5]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - Sean Doron - _PN-asked3]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - _PN-asked4]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[Sean Doron - _PN-asked2]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[_PN-asked0]`
  - `tests/test_name_tail.py::test_retag_asks_a_name_whose_last_part_is_the_tail_alone_as_written`

Old text:

```
    if not identifies(parts[-1]):
        return stem
    return DASH.join(parts)
```

New text:

```
    return DASH.join(parts)
```

### `r1724.N5_tail_alone_empty`

name_title: a tail alone name reads to nothing, round one's code, so it asks nothing and misses its ISRC

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N5_tail_alone_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 9 (killed)
- Killed:
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_asked_as_before`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[ _PN-asked1]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - Artist - ?_PN-asked6]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - Artist - Title - _PN-asked5]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - Sean Doron - _PN-asked3]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[8A - 124 - _PN-asked4]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[Sean Doron - _PN-asked2]`
  - `tests/test_name_tail.py::test_a_name_whose_last_part_is_the_tail_alone_is_read_as_written[_PN-asked0]`
  - `tests/test_name_tail.py::test_retag_asks_a_name_whose_last_part_is_the_tail_alone_as_written`

Old text:

```
    if not identifies(parts[-1]):
        return stem
    return DASH.join(parts)
```

New text:

```
    if not identifies(parts[-1]):
        return ""
    return DASH.join(parts)
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

### `r1724.N8_by_name_raw_stem`

by_name: read the raw stem, so Sunshine Hotel_PN splits with its tail

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N8_by_name_raw_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 6 (killed)
- Killed:
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[06A - 126 - Sean Doron - Sunshine Hotel_PN-asked0]`
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[8A - 124 - Make Luv - Room 5 - Album_PN-asked3]`
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[8A - 124 - [MP3] Lane 8 - Aba_PN-asked2]`
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[8A - 124_PN-asked5]`
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[9A - 136 - Obiman - On The Rocks (Cafe Del Mar Mix)_PN-asked1]`
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[Sunshine Hotel_PN-asked4]`

Old text:

```
    name = name_title(stem)
    rest = _past_head(name)
```

New text:

```
    name = stem
    rest = _past_head(name)
```

### `r1724.N9_by_name_headless_stem`

by_name: a headless name is asked as its raw stem, tail and all

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N9_by_name_headless_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_name_tail.py`, `tests/test_discogs_question.py`, `tests/test_title_matcher.py`, `tests/test_genre_retag.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`
- Collected: 1679 against a baseline of 1679
- Kills: 1 (killed)
- Killed:
  - `tests/test_name_tail.py::test_the_name_read_reads_past_the_tail[Sunshine Hotel_PN-asked4]`

Old text:

```
        return Question("", name, Read.AS_WRITTEN)
```

New text:

```
        return Question("", stem, Read.AS_WRITTEN)
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

### `u178.S1_summary_counts_labels`

_summary: never count a file per label, so label_genres stays empty

- File: `src/cratekit/tagging/summary.py`
- Source: `u178.json`, row `S1_summary_counts_labels`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
            if wrote == tag_engine.LABEL_GENRE:
```

New text:

```
            if False:
```

### `u178.S2_unknown_label_refused`

_label_payload: a --label nobody registered queues the sweep with no label

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S2_unknown_label_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_nobody_registered_is_refused_and_nothing_is_queued`

Old text:

```
        if entry is None:
            raise refuse(
                "label-unknown",
```

New text:

```
        if entry is None and False:
            raise refuse(
                "label-unknown",
```

### `u178.S3_unreadable_registry_refuses_label`

_label_payload: an unreadable registry warns rather than refusing a sweep given --label

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S3_unreadable_registry_refuses_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_an_unreadable_registry_warns_and_refuses_only_a_sweep_that_named_a_label`

Old text:

```
    except CratekitError as exc:
        if label is not None:
            raise

```

New text:

```
    except CratekitError as exc:

```

### `u178.S4_genres_frozen`

_label_payload: freeze no genres, so a registered label genre never reaches the worker

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S4_genres_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_label_tag_reaches_its_genre_with_no_label_named`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
    if genres:
        frozen["label_genres"] = genres
```

New text:

```
    if False:
        frozen["label_genres"] = genres
```

### `u178.S5_worker_takes_label`

handle: hand the engine no --label, so a folder of untagged files is searched

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S5_worker_takes_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        label=str(payload.get("label") or "") or None,
```

New text:

```
        label=None,
```

### `u178.S6_outranked_needs_label`

_label_warnings: warn about outranked tags on a sweep given no --label

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S6_outranked_needs_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_label_tag_that_could_never_name_a_label_is_searched_and_never_fails`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_tag_naming_no_genre_says_nothing_on_a_sweep_given_no_label`

Old text:

```
    if payload.get("label") and outranked:
```

New text:

```
    if outranked:
```

### `u178-e9.E9_label_tag_reset`

tag_one: keep the file's tag in label_tag on a file the label answered for

- File: `src/cratekit/tagging/tag.py`
- Source: `u178-e9.json`, row `E9_label_tag_reset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`

Old text:

```
        label_tag = ""
        _written(
```

New text:

```
        _written(
```

### `u178.E2_no_search_with_picture`

tag_one: drop the early return for a labelled file with a picture, so the catalogues are searched

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E2_no_search_with_picture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_folder_of_mixed_labels_tags_each_by_its_own`
  - `tests/test_label_genre.py::test_a_label_tag_reaches_its_genre_with_no_label_named`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_puls_file_with_no_genre_gets_its_labels_genre_with_no_searcher_called`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`
  - `tests/test_label_genre.py::test_the_verbs_label_names_the_label_of_a_file_with_no_tag_and_the_tag_wins`

Old text:

```
        if settled is not None:
            return TagResult(path=path, **labelled, **repaired, **settled)

```

New text:

```
(empty)
```

### `u178.E3_art_refusal_tolerated`

tag_one: a refusal on a labelled file's art search fails the item

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E3_art_refusal_tolerated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_refusal_on_the_art_search_does_not_fail_a_puls_file`

Old text:

```
        if needs_genre:
            raise
```

New text:

```
        if not existing:
            raise
```

### `u178.E4_isrc_withheld`

tag_one: offer the general catalogue the ISRC of a labelled file searched for art

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E4_isrc_withheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_an_art_search_for_a_labelled_file_never_offers_the_general_catalogue_its_isrc`

Old text:

```
        wanted = needs_genre and not hit.genre
```

New text:

```
        wanted = not existing and not hit.genre
```

### `u178.E6_label_write_checked`

tag_one: the label genre write's False is ignored, so a locked file is reported tagged

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E6_label_write_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`

Old text:

```
        _written(path, by_label.genre, f"its label {by_label.label}")
```

New text:

```
        tags.write_genre(path, by_label.genre)
```

### `u178.E7_catalogue_write_checked`

tag_one: the catalogue genre write's False is ignored, as on main

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E7_catalogue_write_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_a_catalogues_genre_fails_too`

Old text:

```
        written = _written(path, hit.genre, hit.source or "a catalogue")
```

New text:

```
        tags.write_genre(path, hit.genre)
        written = hit.genre
```

### `u244.M04_refusal_remembered`

DiscogsAsker.ask: forget a block, so every later file waits out the 429 ladder again

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M04_refusal_remembered`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_429_on_every_attempt_is_blocked_and_remembered_for_the_run`

Old text:

```
        if self.refused is not None:
```

New text:

```
        if False:
```

### `u244.M05_401_is_rejection`

DiscogsAsker._read: read a 401 as an ordinary unreachable answer, an outage, not a rejected credential

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M05_401_is_rejection`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_401_on_a_release_read_is_the_same_rejection`
  - `tests/test_discogs_searcher.py::test_a_rejected_token_is_a_run_refusal_typed_as_a_rejection`
  - `tests/test_discogs_searcher.py::test_a_rejected_token_is_not_sent_again_in_the_run`

Old text:

```
        if page.status == 401:
```

New text:

```
        if page.status == 4010:
```

### `u244.M06_gone_release_passed_over`

DiscogsAsker._read: hold a gone release as unreachable instead of passing it over

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M06_gone_release_passed_over`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_release_is_taken_only_when_a_track_and_its_artist_match[only gone]`

Old text:

```
        if release and page.status in _GONE_STATUSES:
```

New text:

```
        if False:
```

### `u244.M07_remaining_floor`

DiscogsAsker._read: slow down only under the floor, not at it

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M07_remaining_floor`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_low_remaining_count_slows_the_next_request_and_a_high_one_does_not`

Old text:

```
        if self.remaining is not None and self.remaining <= DISCOGS_REMAINING_FLOOR:
```

New text:

```
        if self.remaining is not None and self.remaining < DISCOGS_REMAINING_FLOOR:
```

### `u244.M08_notes_scrubbed`

DiscogsAsker._scrub: leave the token in a note a transport failure carried

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M08_notes_scrubbed`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_the_token_reaches_no_url_note_record_log_or_refusal`

Old text:

```
        return text.replace(self.token, _SCRUBBED) if self.token else text
```

New text:

```
        return text
```

### `u244.M09_results_not_a_list`

DiscogsAsker._search: read an answer with no results list as a miss, not a parse break

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M09_results_not_a_list`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_search_nobody_can_read_a_result_off_is_unread_and_never_a_miss[{"pagination": {}}-parse-break]`
  - `tests/test_discogs_searcher.py::test_beatport_unreachable_and_a_discogs_parse_break_refuse_as_a_defect`

Old text:

```
            return self._said(
                Answer.PARSE_BREAK, "the search answer carries no list of results"
            )
```

New text:

```
            return self._said(Answer.MISS)
```

### `u244.M10_unread_outranks_styleless`

DiscogsAsker._search: return a styleless match ahead of a pressing that could not be read, round two's R1

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M10_unread_outranks_styleless`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_release_is_taken_only_when_a_track_and_its_artist_match[styleless beside unread]`

Old text:

```
        if held is not None:
            return held
        if styleless is not None:
```

New text:

```
        if styleless is not None:
```

### `u244.M11_block_ends_release_walk`

DiscogsAsker._search: hold a blocked release read and go on reading releases

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M11_block_ends_release_walk`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_block_on_a_release_read_ends_the_walk_over_releases`

Old text:

```
                if read.answer is Answer.BLOCKED:
                    return read
```

New text:

```
                if False:
                    return read
```

### `u244.M13_styleless_gives_way`

DiscogsAsker._search: return the first matching pressing even when it carries no style

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M13_styleless_gives_way`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_pressing_with_no_style_gives_way_to_one_with_styles`
  - `tests/test_discogs_searcher.py::test_a_release_is_taken_only_when_a_track_and_its_artist_match[styleless beside unread]`

Old text:

```
            if not release.styles:
```

New text:

```
            if False:
```

### `u244.M18_article_first`

_discogs_name: leave an article filed last, so Prodigy, The reads as an artist called the

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M18_article_first`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_release_is_taken_only_when_a_track_and_its_artist_match[article filed last]`
  - `tests/test_discogs_searcher.py::test_discogs_names_are_read_as_a_tag_spells_them`

Old text:

```
    return f"{moved['article']} {moved['name']}" if moved else bare
```

New text:

```
    return bare
```

### `r791-a.S10_track_unread_returned`

_search_bandcamp: drop the unread track page and answer MISS, the pre R-791 fall through

- File: `src/cratekit/tagging/shops.py`
- Source: `r791-a.json`, row `S10_track_unread_returned`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 239 against a baseline of 239
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_track_page_unread_is_not_a_miss[challenge]`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_track_page_unread_is_not_a_miss[outage]`

Old text:

```
    if track_unread is not None:
        return track_unread
```

New text:

```
    if False:
        return track_unread
```

### `r791-a.S14_blocked_step`

_decide: the unreachable refusal never says a fallback was blocked

- File: `src/cratekit/tagging/searchers.py`
- Source: `r791-a.json`, row `S14_blocked_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_three_refusals_raise_unreachable_and_say_the_fallbacks_were_blocked`

Old text:

```
    if blocked:
        steps.append(
```

New text:

```
    if False:
        steps.append(
```

### `r791-a.S1_403_blocks`

_BLOCK_STATUSES: drop 403, so Traxsource's Cloudflare 403 reads as unreachable again

- File: `src/cratekit/tagging/catalogues.py`
- Source: `r791-a.json`, row `S1_403_blocks`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
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

### `r791-a.S2_429_blocks`

_BLOCK_STATUSES: drop 429, so a spent rate limit on a fallback reads as unreachable

- File: `src/cratekit/tagging/catalogues.py`
- Source: `r791-a.json`, row `S2_429_blocks`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 239 against a baseline of 239
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_fallbacks_refusal_is_blocked_and_its_outage_unreachable[spent 429]`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`

Old text:

```
_BLOCK_STATUSES = frozenset({403, 429})
```

New text:

```
_BLOCK_STATUSES = frozenset({403})
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

### `r791-a.S4_ellipsis_character`

_CHALLENGE_TITLE: match only three dots, not the single ellipsis character

- File: `src/cratekit/tagging/catalogues.py`
- Source: `r791-a.json`, row `S4_ellipsis_character`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_the_interstitial_title_written_with_one_ellipsis_character_is_blocked`

Old text:

```
just a moment(?:\.\.\.|\u2026)
```

New text:

```
just a moment\.\.\.
```

### `r791-a.S5_challenge_body`

_unread: never read Cloudflare's challenge script in the body

- File: `src/cratekit/tagging/catalogues.py`
- Source: `r791-a.json`, row `S5_challenge_body`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_fallbacks_refusal_is_blocked_and_its_outage_unreachable[challenge script]`

Old text:

```
    if _CHALLENGE_BODY.search(page.text):
```

New text:

```
    if False:
```

### `r791-a.S8_blocked_track_page_stops`

_search_bandcamp: keep fetching track pages after one came back blocked

- File: `src/cratekit/tagging/shops.py`
- Source: `r791-a.json`, row `S8_blocked_track_page_stops`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_blocked_bandcamp_track_page_stops_the_walk_over_further_listings`

Old text:

```
                track_unread = unread
                break
```

New text:

```
                track_unread = unread
```

### `r791-a.S9_gone_track_page`

_GONE_STATUSES: empty, so a dead listing's 404 leaves the file unreachable for ever

- File: `src/cratekit/tagging/catalogues.py`
- Source: `r791-a.json`, row `S9_gone_track_page`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_track_page_that_is_gone_is_a_dead_listing_and_still_a_miss`

Old text:

```
_GONE_STATUSES = frozenset({404, 410})
```

New text:

```
_GONE_STATUSES = frozenset()
```

### `u275.M1_base_back_to_linux`

LIGHT_BASE_BYTES back to U241's 320 megabytes, the figure before the Mac was measured

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M1_base_back_to_linux`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 549 against a baseline of 549
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[729-2346]`
  - `tests/test_analysis_ahead.py::test_the_declared_line_keeps_the_linux_margin_over_the_macs_measured_line`

Old text:

```
LIGHT_BASE_BYTES = 384 * 1024 * 1024
```

New text:

```
LIGHT_BASE_BYTES = 320 * 1024 * 1024
```

### `u275.M2_slope_back_to_linux`

LIGHT_BYTES_PER_SECOND back to U241's 1.5 megabytes a second, under every Mac peak

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M2_slope_back_to_linux`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 549 against a baseline of 549
- Kills: 19 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[376-1281]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[576-1805]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[668-2105]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[690-2162]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[729-2346]`
  - `tests/test_analysis_ahead.py::test_eight_gigabytes_free_over_the_six_mac_tracks_is_one_worker`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[12]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[18]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[24]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[32]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[4]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
LIGHT_BYTES_PER_SECOND = 25 * 1024 * 1024 // 8
```

New text:

```
LIGHT_BYTES_PER_SECOND = 3 * 1024 * 1024 // 2
```

### `u275.M3_slope_rounded_down`

LIGHT_BYTES_PER_SECOND rounded down to 3.0 megabytes a second, over every peak but under a ninth above the measured slope

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M3_slope_rounded_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 549 against a baseline of 549
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[729-2346]`
  - `tests/test_analysis_ahead.py::test_the_declared_line_keeps_the_linux_margin_over_the_macs_measured_line`

Old text:

```
LIGHT_BYTES_PER_SECOND = 25 * 1024 * 1024 // 8
```

New text:

```
LIGHT_BYTES_PER_SECOND = 3 * 1024 * 1024
```

### `u275.M4_base_rounded_down`

LIGHT_BASE_BYTES rounded down to 352 megabytes, over the measured intercept but under an eighth above it

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M4_base_rounded_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 549 against a baseline of 549
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_the_declared_line_keeps_the_linux_margin_over_the_macs_measured_line`

Old text:

```
LIGHT_BASE_BYTES = 384 * 1024 * 1024
```

New text:

```
LIGHT_BASE_BYTES = 352 * 1024 * 1024
```

### `u275.M5_decode_line_dropped`

worker_bytes: drop the decode line, so a 192 kHz file costs only its length's analysis line

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M5_decode_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 549 against a baseline of 549
- Kills: 29 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-45.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-86400.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-86400.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-45.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-86400.0]`
  - ... and 14 more, see the JSON sidecar

Old text:

```
    return LIGHT_BASE_BYTES + max(analysis, decode)
```

New text:

```
    return LIGHT_BASE_BYTES + analysis
```

### `u275.M6_unknown_length_shorter`

_shape_of: bound an unknown length at fifty times the slowest rate, so not knowing plans wider than knowing

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M6_unknown_length_shorter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 549 against a baseline of 549
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_whose_length_is_unknown_costs_no_less_than_before`
  - `tests/test_analysis_ahead.py::test_a_file_whose_length_is_unknown_is_still_planned_narrower`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`

Old text:

```
            seconds = target.stat().st_size / SLOWEST_BYTES_PER_SECOND
```

New text:

```
            seconds = target.stat().st_size / (SLOWEST_BYTES_PER_SECOND * 50)
```

### `u275.M7_cheapest_track_sets_the_cost`

costliest: take the cheapest track's cost, so a folder's longest track no longer sets the plan

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M7_cheapest_track_sets_the_cost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 549 against a baseline of 549
- Kills: 13 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_eight_gigabytes_free_over_the_six_mac_tracks_is_one_worker`
  - `tests/test_analysis_ahead.py::test_one_high_rate_file_sets_the_batchs_cost_though_it_is_not_the_longest`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[12]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[18]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[24]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[32]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[4]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[64]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[6]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[8]`
  - `tests/test_analysis_ahead.py::test_the_cost_is_set_by_the_costliest_track_in_the_batch`
  - `tests/test_analysis_ahead.py::test_the_light_plan_is_never_wider_than_before_u275[12]`
  - `tests/test_analysis_ahead.py::test_the_light_plan_is_never_wider_than_before_u275[8]`

Old text:

```
    return max((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)
```

New text:

```
    return min((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)
```

### `u275.M8_analysis_line_scaled`

worker_bytes: the analysis line at three quarters of the declared slope, a coefficient mutation

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M8_analysis_line_scaled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 549 against a baseline of 549
- Kills: 18 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[376-1281]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[576-1805]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[668-2105]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[690-2162]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[729-2346]`
  - `tests/test_analysis_ahead.py::test_eight_gigabytes_free_over_the_six_mac_tracks_is_one_worker`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[12]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[18]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[24]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[32]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[4]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    analysis = int(seconds * LIGHT_BYTES_PER_SECOND)
```

New text:

```
    analysis = int(seconds * LIGHT_BYTES_PER_SECOND * 3 // 4)
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

### `r791-b.C3_summary_counts_answers`

_summary: count no answers

- File: `src/cratekit/tagging/summary.py`
- Source: `r791-b.json`, row `C3_summary_counts_answers`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
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
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
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

### `u263.D18_vocal_reason`

vocals.analyse: let a missing decoder fail the item rather than name it

- File: `src/cratekit/analysis/vocals.py`
- Source: `u263.json`, row `D18_vocal_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`, `tests/test_analysis_workers.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_the_vocal_pass_names_the_missing_decoder`

Old text:

```
    except DecoderMissing:
        return _inactive(result, REASON_NO_DECODER)
```

New text:

```
    except DecoderMissing:
        raise
```

### `u192.T1_typed_label_on_queue`

tag_folder: hand the queue's own --label to the resume, so a sweep driven at its queue says its label was not applied

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T1_typed_label_on_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_driven_at_its_queue_keeps_the_label_warning_and_never_calls_its_label_unapplied`

Old text:

```
        lambda: _resume(ctx, cfg, job.job_id, typed_label=None, queued=label_warnings),
```

New text:

```
        lambda: _resume(ctx, cfg, job.job_id, typed_label=ctx.args.label, queued=label_warnings),
```

### `u192.T2_queue_warnings_lost`

tag_folder: drop the queue's label warnings from the settled answer

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T2_queue_warnings_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_driven_at_its_queue_keeps_the_label_warning_and_never_calls_its_label_unapplied`

Old text:

```
        lambda: _resume(ctx, cfg, job.job_id, typed_label=None, queued=label_warnings),
```

New text:

```
        lambda: _resume(ctx, cfg, job.job_id, typed_label=None),
```

### `u192.T3_resume_label_unsaid`

tag_folder --job: stop passing the typed --label, so a label typed on a resume is applied silently in the report's eyes

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T3_resume_label_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`
- Collected: 166 against a baseline of 166
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_typed_on_a_resume_is_not_applied_and_says_so`
  - `tests/test_label_genre.py::test_a_label_typed_on_a_resume_is_still_said_to_be_unapplied`

Old text:

```
        return _resume(ctx, cfg, ctx.args.job, typed_label=ctx.args.label)
```

New text:

```
        return _resume(ctx, cfg, ctx.args.job, typed_label=None)
```

### `u276.K13_record_key_method_dropped`

head_agreement: leave out key_method, so the run's answer no longer says which method its key was read with

- File: `src/cratekit/analysis/detect.py`
- Source: `u276.json`, row `K13_record_key_method_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`, `tests/test_head_agreement.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_the_record_names_the_runs_method_and_the_method_its_key_was_read_with`

Old text:

```
    record["key_method"] = KEY_DEFAULT
    return record
```

New text:

```
    return record
```

### `u276.K14_record_read_with_plain`

_HEAD_AGREEMENT: say its key buckets were read with plain, which they were not

- File: `src/cratekit/analysis/detect.py`
- Source: `u276.json`, row `K14_record_read_with_plain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`, `tests/test_head_agreement.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_the_record_names_the_runs_method_and_the_method_its_key_was_read_with`

Old text:

```
    "key_read_with": "whole",
```

New text:

```
    "key_read_with": "plain",
```

### `u40-author-full.C3_resume_without_run`

Drop --run from the resume argv, so the job driver's child meets the explicit gate with nothing recorded and stalls for ever

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u40-author-full.json`, row `C3_resume_without_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`
- Collected: 70 against a baseline of 70
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_resume_argv_carries_the_folder_the_job_and_the_gate_run`
  - `tests/test_queued_resume_contract.py::test_a_queued_gated_verb_emits_the_run_its_decision_was_recorded_against[tag.retag]`
  - `tests/test_queued_resume_contract.py::test_the_resume_the_job_driver_spawns_can_actually_proceed[tag.retag]`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
```

New text:

```
    resume = []
```

### `u40-author-full.C4_resume_always_runs`

Emit --run even when no gate run is frozen, so a job from an older build hands its child an empty run identifier

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u40-author-full.json`, row `C4_resume_always_runs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_queued_resume_contract.py::test_a_payload_from_an_older_build_still_builds_a_valid_command_line[tag.retag]`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "tag", "retag", folder, "--job", job.job_id]
```

New text:

```
    return ["--run", str(gate_run), "tag", "retag", folder, "--job", job.job_id]
```

### `u294.M03_suggest_narrowed_ignores_genre`

suggest.narrowed: keep a write whatever genre it now carries, so a proposal that moved since the gate is written

- File: `src/cratekit/tagging/suggest.py`
- Source: `u294.json`, row `M03_suggest_narrowed_ignores_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_suggest.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_suggest_plan_narrowed_writes_a_row_only_with_the_genre_approved`

Old text:

```
        if keep.get(item.content_id) != item.genre
```

New text:

```
        if item.content_id not in keep
```

### `u294.M04_suggest_narrowed_changes_unfiltered`

suggest.narrowed: leave every change in the write, so a held proposal's row is written

- File: `src/cratekit/tagging/suggest.py`
- Source: `u294.json`, row `M04_suggest_narrowed_changes_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_suggest.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_suggest_plan_narrowed_writes_a_row_only_with_the_genre_approved`

Old text:

```
                change for change in plan.changes.changes if change.content_id not in held
```

New text:

```
                change for change in plan.changes.changes
```

### `u157.A1_no_level_tag`

_finalize: write no driftlevel tag

- File: `src/cratekit/analysis/cli.py`
- Source: `u157.json`, row `A1_no_level_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_analysis_workers.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_a_measured_drift_is_written_as_its_level_and_verdict`

Old text:

```
        "driftlevel": _drift_level(scored.get("drift")),
```

New text:

```
        "driftlevel": None,
```

### `u276.K1_default_is_whole`

KEY_DEFAULT: the whole track again, so every caller naming no method separates and the key reverts to the old reading

- File: `src/cratekit/analysis/detect.py`
- Source: `u276.json`, row `K1_default_is_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`, `tests/test_analysis_key_methods.py`, `tests/test_analysis_key_windows.py`, `tests/test_head_agreement.py`
- Collected: 119 against a baseline of 119
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_the_default_key_method_is_the_plain_chroma`
  - `tests/test_analysis_key_default.py::test_the_record_names_the_runs_method_and_the_method_its_key_was_read_with`
  - `tests/test_analysis_key_default.py::test_the_run_reads_the_method_that_agreed_the_most_in_the_least_time`

Old text:

```
KEY_DEFAULT = KEY_PLAIN
```

New text:

```
KEY_DEFAULT = KEY_WHOLE
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

### `u181.C3_unscored_flag_ignored`

analyze vocals: ignore --unscored, so the whole folder is queued

- File: `src/cratekit/vocals/cli.py`
- Source: `u181.json`, row `C3_unscored_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`
- Collected: 105 against a baseline of 105
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_analyze_step_rescores_after_analyze_run_and_before_the_restamp`
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_over_a_folder_whose_headed_files_all_carry_a_score_queues_nothing`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`

Old text:

```
    unscored = bool(getattr(ctx.args, "unscored", False))
```

New text:

```
    unscored = False
```

### `u94-b.W6_outcome_energy_only`

analyze_calibrate: derive the outcome from the energy half alone, so a run that replaced only the vocal cut answers no_op

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W6_outcome_energy_only`
- Moved: the calibrate verb's body moved from analysis/cli.py to analysis/calibrate.py, a file the base did not hold, and the text occurs once there
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_run_where_only_the_vocal_half_wrote_does_not_answer_no_op`

Old text:

```
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if calibrated else Outcome.NO_OP,
```

### `u244.M02_rejection_remembered`

DiscogsAsker.ask: forget a rejected token, so it is resent on every later file

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M02_rejection_remembered`
- Moved: DiscogsAsker moved verbatim from tagging/searchers.py to tagging/discogs.py, where the text occurs once, in DiscogsAsker.ask; the identical line in tagging/cyanite.py is Cyanite's own guard and not this one
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

