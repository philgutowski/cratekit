# Mutation table: u308-replay-before-a

Measured by `scripts/mutate.py` on 2026-11-22 14:20 UTC, branch `HEAD` at `c9192091`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 188.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 19, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/5bcab4be-2978-53ef-b3bd-2807d1f5544d/scratchpad/known-failures-plus.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1114.M10_message_reworded_many` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M11_message_reworded_one` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M12_match_step_dropped` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M13_detail_labels_empty` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M14_withheld_reads_no_op` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M15_skipped_line_not_fail` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 5 | killed |
| `r1114.M16_remedy_line_dropped` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 2 | killed |
| `r1114.M17_remedy_line_only_doctor` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M1_every_skipped_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 3 | killed |
| `r1114.M2_single_label_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M3_mixed_run_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M4_closing_line_ignores_skips` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M5_closing_line_names_every_label` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1114.M6_nothing_new_not_counted` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 13 | killed |
| `r1114.M7_refusal_drops_the_lines` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 3 | killed |
| `r1114.M8_refusal_not_retryable` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `r1634.M17_check_drops_how` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 131 | 5 | killed |
| `r515-operator.S8_short_of_keeps_zero` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r515-operator.S9_question_no_short` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-a.S03_marker_moves` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 13 | killed |
| `u107-a.S04_marker_takes_window_place` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 8 | killed |
| `u107-a.S07_gate_before_asking` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-a.S08_catch_up_withhold` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u107-b.S10_pick_unknown` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u107-b.S11_pick_takes_only_chosen` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 7 | killed |
| `u107-b.S12_stop_removes` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 3 | killed |
| `u107-b.S13_take_accepts` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 10 | killed |
| `u107-b.S15_no_default_answer` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-b.S16_save_before_ask` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 9 | killed |
| `u107-b.S17_dead_verifier_skip` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-c.S20_pick_isdecimal` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-c.S21_filing_run` | `src/cratekit/label/sync_cli.py` | maintainer | 1 file(s) | 94 | 1 | killed |
| `u107-c.S23_stop_remedy` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-c.S24_size_coefficient` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u107-d.S02_record_version_again` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-d.S14_take_respects_decided_again` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u107-d.S25_measured_passes_refusal_again` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u108-a.G01_unsettled_skips_settled` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 4 | killed |
| `u108-c.G19_settle_keeps` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u108-c.G24_walk_ends_at_gate` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 8 | killed |
| `u108-d.G18_settle_matches_identity_again` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u108-d.G20_settle_skips_settled_again` | `src/cratekit/label/sync_cli.py` | maintainer | 2 file(s) | 204 | 1 | killed |
| `u189.M11_answer_remedy_plain_next` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u189.M12_pick_remedy_plain_next` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u189.M13_walk_remedy_plain_next` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u189.M14_pick_no_release_remedy_plain_next` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 3 | killed |
| `u189.M15_pick_remedy_unquoted` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 3 | killed |
| `u189.M16_empty_label_alone_walks` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 1 | killed |
| `u189.M1_next_label_refused_again` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 12 | killed |
| `u189.M2_label_alone_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 5 | killed |
| `u189.M3_next_release_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 2 | killed |
| `u189.M4_empty_name_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 2 | killed |
| `u189.M5_alone_hint_drops_the_label` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 3 | killed |
| `u189.M6_label_not_passed` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 11 | killed |
| `u189.M7_unknown_name_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 2 | killed |
| `u189.M8_entries_ignore_the_one` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 9 | killed |
| `u189.S1_saved_question_relisted` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 4 | killed |
| `u189.S2_question_not_saved` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 204 | 119 | killed |
| `u238.M10_question_drops_the_split` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 3 | killed |
| `u238.M11_saved_question_drops_the_split` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 3 | killed |
| `u238.M7_old_question_read_as_count` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 5 | killed |
| `u238.M8_bound_said_as_the_labels` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 8 | killed |
| `u238.M9_nothing_line_loses_the_split` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 319 | 2 | killed |
| `u277.M10_next_says_no_canary` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 131 | 12 | killed |
| `u278.M24_label_sync_not_narrowed` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `u278.M25_sweep_never_refuses` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `r798-c.H6_a_returned_release_passes_at_approval` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 195 | 3 | killed |
| `r798-d.H7_again_an_owned_release_is_not_asked_about` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 195 | 1 | killed |
| `u101.G10_ungated_not_reported_in_judged_label` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 3 | killed |
| `u101.G11_keep_read_as_drop` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 12 | killed |
| `u101.G12_reported_share_not_the_taxonomys` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G13_family_count_off_by_one` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u101.G14_classified_counts_unjudged` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G17_refusal_silent_on_held` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G18_no_op_claims_held` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G1_held_is_listed` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 7 | killed |
| `u101.G20_summary_held_empty` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 5 | killed |
| `u101.G2_judged_per_release` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 10 | killed |
| `u101.G3_all_labels_one_group` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 4 | killed |
| `u101.G4_unlabelled_grouped_together` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G5_unread_label_judged` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G6_unread_from_every_label` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 2 | killed |
| `u101.G7_mixed_is_a_genre` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G8_case_is_a_difference` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u101.G9_mapping_row_unread` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 57 | 1 | killed |
| `u107-c.S19_approved_superseded` | `src/cratekit/label/approved_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u108-c.G21_listing_skips_already` | `src/cratekit/label/approved_cli.py` | user | 4 file(s) | 368 | 2 | killed |
| `u108-c.G22_listing_excuse_applies` | `src/cratekit/label/approved_cli.py` | user | 4 file(s) | 368 | 1 | killed |
| `u75-a.A1_kind_filter` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A3_nothing_accepted_before_the_catalogue` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A5_only_the_seams_exception_is_gone` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A6_no_identifier_is_not_asked_of_the_provider` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A7_each_row_read_alone` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B11_write_failure_is_the_verbs_refusal` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B1_outage_threshold` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B3_only_a_provider_failure_counts` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B7_same_recording_listed_once` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B9_name_digests_the_provenance` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 2 | killed |
| `u75-zeros.B6_missing_and_nothing_listable_refuses` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `r840-a.A1_address_is_the_whole_field` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-a.A2_a_name_is_not_asked_about` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 6 | killed |
| `r840-a.A3_unreadable_verdict_is_decided` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-a.A4_only_label_releases` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-a.A5_no_identifier_is_not_read` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-a.A6_another_items_release_is_not_read` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-a.A7_catalogue_opened_on_demand` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-a.A8_outage_bound` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-a.A9_an_answer_resets_the_count` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B10_unaddressed_is_keyed_by_item` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-b.B11_left_counts_what_was_not_reached` | `src/cratekit/label/artists_cli.py` | maintainer | 1 file(s) | 61 | 6 | killed |
| `r840-b.B1_only_the_seams_exception_is_not_served` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-b.B2_a_refusal_stops_the_run` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 1 | killed |
| `r840-b.B3_no_name_never_blanks` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B4_an_unread_release_refuses` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B5_decided_meanwhile_is_not_fine` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B6_put_right_meanwhile_is_kept` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `r840-b.B7_addresses_are_what_still_read_one` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 5 | killed |
| `r840-b.B8_only_the_artist_is_rewritten` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 3 | killed |
| `r840-b.B9_a_refusal_carries_why_each_read_failed` | `src/cratekit/label/artists_cli.py` | user | 1 file(s) | 61 | 2 | killed |
| `u123.H10_year_filter` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 3 | killed |
| `u123.H11_day_filter` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 2 | killed |
| `u123.H12_newly_excludes_heard` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 2 | killed |
| `u123.H13_year_shape` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H14_ambiguous_bound` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H15_no_year_refusal` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H1_outside_refusal` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 2 | killed |
| `u123.H2_no_releases_refusal` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H3_vouched_before_a_write` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H4_unheard_tracks_stay` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H5_missing_holds_the_removal` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H6_heard_recorded` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 7 | killed |
| `u123.H7_year_adds_recorded` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H8_prefixed_year` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u123.H9_stray_said` | `src/cratekit/label/heard.py` | user | 1 file(s) | 38 | 1 | killed |
| `u243.L11_heard_adds_a_tombstoned_track` | `src/cratekit/label/heard.py` | user | 2 file(s) | 68 | 3 | killed |
| `u243.L13_heard_merges_a_pruned_track` | `src/cratekit/label/heard.py` | user | 2 file(s) | 68 | 1 | killed |
| `r1056.N10_pass_not_required` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N1_no_refusal_of_an_unreadable_record` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 7 | killed |
| `r1056.N2_first_landing_only` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N3_years_from_the_argument` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N4_no_landings_in_digest` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `r1056.N5_no_reread_before_rename` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N6_no_nothing_filed_warning` | `src/cratekit/label/mark_cli.py` | user | 2 file(s) | 89 | 4 | killed |
| `r1056.N7_nothing_filed_against_any_year` | `src/cratekit/label/mark_cli.py` | user | 2 file(s) | 89 | 1 | killed |
| `r1056.N8_shown_pass_bare` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.N9_verb_not_threaded` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 33 | 6 | killed |
| `r835-b.M1_only_the_batch_years_marked` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-b.M5_deleted_folder_said` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-c.M4_recheck_before_rename_again` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `u180.M14_root_refused` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M15_digest_is_the_target_order` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M16_stale_digest_refused` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M17_confined_seated_position` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M18_confined_unplanned_rows` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 2 | killed |
| `u180.M19_confined_memberships` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M20_confined_content` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M21_confinement_called` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `u180.M22_read_back_compares` | `src/cratekit/favorites/order.py` | user | 1 file(s) | 30 | 1 | killed |
| `r381-b.M14_follow_all_renames` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r381.M13_follow_overwrites` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r381.M15_read_does_not_persist` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r381.M16_advance_does_not_follow` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r381.M17_read_no_follow` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r798-b.G1_an_unread_answer_holds_nothing` | `src/cratekit/label/gate.py` | user | 4 file(s) | 316 | 4 | killed |
| `r798-b.G2_a_would_be_hold_is_asked_about_again` | `src/cratekit/label/gate.py` | user | 4 file(s) | 316 | 3 | killed |
| `r815-a.G1_the_asking_gives_up_at_the_bound` | `src/cratekit/label/gate.py` | user | 2 file(s) | 214 | 3 | killed |
| `u123.C1_declined_writes_nothing` | `src/cratekit/label/heard_cli.py` | user | 1 file(s) | 38 | 1 | killed |

## Row definitions

### `r1114.M10_message_reworded_many`

_unlisted_cause: reword the many label message so it no longer says none could be read

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M10_message_reworded_many`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
        else f"none of the {len(entries)} labels asked about could be read ({names}), "
```

New text:

```
        else f"the {len(entries)} labels asked about were skipped ({names}), "
```

### `r1114.M11_message_reworded_one`

_unlisted_cause: reword the single label message so it no longer says the label could not be read

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M11_message_reworded_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`

Old text:

```
        f"the label asked about could not be read ({names}), so whether it has"
```

New text:

```
        f"the label asked about was skipped ({names}), so whether it has"
```

### `r1114.M12_match_step_dropped`

_UNLISTED_STEPS: drop the step naming the registry's --match needle, the remedy for a listing that confirmed nothing, from the cause and the line

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M12_match_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
    "a listing that confirmed nothing: check the label's --match needle "
    "with: crate label registry",

```

New text:

```
(empty)
```

### `r1114.M13_detail_labels_empty`

_unlisted_cause: carry no label identifiers in the detail, so a script cannot tell which labels failed

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M13_detail_labels_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
        detail={"labels": [entry.label_id for entry in entries]},
```

New text:

```
        detail={"labels": []},
```

### `r1114.M14_withheld_reads_no_op`

_next, existing guard sampled: a run whose gate withheld an item ends no_op though it wrote

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M14_withheld_reads_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_walk_whose_gate_took_back_every_open_item_is_not_a_no_op`

Old text:

```
        # back has left review even when no question was left to ask.
        outcome=Outcome.OK if withheld else Outcome.NO_OP,
    )


#: What to do about a label
```

New text:

```
        # back has left review even when no question was left to ask.
        outcome=Outcome.NO_OP,
    )


#: What to do about a label
```

### `r1114.M15_skipped_line_not_fail`

_skipped_check, existing guard sampled: a skipped label's line is a note rather than a fail

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M15_skipped_line_not_fail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`
  - `tests/test_label_sync.py::test_next_closing_line_names_only_the_label_that_was_listed`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`
  - `tests/test_label_sync.py::test_next_with_one_label_skipped_and_the_next_asked_still_asks`

Old text:

```
    return _check(f"label.{entry.label_id}", "fail", f"{entry.name}: not asked; {why}")
```

New text:

```
    return _check(f"label.{entry.label_id}", "info", f"{entry.name}: not asked; {why}")
```

### `r1114.M16_remedy_line_dropped`

_next: refuse without the info line naming what to do, so the human rendering shows no remedy, the review's round one finding

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M16_remedy_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
        checks.append(_check("next", "info", _UNLISTED_REMEDY))
```

New text:

```
        pass
```

### `r1114.M17_remedy_line_only_doctor`

_UNLISTED_REMEDY: the line carries only the first step, so a listing that confirmed nothing is told to run doctor

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M17_remedy_line_only_doctor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
_UNLISTED_REMEDY = "; ".join(_UNLISTED_STEPS)
```

New text:

```
_UNLISTED_REMEDY = _UNLISTED_STEPS[0]
```

### `r1114.M1_every_skipped_not_refused`

_next: drop the refusal of a run whose every label was skipped, so it ends no_op with exit 0 again, the defect R-1114 names

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M1_every_skipped_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
    if not nothing:
```

New text:

```
    if False:
```

### `r1114.M2_single_label_not_refused`

_next: refuse only the walk over every label, so --next --label on a label whose listing failed ends no_op with exit 0

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M2_single_label_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`

Old text:

```
    if not nothing:
```

New text:

```
    if not nothing and only is None:
```

### `r1114.M3_mixed_run_refused`

_next: refuse whenever any label was skipped, so a run with one label listed and nothing new also fails

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M3_mixed_run_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_closing_line_names_only_the_label_that_was_listed`

Old text:

```
    if not nothing:
```

New text:

```
    if len(nothing) < len(entries):
```

### `r1114.M4_closing_line_ignores_skips`

_next: say no label has anything new whatever was skipped, the false closing line on a mixed run

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M4_closing_line_ignores_skips`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_closing_line_names_only_the_label_that_was_listed`

Old text:

```
            if len(nothing) == len(entries)
```

New text:

```
            if True
```

### `r1114.M5_closing_line_names_every_label`

_next: name every label in the mixed closing line, the skipped ones included, as having nothing new

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M5_closing_line_names_every_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_closing_line_names_only_the_label_that_was_listed`

Old text:

```
{', '.join(nothing)}"
```

New text:

```
{', '.join(one.name for one in entries)}"
```

### `r1114.M6_nothing_new_not_counted`

_next: stop counting a label listed with nothing new, so every run with no question refuses as unlisted

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M6_nothing_new_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_label_with_nothing_new_is_not_asked_and_a_run_with_nothing_to_ask_says_so`
  - `tests/test_label_sync.py::test_a_label_with_three_new_releases_is_asked_once`
  - `tests/test_label_sync.py::test_a_release_the_sweep_filed_while_its_question_waited_is_settled_by_the_answer`
  - `tests/test_label_sync.py::test_a_walk_whose_gate_took_back_every_open_item_is_not_a_no_op`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[all]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[not-now]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[pick]`
  - `tests/test_label_sync.py::test_next_closing_line_names_only_the_label_that_was_listed`
  - `tests/test_label_sync.py::test_next_label_then_answer_then_next_label_says_nothing_new`
  - `tests/test_label_sync.py::test_next_label_with_nothing_new_says_so_in_one_check`
  - `tests/test_label_sync.py::test_next_over_two_labels_both_listed_with_nothing_new_is_unchanged`
  - `tests/test_label_sync.py::test_nothing_new_after_an_answer_says_the_count_past_the_window`
  - `tests/test_label_sync.py::test_open_review_items_are_offered_once_and_settled_by_the_answer`

Old text:

```
                    nothing.append(entry.name)

```

New text:

```
(empty)
```

### `r1114.M7_refusal_drops_the_lines`

_next: refuse without the run's checks as data, so the per label fail lines vanish from the refusal

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M7_refusal_drops_the_lines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
            cause=_unlisted_cause(entries),
            data=data,
```

New text:

```
            cause=_unlisted_cause(entries),
            data=None,
```

### `r1114.M8_refusal_not_retryable`

_unlisted_cause: mark the refusal not retryable, though a provider answering later clears it

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M8_refusal_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
        retryable=True,
        origin=("label.sync",),
        detail={"labels": [entry.label_id for entry in entries]},
```

New text:

```
        retryable=False,
        origin=("label.sync",),
        detail={"labels": [entry.label_id for entry in entries]},
```

### `r1634.M17_check_drops_how`

label sync --next: the reverified line no longer says how the release was asked

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1634.json`, row `M17_check_drops_how`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_sync.py`
- Collected: 131 against a baseline of 131
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_provider_crediting_another_label_still_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`

Old text:

```
                f"{listing.canary.how()}: {listing.canary.said()}",
```

New text:

```
                f": {listing.canary.said()}",
```

### `r515-operator.S8_short_of_keeps_zero`

Read a saved shortfall block back even when it withheld nothing

- File: `src/cratekit/label/sync_cli.py`
- Source: `r515-operator.json`, row `S8_short_of_keeps_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_saved_shortfall_that_withheld_nothing_reads_back_as_no_shortfall`

Old text:

```
    if any(value is None for value in block.values()) or not block["withheld"]:
```

New text:

```
    if any(value is None for value in block.values()):
```

### `r515-operator.S9_question_no_short`

The label sync question drops the release shortfall

- File: `src/cratekit/label/sync_cli.py`
- Source: `r515-operator.json`, row `S9_question_no_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_short_release_is_counted_over_its_rows_and_the_question_says_the_shortfall`

Old text:

```
    if question.provider_withheld:
```

New text:

```
    if False:
```

### `u107-a.S03_marker_moves`

sync_cli.record_answer: keep the asked set as it was, so an answer does not move the marker and the same releases are asked again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-a.json`, row `S03_marker_moves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_label_with_three_new_releases_is_asked_once`
  - `tests/test_label_sync.py::test_a_release_answered_not_now_is_not_filed_by_the_labels_sweep`
  - `tests/test_label_sync.py::test_a_release_the_genre_gate_holds_never_appears_in_a_question`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[all]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[not-now]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[pick]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[stop]`
  - `tests/test_label_sync.py::test_not_now_moves_the_marker_and_a_release_published_after_is_asked_next_run`
  - `tests/test_label_sync.py::test_nothing_new_after_an_answer_says_the_count_past_the_window`
  - `tests/test_label_sync.py::test_open_review_items_are_offered_once_and_settled_by_the_answer`
  - `tests/test_label_sync.py::test_pick_records_exactly_the_chosen_releases_and_no_others`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`

Old text:

```
        asked = set(asked_releases(document, entry.label_id)) | set(question.identities())
```

New text:

```
        asked = set(asked_releases(document, entry.label_id))
```

### `u107-a.S04_marker_takes_window_place`

sync_cli._question_for: hand the label's source no asked set, so releases already answered are offered again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-a.json`, row `S04_marker_takes_window_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_release_answered_not_now_is_not_filed_by_the_labels_sweep`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[not-now]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[pick]`
  - `tests/test_label_sync.py::test_not_now_moves_the_marker_and_a_release_published_after_is_asked_next_run`
  - `tests/test_label_sync.py::test_nothing_new_after_an_answer_says_the_count_past_the_window`
  - `tests/test_label_sync.py::test_open_review_items_are_offered_once_and_settled_by_the_answer`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`

Old text:

```
        offered=asked,
```

New text:

```
        offered=None,
```

### `u107-a.S07_gate_before_asking`

sync_cli._question_for: list the label with no genre gate, so a release the gate would hold reaches a question

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-a.json`, row `S07_gate_before_asking`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_release_the_genre_gate_holds_never_appears_in_a_question`

Old text:

```
        gate=genre_gate.SweepGate(
            declared,
            tracks=reader.release_tracks,
            standing=genre_gate.StandingHolds(store),
            asking=tools.asking,
        ),
```

New text:

```
        gate=None,
```

### `u107-a.S08_catch_up_withhold`

sync_cli._question_for: never take back an open item the gate would now hold, so it is offered in the catch up

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-a.json`, row `S08_catch_up_withhold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_walk_whose_gate_took_back_every_open_item_is_not_a_no_op`
  - `tests/test_label_sync.py::test_an_open_item_the_gate_would_now_hold_is_taken_back_before_the_question`

Old text:

```
            elif judged.held:
```

New text:

```
            elif False:
```

### `u107-b.S10_pick_unknown`

sync_cli.record_answer: accept a pick naming a release the question did not offer

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S10_pick_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_naming_a_release_the_question_did_not_offer_is_refused`
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`

Old text:

```
            if unknown or not wanted:
```

New text:

```
            if not wanted:
```

### `u107-b.S11_pick_takes_only_chosen`

sync_cli.record_answer: a pick takes every offered release, not only the chosen ones

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S11_pick_takes_only_chosen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_of_a_digit_that_is_not_a_number_is_asked_again`
  - `tests/test_label_sync.py::test_a_pick_outside_the_numbers_is_asked_again`
  - `tests/test_label_sync.py::test_a_superseded_item_is_not_counted_as_waiting_by_label_approved`
  - `tests/test_label_sync.py::test_open_review_items_are_offered_once_and_settled_by_the_answer`
  - `tests/test_label_sync.py::test_pick_records_exactly_the_chosen_releases_and_no_others`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`

Old text:

```
            if answer == ALL or (answer == PICK and one.identity in wanted)
```

New text:

```
            if answer in (ALL, PICK)
```

### `u107-b.S12_stop_removes`

sync_cli.record_answer: stop reports the label removed and leaves it in the registry

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S12_stop_removes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[stop]`
  - `tests/test_label_sync.py::test_stop_following_removes_the_label_and_records_no_download`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`

Old text:

```
            removed = labels.RegistryStore().remove(entry.label_id)
```

New text:

```
            removed = True
```

### `u107-b.S13_take_accepts`

sync_cli._take: file a taken release and never record it accepted

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S13_take_accepts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_label_with_three_new_releases_is_asked_once`
  - `tests/test_label_sync.py::test_a_superseded_item_is_not_counted_as_waiting_by_label_approved`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[all]`
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[pick]`
  - `tests/test_label_sync.py::test_an_item_decided_between_the_question_and_the_answer_is_left_as_decided`
  - `tests/test_label_sync.py::test_next_label_then_answer_then_next_label_says_nothing_new`
  - `tests/test_label_sync.py::test_open_review_items_are_offered_once_and_settled_by_the_answer`
  - `tests/test_label_sync.py::test_pick_records_exactly_the_chosen_releases_and_no_others`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`

Old text:

```
    review.resolve(store, item.item_id, Verdict.ACCEPTED, actor=ACTOR)
```

New text:

```
    pass
```

### `u107-b.S15_no_default_answer`

sync_cli._ask: give the prompt a default of not-now, so an empty line moves the marker

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S15_no_default_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_an_empty_line_never_moves_a_marker_and_a_prompt_nobody_answers_refuses`

Old text:

```
        answer = prompter.ask(f"Answer ({', '.join(words)})").lower()
```

New text:

```
        answer = prompter.ask(f"Answer ({', '.join(words)})", default=NOT_NOW).lower()
```

### `u107-b.S16_save_before_ask`

sync_cli._walk: ask without saving the question first, so the answer has no question to apply to

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S16_save_before_ask`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 9 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_label_whose_catalogue_cannot_be_listed_fails_its_line_and_the_walk_goes_on`
  - `tests/test_label_sync.py::test_a_pick_of_a_digit_that_is_not_a_number_is_asked_again`
  - `tests/test_label_sync.py::test_a_pick_outside_the_numbers_is_asked_again`
  - `tests/test_label_sync.py::test_a_provider_refusal_mid_run_parks_it_with_the_remaining_labels_unasked`
  - `tests/test_label_sync.py::test_a_walk_left_unanswered_after_its_question_was_saved_is_not_a_no_op`
  - `tests/test_label_sync.py::test_a_word_outside_the_set_is_asked_again_and_the_answers_before_it_are_saved`
  - `tests/test_label_sync.py::test_an_empty_line_never_moves_a_marker_and_a_prompt_nobody_answers_refuses`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`

Old text:

```
            _save_pending(cfg, listed.question)
```

New text:

```
            pass
```

### `u107-b.S17_dead_verifier_skip`

sync_cli._question_for: read a catalogue that confirmed nothing as a label with nothing new

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S17_dead_verifier_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`

Old text:

```
    if not candidates and source.dropped and unconfirmed == source.read:
```

New text:

```
    if False:
```

### `u107-c.S20_pick_isdecimal`

sync_cli._pick: decide a release number with isdigit again, so a superscript digit crashes the walk (fix round guard)

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-c.json`, row `S20_pick_isdecimal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_of_a_digit_that_is_not_a_number_is_asked_again`

Old text:

```
            if word.isdecimal() and 1 <= int(word) <= count:
```

New text:

```
            if word.isdigit() and 1 <= int(word) <= count:
```

### `u107-c.S21_filing_run`

sync_cli.record_answer: file taken releases under the answering run, not the run that asked (fix round guard)

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-c.json`, row `S21_filing_run`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_later_answer_files_its_releases_under_the_run_that_asked`

Old text:

```
        filing_run = question.run or run_id
```

New text:

```
        filing_run = run_id
```

### `u107-c.S23_stop_remedy`

sync_cli.record_answer: stop with nothing waiting sends a person to --next, which asks nothing (fix round guard)

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-c.json`, row `S23_stop_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_stop_with_no_question_waiting_names_the_registry_remove`

Old text:

```
                    if answer == STOP
```

New text:

```
                    if False
```

### `u107-c.S24_size_coefficient`

sync_cli: halve the bytes per second the size estimate uses

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-c.json`, row `S24_size_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_the_default_human_output_names_the_question_and_each_release`
  - `tests/test_label_sync.py::test_the_structured_path_asks_the_same_question_and_takes_the_same_answer`

Old text:

```
BYTES_PER_SECOND = 110_000
```

New text:

```
BYTES_PER_SECOND = 55_000
```

### `u107-d.S02_record_version_again`

sync_cli.load_record: accept a record of any version as this build's

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-d.json`, row `S02_record_version_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_record_of_another_version_refuses_rather_than_being_read_as_this_builds`

Old text:

```
    if version != RECORD_VERSION:
```

New text:

```
    if False:
```

### `u107-d.S14_take_respects_decided_again`

sync_cli._take: overwrite an item a person decided between the question and the answer

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-d.json`, row `S14_take_respects_decided_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_an_item_decided_between_the_question_and_the_answer_is_left_as_decided`

Old text:

```
    if item.stored_verdict is not None:
        return False
```

New text:

```
    if False:
        return False
```

### `u107-d.S25_measured_passes_refusal_again`

sync_cli._measured: count a provider refusal while reading a release's tracks as tracks unread, so the walk goes on instead of parking

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-d.json`, row `S25_measured_passes_refusal_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_provider_refusal_while_counting_a_catch_up_release_parks_the_run`

Old text:

```
    except CratekitError:
        raise
    except Exception:  # noqa: BLE001 - counted as unread, never guessed at
```

New text:

```
    except Exception:  # noqa: BLE001 - counted as unread, never guessed at
```

### `u108-a.G01_unsettled_skips_settled`

sync_cli.unsettled: read every saved answer as unsettled, so a go summarises answers an earlier go already took

- File: `src/cratekit/label/sync_cli.py`
- Source: `u108-a.json`, row `G01_unsettled_skips_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
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
- Collected: 204 against a baseline of 204
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
- Collected: 204 against a baseline of 204
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
- Collected: 204 against a baseline of 204
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
- Collected: 204 against a baseline of 204
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

### `u189.M11_answer_remedy_plain_next`

record_answer: the remedy of an answer with nothing waiting names the plain --next again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M11_answer_remedy_plain_next`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_an_answer_with_nothing_waiting_names_next_label_and_following_it_reaches_that_label`

Old text:

```
                    else f"ask it first with: crate label sync --next --label {entry.label_id}"
```

New text:

```
                    else "ask it first with: crate label sync --next"
```

### `u189.M12_pick_remedy_plain_next`

record_answer: the remedy of a pick outside the question names the plain --next again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M12_pick_remedy_plain_next`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`

Old text:

```
                    f"take the identifiers from: crate label sync --next --label "
                    f"{entry.label_id}",
```

New text:

```
                    "take the identifiers from: crate label sync --next",
```

### `u189.M13_walk_remedy_plain_next`

_walk: the unanswerable refusal's remedy names the plain --next and a placeholder label again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M13_walk_remedy_plain_next`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_walk_nobody_can_answer_names_next_label_for_the_label_it_stopped_at`

Old text:

```
                        f"sync --next --label {entry.label_id}, then crate label sync "
                        f"--answer ANSWER --label {entry.label_id}",
```

New text:

```
                        f"sync --next, then crate label sync "
                        f"--answer ANSWER --label NAME",
```

### `u189.M14_pick_no_release_remedy_plain_next`

label_sync: the remedy of --answer pick with no --release names the plain --next again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M14_pick_no_release_remedy_plain_next`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_with_no_release_names_next_label_for_the_label_it_named[Beta Works-'Beta Works']`
  - `tests/test_label_sync.py::test_a_pick_with_no_release_names_next_label_for_the_label_it_named[Kit's Works-"Kit's Works"]`
  - `tests/test_label_sync.py::test_a_pick_with_no_release_names_next_label_for_the_label_it_named[beta-works-'beta-works']`

Old text:

```
                f"--next --label {args.label!r}",
```

New text:

```
                f"--next",
```

### `u189.M15_pick_remedy_unquoted`

label_sync: the pick remedy names the label unquoted, so a name with a space pastes as two words

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M15_pick_remedy_unquoted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_with_no_release_names_next_label_for_the_label_it_named[Beta Works-'Beta Works']`
  - `tests/test_label_sync.py::test_a_pick_with_no_release_names_next_label_for_the_label_it_named[Kit's Works-"Kit's Works"]`
  - `tests/test_label_sync.py::test_a_pick_with_no_release_names_next_label_for_the_label_it_named[beta-works-'beta-works']`

Old text:

```
                f"--next --label {args.label!r}",
```

New text:

```
                f"--next --label {args.label}",
```

### `u189.M16_empty_label_alone_walks`

label_sync: test --label for truth again, so an empty --label alone runs the whole walk

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M16_empty_label_alone_walks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv2]`

Old text:

```
    elif not args.next_question and (args.label is not None or args.releases):
```

New text:

```
    elif not args.next_question and (args.label or args.releases):
```

### `u189.M1_next_label_refused_again`

label_sync: restore the old refusal of --label without --answer, so --next --label is refused and no single label can be asked

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M1_next_label_refused_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`
  - `tests/test_label_sync.py::test_an_answer_with_nothing_waiting_names_next_label_and_following_it_reaches_that_label`
  - `tests/test_label_sync.py::test_next_label_asks_the_named_label_and_leaves_the_one_above_it_unlisted`
  - `tests/test_label_sync.py::test_next_label_for_a_label_nobody_follows_is_refused_before_any_listing[Nobody Works]`
  - `tests/test_label_sync.py::test_next_label_for_a_label_nobody_follows_is_refused_before_any_listing[nobody-works]`
  - `tests/test_label_sync.py::test_next_label_human_output_names_the_one_label`
  - `tests/test_label_sync.py::test_next_label_leaves_another_labels_saved_question_exactly_as_it_was`
  - `tests/test_label_sync.py::test_next_label_prints_a_question_the_plain_next_saved_with_no_catalogue_call`
  - `tests/test_label_sync.py::test_next_label_prints_a_saved_question_again_with_no_catalogue_call`
  - `tests/test_label_sync.py::test_next_label_then_answer_then_next_label_says_nothing_new`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_label_with_nothing_new_says_so_in_one_check`

Old text:

```
    elif not args.next_question and (args.label is not None or args.releases):
```

New text:

```
    elif args.label is not None or args.releases:
```

### `u189.M2_label_alone_not_refused`

label_sync: drop the refusal of --label or --release alone, so they fall through to the interactive walk and name nothing

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M2_label_alone_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv2-go with --answer]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv3-go with --answer]`
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv0]`
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv1]`
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv2]`

Old text:

```
    elif not args.next_question and (args.label is not None or args.releases):
```

New text:

```
    elif False:
```

### `u189.M3_next_release_not_refused`

label_sync: drop the refusal of --next with --release, so the named releases are silently ignored

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M3_next_release_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv6---next would ignore the releases]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv7---next would ignore the releases]`

Old text:

```
    elif args.next_question and args.releases:
```

New text:

```
    elif False:
```

### `u189.M4_empty_name_not_refused`

label_sync: drop the refusal of --next with an empty --label, so a blank name reaches the registry as an unfollowed label

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M4_empty_name_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_label_with_an_empty_name_is_refused_as_no_name_given[   ]`
  - `tests/test_label_sync.py::test_next_label_with_an_empty_name_is_refused_as_no_name_given[]`

Old text:

```
    elif args.next_question and args.label is not None and not args.label.strip():
```

New text:

```
    elif False:
```

### `u189.M5_alone_hint_drops_the_label`

label_sync: reword the --label alone hint to the plain --next, which walks from the top

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M5_alone_hint_drops_the_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv0]`
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv1]`
  - `tests/test_label_sync.py::test_label_or_release_alone_refuses_and_names_next_label[argv2]`

Old text:

```
            "to ask about one label: crate label sync --next --label NAME",
```

New text:

```
            "to ask about one label: crate label sync --next",
```

### `u189.M6_label_not_passed`

label_sync: call _next without the named label, so --next --label walks every label from the top

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M6_label_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`
  - `tests/test_label_sync.py::test_an_answer_with_nothing_waiting_names_next_label_and_following_it_reaches_that_label`
  - `tests/test_label_sync.py::test_next_label_asks_the_named_label_and_leaves_the_one_above_it_unlisted`
  - `tests/test_label_sync.py::test_next_label_for_a_label_nobody_follows_is_refused_before_any_listing[Nobody Works]`
  - `tests/test_label_sync.py::test_next_label_for_a_label_nobody_follows_is_refused_before_any_listing[nobody-works]`
  - `tests/test_label_sync.py::test_next_label_human_output_names_the_one_label`
  - `tests/test_label_sync.py::test_next_label_leaves_another_labels_saved_question_exactly_as_it_was`
  - `tests/test_label_sync.py::test_next_label_prints_a_saved_question_again_with_no_catalogue_call`
  - `tests/test_label_sync.py::test_next_label_then_answer_then_next_label_says_nothing_new`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_label_with_nothing_new_says_so_in_one_check`

Old text:

```
        return _next(ctx, cfg, args.label)
```

New text:

```
        return _next(ctx, cfg)
```

### `u189.M7_unknown_name_not_refused`

_next: resolve the name without refusing, so an unfollowed name walks every label

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M7_unknown_name_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_label_for_a_label_nobody_follows_is_refused_before_any_listing[Nobody Works]`
  - `tests/test_label_sync.py::test_next_label_for_a_label_nobody_follows_is_refused_before_any_listing[nobody-works]`

Old text:

```
    only = _entry_or_refuse(followed, name) if name is not None else None
```

New text:

```
    only = followed.resolve(name) if name is not None else None
```

### `u189.M8_entries_ignore_the_one`

_next: walk every followed label even when one is named

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M8_entries_ignore_the_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 9 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`
  - `tests/test_label_sync.py::test_an_answer_with_nothing_waiting_names_next_label_and_following_it_reaches_that_label`
  - `tests/test_label_sync.py::test_next_label_asks_the_named_label_and_leaves_the_one_above_it_unlisted`
  - `tests/test_label_sync.py::test_next_label_human_output_names_the_one_label`
  - `tests/test_label_sync.py::test_next_label_leaves_another_labels_saved_question_exactly_as_it_was`
  - `tests/test_label_sync.py::test_next_label_prints_a_saved_question_again_with_no_catalogue_call`
  - `tests/test_label_sync.py::test_next_label_then_answer_then_next_label_says_nothing_new`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_label_with_nothing_new_says_so_in_one_check`

Old text:

```
    entries = [only] if only is not None else list(followed.labels.values())
```

New text:

```
    entries = list(followed.labels.values())
```

### `u189.S1_saved_question_relisted`

_next, sample of the unit's existing guards: never reuse a saved question, so every --next lists the label again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `S1_saved_question_relisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_saved_question_is_printed_again_with_no_provider_call`
  - `tests/test_label_sync.py::test_next_label_leaves_another_labels_saved_question_exactly_as_it_was`
  - `tests/test_label_sync.py::test_next_label_prints_a_question_the_plain_next_saved_with_no_catalogue_call`
  - `tests/test_label_sync.py::test_next_label_prints_a_saved_question_again_with_no_catalogue_call`

Old text:

```
            if isinstance(pending, Mapping) and pending.get("releases"):
                question = Question.from_json(pending)
            else:
                listed = _question_for(tools, store, entry, asked_releases(document, entry.label_id))
```

New text:

```
            if False:
                question = Question.from_json(pending)
            else:
                listed = _question_for(tools, store, entry, asked_releases(document, entry.label_id))
```

### `u189.S2_question_not_saved`

_next, sample of the unit's existing guards: print a new question without saving it, so no answer can apply to it

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `S2_question_not_saved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 204 against a baseline of 204
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

### `u238.M10_question_drops_the_split`

_question_for: build the question without the listing's unchecked count

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M10_question_drops_the_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_question_counts_only_the_labels_own_releases_past_its_window`
  - `tests/test_label_sync.py::test_an_unread_listing_still_says_so_beside_the_count_past_the_window`

Old text:

```
            beyond_unchecked=listing.beyond_unchecked,

```

New text:

```
(empty)
```

### `u238.M11_saved_question_drops_the_split`

Question.to_json: save no unchecked count, so a saved question reread says its own as a bound

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M11_saved_question_drops_the_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_question_counts_only_the_labels_own_releases_past_its_window`
  - `tests/test_label_sync.py::test_an_unread_listing_still_says_so_beside_the_count_past_the_window`

Old text:

```
            "beyond_unchecked": self.beyond_unchecked,

```

New text:

```
(empty)
```

### `u238.M7_old_question_read_as_count`

Question.from_json: a question saved before the split reads none as unchecked, so 414 is said as the label's

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M7_old_question_read_as_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_question_saved_before_the_count_was_split_reads_as_a_bound`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[-1]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[9]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[None]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[True]`

Old text:

```
            beyond_unchecked=beyond if unchecked is None else min(beyond, unchecked),
```

New text:

```
            beyond_unchecked=0 if unchecked is None else min(beyond, unchecked),
```

### `u238.M8_bound_said_as_the_labels`

sync_cli._past_window: say the unchecked alone as the label's releases rather than as a bound

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M8_bound_said_as_the_labels`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_question_saved_before_the_count_was_split_reads_as_a_bound`
  - `tests/test_label_sync.py::test_a_saved_split_larger_than_its_figure_is_held_to_the_figure`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[-1]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[9]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[None]`
  - `tests/test_label_sync.py::test_a_saved_split_that_cannot_be_read_reads_as_a_bound[True]`
  - `tests/test_label_sync.py::test_the_phrase_past_the_window_is_a_count_or_a_bound_and_never_zero`

Old text:

```
        said = f"up to {unchecked} more past this run's window, not yet checked"
```

New text:

```
        said = f"{unchecked} more of the label's release(s) past this run's window"
```

### `u238.M9_nothing_line_loses_the_split`

sync_cli._nothing_check: pass no unchecked count, so the nothing new line says every release as the label's

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M9_nothing_line_loses_the_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 319 against a baseline of 319
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_nothing_new_after_an_answer_says_the_count_past_the_window`
  - `tests/test_label_sync.py::test_nothing_new_says_the_count_past_the_window_the_same_way`

Old text:

```
        past = _past_window(listed.listing.beyond, listed.listing.beyond_unchecked)
```

New text:

```
        past = _past_window(listed.listing.beyond, 0)
```

### `u277.M10_next_says_no_canary`

_listing_checks: never say the reverified line, so --next is silent about which release it re-verified

- File: `src/cratekit/label/sync_cli.py`
- Source: `u277.json`, row `M10_next_says_no_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_sync.py`
- Collected: 131 against a baseline of 131
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_provider_crediting_another_label_still_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_turns_the_same_shape_into_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_held_releases_whose_lines_name_another_act_still_refuse`
  - `tests/test_label_canary.py::test_the_record_names_the_release_re_verified_and_what_it_answered`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
    if listing.canary is not None:
```

New text:

```
    if False:
```

### `u278.M24_label_sync_not_narrowed`

label sync: ask and walk spend the reserve

- File: `src/cratekit/label/sync_cli.py`
- Source: `u278.json`, row `M24_label_sync_not_narrowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`

Old text:

```
    if not args.go:
        provider_gate.reading(
```

New text:

```
    if False:
        provider_gate.reading(
```

### `u278.M25_sweep_never_refuses`

label sync: the estimate never refuses

- File: `src/cratekit/label/sync_cli.py`
- Source: `u278.json`, row `M25_sweep_never_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`

Old text:

```
    if calls > left:
```

New text:

```
    if False:
```

### `r798-c.H6_a_returned_release_passes_at_approval`

label approved: judge a release a person returned, so it is held a second time when it is accepted

- File: `src/cratekit/label/approved_cli.py`
- Source: `r798-c.json`, row `H6_a_returned_release_passes_at_approval`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`
- Collected: 195 against a baseline of 195
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_release_held_at_approval_is_returned_by_name_and_listed_the_next_time`
  - `tests/test_label_genre_gate.py::test_a_returned_mark_on_the_payload_alone_is_believed`
  - `tests/test_label_genre_gate.py::test_a_returned_release_is_listed_at_approval_and_not_judged_again`

Old text:

```
        if release.returned:
            continue
```

New text:

```
        if False:
            continue
```

### `r798-d.H7_again_an_owned_release_is_not_asked_about`

label approved: ask the general catalogue about a release the library holds in full. H7 measured again, against the line as the second review left it, where ownership is read off the one resolution of each release

- File: `src/cratekit/label/approved_cli.py`
- Source: `r798-d.json`, row `H7_again_an_owned_release_is_not_asked_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_the_catalogue_is_not_asked_about_a_release_the_library_already_holds`

Old text:

```
        elif owned(release):
```

New text:

```
        elif False:
```

### `u101.G10_ungated_not_reported_in_judged_label`

Drop the ungated branch in a judged label, so a release with no genre is listed silently

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G10_ungated_not_reported_in_judged_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_known_is_listed_with_a_failing_line`
  - `tests/test_label_approved.py::test_tracks_that_disagree_on_the_genre_are_not_judged_and_are_listed`

Old text:

```
            if outcome.ungated is not None:
```

New text:

```
            if False:
```

### `u101.G11_keep_read_as_drop`

Hold on the KEEP verdict instead of DROP

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G11_keep_read_as_drop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_family_exactly_at_the_share_belongs_and_is_listed`
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_genre_the_label_makes_enough_of_is_listed`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`
  - `tests/test_label_approved.py::test_the_default_human_output_names_a_held_release`

Old text:

```
            elif verdict is routing.GateVerdict.DROP and family and outcome.genre:
```

New text:

```
            elif verdict is routing.GateVerdict.KEEP and family and outcome.genre:
```

### `u101.G12_reported_share_not_the_taxonomys`

Report a share the taxonomy did not declare

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G12_reported_share_not_the_taxonomys`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`

Old text:

```
    share = declared.label_gate.out_of_place_share
```

New text:

```
    share = 0.2
```

### `u101.G13_family_count_off_by_one`

Report one more release of the family than there were

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G13_family_count_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`

Old text:

```
families.count(family), classified, share
```

New text:

```
families.count(family) + 1, classified, share
```

### `u101.G14_classified_counts_unjudged`

Count every release in the label as classified, including those with no genre

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G14_classified_counts_unjudged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`

Old text:

```
        classified = sum(1 for genre in genres if genre)
```

New text:

```
        classified = len(genres)
```

### `u101.G17_refusal_silent_on_held`

Drop the held clause from the nothing missing refusal

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G17_refusal_silent_on_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
            + (f" and passed the genre gate ({len(held)} more held by it)" if held else "")
```

New text:

```
            + ""
```

### `u101.G18_no_op_claims_held`

The no op wording ignores held releases and says the library holds everything read

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G18_no_op_claims_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`

Old text:

```
            f"held by it"
            if held
            else
```

New text:

```
            f"held by it"
            if False
            else
```

### `u101.G1_held_is_listed`

Drop the skip, so a release the gate held is resolved, offered and listed anyway

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G1_held_is_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
        if release.item_id in held:
            continue

```

New text:

```
(empty)
```

### `u101.G20_summary_held_empty`

The summary carries no held releases

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G20_summary_held_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`

Old text:

```
        held=[one.to_json() for one in held.values()],
```

New text:

```
        held=[],
```

### `u101.G2_judged_per_release`

Group every release under itself, so each is judged alone and nothing is ever held

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G2_judged_per_release`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`
  - `tests/test_label_approved.py::test_a_held_release_is_never_offered_for_review`
  - `tests/test_label_approved.py::test_a_label_with_a_release_unread_this_run_is_not_judged_and_says_why`
  - `tests/test_label_approved.py::test_a_release_of_an_out_of_place_genre_is_held_by_name_and_not_listed`
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_a_release_with_no_genre_is_not_counted_in_its_labels_share`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_the_default_human_output_names_a_held_release`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return f"release:{release.release_id}"
```

### `u101.G3_all_labels_one_group`

Group every release under one key, so labels are judged against each other

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G3_all_labels_one_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_each_label_is_judged_against_its_own_output`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return "all"
```

### `u101.G4_unlabelled_grouped_together`

Group every release naming no label under one key instead of judging each alone

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G4_unlabelled_grouped_together`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_releases_naming_no_label_are_each_judged_alone`

Old text:

```
    return release.label_id or release.label_name or f"release:{release.release_id}"
```

New text:

```
    return release.label_id or release.label_name or "release:"
```

### `u101.G5_unread_label_judged`

Judge a label even when one of its releases was unread this run

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G5_unread_label_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_label_with_a_release_unread_this_run_is_not_judged_and_says_why`

Old text:

```
        if label in unread:
```

New text:

```
        if label in unread and False:
```

### `u101.G6_unread_from_every_label`

Treat every label as having an unread release whenever any release failed

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G6_unread_from_every_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_release_unread_on_another_label_does_not_stop_this_label_being_judged`
  - `tests/test_label_approved.py::test_nothing_missing_with_one_held_and_one_unread_is_refused_and_says_both`

Old text:

```
        if label in unread:
```

New text:

```
        if unread:
```

### `u101.G7_mixed_is_a_genre`

Rows that disagree yield their first genre instead of none

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G7_mixed_is_a_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_tracks_that_disagree_on_the_genre_are_not_judged_and_are_listed`

Old text:

```
    if len(said) > 1:
```

New text:

```
    if len(said) > 99:
```

### `u101.G8_case_is_a_difference`

Compare genres by exact text, so one genre in two cases reads as mixed

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G8_case_is_a_difference`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_one_genre_in_two_cases_is_one_genre_and_is_judged`

Old text:

```
            said.setdefault(text.casefold(), text)
```

New text:

```
            said.setdefault(text, text)
```

### `u101.G9_mapping_row_unread`

Read the genre by attribute only, so a mapping shaped row reports none

- File: `src/cratekit/label/approved_cli.py`
- Source: `u101.json`, row `G9_mapping_row_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_genre_on_a_mapping_row_is_read_like_one_on_an_object`

Old text:

```
        value = row.get("genre") if isinstance(row, Mapping) else getattr(row, "genre", None)
```

New text:

```
        value = getattr(row, "genre", None)
```

### `u107-c.S19_approved_superseded`

approved_cli._queued: count a superseded item as not yet answered

- File: `src/cratekit/label/approved_cli.py`
- Source: `u107-c.json`, row `S19_approved_superseded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_superseded_item_is_not_counted_as_waiting_by_label_approved`

Old text:

```
        elif item.verdict is not review.Verdict.SUPERSEDED:
```

New text:

```
        else:
```

### `u108-c.G21_listing_skips_already`

approved_cli.list_releases: a track another job already holds is listed again

- File: `src/cratekit/label/approved_cli.py`
- Source: `u108-c.json`, row `G21_listing_skips_already`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_sync_go.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_landing_labels.py`
- Collected: 368 against a baseline of 368
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`

Old text:

```
            elif str(settled.wanted.ref or "").strip() in already:
```

New text:

```
            elif False:
```

### `u108-c.G22_listing_excuse_applies`

approved_cli.list_releases: an excused failure kind still refuses an empty listing

- File: `src/cratekit/label/approved_cli.py`
- Source: `u108-c.json`, row `G22_listing_excuse_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_sync_go.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_landing_labels.py`
- Collected: 368 against a baseline of 368
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_release_gone_from_the_provider_does_not_refuse_every_go_after_it`

Old text:

```
    unexcused = [one for one in failures if one.kind not in excuse]
```

New text:

```
    unexcused = list(failures)
```

### `u75-a.A1_kind_filter`

Drop the kind filter, so an accepted harvested label name, which shares the queue, is read as a release

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A1_kind_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_an_accepted_harvested_label_shares_the_queue_and_is_not_a_release`

Old text:

```
        kinds=(sweep.KIND,),

```

New text:

```
(empty)
```

### `u75-a.A3_nothing_accepted_before_the_catalogue`

Remove the early return, so a queue with nothing accepted resolves the catalogue and spends a login

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A3_nothing_accepted_before_the_catalogue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_nothing_accepted_is_a_no_op_that_never_opens_the_catalogue`

Old text:

```
    if not accepted:
        # ASKED BEFORE THE CATALOGUE IS RESOLVED
```

New text:

```
    if False:
        # ASKED BEFORE THE CATALOGUE IS RESOLVED
```

### `u75-a.A5_only_the_seams_exception_is_gone`

Catch LookupError again instead of the seam's own class, the review's first finding

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A5_only_the_seams_exception_is_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_lookup_error_that_is_not_the_seams_own_is_never_read_as_a_gone_release`

Old text:

```
    except catalogue.ReleaseUnresolvable as exc:
        return _Failed(release, GONE, str(exc))
```

New text:

```
    except LookupError as exc:
        return _Failed(release, GONE, str(exc))
```

### `u75-a.A6_no_identifier_is_not_asked_of_the_provider`

Remove the empty identifier guard, so the provider is asked for a release with no name

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A6_no_identifier_is_not_asked_of_the_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_an_accepted_item_naming_no_release_is_a_named_failure`

Old text:

```
    if not release.release_id:
        return _Failed(release, NO_IDENTIFIER, "the review item names no release identifier")

```

New text:

```
(empty)
```

### `u75-a.A7_each_row_read_alone`

Let one unreadable row escape, which costs the run instead of one line

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A7_each_row_read_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_one_unreadable_row_is_reported_and_the_rest_of_the_release_still_lists`

Old text:

```
        except match.UnreadableList as exc:
            unreadable.append(str(exc))
```

New text:

```
        except ZeroDivisionError as exc:
            unreadable.append(str(exc))
```

### `u75-b.B11_write_failure_is_the_verbs_refusal`

Remove the OSError conversion, so a full disk reaches a person as an internal error

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B11_write_failure_is_the_verbs_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_write_the_disk_refuses_is_the_verbs_refusal_and_not_an_internal_error`

Old text:

```
        except OSError as exc:
            # A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL.
```

New text:

```
        except ZeroDivisionError as exc:
            # A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL.
```

### `u75-b.B1_outage_threshold`

Raise the outage threshold from three to thirty, a realistic slip, so a dead provider is asked about every release

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B1_outage_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_provider_that_stopped_answering_is_not_asked_about_every_release`

Old text:

```
OUTAGE_AFTER = 3
```

New text:

```
OUTAGE_AFTER = 30
```

### `u75-b.B3_only_a_provider_failure_counts`

Count a gone release towards an outage

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B3_only_a_provider_failure_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_gone_release_does_not_count_towards_an_outage`

Old text:

```
            in_a_row = in_a_row + 1 if outcome.kind == PROVIDER else 0
```

New text:

```
            in_a_row = in_a_row + 1
```

### `u75-b.B7_same_recording_listed_once`

Remove the match id dedupe, so a single and its album list one recording twice

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B7_same_recording_listed_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_the_same_recording_on_two_releases_is_listed_once_under_the_first`

Old text:

```
            elif settled.match_id in seen:
                counts["duplicate"] += 1

```

New text:

```
(empty)
```

### `u75-b.B9_name_digests_the_provenance`

Digest the tracks alone, the review's fourth finding, so a corrected year meets the emitter's refusal

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B9_name_digests_the_provenance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_the_list_name_moves_with_anything_the_emitter_would_write`
  - `tests/test_label_approved.py::test_the_same_tracks_with_a_corrected_year_take_a_new_name_and_are_not_refused`

Old text:

```
        "provenance": [
            dataclasses.asdict(provenance[track["id"]]) for track in body["tracks"]
        ],
```

New text:

```
        "provenance": [],
```

### `u75-zeros.B6_missing_and_nothing_listable_refuses`

Remove the refusal for missing tracks none of which carries a provider identifier

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-zeros.json`, row `B6_missing_and_nothing_listable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_missing_tracks_none_of_which_can_be_asked_for_is_refused_and_not_a_no_op`

Old text:

```
    if missing and not listed:
```

New text:

```
    if False:
```

### `r840-a.A1_address_is_the_whole_field`

is_address: search for the address shape anywhere in the field, so a name that merely contains one is asked about and overwritten

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A1_address_is_the_whole_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_name_is_never_read_as_an_address[<provider.artist.Artist object at 0x10b77ec00> (remix)]`
  - `tests/test_label_artists.py::test_a_name_is_never_read_as_an_address[Label Act <provider.artist.Artist object at 0x10b77ec00>]`

Old text:

```
ADDRESS.fullmatch(value.strip()) is not None
```

New text:

```
ADDRESS.search(value.strip()) is not None
```

### `r840-a.A2_a_name_is_not_asked_about`

_listed: drop the address check, so every open label release is read from the provider and rewritten

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A2_a_name_is_not_asked_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_a_second_run_asks_about_nothing_the_first_repaired`
  - `tests/test_label_artists.py::test_an_item_whose_artist_is_a_name_is_not_asked_about`
  - `tests/test_label_artists.py::test_an_item_with_no_artist_at_all_is_not_an_address_and_is_not_said_to_have_one`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`
  - `tests/test_label_artists.py::test_the_provider_is_asked_once_for_each_repaired_item_and_never_for_the_others`

Old text:

```
        if not is_address(item.payload.get("artist")):
            done.counts[ALREADY_FINE] += 1
            continue
        if item.stored_verdict
```

New text:

```
        if item.stored_verdict
```

### `r840-a.A3_unreadable_verdict_is_decided`

_listed: drop the stored verdict check, so an item carrying a verdict this build cannot read is asked about

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A3_unreadable_verdict_is_decided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_item_carrying_a_verdict_this_build_cannot_read_is_left_and_not_asked_about`

Old text:

```
        if item.stored_verdict is not None:
            done.counts[DECIDED] += 1
            continue

```

New text:

```
(empty)
```

### `r840-a.A4_only_label_releases`

_listed: drop the kind from the selection, so another producer's item in the same queue is read as a release

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A4_only_label_releases`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_another_queues_item_reading_an_address_is_not_this_verbs`

Old text:

```
review.Predicate(queue=str(Queue.LABEL_RELEASE), kind=genre_gate.RELEASE_KIND)
```

New text:

```
review.Predicate(queue=str(Queue.LABEL_RELEASE))
```

### `r840-a.A5_no_identifier_is_not_read`

_walk: drop the empty identifier half of the unaddressed check, so an item filed under an empty identifier is asked for and reported as no longer served

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A5_no_identifier_is_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_item_filed_under_an_empty_identifier_is_not_asked_about`

Old text:

```
        if (
            not subject.release_id
            or genre_gate.release_item_id(subject.release_id) != subject.item_id
        ):
```

New text:

```
        if (
            genre_gate.release_item_id(subject.release_id) != subject.item_id
        ):
```

### `r840-a.A6_another_items_release_is_not_read`

_walk: drop the addressing half of the unaddressed check, so an item naming another item's release is given that release's artist

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A6_another_items_release_is_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_item_naming_another_items_release_is_not_given_that_releases_artist`
  - `tests/test_label_artists.py::test_two_items_naming_one_release_are_two_lines_under_two_keys`

Old text:

```
        if (
            not subject.release_id
            or genre_gate.release_item_id(subject.release_id) != subject.item_id
        ):
```

New text:

```
        if (
            not subject.release_id
        ):
```

### `r840-a.A7_catalogue_opened_on_demand`

_walk: open the catalogue before the walk, so a queue with no address in it logs in and can refuse on the credential

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A7_catalogue_opened_on_demand`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_an_empty_queue_is_a_no_op_that_opens_no_catalogue`

Old text:

```
    found: catalogue.Catalogue | None = None
    failed_in_a_row = 0
```

New text:

```
    found: catalogue.Catalogue | None = catalogue.resolve(cfg)
    failed_in_a_row = 0
```

### `r840-a.A8_outage_bound`

_walk: stop after four reads failing in a row and not three

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A8_outage_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_three_reads_failing_in_a_row_stop_the_run_and_say_what_was_left`

Old text:

```
        if failed_in_a_row >= catalogue.READS_FAILED_IN_A_ROW:
            # THE RUN STOPS
```

New text:

```
        if failed_in_a_row > catalogue.READS_FAILED_IN_A_ROW:
            # THE RUN STOPS
```

### `r840-a.A9_an_answer_resets_the_count`

_walk: never reset the count of failed reads, so three scattered failures stop the run as an outage

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-a.json`, row `A9_an_answer_resets_the_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_that_is_gone_does_not_count_towards_an_outage`
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`

Old text:

```
failed_in_a_row = failed_in_a_row + 1 if failed else 0
```

New text:

```
failed_in_a_row = failed_in_a_row + (1 if failed else 0)
```

### `r840-b.B10_unaddressed_is_keyed_by_item`

_Run.record: key a line by its item only when it names no release, so an item naming another item's release shares that release's key

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B10_unaddressed_is_keyed_by_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_two_items_naming_one_release_are_two_lines_under_two_keys`

Old text:

```
            if outcome == UNADDRESSED
            else
```

New text:

```
            if not subject.release_id
            else
```

### `r840-b.B11_left_counts_what_was_not_reached`

_with_counts: count left against every address and not against the items the run set out to read

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B11_left_counts_what_was_not_reached`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_catalogue_that_cannot_be_opened_refuses_and_repairs_nothing`
  - `tests/test_label_artists.py::test_a_release_the_provider_could_not_answer_for_is_left_and_the_run_refuses`
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_an_outage_over_the_last_releases_of_a_run_is_the_same_refusal`
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`
  - `tests/test_label_artists.py::test_three_reads_failing_in_a_row_stop_the_run_and_say_what_was_left`

Old text:

```
    left = listed - len(done.releases)
```

New text:

```
    left = done.addresses - done.counts[REPAIRED]
```

### `r840-b.B1_only_the_seams_exception_is_not_served`

_repair_one: catch LookupError where the seam's own exception is caught, so a client that could not parse a payload is reported as a release that is gone

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B1_only_the_seams_exception_is_not_served`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_lookup_error_that_is_not_the_seams_own_is_unread_and_never_not_served`

Old text:

```
    except catalogue.ReleaseUnresolvable as exc:
```

New text:

```
    except LookupError as exc:
```

### `r840-b.B2_a_refusal_stops_the_run`

_repair_one: drop the CratekitError passthrough, so an expired session is recorded as one unread release and the walk goes on asking

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B2_a_refusal_stops_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`

Old text:

```
        name = found.release_artist(subject.release_id)
    except CratekitError:
        raise
    except catalogue
```

New text:

```
        name = found.release_artist(subject.release_id)
    except catalogue
```

### `r840-b.B3_no_name_never_blanks`

_repair_one: write whatever the provider answered unless it is None, so a release it names no artist for has its address replaced by nothing

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B3_no_name_never_blanks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[   ]`
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[]`

Old text:

```
    name = _text(name)
    if not name:
```

New text:

```
    name = _text(name)
    if name is None:
```

### `r840-b.B4_an_unread_release_refuses`

_walk: refuse only when the outage bound was reached, so a run that left one or two releases unread exits clean

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B4_an_unread_release_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_lookup_error_that_is_not_the_seams_own_is_unread_and_never_not_served`
  - `tests/test_label_artists.py::test_a_release_the_provider_could_not_answer_for_is_left_and_the_run_refuses`

Old text:

```
    if done.counts[UNREAD]:
        # AFTER THE WALK
```

New text:

```
    if done.counts[UNREAD] >= catalogue.READS_FAILED_IN_A_ROW:
        # AFTER THE WALK
```

### `r840-b.B5_decided_meanwhile_is_not_fine`

_write: answer already fine whenever nothing was written, so an item decided during the read is said to have stopped reading an address

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B5_decided_meanwhile_is_not_fine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_decided_while_it_was_being_read_is_not_rewritten`
  - `tests/test_label_artists.py::test_a_release_that_left_review_while_it_was_being_read_is_not_filed_again`

Old text:

```
    return ALREADY_FINE if seen else DECIDED
```

New text:

```
    return ALREADY_FINE
```

### `r840-b.B6_put_right_meanwhile_is_kept`

_write: drop the address check on the payload as it stands, so an artist somebody typed during the read is overwritten by the provider's

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B6_put_right_meanwhile_is_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_artist_put_right_meanwhile_is_not_overwritten`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`

Old text:

```
        if not is_address(current.get("artist")):
            return None
        return {**current, "artist": name}
```

New text:

```
        return {**current, "artist": name}
```

### `r840-b.B7_addresses_are_what_still_read_one`

_Run.addresses: count every outcome, so an item that stopped reading an address, and every item that never did, is counted as one

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B7_addresses_are_what_still_read_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_an_artist_put_right_meanwhile_is_not_overwritten`
  - `tests/test_label_artists.py::test_an_item_whose_artist_is_a_name_is_not_asked_about`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`
  - `tests/test_label_artists.py::test_the_provider_is_asked_once_for_each_repaired_item_and_never_for_the_others`

Old text:

```
        return sum(n for outcome, n in self.counts.items() if outcome != ALREADY_FINE)
```

New text:

```
        return sum(self.counts.values())
```

### `r840-b.B8_only_the_artist_is_rewritten`

_write: write a payload holding the artist alone, so every other field of the item is lost

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B8_only_the_artist_is_rewritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_an_open_item_reading_an_address_is_given_the_name_and_nothing_else_moves`
  - `tests/test_label_artists.py::test_what_a_judging_job_stamped_meanwhile_is_kept`

Old text:

```
        return {**current, "artist": name}
```

New text:

```
        return {"artist": name}
```

### `r840-b.B9_a_refusal_carries_why_each_read_failed`

_Run.record: leave the sentence off the release's row, so a refusal, which carries no check line, says a read failed and not why

- File: `src/cratekit/label/artists_cli.py`
- Source: `r840-b.json`, row `B9_a_refusal_carries_why_each_read_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_the_provider_could_not_answer_for_is_left_and_the_run_refuses`
  - `tests/test_label_artists.py::test_an_open_item_reading_an_address_is_given_the_name_and_nothing_else_moves`

Old text:

```
                "artist": artist,
                "said": said,

```

New text:

```
                "artist": artist,

```

### `u123.H10_year_filter`

Read a release of any year as the dated playlist's

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H10_year_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_date_no_go_took_anything_on_is_refused`
  - `tests/test_label_heard.py::test_a_release_not_in_the_dated_playlist_is_refused_by_name`
  - `tests/test_label_heard.py::test_the_releases_of_a_dated_playlist_are_the_dated_plans_own`

Old text:

```
            if taken_on == day and (catalogue.by_release.get(identity) or ("",))[0] == year
```

New text:

```
            if taken_on == day and identity in catalogue.by_release
```

### `u123.H11_day_filter`

Read a release taken on any day as the dated playlist's

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H11_day_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_date_no_go_took_anything_on_is_refused`
  - `tests/test_label_heard.py::test_the_releases_of_a_dated_playlist_are_the_dated_plans_own`

Old text:

```
            if taken_on == day and (catalogue.by_release.get(identity) or ("",))[0] == year
```

New text:

```
            if (catalogue.by_release.get(identity) or ("",))[0] == year
```

### `u123.H12_newly_excludes_heard`

Count a release already heard as newly heard, so a second run writes

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H12_newly_excludes_heard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_named_release_already_heard_is_said_and_writes_nothing`
  - `tests/test_label_heard.py::test_heard_writes_the_ids_merges_and_removes_and_a_second_run_is_a_no_op`

Old text:

```
    newly = tuple(one for one in target if one not in heard)
```

New text:

```
    newly = tuple(target)
```

### `u123.H13_year_shape`

Accept a two digit year

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H13_year_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_year_or_date_that_is_not_one_is_refused[argv0]`

Old text:

```
_YEAR = re.compile(r"^\d{4}$")
```

New text:

```
_YEAR = re.compile(r"^\d{2,4}$")
```

### `u123.H14_ambiguous_bound`

Let two playlists with one name through as one, mutate the bound

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H14_ambiguous_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_two_playlists_with_the_dated_name_refuse`

Old text:

```
    if len(matching) > 1:
```

New text:

```
    if len(matching) > 2:
```

### `u123.H15_no_year_refusal`

Drop the refusal when there are tracks to add and no year playlist

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H15_no_year_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_folder_with_no_year_playlist_refuses_when_there_is_something_to_add`

Old text:

```
    if not year_id:
        raise _refused(
```

New text:

```
    if False:
        raise _refused(
```

### `u123.H1_outside_refusal`

Drop the refusal of a --release that is not one of the dated playlist's

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H1_outside_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_release_not_in_the_dated_playlist_is_refused_by_name`
  - `tests/test_label_heard.py::test_the_plan_refuses_through_the_engine_as_through_the_verb`

Old text:

```
    if outside:
        raise _refused(
```

New text:

```
    if False:
        raise _refused(
```

### `u123.H2_no_releases_refusal`

Drop the refusal when no go took a release that year on that day

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H2_no_releases_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_date_no_go_took_anything_on_is_refused`

Old text:

```
    releases = releases_of(document, catalogue, year, day)
    if not releases:
```

New text:

```
    releases = releases_of(document, catalogue, year, day)
    if False:
```

### `u123.H3_vouched_before_a_write`

Drop the ledger's vouching before a removal or a take off

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H3_vouched_before_a_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_playlist_the_ledger_does_not_vouch_for_is_refused`

Old text:

```
    if action in (REMOVE, TAKE_OFF) and not ledger.product_made(cfg, dated_id):
```

New text:

```
    if False:
```

### `u123.H4_unheard_tracks_stay`

Take off every track of the named releases, a shared one with an unheard release too

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H4_unheard_tracks_stay`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_track_an_unheard_release_also_carries_stays_on_the_dated_playlist`

Old text:

```
        leaving = tracks_of(target) - tracks_of(unheard)
```

New text:

```
        leaving = tracks_of(target)
```

### `u123.H5_missing_holds_the_removal`

Remove the dated playlist even when a track did not reach the year

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H5_missing_holds_the_removal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_track_the_year_will_not_take_keeps_the_dated_playlist`

Old text:

```
            if done.missing:
                done.kept = True
```

New text:

```
            if False:
                done.kept = True
```

### `u123.H6_heard_recorded`

Never write the heard list

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H6_heard_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_named_release_already_heard_is_said_and_writes_nothing`
  - `tests/test_label_heard.py::test_a_removal_refused_part_way_names_the_adds_marks_nothing_and_a_resume_finishes`
  - `tests/test_label_heard.py::test_a_track_the_year_will_not_take_keeps_the_dated_playlist`
  - `tests/test_label_heard.py::test_heard_writes_the_ids_merges_and_removes_and_a_second_run_is_a_no_op`
  - `tests/test_label_heard.py::test_marking_heard_with_nothing_to_write_on_a_playlist_made_by_hand_is_not_refused`
  - `tests/test_label_heard.py::test_no_dated_playlist_on_the_account_marks_heard_and_touches_nothing`
  - `tests/test_label_heard.py::test_some_releases_heard_take_their_tracks_off_and_the_last_removes_it`

Old text:

```
        done.recorded = record_heard(cfg, planned.label_id, planned.newly)
```

New text:

```
        done.recorded = 0
```

### `u123.H7_year_adds_recorded`

Do not record the merge's adds on the recorded year

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H7_year_adds_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_what_the_merge_adds_to_a_recorded_year_is_recorded_on_it`

Old text:

```
            if planned.year_recorded:
                ledger.record_label_tracks(
```

New text:

```
            if False:
                ledger.record_label_tracks(
```

### `u123.H8_prefixed_year`

Drop the mark's prefixed name from the year fallback

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H8_prefixed_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_year_known_only_by_the_marks_prefixed_name_is_the_year`

Old text:

```
    year_id = year_id or _one_named(inside, year_name, folders.MARK_PREFIX + year_name)
```

New text:

```
    year_id = year_id or _one_named(inside, year_name)
```

### `u123.H9_stray_said`

Never name a dated playlist the ledger records outside the folder

- File: `src/cratekit/label/heard.py`
- Source: `u123.json`, row `H9_stray_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_playlist_the_ledger_records_outside_the_folder_is_said`

Old text:

```
        return replace(base, stray_id=shape.dated.get(name, ""))
```

New text:

```
        return replace(base, stray_id="")
```

### `u243.L11_heard_adds_a_tombstoned_track`

heard.plan: a tombstoned track on the dated playlist is added to the year, round one's blocker

- File: `src/cratekit/label/heard.py`
- Source: `u243.json`, row `L11_heard_adds_a_tombstoned_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_label_heard.py`
- Collected: 68 against a baseline of 68
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_hearing_a_dated_playlist_never_puts_a_removed_track_back`
  - `tests/test_label_tombstoned.py::test_hearing_never_merges_back_a_removed_single`
  - `tests/test_label_tombstoned.py::test_hearing_never_undoes_a_prune_of_a_held_release`

Old text:

```
        add=tuple(one for one in merging if one not in have and one not in taken_away),
```

New text:

```
        add=tuple(one for one in merging if one not in have),
```

### `u243.L13_heard_merges_a_pruned_track`

heard.plan: a track the ledger records as pruned from the year is merged back by hearing

- File: `src/cratekit/label/heard.py`
- Source: `u243.json`, row `L13_heard_merges_a_pruned_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_label_heard.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_hearing_never_undoes_a_prune_of_a_held_release`

Old text:

```
        set(year_record.pruned) if year_record is not None else set()
```

New text:

```
        set()
```

### `r1056.N10_pass_not_required`

build_mark: neither --xml nor --pass required, so a bare mark reaches the handler

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N10_pass_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_the_pass_is_named_by_exactly_one_of_the_file_and_the_name[neither]`

Old text:

```
    proof = parser.add_mutually_exclusive_group(required=True)
```

New text:

```
    proof = parser.add_mutually_exclusive_group(required=False)
```

### `r1056.N1_no_refusal_of_an_unreadable_record`

native_years: read a record this build cannot read as one that filed nothing

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N1_no_refusal_of_an_unreadable_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-bool-tracks]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-bool-year]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-list-of-strings]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-string]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-text-year]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[no-label]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[no-tracks]`

Old text:

```
        if filed is None:
            raise _blocked(
```

New text:

```
        if filed is None:
            filed = frozenset()
        if False:
            raise _blocked(
```

### `r1056.N2_first_landing_only`

native_years: read only the first landing the proof names, so a pass landed twice loses the second's years

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N2_first_landing_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_every_committed_landing_of_the_pass_counts_and_no_other_does`

Old text:

```
    for session_id in proof.landings:
```

New text:

```
    for session_id in proof.landings[:1]:
```

### `r1056.N3_years_from_the_argument`

label_mark: read the native years under the name given on the command line, not the registry's name

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N3_years_from_the_argument`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_label_named_by_its_registry_identifier_is_compared_under_its_name`

Old text:

```
native_years(cfg, native, label)
```

New text:

```
native_years(cfg, native, name)
```

### `r1056.N4_no_landings_in_digest`

_payload: leave the landings out of the native digest, so a landing after the answer is not stale

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N4_no_landings_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_landing_of_the_pass_after_the_answer_makes_it_stale`
  - `tests/test_label_mark_native.py::test_the_gate_digest_names_the_landings`

Old text:

```
        identity["landings"] = list(native.landings)
```

New text:

```
        pass
```

### `r1056.N5_no_reread_before_rename`

label_mark: drop the reread of the native proof before the first rename

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N5_no_reread_before_rename`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_landing_between_the_plan_and_the_first_rename_renames_nothing`

Old text:

```
    if native is not None and native_proof(cfg, pass_name, verb=_VERB, named=_NAMED) != native:
```

New text:

```
    if False:
```

### `r1056.N6_no_nothing_filed_warning`

label_mark: never say a batch filed none of the built years

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N6_no_nothing_filed_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_label_playlists.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_bridge_batch_of_another_label_says_it_filed_nothing_too`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[a-year-never-built]`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[another-label]`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[no-label-filed]`

Old text:

```
    if not filed & {year.year for year in built}:
```

New text:

```
    if False:
```

### `r1056.N7_nothing_filed_against_any_year`

label_mark: warn only when the batch filed no year at all, not none of the built ones

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N7_nothing_filed_against_any_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`, `tests/test_label_playlists.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[a-year-never-built]`

Old text:

```
    if not filed & {year.year for year in built}:
```

New text:

```
    if not filed:
```

### `r1056.N8_shown_pass_bare`

_shown: name the native pass with no word that it landed on the database native tree

- File: `src/cratekit/label/mark_cli.py`
- Source: `r1056.json`, row `N8_shown_pass_bare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_native_pass_marks_exactly_the_years_its_landing_filed`

Old text:

```
            else f"{pass_name}, landed on the database native {native.tree_id!r} tree"
```

New text:

```
            else pass_name
```

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

### `r835-b.M1_only_the_batch_years_marked`

mark_cli._item: a year the landed batch did not file is marked anyway

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-b.json`, row `M1_only_the_batch_years_marked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_year_the_batch_did_not_file_is_left_alone`

Old text:

```
    if year.year not in filed:
        return {
```

New text:

```
    if False:
        return {
```

### `r835-b.M5_deleted_folder_said`

mark_cli.label_mark: a label folder deleted on the account is listed as if it were there, and the read fails every run

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-b.json`, row `M5_deleted_folder_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`

Old text:

```
            if shape.folder_id in remote.folders()
```

New text:

```
            if True
```

### `r835-c.M4_recheck_before_rename_again`

mark_cli.label_mark: a title changed between the plan and the write is renamed anyway

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-c.json`, row `M4_recheck_before_rename_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_title_changed_between_the_plan_and_the_write_is_not_renamed`

Old text:

```
            if now.get(identity) != item["built_as"]:
```

New text:

```
            if False:
```

### `u180.M14_root_refused`

plan: an All Favorites at the playlist root is not refused, so the verb answers over no folder

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M14_root_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_no_favorites_folder_refuses_by_name_and_writes_nothing`

Old text:

```
    if not home.folder_id:
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `u180.M15_digest_is_the_target_order`

identity: the digest covers the set of rows and not their order, so a target that moved keeps its digest

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M15_digest_is_the_target_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_digest_moves_when_the_target_order_moves_and_not_otherwise`

Old text:

```
            "order": [one.row for one in self.children],
```

New text:

```
            "order": sorted(one.row for one in self.children),
```

### `u180.M16_stale_digest_refused`

apply: a digest that moved since the approval is not refused, so an order nobody approved is written

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M16_stale_digest_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_a_folder_that_changed_after_the_approval_is_refused_and_nothing_is_written`

Old text:

```
    if again.digest != approved.digest:
```

New text:

```
    if False:
```

### `u180.M17_confined_seated_position`

order_violations: a seated row is not asked whether it took its planned position

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M17_confined_seated_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[not-made]`

Old text:

```
            or int(row[seq_at] or 0) != slot
        ):
```

New text:

```
        ):
```

### `u180.M18_confined_unplanned_rows`

order_violations: any playlist row may change its position and bookkeeping, planned or not

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M18_confined_unplanned_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[source-moved]`
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[unplanned-move]`

Old text:

```
        allowed = _SEATED_COLUMNS if key in planned else frozenset()
```

New text:

```
        allowed = _SEATED_COLUMNS
```

### `u180.M19_confined_memberships`

order_violations: a membership that changed is not a violation

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M19_confined_memberships`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[membership-changed]`

Old text:

```
        if before.memberships[key] != after.memberships[key]:
```

New text:

```
        if False:
```

### `u180.M20_confined_content`

order_violations: a content row that changed is not a violation

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M20_confined_content`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_an_order_reaching_what_it_did_not_plan_is_a_violation[content-changed]`

Old text:

```
    if before.content != after.content:
        violations.append(
            f"a {rb_writer.CONTENT_TABLE} row changed, and an order touches no track"
```

New text:

```
    if False:
        violations.append(
            f"a {rb_writer.CONTENT_TABLE} row changed, and an order touches no track"
```

### `u180.M21_confinement_called`

apply: the commit is not confined from SQL, so a write beyond the positions lands

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M21_confinement_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_writer_refuses_an_order_that_reached_a_name`

Old text:

```
                assert_order_confined(
                    db,
                    before,
```

New text:

```
                (lambda *a, **k: None)(
                    db,
                    before,
```

### `u180.M22_read_back_compares`

_read_back: the folder read back is never compared with the plan, so a clean answer is given over any order

- File: `src/cratekit/favorites/order.py`
- Source: `u180.json`, row `M22_read_back_compares`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_order.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_order.py::test_the_read_back_names_a_folder_that_does_not_read_in_the_planned_order`

Old text:

```
    if found == wanted:
        return ()
```

New text:

```
    if True:
        return ()
```

### `r381-b.M14_follow_all_renames`

marks follows every recorded move, including one whose old identifier is held again

- File: `src/cratekit/label/marks.py`
- Source: `r381-b.json`, row `M14_follow_all_renames`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_slug.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_stored_move_whose_old_identifier_is_held_is_not_followed`

Old text:

```
        renamed = registry.RegistryStore().load().live_renames()
```

New text:

```
        renamed = registry.RegistryStore().load().renamed
```

### `r381.M13_follow_overwrites`

marks follow overwrites a year already held under the new identifier

- File: `src/cratekit/label/marks.py`
- Source: `r381.json`, row `M13_follow_overwrites`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_slug.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_year_already_held_under_the_new_identifier_is_not_overwritten`

Old text:

```
        if old in records and new not in records:
```

New text:

```
        if old in records:
```

### `r381.M15_read_does_not_persist`

read answers the followed year and never writes the move

- File: `src/cratekit/label/marks.py`
- Source: `r381.json`, row `M15_read_does_not_persist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_slug.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`

Old text:

```
                if _follow(held):
                    _write(cfg, held)
```

New text:

```
                if _follow(held):
                    pass
```

### `r381.M16_advance_does_not_follow`

advance writes without following, so another label's advance leaves the old key

- File: `src/cratekit/label/marks.py`
- Source: `r381.json`, row `M16_advance_does_not_follow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_slug.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_an_advance_of_another_label_carries_the_migrated_year_along`

Old text:

```
        _follow(records)
        records[label_id] = recorded
```

New text:

```
        records[label_id] = recorded
```

### `r381.M17_read_no_follow`

read never follows, so a migrated label reads no year

- File: `src/cratekit/label/marks.py`
- Source: `r381.json`, row `M17_read_no_follow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_slug.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`

Old text:

```
    records = _load(cfg)
    if _follow(records):
```

New text:

```
    records = _load(cfg)
    if False:
```

### `r798-b.G1_an_unread_answer_holds_nothing`

published_words: read on past an answer that could not be read, so words read before a refusal still hold the release

- File: `src/cratekit/label/gate.py`
- Source: `r798-b.json`, row `G1_an_unread_answer_holds_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`, `tests/test_label_offer_window.py`, `tests/test_label_workers.py`
- Collected: 316 against a baseline of 316
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_catalogue_that_refuses_after_a_would_be_hold_holds_nothing`
  - `tests/test_label_genre_gate.py::test_an_answer_that_could_not_be_read_stops_the_asking[blocked]`
  - `tests/test_label_genre_gate.py::test_an_answer_that_could_not_be_read_stops_the_asking[parse-break]`
  - `tests/test_label_genre_gate.py::test_an_answer_that_could_not_be_read_stops_the_asking[unreachable]`

Old text:

```
        if said.answer in published.UNREAD:
            return Words((), said.answer, said.note)
```

New text:

```
        if False:
            return Words((), said.answer, said.note)
```

### `r798-b.G2_a_would_be_hold_is_asked_about_again`

published_words: stop at the first track that publishes a genre whatever the caller needs, so a hold rests on one track's album

- File: `src/cratekit/label/gate.py`
- Source: `r798-b.json`, row `G2_a_would_be_hold_is_asked_about_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`, `tests/test_label_offer_window.py`, `tests/test_label_workers.py`
- Collected: 316 against a baseline of 316
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_catalogue_that_refuses_after_a_would_be_hold_holds_nothing`
  - `tests/test_label_genre_gate.py::test_a_release_is_held_only_when_every_track_asked_agrees`
  - `tests/test_label_genre_gate.py::test_a_release_that_would_be_held_is_asked_about_again_before_it_is`

Old text:

```
    settled = enough if enough is not None else bool
```

New text:

```
    settled = bool
```

### `r815-a.G1_the_asking_gives_up_at_the_bound`

Asking.given_up: one release later than the bound

- File: `src/cratekit/label/gate.py`
- Source: `r815-a.json`, row `G1_the_asking_gives_up_at_the_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_an_unreachable_catalogue_is_given_up_on_once_for_the_whole_sweep`
  - `tests/test_label_genre_gate.py::test_three_releases_unread_in_a_row_end_the_asking_and_an_answer_resets_it`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`

Old text:

```
        return self._unread_in_a_row >= UNREAD_IN_A_ROW
```

New text:

```
        return self._unread_in_a_row > UNREAD_IN_A_ROW
```

### `u123.C1_declined_writes_nothing`

Write on any answer, not only apply

- File: `src/cratekit/label/heard_cli.py`
- Source: `u123.json`, row `C1_declined_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_declined_nothing_is_written`

Old text:

```
    if option != "apply" or not planned.writes:
```

New text:

```
    if not planned.writes:
```

