# Mutation table: u333-replay-after-6r

Measured by `scripts/mutate.py` on 2026-11-24 06:47 UTC, branch `cloud/982-test-slice-2` at `5f795789`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23236 collected. pytest invocations for this batch: 408.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `0ed43045c587`, and this tree is at `5f795789c100`).

Subset baselines: 35, each measured by this driver.

Known failures: 248 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23236 against 23236. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r263.W4_stale_suffix` | `src/cratekit/sync/watermarks.py` | user | 1 file(s) | 31 | 1 | killed |
| `u322.M23_backlog_row_digest_keeps_words` | `src/cratekit/tagging/backlog.py` | user | 1 file(s) | 38 | 1 | killed |
| `r791-a.S1_403_blocks` | `src/cratekit/tagging/catalogues.py` | user | 1 file(s) | 67 | 4 | killed |
| `r791-a.S3_client_challenge_title` | `src/cratekit/tagging/catalogues.py` | user | 1 file(s) | 67 | 5 | killed |
| `r791-a.S4_ellipsis_character` | `src/cratekit/tagging/catalogues.py` | user | 1 file(s) | 67 | 1 | killed |
| `r791-a.S5_challenge_body` | `src/cratekit/tagging/catalogues.py` | user | 1 file(s) | 67 | 1 | killed |
| `r791-a.S9_gone_track_page` | `src/cratekit/tagging/catalogues.py` | user | 1 file(s) | 67 | 1 | killed |
| `u282.W1_walk_beatport_first` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 141 | 32 | killed |
| `u282.W2_sources_beatport_first` | `src/cratekit/tagging/catalogues.py` | user | 1 file(s) | 40 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R7_pacer_does_not_sleep` | `src/cratekit/tagging/catalogues.py` | user | 1 file(s) | 67 | 5 | killed |
| `u56-catalogue-searcher-and-tag-workers.R8_no_jitter` | `src/cratekit/tagging/catalogues.py` | user | 1 file(s) | 67 | 1 | killed |
| `r1476.M10_no_name_slug_step` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 4 | killed |
| `r1476.M11_slug_step_beats_exact_name` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `r1476.M12_no_identifier_fallback` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 3 | killed |
| `r1476.M13_needles_not_held` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 11 | killed |
| `r1476.M14_genre_join_by_name` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 2 | killed |
| `r1476.M15_answer_without_genre` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 5 | killed |
| `r1476.M16_unsluggable_raises` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 2 | killed |
| `r1476.M17_remedy_names_display_name` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 3 | killed |
| `r1476.M18_remedy_head_never_shared` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `r1476.M19_outranked_wording` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `r1476.M1_identifier_not_frozen` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 7 | killed |
| `r1476.M2_folder_seam_by_name` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 2 | killed |
| `r1476.M3_folder_seam_with_no_identifier` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 2 | killed |
| `r1476.M6_worker_hands_no_folder_seam` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 2 | killed |
| `r1476.M7_worker_hands_identifier_as_label` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `r1476.M8_shared_name_takes_first` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 10 | killed |
| `r1476.M9_identifier_first` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 5 | killed |
| `u178.S2_unknown_label_refused` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.S3_unreadable_registry_refuses_label` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.S4_genres_frozen` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 13 | killed |
| `u178.S5_worker_takes_label` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 7 | killed |
| `u178.S6_outranked_needs_label` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 4 | killed |
| `u192.T1_typed_label_on_queue` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `u192.T2_queue_warnings_lost` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 1 | killed |
| `u192.T3_resume_label_unsaid` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 2 | killed |
| `u192.T4_tag_queue_only_ignored` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 64 | 2 | killed |
| `u289.C1_record_drops_asked` | `src/cratekit/tagging/cli.py` | user | 1 file(s) | 167 | 1 | killed |
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
| `u244.M01_no_token_not_asked` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 8 | killed |
| `u244.M02_rejection_remembered` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 1 | killed |
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
| `u283.D6_said_unscrubbed` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 101 | 1 | killed |
| `u289.S4_discogs_asked_head` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 167 | 27 | killed |
| `u318.S01_track_needs_the_mix` | `src/cratekit/tagging/discogs.py` | user | 2 file(s) | 505 | 33 | killed |
| `u318.S02_single_needs_the_mix` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 338 | 14 | killed |
| `u318.S03_single_track_alone` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 338 | 2 | killed |
| `u318.S04_miss_names_the_release` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 338 | 8 | killed |
| `u318.S05_fallback_found` | `src/cratekit/tagging/discogs.py` | user | 1 file(s) | 338 | 1 | killed |
| `u244.M23_published_waits_for_discogs` | `src/cratekit/tagging/published.py` | user | 1 file(s) | 101 | 1 | killed |
| `u322.M17_deezer_gate_open_always` | `src/cratekit/tagging/published.py` | user | 1 file(s) | 38 | 1 | killed |
| `u322.M18_deezer_past_an_outage` | `src/cratekit/tagging/published.py` | user | 1 file(s) | 38 | 2 | killed |
| `u322.M19_suggest_binder_flag_off` | `src/cratekit/tagging/published.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1103.S1_answer_too_coarse` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 2 | killed |
| `r1103.S2_rejected_verdict` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 2 | killed |
| `r1103.S3_written_property` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 6 | killed |
| `r1103.W1_writer_answer_ignored` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 3 | killed |
| `r1103.W2_unwritten_reason_blank` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 2 | killed |
| `r1103.W3_unwritten_reason_wrong` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 2 | killed |
| `r1103.W4_unwritten_proposed_dropped` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 2 | killed |
| `r1103.W5_unwritten_claims_written` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 3 | killed |
| `r1103.W6_unwritten_current_swapped` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 1 | killed |
| `u40-author-full.D2_ambiguous_written` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 1 | killed |
| `u40-author-full.D4_absent_row_silent` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 1 | killed |
| `u40-author-full.D5_no_enable` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 5 | killed |
| `u40-author-full.D6_no_policy_assert` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 1 | killed |
| `u40-author-full.D7_unmatched_dropped` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 3 | killed |
| `u40-author-full.D8_contested_last_wins` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 1 | killed |
| `u40-author-full.D9_contested_first_still_written` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 1 | killed |
| `u40-author-full.P10_resolved_not_read` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 5 | killed |
| `u40-author-full.P6_option_id_as_genre` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 3 | killed |
| `u40-author-full.P7_coarse_offered` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 1 | killed |
| `u40-author-full.P9_settled_counted_as_asked` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 2 | killed |
| `u40-author-full.S1_blank_selected` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 2 | killed |
| `u40-author-full.S2_specific_selected` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 19 | killed |
| `u40-author-full.S3_unsorted_walk` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 1 | killed |
| `u40-author-full.S6_plan_drops_current` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 1 | killed |
| `u40-author-round-2.D1_plan_from_selection` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 2 | killed |
| `u40-author-round-2.P5_verdict_not_checked` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 1 | killed |
| `u40-author-round-2.P8_identity_key` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 1 | killed |
| `r185-r246-author.E1_plan_gate_by_position` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 50 | 1 | killed |
| `r290-author.R1_retag_rebuild_drops_the_type` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 126 | 1 | killed |
| `u40-author-full.C1_gate_by_position` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 50 | 1 | killed |
| `u40-author-full.C2_no_gate_no_refusal` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 50 | 1 | killed |
| `u40-author-full.C3_resume_without_run` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 50 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R25_digest_drops_the_folder` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 50 | 2 | killed |
| `r650-a.B1_searcher_drops_the_flag` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 67 | 1 | killed |
| `r650-a.B2_searcher_flags_a_decline` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 67 | 1 | killed |
| `r650-a.D2_too_coarse_as_source` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 67 | 2 | killed |
| `r791-a.S14_blocked_step` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 67 | 1 | killed |
| `u244.M20_discogs_named_only` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 101 | 1 | killed |
| `u244.M21_passed_over_rides_unread` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 101 | 4 | killed |
| `u282.D1_discogs_decline_ends_the_walk` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 9 | killed |
| `u282.D2_shop_decline_gives_way` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 1 | killed |
| `u282.D3_second_decline_named` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 1 | killed |
| `u282.D5_held_decline_dropped` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 141 | 6 | killed |
| `u282.L1_decline_lends_no_picture` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 1 | killed |
| `u282.L2_nobody_named_is_the_source` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 4 | killed |
| `u282.L3_shop_row_not_recorded` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 1 | killed |
| `u282.P1_no_picture_question` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 6 | killed |
| `u282.P3_answer_not_folded` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 4 | killed |
| `u282.P4_refusal_not_unread` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 2 | killed |
| `u282.P5_match_names_no_picture` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 3 | killed |
| `u282.P6_waiting_note_dropped` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 1 | killed |
| `u282.R1_rejection_raised_at_once` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 4 | killed |
| `u282.R2_any_refusal_held` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 1 | killed |
| `u282.R4_rejection_reads_as_no_token` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 40 | 2 | killed |
| `u289.S1_question_unused` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 167 | 28 | killed |
| `u289.S2_asked_not_carried` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 167 | 127 | killed |
| `u289.S5_shop_asked_head` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 167 | 4 | killed |
| `u289.S6_picture_asked_head` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 167 | 2 | killed |
| `u306.S1_shop_query` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 67 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R11_no_attempt_cap` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 67 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R13_query_unescaped` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 67 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R3_parse_break_folds_into_unreachable` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 67 | 2 | killed |
| `u56-catalogue-searcher-and-tag-workers.R5_bare_alias_lookup` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 67 | 24 | killed |
| `u85-b.B9_image_fetch_paced` | `src/cratekit/tagging/searchers.py` | user | 1 file(s) | 67 | 1 | killed |
| `r791-a.S10_track_unread_returned` | `src/cratekit/tagging/shops.py` | user | 1 file(s) | 67 | 2 | killed |
| `r791-a.S8_blocked_track_page_stops` | `src/cratekit/tagging/shops.py` | maintainer | 1 file(s) | 67 | 1 | killed |
| `u281.S1_beatport_reads_no_refusal` | `src/cratekit/tagging/shops.py` | user | 1 file(s) | 67 | 1 | killed |
| `u85-b.B1_beatport_resized` | `src/cratekit/tagging/shops.py` | user | 1 file(s) | 67 | 2 | killed |
| `u85-b.B2_edge_coefficient` | `src/cratekit/tagging/shops.py` | maintainer | 1 file(s) | 67 | 2 | killed |
| `u85-b.B3_picture_off_the_winning_row` | `src/cratekit/tagging/shops.py` | user | 1 file(s) | 67 | 1 | killed |
| `u85-b.B4_only_web_addresses` | `src/cratekit/tagging/shops.py` | user | 1 file(s) | 67 | 2 | killed |
| `u85-b.B5_bandcamp_original_size` | `src/cratekit/tagging/shops.py` | user | 1 file(s) | 67 | 2 | killed |
| `u85-b.B6_bandcamp_page_for_art` | `src/cratekit/tagging/shops.py` | user | 1 file(s) | 67 | 1 | killed |
| `u85-b.B7_listing_genre_wins` | `src/cratekit/tagging/shops.py` | user | 1 file(s) | 67 | 1 | killed |
| `u322.M01_stop_counts_partly_read` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 5 | killed |
| `u322.M02_stop_counts_passed_over` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 3 | killed |
| `u322.M03_partly_read_ignores_passed_over` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 1 | killed |
| `u322.M04_partly_read_reads_refusals` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 3 | killed |
| `u322.M05_not_sent_read_as_sent` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 2 | killed |
| `u322.M06_refused_row_drops_words` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 3 | killed |
| `u322.M07_refusal_words_dropped` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 3 | killed |
| `u322.M08_credential_counts` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 2 | killed |
| `u322.M09_token_row_asked_every_run` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 1 | killed |
| `u322.M10_old_answer_kept` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 3 | killed |
| `u322.M11_kept_words_lost` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 4 | killed |
| `u322.M12_digest_keeps_words` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 2 | killed |
| `u322.M13_beside_any_said_dropped` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 2 | killed |
| `u322.M14_token_rows_said_no_token` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 3 | killed |
| `u322.M15_counts_not_sent_as_asked` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 1 | killed |
| `u322.M16_counts_stopped_zero` | `src/cratekit/tagging/suggest.py` | user | 1 file(s) | 38 | 1 | killed |
| `u178.S1_summary_counts_labels` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 64 | 5 | killed |
| `u282.C3_label_genre_counted_as_owed` | `src/cratekit/tagging/summary.py` | user | 1 file(s) | 40 | 1 | killed |
| `r1476.M4_engine_ignores_folder_seam` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 64 | 2 | killed |
| `r1476.M5_tag_one_drops_folder_seam` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 64 | 2 | killed |
| `r1724.N11_tag_one_raw_stem` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 167 | 1 | killed |
| `u178-e9.E9_label_tag_reset` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.E2_no_search_with_picture` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 64 | 11 | killed |
| `u178.E3_art_refusal_tolerated` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.E4_isrc_withheld` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.E6_label_write_checked` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 64 | 1 | killed |
| `u178.E7_catalogue_write_checked` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 64 | 1 | killed |
| `u240.M3_tag_no_longer_outranks_the_line` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 64 | 15 | killed |
| `u240.M4_folder_label_no_longer_outranks_the_line` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 64 | 8 | killed |
| `u282.T1_question_asked_with_a_picture` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 40 | 1 | killed |
| `u282.T2_question_never_asked` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 40 | 4 | killed |
| `u282.T3_failed_question_raises` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 40 | 1 | killed |
| `u282.T4_failed_question_result_dropped` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 40 | 1 | killed |
| `u289.T1_title_tag_split` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 167 | 1 | killed |
| `u289.T2_split_artist_dropped` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 167 | 4 | killed |
| `u289.T3_record_read_from_title` | `src/cratekit/tagging/tag.py` | user | 1 file(s) | 167 | 3 | killed |
| `r1724.N6_tail_never_dropped` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 1 | killed |
| `r1724.N7_tail_word` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 1 | killed |
| `r1724.S1_u289_head_needs_a_key` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 3 | killed |
| `r1724.S2_u289_version_part` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 1 | killed |
| `u289.N2_head_alone_ambiguous` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 1 | killed |
| `u289.N3_three_parts_split` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 3 | killed |
| `u289.N4_version_title_split` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 1 | killed |
| `u289.N5_numbered_title_split` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 1 | killed |
| `u289.N6_track_number_artist_split` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 1 | killed |
| `u289.N7_numbered_artist_split` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 1 | killed |
| `u289.Q2_head_alone_two_parts` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 2 | killed |
| `u289.Q3_marker_kept` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 9 | killed |
| `u289.Q4_artist_part_kept` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 9 | killed |
| `u289.Q5_artist_part_needs_title` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 1 | killed |
| `u289.Q6_same_name_any_overlap` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 1 | killed |
| `u289.Q7_empty_title_asked` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 3 | killed |
| `u289.Q8_headless_read_past` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 167 | 1 | killed |
| `u318.T01_outcome_guard` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 1 | killed |
| `u318.T02_empty_title_part` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 1 | killed |
| `u318.T03_title_of_brackets` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 5 | killed |
| `u318.T04_after_is_later` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 1 | killed |
| `u318.T05_later_groups` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 1 | killed |
| `u318.T06_later_stretch` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 3 | killed |
| `u318.T07_track_number_before` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 2 | killed |
| `u318.T08_marker_before` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 1 | killed |
| `u318.T09_ends_in_version_word` | `src/cratekit/tagging/titles.py` | user | 2 file(s) | 505 | 4 | killed |
| `u318.T10_credit_group` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 4 | killed |
| `u318.T11_trailing_descriptions` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 2 | killed |
| `u318.T12_leading_fold` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 3 | killed |
| `u318.T13_name_joins` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 9 | killed |
| `u318.T14_accents` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 35 | killed |
| `u318.T15_rmx` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 2 | killed |
| `u318.T16_remaster_year` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 2 | killed |
| `u318.T17_alone_strict` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 9 | killed |
| `u318.T20_middle_dash_part` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 2 | killed |
| `u318.T21_unbracketed_suffix` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 3 | killed |
| `u324.F01_entry_o_slash` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 12 | killed |
| `u324.F02_entry_O_slash` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 1 | killed |
| `u324.F03_entry_ae` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 6 | killed |
| `u324.F04_entry_AE` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 1 | killed |
| `u324.F05_entry_oe` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 5 | killed |
| `u324.F06_entry_OE` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 1 | killed |
| `u324.F07_entry_sharp_s` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 3 | killed |
| `u324.F08_entry_d_stroke` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 5 | killed |
| `u324.F09_entry_D_stroke` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 1 | killed |
| `u324.F10_entry_l_stroke` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 5 | killed |
| `u324.F11_entry_L_stroke` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 1 | killed |
| `u324.F12_entry_thorn` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 5 | killed |
| `u324.F13_entry_THORN` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 1 | killed |
| `u324.F14_o_as_oe` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 13 | killed |
| `u324.F15_no_table` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 34 | killed |
| `u324.F16_table_before_nfkd` | `src/cratekit/tagging/titles.py` | user | 1 file(s) | 338 | 1 | killed |
| `u331.S11_vocals_imports_analysis_cli_at_top` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `r745-a.E10_text_not_cleaned` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 7 | killed |
| `r745-a.E11_any_path_encoded` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-a.E12_three_stars_moved` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-a.E13_siblings_by_identifier` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-a.E1_tombstone_row_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 16 | killed |
| `r745-a.E3_tombstone_playlist_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 4 | killed |
| `r745-a.E4_dangling_member_written` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 6 | killed |
| `r745-a.E5_empty_folder_self_closed` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 34 | killed |
| `r745-a.E6_tempo_constant_moved` | `src/cratekit/write/collection_export.py` | user | 1 file(s) | 94 | 2 | killed |
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
| `r1949.E1_missing_never` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 46 | 1 | killed |
| `r1949.E4_uncompared_filter_dropped` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 46 | 1 | killed |
| `r1949.E7_record_union_dropped` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 46 | 1 | killed |
| `r1949.E8_favorites_gap_unread` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 46 | 1 | killed |
| `r1949.N12_undeclared_pair_raises` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 46 | 4 | killed |
| `u119-c.C3_uncompared_still_compared` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 46 | 1 | killed |
| `u302.W7_two_candidates_chosen_by_position` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 82 | 1 | killed |
| `u302.W8_display_pair_keyed_on_the_folder_twice` | `src/cratekit/write/convergence_check.py` | user | 2 file(s) | 128 | 5 | killed |
| `u119-b.G12r_removed_namesake_written_into` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119-b.G5r_favorites_counted_as_members` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119-c.C2_torn_bucket_bound_anyway` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119-c.C5_interruption_unreported` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 4 | killed |
| `u119.G10_placements_no_gap` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 2 | killed |
| `u119.G11_stale_digest` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 2 | killed |
| `u119.G13_removals_when_not_asked` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 2 | killed |
| `u119.G15_removal_commit_admits_nothing` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 6 | killed |
| `u119.G1_class_undeclared` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 2 | killed |
| `u119.G4_removed_membership_live` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119.G6_wanted_is_members` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 14 | killed |
| `u119.G7_twin_folders_first_taken` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119.G9_digest_over_adds` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u132.G1_undeclared_cause` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 3 | 1 | killed |
| `u185.R4_genre_source` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u302.W15_landed_removals_recorded_as_zero` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u302.W18c_removed_nodes_planned` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u302.W19_emptied_source_mirrored` | `src/cratekit/write/genre_favorites.py` | user | 1 file(s) | 46 | 1 | killed |
| `u163.W17_first_active` | `src/cratekit/write/metadata.py` | user | 1 file(s) | 18 | 1 | killed |
| `u40-author-full.F2_genre_unknown_silent` | `src/cratekit/write/metadata.py` | user | 1 file(s) | 50 | 2 | killed |
| `u40-author-full.F3_policy_owns_more` | `src/cratekit/write/metadata.py` | user | 1 file(s) | 50 | 2 | killed |
| `u59.M1_permissive_default` | `src/cratekit/write/metadata.py` | user | 1 file(s) | 50 | 1 | killed |
| `u59.M2_refusal_removed` | `src/cratekit/write/metadata.py` | user | 1 file(s) | 50 | 1 | killed |
| `u59.M4_tombstone_resolves` | `src/cratekit/write/metadata.py` | user | 1 file(s) | 50 | 6 | killed |
| `u59.M5_first_row_wins` | `src/cratekit/write/metadata.py` | user | 1 file(s) | 50 | 3 | killed |
| `u59.M6_reason_reworded` | `src/cratekit/write/metadata.py` | user | 1 file(s) | 50 | 1 | killed |
| `u119-c.C4_favorites_beside_renamed_folder` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 46 | 1 | killed |
| `u119.R1_vox_unknown_by_id` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 46 | 2 | killed |
| `u119.R2_with_favorites_every_tree` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 46 | 1 | killed |
| `u246.R1_rebuild_set_per_placement` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 33 | 1 | killed |
| `u246.R3_rebuild_set_of_placements` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 46 | 2 | killed |
| `u246.R4_rebuild_membership_inverted` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 46 | 2 | killed |
| `r501-d.R2_settled_is_not_imported` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-d.R3_pass_is_proof` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 34 | 1 | killed |
| `r318.P1_withdrawn_branch_removed` | `src/cratekit/write/routing_pass.py` | user | 1 file(s) | 82 | 2 | killed |
| `r318.P3_unresolved_branch_removed` | `src/cratekit/write/routing_pass.py` | user | 1 file(s) | 82 | 1 | killed |
| `r318.P4_ambiguous_reads_not_imported` | `src/cratekit/write/routing_pass.py` | user | 1 file(s) | 82 | 1 | killed |
| `u155.W2_destination` | `src/cratekit/write/routing_pass.py` | user | 1 file(s) | 48 | 1 | killed |
| `u329.W2_watch_drops_roots` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 30 | 1 | killed |
| `u126.M1_half_is_a_majority` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 44 | 2 | killed |
| `u126.M2_plurality` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 44 | 3 | killed |
| `u126.M3_dead_rows_count` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 44 | 2 | killed |
| `u126.M4_least_common_first` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 44 | 4 | killed |
| `u126.M5_null_is_a_value` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 44 | 3 | killed |
| `u126.M6_any_text` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 44 | 2 | killed |
| `u111-b.B1_move_names_every_table` | `src/cratekit/write/trees.py` | user | 1 file(s) | 30 | 1 | killed |
| `u40-author-full.F4_tombstone_indexed` | `src/cratekit/write/trees.py` | user | 1 file(s) | 50 | 1 | killed |
| `u232.A9_fake_host_iter` | `tests/_host_processes.py` | maintainer | 1 file(s) | 9 | 1 | killed |
| `u326.W1_children_reads_lists` | `tests/_source_guards.py` | maintainer | 1 file(s) | 1021 | 1 | killed |
| `u326.W2_cache_by_identity` | `tests/_source_guards.py` | maintainer | 1 file(s) | 1021 | 11 | killed |
| `r658-a.C2_keychain_shared` | `tests/conftest.py` | user | 1 file(s) | 3 | 1 | killed |
| `r658-a.C4_recognition_shared` | `tests/conftest.py` | user | 1 file(s) | 3 | 1 | killed |
| `r658-a.C5_fetcher_shared` | `tests/conftest.py` | user | 1 file(s) | 3 | 1 | killed |
| `r926.C1_root_is_state_roots_only` | `tests/conftest.py` | maintainer | 3 file(s) | 285 | 11 | killed |
| `r926.C2_root_never_registered` | `tests/conftest.py` | maintainer | 4 file(s) | 311 | 30 | killed |
| `u232.A1_platform_stub` | `tests/conftest.py` | maintainer | 1 file(s) | 9 | 2 | killed |
| `u232.A2_pyrekordbox_stub` | `tests/conftest.py` | maintainer | 1 file(s) | 9 | 3 | killed |
| `u232.A3_stub_raise_exec` | `tests/conftest.py` | maintainer | 1 file(s) | 9 | 1 | killed |
| `u232.A4_tripwire_records` | `tests/conftest.py` | maintainer | 1 file(s) | 9 | 1 | killed |
| `u232.A5_tripwire_refuses` | `tests/conftest.py` | maintainer | 1 file(s) | 9 | 1 | killed |
| `u232.A7_tripwire_on_pids` | `tests/conftest.py` | maintainer | 1 file(s) | 9 | 1 | killed |
| `u232.A8_opt_in` | `tests/conftest.py` | maintainer | 1 file(s) | 9 | 3 | killed |
| `u312.D1_library_root_redirected` | `tests/conftest.py` | maintainer | 1 file(s) | 3 | 1 | killed |
| `u312.D2_live_provider_refused` | `tests/conftest.py` | maintainer | 1 file(s) | 3 | 1 | killed |
| `u312.P1_presence_cached_as_absent` | `tests/conftest.py` | maintainer | 2 file(s) | 256 | 9 | killed |
| `u326.R6_cyanite_refused` | `tests/conftest.py` | maintainer | 1 file(s) | 78 | 1 | killed |
| `u326.R9_host_process_tripwire` | `tests/conftest.py` | maintainer | 1 file(s) | 9 | 1 | killed |
| `u27-restore-cli-independent.I_H5_the_anti_vacuity_set_names_a_landed_verb` | `tests/test_cli_contract.py` | maintainer | 1 file(s) | 1021 | 1 | killed |
| `r1917.T1_outside_not_removed` | `tests/test_config_test_root.py` | maintainer | 1 file(s) | 1 | 1 | killed |
| `r1917.T2_allowance_not_narrowed` | `tests/test_config_test_root.py` | maintainer | 2 file(s) | 18 | 6 | killed |
| `r1917.T3_configuration_scratch_kept` | `tests/test_config_test_root.py` | maintainer | 1 file(s) | 1 | 1 | killed |
| `u329.D1_body_floor_four` | `tests/test_duplication.py` | maintainer | 1 file(s) | 31 | 1 | killed |
| `u329.D2_three_files_to_copy` | `tests/test_duplication.py` | maintainer | 1 file(s) | 31 | 4 | killed |
| `u329.D3_docstring_kept` | `tests/test_duplication.py` | maintainer | 1 file(s) | 31 | 1 | killed |
| `u329.D4_arguments_ignored` | `tests/test_duplication.py` | maintainer | 1 file(s) | 31 | 2 | killed |
| `u256.T1_existing_path_fallback` | `tests/test_rb_writer_db.py` | maintainer | 1 file(s) | 13 | 5 | killed |
| `u256.T2_sidecars_in_the_check` | `tests/test_rb_writer_db.py` | maintainer | 1 file(s) | 13 | 3 | killed |
| `u256.T3_key_carries_the_pin` | `tests/test_rb_writer_db.py` | maintainer | 1 file(s) | 13 | 1 | killed |
| `u256.T4_key_carries_the_variant` | `tests/test_rb_writer_db.py` | maintainer | 1 file(s) | 13 | 1 | killed |
| `u256.T5_template_kept` | `tests/test_rb_writer_db.py` | maintainer | 1 file(s) | 13 | 3 | killed |
| `u256.T7_wal_mode_kept` | `tests/test_rb_writer_db.py` | maintainer | 1 file(s) | 13 | 2 | killed |
| `u256.T8_private_copy_per_call` | `tests/test_rb_writer_db.py` | maintainer | 1 file(s) | 13 | 2 | killed |
| `u256.T9_copy_mode` | `tests/test_rb_writer_db.py` | maintainer | 1 file(s) | 13 | 1 | killed |
| `r658-d.D2_the_ban_looks_for_another_name` | `tests/test_isolation_survives_undo.py` | maintainer | 1 file(s) | 3 | 1 | killed |

## Row definitions

### `r263.W4_stale_suffix`

Drop the note that an earlier build's cursor no longer moves

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W4_stale_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
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

### `u322.M23_backlog_row_digest_keeps_words`

backlog.Row.digested: the backlog digest keeps the words

- File: `src/cratekit/tagging/backlog.py`
- Source: `u322.json`, row `M23_backlog_row_digest_keeps_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_backlog_rows_digest_leaves_the_words_out_and_its_envelope_keeps_them`

Old text:

```
            "catalogue": self.asked.digested() if self.asked else None,
        }
```

New text:

```
            "catalogue": self.asked.to_json() if self.asked else None,
        }
```

### `r791-a.S1_403_blocks`

_BLOCK_STATUSES: drop 403, so Traxsource's Cloudflare 403 reads as unreachable again

- File: `src/cratekit/tagging/catalogues.py`
- Source: `r791-a.json`, row `S1_403_blocks`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 4 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_beatport_miss_beside_two_blocked_fallbacks_is_not_a_no_hit`
  - `tests/test_catalogue_searcher.py::test_a_fallbacks_refusal_is_blocked_and_its_outage_unreachable[403 interstitial]`
  - `tests/test_catalogue_searcher.py::test_beatport_answering_403_is_blocked_like_the_fallbacks`
  - `tests/test_catalogue_searcher.py::test_three_refusals_raise_unreachable_and_say_the_fallbacks_were_blocked`

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
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 5 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_client_challenge_page_is_blocked_rather_than_a_miss`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_track_page_unread_is_not_a_miss[challenge]`
  - `tests/test_catalogue_searcher.py::test_a_beatport_miss_beside_two_blocked_fallbacks_is_not_a_no_hit`
  - `tests/test_catalogue_searcher.py::test_a_blocked_bandcamp_track_page_stops_the_walk_over_further_listings`
  - `tests/test_catalogue_searcher.py::test_three_refusals_raise_unreachable_and_say_the_fallbacks_were_blocked`

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
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
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
- Moved: the challenge check moved whole from tagging/searchers.py to tagging/catalogues.py with the shared matchers (U306); the test that killed it, test_cloudflare_challenge_machinery_in_the_body_blocks_whatever_the_title_says, is now the challenge script case of test_a_fallbacks_refusal_is_blocked_and_its_outage_unreachable in the same file, Cloudflare's interstitial retitled on a 200 from Traxsource and the same blocked answer
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
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

### `r791-a.S9_gone_track_page`

_GONE_STATUSES: empty, so a dead listing's 404 leaves the file unreachable for ever

- File: `src/cratekit/tagging/catalogues.py`
- Source: `r791-a.json`, row `S9_gone_track_page`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
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

### `u282.W1_walk_beatport_first`

WALK: Beatport first again, the order before the card

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u282.json`, row `W1_walk_beatport_first`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`
- Collected: 141 against a baseline of 141
- Kills: 32 (killed)
- Killed:
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
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_that_has_a_picture_sends_beatport_nothing`
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - ... and 17 more, see the JSON sidecar

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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_record_and_a_summary_list_discogs_first`

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
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 5 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_no_genre_spends_a_second_fetch_on_the_track_page`
  - `tests/test_catalogue_searcher.py::test_jitter_is_drawn_from_the_injected_random_source`
  - `tests/test_catalogue_searcher.py::test_the_image_fetch_is_paced_and_answers_the_bytes`
  - `tests/test_catalogue_searcher.py::test_the_pacer_sleeps_before_every_fetch_including_the_first`

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

### `u56-catalogue-searcher-and-tag-workers.R8_no_jitter`

Fixed intervals, so two runs that started together stay in step and trip the same limit together

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R8_no_jitter`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_jitter_is_drawn_from_the_injected_random_source`

Old text:

```
    jitter_fraction: float = JITTER_FRACTION
```

New text:

```
    jitter_fraction: float = 0.0
```

### `r1476.M10_no_name_slug_step`

_label_seam: drop the name slug step, so Some*Label no longer names Some Label

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M10_no_name_slug_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_tag_names_the_one_label_its_frozen_payload_answers_for[a-name-one-label-holds-exactly-is-never-lost-to-a-slug-it-shares]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[(Alpha)]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha.]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[\xc1lpha]`

Old text:

```
            named = tuple(entry for entry in held.labels.values() if _name_slug(entry.name) == wanted)
```

New text:

```
            named = ()
```

### `r1476.M11_slug_step_beats_exact_name`

_label_seam: run the name slug step even when a label is called the tag exactly

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M11_slug_step_beats_exact_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_tag_names_the_one_label_its_frozen_payload_answers_for[a-name-one-label-holds-exactly-is-never-lost-to-a-slug-it-shares]`

Old text:

```
        if not named and wanted:
            named = tuple(entry for entry in held.labels.values() if _name_slug(entry.name) == wanted)
```

New text:

```
        if wanted:
            named = tuple(entry for entry in held.labels.values() if _name_slug(entry.name) == wanted)
```

### `r1476.M12_no_identifier_fallback`

_label_seam: drop the identifier step, so a renamed label's old name reaches nothing

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M12_no_identifier_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_names_the_one_label_its_frozen_payload_answers_for[a-tag-is-read-as-a-name-before-an-identifier]`
  - `tests/test_label_genre.py::test_a_tag_names_the_one_label_its_frozen_payload_answers_for[by-its-name-its-slug-or-the-name-it-was-registered-under]`

Old text:

```
            named = tuple(entry for entry in (held.labels.get(wanted),) if entry is not None)
```

New text:

```
            named = ()
```

### `r1476.M13_needles_not_held`

_frozen_labels: hold only the labels with a genre, so a lookup falls through to another label

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M13_needles_not_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_tag_names_the_one_label_its_frozen_payload_answers_for[a-name-one-label-holds-exactly-is-never-lost-to-a-slug-it-shares]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ Alpha ]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[(Alpha)]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ALPHA]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha.]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[\xc1lpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[alpha]`

Old text:

```
    for rows in (needles if isinstance(needles, Mapping) else {}, frozen):
```

New text:

```
    for rows in (frozen,):
```

### `r1476.M14_genre_join_by_name`

_frozen_labels: give each frozen label the genre of the first label with a genre sharing its name

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M14_genre_join_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_the_folders_label_is_answered_by_its_frozen_identifier_whatever_it_is_called`

Old text:

```
                    genre=genres.get(str(label_id)),
```

New text:

```
                    genre=next((genres[other] for other, them in frozen.items() if other in genres and isinstance(them, Mapping) and them.get("name") == row.get("name")), None),
```

### `r1476.M15_answer_without_genre`

_answered: answer a label with no genre as one

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M15_answer_without_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_tag_names_the_one_label_its_frozen_payload_answers_for[a-tag-is-read-as-a-name-before-an-identifier]`
  - `tests/test_label_genre.py::test_a_tag_names_the_one_label_its_frozen_payload_answers_for[by-its-name-its-slug-or-the-name-it-was-registered-under]`
  - `tests/test_label_genre.py::test_the_folders_label_is_answered_by_its_frozen_identifier_whatever_it_is_called`

Old text:

```
    if entry is None or not entry.genre:
        return None
    return tag_engine.LabelAnswer
```

New text:

```
    if entry is None:
        return None
    return tag_engine.LabelAnswer
```

### `r1476.M16_unsluggable_raises`

_name_slug: let a name that could never be a label raise rather than read as none

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M16_unsluggable_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_tag_that_could_never_name_a_label_is_searched_and_never_fails`
  - `tests/test_label_genre.py::test_a_tag_names_the_one_label_its_frozen_payload_answers_for[by-its-name-its-slug-or-the-name-it-was-registered-under]`

Old text:

```
    except CratekitError:
        return ""


def _label_seam
```

New text:

```
    except CratekitError:
        raise


def _label_seam
```

### `r1476.M17_remedy_names_display_name`

_label_payload: the no genre remedy names the label by its display name

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M17_remedy_names_display_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_the_remedy_names_the_label_by_its_identifier`

Old text:

```
            handle = entry.label_id
```

New text:

```
            handle = entry.name
```

### `r1476.M18_remedy_head_never_shared`

_label_payload: never name the identifier beside a shared display name in the warning's head

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M18_remedy_head_never_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`

Old text:

```
            shared = len(held.named(entry.name)) > 1
```

New text:

```
            shared = False
```

### `r1476.M19_outranked_wording`

_label_warnings: the outranked warning no longer says a tag can name two labels

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M19_outranked_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`

Old text:

```
names two labels or "
```

New text:

```
names a retired label "
```

### `r1476.M1_identifier_not_frozen`

_label_payload: freeze the label's display name where its identifier goes, so the sweep answers --label by a name another label may share

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M1_identifier_not_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        frozen["label_id"] = entry.label_id
```

New text:

```
        frozen["label_id"] = entry.name
```

### `r1476.M2_folder_seam_by_name`

_folder_seam: look the folder's label up again by the name the engine hands it, the card's defect

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M2_folder_seam_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_the_folders_label_is_answered_by_its_frozen_identifier_whatever_it_is_called`

Old text:

```
        return _answered(held.labels.get(wanted))
```

New text:

```
        return _answered(held.by_name(_name) or held.labels.get(wanted))
```

### `r1476.M3_folder_seam_with_no_identifier`

_folder_seam: hand a seam for a job frozen with no identifier, so its --label answers nothing

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M3_folder_seam_with_no_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_frozen_with_no_identifier_reads_its_label_as_a_name`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`

Old text:

```
    if held is None or not wanted:
```

New text:

```
    if held is None:
```

### `r1476.M6_worker_hands_no_folder_seam`

handle: hand the engine no folder seam

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M6_worker_hands_no_folder_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        folder_genre=_folder_seam(payload),
```

New text:

```
        folder_genre=None,
```

### `r1476.M7_worker_hands_identifier_as_label`

handle: hand the engine the frozen identifier as the folder's label text, round one's shape

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M7_worker_hands_identifier_as_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`

Old text:

```
        label=str(payload.get("label") or "") or None,
```

New text:

```
        label=str(payload.get("label_id") or "") or None,
```

### `r1476.M8_shared_name_takes_first`

_label_seam: a name two labels hold answers the first holder

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M8_shared_name_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_tag_names_the_one_label_its_frozen_payload_answers_for[a-name-one-label-holds-exactly-is-never-lost-to-a-slug-it-shares]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ Alpha ]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[(Alpha)]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ALPHA]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha.]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[\xc1lpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[alpha]`

Old text:

```
        return _answered(named[0]) if len(named) == 1 else None
```

New text:

```
        return _answered(named[0]) if named else None
```

### `r1476.M9_identifier_first`

_label_seam: read a tag as an identifier before a name, round one's blockers

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M9_identifier_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_tag_names_the_one_label_its_frozen_payload_answers_for[a-tag-is-read-as-a-name-before-an-identifier]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[alpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`

Old text:

```
        named = held.named(name)
        wanted = _name_slug(name)
```

New text:

```
        named = tuple(entry for entry in (held.labels.get(name),) if entry is not None) or held.named(name)
        wanted = _name_slug(name)
```

### `u178.S2_unknown_label_refused`

_label_payload: a --label nobody registered queues the sweep with no label

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S2_unknown_label_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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

### `u192.T1_typed_label_on_queue`

tag_folder: hand the queue's own --label to the resume, so a sweep driven at its queue says its label was not applied

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T1_typed_label_on_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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

### `u192.T4_tag_queue_only_ignored`

tag_folder: ignore --queue-only and drive the sweep

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T4_tag_queue_only_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_an_unreadable_registry_warns_and_refuses_only_a_sweep_that_named_a_label`
  - `tests/test_label_genre.py::test_the_remedy_names_the_label_by_its_identifier`

Old text:

```
        if foreground.queue_only(ctx.args):
```

New text:

```
        if False:
```

### `u289.C1_record_drops_asked`

the sweep's record leaves the question's read out

- File: `src/cratekit/tagging/cli.py`
- Source: `u289.json`, row `C1_record_drops_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
  - `tests/test_cyanite_trial.py::test_a_send_without_a_cap_and_a_price_that_allow_it_refuses_before_anything_is_sent[no-cap]`

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
  - `tests/test_cyanite_trial.py::test_a_send_without_a_cap_and_a_price_that_allow_it_refuses_before_anything_is_sent[a-count-over-a-cap-of-3]`

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
  - `tests/test_cyanite_trial.py::test_a_send_without_a_cap_and_a_price_that_allow_it_refuses_before_anything_is_sent[no-price]`

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
  - `tests/test_cyanite_trial.py::test_a_declared_cyanite_vocabulary_answers_before_the_aliases`
  - `tests/test_cyanite_trial.py::test_a_file_retagged_between_two_runs_is_not_paid_for_again`
  - `tests/test_cyanite_trial.py::test_a_file_that_is_not_an_mp3_is_listed_and_never_sent`
  - `tests/test_cyanite_trial.py::test_a_folder_moved_between_two_runs_is_not_paid_for_again`
  - `tests/test_cyanite_trial.py::test_a_run_with_nothing_to_send_leaves_an_empty_table_and_asks_nothing`
  - `tests/test_cyanite_trial.py::test_a_run_writes_each_files_folder_beside_cyanites_and_the_agreement`
  - `tests/test_cyanite_trial.py::test_a_send_without_a_cap_and_a_price_that_allow_it_refuses_before_anything_is_sent[a-count-over-a-cap-of-0]`
  - `tests/test_cyanite_trial.py::test_a_send_without_a_cap_and_a_price_that_allow_it_refuses_before_anything_is_sent[a-count-over-a-cap-of-3]`
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

### `u244.M01_no_token_not_asked`

DiscogsAsker.ask: answer MISS for a searcher with no token instead of not-asked, so a sweep with no token records no-hit

- File: `src/cratekit/tagging/discogs.py`
- Source: `u244.json`, row `M01_no_token_not_asked`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 8 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_file_swept_without_a_token_is_sources_unread_not_no_hit`
  - `tests/test_discogs_searcher.py::test_a_recorded_token_the_keychain_lost_is_not_asked_and_says_so`
  - `tests/test_discogs_searcher.py::test_a_searcher_built_with_no_asker_has_no_token_and_reads_no_keychain`
  - `tests/test_discogs_searcher.py::test_a_walk_that_asked_nothing_is_a_decline_naming_what_it_passed_over`
  - `tests/test_discogs_searcher.py::test_beatport_unreachable_and_discogs_unasked_refuse_as_an_outage_naming_the_token`
  - `tests/test_discogs_searcher.py::test_no_recorded_token_reads_no_keychain_and_is_not_asked`
  - `tests/test_discogs_searcher.py::test_no_token_is_not_asked_with_how_to_record_one_and_never_no_hit`
  - `tests/test_discogs_searcher.py::test_the_general_catalogue_is_still_asked_beside_an_unasked_discogs`

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
- Moved: DiscogsAsker moved verbatim from tagging/searchers.py to tagging/discogs.py, where the text occurs once, in DiscogsAsker.ask; the identical line in tagging/cyanite.py is Cyanite's own guard and not this one
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_rejected_token_is_not_sent_again_in_the_run`

Old text:

```
        if self.rejected is not None:
```

New text:

```
        if False:
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
- Moved: DiscogsAsker's release walk moved whole from tagging/searchers.py to tagging/discogs.py (U306); the test that killed it, test_a_gone_release_is_passed_over, was folded into test_a_release_is_taken_only_when_a_track_and_its_artist_match in the same file, and its only gone assertion is now that test's only gone case, the same 404 page and the same miss
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
- Moved: DiscogsAsker's release walk moved whole from tagging/searchers.py to tagging/discogs.py (U306); the test that killed it, test_a_styleless_match_beside_an_unread_pressing_is_unread_not_a_match, is now the styleless beside unread case of test_a_release_is_taken_only_when_a_track_and_its_artist_match in the same file, a styleless release beside a 503 and the same unreachable answer
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

### `u283.D6_said_unscrubbed`

_said: a note is no longer scrubbed of the token, the check's only scrub since round one

- File: `src/cratekit/tagging/discogs.py`
- Source: `u283.json`, row `D6_said_unscrubbed`
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
        return SourceOutcome(DISCOGS, answer, note=self._scrub(note))
```

New text:

```
        return SourceOutcome(DISCOGS, answer, note=note)
```

### `u289.S4_discogs_asked_head`

DiscogsAsker._search: ask the track field with the file's own text

- File: `src/cratekit/tagging/discogs.py`
- Source: `u289.json`, row `S4_discogs_asked_head`
- Moved: the same text, now in src/cratekit/tagging/discogs.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_version.py`
- Collected: 505 against a baseline of 505
- Kills: 33 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[Sunrise Mood (Mike's (Dub) Mix)-Sunrise Mood]`
  - `tests/test_discogs_version.py::test_a_different_spelling_is_still_another_maker[Stra\xdfe-Strase]`
  - `tests/test_discogs_version.py::test_a_different_spelling_is_still_another_maker[Trentem\xf8ller-Trentemoeller]`
  - `tests/test_discogs_version.py::test_a_different_spelling_is_still_another_maker[\u0110or\u0111e-Dorje]`
  - `tests/test_discogs_version.py::test_a_different_spelling_is_still_another_maker[\xc6ther-Ather]`
  - `tests/test_discogs_version.py::test_a_different_spelling_is_still_another_maker[\xde\xf3r-Tor]`
  - `tests/test_discogs_version.py::test_a_mix_named_by_a_word_no_list_holds_is_read_as_its_makers`
  - `tests/test_discogs_version.py::test_a_refused_release_gives_way_to_a_later_one_that_carries_the_mix`
  - `tests/test_discogs_version.py::test_a_release_is_taken_only_for_the_version_it_writes[main-named-mix]`
  - `tests/test_discogs_version.py::test_a_release_is_taken_only_for_the_version_it_writes[named-vocal-mix-plain]`
  - `tests/test_discogs_version.py::test_a_release_is_taken_only_for_the_version_it_writes[remix-of-plain-and-other]`
  - `tests/test_discogs_version.py::test_a_title_naming_two_mixes_lists_them_in_order_in_the_note`
  - `tests/test_discogs_version.py::test_an_article_is_folded_out_of_a_makers_name_on_both_sides`
  - `tests/test_discogs_version.py::test_an_unread_release_beside_a_version_refusal_is_unread_not_a_miss`
  - `tests/test_discogs_version.py::test_another_maker_is_still_a_version_miss_with_the_note`
  - ... and 18 more, see the JSON sidecar

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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
- Kills: 14 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_refused_release_gives_way_to_a_later_one_that_carries_the_mix`
  - `tests/test_discogs_version.py::test_an_unread_release_beside_a_version_refusal_is_unread_not_a_miss`
  - `tests/test_discogs_version.py::test_the_miss_names_a_release_refused_on_its_tracks_alone_or_its_title_alone`
  - `tests/test_discogs_version.py::test_the_miss_names_every_release_refused_for_its_version_and_no_other`
  - `tests/test_discogs_version.py::test_the_refused_file_is_left_untagged_with_the_reason_in_its_record`
  - `tests/test_discogs_version.py::test_the_single_fallback_reads_no_other_track_of_the_release_as_the_mix`
  - `tests/test_discogs_version.py::test_the_single_fallback_takes_only_a_release_that_writes_the_version[refuses-a-one-track-original]`
  - `tests/test_discogs_version.py::test_the_single_fallback_takes_only_a_release_that_writes_the_version[refuses-a-one-track-release-of-the-title]`
  - `tests/test_discogs_version.py::test_the_single_fallback_takes_only_a_release_that_writes_the_version[refuses-another-version-alone]`
  - `tests/test_discogs_version.py::test_the_single_fallback_takes_only_a_release_that_writes_the_version[refuses-its-own-title-writing-other]`
  - `tests/test_discogs_version.py::test_the_sitting_files_refuse_a_release_that_lacks_their_mix[headed-mita-gami]`
  - `tests/test_discogs_version.py::test_the_sitting_files_refuse_a_release_that_lacks_their_mix[headed-tim-green]`
  - `tests/test_discogs_version.py::test_the_sitting_files_refuse_a_release_that_lacks_their_mix[the-mita-gami-extended-mix-refuses-the-16bl-remix-single]`
  - `tests/test_discogs_version.py::test_the_sitting_files_refuse_a_release_that_lacks_their_mix[the-tim-green-remix-refuses-a-release-of-four-other-mixes]`

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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_the_single_fallback_reads_no_other_track_of_the_release_as_the_mix`
  - `tests/test_discogs_version.py::test_the_single_fallback_takes_only_a_release_that_writes_the_version[takes-a-track-of-the-version]`

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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
- Kills: 8 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_plain_miss_still_carries_no_note`
  - `tests/test_discogs_version.py::test_a_title_naming_two_mixes_lists_them_in_order_in_the_note`
  - `tests/test_discogs_version.py::test_another_maker_is_still_a_version_miss_with_the_note`
  - `tests/test_discogs_version.py::test_the_miss_names_a_release_refused_on_its_tracks_alone_or_its_title_alone`
  - `tests/test_discogs_version.py::test_the_miss_names_every_release_refused_for_its_version_and_no_other`
  - `tests/test_discogs_version.py::test_the_refused_file_is_left_untagged_with_the_reason_in_its_record`
  - `tests/test_discogs_version.py::test_the_sitting_files_refuse_a_release_that_lacks_their_mix[the-mita-gami-extended-mix-refuses-the-16bl-remix-single]`
  - `tests/test_discogs_version.py::test_the_sitting_files_refuse_a_release_that_lacks_their_mix[the-tim-green-remix-refuses-a-release-of-four-other-mixes]`

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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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

### `u244.M23_published_waits_for_discogs`

second_opinion: ask the general catalogue while Discogs was asked and unread

- File: `src/cratekit/tagging/published.py`
- Source: `u244.json`, row `M23_published_waits_for_discogs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_the_general_catalogue_waits_for_a_discogs_that_was_asked_and_unread`

Old text:

```
        if discogs is not None and discogs.answer in UNREAD:
```

New text:

```
        if False:
```

### `u322.M17_deezer_gate_open_always`

second_opinion: the flag is ignored, so tag folder asks Deezer past a refusing Beatport too

- File: `src/cratekit/tagging/published.py`
- Source: `u322.json`, row `M17_deezer_gate_open_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_tag_folders_gate_is_unchanged`

Old text:

```
            and not (past_a_refusing_shop and _refused_beside_discogs(first, hit))
```

New text:

```
            and not _refused_beside_discogs(first, hit)
```

### `u322.M18_deezer_past_an_outage`

_refused_beside_discogs: any unread Beatport lets Deezer be asked, an outage included

- File: `src/cratekit/tagging/published.py`
- Source: `u322.json`, row `M18_deezer_past_an_outage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_deezer_still_waits_for_a_beatport_that_is_down_rather_than_refusing[parse-break]`
  - `tests/test_catalogue_walk_refusal.py::test_deezer_still_waits_for_a_beatport_that_is_down_rather_than_refusing[unreachable]`

Old text:

```
    if beatport.answer != Answer.BLOCKED.value:
        return False
```

New text:

```
    if beatport.answer not in UNREAD:
        return False
```

### `u322.M19_suggest_binder_flag_off`

for_suggestions: the binder does not ask past a refusing Beatport, so Deezer is asked about no row

- File: `src/cratekit/tagging/published.py`
- Source: `u322.json`, row `M19_suggest_binder_flag_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_the_suggest_binder_is_built_over_the_one_lookup`

Old text:

```
    return second_opinion(declared, lookup=for_lookup(), past_a_refusing_shop=True)
```

New text:

```
    return second_opinion(declared, lookup=for_lookup(), past_a_refusing_shop=False)
```

### `r1103.S1_answer_too_coarse`

Sample of the unit's existing guards: retag_one writes an answer the taxonomy calls too coarse

- File: `src/cratekit/tagging/retag.py`
- Source: `r1103.json`, row `S1_answer_too_coarse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_accepted_answer_that_is_itself_a_catch_all_is_still_refused`
  - `tests/test_genre_retag.py::test_an_answer_that_is_itself_a_catch_all_is_refused_and_the_file_is_untouched`

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
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
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
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
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
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`
  - `tests/test_genre_retag.py::test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run`
  - `tests/test_genre_retag.py::test_an_unwritten_file_never_reaches_the_library_plan`

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
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`
  - `tests/test_genre_retag.py::test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run`

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
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`
  - `tests/test_genre_retag.py::test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run`

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
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`
  - `tests/test_genre_retag.py::test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run`

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
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
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
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`

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

### `u40-author-full.D2_ambiguous_written`

Take the first of two live rows on one location instead of surfacing the collision

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `D2_ambiguous_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_two_live_rows_on_one_location_are_surfaced_rather_than_written_to_both`

Old text:

```
        if match.outcome is not trees.MatchOutcome.MATCHED or match.content_id is None:
```

New text:

```
        if match.content_id is None and not match.content_ids:
```

### `u40-author-full.D4_absent_row_silent`

Drop the row-absent skips, so a matched row the caller did not supply vanishes from the plan

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `D4_absent_row_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_matched_row_the_caller_did_not_supply_is_surfaced_rather_than_silent`

Old text:

```
    if absent:
        plan = metadata.Plan(
            plan.owner,
            plan.changes,
            plan.skipped + tuple(metadata.Skipped(cid, "row-absent") for cid in absent),
        )

```

New text:

```
(empty)
```

### `u40-author-full.D5_no_enable`

Do not register the operation, so every change decides SKIP_UNOWNED and the sweep reports a clean run over a library it did not touch

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `D5_no_enable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 5 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_live_namesake_behind_a_tombstone_is_still_found_through_the_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`
  - `tests/test_genre_retag.py::test_a_written_file_is_relinked_to_the_existing_genre_row`
  - `tests/test_genre_retag.py::test_an_unregistered_operation_writes_nothing_and_the_apply_is_what_prevents_it`
  - `tests/test_genre_retag.py::test_re_applying_a_plan_over_an_already_linked_row_is_a_no_op`

Old text:

```
    metadata.enable((metadata.RETAG_GENRE,))
    metadata.assert_within_policy(library_plan.plan)
```

New text:

```
    metadata.assert_within_policy(library_plan.plan)
```

### `u40-author-full.D6_no_policy_assert`

Drop the policy refusal, so a plan naming an unowned field writes nothing and reports success

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `D6_no_policy_assert`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_apply_refuses_a_field_the_retag_policy_does_not_own`

Old text:

```
    metadata.enable((metadata.RETAG_GENRE,))
    metadata.assert_within_policy(library_plan.plan)
    return metadata.write_plan(library_plan.plan, mapped)
```

New text:

```
    metadata.enable((metadata.RETAG_GENRE,))
    return metadata.write_plan(library_plan.plan, mapped)
```

### `u40-author-full.D7_unmatched_dropped`

Do not surface a written file no row claims, so a half-applied sweep reports as a full one

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `D7_unmatched_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_soft_deleted_row_is_never_retagged`
  - `tests/test_genre_retag.py::test_a_written_file_no_live_row_claims_is_surfaced_rather_than_dropped`
  - `tests/test_genre_retag.py::test_two_live_rows_on_one_location_are_surfaced_rather_than_written_to_both`

Old text:

```
            unmatched.append(
                Unmatched(
                    path=str(result.path),
                    outcome=str(match.outcome.value),
                    content_ids=tuple(match.content_ids),
                )
            )
            continue
```

New text:

```
            continue
```

### `u40-author-full.D8_contested_last_wins`

Let a second file claiming one row overwrite the first, so whichever came last decides the row and the report names both as written

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `D8_contested_last_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_two_written_files_resolving_to_one_row_are_both_surfaced_and_neither_wins`

Old text:

```
        if content_id in claimed_by:
            contested.add(content_id)
            unmatched.append(
                Unmatched(path=str(result.path), outcome="contested", content_ids=(content_id,))
            )
            continue

```

New text:

```
(empty)
```

### `u40-author-full.D9_contested_first_still_written`

Remove only the second layer, so the second claimant is surfaced and the FIRST one is still written to the contested row

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `D9_contested_first_still_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_two_written_files_resolving_to_one_row_are_both_surfaced_and_neither_wins`

Old text:

```
    for content_id in sorted(contested):
        genres.pop(content_id, None)
        unmatched.append(
            Unmatched(path=claimed_by[content_id], outcome="contested", content_ids=(content_id,))
        )

```

New text:

```
(empty)
```

### `u40-author-full.P10_resolved_not_read`

Read only unresolved items out of the queue, so a settled verdict is invisible and re-asked

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `P10_resolved_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 5 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_settled_against_every_candidate_is_not_counted_as_an_open_question`
  - `tests/test_genre_retag.py::test_a_rejected_verdict_leaves_the_file_alone_and_asks_nobody`
  - `tests/test_genre_retag.py::test_a_resolved_verdict_is_used_and_the_searcher_is_never_asked_again`
  - `tests/test_genre_retag.py::test_an_accepted_answer_that_is_itself_a_catch_all_is_still_refused`
  - `tests/test_genre_retag.py::test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run`

Old text:

```
        for item in review.iter_items(store, predicate=predicate, include_resolved=True)
```

New text:

```
        for item in review.iter_items(store, predicate=predicate)
```

### `u40-author-full.P6_option_id_as_genre`

Return the bucket identifier rather than its display name, so the tag written is an id

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `P6_option_id_as_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_resolved_verdict_is_used_and_the_searcher_is_never_asked_again`
  - `tests/test_genre_retag.py::test_an_accepted_answer_that_is_itself_a_catch_all_is_still_refused`
  - `tests/test_genre_retag.py::test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run`

Old text:

```
        detail = option.detail or {}
        return str(detail.get("genre") or option.summary or "").strip()
```

New text:

```
        return str(option.option_id).strip()
```

### `u40-author-full.P7_coarse_offered`

Offer every bucket including the fallback, so a person can choose the catch-all the write then refuses

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `P7_coarse_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_offered_candidates_are_the_declared_buckets_and_never_a_catch_all`

Old text:

```
        if not declared.is_too_coarse_as_source(bucket.display)
```

New text:

```
        if bucket.display
```

### `u40-author-full.P9_settled_counted_as_asked`

Count any result carrying an item id as an open question, so a decision a person already made is reported back to them as work waiting

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `P9_settled_counted_as_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_settled_against_every_candidate_is_not_counted_as_an_open_question`
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`

Old text:

```
            if result.item_id and result.reason in {NO_ANSWER, ANSWER_TOO_COARSE}
```

New text:

```
            if result.item_id and not result.written
```

### `u40-author-full.S1_blank_selected`

Drop the blank-genre exclusion, so a file with no genre becomes this verb's candidate as well as tag.folder's

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `S1_blank_selected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_file_with_no_genre_is_passed_over_rather_than_selected`
  - `tests/test_genre_retag.py::test_a_second_run_over_a_corrected_folder_selects_nothing`

Old text:

```
        if not current:
            # tag.folder's, under fill-if-empty. See the module docstring.
            passed.append(Passed(path=path, reason=NO_GENRE))
            continue

```

New text:

```
(empty)
```

### `u40-author-full.S2_specific_selected`

Invert the too-coarse predicate, so a curated genre is selected and a catch-all is not

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `S2_specific_selected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 19 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_catch_all_gets_a_specific_answer_and_the_taxonomy_recognises_it`
  - `tests/test_genre_retag.py::test_a_declared_catch_all_is_selected_and_a_specific_genre_is_not`
  - `tests/test_genre_retag.py::test_a_declined_answer_lands_in_the_review_queue`
  - `tests/test_genre_retag.py::test_a_file_settled_against_every_candidate_is_not_counted_as_an_open_question`
  - `tests/test_genre_retag.py::test_a_file_that_will_not_take_its_answer_is_reported_unwritten_and_the_rest_corrected`
  - `tests/test_genre_retag.py::test_a_padded_catch_all_reaches_the_selection_already_trimmed`
  - `tests/test_genre_retag.py::test_a_pass_with_no_store_reports_what_it_could_not_settle`
  - `tests/test_genre_retag.py::test_a_rejected_verdict_leaves_the_file_alone_and_asks_nobody`
  - `tests/test_genre_retag.py::test_a_resolved_verdict_is_used_and_the_searcher_is_never_asked_again`
  - `tests/test_genre_retag.py::test_a_second_run_offers_one_item_rather_than_a_second`
  - `tests/test_genre_retag.py::test_a_second_run_over_a_corrected_folder_selects_nothing`
  - `tests/test_genre_retag.py::test_an_accepted_answer_that_is_itself_a_catch_all_is_still_refused`
  - `tests/test_genre_retag.py::test_an_accepted_verdict_a_file_will_not_take_is_unwritten_and_kept_for_the_next_run`
  - `tests/test_genre_retag.py::test_an_answer_that_is_itself_a_catch_all_is_refused_and_the_file_is_untouched`
  - `tests/test_genre_retag.py::test_the_item_id_this_pass_computes_is_the_one_the_queue_stores`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        if not declared.is_too_coarse_as_source(current):
```

New text:

```
        if declared.is_too_coarse_as_source(current):
```

### `u40-author-full.S3_unsorted_walk`

Walk the folder unsorted, so the plan digest depends on directory order

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `S3_unsorted_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_selection_is_sorted_so_one_unchanged_folder_digests_the_same_twice`

Old text:

```
    for path in sorted(root.rglob("*")):
```

New text:

```
    for path in root.rglob("*"):
```

### `u40-author-full.S6_plan_drops_current`

Drop the current value from the plan row, so the person confirms a list of paths with nothing to judge

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `S6_plan_drops_current`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_plan_carries_the_current_value_so_the_person_sees_what_is_being_replaced`

Old text:

```
        {"path": str(candidate.path), "current": candidate.current}
```

New text:

```
        {"path": str(candidate.path)}
```

### `u40-author-round-2.D1_plan_from_selection`

Round one zero, and the most useful row in the table. Plan from every result rather than from what was written; the assertion that missed it asserted an empty change list, which the mutation also produces by a different mechanism

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-round-2.json`, row `D1_plan_from_selection`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unwritten_file_never_reaches_the_library_plan`
  - `tests/test_genre_retag.py::test_the_plan_is_built_from_what_was_written_and_never_from_the_selection`

Old text:

```
    written = outcome.written
```

New text:

```
    written = outcome.results
```

### `u40-author-round-2.P5_verdict_not_checked`

Round one zero, now guarded directly. Accept a REJECTED item's chosen option as an answer, so every rejection reads as an acceptance

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-round-2.json`, row `P5_verdict_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_rejected_items_chosen_option_is_not_an_answer`

Old text:

```
    if item.verdict is not review.Verdict.ACCEPTED or not item.option:
```

New text:

```
    if not item.option:
```

### `u40-author-round-2.P8_identity_key`

Round one zero, now guarded. Address a review item by a different key, so every item any earlier build offered is orphaned

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-round-2.json`, row `P8_identity_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_review_item_is_addressed_by_the_file_path_under_that_exact_name`

Old text:

```
    return {"path": str(path)}
```

New text:

```
    return {"file": str(path)}
```

### `r185-r246-author.E1_plan_gate_by_position`

Index gates[0] instead of searching by digest source, the guard the repaired case in test_genre_retag.py measures

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r185-r246-author.json`, row `E1_plan_gate_by_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
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
    for spec in ctx.entry.gates[:1]:
        return spec
```

### `r290-author.R1_retag_rebuild_drops_the_type`

Rebuild the retag refusal as a plain CratekitError again, so a retag parked after correcting a file says failed

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r290-author.json`, row `R1_retag_rebuild_drops_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`

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

### `u40-author-full.C1_gate_by_position`

Take gates[0] rather than the gate declared against the plan, so a reordered tuple answers the wrong question

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u40-author-full.json`, row `C1_gate_by_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
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
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
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

### `u40-author-full.C3_resume_without_run`

Drop --run from the resume argv, so the job driver's child meets the explicit gate with nothing recorded and stalls for ever

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u40-author-full.json`, row `C3_resume_without_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_resume_argv_carries_the_folder_the_job_and_the_gate_run`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
```

New text:

```
    resume = []
```

### `u56-catalogue-searcher-and-tag-workers.R25_digest_drops_the_folder`

Two different empty folders digest identically, so a decision recorded against one satisfies the gate for the other

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R25_digest_drops_the_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_shell_digests_the_selection_and_the_folder_rather_than_a_constant`
  - `tests/test_genre_retag.py::test_two_different_empty_folders_digest_differently_through_the_pure_function`

Old text:

```
            FOLDER_KEY: folder,
            ITEMS_KEY: [dict(row) for row in items],
```

New text:

```
            ITEMS_KEY: [dict(row) for row in items],
```

### `r650-a.B1_searcher_drops_the_flag`

The hit never carries the flag, so nothing above the resolver can see it

- File: `src/cratekit/tagging/searchers.py`
- Source: `r650-a.json`, row `B1_searcher_drops_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[unknown word]`

Old text:

```
        off_taxonomy=tag is not None and suggestion.off_taxonomy,
```

New text:

```
        off_taxonomy=False,
```

### `r650-a.B2_searcher_flags_a_decline`

A pass through the taxonomy calls too coarse carries the flag as well as declining

- File: `src/cratekit/tagging/searchers.py`
- Source: `r650-a.json`, row `B2_searcher_flags_a_decline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_an_unknown_source_genre_a_taxonomy_calls_too_coarse_is_a_plain_decline`

Old text:

```
        off_taxonomy=tag is not None and suggestion.off_taxonomy,
```

New text:

```
        off_taxonomy=suggestion.off_taxonomy,
```

### `r650-a.D2_too_coarse_as_source`

Existing: an answer too coarse to be a final tag is a decline, not a hit

- File: `src/cratekit/tagging/searchers.py`
- Source: `r650-a.json`, row `D2_too_coarse_as_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it[acapella]`
  - `tests/test_catalogue_searcher.py::test_an_unknown_source_genre_a_taxonomy_calls_too_coarse_is_a_plain_decline`

Old text:

```
    if suggestion.declined or not tag or declared.is_too_coarse_as_source(tag):
```

New text:

```
    if suggestion.declined or not tag:
```

### `r791-a.S14_blocked_step`

_decide: the unreachable refusal never says a fallback was blocked

- File: `src/cratekit/tagging/searchers.py`
- Source: `r791-a.json`, row `S14_blocked_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
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

### `u244.M20_discogs_named_only`

_resolved: choose Discogs' style without requiring an exact folder declaration

- File: `src/cratekit/tagging/searchers.py`
- Source: `u244.json`, row `M20_discogs_named_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_discogs_chooses_only_a_named_folder_even_on_a_copy_with_no_table`

Old text:

```
        picked = choose_word(declared, outcome.words, source=outcome.source, named_only=True)
```

New text:

```
        picked = choose_word(declared, outcome.words, source=outcome.source, named_only=False)
```

### `u244.M21_passed_over_rides_unread`

_unread_sources: leave a source passed over for want of a token out of unread, so the file reads no-hit

- File: `src/cratekit/tagging/searchers.py`
- Source: `u244.json`, row `M21_passed_over_rides_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`
- Collected: 101 against a baseline of 101
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_searcher.py::test_a_file_swept_without_a_token_is_sources_unread_not_no_hit`
  - `tests/test_discogs_searcher.py::test_a_walk_that_asked_nothing_is_a_decline_naming_what_it_passed_over`
  - `tests/test_discogs_searcher.py::test_no_token_is_not_asked_with_how_to_record_one_and_never_no_hit`
  - `tests/test_discogs_searcher.py::test_the_general_catalogue_is_still_asked_beside_an_unasked_discogs`

Old text:

```
    ) + tuple(skipped.source for skipped in passed)
```

New text:

```
    )
```

### `u282.D1_discogs_decline_ends_the_walk`

search: a Discogs decline is returned at once, so Beatport is never asked after an unmapped style (merge blocker 2)

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `D1_discogs_decline_ends_the_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_record_shop_decline_still_ends_an_explicit_walk`

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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
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
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`
- Collected: 141 against a baseline of 141
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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
- Kills: 6 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_misses_names_no_picture_and_no_unread`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_refuses_is_unread_and_counts_toward_the_stop`
  - `tests/test_discogs_first.py::test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread`
  - `tests/test_discogs_first.py::test_a_tagged_file_with_no_picture_keeps_its_genre_and_gets_the_cover`

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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_misses_names_no_picture_and_no_unread`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_refuses_is_unread_and_counts_toward_the_stop`

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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_tagged_file_with_no_picture_keeps_its_genre_and_gets_the_cover`

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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_401_is_sent_once_and_beatport_decides_every_file`
  - `tests/test_discogs_first.py::test_a_beatport_decline_beside_a_refused_token_is_a_decline_and_never_raises`
  - `tests/test_discogs_first.py::test_a_tagged_file_still_gets_its_cover_when_the_token_is_refused`
  - `tests/test_discogs_first.py::test_a_token_refused_on_its_shape_still_lets_beatport_decide_and_lend_its_cover`

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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_beatport_decline_beside_a_refused_token_is_a_decline_and_never_raises`
  - `tests/test_discogs_first.py::test_a_token_refused_on_its_shape_still_lets_beatport_decide_and_lend_its_cover`

Old text:

```
                        NotAsked(DISCOGS, f"{DISCOGS_TOKEN_REFUSED}{refusal.cause.message}")
```

New text:

```
                        NotAsked(DISCOGS, DISCOGS_NO_TOKEN)
```

### `u289.S1_question_unused`

catalogue_searcher: ask every source the file's own text, the head included, as main did

- File: `src/cratekit/tagging/searchers.py`
- Source: `u289.json`, row `S1_question_unused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_an_artist_and_title_that_need_escaping_reach_the_seam_as_a_quoted_url`

Old text:

```
            artist, title, fetch=touch, pacer=pacer, declared=declared, track=track, query=_query
```

New text:

```
            artist, title, fetch=touch, pacer=pacer, declared=declared, track=track, query=lambda *parts: " ".join(parts)
```

### `u56-catalogue-searcher-and-tag-workers.R11_no_attempt_cap`

One attempt per fetch, so a single 429 is unreachable and a source that would have answered on the second try never does

- File: `src/cratekit/tagging/searchers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R11_no_attempt_cap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_source_answering_429_twice_then_200_succeeds_and_the_backoff_grew`
  - `tests/test_catalogue_searcher.py::test_an_image_fetch_that_meets_a_rate_limit_backs_off_like_a_search`

Old text:

```
RATE_LIMIT_ATTEMPTS = 3
```

New text:

```
RATE_LIMIT_ATTEMPTS = 1
```

### `u56-catalogue-searcher-and-tag-workers.R13_query_unescaped`

An unescaped query truncates at the first ampersand, so a different search is reported as this track's miss

- File: `src/cratekit/tagging/searchers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R13_query_unescaped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_an_artist_and_title_that_need_escaping_reach_the_seam_as_a_quoted_url`

Old text:

```
    return quote_plus(f"{artist} {title}".strip())
```

New text:

```
    return f"{artist} {title}".strip()
```

### `u56-catalogue-searcher-and-tag-workers.R3_parse_break_folds_into_unreachable`

The same mistake one layer along: a moved page shape reports as a network problem, which is a permanent state wearing a transient remedy

- File: `src/cratekit/tagging/searchers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R3_parse_break_folds_into_unreachable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_page_that_parsed_to_nothing_recognizable_raises_its_own_refusal[beatport payload missing]`
  - `tests/test_catalogue_searcher.py::test_a_page_that_parsed_to_nothing_recognizable_raises_its_own_refusal[traxsource rows unread]`

Old text:

```
    broken = [outcome for outcome in outcomes if outcome.answer is Answer.PARSE_BREAK]
    if broken:
```

New text:

```
    broken: list[SourceOutcome] = []
    if broken:
```

### `u56-catalogue-searcher-and-tag-workers.R5_bare_alias_lookup`

The defect the document review found: hand roll the resolution out of tagging_alias instead of routing.suggest_tag, which loses the sub display and every declared refusal

- File: `src/cratekit/tagging/searchers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R5_bare_alias_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 24 (killed)
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
  - ... and 9 more, see the JSON sidecar

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
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_the_image_fetch_is_paced_and_answers_the_bytes`

Old text:

```
    def fetch_image(url: str) -> bytes | None:
        pacer.wait()

```

New text:

```
    def fetch_image(url: str) -> bytes | None:

```

### `r791-a.S10_track_unread_returned`

_search_bandcamp: drop the unread track page and answer MISS, the pre R-791 fall through

- File: `src/cratekit/tagging/shops.py`
- Source: `r791-a.json`, row `S10_track_unread_returned`
- Moved: the Bandcamp reader moved whole from tagging/searchers.py to tagging/shops.py (U306); the two tests that killed it, the Bandcamp track page behind a challenge and the one that cannot be reached, are now the challenge and outage cases of test_a_bandcamp_track_page_unread_is_not_a_miss in the same file, the same track page replies and the same blocked and unreachable answers
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
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

### `r791-a.S8_blocked_track_page_stops`

_search_bandcamp: keep fetching track pages after one came back blocked

- File: `src/cratekit/tagging/shops.py`
- Source: `r791-a.json`, row `S8_blocked_track_page_stops`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
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

### `u281.S1_beatport_reads_no_refusal`

_search_beatport: drop the shared refusal check, so a 403 is unreachable and a 200 challenge a parse break, as before the card

- File: `src/cratekit/tagging/shops.py`
- Source: `u281.json`, row `S1_beatport_reads_no_refusal`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_beatport_answering_403_is_blocked_like_the_fallbacks`

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

### `u85-b.B1_beatport_resized`

The Beatport release image URL is asked for at the size the payload named, not the source edge

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B1_beatport_resized`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_beatport_hit_carries_its_release_picture_resized_to_the_source_edge`
  - `tests/test_catalogue_searcher.py::test_the_picture_comes_off_the_same_row_as_the_genre_and_never_another`

Old text:

```
    return _BEATPORT_IMAGE_SIZE.sub(f"image_size/{edge}x{edge}/", uri)
```

New text:

```
    return uri
```

### `u85-b.B2_edge_coefficient`

The Beatport edge drops from 1400 to 1200

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B2_edge_coefficient`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_beatport_hit_carries_its_release_picture_resized_to_the_source_edge`
  - `tests/test_catalogue_searcher.py::test_the_picture_comes_off_the_same_row_as_the_genre_and_never_another`

Old text:

```
BEATPORT_IMAGE_EDGE = 1400
```

New text:

```
BEATPORT_IMAGE_EDGE = 1200
```

### `u85-b.B3_picture_off_the_winning_row`

The picture is read off the loop's last row rather than the winning row, the wrong cover hazard

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B3_picture_off_the_winning_row`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_the_picture_comes_off_the_same_row_as_the_genre_and_never_another`

Old text:

```
    return best


def _search_beatport(
```

New text:

```
    return best and _Pick(best.genre, _beatport_art(track))


def _search_beatport(
```

### `u85-b.B4_only_web_addresses`

A payload value that is not an http or https URL becomes a GET

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B4_only_web_addresses`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_release_picture_that_is_not_a_web_address_is_no_picture[file:///etc/passwd]`
  - `tests/test_catalogue_searcher.py::test_a_release_picture_that_is_not_a_web_address_is_no_picture[javascript:alert(1)]`

Old text:

```
    return text if text.startswith(("https://", "http://")) else ""
```

New text:

```
    return text
```

### `u85-b.B5_bandcamp_original_size`

The Bandcamp picture is asked for at the thumbnail size the page named

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B5_bandcamp_original_size`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_genre_costs_one_fetch_and_its_picture_is_the_original`
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image`

Old text:

```
    return _BC_IMAGE_SIZE.sub("_10.jpg", _web_url(found.group(1)))
```

New text:

```
    return _web_url(found.group(1))
```

### `u85-b.B6_bandcamp_page_for_art`

A listing with a genre and no picture never reads the track page's og:image

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B6_bandcamp_page_for_art`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image`

Old text:

```
        if not genre or not art_url:
```

New text:

```
        if not genre:
```

### `u85-b.B7_listing_genre_wins`

The track page's tags overwrite a genre the listing already gave

- File: `src/cratekit/tagging/shops.py`
- Source: `u85-b.json`, row `B7_listing_genre_wins`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image`

Old text:

```
genre = genre or _bandcamp_tag(
```

New text:

```
genre = _bandcamp_tag(
```

### `u322.M01_stop_counts_partly_read`

KeptCatalogue.answer: a partly read row no longer resets the run, the card's defect: a Discogs miss beside a refusing Beatport stops the walk at the third row

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M01_stop_counts_partly_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 5 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_discogs_miss_beside_a_refusing_beatport_does_not_stop_the_walk`
  - `tests/test_catalogue_walk_refusal.py::test_a_partly_read_row_never_lets_a_run_of_refusals_stop_the_walk[a-partly-read-row-resets-the-run-of-refusals]`
  - `tests/test_catalogue_walk_refusal.py::test_a_partly_read_row_never_lets_a_run_of_refusals_stop_the_walk[partly-read-rows-never-count]`
  - `tests/test_catalogue_walk_refusal.py::test_a_row_read_beside_a_refusal_stays_unread_and_askable`
  - `tests/test_catalogue_walk_refusal.py::test_deezer_is_asked_on_every_row_with_an_isrc_while_beatport_refuses`

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
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_catalogue_nobody_asked_neither_counts_nor_resets`
  - `tests/test_catalogue_walk_refusal.py::test_a_rejected_discogs_token_beside_a_beatport_that_answers_does_not_stop_the_walk`
  - `tests/test_catalogue_walk_refusal.py::test_a_row_passed_over_for_a_refused_token_is_kept_for_the_day`

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

### `u322.M03_partly_read_ignores_passed_over`

Asked.partly_read: a passed over row reads as partly read, so it resets a run of refusals

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M03_partly_read_ignores_passed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_catalogue_nobody_asked_neither_counts_nor_resets`

Old text:

```
        if self.said != UNREAD or self.passed_over:
            return False
        return any(word in _ANSWERED
```

New text:

```
        if self.said != UNREAD:
            return False
        return any(word in _ANSWERED
```

### `u322.M04_partly_read_reads_refusals`

Asked.partly_read: a refusal counts as an answer, so a row every catalogue refused never stops the walk

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M04_partly_read_reads_refusals`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_catalogue_nobody_asked_neither_counts_nor_resets`
  - `tests/test_catalogue_walk_refusal.py::test_every_catalogue_refusing_three_rows_in_a_row_still_stops_the_walk`
  - `tests/test_catalogue_walk_refusal.py::test_the_words_of_a_refusal_by_every_catalogue_are_read_off_its_detail`

Old text:

```
        return any(word in _ANSWERED for _source, word in self.answers)

    @property
    def unread_by
```

New text:

```
        return any(word in (*_ANSWERED, *searchers.UNREAD_ANSWERS) for _source, word in self.answers)

    @property
    def unread_by
```

### `u322.M05_not_sent_read_as_sent`

_word: a refusal never sent is recorded as one sent, so the counts call Beatport asked on every row

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M05_not_sent_read_as_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_row_read_beside_a_refusal_stays_unread_and_askable`
  - `tests/test_catalogue_walk_refusal.py::test_the_words_of_a_refusal_by_every_catalogue_are_read_off_its_detail`

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
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_discogs_miss_beside_a_refusing_beatport_does_not_stop_the_walk`
  - `tests/test_catalogue_walk_refusal.py::test_a_row_read_beside_a_refusal_stays_unread_and_askable`
  - `tests/test_catalogue_walk_refusal.py::test_deezer_is_asked_on_every_row_with_an_isrc_while_beatport_refuses`

Old text:

```
            return Asked(UNREAD, note=f"unread: {', '.join(refused)}", answers=words)
```

New text:

```
            return Asked(UNREAD, note=f"unread: {', '.join(refused)}")
```

### `u322.M07_refusal_words_dropped`

catalogue_lookup: a refusal raised by the searcher carries no words, so the line counts its catalogues not asked

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M07_refusal_words_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_discogs_passed_over_beside_a_refusal_is_named_among_the_words`
  - `tests/test_catalogue_walk_refusal.py::test_a_refusals_detail_of_the_wrong_shape_carries_no_words`
  - `tests/test_catalogue_walk_refusal.py::test_the_words_of_a_refusal_by_every_catalogue_are_read_off_its_detail`

Old text:

```
                answers=_words_of_refusal(exc),
```

New text:

```
                answers=(),
```

### `u322.M08_credential_counts`

catalogue_lookup: a token Discogs refused is read as every catalogue refusing, so a Beatport that answers stops the walk at row three

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M08_credential_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_rejected_discogs_token_beside_a_beatport_that_answers_does_not_stop_the_walk`
  - `tests/test_catalogue_walk_refusal.py::test_a_row_passed_over_for_a_refused_token_is_kept_for_the_day`

Old text:

```
            if exc.cause.reason == searchers.CREDENTIAL_REASON:
```

New text:

```
            if False:
```

### `u322.M09_token_row_asked_every_run`

KeptCatalogue._askable_now: a row passed over for a refused token is asked again by every run of the day

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M09_token_row_asked_every_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_row_passed_over_for_a_refused_token_is_kept_for_the_day`

Old text:

```
        if self._unasked is None or not kept.passed_over or kept.note.endswith(TOKEN_UNUSABLE):
```

New text:

```
        if self._unasked is None or not kept.passed_over:
```

### `u322.M10_old_answer_kept`

_kept_answer: an answer kept before the words were is kept, so the line counts it as not asked

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M10_old_answer_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_an_answer_kept_before_the_words_is_asked_again_once[declined]`
  - `tests/test_catalogue_walk_refusal.py::test_an_answer_kept_before_the_words_is_asked_again_once[matched]`
  - `tests/test_catalogue_walk_refusal.py::test_an_answer_kept_before_the_words_is_asked_again_once[unread]`

Old text:

```
        if "answers" not in said:
            return None
```

New text:

```
        if False:
            return None
```

### `u322.M11_kept_words_lost`

_kept_answer: the words are not read back, so a kept partly read row counts toward the stop

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M11_kept_words_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 4 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_kept_answer_keeps_its_words`
  - `tests/test_catalogue_walk_refusal.py::test_an_answer_kept_before_the_words_is_asked_again_once[declined]`
  - `tests/test_catalogue_walk_refusal.py::test_an_answer_kept_before_the_words_is_asked_again_once[matched]`
  - `tests/test_catalogue_walk_refusal.py::test_an_answer_kept_before_the_words_is_asked_again_once[unread]`

Old text:

```
            answers=tuple((str(source), str(word)) for source, word in said.get("answers") or ()),
```

New text:

```
            answers=(),
```

### `u322.M12_digest_keeps_words`

Asked.digested: the words stay in the digest, so a gate answered the next day is refused stale

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M12_digest_keeps_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_backlog_rows_digest_leaves_the_words_out_and_its_envelope_keeps_them`
  - `tests/test_catalogue_walk_refusal.py::test_the_words_are_left_out_of_a_plans_digest`

Old text:

```
        del found["answers"]

```

New text:

```
(empty)
```

### `u322.M13_beside_any_said_dropped`

Asked.unread_beside_an_answer: only an unread row is named, so a row written from Deezer while Beatport refused is silent

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M13_beside_any_said_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_row_written_from_deezer_while_beatport_refused_is_named_in_the_warning`
  - `tests/test_catalogue_walk_refusal.py::test_rows_are_sorted_by_why_they_were_not_read_whole`

Old text:

```
        if not any(word in _ANSWERED for _source, word in self.answers):
            return ()
        return self.unread_by
```

New text:

```
        if self.said != UNREAD or not any(word in _ANSWERED for _source, word in self.answers):
            return ()
        return self.unread_by
```

### `u322.M14_token_rows_said_no_token`

sort_unread: a row passed over for a refused token is said as no token recorded

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M14_token_rows_said_no_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_a_rejected_discogs_token_beside_a_beatport_that_answers_does_not_stop_the_walk`
  - `tests/test_catalogue_walk_refusal.py::test_rows_are_sorted_by_why_they_were_not_read_whole`
  - `tests/test_catalogue_walk_refusal.py::test_the_suggest_verb_says_a_token_that_could_not_be_used`

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
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_the_backlogs_catalogue_line_counts_each_catalogues_answers`

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
- Ran: `tests/test_catalogue_walk_refusal.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_walk_refusal.py::test_the_backlogs_catalogue_line_counts_each_catalogues_answers`

Old text:

```
        "stopped": sum(asked.note == STOPPED_NOTE for asked in listed),
```

New text:

```
        "stopped": 0,
```

### `u178.S1_summary_counts_labels`

_summary: never count a file per label, so label_genres stays empty

- File: `src/cratekit/tagging/summary.py`
- Source: `u178.json`, row `S1_summary_counts_labels`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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

### `u282.C3_label_genre_counted_as_owed`

_summary: a file whose label gave its genre is counted as having no token, overstating the warning

- File: `src/cratekit/tagging/summary.py`
- Source: `u282.json`, row `C3_label_genre_counted_as_owed`
- Moved: the same text, now in src/cratekit/tagging/summary.py, was in src/cratekit/tagging/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_the_no_token_count_leaves_out_files_whose_genre_was_their_own_or_their_labels`

Old text:

```
                and str(report.get("source") or "") != tag_engine.LABEL_GENRE
            )
```

New text:

```
            )
```

### `r1476.M4_engine_ignores_folder_seam`

_by_label: answer --label through the tag seam, never the folder seam

- File: `src/cratekit/tagging/tag.py`
- Source: `r1476.json`, row `M4_engine_ignores_folder_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        return _Labelled((folder_genre or label_genre)(typed), own, NAMED_BY_FOLDER)
```

New text:

```
        return _Labelled(label_genre(typed), own, NAMED_BY_FOLDER)
```

### `r1476.M5_tag_one_drops_folder_seam`

tag_one: never hand the folder seam to _by_label

- File: `src/cratekit/tagging/tag.py`
- Source: `r1476.json`, row `M5_tag_one_drops_folder_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        else _by_label(path, label_genre, label, copyright_labels, folder_genre)
```

New text:

```
        else _by_label(path, label_genre, label, copyright_labels)
```

### `r1724.N11_tag_one_raw_stem`

tag_one: hand the searcher the raw stem, so the match reads mix)_pn and the Obiman release is missed

- File: `src/cratekit/tagging/tag.py`
- Source: `r1724.json`, row `N11_tag_one_raw_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`

Old text:

```
    title = title_tag or titles.name_title(path.stem)
```

New text:

```
    title = title_tag or path.stem
```

### `u178-e9.E9_label_tag_reset`

tag_one: keep the file's tag in label_tag on a file the label answered for

- File: `src/cratekit/tagging/tag.py`
- Source: `u178-e9.json`, row `E9_label_tag_reset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
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

### `u240.M3_tag_no_longer_outranks_the_line`

_by_label: a file's own label tag no longer comes first, so the line or --label decides a tagged file

- File: `src/cratekit/tagging/tag.py`
- Source: `u240.json`, row `M3_tag_no_longer_outranks_the_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 15 (killed)
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
- Ran: `tests/test_label_genre.py`
- Collected: 64 against a baseline of 64
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`
  - `tests/test_label_genre.py::test_the_verbs_label_names_the_label_of_a_file_with_no_tag_and_the_tag_wins`

Old text:

```
    if typed:

```

New text:

```
    if False:

```

### `u282.T1_question_asked_with_a_picture`

tag_one: the picture's question is asked whatever the file holds, so a file with a picture spends a Beatport request

- File: `src/cratekit/tagging/tag.py`
- Source: `u282.json`, row `T1_question_asked_with_a_picture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_that_has_a_picture_sends_beatport_nothing`

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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_picture_ask_that_raises_never_fails_the_file`
  - `tests/test_discogs_first.py::test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread`
  - `tests/test_discogs_first.py::test_a_tagged_file_with_no_picture_keeps_its_genre_and_gets_the_cover`

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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
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
- Ran: `tests/test_discogs_first.py`
- Collected: 40 against a baseline of 40
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

### `u289.T1_title_tag_split`

tag_one: a file with a title tag and no artist tag is split by its name

- File: `src/cratekit/tagging/tag.py`
- Source: `u289.json`, row `T1_title_tag_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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

### `r1724.N6_tail_never_dropped`

name_title: return the stem whatever it ends with, main's reading

- File: `src/cratekit/tagging/titles.py`
- Source: `r1724.json`, row `N6_tail_never_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`

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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_an_untagged_file_is_asked_by_the_artist_and_title_its_name_reads_to`

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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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

### `u289.N2_head_alone_ambiguous`

by_name: a head alone name is recorded ambiguous rather than head alone

- File: `src/cratekit/tagging/titles.py`
- Source: `u289.json`, row `N2_head_alone_ambiguous`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
- Kills: 9 (killed)
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
- Kills: 9 (killed)
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_the_question_reads_past_the_head_the_marker_and_the_artists_own_part[03B - 83 - Kerri Chandler & Tide - On My Way-Kerri Chandler-Kerri Chandler & Tide - On My Way]`

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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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
- Ran: `tests/test_discogs_question.py`
- Collected: 167 against a baseline of 167
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

### `u318.T01_outcome_guard`

named_versions: read a version off an ambiguous name too, not only a titled one

- File: `src/cratekit/tagging/titles.py`
- Source: `u318.json`, row `T01_outcome_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_question.py`, `tests/test_discogs_version.py`
- Collected: 505 against a baseline of 505
- Kills: 4 (killed)
- Killed:
  - `tests/test_discogs_question.py::test_every_matcher_corpus_case_keeps_its_verdict_when_asked_past_its_head[08A - 124 - Make Luv - Room 5-Make Luv]`
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Lost And Found Tim Green-False-False]`
  - `tests/test_discogs_version.py::test_a_catalogue_title_writes_a_version[Two Months Off (Tim Green)-False-False]`
  - `tests/test_discogs_version.py::test_what_a_title_names_as_its_mix[Two Months Off (Tim Green Vocal)-Fixture Artist-named3]`

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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_files_named_versions[Two Months Off (Tim Green Vocal Mix)-named17]`
  - `tests/test_discogs_version.py::test_a_release_is_taken_only_for_the_version_it_writes[named-vocal]`

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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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

### `u324.F01_entry_o_slash`

_PLAIN_SPELLINGS: delete the ø entry, so it is read as a letter of its own again

- File: `src/cratekit/tagging/titles.py`
- Source: `u324.json`, row `F01_entry_o_slash`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
- Kills: 12 (killed)
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
- Kills: 6 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xc6ther-Aether]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\xe6ther-Aether]`
  - `tests/test_discogs_version.py::test_a_letter_that_also_carries_an_accent_is_read_plain`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\xc6ther-Aether]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\xe6ther-Aether]`
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`

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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[Stra\xdfe-Strasse]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[Stra\xdfe-Strasse]`
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`

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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
- Kills: 5 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0141ukasz-Lukasz]`
  - `tests/test_discogs_version.py::test_a_folded_maker_written_with_no_bracket_is_read_by_its_last_words[\u0142ukasz-Lukasz]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\u0141ukasz-Lukasz]`
  - `tests/test_discogs_version.py::test_a_maker_spelled_with_a_letter_nfkd_leaves_is_one_maker[\u0142ukasz-Lukasz]`
  - `tests/test_discogs_version.py::test_the_fold_takes_exactly_the_letters_nfkd_leaves_alone`

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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
- Kills: 13 (killed)
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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
- Kills: 34 (killed)
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
  - ... and 19 more, see the JSON sidecar

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
- Ran: `tests/test_discogs_version.py`
- Collected: 338 against a baseline of 338
- Kills: 1 (killed)
- Killed:
  - `tests/test_discogs_version.py::test_a_letter_that_also_carries_an_accent_is_read_plain`

Old text:

```
    return _unaccented(word).translate(_PLAIN_LETTERS)
```

New text:

```
    return _unaccented(word.translate(_PLAIN_LETTERS))
```

### `u331.S11_vocals_imports_analysis_cli_at_top`

vocals/cli: import the analysis verbs' module at the top, so analyze vocals cannot build with the analysis toggle off

- File: `src/cratekit/vocals/cli.py`
- Source: `u331.json`, row `S11_vocals_imports_analysis_cli_at_top`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`
  - `tests/test_import_rules.py::test_with_a_toggle_off_every_remaining_verb_builds_and_formats_its_help`

Old text:

```
from cratekit.core.exit_codes import Remedy

```

New text:

```
from cratekit.core.exit_codes import Remedy
from cratekit.analysis import cli as _analysis_cli  # noqa: F401

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
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
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
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`

Old text:

```
        if content_id not in held:
```

New text:

```
        if False:
```

### `r1949.E4_uncompared_filter_dropped`

check: keep the differences of a playlist dimension the run could not read

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `E4_uncompared_filter_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_check_with_no_source_leaves_the_recorded_favorites_out_and_names_the_gap`

Old text:

```
    if uncompared:
```

New text:

```
    if False:
```

### `r1949.E7_record_union_dropped`

resolve_destinations: drop the recorded destinations from the set, so one that lost every track falls into foreign

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `E7_record_union_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_check_with_no_source_leaves_the_recorded_favorites_out_and_names_the_gap`

Old text:

```
        wanted |= {(entry.bucket, entry.sub) for entry in record.nodes}
```

New text:

```
        pass
```

### `r1949.E8_favorites_gap_unread`

_uncompared_playlist_subs: answer the playlist classes whether or not the favourites source was read

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `E8_favorites_gap_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`

Old text:

```
    if genre_favorites.FAVORITES_DIMENSION not in tuple(not_compared):
        return set()
```

New text:

```
    if False:
        return set()
```

### `r1949.N12_undeclared_pair_raises`

declared_names: let a former or split place's KeyError escape, so every check refuses

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1949.json`, row `N12_undeclared_pair_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_check_with_no_source_leaves_the_recorded_favorites_out_and_names_the_gap`
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`
  - `tests/test_genre_favorites.py::test_the_rebuild_files_a_favourite_into_the_folder_it_moves_it_to`
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`

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

### `u119-c.C3_uncompared_still_compared`

check: a playlist dimension not compared still counts its differences, so the tree reads unconverged

- File: `src/cratekit/write/convergence_check.py`
- Source: `u119-c.json`, row `C3_uncompared_still_compared`
- Moved: the same text, now in src/cratekit/write/convergence_check.py, was in src/cratekit/write/rebuild.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_check_with_no_source_leaves_the_recorded_favorites_out_and_names_the_gap`

Old text:

```
    uncompared = _uncompared_playlist_subs(declared, not_compared)
    if uncompared:
```

New text:

```
    uncompared = _uncompared_playlist_subs(declared, not_compared)
    if False:
```

### `u302.W7_two_candidates_chosen_by_position`

only_one: of two nodes on one display pair, the first is taken

- File: `src/cratekit/write/convergence_check.py`
- Source: `u302.json`, row `W7_two_candidates_chosen_by_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_two_playlists_of_the_destinations_name_leave_its_node_unrecorded`

Old text:

```
    return candidates[0] if len(candidates) == 1 else None
```

New text:

```
    return candidates[0] if candidates else None
```

### `u302.W8_display_pair_keyed_on_the_folder_twice`

by_display_pair: the key forgets the playlist name

- File: `src/cratekit/write/convergence_check.py`
- Source: `u302.json`, row `W8_display_pair_keyed_on_the_folder_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_genre_favorites.py`
- Collected: 128 against a baseline of 128
- Kills: 5 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_recovery_run_after_a_rename_converges_once_the_tree_layer_can`
  - `tests/test_deferred_routing.py::test_a_recovery_run_after_a_taxonomy_rename_converges_rather_than_duplicating`
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`
  - `tests/test_genre_favorites.py::test_the_rebuild_files_a_favourite_into_the_folder_it_moves_it_to`
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`

Old text:

```
        out.setdefault((node.folder_display, node.playlist_display), []).append(node)
```

New text:

```
        out.setdefault((node.folder_display, node.folder_display), []).append(node)
```

### `u119-b.G12r_removed_namesake_written_into`

_playlist_row: a removed Favorites of the name under the folder is written into

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-b.json`, row `G12r_removed_namesake_written_into`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_removed_favorites_under_the_folder_is_not_written_into`

Old text:

```
    for row in list(db.get_playlist(Name=folder.playlist_display)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
```

New text:

```
    for row in list(db.get_playlist(Name=folder.playlist_display)):
        if rb_writer.is_folder(row):
            continue
```

### `u119-b.G5r_favorites_counted_as_members`

plan_refresh: the folder's own Favorites counts among the folder's members

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-b.json`, row `G5r_favorites_counted_as_members`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_favourite_sitting_only_in_favorites_after_leaving_its_band_is_removed`

Old text:

```
            if favorites_node is not None and node.playlist_id == favorites_node.playlist_id:
                continue
            members.update(node.content_ids)
```

New text:

```
            members.update(node.content_ids)
```

### `u119-c.C2_torn_bucket_bound_anyway`

plan_refresh: a bucket whose record names two live folders is bound to the first

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-c.json`, row `C2_torn_bucket_bound_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_bucket_is_bound_by_its_band_entries_before_its_favorites_entry`

Old text:

```
        if bucket.id in recorded_folder and bucket.id not in torn
    }
```

New text:

```
        if bucket.id in recorded_folder
    }
```

### `u119-c.C5_interruption_unreported`

apply_refresh: a failure after the additions landed is raised bare, the additions unreported

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119-c.json`, row `C5_interruption_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_removal_commit_that_lands_and_then_raises_is_recorded_with_its_count`
  - `tests/test_genre_favorites.py::test_a_removal_that_fails_after_the_additions_landed_says_what_landed`
  - `tests/test_genre_favorites.py::test_the_additive_half_carries_the_additions_when_interrupted_past_them`
  - `tests/test_genre_favorites.py::test_the_verb_reports_an_interrupted_refresh_with_the_additions_that_committed`

Old text:

```
        except Exception as exc:
            raise RefreshInterrupted(landed) from exc
```

New text:

```
        except Exception:
            raise
```

### `u119.G10_placements_no_gap`

placements: a source that cannot be read names no dimension as not compared

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G10_placements_no_gap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_check_with_no_source_leaves_the_recorded_favorites_out_and_names_the_gap`
  - `tests/test_genre_favorites.py::test_the_favourites_become_declared_placements_and_a_missing_source_a_gap`

Old text:

```
        return (), (FAVORITES_DIMENSION,)
```

New text:

```
        return (), ()
```

### `u119.G11_stale_digest`

apply_refresh: a plan whose digest moved since the approval is written anyway

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G11_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_plan_that_moved_between_the_approval_and_the_write_is_refused`
  - `tests/test_genre_favorites.py::test_the_digest_moves_when_a_track_is_dragged_into_favorites_between_the_acts`

Old text:

```
    if again.digest != plan.digest:
        raise refuse(
            "decision-stale",
            "the genre Favorites are not as the approved plan read them
```

New text:

```
    if False:
        raise refuse(
            "decision-stale",
            "the genre Favorites are not as the approved plan read them
```

### `u119.G13_removals_when_not_asked`

apply_refresh: the removals are made whether or not the caller was approved for them

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G13_removals_when_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_additive_half_adds_and_counts_what_it_leaves_owed`
  - `tests/test_genre_favorites.py::test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply`

Old text:

```
        if remove and owed:
```

New text:

```
        if owed:
```

### `u119.G15_removal_commit_admits_nothing`

apply_refresh: the second commit does not admit the membership table

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G15_removal_commit_admits_nothing`
- Moved: the removal commit now sits in _remove_favorites, one level less indented, the same call
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 6 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_favourite_sitting_only_in_favorites_after_leaving_its_band_is_removed`
  - `tests/test_genre_favorites.py::test_a_hand_added_track_not_in_all_favorites_is_removed_at_the_refresh`
  - `tests/test_genre_favorites.py::test_a_removal_commit_that_lands_and_then_raises_is_recorded_with_its_count`
  - `tests/test_genre_favorites.py::test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band`
  - `tests/test_genre_favorites.py::test_no_content_row_tempo_or_rating_is_written`
  - `tests/test_genre_favorites.py::test_the_verb_asks_its_explicit_gate_then_adds_and_removes_and_reads_back`

Old text:

```
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
```

New text:

```
            rb_writer.commit_guarded(db)
```

### `u119.G1_class_undeclared`

require_class: a taxonomy with no playlist class is not refused

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G1_class_undeclared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_taxonomy_declaring_no_playlist_class_refuses_by_name`
  - `tests/test_genre_favorites.py::test_the_verb_refuses_an_undeclared_class_by_name`

Old text:

```
    found = favorites_class(declared)
    if found is None:
        raise refuse(
            CLASS_UNDECLARED,
```

New text:

```
    found = favorites_class(declared)
    if False:
        raise refuse(
            CLASS_UNDECLARED,
```

### `u119.G4_removed_membership_live`

_live_members: a membership rekordbox removed still counts as held

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G4_removed_membership_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band`

Old text:

```
        if not rb_writer.membership_removed(song)
    )
```

New text:

```
    )
```

### `u119.G6_wanted_is_members`

plan_refresh: every member of the folder is wanted, favourite or not

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G6_wanted_is_members`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 14 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_hand_added_track_not_in_all_favorites_is_removed_at_the_refresh`
  - `tests/test_genre_favorites.py::test_a_plan_that_moved_between_the_approval_and_the_write_is_refused`
  - `tests/test_genre_favorites.py::test_a_removal_commit_that_lands_and_then_raises_is_recorded_with_its_count`
  - `tests/test_genre_favorites.py::test_a_removal_that_fails_after_the_additions_landed_says_what_landed`
  - `tests/test_genre_favorites.py::test_a_source_that_went_between_the_two_acts_is_refused_by_the_gate`
  - `tests/test_genre_favorites.py::test_a_track_that_leaves_all_favorites_leaves_its_genre_favorites_and_keeps_its_band`
  - `tests/test_genre_favorites.py::test_a_vocal_favourite_is_in_its_band_with_vox_and_favorites_under_one_genre`
  - `tests/test_genre_favorites.py::test_the_additive_half_adds_and_counts_what_it_leaves_owed`
  - `tests/test_genre_favorites.py::test_the_check_reports_a_favourite_missing_from_its_favorites_and_not_a_hand_added_one_as_foreign`
  - `tests/test_genre_favorites.py::test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply`
  - `tests/test_genre_favorites.py::test_the_digest_moves_when_a_track_is_dragged_into_favorites_between_the_acts`
  - `tests/test_genre_favorites.py::test_the_favourites_become_declared_placements_and_a_missing_source_a_gap`
  - `tests/test_genre_favorites.py::test_the_verb_asks_its_explicit_gate_then_adds_and_removes_and_reads_back`
  - `tests/test_genre_favorites.py::test_the_verb_reports_an_interrupted_refresh_with_the_additions_that_committed`

Old text:

```
                wanted=tuple(sorted(members & favourites)),
```

New text:

```
                wanted=tuple(sorted(members)),
```

### `u119.G7_twin_folders_first_taken`

plan_refresh: two folders of one bucket's name, the first is taken

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G7_twin_folders_first_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_folder_nobody_declares_and_a_name_two_folders_carry_are_left_alone`

Old text:

```
        if len(named) > 1:
            unclaimed.extend(
```

New text:

```
        if len(named) > 9:
            unclaimed.extend(
```

### `u119.G9_digest_over_adds`

identity: the digest covers the adds rather than the target

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u119.json`, row `G9_digest_over_adds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_digest_covers_the_target_and_stands_still_across_a_partial_apply`

Old text:

```
            "wanted": list(self.wanted),
            "removes": list(self.removes),
```

New text:

```
            "wanted": list(self.adds),
            "removes": list(self.removes),
```

### `u132.G1_undeclared_cause`

The additive half's skip over an undeclared class carries no cause

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u132.json`, row `G1_undeclared_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites_adoption.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_over_a_taxonomy_without_the_class_names_the_skipped_step`

Old text:

```
            cause=CLASS_UNDECLARED,

```

New text:

```
            cause="",

```

### `u185.R4_genre_source`

source_playlist: count a playlist of the source's name inside the folder

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u185.json`, row `R4_genre_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_source_namesake_inside_deadca7s_folder_is_not_a_second_source`

Old text:

```
    live = foreign_tree.outside(live, list(db.get_playlist()))
```

New text:

```
    live = list(live)
```

### `u302.W15_landed_removals_recorded_as_zero`

_remove_favorites: removals that landed and raised are recorded as none

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u302.json`, row `W15_landed_removals_recorded_as_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_removal_commit_that_lands_and_then_raises_is_recorded_with_its_count`

Old text:

```
                _record_favorites_commit(record, plan.tree_id, added=0, removed=removed, cfg=cfg)
                convergence.record_fingerprint(cfg, db)
            raise
    return removed
```

New text:

```
                _record_favorites_commit(record, plan.tree_id, added=0, removed=0, cfg=cfg)
                convergence.record_fingerprint(cfg, db)
            raise
    return removed
```

### `u302.W18c_removed_nodes_planned`

what W18 holds: plan_refresh keeps soft deleted nodes in the tree it plans, the drop that keeps a removed folder from reaching the write

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u302.json`, row `W18c_removed_nodes_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_removed_favorites_under_the_folder_is_not_written_into`

Old text:

```
    nodes = tuple(node for node in tree_read.read_tree(db, root_id) if not node.removed)
```

New text:

```
    nodes = tuple(tree_read.read_tree(db, root_id))
```

### `u302.W19_emptied_source_mirrored`

source_playlist: an emptied playlist of the source name is taken as the source

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u302.json`, row `W19_emptied_source_mirrored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_a_smart_playlist_or_an_emptied_playlist_of_the_source_name_is_not_the_source`

Old text:

```
    if len(live) == 1 and live_members(db, str(live[0].ID)):
```

New text:

```
    if len(live) == 1:
```

### `u163.W17_first_active`

first_active_id: take the first row, tombstone or not

- File: `src/cratekit/write/metadata.py`
- Source: `u163.json`, row `W17_first_active`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_tombstoned_namesake_is_skipped_for_the_active_row_after_it_or_else_minted`

Old text:

```
        if not marker:
            return row.ID
```

New text:

```
        return row.ID
```

### `u40-author-full.F2_genre_unknown_silent`

First caller sample: drop the genre-unknown skip, so an unresolvable answer disappears from the plan

- File: `src/cratekit/write/metadata.py`
- Source: `u40-author-full.json`, row `F2_genre_unknown_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_genre_the_library_has_never_seen_is_skipped_and_surfaced`
  - `tests/test_genre_retag.py::test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader`

Old text:

```
        if genre_id is None:
            skipped.append(Skipped(content_id, "genre-unknown", wanted))
            continue
```

New text:

```
        if genre_id is None:
            continue
```

### `u40-author-full.F3_policy_owns_more`

First caller sample: widen the RETAG_GENRE policy to a second column

- File: `src/cratekit/write/metadata.py`
- Source: `u40-author-full.json`, row `F3_policy_owns_more`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_apply_refuses_a_field_the_retag_policy_does_not_own`
  - `tests/test_genre_retag.py::test_the_retag_operation_owns_the_genre_column_and_nothing_else`

Old text:

```
            fields=MappingProxyType({"GenreID": rb_writer.Ownership.OWNED}),
```

New text:

```
            fields=MappingProxyType(
                {"GenreID": rb_writer.Ownership.OWNED, "Rating": rb_writer.Ownership.OWNED}
            ),
```

### `u59.M1_permissive_default`

Restore the permissive default: an unreadable marker reads as active

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M1_permissive_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row`

Old text:

```
        marker = getattr(row, rb_writer.SOFT_DELETE_COLUMN, _MARKER_ABSENT)
```

New text:

```
        marker = getattr(row, rb_writer.SOFT_DELETE_COLUMN, 0)
```

### `u59.M2_refusal_removed`

Delete the refusal entirely, so an absent marker falls through as falsey

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M2_refusal_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row`

Old text:

```
        if marker is _MARKER_ABSENT or marker is None:
```

New text:

```
        if False:
```

### `u59.M4_tombstone_resolves`

Invert the active test, so a soft-deleted genre is the one that resolves

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M4_tombstone_resolves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 6 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_live_namesake_behind_a_tombstone_is_still_found_through_the_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`
  - `tests/test_genre_retag.py::test_a_written_file_is_relinked_to_the_existing_genre_row`
  - `tests/test_genre_retag.py::test_an_unregistered_operation_writes_nothing_and_the_apply_is_what_prevents_it`
  - `tests/test_genre_retag.py::test_re_applying_a_plan_over_an_already_linked_row_is_a_no_op`

Old text:

```
        if not marker:
            return row.ID
```

New text:

```
        if marker:
            return row.ID
```

### `u59.M5_first_row_wins`

Return the first row rather than the first ACTIVE one, ending the loop

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M5_first_row_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_live_namesake_behind_a_tombstone_is_still_found_through_the_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`

Old text:

```
        if not marker:
            return row.ID
    return None
```

New text:

```
        return row.ID
    return None
```

### `u59.M6_reason_reworded`

Reword the refusal reason, which the plan and the report both key on

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M6_reason_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row`

Old text:

```
                "soft-delete-marker-unreadable",
```

New text:

```
                "soft-delete-marker-unknown",
```

### `u119-c.C4_favorites_beside_renamed_folder`

rebuild_tree: a first Favorites is made under the declared name beside a renamed folder

- File: `src/cratekit/write/rebuild.py`
- Source: `u119-c.json`, row `C4_favorites_beside_renamed_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`

Old text:

```
        more, second_plan = _under_recorded_folders(more, second_plan, record_now, standing_now)

```

New text:

```
(empty)
```

### `u119.R1_vox_unknown_by_id`

derive_from_taxonomy: a playlist class is asked of the vocal derivation and refused

- File: `src/cratekit/write/rebuild.py`
- Source: `u119.json`, row `R1_vox_unknown_by_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_rebuild_files_a_favourite_into_the_folder_it_moves_it_to`
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`

Old text:

```
        if entry.additive and entry.signal == taxonomy.SIGNAL_VOX
    )
    unknown = sorted(
```

New text:

```
        if entry.additive
    )
    unknown = sorted(
```

### `u119.R2_with_favorites_every_tree`

with_favorites: the favourites are added to every governed tree, not only the routing tree

- File: `src/cratekit/write/rebuild.py`
- Source: `u119.json`, row `R2_with_favorites_every_tree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_with_favorites_leaves_another_tree_and_an_undeclared_class_alone`

Old text:

```
    if tree_id != declared.tree.id or genre_favorites.favorites_class(declared) is None:
```

New text:

```
    if genre_favorites.favorites_class(declared) is None:
```

### `u246.R1_rebuild_set_per_placement`

rebuild_tree: put the set back inside the comprehension, one set of the derived placements built per placement (the shape on main)

- File: `src/cratekit/write/rebuild.py`
- Source: `u246.json`, row `R1_rebuild_set_per_placement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_comprehension_sets.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`

Old text:

```
    favorites = tuple(entry for entry in placements if entry not in first_pass)
```

New text:

```
    favorites = tuple(entry for entry in placements if entry not in set(derived))
```

### `u246.R3_rebuild_set_of_placements`

rebuild_tree: build the set from every placement rather than the derived ones, so the second pass files no favourite

- File: `src/cratekit/write/rebuild.py`
- Source: `u246.json`, row `R3_rebuild_set_of_placements`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_rebuild_files_a_favourite_into_the_folder_it_moves_it_to`
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`

Old text:

```
    first_pass = set(derived)
```

New text:

```
    first_pass = set(placements)
```

### `u246.R4_rebuild_membership_inverted`

rebuild_tree: keep the placements present in the derived set, so the second pass refiles the first pass's placements and no favourite

- File: `src/cratekit/write/rebuild.py`
- Source: `u246.json`, row `R4_rebuild_membership_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_favorites.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_favorites.py::test_the_rebuild_files_a_favourite_into_the_folder_it_moves_it_to`
  - `tests/test_genre_favorites.py::test_the_rebuild_puts_a_first_favorites_under_a_renamed_folder_its_record_binds`

Old text:

```
    favorites = tuple(entry for entry in placements if entry not in first_pass)
```

New text:

```
    favorites = tuple(entry for entry in placements if entry in first_pass)
```

### `r501-d.R2_settled_is_not_imported`

routing_cli._all_settled: count acknowledged tracks as proof, so a run nobody imported is recorded as proven

- File: `src/cratekit/write/routing_cli.py`
- Source: `r501-d.json`, row `R2_settled_is_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_tracks_acknowledged_as_gone_are_not_proof_of_an_import`

Old text:

```
    return bool(routed) and not ledger.outstanding(session_id)
```

New text:

```
    return not ledger.outstanding(session_id)
```

### `r501-d.R3_pass_is_proof`

routing_cli._close_if_settled: never record the pass as proof, so after a cutover no landed run can close

- File: `src/cratekit/write/routing_cli.py`
- Source: `r501-d.json`, row `R3_pass_is_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_after_a_cutover_the_pass_placing_every_track_is_proof_and_closes_the_run`

Old text:

```
        if record.state is session.SessionState.AWAITING_IMPORT and _all_settled(
```

New text:

```
        if False and _all_settled(
```

### `r318.P1_withdrawn_branch_removed`

row_placement: never answer withdrawn, so a track imported then removed in rekordbox is reported as never imported and the person is sent to import it again

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P1_withdrawn_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`
- Collected: 82 against a baseline of 82
- Kills: 2 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_track_deleted_after_import_is_surfaced`
  - `tests/test_deferred_routing.py::test_one_intent_is_placed_by_the_rows_its_location_reaches[only-soft-deleted-rows-is-withdrawn]`

Old text:

```
    if removed.outcome in (trees.MatchOutcome.MATCHED, trees.MatchOutcome.AMBIGUOUS):
        # A row exists and every one of them is a tombstone: imported once, then
```

New text:

```
    if False:
        # A row exists and every one of them is a tombstone: imported once, then
```

### `r318.P3_unresolved_branch_removed`

row_placement: drop the unresolved answer, so a location no prefix maps falls through to not imported, a configuration failure reported as a missing import

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P3_unresolved_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_one_intent_is_placed_by_the_rows_its_location_reaches[locations-that-resolve-to-nothing-are-not-told-to-import]`

Old text:

```
    if alive.outcome is trees.MatchOutcome.UNRESOLVED:
        return Placement.UNRESOLVED

```

New text:

```
(empty)
```

### `r318.P4_ambiguous_reads_not_imported`

row_placement: two live rows claiming a location answer not imported instead of ambiguous

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P4_ambiguous_reads_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_one_intent_is_placed_by_the_rows_its_location_reaches[two-active-rows-are-ambiguous-and-never-written]`

Old text:

```
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.AMBIGUOUS
```

New text:

```
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.NOT_IMPORTED
```

### `u155.W2_destination`

destination: resolve no genre sub, so its playlist has no name

- File: `src/cratekit/write/routing_pass.py`
- Source: `u155.json`, row `W2_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_rominimal_track_at_energy_3_lands_in_its_band_and_in_rominimal`

Old text:

```
    for genre in bucket.genre_subs:
        if genre.id == sub_id:
            return bucket.display, genre.display
```

New text:

```
(empty)
```

### `u329.W2_watch_drops_roots`

watched_roots keeps only the first root, so a grid written under a second root goes unwatched

- File: `src/cratekit/write/row_defaults.py`
- Source: `u329.json`, row `W2_watch_drops_roots`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_an_empty_analysis_watch_is_refused_for_every_write_that_shares_it`

Old text:

```
    watched = [Path(root) for root in analysis_roots]

```

New text:

```
    watched = [Path(root) for root in analysis_roots][:1]

```

### `u126.M1_half_is_a_majority`

Accept a value carried by exactly half the live rows

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M1_half_is_a_majority`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_approval_at_one_link_is_not_applied_at_another_and_no_majority_refuses`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows0]`

Old text:

```
and carriers * 2 > rows:
```

New text:

```
and carriers * 2 >= rows:
```

### `u126.M2_plurality`

Accept the most common value whatever share of the live rows carries it

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M2_plurality`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_approval_at_one_link_is_not_applied_at_another_and_no_majority_refuses`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows0]`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows1]`

Old text:

```
and carriers * 2 > rows:
```

New text:

```
:
```

### `u126.M3_dead_rows_count`

Count removed rows in the majority, so a library's tombstones vote

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M3_dead_rows_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows6]`
  - `tests/test_intake_land_native.py::test_the_library_link_is_the_value_more_than_half_the_live_rows_carry[rows1-2]`

Old text:

```
            f"WHERE {rb_writer.SOFT_DELETE_COLUMN} = 0 GROUP BY {LINK} "
```

New text:

```
            f"GROUP BY {LINK} "
```

### `u126.M4_least_common_first`

Order the values least common first, so the first read is not the majority

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M4_least_common_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_the_library_link_is_the_value_more_than_half_the_live_rows_carry[rows0-3]`
  - `tests/test_intake_land_native.py::test_the_library_link_is_the_value_more_than_half_the_live_rows_carry[rows2-2]`
  - `tests/test_intake_land_native.py::test_the_link_its_count_the_playlist_and_each_file_move_the_digest`

Old text:

```
            f"ORDER BY COUNT(*) DESC"
```

New text:

```
            f"ORDER BY COUNT(*) ASC"
```

### `u126.M5_null_is_a_value`

Drop the NULL test, so a NULL majority is taken as the value

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M5_null_is_a_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows2]`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows6]`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows7]`

Old text:

```
    if whole is not None and _WHOLE.fullmatch(whole) and carriers * 2 > rows:
```

New text:

```
    if whole is None or _WHOLE.fullmatch(whole) and carriers * 2 > rows:
```

### `u126.M6_any_text`

Loosen the whole number test to the sign stripped isdigit the review found, so --5 and a superscript digit reach int()

- File: `src/cratekit/write/row_link.py`
- Source: `u126.json`, row `M6_any_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows4]`
  - `tests/test_intake_land_native.py::test_no_majority_link_refuses_by_name[rows5]`

Old text:

```
    if whole is not None and _WHOLE.fullmatch(whole) and carriers * 2 > rows:
```

New text:

```
    if whole is not None and whole.lstrip("-").isdigit() and carriers * 2 > rows:
```

### `u111-b.B1_move_names_every_table`

The membership move's commit admits the whole removable set again, the playlist table included

- File: `src/cratekit/write/trees.py`
- Source: `u111-b.json`, row `B1_move_names_every_table`
- Moved: the removal commit is now in the step _remove_leavers, one level less indented, the same call
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_only_the_rotation_asks_its_commit_to_admit_a_removed_playlist`

Old text:

```
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
```

New text:

```
            rb_writer.commit_guarded(db, removals=rb_writer.REMOVABLE_TABLES)
```

### `u40-author-full.F4_tombstone_indexed`

First caller sample: stop dropping tombstones from the active row index, so a removed track claims its location

- File: `src/cratekit/write/trees.py`
- Source: `u40-author-full.json`, row `F4_tombstone_indexed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_soft_deleted_row_is_never_retagged`

Old text:

```
    for row in rows:
        if row.deleted:
            continue
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
```

New text:

```
    for row in rows:
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
```

### `u232.A9_fake_host_iter`

the fake host: leave psutil.process_iter real, so pyrekordbox's walk never sees rekordbox

- File: `tests/_host_processes.py`
- Source: `u232.json`, row `A9_fake_host_iter`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_the_fake_host_lists_rekordbox_and_its_agent`

Old text:

```
    monkeypatch.setattr(psutil, "process_iter", process_iter)
```

New text:

```
    pass
```

### `u326.W1_children_reads_lists`

_children: skip a list field's nodes, so a walk never enters a body, an argument list or a target list

- File: `tests/_source_guards.py`
- Source: `u326.json`, row `W1_children_reads_lists`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1021 against a baseline of 1021
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_the_csv_writer_guard_bites_and_stays_quiet_on_correct_code`

Old text:

```
            found.extend([item for item in value if isinstance(item, _AST)])
```

New text:

```
            pass
```

### `u326.W2_cache_by_identity`

_walk: hand back the held walk for any module once one is held, so a second module is answered from the first

- File: `tests/_source_guards.py`
- Source: `u326.json`, row `W2_cache_by_identity`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1021 against a baseline of 1021
- Kills: 11 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[acquire.fallback-fetch]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[acquire.fallback]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[audit.duplicates]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[intake.identify]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[intake.missing]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[intake.playlist]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[intake.set]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[match.run]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[repair.paths]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[tag.retag]`
  - `tests/test_cli_contract.py::test_the_csv_writer_guard_bites_and_stays_quiet_on_correct_code`

Old text:

```
    if not (_LAST_MODULE_WALK and _LAST_MODULE_WALK[0] is node):
```

New text:

```
    if not _LAST_MODULE_WALK:
```

### `r658-a.C2_keychain_shared`

Keychain stub recorded on the shared monkeypatch again, so a body undo restores the real keychain

- File: `tests/conftest.py`
- Source: `r658-a.json`, row `C2_keychain_shared`
- Moved: The same mutation on the same fixture: U312 cut the fixture's docstring to its rule, so the recorded text, which quoted the whole fixture, no longer occurs; the stub is still moved from the fixture's own MonkeyPatch onto the test's shared one.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isolation_survives_undo.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_isolation_survives_undo.py::test_every_redirect_survives_an_undo_of_the_body_s_own_patch`

Old text:

```

def _isolate_keychain():
    """Swap the OS keychain for an in-memory dictionary.

    Replacing keyring's three module functions does not depend on its backend
    protocol. Without it a credential test on macOS pops a real dialog, and a
    headless run hangs rather than fails.
    """
    try:
        import keyring
    except ImportError:  # pragma: no cover - keyring is a core dependency
        yield {}
        return

    store: dict[tuple[str, str], str] = {}

    def _set(service: str, username: str, password: str) -> None:
        store[(service, username)] = password

    def _get(service: str, username: str):
        return store.get((service, username))

    def _delete(service: str, username: str) -> None:
        store.pop((service, username), None)

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(keyring, "set_password", _set)
        monkeypatch.setattr(keyring, "get_password", _get)
        monkeypatch.setattr(keyring, "delete_password", _delete)
        yield store

```

New text:

```

def _isolate_keychain(monkeypatch):
    """Swap the OS keychain for an in-memory dictionary.

    Replacing keyring's three module functions does not depend on its backend
    protocol. Without it a credential test on macOS pops a real dialog, and a
    headless run hangs rather than fails.
    """
    try:
        import keyring
    except ImportError:  # pragma: no cover - keyring is a core dependency
        yield {}
        return

    store: dict[tuple[str, str], str] = {}

    def _set(service: str, username: str, password: str) -> None:
        store[(service, username)] = password

    def _get(service: str, username: str):
        return store.get((service, username))

    def _delete(service: str, username: str) -> None:
        store.pop((service, username), None)

    monkeypatch.setattr(keyring, "set_password", _set)
    monkeypatch.setattr(keyring, "get_password", _get)
    monkeypatch.setattr(keyring, "delete_password", _delete)
    yield store

```

### `r658-a.C4_recognition_shared`

Recognition transport refusal on the shared monkeypatch again

- File: `tests/conftest.py`
- Source: `r658-a.json`, row `C4_recognition_shared`
- Moved: The same mutation on the same fixture: U312 cut the fixture's docstring to its rule, so the recorded text, which quoted the whole fixture, no longer occurs; the stub is still moved from the fixture's own MonkeyPatch onto the test's shared one.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isolation_survives_undo.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_isolation_survives_undo.py::test_every_redirect_survives_an_undo_of_the_body_s_own_patch`

Old text:

```

def _no_paid_recognition():
    """Refuse the live ACRCloud transport (U57); a test injects its own."""
    from cratekit.intake import acrcloud

    def refused(request):
        raise AssertionError(
            "a test reached the live recognition transport; inject a fake one"
        )

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(acrcloud, "http_transport", refused)
        yield

```

New text:

```

def _no_paid_recognition(monkeypatch):
    """Refuse the live ACRCloud transport (U57); a test injects its own."""
    from cratekit.intake import acrcloud

    def refused(request):
        raise AssertionError(
            "a test reached the live recognition transport; inject a fake one"
        )

    monkeypatch.setattr(acrcloud, "http_transport", refused)
    yield

```

### `r658-a.C5_fetcher_shared`

Mix fetcher refusal on the shared monkeypatch again

- File: `tests/conftest.py`
- Source: `r658-a.json`, row `C5_fetcher_shared`
- Moved: The same mutation on the same fixture: U312 cut the fixture's docstring to its rule, so the recorded text, which quoted the whole fixture, no longer occurs; the stub is still moved from the fixture's own MonkeyPatch onto the test's shared one.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isolation_survives_undo.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_isolation_survives_undo.py::test_every_redirect_survives_an_undo_of_the_body_s_own_patch`

Old text:

```

def _no_real_mix_download():
    """Refuse the shipped mix fetcher (U104); a test sets ``fetch.fetcher``."""
    from cratekit.intake import fetch

    def refused():
        raise AssertionError(
            "a test reached the shipped mix fetcher; set fetch.fetcher to a fake"
        )

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(fetch, "fetcher", refused)
        yield

```

New text:

```

def _no_real_mix_download(monkeypatch):
    """Refuse the shipped mix fetcher (U104); a test sets ``fetch.fetcher``."""
    from cratekit.intake import fetch

    def refused():
        raise AssertionError(
            "a test reached the shipped mix fetcher; set fetch.fetcher to a fake"
        )

    monkeypatch.setattr(fetch, "fetcher", refused)
    yield

```

### `r926.C1_root_is_state_roots_only`

The conftest registers its own state_roots folder rather than the base temp, so a save to a test's tmp_path is refused

- File: `tests/conftest.py`
- Source: `r926.json`, row `C1_root_is_state_roots_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_config_migration.py`, `tests/test_config_test_root.py`
- Collected: 285 against a baseline of 285
- Kills: 11 (killed)
- Killed:
  - `tests/test_config.py::test_a_failed_write_leaves_no_temporary_file_behind`
  - `tests/test_config.py::test_a_migration_backup_gets_the_same_mode_as_the_file_it_copies`
  - `tests/test_config.py::test_a_rewritten_config_is_not_served_from_the_memo`
  - `tests/test_config.py::test_a_save_under_a_relocation_writes_a_file_that_loads_again`
  - `tests/test_config.py::test_saving_creates_the_directory_only_when_it_writes`
  - `tests/test_config.py::test_the_fingerprint_survives_a_round_trip_through_disk`
  - `tests/test_config_migration.py::test_a_migration_that_cannot_take_the_lock_refuses`
  - `tests/test_config_migration.py::test_a_second_process_that_migrated_first_does_not_get_its_backup_clobbered`
  - `tests/test_config_migration.py::test_a_successful_migration_rewrites_the_file_and_keeps_a_backup`
  - `tests/test_config_test_root.py::test_a_write_to_a_tmp_path_lands_as_it_always_has`
  - `tests/test_config_test_root.py::test_with_the_isolation_a_save_lands_in_the_temporary_root`

Old text:

```
                config, "_TEST_WRITE_ROOT", tmp_path_factory.getbasetemp()
```

New text:

```
                config, "_TEST_WRITE_ROOT", root
```

### `r926.C2_root_never_registered`

The conftest never registers a root, the state a probe outside tests/ is in, for every test

- File: `tests/conftest.py`
- Source: `r926.json`, row `C2_root_never_registered`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_config_migration.py`, `tests/test_config_test_root.py`, `tests/test_config_update.py`
- Collected: 311 against a baseline of 311
- Kills: 30 (killed)
- Killed:
  - `tests/test_config.py::test_a_failed_write_leaves_no_temporary_file_behind`
  - `tests/test_config.py::test_a_migration_backup_gets_the_same_mode_as_the_file_it_copies`
  - `tests/test_config.py::test_a_rewritten_config_is_not_served_from_the_memo`
  - `tests/test_config.py::test_a_save_under_a_relocation_writes_a_file_that_loads_again`
  - `tests/test_config.py::test_every_file_and_directory_this_unit_creates_is_private_under_any_umask`
  - `tests/test_config.py::test_saving_creates_the_directory_only_when_it_writes`
  - `tests/test_config.py::test_the_default_location_round_trips_end_to_end`
  - `tests/test_config.py::test_the_fingerprint_survives_a_round_trip_through_disk`
  - `tests/test_config_migration.py::test_a_migration_that_cannot_take_the_lock_refuses`
  - `tests/test_config_migration.py::test_a_second_process_that_migrated_first_does_not_get_its_backup_clobbered`
  - `tests/test_config_migration.py::test_a_successful_migration_rewrites_the_file_and_keeps_a_backup`
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[durable-append]`
  - `tests/test_config_test_root.py::test_a_write_to_a_tmp_path_lands_as_it_always_has`
  - ... and 15 more, see the JSON sidecar

Old text:

```
                config, "_TEST_WRITE_ROOT", tmp_path_factory.getbasetemp()
```

New text:

```
                config, "_TEST_WRITE_ROOT", None
```

### `u232.A1_platform_stub`

_no_host_process_table: leave core.processes._platform as psutil, so the careful scan reads the host

- File: `tests/conftest.py`
- Source: `u232.json`, row `A1_platform_stub`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 2 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`
  - `tests/test_host_process_table.py::test_the_careful_scan_reads_no_rekordbox_with_rekordbox_open_on_the_host`

Old text:

```
        monkeypatch.setattr(processes, "_platform", lambda: empty)
```

New text:

```
        pass
```

### `u232.A2_pyrekordbox_stub`

_no_host_process_table: leave pyrekordbox's get_process_id walking the host, the refused cut's own route

- File: `tests/conftest.py`
- Source: `u232.json`, row `A2_pyrekordbox_stub`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 3 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`
  - `tests/test_host_process_table.py::test_pyrekordbox_reads_no_rekordbox_with_rekordbox_open_on_the_host`
  - `tests/test_host_process_table.py::test_the_writers_guard_reads_clear_with_rekordbox_open_on_the_host`

Old text:

```
            monkeypatch.setattr(utils, "get_process_id", no_process)
```

New text:

```
            pass
```

### `u232.A3_stub_raise_exec`

_no_host_process_table: the no process stub answers zero under raise_exec, where pyrekordbox raises

- File: `tests/conftest.py`
- Source: `u232.json`, row `A3_stub_raise_exec`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_pyrekordbox_reads_no_rekordbox_with_rekordbox_open_on_the_host`

Old text:

```
        if raise_exec:
            # pyrekordbox's own words, which name rekordbox whatever was asked.
```

New text:

```
        if False:
            # pyrekordbox's own words, which name rekordbox whatever was asked.
```

### `u232.A4_tripwire_records`

tripwire: refuse without recording, so a call the code swallows passes silently

- File: `tests/conftest.py`
- Source: `u232.json`, row `A4_tripwire_records`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`

Old text:

```
            reached.append(f"psutil.{name} was called from:\n{where}")
```

New text:

```
            where = where
```

### `u232.A5_tripwire_refuses`

tripwire: record without refusing, answering an empty listing instead

- File: `tests/conftest.py`
- Source: `u232.json`, row `A5_tripwire_refuses`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`

Old text:

```
            raise AssertionError(
                f"a test reached the host's real process table through psutil.{name}; "
```

New text:

```
            return []
            raise AssertionError(
                f"a test reached the host's real process table through psutil.{name}; "
```

### `u232.A7_tripwire_on_pids`

_no_host_process_table: trip on process_iter only, leaving psutil.pids, the careful scan's own read, open

- File: `tests/conftest.py`
- Source: `u232.json`, row `A7_tripwire_on_pids`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`

Old text:

```
        monkeypatch.setattr(psutil, "pids", tripwire("pids"))
```

New text:

```
        pass
```

### `u232.A8_opt_in`

_no_host_process_table: ignore the real_process_table marker, so no test can reach the real table

- File: `tests/conftest.py`
- Source: `u232.json`, row `A8_opt_in`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 3 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_opted_in_reads_the_real_host`
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`
  - `tests/test_host_process_table.py::test_the_fake_host_is_what_the_real_scan_reads`

Old text:

```
    if request.node.get_closest_marker(REAL_PROCESS_TABLE) is not None:
        yield
        return
    import psutil
```

New text:

```
    import psutil
```

### `u312.D1_library_root_redirected`

_block_real_library_paths: leave CRATEKIT_LIBRARY_ROOT as the process found it, a null edit of the no real library path detonator

- File: `tests/conftest.py`
- Source: `u312.json`, row `D1_library_root_redirected`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_isolation_survives_undo.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_isolation_survives_undo.py::test_every_redirect_survives_an_undo_of_the_body_s_own_patch`

Old text:

```
        monkeypatch.setenv("CRATEKIT_LIBRARY_ROOT", str(library))
```

New text:

```
        pass
```

### `u312.D2_live_provider_refused`

_no_live_provider_client: leave the shipped provider client factory in place, a null edit of the no live provider detonator

- File: `tests/conftest.py`
- Source: `u312.json`, row `D2_live_provider_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_isolation_survives_undo.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_isolation_survives_undo.py::test_every_redirect_survives_an_undo_of_the_body_s_own_patch`

Old text:

```
        monkeypatch.setattr(provider_session, "CLIENT_FACTORY", refused)
```

New text:

```
        pass
```

### `u312.P1_presence_cached_as_absent`

_module_if_present: remember every dotted name as absent after its first lookup, so from the second test on the config roots are not re-pointed

- File: `tests/conftest.py`
- Source: `u312.json`, row `P1_presence_cached_as_absent`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_isolation_survives_undo.py`
- Collected: 256 against a baseline of 256
- Kills: 9 (killed)
- Killed:
  - `tests/test_config.py::test_a_failed_write_leaves_no_temporary_file_behind`
  - `tests/test_config.py::test_a_migration_backup_gets_the_same_mode_as_the_file_it_copies`
  - `tests/test_config.py::test_a_rewritten_config_is_not_served_from_the_memo`
  - `tests/test_config.py::test_a_save_under_a_relocation_writes_a_file_that_loads_again`
  - `tests/test_config.py::test_every_file_and_directory_this_unit_creates_is_private_under_any_umask`
  - `tests/test_config.py::test_saving_creates_the_directory_only_when_it_writes`
  - `tests/test_config.py::test_the_default_location_round_trips_end_to_end`
  - `tests/test_config.py::test_the_fingerprint_survives_a_round_trip_through_disk`
  - `tests/test_isolation_survives_undo.py::test_every_redirect_survives_an_undo_of_the_body_s_own_patch`

Old text:

```
        _PRESENT[dotted] = present
```

New text:

```
        _PRESENT[dotted] = False
```

### `u326.R6_cyanite_refused`

_no_live_cyanite: leave the shipped Cyanite send in place, so a forgotten fake uploads to the paid service

- File: `tests/conftest.py`
- Source: `u326.json`, row `R6_cyanite_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cyanite_trial.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_cyanite_trial.py::test_the_shipped_send_is_detonated_for_every_test`

Old text:

```
        monkeypatch.setattr(cyanite, "_requests_send", refused)
```

New text:

```
        pass
```

### `u326.R9_host_process_tripwire`

_no_host_process_table: leave psutil.process_iter real, so pyrekordbox's walk reads the host's process table

- File: `tests/conftest.py`
- Source: `u326.json`, row `R9_host_process_tripwire`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`

Old text:

```
        monkeypatch.setattr(psutil, "process_iter", tripwire("process_iter"))
```

New text:

```
        pass
```

### `u27-restore-cli-independent.I_H5_the_anti_vacuity_set_names_a_landed_verb`

Expect a comparison that cannot happen, the opposite direction from the author's row on the same assertion

- File: `tests/test_cli_contract.py`
- Source: `u27-restore-cli-independent.json`, row `I_H5_the_anti_vacuity_set_names_a_landed_verb`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1021 against a baseline of 1021
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_and_the_pending_register_name_the_same_unit`

Old text:

```
EXPECTED_COMPARED: frozenset[str] = frozenset()
```

New text:

```
EXPECTED_COMPARED: frozenset[str] = frozenset({"restore.list"})
```

### `r1917.T1_outside_not_removed`

The outside fixture no longer removes its scratch, so what a broken guard lets land outlives the test

- File: `tests/test_config_test_root.py`
- Source: `r1917.json`, row `T1_outside_not_removed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root_leaves_nothing.py`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_config_test_root_leaves_nothing.py::test_a_broken_guard_fails_the_file_leaves_nothing_and_a_later_run_passes`

Old text:

```
        yield folder
    finally:
        shutil.rmtree(scratch)
```

New text:

```
        yield folder
    finally:
        pass
```

### `r1917.T2_allowance_not_narrowed`

The outside fixture leaves the guard's system temporary allowance whole, so the state writers' refusals aim inside it

- File: `tests/test_config_test_root.py`
- Source: `r1917.json`, row `T2_allowance_not_narrowed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config_test_root_leaves_nothing.py`
- Collected: 18 against a baseline of 18
- Kills: 6 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[durable-append]`
  - `tests/test_config_test_root_leaves_nothing.py::test_a_broken_guard_fails_the_file_leaves_nothing_and_a_later_run_passes`

Old text:

```
    monkeypatch.setattr(tempfile, "tempdir", str(narrowed))
```

New text:

```
(empty)
```

### `r1917.T3_configuration_scratch_kept`

The configuration test removes its scratch only when empty, so a broken guard leaves a folder in the temporary directory

- File: `tests/test_config_test_root.py`
- Source: `r1917.json`, row `T3_configuration_scratch_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root_leaves_nothing.py`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_config_test_root_leaves_nothing.py::test_a_broken_guard_fails_the_file_leaves_nothing_and_a_later_run_passes`

Old text:

```
        assert list(scratch.iterdir()) == []
    finally:
        shutil.rmtree(scratch)
```

New text:

```
        assert list(scratch.iterdir()) == []
    finally:
        scratch.rmdir()
```

### `u329.D1_body_floor_four`

the identical body check counts from four lines, so a copied three line helper passes

- File: `tests/test_duplication.py`
- Source: `u329.json`, row `D1_body_floor_four`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_duplication.py::test_a_body_of_exactly_three_lines_is_a_copy_and_two_is_not`

Old text:

```
BODY_LINES = 3
```

New text:

```
BODY_LINES = 4
```

### `u329.D2_three_files_to_copy`

the identical body check needs three files, so a helper copied once passes

- File: `tests/test_duplication.py`
- Source: `u329.json`, row `D2_three_files_to_copy`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`
- Collected: 31 against a baseline of 31
- Kills: 4 (killed)
- Killed:
  - `tests/test_duplication.py::test_a_body_defined_in_two_files_is_a_copy_whatever_its_docstring`
  - `tests/test_duplication.py::test_a_body_of_exactly_three_lines_is_a_copy_and_two_is_not`
  - `tests/test_duplication.py::test_a_method_a_nested_function_and_an_async_function_are_read`
  - `tests/test_duplication.py::test_a_renamed_function_with_the_same_body_is_still_a_copy`

Old text:

```
        if len({path for path, _ in found}) > 1
```

New text:

```
        if len({path for path, _ in found}) > 2
```

### `u329.D3_docstring_kept`

the identical body check keeps the docstring, so a copy with its own docstring passes

- File: `tests/test_duplication.py`
- Source: `u329.json`, row `D3_docstring_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_duplication.py::test_a_body_defined_in_two_files_is_a_copy_whatever_its_docstring`

Old text:

```
            body = node.body[1:] if ast.get_docstring(node, clean=False) is not None else node.body
```

New text:

```
            body = node.body
```

### `u329.D4_arguments_ignored`

the identical body check drops the arguments, so two bodies taking different arguments read as one copy

- File: `tests/test_duplication.py`
- Source: `u329.json`, row `D4_arguments_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_duplication.py`
- Collected: 31 against a baseline of 31
- Kills: 2 (killed)
- Killed:
  - `tests/test_duplication.py::test_bodies_that_differ_in_an_argument_or_a_statement_are_not_copies`
  - `tests/test_duplication.py::test_no_function_body_is_defined_identically_in_two_files`

Old text:

```
            key = ast.dump(node.args) + "".join(
```

New text:

```
            key = "".join(
```

### `u256.T1_existing_path_fallback`

_build_disposable_database: drop the check for a file already at the path, so a copy is written over (or refused at) a path that holds a database or a sidecar

- File: `tests/test_rb_writer_db.py`
- Source: `u256.json`, row `T1_existing_path_fallback`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_fixture_database_template.py`
- Collected: 13 against a baseline of 13
- Kills: 5 (killed)
- Killed:
  - `tests/test_fixture_database_template.py::test_a_path_already_holding_a_file_is_built_from_nothing_as_before[-journal]`
  - `tests/test_fixture_database_template.py::test_a_path_already_holding_a_file_is_built_from_nothing_as_before[-shm]`
  - `tests/test_fixture_database_template.py::test_a_path_already_holding_a_file_is_built_from_nothing_as_before[-wal]`
  - `tests/test_fixture_database_template.py::test_a_path_already_holding_a_file_is_built_from_nothing_as_before[file]`
  - `tests/test_fixture_database_template.py::test_a_second_build_over_the_same_database_still_refuses`

Old text:

```
    if any(os.path.lexists(f"{db_path}{suffix}") for suffix in _DATABASE_FILES):
```

New text:

```
    if False:
```

### `u256.T2_sidecars_in_the_check`

_DATABASE_FILES: check the database file alone, so a path with a stray WAL, shared memory or journal sidecar gets a copy written beside it

- File: `tests/test_rb_writer_db.py`
- Source: `u256.json`, row `T2_sidecars_in_the_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_fixture_database_template.py`
- Collected: 13 against a baseline of 13
- Kills: 3 (killed)
- Killed:
  - `tests/test_fixture_database_template.py::test_a_path_already_holding_a_file_is_built_from_nothing_as_before[-journal]`
  - `tests/test_fixture_database_template.py::test_a_path_already_holding_a_file_is_built_from_nothing_as_before[-shm]`
  - `tests/test_fixture_database_template.py::test_a_path_already_holding_a_file_is_built_from_nothing_as_before[-wal]`

Old text:

```
_DATABASE_FILES = ("", "-wal", "-shm", "-journal")
```

New text:

```
_DATABASE_FILES = ("",)
```

### `u256.T3_key_carries_the_pin`

_build_disposable_database: key the cache on the variant alone, so a schema pin configured before the build is lost to the first build's

- File: `tests/test_rb_writer_db.py`
- Source: `u256.json`, row `T3_key_carries_the_pin`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_fixture_database_template.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_fixture_database_template.py::test_the_schema_pin_read_at_the_call_reaches_the_file`

Old text:

```
    key = (with_tag_category, db_version)
```

New text:

```
    key = (with_tag_category, "")
```

### `u256.T4_key_carries_the_variant`

_build_disposable_database: key the cache on the pin alone, so an untagged call gets the tagged database or the other way about

- File: `tests/test_rb_writer_db.py`
- Source: `u256.json`, row `T4_key_carries_the_variant`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_fixture_database_template.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_fixture_database_template.py::test_each_variant_is_built_from_nothing_once_and_every_call_gets_its_own_file`

Old text:

```
    key = (with_tag_category, db_version)
```

New text:

```
    key = (True, db_version)
```

### `u256.T5_template_kept`

_build_disposable_database: never keep the template, so every call builds from nothing again and the unit saves nothing

- File: `tests/test_rb_writer_db.py`
- Source: `u256.json`, row `T5_template_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_fixture_database_template.py`
- Collected: 13 against a baseline of 13
- Kills: 3 (killed)
- Killed:
  - `tests/test_fixture_database_template.py::test_a_database_written_and_encrypted_leaves_its_sibling_and_the_next_untouched`
  - `tests/test_fixture_database_template.py::test_each_variant_is_built_from_nothing_once_and_every_call_gets_its_own_file`
  - `tests/test_fixture_database_template.py::test_the_schema_pin_read_at_the_call_reaches_the_file`

Old text:

```
        _TEMPLATES[key] = template
```

New text:

```
        pass
```

### `u256.T7_wal_mode_kept`

_build_from_nothing (existing guard, sampled): leave the database in rollback mode, so the copies are not in the mode the real database and the snapshot pair run in

- File: `tests/test_rb_writer_db.py`
- Source: `u256.json`, row `T7_wal_mode_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_fixture_database_template.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_fixture_database_template.py::test_a_copy_is_the_database_a_build_from_nothing_makes[tagged]`
  - `tests/test_fixture_database_template.py::test_a_copy_is_the_database_a_build_from_nothing_makes[untagged]`

Old text:

```
    conn.execute("PRAGMA journal_mode=WAL")
    conn.commit()
    conn.close()


def _encrypt_in_place
```

New text:

```
    conn.commit()
    conn.close()


def _encrypt_in_place
```

### `u256.T8_private_copy_per_call`

_build_disposable_database: hand every caller the first caller's file by a hard link instead of a copy, the shared mutable state the unit must not introduce

- File: `tests/test_rb_writer_db.py`
- Source: `u256.json`, row `T8_private_copy_per_call`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_fixture_database_template.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_fixture_database_template.py::test_a_database_written_and_encrypted_leaves_its_sibling_and_the_next_untouched`
  - `tests/test_fixture_database_template.py::test_each_variant_is_built_from_nothing_once_and_every_call_gets_its_own_file`

Old text:

```
    descriptor = os.open(db_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, _SQLITE_FILE_MODE)
```

New text:

```
    first = _TEMPLATES.setdefault(("first", key), db_path)
    if first != db_path and os.path.exists(first):
        os.link(first, db_path)
        return
    descriptor = os.open(db_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, _SQLITE_FILE_MODE)
```

### `u256.T9_copy_mode`

_SQLITE_FILE_MODE: create a copy at 0666 before the umask, a plain create, so under a loose umask a copy is group writable where a build from nothing is not

- File: `tests/test_rb_writer_db.py`
- Source: `u256.json`, row `T9_copy_mode`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_fixture_database_template.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_fixture_database_template.py::test_a_copy_has_the_mode_a_build_from_nothing_has_under_a_loose_umask`

Old text:

```
_SQLITE_FILE_MODE = 0o644
```

New text:

```
_SQLITE_FILE_MODE = 0o666
```

### `r658-d.D2_the_ban_looks_for_another_name`

The ban matches a method named undone rather than undo, so it sees nothing

- File: `tests/test_isolation_survives_undo.py`
- Source: `r658-d.json`, row `D2_the_ban_looks_for_another_name`
- Moved: U333 rewrote the ban's call filter from a chain of isinstance and attribute tests into the comprehension in _body_undoes; the comparison of the call's attribute with undo is the same guard, now written with getattr
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_isolation_survives_undo.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_isolation_survives_undo.py::test_no_test_undoes_the_shared_monkeypatch`

Old text:

```
undo = [node for node in calls if getattr(node.func, "attr", None) == "undo"]
```

New text:

```
undo = [node for node in calls if getattr(node.func, "attr", None) == "undone"]
```

