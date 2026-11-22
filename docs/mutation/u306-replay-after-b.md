# Mutation table: u306-replay-after-b

Measured by `scripts/mutate.py` on 2026-11-22 21:48 UTC, branch `HEAD` at `8c3c2c3a`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22940 collected. pytest invocations for this batch: 228.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `c919209162e4`, and this tree is at `8c3c2c3ad1de`).

Subset baselines: 22, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/known.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22940 against 22940. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u318.S01_track_needs_the_mix` | `src/cratekit/tagging/discogs.py` | user | 8 file(s) | 1728 | 32 | killed |
| `u318.S02_single_needs_the_mix` | `src/cratekit/tagging/discogs.py` | user | 8 file(s) | 1728 | 12 | killed |
| `u318.S03_single_track_alone` | `src/cratekit/tagging/discogs.py` | user | 8 file(s) | 1728 | 2 | killed |
| `u318.S04_miss_names_the_release` | `src/cratekit/tagging/discogs.py` | user | 8 file(s) | 1728 | 8 | killed |
| `u318.S05_fallback_found` | `src/cratekit/tagging/discogs.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u318.T01_outcome_guard` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u318.T02_empty_title_part` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u318.T03_title_of_brackets` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 5 | killed |
| `u318.T04_after_is_later` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u318.T05_later_groups` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u318.T06_later_stretch` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 3 | killed |
| `u318.T07_track_number_before` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 2 | killed |
| `u318.T08_marker_before` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u318.T09_ends_in_version_word` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 6 | killed |
| `u318.T10_credit_group` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 4 | killed |
| `u318.T11_trailing_descriptions` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 2 | killed |
| `u318.T12_leading_fold` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 3 | killed |
| `u318.T13_name_joins` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 9 | killed |
| `u318.T14_accents` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 35 | killed |
| `u318.T15_rmx` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 2 | killed |
| `u318.T16_remaster_year` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 2 | killed |
| `u318.T17_alone_strict` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 9 | killed |
| `u318.T20_middle_dash_part` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 2 | killed |
| `u318.T21_unbracketed_suffix` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 3 | killed |
| `u324-pinned.F20_initial_prefix_dropped_pinned` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 2 | killed |
| `u324.F01_entry_o_slash` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 14 | killed |
| `u324.F02_entry_O_slash` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u324.F03_entry_ae` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 7 | killed |
| `u324.F04_entry_AE` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u324.F05_entry_oe` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 5 | killed |
| `u324.F06_entry_OE` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u324.F07_entry_sharp_s` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 4 | killed |
| `u324.F08_entry_d_stroke` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 5 | killed |
| `u324.F09_entry_D_stroke` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u324.F10_entry_l_stroke` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 6 | killed |
| `u324.F11_entry_L_stroke` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u324.F12_entry_thorn` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 5 | killed |
| `u324.F13_entry_THORN` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u324.F14_o_as_oe` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 16 | killed |
| `u324.F15_no_table` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 39 | killed |
| `u324.F16_table_before_nfkd` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 2 | killed |
| `u324.F17_table_letter_no_initial` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 4 | killed |
| `u324.F18_written_length_initial` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 1 | killed |
| `u324.F19_no_initials` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 7 | killed |
| `u324.F21_folded_credit_words` | `src/cratekit/tagging/titles.py` | user | 8 file(s) | 1728 | 4 | killed |
| `u245.M01_opt_in` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 3 | killed |
| `u245.M02_cap_required` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 1 | killed |
| `u245.M03_cap_bound` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 6 | killed |
| `u245.M04_cap_counts_uploads` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 1 | killed |
| `u245.M06_price_required` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 1 | killed |
| `u245.M07_digest_without_tags` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 1 | killed |
| `u245.M08_never_overwrite` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 2 | killed |
| `u245.M09_resume_skips_answered` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 4 | killed |
| `u245.M10_resume_asks_again` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 2 | killed |
| `u245.M11_track_written_ahead` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 4 | killed |
| `u245.M12_digest_identity` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 5 | killed |
| `u245.M13_same_audio_once` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 1 | killed |
| `u245.M14_mp3_only` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 26 | killed |
| `u245.M15_scrub` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 4 | killed |
| `u245.M16_cells_scrubbed` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 1 | killed |
| `u245.M17_key_to_upload` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 1 | killed |
| `u245.M18_rejected_remembered` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 1 | killed |
| `u245.M19_401_rejected` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 2 | killed |
| `u245.M20_graphql_errors` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 4 | killed |
| `u245.M21_https_upload` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 1 | killed |
| `u245.M22_library_full_stops` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 2 | killed |
| `u245.M23_not_started_stops` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 2 | killed |
| `u245.M24_unread_not_a_disagreement` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 6 | killed |
| `u245.M25_share_leaves_out_unplaced` | `src/cratekit/tagging/cyanite.py` | user | 1 file(s) | 78 | 1 | killed |
| `u240.M11_needle_is_the_name` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 2 | killed |
| `u240.M12_raw_line_matched` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 2 | killed |
| `u240.M13_two_way_match` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 7 | killed |
| `u240.M14_widest_any` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 1 | killed |
| `u240.M15_no_widest_rule` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 1 | killed |
| `u240.M16_genres_joined_by_name` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 1 | killed |
| `u240.M17_worker_hands_no_seam` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 8 | killed |
| `u240.M18_way_inverted` | `src/cratekit/tagging/summary.py` | user | 5 file(s) | 334 | 3 | killed |
| `u240.M19_one_name_ambiguous` | `src/cratekit/tagging/summary.py` | user | 5 file(s) | 334 | 2 | killed |
| `u240.M20_warning_dropped` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 1 | killed |
| `u240.M21_failed_sweep_unreported` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 3 | killed |
| `u240.M22_failed_items_left_out` | `src/cratekit/tagging/summary.py` | user | 5 file(s) | 334 | 3 | killed |
| `u240.M23_cap_lowered` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 334 | 1 | killed |
| `u240.M1_two_names_take_the_first` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 4 | killed |
| `u240.M2_no_genre_label_named` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 4 | killed |
| `u240.M3_tag_no_longer_outranks_the_line` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 17 | killed |
| `u240.M4_folder_label_no_longer_outranks_the_line` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 9 | killed |
| `u240.M5_wrong_field_read` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 11 | killed |
| `u240.M6_named_by_lost` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 5 | killed |
| `u240.M7_line_labels_dropped_from_result` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 3 | killed |
| `u240.M8_failed_files_line_dropped` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 1 | killed |
| `u240.M9_park_flattened` | `src/cratekit/tagging/tag.py` | user | 5 file(s) | 334 | 1 | killed |
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
| `r816-b.B3_blank_spellings` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 3 | killed |
| `r816-b.B4_restore_detection` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-c.B6_bookkeeping_exempt` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 10 | killed |
| `r816-c.B7_read_back_word` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-c.B8_read_back_columns` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-c.B9_cache_reset` | `src/cratekit/tagging/rows.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C1_acknowledgment` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C4_only_apply_writes` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 1 | killed |
| `r816-d.C5_leave_reaches_the_plan` | `src/cratekit/tagging/rows_cli.py` | user | 1 file(s) | 72 | 2 | killed |
| `r289-a.A1_appledouble_gone` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r289-a.A2_appledouble_one_dot` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r289-a.A3_staging_dirs_gone` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 4 | killed |
| `r289-a.A4_staging_dirs_acquire_only` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 2 | killed |
| `r289-a.A5_staging_dirs_absolute` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r650-a.B3_engine_drops_the_flag_on_the_write` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 3 | killed |
| `r650-a.B4_engine_leaks_the_flag_onto_a_skip` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R14_walk_unsorted` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 7 | killed |
| `u56-catalogue-searcher-and-tag-workers.R15_walk_not_recursive` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 4 | killed |
| `u85-a.A11_failed_write_is_error` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u85-a.A13_art_only_refusal_absorbed` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 2 | killed |
| `u85-a.A1_search_skipped_only_with_both` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 11 | killed |
| `u85-a.A2_any_picture_settles` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 8 | killed |
| `u85-a.A3_unreadable_is_unchecked` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u85-a.A5_no_url_guard` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 141 | 1 | killed |
| `u85-a.A6_no_fetch_guard` | `src/cratekit/tagging/tag.py` | maintainer | 4 file(s) | 242 | 1 | killed |
| `u85-a.A7_fetch_raise_is_a_decline` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u85-a.A9_not_a_picture_is_a_decline` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u25-author-light.G1_resume_prefix` | `src/cratekit/analysis/run.py` | user | 1 file(s) | 17 | 1 | killed |
| `sitting3.G10_lone_clip_not_padded` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 3 | killed |
| `sitting3.G11_tail_dropped` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 2 | killed |
| `sitting3.G13_padded_frames_kept` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 1 | killed |
| `sitting3.G14_unchunked_floor_is_width` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 1 | killed |
| `sitting3.G15_fold_any_ragged_tail` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 3 | killed |
| `sitting3.G1_columns_by_number` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 4 | killed |
| `sitting3.G2_missing_target_read_as_fixture` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 2 | killed |
| `sitting3.G4_clip_wrapper` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 1 | killed |
| `sitting3.G5_loader_skips_readiness` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 1 | killed |
| `sitting3.G7_chatter_on_stdout` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 1 | killed |
| `sitting3.G9_tail_sent_alone` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 5 | killed |
| `u25-author-light.G3_unchunked_only` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 17 | 4 | killed |
| `sitting3.G12_columns_per_track` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 17 | 1 | killed |
| `u260.F10_fetch_memory_one` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 2 | killed |
| `u260.F11_reset_images_forgets_nothing` | `src/cratekit/tagging/searchers.py` | maintainer | 4 file(s) | 263 | 9 | killed |
| `u260.F1_fetch_never_answers_from_memory` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 10 | killed |
| `u260.F2_empty_answer_remembered` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 1 | killed |
| `u260.F3_admission_ignored` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 2 | killed |
| `u260.F4_binder_admits_everything` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 1 | killed |
| `u260.F5_binder_builds_per_call` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 8 | killed |
| `u260.F6_fetch_bound_off_by_one` | `src/cratekit/tagging/searchers.py` | maintainer | 4 file(s) | 263 | 1 | killed |
| `u260.F7_fetch_evicts_newest` | `src/cratekit/tagging/searchers.py` | maintainer | 4 file(s) | 263 | 1 | killed |
| `u260.F8_fetch_hit_not_refreshed` | `src/cratekit/tagging/searchers.py` | maintainer | 4 file(s) | 263 | 1 | killed |
| `u260.F9_fetch_memory_unbounded` | `src/cratekit/tagging/searchers.py` | maintainer | 4 file(s) | 263 | 1 | killed |
| `r1103.S1_answer_too_coarse` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 4 | killed |
| `r1103.S2_rejected_verdict` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 2 | killed |
| `r1103.S3_written_property` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 6 | killed |
| `r1103.W1_writer_answer_ignored` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 6 | killed |
| `r1103.W2_unwritten_reason_blank` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 5 | killed |
| `r1103.W3_unwritten_reason_wrong` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 5 | killed |
| `r1103.W4_unwritten_proposed_dropped` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 4 | killed |
| `r1103.W5_unwritten_claims_written` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 3 | killed |
| `r1103.W6_unwritten_current_swapped` | `src/cratekit/tagging/retag.py` | user | 3 file(s) | 222 | 2 | killed |
| `r744.A1_near_miss_widened` | `src/cratekit/analysis/agreement.py` | maintainer | 1 file(s) | 65 | 5 | killed |
| `r744.A2_half_not_recognised` | `src/cratekit/analysis/agreement.py` | maintainer | 1 file(s) | 65 | 4 | killed |
| `r744.A3_classic_names_unmapped` | `src/cratekit/analysis/agreement.py` | user | 1 file(s) | 65 | 18 | killed |
| `r744.A4_whole_number_counts_as_rekordbox` | `src/cratekit/analysis/agreement.py` | maintainer | 1 file(s) | 65 | 2 | killed |
| `r744.A5_removed_rows_counted` | `src/cratekit/analysis/agreement.py` | user | 1 file(s) | 65 | 2 | killed |
| `r744.A6_sample_never_full` | `src/cratekit/analysis/agreement.py` | maintainer | 1 file(s) | 65 | 1 | killed |
| `r744.E8_record_applies_to_every_window` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 65 | 1 | killed |
| `r744.E9_record_does_not_sum` | `src/cratekit/analysis/detect.py` | maintainer | 1 file(s) | 65 | 1 | killed |
| `u283.D1_shape_sent` | `src/cratekit/tagging/discogs.py` | user | 3 file(s) | 200 | 4 | killed |
| `u283.D2_401_unchecked` | `src/cratekit/tagging/discogs.py` | user | 3 file(s) | 200 | 4 | killed |
| `u283.D3_reraise_swallowed` | `src/cratekit/tagging/discogs.py` | maintainer | 3 file(s) | 200 | 1 | killed |
| `u283.D4_any_object_accepted` | `src/cratekit/tagging/discogs.py` | user | 3 file(s) | 200 | 3 | killed |
| `u283.D5_id_truthy` | `src/cratekit/tagging/discogs.py` | user | 3 file(s) | 200 | 2 | killed |
| `u283.D6_said_unscrubbed` | `src/cratekit/tagging/discogs.py` | user | 3 file(s) | 200 | 2 | killed |
| `u283.D7_check_unpaced_sleep` | `src/cratekit/tagging/searchers.py` | maintainer | 3 file(s) | 200 | 1 | killed |
| `u283.D8_identity_address` | `src/cratekit/tagging/discogs.py` | user | 3 file(s) | 200 | 1 | killed |
| `u284.R1_since_moves_every_refusal` | `src/cratekit/tagging/refused.py` | user | 1 file(s) | 35 | 3 | killed |
| `u284.R2_an_answer_never_clears` | `src/cratekit/tagging/refused.py` | user | 1 file(s) | 35 | 2 | killed |
| `u284.R3_write_without_the_lock` | `src/cratekit/tagging/refused.py` | maintainer | 1 file(s) | 35 | 1 | killed |
| `u284.R4_empty_since_read` | `src/cratekit/tagging/refused.py` | maintainer | 1 file(s) | 35 | 1 | killed |
| `u284.R5_count_never_grows` | `src/cratekit/tagging/refused.py` | maintainer | 1 file(s) | 35 | 2 | killed |
| `u284.R6_write_failure_raises` | `src/cratekit/tagging/refused.py` | user | 1 file(s) | 35 | 1 | killed |
| `u284.R7_deep_record_raises` | `src/cratekit/tagging/refused.py` | user | 1 file(s) | 35 | 1 | killed |
| `u276.K12_stream_worker_binding_names_whole` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 24 | 2 | killed |
| `u276.K11_run_binding_names_whole` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `u276.K15_warm_up_names_whole` | `src/cratekit/analysis/warm.py` | maintainer | 1 file(s) | 24 | 1 | killed |
| `u276.K2_profile_default_whole` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 54 | 1 | killed |
| `u276.K3_analyse_file_default_whole` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 54 | 1 | killed |
| `u294.M01_rows_narrowed_keeps_all` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 128 | 11 | killed |
| `u294.M02_rows_narrowed_changes_unfiltered` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 128 | 21 | killed |
| `u294.M23_rows_read_back` | `src/cratekit/tagging/rows_cli.py` | user | 2 file(s) | 128 | 1 | killed |
| `u40-author-full.C1_gate_by_position` | `src/cratekit/tagging/retag_cli.py` | user | 3 file(s) | 1067 | 1 | killed |
| `u40-author-full.C2_no_gate_no_refusal` | `src/cratekit/tagging/retag_cli.py` | user | 3 file(s) | 1067 | 1 | killed |
| `u281.S3_challenge_header_case` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 204 | 1 | killed |
| `u281.S4_any_mitigation_is_a_challenge` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 204 | 1 | killed |
| `r744.B1_window_not_bound` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 237 | 1 | killed |
| `u181.V2_torch_failure_kind` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 451 | 1 | killed |
| `r1103.H1_item_not_failed` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 152 | 3 | killed |
| `u114.M18_narrow_called` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 131 | 21 | killed |
| `u260.E1_engine_encodes_per_file` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 196 | 8 | killed |
| `r816-d.C2_empty_plan` | `src/cratekit/tagging/plan_verbs.py` | user | 1 file(s) | 72 | 2 | killed |
| `r816-d.C3_majority_unmapped` | `src/cratekit/tagging/plan_verbs.py` | user | 1 file(s) | 72 | 1 | killed |

## Row definitions

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

### `u318.S02_single_needs_the_mix`

_release_carries: the single fallback counts whatever the release writes

- File: `src/cratekit/tagging/discogs.py`
- Source: `u318.json`, row `S02_single_needs_the_mix`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 12 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_refused_release_gives_way_to_a_later_one_that_carries_the_mix`
  - `tests/test_discogs_version.py::test_an_unread_release_beside_a_version_refusal_is_unread_not_a_miss`
  - `tests/test_discogs_version.py::test_the_miss_names_a_release_refused_on_its_tracks_alone_or_its_title_alone`
  - `tests/test_discogs_version.py::test_the_miss_names_every_release_refused_for_its_version_and_no_other`
  - `tests/test_discogs_version.py::test_the_mita_gami_extended_mix_refuses_the_16bl_remix_single`
  - `tests/test_discogs_version.py::test_the_refused_file_is_left_untagged_with_the_reason_in_its_record`
  - `tests/test_discogs_version.py::test_the_single_fallback_reads_no_other_track_of_the_release_as_the_mix`
  - `tests/test_discogs_version.py::test_the_single_fallback_refuses_a_remix_on_a_one_track_release_of_the_title`
  - `tests/test_discogs_version.py::test_the_single_fallback_takes_a_release_whose_own_title_writes_the_version`
  - `tests/test_discogs_version.py::test_the_single_fallback_takes_a_release_whose_track_is_the_version_alone`
  - `tests/test_discogs_version.py::test_the_sitting_files_headed_as_the_library_writes_them_refuse_too`
  - `tests/test_discogs_version.py::test_the_tim_green_remix_refuses_a_release_of_four_other_mixes`

Old text:

```
        if (
            not named
            or titles.writes_version(release.title, named, titled=True)
```

New text:

```
        if (
            True
            or titles.writes_version(release.title, named, titled=True)
```

### `u318.S03_single_track_alone`

_release_carries: the single fallback reads no track that is the mix alone, so a single titled X with a track A Remix refuses X (A Remix)

- File: `src/cratekit/tagging/discogs.py`
- Source: `u318.json`, row `S03_single_track_alone`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_the_single_fallback_reads_no_other_track_of_the_release_as_the_mix`
  - `tests/test_discogs_version.py::test_the_single_fallback_takes_a_release_whose_track_is_the_version_alone`

Old text:

```
            or any(titles.writes_version(track, named, titled=False) for track, _ in release.tracks)
```

New text:

```
            or False
```

### `u318.S04_miss_names_the_release`

_search: never record a release refused for its version, so the miss carries no note

- File: `src/cratekit/tagging/discogs.py`
- Source: `u318.json`, row `S04_miss_names_the_release`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 8 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_plain_miss_still_carries_no_note`
  - `tests/test_discogs_version.py::test_a_title_naming_two_mixes_lists_them_in_order_in_the_note`
  - `tests/test_discogs_version.py::test_another_maker_is_still_a_version_miss_with_the_note`
  - `tests/test_discogs_version.py::test_the_miss_names_a_release_refused_on_its_tracks_alone_or_its_title_alone`
  - `tests/test_discogs_version.py::test_the_miss_names_every_release_refused_for_its_version_and_no_other`
  - `tests/test_discogs_version.py::test_the_mita_gami_extended_mix_refuses_the_16bl_remix_single`
  - `tests/test_discogs_version.py::test_the_refused_file_is_left_untagged_with_the_reason_in_its_record`
  - `tests/test_discogs_version.py::test_the_tim_green_remix_refuses_a_release_of_four_other_mixes`

Old text:

```
            if carries is _Carries.ANOTHER_VERSION:
                refused_version.append(number)
```

New text:

```
            if carries is _Carries.NO:
                refused_version.append(number)
```

### `u318.S05_fallback_found`

_release_carries: a single refused on its title alone is no version refusal, so its miss names nothing

- File: `src/cratekit/tagging/discogs.py`
- Source: `u318.json`, row `S05_fallback_found`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_the_miss_names_a_release_refused_on_its_tracks_alone_or_its_title_alone`

Old text:

```
            return _Carries.YES
        found = True
    return _Carries.ANOTHER_VERSION if found else _Carries.NO
```

New text:

```
            return _Carries.YES
    return _Carries.ANOTHER_VERSION if found else _Carries.NO
```

### `u318.T01_outcome_guard`

named_versions: read a version off an ambiguous name too, not only a titled one

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T01_outcome_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_what_a_title_names_as_its_mix[Fixture Artist - Vocal Mix (Tide Remix)-Fixture Artist-named2]`

Old text:

```
    if file.outcome is not Outcome.TITLED:
        return frozenset()
    named: set[Words] = set()
```

New text:

```
    if file.outcome is Outcome.UNREADABLE:
        return frozenset()
    named: set[Words] = set()
```

### `u318.T02_empty_title_part`

named_versions: read a version after a title part that names nothing, so 08A - 124 -  - Sunrise Mood Extended Mix names sunrise mood

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T02_empty_title_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_files_named_versions[08A - 124 -  - Sunrise Mood Extended Mix-named32]`

Old text:

```
        if part.role is not Role.TITLE or not identifies(part.text):
```

New text:

```
        if part.role is not Role.TITLE:
```

### `u318.T03_title_of_brackets`

named_versions: read the title part's groups without the title rule, so (Sunrise Mood Extended Mix) names its own title as a mix

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T03_title_of_brackets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_files_named_versions[(Kerri Chandler Remix) - Original Mix-named25]`
  - `tests/test_discogs_version.py::test_a_files_named_versions[(Sunrise Mood Extended Mix)-named24]`
  - `tests/test_discogs_version.py::test_a_files_named_versions[02 (Sunrise Mood Extended Mix)-named27]`
  - `tests/test_discogs_version.py::test_a_files_named_versions[Fixture Artist - Sun Path - 02 (Sunrise Mood Extended Mix)-named29]`
  - `tests/test_discogs_version.py::test_a_files_named_versions[[MP3] (Sunrise Mood Extended Mix)-named28]`

Old text:

```
        named |= _group_versions(part.text, title=True)
```

New text:

```
        named |= _group_versions(part.text)
```

### `u318.T04_after_is_later`

named_versions: read the part after the title as its version whatever its role, an artist's credit included

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T04_after_is_later`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_what_a_title_names_as_its_mix[Two Months Off - Culture Club - Album-Culture Club-named0]`

Old text:

```
        if after is not None and after.role is Role.LATER:
```

New text:

```
        if after is not None:
```

### `u318.T05_later_groups`

named_versions: drop the bracket groups of the dash part after the title

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T05_later_groups`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_what_a_title_names_as_its_mix[Two Months Off - Extended Mix (Tim Green Remix)-Fixture Artist-named1]`

Old text:

```
            named |= _group_versions(after.text)
            if own := _stretch_version(after.text):
```

New text:

```
            if own := _stretch_version(after.text):
```

### `u318.T06_later_stretch`

named_versions: drop the dash tail version, so Two Months Off - Tim Green Remix names nothing

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T06_later_stretch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_files_named_versions[Two Months Off - Tim Green Remix (Extended)-named4]`
  - `tests/test_discogs_version.py::test_a_files_named_versions[Two Months Off - Tim Green Remix-named3]`
  - `tests/test_discogs_version.py::test_another_version_or_none_takes_nothing[X - A Remix-X]`

Old text:

```
            if own := _stretch_version(after.text):
```

New text:

```
            if own := tuple():
```

### `u318.T07_track_number_before`

_a_title_before: a lone track number counts as a title, so 02 (Sunrise Mood Extended Mix) names a mix

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T07_track_number_before`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_files_named_versions[02 (Sunrise Mood Extended Mix)-named27]`
  - `tests/test_discogs_version.py::test_a_files_named_versions[Fixture Artist - Sun Path - 02 (Sunrise Mood Extended Mix)-named29]`

Old text:

```
    return identifies(rest) and not _a_track_number(rest)
```

New text:

```
    return identifies(rest)
```

### `u318.T08_marker_before`

_a_title_before: the naming verb's marker counts as a title, so [MP3] (Sunrise Mood Extended Mix) names a mix

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T08_marker_before`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_files_named_versions[[MP3] (Sunrise Mood Extended Mix)-named28]`

Old text:

```
    rest = _MARKER.sub("", before, count=1).strip()
```

New text:

```
    rest = before.strip()
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
  - `tests/test_title_matcher.py::test_a_files_title_among_its_dash_parts_still_finds_its_own_row[08A - 124 - Make Luv - Room 5-Make Luv]`
  - `tests/test_title_matcher.py::test_discogs_still_matches_a_title_to_its_own_track[08A - 124 - Make Luv - Room 5-Make Luv]`

Old text:

```
    if not found or not _a_kind_word(found, len(found) - 1) or found[0] in _CREDITS:
```

New text:

```
    if not found or found[0] in _CREDITS:
```

### `u318.T10_credit_group`

_naming_words: drop the credit test, so (feat. Tom Tom Club) is read as a mix (fix round two)

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T10_credit_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_credit_group_ending_in_a_version_word_is_no_version[feat. Culture Club]`
  - `tests/test_discogs_version.py::test_a_credit_group_ending_in_a_version_word_is_no_version[feat. Tom Tom Club]`
  - `tests/test_discogs_version.py::test_a_credit_group_ending_in_a_version_word_is_no_version[ft. Amp Live]`
  - `tests/test_discogs_version.py::test_a_credit_group_ending_in_a_version_word_is_no_version[with Bombay Bicycle Club]`

Old text:

```
    if not found or not _a_kind_word(found, len(found) - 1) or found[0] in _CREDITS:
```

New text:

```
    if not found or not _a_kind_word(found, len(found) - 1):
```

### `u318.T11_trailing_descriptions`

_naming_words: fold only version words off the end, never a description, so LP Version names lp (round one's BLOCKING)

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T11_trailing_descriptions`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_files_named_versions[Two Months Off (Tim Green Vocal Mix)-named17]`
  - `tests/test_discogs_version.py::test_a_named_mix_after_a_description_still_names_its_maker`

Old text:

```
    while end and _a_mix_word(found, end - 1):
```

New text:

```
    while end and _a_kind_word(found, end - 1):
```

### `u318.T12_leading_fold`

_naming_words: fold nothing off the front, so Extended Tim Green Remix names extended tim green

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T12_leading_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_files_named_versions[Two Months Off (Extended Tim Green Remix)-named7]`
  - `tests/test_discogs_version.py::test_a_maker_is_folded_as_a_name_is[Sunrise Mood (Main Tim Green Mix)-Sunrise Mood (Tim Green Remix)]`
  - `tests/test_discogs_version.py::test_what_a_title_names_as_its_mix[Two Months Off (Main Tim Green Mix)-Fixture Artist-named4]`

Old text:

```
    while start < end and _a_mix_word(found, start):
```

New text:

```
    while start < end and False:
```

### `u318.T13_name_joins`

_naming_words: keep and, the and a possessive s in a maker's name

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T13_name_joins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 9 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off (Tim Green's Remix)-True-False]`
  - `tests/test_discogs_version.py::test_a_files_named_versions[Two Months Off (Mike's (Dub) Mix)-named18]`
  - `tests/test_discogs_version.py::test_a_maker_is_folded_as_a_name_is[Sunrise Mood (Tide & Sun Remix)-Sunrise Mood (Tide And Sun Remix)]`
  - `tests/test_discogs_version.py::test_a_maker_is_folded_as_a_name_is[Sunrise Mood (Tim Green's Remix)-Sunrise Mood (Tim Green Remix)]`
  - `tests/test_discogs_version.py::test_an_article_is_folded_out_of_a_makers_name_on_both_sides`
  - `tests/test_discogs_version.py::test_an_article_names_no_maker[The Original Mix]`
  - `tests/test_discogs_version.py::test_an_article_names_no_maker[The Radio Edit]`
  - `tests/test_discogs_version.py::test_an_article_names_no_maker[The Remix]`
  - `tests/test_discogs_version.py::test_what_a_title_names_as_its_mix[Two Months Off (Tim Green's Remix)-Fixture Artist-named5]`

Old text:

```
    return tuple(_folded(word) for word in found[start:end] if word not in _NAME_JOINS)
```

New text:

```
    return tuple(_folded(word) for word in found[start:end])
```

### `u318.T14_accents`

_naming_words: keep a maker's accents, so Ame and Âme are two makers

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T14_accents`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 35 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[Stra\xdfe-Strasse]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[TRENTEM\xd8LLER-Trentemoller]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[Trentem\xf8ller-Trentemoller]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0110OR\u0110E-Dorde]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0110or\u0111e-Dorde]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0141ukasz-Lukasz]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0142ukasz-Lukasz]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0152uvre-Oeuvre]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0153uvre-Oeuvre]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xc6ther-Aether]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xde\xf3r-Thor]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xe6ther-Aether]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xfe\xf3r-Thor]`
  - `tests/test_discogs_version.py::test_a_letter_that_also_carries_an_accent_is_read_plain`
  - `tests/test_discogs_version.py::test_a_maker_is_folded_as_a_name_is[Sunrise Mood (Ame Remix)-Sunrise Mood (\xc2me Remix)]`
  - ... and 20 more, see the JSON sidecar

Old text:

```
    return tuple(_folded(word) for word in found[start:end] if word not in _NAME_JOINS)
```

New text:

```
    return tuple(word for word in found[start:end] if word not in _NAME_JOINS)
```

### `u318.T15_rmx`

_VERSION_SPELLINGS: drop rmx, so Tim Green Rmx is no version

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T15_rmx`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off (Tim Green Rmx)-True-False]`
  - `tests/test_discogs_version.py::test_a_maker_is_folded_as_a_name_is[Sunrise Mood (Tim Green Remix)-Sunrise Mood (Tim Green Rmx)]`

Old text:

```
_VERSION_SPELLINGS = frozenset({"rmx", "remixed"})
```

New text:

```
_VERSION_SPELLINGS = frozenset({"remixed"})
```

### `u318.T16_remaster_year`

_a_mix_word: fold no year away from a remaster, so 2009 Digital Remaster names 2009

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T16_remaster_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_mix_of_the_same_recording_still_takes_the_album_track[2009 Digital Remaster]`
  - `tests/test_discogs_version.py::test_what_a_title_names_as_its_mix[Two Months Off (2009 Digital Remaster)-Fixture Artist-named6]`

Old text:

```
    return _YEAR.fullmatch(found[index]) is not None and not _REMASTER.isdisjoint(found)
```

New text:

```
    return False
```

### `u318.T17_alone_strict`

writes_version untitled: read any group of the row too, so a single's other title's remix Sun Path (Tide Remix) counts (round one's finding 6)

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T17_alone_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 9 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Sun Path (Tim Green Remix)-True-False]`
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off (TIM GREEN REMIX)-True-False]`
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off (Tim Green Dub)-True-False]`
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off (Tim Green Remix) (Extended)-True-False]`
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off (Tim Green Remix)-True-False]`
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off (Tim Green Rmx)-True-False]`
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off (Tim Green's Remix)-True-False]`
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off [Tim Green Remix]-True-False]`
  - `tests/test_discogs_version.py::test_the_single_fallback_reads_no_other_track_of_the_release_as_the_mix`

Old text:

```
        return bool(named & alone)
```

New text:

```
        return bool(named & (alone | _group_versions(text)))
```

### `u318.T20_middle_dash_part`

writes_version titled: read dash suffixes only, so a three part row written as the file is refused (round one's finding 9)

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T20_middle_dash_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off - Tim Green Remix - Part 2-True-False]`
  - `tests/test_discogs_version.py::test_a_row_written_as_the_file_is_written_matches_whatever_its_dash_parts`

Old text:

```
        written |= {_stretch_version(DASH.join(parts[first:])), _stretch_version(parts[first])}
```

New text:

```
        written |= {_stretch_version(DASH.join(parts[first:]))}
```

### `u318.T21_unbracketed_suffix`

writes_version titled: drop the suffix rule, so a track Two Months Off Tim Green Remix writes nothing

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T21_unbracketed_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Lost And Found Tim Green Dub-True-False]`
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off Tim Green Remix-True-False]`
  - `tests/test_discogs_version.py::test_a_version_is_read_as_the_reader_reads_it_wherever_it_is_written[X (A Remix)-X A Remix]`

Old text:

```
    return any(len(whole) > len(name) and whole[-len(name) :] == name for name in named)
```

New text:

```
    return False
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
  - `tests/test_title_matcher.py::test_a_folded_name_is_no_wider_than_its_letters[Bernard Badie-08A - 124 - C. Badie - Sun Path-Sun Path]`
  - `tests/test_title_matcher.py::test_a_folded_name_is_no_wider_than_its_letters[\xde\xf3r\xf0ur Badie-08A - 124 - \xc6. Badie - Sun Path-Sun Path]`

Old text:

```
        return mine == theirs or (initial(index) and theirs.startswith(mine))
```

New text:

```
        return mine == theirs or initial(index)
```

### `u324.F01_entry_o_slash`

_PLAIN_SPELLINGS: delete the ø entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F01_entry_o_slash`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 14 (killed)
- Killed:
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

Old text:

```
        "ø": "o",

```

New text:

```
(empty)
```

### `u324.F02_entry_O_slash`

_PLAIN_SPELLINGS: delete the Ø entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F02_entry_O_slash`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`

Old text:

```
        "Ø": "o",

```

New text:

```
(empty)
```

### `u324.F03_entry_ae`

_PLAIN_SPELLINGS: delete the æ entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F03_entry_ae`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 7 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xc6ther-Aether]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xe6ther-Aether]`
  - `tests/test_discogs_version.py::test_a_letter_that_also_carries_an_accent_is_read_plain`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\xc6ther-Aether]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\xe6ther-Aether]`
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xc6ther-08A - 124 - [MP3] Aether - Sun Path-Aether-Sun Path]`

Old text:

```
        "æ": "ae",

```

New text:

```
(empty)
```

### `u324.F04_entry_AE`

_PLAIN_SPELLINGS: delete the Æ entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F04_entry_AE`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`

Old text:

```
        "Æ": "ae",

```

New text:

```
(empty)
```

### `u324.F05_entry_oe`

_PLAIN_SPELLINGS: delete the œ entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F05_entry_oe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0152uvre-Oeuvre]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0153uvre-Oeuvre]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\u0152uvre-Oeuvre]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\u0153uvre-Oeuvre]`
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`

Old text:

```
        "œ": "oe",

```

New text:

```
(empty)
```

### `u324.F06_entry_OE`

_PLAIN_SPELLINGS: delete the Œ entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F06_entry_OE`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`

Old text:

```
        "Œ": "oe",

```

New text:

```
(empty)
```

### `u324.F07_entry_sharp_s`

_PLAIN_SPELLINGS: delete the ß entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F07_entry_sharp_s`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[Stra\xdfe-Strasse]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[Stra\xdfe-Strasse]`
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[Stra\xdfe Bloom-08A - 124 - Strasse Bloom - Sun Path-Strasse Bloom-Sun Path]`

Old text:

```
        "ß": "ss",

```

New text:

```
(empty)
```

### `u324.F08_entry_d_stroke`

_PLAIN_SPELLINGS: delete the đ entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F08_entry_d_stroke`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0110OR\u0110E-Dorde]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0110or\u0111e-Dorde]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\u0110OR\u0110E-Dorde]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\u0110or\u0111e-Dorde]`
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`

Old text:

```
        "đ": "d",

```

New text:

```
(empty)
```

### `u324.F09_entry_D_stroke`

_PLAIN_SPELLINGS: delete the Đ entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F09_entry_D_stroke`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`

Old text:

```
        "Đ": "d",

```

New text:

```
(empty)
```

### `u324.F10_entry_l_stroke`

_PLAIN_SPELLINGS: delete the ł entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F10_entry_l_stroke`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 6 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0141ukasz-Lukasz]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0142ukasz-Lukasz]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\u0141ukasz-Lukasz]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\u0142ukasz-Lukasz]`
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\u0141ukasz Bloom-08A - 124 - Lukasz Bloom & Tide - Sun Path-Lukasz Bloom & Tide-Lukasz Bloom & Tide - Sun Path]`

Old text:

```
        "ł": "l",

```

New text:

```
(empty)
```

### `u324.F11_entry_L_stroke`

_PLAIN_SPELLINGS: delete the Ł entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F11_entry_L_stroke`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`

Old text:

```
        "Ł": "l",

```

New text:

```
(empty)
```

### `u324.F12_entry_thorn`

_PLAIN_SPELLINGS: delete the þ entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F12_entry_thorn`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xde\xf3r-Thor]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xfe\xf3r-Thor]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\xde\xf3r-Thor]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\xfe\xf3r-Thor]`
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`

Old text:

```
        "þ": "th",

```

New text:

```
(empty)
```

### `u324.F13_entry_THORN`

_PLAIN_SPELLINGS: delete the Þ entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F13_entry_THORN`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`

Old text:

```
        "Þ": "th",

```

New text:

```
(empty)
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

### `u324.F15_no_table`

_folded: drop the table, the fold main had

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F15_no_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 39 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[Stra\xdfe-Strasse]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[TRENTEM\xd8LLER-Trentemoller]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[Trentem\xf8ller-Trentemoller]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0110OR\u0110E-Dorde]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0110or\u0111e-Dorde]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0141ukasz-Lukasz]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0142ukasz-Lukasz]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0152uvre-Oeuvre]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0153uvre-Oeuvre]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xc6ther-Aether]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xde\xf3r-Thor]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xe6ther-Aether]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xfe\xf3r-Thor]`
  - `tests/test_discogs_version.py::test_a_letter_that_also_carries_an_accent_is_read_plain`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[Stra\xdfe-Strasse]`
  - ... and 24 more, see the JSON sidecar

Old text:

```
    return _unaccented(word).translate(_PLAIN_LETTERS)
```

New text:

```
    return _unaccented(word)
```

### `u324.F16_table_before_nfkd`

_folded: read the table before the accents come off, so ǿ keeps its ø

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F16_table_before_nfkd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_letter_that_also_carries_an_accent_is_read_plain`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xc6sir Badie-08A - 124 - \u01fc. Badie - Sun Path-\u01fc Badie-\u01fc. Badie - Sun Path]`

Old text:

```
    return _unaccented(word).translate(_PLAIN_LETTERS)
```

New text:

```
    return _unaccented(word.translate(_PLAIN_LETTERS))
```

### `u324.F17_table_letter_no_initial`

_runs_in: judge an initial on its folded length, so Þ. no longer stands for Þórður

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F17_table_letter_no_initial`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 4 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\u01e2sir Badie-08A - 124 - \u01e2. Badie - Sun Path-\u01e2 Badie-\u01e2. Badie - Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xc6sir Badie-08A - 124 - \u01fc. Badie - Sun Path-\u01fc Badie-\u01fc. Badie - Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xc6sop Badie-08A - 124 - \xc6. Badie - Sun Path-\xc6 Badie-\xc6. Badie - Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xde\xf3r\xf0ur Badie-08A - 124 - \xde. Badie - Sun Path-\xde Badie-\xde. Badie - Sun Path]`

Old text:

```
        return written is not None and len(_unaccented(written[index])) == 1
```

New text:

```
        return written is not None and len(inner[index]) == 1
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
  - `tests/test_title_matcher.py::test_a_folded_name_is_no_wider_than_its_letters[Ijsbrand Badie-08A - 124 - \u0132. Badie - Sun Path-Sun Path]`

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
  - `tests/test_title_matcher.py::test_each_way_a_credit_is_written_is_known[Bernard Badie-08A - 124 - B. Badie - Sun Path-Sun Path]`
  - `tests/test_title_matcher.py::test_every_name_the_naming_verb_renders_finds_its_own_row_and_no_other`
  - `tests/test_title_matcher.py::test_what_is_not_the_artists_credit_is_never_passed_over[Bernard Badie-08A - 124 - B. Badie - Sun Path-B Badie]`

Old text:

```
    return len(folded) > 1 and any(_runs_in(folded, name, written=written) for name in names)
```

New text:

```
    return len(folded) > 1 and any(_runs_in(folded, name) for name in names)
```

### `u324.F21_folded_credit_words`

_names_the_artist: compare a run of the credit's written words rather than its folded ones

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F21_folded_credit_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`, `tests/test_title_matcher.py`, `tests/test_discogs_question.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 1728 against a baseline of 1728
- Kills: 4 (killed)
- Killed:
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\u01e2sir Badie-08A - 124 - \u01e2. Badie - Sun Path-\u01e2 Badie-\u01e2. Badie - Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xc6sir Badie-08A - 124 - \u01fc. Badie - Sun Path-\u01fc Badie-\u01fc. Badie - Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xc6sop Badie-08A - 124 - \xc6. Badie - Sun Path-\xc6 Badie-\xc6. Badie - Sun Path]`
  - `tests/test_title_matcher.py::test_a_credit_spelled_with_a_letter_nfkd_leaves_is_the_artists[\xde\xf3r\xf0ur Badie-08A - 124 - \xde. Badie - Sun Path-\xde Badie-\xde. Badie - Sun Path]`

Old text:

```
    folded = tuple(_folded(word) for word in written)
```

New text:

```
    folded = written
```

### `u245.M01_opt_in`

run: drop the opt in check, so a run without --send-to-cyanite reads the key and uploads

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M01_opt_in`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 3 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_price_that_is_not_a_number_is_said_as_such_in_the_plan`
  - `tests/test_cyanite_trial.py::test_the_script_plans_without_the_opt_in`
  - `tests/test_cyanite_trial.py::test_without_the_opt_in_the_run_is_a_plan_and_sends_nothing`

Old text:

```
    if not settings.send:
        say("nothing was sent: this is the plan. Add --send-to-cyanite to send it")
        return Ran(dry=True)
```

New text:

```
    if False:
        say("nothing was sent: this is the plan. Add --send-to-cyanite to send it")
        return Ran(dry=True)
```

### `u245.M02_cap_required`

run: send with no cap, so --send-to-cyanite without --cap uploads everything

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M02_cap_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_sending_needs_a_cap_and_a_price[given0-needs --cap]`

Old text:

```
    if settings.cap is None:
        raise TrialRefused("--send-to-cyanite needs --cap, the most files this run may upload")
```

New text:

```
    if settings.cap is None:
        settings = Settings(settings.paths, settings.output, settings.send, 10**6, settings.price, settings.resume)
```

### `u245.M03_cap_bound`

run: compare the count to the cap with >= rather than >, an off by one that refuses a run at the cap

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M03_cap_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 6 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_count_at_the_cap_is_sent`
  - `tests/test_cyanite_trial.py::test_a_file_retagged_between_two_runs_is_not_paid_for_again`
  - `tests/test_cyanite_trial.py::test_a_folder_moved_between_two_runs_is_not_paid_for_again`
  - `tests/test_cyanite_trial.py::test_an_interrupt_while_waiting_keeps_the_track_and_the_resume_does_not_upload_it`
  - `tests/test_cyanite_trial.py::test_resume_asks_again_about_an_unfinished_analysis_without_uploading`
  - `tests/test_cyanite_trial.py::test_resume_uploads_only_the_files_with_no_answer`

Old text:

```
    if len(upload) > settings.cap:
```

New text:

```
    if len(upload) >= settings.cap:
```

### `u245.M04_cap_counts_uploads`

run: read the cap against one fewer than the uploads, so a count one over the cap is sent

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M04_cap_counts_uploads`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_count_over_the_cap_refuses_before_anything_is_sent[3]`

Old text:

```
    if len(upload) > settings.cap:
```

New text:

```
    if len(upload) - 1 > settings.cap:
```

### `u245.M06_price_required`

run: send with no price, so the cost is never estimated before the upload

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M06_price_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_sending_needs_a_cap_and_a_price[given1-needs --price-per-track]`

Old text:

```
    if settings.price is None:
        raise TrialRefused(
```

New text:

```
    if settings.price is None and False:
        raise TrialRefused(
```

### `u245.M07_digest_without_tags`

audio_digest: hash the whole file, tags included, so a file retagged between two runs is uploaded and paid for again

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M07_digest_without_tags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_file_retagged_between_two_runs_is_not_paid_for_again`

Old text:

```
    start, end = _audio_span(data)
    return hashlib.sha256(data[start:end]).hexdigest()
```

New text:

```
    start, end = 0, len(data)
    return hashlib.sha256(data[start:end]).hexdigest()
```

### `u245.M08_never_overwrite`

run: drop the refusal of an output already there, so an earlier paid table is overwritten

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M08_never_overwrite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_an_output_already_there_refuses_without_resume[summary]`
  - `tests/test_cyanite_trial.py::test_an_output_already_there_refuses_without_resume[table]`

Old text:

```
            if taken.exists():
```

New text:

```
            if False:
```

### `u245.M09_resume_skips_answered`

run: read every prior row as unanswered, so a resume uploads and pays for answered files again

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M09_resume_skips_answered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 4 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_file_retagged_between_two_runs_is_not_paid_for_again`
  - `tests/test_cyanite_trial.py::test_a_folder_moved_between_two_runs_is_not_paid_for_again`
  - `tests/test_cyanite_trial.py::test_an_interrupt_while_waiting_keeps_the_track_and_the_resume_does_not_upload_it`
  - `tests/test_cyanite_trial.py::test_resume_uploads_only_the_files_with_no_answer`

Old text:

```
        if before is not None and before["agreement"] != NOT_READ:
```

New text:

```
        if before is not None and before["agreement"] == "never":
```

### `u245.M10_resume_asks_again`

run: upload a pending file again instead of asking about its library track

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M10_resume_asks_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_an_interrupt_while_waiting_keeps_the_track_and_the_resume_does_not_upload_it`
  - `tests/test_cyanite_trial.py::test_resume_asks_again_about_an_unfinished_analysis_without_uploading`

Old text:

```
        elif before is not None and before["library_track"]:
```

New text:

```
        elif False:
```

### `u245.M11_track_written_ahead`

analyse: never tell the run the track Cyanite made before the wait, so a run ended mid wait loses it and a resume pays for it again

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M11_track_written_ahead`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 4 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_stop_after_a_track_was_made_keeps_the_track`
  - `tests/test_cyanite_trial.py::test_a_tab_or_a_line_break_in_an_answer_stays_in_its_cell`
  - `tests/test_cyanite_trial.py::test_an_interrupt_while_waiting_keeps_the_track_and_the_resume_does_not_upload_it`
  - `tests/test_cyanite_trial.py::test_the_made_track_is_written_before_the_wait_so_a_signal_cannot_lose_it`

Old text:

```
        if self.on_made is not None:
            self.on_made(track_id)
```

New text:

```
        if False:
            self.on_made(track_id)
```

### `u245.M12_digest_identity`

read_table: key prior rows by the file's path again, so a moved folder is paid for twice

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M12_digest_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 5 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_file_retagged_between_two_runs_is_not_paid_for_again`
  - `tests/test_cyanite_trial.py::test_a_folder_moved_between_two_runs_is_not_paid_for_again`
  - `tests/test_cyanite_trial.py::test_an_interrupt_while_waiting_keeps_the_track_and_the_resume_does_not_upload_it`
  - `tests/test_cyanite_trial.py::test_resume_asks_again_about_an_unfinished_analysis_without_uploading`
  - `tests/test_cyanite_trial.py::test_resume_uploads_only_the_files_with_no_answer`

Old text:

```
    return {row["audio_sha256"]: row for row in rows if row["audio_sha256"]}
```

New text:

```
    return {row["file"]: row for row in rows if row["audio_sha256"]}
```

### `u245.M13_same_audio_once`

plan_files: send two files holding the same audio twice

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M13_same_audio_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_two_files_holding_the_same_audio_are_sent_once`

Old text:

```
            if digest in digests:
```

New text:

```
            if False:
```

### `u245.M14_mp3_only`

plan_files: send every file whatever its suffix

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M14_mp3_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 26 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_cell_opening_with_a_quote_reads_back_whole`
  - `tests/test_cyanite_trial.py::test_a_cell_the_encoding_cannot_carry_keeps_its_row`
  - `tests/test_cyanite_trial.py::test_a_count_at_the_cap_is_sent`
  - `tests/test_cyanite_trial.py::test_a_count_over_the_cap_refuses_before_anything_is_sent[0]`
  - `tests/test_cyanite_trial.py::test_a_count_over_the_cap_refuses_before_anything_is_sent[3]`
  - `tests/test_cyanite_trial.py::test_a_declared_cyanite_vocabulary_answers_before_the_aliases`
  - `tests/test_cyanite_trial.py::test_a_file_retagged_between_two_runs_is_not_paid_for_again`
  - `tests/test_cyanite_trial.py::test_a_file_that_is_not_an_mp3_is_listed_and_never_sent`
  - `tests/test_cyanite_trial.py::test_a_folder_moved_between_two_runs_is_not_paid_for_again`
  - `tests/test_cyanite_trial.py::test_a_run_with_nothing_to_send_leaves_an_empty_table_and_asks_nothing`
  - `tests/test_cyanite_trial.py::test_a_run_writes_each_files_folder_beside_cyanites_and_the_agreement`
  - `tests/test_cyanite_trial.py::test_a_tab_or_a_line_break_in_an_answer_stays_in_its_cell`
  - `tests/test_cyanite_trial.py::test_an_interrupt_while_waiting_keeps_the_track_and_the_resume_does_not_upload_it`
  - `tests/test_cyanite_trial.py::test_an_mp3_that_cannot_be_read_is_listed_and_not_sent`
  - `tests/test_cyanite_trial.py::test_an_unreadable_tag_is_shown_as_unreadable_not_as_no_folder`
  - ... and 11 more, see the JSON sidecar

Old text:

```
            if suffix not in UPLOADABLE:
```

New text:

```
            if False:
```

### `u245.M15_scrub`

CyaniteAsker.scrub: return the text unscrubbed, so an echoed key reaches a note, a row and a refusal

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M15_scrub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 4 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_failed_create_and_a_failed_analysis_are_scrubbed_of_the_key`
  - `tests/test_cyanite_trial.py::test_an_echoed_key_in_a_state_or_a_track_never_reaches_the_table`
  - `tests/test_cyanite_trial.py::test_an_echoed_key_in_a_track_id_alone_never_reaches_the_table`
  - `tests/test_cyanite_trial.py::test_the_key_is_in_no_note_row_refusal_or_repr`

Old text:

```
        return text.replace(self.key, _SCRUBBED) if self.key else text
```

New text:

```
        return text
```

### `u245.M16_cells_scrubbed`

_keep: write the row's cells unscrubbed

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M16_cells_scrubbed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_an_echoed_key_in_a_track_id_alone_never_reaches_the_table`

Old text:

```
    row = {name: asker.scrub(value) for name, value in row_for(declared, entry, analysis).items()}
```

New text:

```
    row = dict(row_for(declared, entry, analysis))
```

### `u245.M17_key_to_upload`

analyse: send the API's headers, the key among them, to the presigned upload address

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M17_key_to_upload`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_the_key_goes_only_in_the_authorization_header_of_the_api_requests`

Old text:

```
            Request("PUT", address, {"Content-Type": "audio/mpeg"}, audio, UPLOAD_TIMEOUT_S)
```

New text:

```
            Request("PUT", address, self._headers(), audio, UPLOAD_TIMEOUT_S)
```

### `u245.M18_rejected_remembered`

query: forget a rejected key, so it is sent again

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M18_rejected_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_rejected_key_is_never_sent_again`

Old text:

```
        if self.rejected is not None:
            raise secrets.CredentialRejected(
```

New text:

```
        if False:
            raise secrets.CredentialRejected(
```

### `u245.M19_401_rejected`

query: read a 401 as an outage rather than a rejected key

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M19_401_rejected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_rejected_key_is_never_sent_again`
  - `tests/test_cyanite_trial.py::test_a_rejected_key_refuses_at_the_preflight_with_nothing_uploaded[answer0]`

Old text:

```
        if reply.status == 401:
```

New text:

```
        if reply.status == 4010:
```

### `u245.M20_graphql_errors`

query: ignore GraphQL errors, so a refused query reads as an empty answer

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M20_graphql_errors`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 4 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_query_cyanite_refuses_stops_before_any_upload`
  - `tests/test_cyanite_trial.py::test_a_rejected_key_refuses_at_the_preflight_with_nothing_uploaded[answer1]`
  - `tests/test_cyanite_trial.py::test_a_rejected_key_refuses_at_the_preflight_with_nothing_uploaded[answer2]`
  - `tests/test_cyanite_trial.py::test_the_key_is_in_no_note_row_refusal_or_repr`

Old text:

```
        if errors:
```

New text:

```
        if False:
```

### `u245.M21_https_upload`

analyse: upload to an address that is not https

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M21_https_upload`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_an_upload_address_that_is_not_https_stops_before_the_upload`

Old text:

```
        if not address.startswith("https://"):
```

New text:

```
        if False:
```

### `u245.M22_library_full_stops`

analyse: read Cyanite's full library as one file's refusal, so the run goes on uploading

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M22_library_full_stops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_full_library_stops_the_run_and_keeps_the_rows_written`
  - `tests/test_cyanite_trial.py::test_resume_uploads_only_the_files_with_no_answer`

Old text:

```
            if code == LIBRARY_FULL:
```

New text:

```
            if code == "never":
```

### `u245.M23_not_started_stops`

wait: read an analysis never started as unfinished, so the run goes on uploading past a spent limit

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M23_not_started_stops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_stop_after_a_track_was_made_keeps_the_track`
  - `tests/test_cyanite_trial.py::test_an_analysis_never_started_stops_the_run`

Old text:

```
        if state == "AudioAnalysisV6NotStarted":
```

New text:

```
        if state == "never":
```

### `u245.M24_unread_not_a_disagreement`

agreement: read a file Cyanite gave no words for as no folder rather than not read

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M24_unread_not_a_disagreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 6 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_stop_after_a_track_was_made_keeps_the_track`
  - `tests/test_cyanite_trial.py::test_an_analysis_that_does_not_finish_in_the_window_is_kept_for_a_resume`
  - `tests/test_cyanite_trial.py::test_an_interrupt_while_waiting_keeps_the_track_and_the_resume_does_not_upload_it`
  - `tests/test_cyanite_trial.py::test_one_upload_refused_is_that_files_row_and_the_run_goes_on`
  - `tests/test_cyanite_trial.py::test_resume_asks_again_about_an_unfinished_analysis_without_uploading`
  - `tests/test_cyanite_trial.py::test_the_made_track_is_written_before_the_wait_so_a_signal_cannot_lose_it`

Old text:

```
    if analysis.words is None:
        return NOT_READ
```

New text:

```
    if analysis.words is None:
        return NO_FOLDER
```

### `u245.M25_share_leaves_out_unplaced`

summarise: count a word placing nowhere in the share again, as a disagreement

- File: `src/cratekit/tagging/cyanite.py`
- Source: `u245.json`, row `M25_share_leaves_out_unplaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_a_run_writes_each_files_folder_beside_cyanites_and_the_agreement`

Old text:

```
        placed = sum(tally[said] for said in (SAME_FOLDER, SAME_BUCKET, DIFFERENT))
```

New text:

```
        placed = sum(tally[said] for said in (SAME_FOLDER, SAME_BUCKET, DIFFERENT, NO_FOLDER))
```

### `u240.M11_needle_is_the_name`

_label_payload: freeze the label's name as its needle, ignoring --match

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M11_needle_is_the_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
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
- Collected: 334 against a baseline of 334
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
- Collected: 334 against a baseline of 334
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

### `u240.M14_widest_any`

copyright_matcher: the longer needle wins when it carries any other named, not every other

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M14_widest_any`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_sublabel_beside_a_third_label_settles_nothing`

Old text:

```
            if all(label_verify.credit_names(other[1], row[1]) for other in named)
```

New text:

```
            if any(label_verify.credit_names(other[1], row[1]) for other in named if other is not row)
```

### `u240.M15_no_widest_rule`

copyright_matcher: no specificity rule, so a sublabel's line settles neither label

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M15_no_widest_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_sublabels_own_line_names_the_sublabel_and_the_parents_names_the_parent`

Old text:

```
        if len(widest) == 1:
```

New text:

```
        if False:
```

### `u240.M16_genres_joined_by_name`

_copyright_seam: join a label's genre by its display name, round one's second blocker

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M16_genres_joined_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
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
- Collected: 334 against a baseline of 334
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

### `u240.M18_way_inverted`

_way: a label's genre reported as a catalogue's

- File: `src/cratekit/tagging/summary.py`
- Source: `u240.json`, row `M18_way_inverted`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
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
- Collected: 334 against a baseline of 334
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

### `u240.M20_warning_dropped`

_resume: the two label warning never reaches the envelope

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M20_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
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
- Collected: 334 against a baseline of 334
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

### `u240.M22_failed_items_left_out`

_summary: items with no report are not listed

- File: `src/cratekit/tagging/summary.py`
- Source: `u240.json`, row `M22_failed_items_left_out`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
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

### `u240.M23_cap_lowered`

_with_report: name three failed files rather than ten

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M23_cap_lowered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
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

### `u240.M1_two_names_take_the_first`

_by_label: a line naming two registered labels gives the file the first one's genre

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M1_two_names_take_the_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 334 against a baseline of 334
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_two_registered_labels_is_refused_for_that_file`
  - `tests/test_tag_folder_copyright.py::test_a_searchers_park_reaches_the_job_as_a_park_on_a_file_its_line_could_not_settle`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
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
- Collected: 334 against a baseline of 334
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_one_label_with_no_genre_is_asked_of_the_catalogues`
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_two_registered_labels_is_refused_for_that_file`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
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
- Collected: 334 against a baseline of 334
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
- Collected: 334 against a baseline of 334
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
- Collected: 334 against a baseline of 334
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_label_batch_with_every_catalogue_blocked_lands_tagged_by_label`
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_one_label_with_no_genre_is_asked_of_the_catalogues`
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_two_registered_labels_is_refused_for_that_file`
  - `tests/test_tag_folder_copyright.py::test_a_mixed_folder_with_every_catalogue_blocked_tags_each_file_by_its_line`
  - `tests/test_tag_folder_copyright.py::test_a_sweep_one_file_of_which_fails_still_reports_every_file`
  - `tests/test_tag_folder_copyright.py::test_an_unregistered_file_in_the_batch_is_left_untagged_and_its_item_fails`
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
- Collected: 334 against a baseline of 334
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
- Collected: 334 against a baseline of 334
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_one_label_with_no_genre_is_asked_of_the_catalogues`
  - `tests/test_tag_folder_copyright.py::test_a_line_naming_two_registered_labels_is_refused_for_that_file`
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
- Collected: 334 against a baseline of 334
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
- Collected: 334 against a baseline of 334
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

### `r816-b.B3_blank_spellings`

assert_rows_as_planned: read two spellings of a blank genre as a change

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-b.json`, row `B3_blank_spellings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[0_0]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[0_1]`
  - `tests/test_tag_rows.py::test_a_blank_row_is_as_planned_however_the_database_spells_blank[]`

Old text:

```
        if (_empty(held) and _empty(planned)) or str(held) == str(planned):
```

New text:

```
        if str(held) == str(planned):
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

### `r816-c.B7_read_back_word`

judge: stop comparing the genre read back with the file's word

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-c.json`, row `B7_read_back_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_read_back_names_a_row_that_does_not_carry_its_files_word`
  - `tests/test_tag_rows.py::test_the_read_back_names_a_row_whose_genre_points_at_no_lookup_row`

Old text:

```
        if word != item.file:
```

New text:

```
        if False:
```

### `r816-c.B8_read_back_columns`

judge: stop reporting another column that moved

- File: `src/cratekit/tagging/rows.py`
- Source: `r816-c.json`, row `B8_read_back_columns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_the_read_back_names_every_other_column_that_moved`

Old text:

```
        if changed:
```

New text:

```
        if False:
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
  - `tests/test_tagging_engine.py::test_the_walk_skips_the_appledouble_sidecar_beside_a_real_track`

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
  - `tests/test_tagging_engine.py::test_a_title_that_opens_with_dots_is_walked_and_so_is_the_album_holding_it`

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
  - `tests/test_tagging_engine.py::test_the_master_staging_tree_is_skipped_too`
  - `tests/test_tagging_engine.py::test_the_walk_does_not_descend_into_the_acquisition_staging_tree`

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
  - `tests/test_tagging_engine.py::test_the_master_staging_tree_is_skipped_too`
  - `tests/test_tagging_engine.py::test_the_skipped_dirnames_are_the_two_constants_that_own_them`

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
  - `tests/test_tagging_engine.py::test_a_word_the_taxonomy_does_not_know_is_written_and_reported`

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
  - `tests/test_tagging_engine.py::test_a_title_that_opens_with_dots_is_walked_and_so_is_the_album_holding_it`
  - `tests/test_tagging_engine.py::test_the_skip_does_not_stop_the_walk_recursing`
  - `tests/test_tagging_engine.py::test_the_walk_recurses_and_comes_back_sorted`

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

### `u85-a.A13_art_only_refusal_absorbed`

A refusal on a tagged file searched only for art fails the item again

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A13_art_only_refusal_absorbed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 2 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal[catalogue-parse-broken]`
  - `tests/test_tagging_engine.py::test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal[catalogue-unreachable]`

Old text:

```
    except CratekitError as exc:
```

New text:

```
    except ZeroDivisionError as exc:
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

### `u85-a.A3_unreadable_is_unchecked`

A file whose pictures cannot be read raises out of the item instead of reporting unchecked

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A3_unreadable_is_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_file_whose_pictures_cannot_be_read_is_unchecked_and_not_fetched`

Old text:

```
except (tags.UnsupportedContainer, art.UnreadableFile) as exc:
```

New text:

```
except tags.UnsupportedContainer as exc:
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
  - `tests/test_tagging_engine.py::test_no_fetch_supplied_is_unavailable_rather_than_a_silent_skip`

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
  - `tests/test_tagging_engine.py::test_a_fetch_that_raises_is_unavailable_and_never_fails_the_item`

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
  - `tests/test_tagging_engine.py::test_bytes_that_are_not_a_picture_are_unavailable_and_nothing_is_embedded`

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

### `u25-author-light.G1_resume_prefix`

Treat every filename as unfinished, including a complete Camelot head

- File: `src/cratekit/analysis/run.py`
- Source: `u25-author-light.json`, row `G1_resume_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_killed_batch_resumes_skipping_completed_tracks`

Old text:

```
    return has_head(path.name, template=_RESUME_TEMPLATE)

```

New text:

```
    return False

```

### `sitting3.G10_lone_clip_not_padded`

A lone clip shorter than the floor goes to the network unpadded

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G10_lone_clip_not_padded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_lone_short_clip_is_padded_to_the_floor`
  - `tests/test_analysis.py::test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length`
  - `tests/test_analysis.py::test_the_unchunked_path_pads_a_short_signal_too`

Old text:

```
    if len(slices) == 1:
        pad = floor - int(last.shape[-1])
        return [np.concatenate([last, np.zeros((last.shape[0], pad), last.dtype)], axis=-1)]

```

New text:

```
    if len(slices) == 1:
        return slices

```

### `sitting3.G11_tail_dropped`

Drop a short tail instead of folding it, so its frames are never scored

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G11_tail_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_short_tail_is_folded_into_the_chunk_before_it`
  - `tests/test_analysis.py::test_at_the_real_chunk_size_only_a_tail_under_the_floor_is_folded`

Old text:

```
    merged = np.concatenate([slices[-2], last], axis=-1)
    return [*slices[:-2], merged]

```

New text:

```
    return slices[:-1]

```

### `sitting3.G13_padded_frames_kept`

Count the frames the padding added, so a short clip's presence is diluted

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G13_padded_frames_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length`

Old text:

```
    if padded > width and vocals.size:

```

New text:

```
    if False:

```

### `sitting3.G14_unchunked_floor_is_width`

Let the unchunked path's floor collapse to the signal's own width

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G14_unchunked_floor_is_width`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_the_unchunked_path_pads_a_short_signal_too`

Old text:

```
    floor = MIN_CHUNK_SAMPLES if chunk_samples is None else min(MIN_CHUNK_SAMPLES, chunk_samples)

```

New text:

```
    floor = min(MIN_CHUNK_SAMPLES, chunk_samples or width)

```

### `sitting3.G15_fold_any_ragged_tail`

Fold every tail shorter than the chunk, not only one under the floor

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G15_fold_any_ragged_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_lone_short_clip_is_padded_to_the_floor`
  - `tests/test_analysis.py::test_at_the_real_chunk_size_only_a_tail_under_the_floor_is_folded`
  - `tests/test_analysis.py::test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length`

Old text:

```
    floor = MIN_CHUNK_SAMPLES if chunk_samples is None else min(MIN_CHUNK_SAMPLES, chunk_samples)

```

New text:

```
    floor = MIN_CHUNK_SAMPLES if chunk_samples is None else chunk_samples

```

### `sitting3.G1_columns_by_number`

Read the first three columns whatever the label table says, the R-370 defect

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G1_columns_by_number`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis.py::test_analyse_scores_the_singing_columns_not_the_first_three`
  - `tests/test_analysis.py::test_class_indices_resolve_the_singing_columns_by_name`
  - `tests/test_analysis.py::test_default_loader_builds_the_frame_wrapper_from_the_checkpoint_on_disk`

Old text:

```
    labels = getattr(model, "labels", None)
    if labels is None:
        raise ValueError(

```

New text:

```
    labels = getattr(model, "labels", None)
    if True:
        return (0, 1, 2)
        raise ValueError(

```

### `sitting3.G2_missing_target_read_as_fixture`

A label table lacking a target falls back to the first three columns instead of raising

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G2_missing_target_read_as_fixture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis.py::test_class_indices_resolve_the_singing_columns_by_name`

Old text:

```
    except ValueError as exc:
        raise ValueError(
            f"the vocal model's label table does not name all of {TARGET_LABELS}"
        ) from exc
    return (first, second, third)

```

New text:

```
    except ValueError:
        return (0, 1, 2)
    return (first, second, third)

```

### `sitting3.G4_clip_wrapper`

Build the clip level wrapper again

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G4_clip_wrapper`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_default_loader_builds_the_frame_wrapper_from_the_checkpoint_on_disk`

Old text:

```
    from panns_inference import SoundEventDetection

    # The wrapper prints its checkpoint path and device to stdout on
    # construction, and stdout is where the JSON envelope goes.
    with contextlib.redirect_stdout(io.StringIO()):
        return SoundEventDetection(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")

```

New text:

```
    from panns_inference import AudioTagging

    with contextlib.redirect_stdout(io.StringIO()):
        return AudioTagging(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")

```

### `sitting3.G5_loader_skips_readiness`

Ask the library for files that are not there, which is the wget shell out

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G5_loader_skips_readiness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_default_loader_refuses_before_the_extra_is_asked_for_a_missing_checkpoint`

Old text:

```
    missing = scoring.missing_requirement()
    if missing is not None:
        raise FileNotFoundError(missing)

```

New text:

```
    missing = None
    if missing is not None:
        raise FileNotFoundError(missing)

```

### `sitting3.G7_chatter_on_stdout`

Let the wrapper print onto the JSON envelope's stream

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G7_chatter_on_stdout`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_default_loader_builds_the_frame_wrapper_from_the_checkpoint_on_disk`

Old text:

```
    with contextlib.redirect_stdout(io.StringIO()):
        return SoundEventDetection(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")

```

New text:

```
    with contextlib.nullcontext():
        return SoundEventDetection(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")

```

### `sitting3.G9_tail_sent_alone`

Send a short tail to the network as its own piece, the R-371 defect

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G9_tail_sent_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_lone_short_clip_is_padded_to_the_floor`
  - `tests/test_analysis.py::test_a_short_tail_is_folded_into_the_chunk_before_it`
  - `tests/test_analysis.py::test_at_the_real_chunk_size_only_a_tail_under_the_floor_is_folded`
  - `tests/test_analysis.py::test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length`
  - `tests/test_analysis.py::test_the_unchunked_path_pads_a_short_signal_too`

Old text:

```
    slices = _without_a_short_tail(slices, floor=floor)

```

New text:

```
    slices = list(slices)

```

### `u25-author-light.G3_unchunked_only`

Ignore chunk_samples and always run one whole-track pass

- File: `src/cratekit/analysis/vocal.py`
- Source: `u25-author-light.json`, row `G3_unchunked_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_short_tail_is_folded_into_the_chunk_before_it`
  - `tests/test_analysis.py::test_an_exact_multiple_still_walks_in_equal_pieces`
  - `tests/test_analysis.py::test_at_the_real_chunk_size_only_a_tail_under_the_floor_is_folded`
  - `tests/test_analysis.py::test_chunked_inference_walks_the_signal_in_pieces`

Old text:

```
    if chunk_samples is None or width <= chunk_samples:
        slices = [batch]
    else:
        slices = [
            batch[:, start : start + chunk_samples]
            for start in range(0, width, chunk_samples)
        ]

```

New text:

```
    slices = [batch]

```

### `sitting3.G12_columns_per_track`

Resolve the columns per track after the decode instead of once at load

- File: `src/cratekit/analysis/vocals.py`
- Source: `sitting3.json`, row `G12_columns_per_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`

Old text:

```
        _VOCAL_COLUMNS = class_indices(model)
        _VOCAL_MODEL = model

```

New text:

```
        _VOCAL_COLUMNS = None
        _VOCAL_MODEL = model

```

### `u260.F10_fetch_memory_one`

IMAGE_MEMORY: one entry, so two interleaved albums ask on every file

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F10_fetch_memory_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 2 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_shipped_fetch_memory_is_bounded`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`

Old text:

```
IMAGE_MEMORY = 4
```

New text:

```
IMAGE_MEMORY = 1
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

### `u260.F2_empty_answer_remembered`

remembering: drop the empty answer check, so an empty answer is kept and handed to the next file without a request

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F2_empty_answer_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_an_empty_answer_handed_straight_in_is_not_remembered`

Old text:

```
        if not data or (admit is not None and not admit(data)):
```

New text:

```
        if data is None or (admit is not None and not admit(data)):
```

### `u260.F3_admission_ignored`

remembering: drop the admission, so bytes that are not a picture are remembered and never asked for again

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F3_admission_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 2 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_an_answer_the_admission_refuses_is_handed_on_and_not_remembered`
  - `tests/test_album_cover_once.py::test_bytes_that_are_not_a_picture_are_asked_again_and_fail_as_they_did`

Old text:

```
        if not data or (admit is not None and not admit(data)):
```

New text:

```
        if not data:
```

### `u260.F4_binder_admits_everything`

for_images: build the shared fetch with no admission, so the shipped worker remembers undecodable bytes

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F4_binder_admits_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_bytes_that_are_not_a_picture_are_asked_again_and_fail_as_they_did`

Old text:

```
        _images.append(remembering(default_image_fetch(), admit=art.decodes))
```

New text:

```
        _images.append(remembering(default_image_fetch()))
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

### `u260.F6_fetch_bound_off_by_one`

remembering: keep one entry more than the bound

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F6_fetch_bound_off_by_one`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_fetch_memory_keeps_a_few_addresses_and_forgets_the_oldest`

Old text:

```
            while len(held) > bound:
```

New text:

```
            while len(held) > bound + 1:
```

### `u260.F7_fetch_evicts_newest`

remembering: evict the newest entry instead of the least recently used

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F7_fetch_evicts_newest`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_fetch_memory_keeps_a_few_addresses_and_forgets_the_oldest`

Old text:

```
                held.popitem(last=False)
```

New text:

```
                held.popitem(last=True)
```

### `u260.F8_fetch_hit_not_refreshed`

remembering: a hit no longer refreshes its entry, so the memory is first in first out

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F8_fetch_hit_not_refreshed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_fetch_memory_keeps_a_few_addresses_and_forgets_the_oldest`

Old text:

```
            if data is not None:
                held.move_to_end(url)
                return data
```

New text:

```
            if data is not None:
                return data
```

### `u260.F9_fetch_memory_unbounded`

IMAGE_MEMORY: a hundred entries, near enough unbounded for a sweep

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F9_fetch_memory_unbounded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_shipped_fetch_memory_is_bounded`

Old text:

```
IMAGE_MEMORY = 4
```

New text:

```
IMAGE_MEMORY = 100
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

### `r1103.S2_rejected_verdict`

Sample of the unit's existing guards: retag_one ignores a rejected verdict and asks the searcher again

- File: `src/cratekit/tagging/retag.py`
- Source: `r1103.json`, row `S2_rejected_verdict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 222 against a baseline of 222
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_settled_against_every_candidate_is_not_counted_as_an_open_question`
  - `tests/test_genre_retag.py::test_a_rejected_verdict_leaves_the_file_alone_and_asks_nobody`

Old text:

```
        if item.suppressed:
```

New text:

```
        if False:
```

### `r1103.S3_written_property`

Sample: RetagOutcome.written takes every result, written or not

- File: `src/cratekit/tagging/retag.py`
- Source: `r1103.json`, row `S3_written_property`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 222 against a baseline of 222
- Kills: 6 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_settled_against_every_candidate_is_not_counted_as_an_open_question`
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`
  - `tests/test_genre_retag.py::test_a_second_run_over_a_corrected_folder_selects_nothing`
  - `tests/test_genre_retag.py::test_an_answer_that_is_itself_a_catch_all_is_refused_and_the_file_is_untouched`
  - `tests/test_genre_retag.py::test_an_unwritten_file_never_reaches_the_library_plan`
  - `tests/test_genre_retag.py::test_the_plan_is_built_from_what_was_written_and_never_from_the_selection`

Old text:

```
        return tuple(result for result in self.results if result.written)
```

New text:

```
        return tuple(self.results)
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

### `r1103.W5_unwritten_claims_written`

retag_one: the unwritten result also claims the genre as written, so the sweep's written set and the library plan take it

- File: `src/cratekit/tagging/retag.py`
- Source: `r1103.json`, row `W5_unwritten_claims_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 222 against a baseline of 222
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`
  - `tests/test_genre_retag.py::test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run`
  - `tests/test_genre_retag.py::test_an_unwritten_file_never_reaches_the_library_plan`

Old text:

```
            reason=UNWRITTEN_REASON,
            proposed=answer,
```

New text:

```
            reason=UNWRITTEN_REASON,
            written=answer,
            proposed=answer,
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

### `r744.A1_near_miss_widened`

off by four counts as a near miss, hiding sitting 19's 144 against 140.00 in the bucket the bin width explains

- File: `src/cratekit/analysis/agreement.py`
- Source: `r744.json`, row `A1_near_miss_widened`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 5 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_a_head_off_by_four_is_not_off_by_one_to_three`
  - `tests/test_head_agreement.py::test_the_comparison_buckets_every_row_and_counts_what_it_could_not_compare`
  - `tests/test_head_agreement.py::test_the_four_tempo_buckets[124-120.0-other_level]`
  - `tests/test_head_agreement.py::test_the_measurement_reads_a_disposable_copy_and_buckets_the_fixture`
  - `tests/test_head_agreement.py::test_the_script_prints_the_four_buckets_over_a_fixture_copy`

Old text:

```
    if distance <= 3:
        return OFF_ONE_TO_THREE
```

New text:

```
    if distance <= 4:
        return OFF_ONE_TO_THREE
```

### `r744.A2_half_not_recognised`

a head at half the reference is read as another level rather than as the octave case

- File: `src/cratekit/analysis/agreement.py`
- Source: `r744.json`, row `A2_half_not_recognised`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 4 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_the_comparison_buckets_every_row_and_counts_what_it_could_not_compare`
  - `tests/test_head_agreement.py::test_the_four_tempo_buckets[83-166.0-half_or_double]`
  - `tests/test_head_agreement.py::test_the_measurement_reads_a_disposable_copy_and_buckets_the_fixture`
  - `tests/test_head_agreement.py::test_the_script_prints_the_four_buckets_over_a_fixture_copy`

Old text:

```
    if abs(ratio - 2.0) <= _DOUBLE_TOLERANCE or abs(ratio - 0.5) <= _HALF_TOLERANCE:
```

New text:

```
    if abs(ratio - 2.0) <= _DOUBLE_TOLERANCE:
```

### `r744.A3_classic_names_unmapped`

a classic key name is not mapped, so a library whose display is not Camelot reads every key as unkeyed

- File: `src/cratekit/analysis/agreement.py`
- Source: `r744.json`, row `A3_classic_names_unmapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 18 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[A#-06B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Abm-01A]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Am-08A]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Bb-06B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[C#-03B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[C#m-12A]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[C-08B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Db-03B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Dbm-12A]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[F#-02B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[F#m-11A]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[G#m-01A]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Gb-02B]`
  - `tests/test_head_agreement.py::test_either_key_notation_maps_to_one_padded_camelot[Gbm-11A]`
  - `tests/test_head_agreement.py::test_every_classic_name_reaches_a_code_the_detector_can_emit`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    classic = _CLASSIC_TO_CAMELOT.get(text)
```

New text:

```
    classic = None
```

### `r744.A4_whole_number_counts_as_rekordbox`

a whole number stored tempo counts as rekordbox's own analysis, so the imported back catalogue measures itself

- File: `src/cratekit/analysis/agreement.py`
- Source: `r744.json`, row `A4_whole_number_counts_as_rekordbox`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 2 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_a_fractional_stored_tempo_is_rekordbox_own_analysis_and_a_whole_one_is_not`
  - `tests/test_head_agreement.py::test_reanalysis_samples_rekordbox_own_rows_with_a_file_and_buckets_the_detector`

Old text:

```
        return bool(self.stored_hundredths) and self.stored_hundredths % 100 != 0
```

New text:

```
        return bool(self.stored_hundredths)
```

### `r744.A5_removed_rows_counted`

a row rekordbox removed is compared, measuring a head nobody can see

- File: `src/cratekit/analysis/agreement.py`
- Source: `r744.json`, row `A5_removed_rows_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 2 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_the_measurement_reads_a_disposable_copy_and_buckets_the_fixture`
  - `tests/test_head_agreement.py::test_the_script_prints_the_four_buckets_over_a_fixture_copy`

Old text:

```
            detail={"content_id": str(getattr(content, "ID", ""))},
        ):
            continue
```

New text:

```
            detail={"content_id": str(getattr(content, "ID", ""))},
        ):
            pass
```

### `r744.A6_sample_never_full`

the sample keeps resolving rows after the limit, walking the whole collection for ten files

- File: `src/cratekit/analysis/agreement.py`
- Source: `r744.json`, row `A6_sample_never_full`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_the_sample_stops_resolving_rows_once_it_is_full`

Old text:

```
        if len(chosen) >= limit:
            break
```

New text:

```
        if len(chosen) >= limit:
            pass
```

### `r744.E8_record_applies_to_every_window`

the recorded agreement says it applies whatever window the run bound, so a DJ who raised theirs is shown a rate nobody measured for it

- File: `src/cratekit/analysis/detect.py`
- Source: `r744.json`, row `E8_record_applies_to_every_window`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_the_record_says_whether_it_applies_to_the_bound_window`

Old text:

```
    record["applies_to_window"] = window is None or tuple(window) == measured
```

New text:

```
    record["applies_to_window"] = True
```

### `r744.E9_record_does_not_sum`

one recorded bucket is changed, so the four no longer sum to the files measured

- File: `src/cratekit/analysis/detect.py`
- Source: `r744.json`, row `E9_record_does_not_sum`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_the_recorded_buckets_sum_to_the_files_measured`

Old text:

```
        "equal": 194,
```

New text:

```
        "equal": 190,
```

### `u283.D1_shape_sent`

identity: a token that is not one printable word is sent rather than refused

- File: `src/cratekit/tagging/discogs.py`
- Source: `u283.json`, row `D1_shape_sent`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`
- Collected: 200 against a baseline of 200
- Kills: 4 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_malformed_token_is_refused_without_a_request_and_asked_again`
  - `tests/test_setup_discogs.py::test_a_token_that_is_not_one_printable_word_is_rejected_and_never_sent[caf\xe9token]`
  - `tests/test_setup_discogs.py::test_a_token_that_is_not_one_printable_word_is_rejected_and_never_sent[tab\there]`
  - `tests/test_setup_discogs.py::test_a_token_that_is_not_one_printable_word_is_rejected_and_never_sent[two words]`

Old text:

```
        if not _TOKEN_SHAPE.fullmatch(self.token):
            return TokenCheck(
```

New text:

```
        if False:
            return TokenCheck(
```

### `u283.D2_401_unchecked`

identity: a 401 is read as unchecked, so a rejected token is stored with a note

- File: `src/cratekit/tagging/discogs.py`
- Source: `u283.json`, row `D2_401_unchecked`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`
- Collected: 200 against a baseline of 200
- Kills: 4 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_401_rejects_the_token`
  - `tests/test_setup_discogs.py::test_a_rejected_token_is_refused_offered_again_and_never_stored`
  - `tests/test_setup_discogs.py::test_every_try_rejected_stores_nothing_and_is_a_note_not_a_failure`
  - `tests/test_setup_discogs.py::test_the_verb_refuses_a_rejected_token_and_stores_nothing`

Old text:

```
            return TokenCheck(TokenVerdict.REJECTED, "Discogs answered 401, it does not accept this token")
```

New text:

```
            return TokenCheck(TokenVerdict.UNCHECKED, "Discogs answered 401, it does not accept this token")
```

### `u283.D3_reraise_swallowed`

identity: a refusal that is not a 401 is read as a rejection rather than raised

- File: `src/cratekit/tagging/discogs.py`
- Source: `u283.json`, row `D3_reraise_swallowed`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`
- Collected: 200 against a baseline of 200
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_refusal_the_fetch_raises_is_no_verdict_and_stores_nothing`

Old text:

```
            if self.rejected is None:
                raise
```

New text:

```
            if False:
                raise
```

### `u283.D4_any_object_accepted`

identity: any JSON object is acceptance, an account named or not

- File: `src/cratekit/tagging/discogs.py`
- Source: `u283.json`, row `D4_any_object_accepted`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`
- Collected: 200 against a baseline of 200
- Kills: 3 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_anything_but_an_identity_or_a_401_leaves_the_token_unchecked[id-as-bool]`
  - `tests/test_setup_discogs.py::test_anything_but_an_identity_or_a_401_leaves_the_token_unchecked[id-as-text]`
  - `tests/test_setup_discogs.py::test_anything_but_an_identity_or_a_401_leaves_the_token_unchecked[no-id]`

Old text:

```
        if type(read.get("id")) is not int:
```

New text:

```
        if False:
```

### `u283.D5_id_truthy`

identity: an id that is present in any type is acceptance, a nearby value

- File: `src/cratekit/tagging/discogs.py`
- Source: `u283.json`, row `D5_id_truthy`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`
- Collected: 200 against a baseline of 200
- Kills: 2 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_anything_but_an_identity_or_a_401_leaves_the_token_unchecked[id-as-bool]`
  - `tests/test_setup_discogs.py::test_anything_but_an_identity_or_a_401_leaves_the_token_unchecked[id-as-text]`

Old text:

```
        if type(read.get("id")) is not int:
```

New text:

```
        if read.get("id") is None:
```

### `u283.D6_said_unscrubbed`

_said: a note is no longer scrubbed of the token, the check's only scrub since round one

- File: `src/cratekit/tagging/discogs.py`
- Source: `u283.json`, row `D6_said_unscrubbed`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`
- Collected: 200 against a baseline of 200
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_the_token_reaches_no_url_note_record_log_or_refusal`
  - `tests/test_setup_discogs.py::test_the_check_never_says_the_token_even_when_an_answer_carries_it`

Old text:

```
        return SourceOutcome(DISCOGS, answer, note=self._scrub(note))
```

New text:

```
        return SourceOutcome(DISCOGS, answer, note=note)
```

### `u283.D7_check_unpaced_sleep`

check_discogs_token: the caller's sleep is not handed to the asker, so the pacer sleeps for real and is not the caller's

- File: `src/cratekit/tagging/searchers.py`
- Source: `u283.json`, row `D7_check_unpaced_sleep`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`
- Collected: 200 against a baseline of 200
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_the_check_is_paced_like_a_search`

Old text:

```
    return discogs_asker(token=token, fetch=fetch, sleep=sleep).identity()
```

New text:

```
    return discogs_asker(token=token, fetch=fetch).identity()
```

### `u283.D8_identity_address`

DISCOGS_IDENTITY: the user endpoint rather than the identity one

- File: `src/cratekit/tagging/discogs.py`
- Source: `u283.json`, row `D8_identity_address`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`
- Collected: 200 against a baseline of 200
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_an_identity_naming_an_account_accepts_the_token`

Old text:

```
DISCOGS_IDENTITY = f"{DISCOGS_API}/oauth/identity"
```

New text:

```
DISCOGS_IDENTITY = f"{DISCOGS_API}/users/identity"
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

### `u284.R2_an_answer_never_clears`

refused._change: a match or a miss leaves the date, so a catalogue that answers again still reads as refusing

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R2_an_answer_never_clears`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_miss_from_the_refusing_catalogue_clears_it_and_an_outage_does_not`
  - `tests/test_sync_refused.py::test_an_answer_clears_the_catalogue_and_leaves_the_others`

Old text:

```
            elif held.pop(source, None) is None:
                return
```

New text:

```
            else:
                return
```

### `u284.R3_write_without_the_lock`

refused._change: write though the lock was not had, so two sweeps can lose each other's dates

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R3_write_without_the_lock`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_lock_another_process_holds_skips_the_write_rather_than_waiting`

Old text:

```
            if not had:
                LOG.info
```

New text:

```
            if False:
                LOG.info
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

### `u284.R6_write_failure_raises`

refused._change: catch only ValueError, so a record that cannot be written fails the file it was asked about

- File: `src/cratekit/tagging/refused.py`
- Source: `u284.json`, row `R6_write_failure_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_record_whose_target_cannot_be_replaced_never_raises`

Old text:

```
    except (OSError, ValueError, RecursionError) as exc:
```

New text:

```
    except ValueError as exc:
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

### `u276.K12_stream_worker_binding_names_whole`

analysis/ahead.py: a stream worker's detector binding names the whole method, so a head measured ahead reads another key than the driver's

- File: `src/cratekit/analysis/ahead.py`
- Source: `u276.json`, row `K12_stream_worker_binding_names_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_no_shipped_caller_of_the_detector_names_a_key_method`
  - `tests/test_analysis_key_default.py::test_the_runs_shipped_bindings_name_no_method_so_they_take_the_default[ahead.py]`

Old text:

```
            drift_cut=float(drift_cut),
        )
    )
```

New text:

```
            drift_cut=float(drift_cut),
            key="whole",
        )
    )
```

### `u276.K11_run_binding_names_whole`

analysis/cli.py: the driver's detector binding names the whole method, so analyze run separates whatever the default says

- File: `src/cratekit/analysis/cli.py`
- Source: `u276.json`, row `K11_run_binding_names_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_no_shipped_caller_of_the_detector_names_a_key_method`
  - `tests/test_analysis_key_default.py::test_the_runs_shipped_bindings_name_no_method_so_they_take_the_default[cli.py]`

Old text:

```
            drift_cut=cfg.analysis.drift_cut,
        )
        light.bind_detect(_BOUND_DETECT)
```

New text:

```
            drift_cut=cfg.analysis.drift_cut,
            key=detect.KEY_WHOLE,
        )
        light.bind_detect(_BOUND_DETECT)
```

### `u276.K15_warm_up_names_whole`

analysis/warm.py: the warm up's detector call names the whole method, so every process runs a separation no real head runs

- File: `src/cratekit/analysis/warm.py`
- Source: `u276.json`, row `K15_warm_up_names_whole`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_no_shipped_caller_of_the_detector_names_a_key_method`

Old text:

```
            path, tempo_window=(DEFAULT_TEMPO_FLOOR, DEFAULT_TEMPO_CEILING)
        )
```

New text:

```
            path, tempo_window=(DEFAULT_TEMPO_FLOOR, DEFAULT_TEMPO_CEILING), key="whole"
        )
```

### `u276.K2_profile_default_whole`

key_profile: default its method to whole by name, past KEY_DEFAULT, so a caller of the profile alone separates

- File: `src/cratekit/analysis/detect.py`
- Source: `u276.json`, row `K2_profile_default_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`, `tests/test_analysis_key_methods.py`, `tests/test_analysis_key_windows.py`
- Collected: 54 against a baseline of 54
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_a_detector_function_called_without_a_method_takes_the_default[key_profile]`

Old text:

```
    method: str = KEY_DEFAULT,
    timings: MutableMapping[str, float] | None = None,
) -> Any:
```

New text:

```
    method: str = KEY_WHOLE,
    timings: MutableMapping[str, float] | None = None,
) -> Any:
```

### `u276.K3_analyse_file_default_whole`

analyse_file: default its key to whole by name, so analyze run and its workers, which name none, separate

- File: `src/cratekit/analysis/detect.py`
- Source: `u276.json`, row `K3_analyse_file_default_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`, `tests/test_analysis_key_methods.py`, `tests/test_analysis_key_windows.py`
- Collected: 54 against a baseline of 54
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_a_detector_function_called_without_a_method_takes_the_default[analyse_file]`

Old text:

```
    key: str = KEY_DEFAULT,
    timings
```

New text:

```
    key: str = KEY_WHOLE,
    timings
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

### `u40-author-full.C1_gate_by_position`

Take gates[0] rather than the gate declared against the plan, so a reordered tuple answers the wrong question

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u40-author-full.json`, row `C1_gate_by_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`
- Collected: 1067 against a baseline of 1067
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_handler_finds_its_gate_by_digest_source_and_not_by_position`

Old text:

```
    for spec in ctx.entry.gates:
        if spec.digest_source == PLAN:
            return spec
```

New text:

```
    for spec in ctx.entry.gates:
        return spec
```

### `u40-author-full.C2_no_gate_no_refusal`

Return None instead of refusing when the entry declares no plan gate, so a destructive sweep runs unconfirmed

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u40-author-full.json`, row `C2_no_gate_no_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_cli_contract.py`, `tests/test_queued_resume_contract.py`
- Collected: 1067 against a baseline of 1067
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_handler_refuses_when_its_entry_declares_no_plan_gate`

Old text:

```
    raise refuse(
        "refused-by-policy",
        "this verb is destructive and its registry entry declares no decision "
        "made against the plan, so there is nothing for a person to confirm",
        remedy=Remedy.REPORT_DEFECT,
        origin=("tagging", "retag_cli"),
        detail={"verb": ctx.entry.name},
    )
```

New text:

```
    return None
```

### `u281.S3_challenge_header_case`

_refusal_note: compare the header's value as sent, so ' Challenge ' is not named one

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `S3_challenge_header_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_the_challenge_header_is_read_whatever_case_its_name_and_value_arrive_in`

Old text:

```
    if mitigated.strip().lower() == _CF_CHALLENGE:
```

New text:

```
    if mitigated == _CF_CHALLENGE:
```

### `u281.S4_any_mitigation_is_a_challenge`

_refusal_note: name any Cf-Mitigated value a challenge, so a block is called a challenge

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `S4_any_mitigation_is_a_challenge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_another_mitigation_is_not_called_a_challenge`

Old text:

```
    if mitigated.strip().lower() == _CF_CHALLENGE:
```

New text:

```
    if mitigated:
```

### `r744.B1_window_not_bound`

the run binds the shipped window rather than the configured one, so analysis.tempo_floor and tempo_ceiling change nothing

- File: `src/cratekit/analysis/cli.py`
- Source: `r744.json`, row `B1_window_not_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`, `tests/test_analysis_workers.py`
- Collected: 237 against a baseline of 237
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_a_raised_window_loads_and_reaches_the_detector_binding`

Old text:

```
            tempo_window=(cfg.analysis.tempo_floor, cfg.analysis.tempo_ceiling),
```

New text:

```
            tempo_window=(80, 160),
```

### `u181.V2_torch_failure_kind`

vocals.requirement: a torch that will not import is named as missing files, so doctor offers no reinstall

- File: `src/cratekit/analysis/vocals.py`
- Source: `u181.json`, row `V2_torch_failure_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_doctor.py`
- Collected: 451 against a baseline of 451
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_probe_names_a_missing_extra_as_the_extra`

Old text:

```
        return (
            MISSING_EXTRA,
            f"the 'vocals' extra is not usable here ({type(exc).__name__}: {exc}); {install()}",
        )
```

New text:

```
        return (
            MISSING_FILES,
            f"the 'vocals' extra is not usable here ({type(exc).__name__}: {exc}); {install()}",
        )
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

